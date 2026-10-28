"""AgentKit connection methods, reached as ``client.actions.create_connection(...)`` and friends.

These are new methods on ``client.actions``. Create, get, list and update call the AgentKit-only
connection RPCs (``CreateAppConnection``, ``GetAppConnection``, ``ListAppConnectionSummaries``,
``UpdateAppConnection``). Delete calls the existing environment connection RPC.

``update_connection`` sends only what you pass: the server merges it into the stored settings. Over
gRPC the server clears a list or map only when it arrives empty *and* its path is named in
``update_mask``, so this module adds the path for every list or map you pass as ``[]`` / ``{}``.
"""
import re
from typing import List, Optional, Tuple

from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.wrappers_pb2 import BoolValue, StringValue

from scalekit.actions.connections import errors
from scalekit.actions.connections.models import (
    AgentKitConnection,
    AgentKitConnectionList,
    AuthMode,
    GoogleDWDSettings,
    OAuthSettings,
    ProviderConfigurations,
    connection_from_proto,
    summary_from_proto,
)
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitConflictException,
    ScalekitForbiddenException,
    ScalekitGatewayTimeoutException,
    ScalekitNotFoundException,
    ScalekitServerException,
    ScalekitServiceUnavailableException,
    ScalekitTooManyRequestsException,
    ScalekitUnauthorizedException,
)
from scalekit.v1.connections import connections_pb2 as pb

_CONNECTION_ID = re.compile(r"^conn_\d+$")

_OAUTH_STRINGS = (
    "client_id", "client_secret", "access_type", "prompt", "token_access_type",
    "authorize_uri", "token_uri", "user_info_uri",
)
_OAUTH_BOOLS = ("use_scalekit_creds", "pkce_enabled", "scope_selection_allowed")
_PROVIDER_STRINGS = (
    "provider_domain", "slack_connection_type", "googleads_developer_token", "microsoft_tenant_id",
    "trello_app_name", "smart_fhir_aud", "smart_fhir_domain",
)


# ---------------------------------------------------------------------------
# error mapping
# ---------------------------------------------------------------------------

def _text(exc: BaseException) -> str:
    return (getattr(exc, "message", None) or str(exc) or "").strip()


def _field_violations(exc: BaseException) -> str:
    """Field-level detail the server attaches to a generic "Validation error", as ``field: reason``."""
    parts = []
    for detail in getattr(exc, "_unpacked_details", None) or []:
        info = getattr(detail, "validation_error_info", None)
        for violation in getattr(info, "field_violations", None) or []:
            field = violation.field.removeprefix("connection.")
            parts.append(f"{field}: {violation.description}" if field else violation.description)
    return "; ".join(parts)


def _server_code(exc: BaseException) -> str:
    return (getattr(exc, "error_code", None) or "").upper()


_UNAVAILABLE = (ScalekitServiceUnavailableException, ScalekitGatewayTimeoutException)


def _map_error(exc: ScalekitServerException, step: str, *, writes: bool) -> errors.AgentKitConnectionError:
    """Map a server error. ``writes`` marks calls that may have been applied before they failed."""
    msg = _text(exc)
    violations = _field_violations(exc)
    if violations:
        msg = f"{msg}: {violations}" if msg else violations
    code = _server_code(exc)
    lowered = msg.lower()
    if isinstance(exc, ScalekitNotFoundException):
        return errors.ConnectionNotFoundError(msg or "Connection not found.", step=step, cause=exc)
    if isinstance(exc, (ScalekitUnauthorizedException, ScalekitForbiddenException)):
        return errors.NotAuthorizedError(
            "The API credentials are not allowed to use connections. Check the client id, secret and permissions.",
            step=step, cause=exc)
    if isinstance(exc, _UNAVAILABLE):
        if writes:
            return errors.OutcomeUnknownError(
                "The request was sent but the service did not answer in time. The change may or may not have "
                "been applied. Read the connection to check.", step=step, retryable=True, cause=exc)
        return errors.ConnectionUnavailableError(
            "The service is unavailable or timed out. Nothing was changed; try again.",
            step=step, retryable=True, cause=exc)
    if isinstance(exc, ScalekitTooManyRequestsException):
        return errors.ConnectionUnavailableError(
            "Too many requests. Nothing was changed; try again later.", step=step, retryable=True, cause=exc)
    if "INVALID_RESOURCE_IDENTIFIER" in code:
        return errors.InvalidConnectionIdError(msg or "The connection id is not valid.", step=step, cause=exc)
    if code in ("CONNECTION_ACCOUNT_EXISTS_FOR_CONNECTION", "CONNECTION_REFERENCED_BY_MCP_CONFIG") \
            or "connected accounts" in lowered or "mcp configurations" in lowered:
        return errors.ConnectionInUseError(msg or "The connection is still in use.", step=step, cause=exc)
    if isinstance(exc, ScalekitConflictException) or code in ("DUPLICATE_IDENTIFIER", "RESTRICTED_CONNECTION_NAME") \
            or "is already used" in lowered or "is reserved" in lowered:
        return errors.ConnectionNameConflictError(
            msg or "The connection name is already used or reserved.", step=step, cause=exc)
    if isinstance(exc, ScalekitBadRequestException):
        if "several auth types" in lowered:
            return errors.AmbiguousAuthTypeError(msg, step=step, cause=exc)
        if lowered.startswith("connector") and "not found" in lowered:
            return errors.ProviderNotFoundError(msg, step=step, cause=exc)
        return errors.InvalidConfigurationError(msg or "The server rejected the request.", step=step, cause=exc)
    if writes:
        return errors.ConnectionWriteError(msg or "The server could not apply the change.", step=step, cause=exc)
    return errors.ConnectionReadError(msg or "The connection could not be read.", step=step, cause=exc)


def _invalid(message: str) -> errors.InvalidConfigurationError:
    return errors.InvalidConfigurationError(message, step="validate")


# ---------------------------------------------------------------------------
# request builders
# ---------------------------------------------------------------------------

def _auth_mode_value(auth_mode) -> Optional[int]:
    if auth_mode is None:
        return None
    name = auth_mode.value if isinstance(auth_mode, AuthMode) else str(auth_mode).strip().upper()
    if name not in ("USER", "ORG_WIDE"):
        raise _invalid("auth_mode must be AuthMode.USER or AuthMode.ORG_WIDE.")
    return pb.ConnectionAuthMode.Value(name)


def _build_oauth(settings: OAuthSettings) -> Tuple[pb.AppOAuthConfig, List[str]]:
    """Build the oauth_config patch and the mask paths for lists and maps sent empty."""
    cfg = pb.AppOAuthConfig()
    cleared: List[str] = []
    for name in _OAUTH_STRINGS:
        value = getattr(settings, name)
        if value is not None:
            getattr(cfg, name).CopyFrom(StringValue(value=value))
    for name in _OAUTH_BOOLS:
        value = getattr(settings, name)
        if value is not None:
            getattr(cfg, name).CopyFrom(BoolValue(value=value))
    for name in ("scopes", "required_scopes", "required_optional_scopes"):
        values = getattr(settings, name)
        if values is not None:
            getattr(cfg, name).extend(values)
            if not values:
                cleared.append(f"oauth_config.{name}")
    if settings.optional_scopes is not None:
        cfg.optional_scopes.SetInParent()
        if settings.optional_scopes.field_name is not None:
            cfg.optional_scopes.field_name = settings.optional_scopes.field_name
        if settings.optional_scopes.scopes is not None:
            cfg.optional_scopes.scopes.extend(settings.optional_scopes.scopes)
            if not settings.optional_scopes.scopes:
                cleared.append("oauth_config.optional_scopes.scopes")
    if settings.token_endpoint_auth_method is not None:
        cfg.token_endpoint_auth_method = pb.AppOAuthConfig.TokenEndpointAuthMethod.Value(
            settings.token_endpoint_auth_method.value)
    if settings.extra_authorize_params is not None:
        cfg.extra_authorize_params.update(settings.extra_authorize_params)
        if not settings.extra_authorize_params:
            cleared.append("oauth_config.extra_authorize_params")
    return cfg, cleared


def _build_dwd(settings: GoogleDWDSettings) -> Tuple[pb.GoogleDWDConfig, List[str]]:
    cfg = pb.GoogleDWDConfig()
    cleared: List[str] = []
    for name in ("service_account_json", "token_uri"):
        value = getattr(settings, name)
        if value is not None:
            getattr(cfg, name).CopyFrom(StringValue(value=value))
    if settings.scope_selection_allowed is not None:
        cfg.scope_selection_allowed.CopyFrom(BoolValue(value=settings.scope_selection_allowed))
    for name in ("scopes", "required_scopes"):
        values = getattr(settings, name)
        if values is not None:
            getattr(cfg, name).extend(values)
            if not values:
                cleared.append(f"google_dwd_config.{name}")
    return cfg, cleared


def _build_provider_configurations(settings: ProviderConfigurations) -> pb.AppProviderConfigurations:
    cfg = pb.AppProviderConfigurations()
    for name in _PROVIDER_STRINGS:
        value = getattr(settings, name)
        if value is not None:
            setattr(cfg, name, value)
    return cfg


# ---------------------------------------------------------------------------
# service
# ---------------------------------------------------------------------------

class ConnectionActions:
    """Implements the connection methods; ``ActionClient`` delegates to it."""

    def __init__(self, core_client, connection_client) -> None:
        self._core = core_client
        self._conn = connection_client

    @property
    def _stub(self):
        return self._conn.connection_service

    # -- helpers ----------------------------------------------------------

    def _call(self, rpc, request, step: str, *, writes: bool, **kwargs):
        try:
            return self._core.grpc_exec(rpc.with_call, request, **kwargs)[0]
        except ScalekitServerException as exc:
            raise _map_error(exc, step, writes=writes) from exc

    def _resolve_id(self, connection_name: Optional[str], connection_id: Optional[str]) -> str:
        """Return the connection id for a name or id. A name costs one read."""
        if connection_id and connection_name:
            raise ValueError("Pass connection_name or connection_id, not both.")
        if connection_id:
            if not _CONNECTION_ID.match(connection_id.strip()):
                raise errors.InvalidConnectionIdError(
                    "connection_id is not a valid connection ID; connection IDs look like conn_...", step="resolve")
            return connection_id.strip()
        if not connection_name or not connection_name.strip():
            raise ValueError("connection_name or connection_id is required.")
        return self.get_connection(connection_name).id

    # -- create / get / list ---------------------------------------------

    def create_connection(
        self,
        provider: str,
        connection_name: Optional[str] = None,
        auth_mode: Optional[AuthMode] = None,
        provider_domain: Optional[str] = None,
    ) -> AgentKitConnection:
        if not provider or not provider.strip():
            raise ValueError("provider is required, for example 'gmail'.")
        body = pb.CreateAppConnection(provider=provider.strip())
        if connection_name is not None:
            body.connection_name = connection_name
        mode = _auth_mode_value(auth_mode)
        if mode is not None:
            body.auth_mode = mode
        if provider_domain is not None:
            body.provider_configurations.provider_domain = provider_domain
        # Never retried on unavailable: the first attempt may have created the connection.
        resp = self._call(
            self._stub.CreateAppConnection, pb.CreateAppConnectionRequest(connection=body),
            "create", writes=True, retry_on_unavailable=False)
        return connection_from_proto(resp.connection)

    def get_connection(
        self, connection_name: Optional[str] = None, *, connection_id: Optional[str] = None
    ) -> AgentKitConnection:
        identifier = connection_id if connection_id else connection_name
        if connection_id and connection_name:
            raise ValueError("Pass connection_name or connection_id, not both.")
        if not identifier or not identifier.strip():
            raise ValueError("connection_name or connection_id is required.")
        resp = self._call(
            self._stub.GetAppConnection, pb.GetAppConnectionRequest(connection_identifier=identifier.strip()),
            "read", writes=False)
        return connection_from_proto(resp.connection)

    def list_app_connections(
        self,
        provider: Optional[str] = None,
        query: Optional[str] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> AgentKitConnectionList:
        request = pb.ListAppConnectionSummariesRequest()
        if provider:
            request.provider = provider
        if query:
            request.query = query
        if page_size:
            request.page_size = page_size
        if page_token:
            request.page_token = page_token
        resp = self._call(self._stub.ListAppConnectionSummaries, request, "read", writes=False)
        return AgentKitConnectionList(
            connections=[summary_from_proto(item) for item in resp.connections],
            next_page_token=resp.next_page_token,
            prev_page_token=resp.prev_page_token,
            total_size=resp.total_size,
        )

    # -- update -----------------------------------------------------------

    def update_connection(
        self,
        connection_name: Optional[str] = None,
        *,
        connection_id: Optional[str] = None,
        new_name: Optional[str] = None,
        oauth: Optional[OAuthSettings] = None,
        google_dwd: Optional[GoogleDWDSettings] = None,
        provider_configurations: Optional[ProviderConfigurations] = None,
    ) -> AgentKitConnection:
        groups = [g for g in (oauth, google_dwd) if g is not None]
        if len(groups) > 1:
            raise _invalid("Send only one of oauth or google_dwd.")
        if not groups and provider_configurations is None and new_name is None:
            raise _invalid("Nothing to update: pass oauth, google_dwd, provider_configurations or new_name.")

        body = pb.AppConnectionUpdate()
        mask: List[str] = []
        if oauth is not None:
            cfg, cleared = _build_oauth(oauth)
            body.oauth_config.CopyFrom(cfg)
            mask += cleared
        if google_dwd is not None:
            cfg, cleared = _build_dwd(google_dwd)
            body.google_dwd_config.CopyFrom(cfg)
            mask += cleared
        if provider_configurations is not None:
            body.provider_configurations.CopyFrom(_build_provider_configurations(provider_configurations))
        if new_name is not None:
            body.connection_name = new_name

        cid = self._resolve_id(connection_name, connection_id)
        request = pb.UpdateAppConnectionRequest(connection_id=cid, connection=body)
        if mask:
            request.update_mask.CopyFrom(FieldMask(paths=mask))
        # An update is a partial merge, so repeating it after a timeout is safe.
        resp = self._call(self._stub.UpdateAppConnection, request, "update", writes=True)
        return connection_from_proto(resp.connection)

    # -- delete (existing environment RPC) ---------------------------------

    def delete_connection(
        self, connection_name: Optional[str] = None, *, connection_id: Optional[str] = None
    ) -> None:
        cid = self._resolve_id(connection_name, connection_id)
        self._call(
            self._stub.DeleteEnvironmentConnection, pb.DeleteEnvironmentConnectionRequest(connection_id=cid),
            "delete", writes=True, retry_on_unavailable=False)

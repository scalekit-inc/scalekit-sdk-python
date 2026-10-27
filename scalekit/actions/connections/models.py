"""Typed inputs and outputs for the connection methods on ``client.actions``.

Inputs follow one rule: ``None`` means "leave this field unchanged". A list or map passed empty
(``[]`` or ``{}``) clears the stored one. Only AgentKit settings are exposed; login (SaaSKit)
settings are not.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from scalekit.v1.connections.connections_pb2 import (
    AppConnection,
    AppConnectionSummary,
    ConnectionAuthMode,
    ConnectionType,
)


class AuthMode(str, Enum):
    """How end users authorize a connection. Chosen at creation and cannot be changed afterwards."""

    USER = "USER"  # each end user authorizes their own credential (default)
    ORG_WIDE = "ORG_WIDE"  # one admin-authorized credential is shared; each user still consents


class TokenEndpointAuthMethod(str, Enum):
    """How Scalekit authenticates to the provider's token endpoint."""

    NONE = "NONE"
    BASIC_AUTH = "BASIC_AUTH"  # client_secret_basic
    REQUEST_BODY = "REQUEST_BODY"  # client_secret_post
    DEFAULT = "DEFAULT"  # clears the stored value and lets the platform pick


class _Input(BaseModel):
    # Reject unknown keyword arguments so a typo fails loudly instead of being ignored.
    model_config = ConfigDict(extra="forbid")


class OptionalScopes(_Input):
    """The provider's second scope bucket (for example Slack ``user_scope``)."""

    field_name: Optional[str] = None  # without it the scopes are stored but dropped at sign-in
    scopes: Optional[List[str]] = None  # replaces the stored list; ``[]`` clears it


class OAuthSettings(_Input):
    """Settings for OAuth-style connections. Every field is optional; ``None`` leaves it unchanged."""

    # credentials
    client_id: Optional[str] = None
    client_secret: Optional[str] = None  # write-only; returned masked
    use_scalekit_creds: Optional[bool] = None  # sending your own client_id/secret turns this off unless set
    # scopes (a non-empty list replaces the stored one; [] clears it)
    scopes: Optional[List[str]] = None
    scope_selection_allowed: Optional[bool] = None
    required_scopes: Optional[List[str]] = None  # must be a subset of scopes
    required_optional_scopes: Optional[List[str]] = None  # must be a subset of optional_scopes.scopes
    optional_scopes: Optional[OptionalScopes] = None
    # provider options
    access_type: Optional[str] = None
    prompt: Optional[str] = None  # "" means no prompt is sent to the provider
    token_access_type: Optional[str] = None
    # advanced
    pkce_enabled: Optional[bool] = None
    token_endpoint_auth_method: Optional[TokenEndpointAuthMethod] = None
    # added as given to the provider's authorize URL when you use your own credentials; {} clears it
    extra_authorize_params: Optional[Dict[str, str]] = None
    # URLs (filled from the provider; set only for custom connectors)
    authorize_uri: Optional[str] = None
    token_uri: Optional[str] = None
    user_info_uri: Optional[str] = None


class GoogleDWDSettings(_Input):
    """Settings for Google domain-wide delegation (``GOOGLE_DWD``) connections."""

    service_account_json: Optional[str] = None  # the key file as a string; write-only
    scopes: Optional[List[str]] = None
    scope_selection_allowed: Optional[bool] = None
    required_scopes: Optional[List[str]] = None
    token_uri: Optional[str] = None


class ProviderConfigurations(_Input):
    """Settings only some connectors use. A key sent to the wrong connector is a 400.

    ``provider_domain`` is create-only: pass it to ``create_connection(provider_domain=...)``. Sending it
    to ``update_connection`` is refused by the server (``InvalidConfigurationError``).
    """

    provider_domain: Optional[str] = None  # regional connectors only; never returned
    slack_connection_type: Optional[str] = None  # "BOT" or "USER"
    googleads_developer_token: Optional[str] = None  # masked; cannot be cleared once set
    microsoft_tenant_id: Optional[str] = None
    trello_app_name: Optional[str] = None
    smart_fhir_aud: Optional[str] = None
    smart_fhir_domain: Optional[str] = None


class OAuthSettingsView(OAuthSettings):
    """OAuth settings as returned by the server. Secrets are masked (``****1234``)."""

    model_config = ConfigDict(extra="allow")

    redirect_uri: Optional[str] = None  # register this with the provider; read-only
    is_cimd: Optional[bool] = None  # read-only


class GoogleDWDSettingsView(GoogleDWDSettings):
    model_config = ConfigDict(extra="allow")


class AgentKitConnectionSummary(BaseModel):
    """One row of ``list_connections``."""

    id: str
    connection_name: str
    provider: str
    type: str
    auth_mode: str
    created_at: Optional[datetime] = None


class AgentKitConnectionList(BaseModel):
    connections: List[AgentKitConnectionSummary]
    next_page_token: str = ""
    prev_page_token: str = ""
    total_size: int = 0


class AgentKitConnection(BaseModel):
    """An AgentKit connection with its settings.

    The new APIs do not report whether a connection is enabled.
    """

    id: str
    connection_name: str
    provider: str
    type: str
    auth_mode: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    connection_mcp_url: Optional[str] = None  # present on get, when the environment exposes it
    provider_configurations: Optional[ProviderConfigurations] = None
    oauth: Optional[OAuthSettingsView] = None
    google_dwd: Optional[GoogleDWDSettingsView] = None
    static: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# proto -> model conversion
# ---------------------------------------------------------------------------

def _wrapped(message, field: str):
    """Value of a wrapper-typed (StringValue/BoolValue) field, or None when it is not set."""
    return getattr(message, field).value if message.HasField(field) else None


def _timestamp(message, field: str) -> Optional[datetime]:
    if message.HasField(field):
        return getattr(message, field).ToDatetime(tzinfo=timezone.utc)
    return None


def _oauth_view(cfg) -> OAuthSettingsView:
    from scalekit.v1.connections.connections_pb2 import AppOAuthConfig

    optional = None
    if cfg.HasField("optional_scopes"):
        optional = OptionalScopes(
            field_name=cfg.optional_scopes.field_name or None,
            scopes=list(cfg.optional_scopes.scopes),
        )
    method = cfg.token_endpoint_auth_method
    return OAuthSettingsView(
        client_id=_wrapped(cfg, "client_id"),
        client_secret=_wrapped(cfg, "client_secret"),
        use_scalekit_creds=_wrapped(cfg, "use_scalekit_creds"),
        scopes=list(cfg.scopes),
        scope_selection_allowed=_wrapped(cfg, "scope_selection_allowed"),
        required_scopes=list(cfg.required_scopes),
        required_optional_scopes=list(cfg.required_optional_scopes),
        optional_scopes=optional,
        access_type=_wrapped(cfg, "access_type"),
        prompt=_wrapped(cfg, "prompt"),
        token_access_type=_wrapped(cfg, "token_access_type"),
        pkce_enabled=_wrapped(cfg, "pkce_enabled"),
        token_endpoint_auth_method=(
            TokenEndpointAuthMethod(AppOAuthConfig.TokenEndpointAuthMethod.Name(method))
            if method != AppOAuthConfig.TOKEN_ENDPOINT_AUTH_METHOD_UNSPECIFIED
            else None
        ),
        extra_authorize_params=dict(cfg.extra_authorize_params),
        authorize_uri=_wrapped(cfg, "authorize_uri"),
        token_uri=_wrapped(cfg, "token_uri"),
        user_info_uri=_wrapped(cfg, "user_info_uri"),
        redirect_uri=cfg.redirect_uri or None,
        is_cimd=_wrapped(cfg, "is_cimd"),
    )


def _dwd_view(cfg) -> GoogleDWDSettingsView:
    return GoogleDWDSettingsView(
        service_account_json=_wrapped(cfg, "service_account_json"),
        scopes=list(cfg.scopes),
        scope_selection_allowed=_wrapped(cfg, "scope_selection_allowed"),
        required_scopes=list(cfg.required_scopes),
        token_uri=_wrapped(cfg, "token_uri"),
    )


def _provider_configurations_view(cfg) -> Optional[ProviderConfigurations]:
    # provider_domain is create-only and never returned.
    view = ProviderConfigurations(
        slack_connection_type=cfg.slack_connection_type or None,
        googleads_developer_token=cfg.googleads_developer_token or None,
        microsoft_tenant_id=cfg.microsoft_tenant_id or None,
        trello_app_name=cfg.trello_app_name or None,
        smart_fhir_aud=cfg.smart_fhir_aud or None,
        smart_fhir_domain=cfg.smart_fhir_domain or None,
    )
    return view if view.model_dump(exclude_none=True) else None


def connection_from_proto(conn: AppConnection) -> AgentKitConnection:
    """Convert a server ``AppConnection`` message into the typed model."""
    from google.protobuf.json_format import MessageToDict

    which = conn.WhichOneof("settings")
    return AgentKitConnection(
        id=conn.id,
        connection_name=conn.connection_name,
        provider=conn.provider,
        type=ConnectionType.Name(conn.type),
        auth_mode=ConnectionAuthMode.Name(conn.auth_mode),
        created_at=_timestamp(conn, "create_time"),
        updated_at=_timestamp(conn, "update_time"),
        connection_mcp_url=conn.connection_mcp_url or None,
        provider_configurations=(
            _provider_configurations_view(conn.provider_configurations)
            if conn.HasField("provider_configurations") else None
        ),
        oauth=_oauth_view(conn.oauth_config) if which == "oauth_config" else None,
        google_dwd=_dwd_view(conn.google_dwd_config) if which == "google_dwd_config" else None,
        static=(
            MessageToDict(conn.static_config.static_config) if which == "static_config" else None
        ),
    )


def summary_from_proto(item: AppConnectionSummary) -> AgentKitConnectionSummary:
    return AgentKitConnectionSummary(
        id=item.id,
        connection_name=item.connection_name,
        provider=item.provider,
        type=ConnectionType.Name(item.type),
        auth_mode=ConnectionAuthMode.Name(item.auth_mode),
        created_at=_timestamp(item, "create_time"),
    )

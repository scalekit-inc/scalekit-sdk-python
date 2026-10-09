import enum
from datetime import timedelta
from typing import List, Optional, overload

import grpc
from google.protobuf.duration_pb2 import Duration

from scalekit.core import CoreClient
from scalekit.v1.mcp.mcp_pb2 import *
from scalekit.v1.mcp.mcp_pb2_grpc import McpServiceStub


class _Unset(enum.Enum):
    """Type of ``_UNSET``: marks an argument the caller did not pass."""

    UNSET = enum.auto()


_UNSET = _Unset.UNSET


def _check_connection_token_args(
    mcp_config_id: str | None | _Unset,
    connection_name: str,
    identifier: str | None,
) -> str:
    """Check the arguments of a connection session token before any request.

    Only the connection form is checked here: the MCP configuration form keeps
    the checks each facade had before ``connection_name`` existed.

    Returns:
        The identifier, known to be non-empty.

    Raises:
        ValueError: ``mcp_config_id`` is also given, ``connection_name`` is
            empty, or ``identifier`` is missing or empty.
    """
    if mcp_config_id is not _UNSET and mcp_config_id is not None:
        raise ValueError(
            "Pass either mcp_config_id or connection_name, not both: a session token "
            "is for one MCP configuration or for one connection's MCP server"
        )
    if not connection_name:
        raise ValueError("connection_name must not be empty")
    if not identifier:
        raise ValueError("identifier is required")
    return identifier


class McpClient:
    """Class definition for MCP Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for MCP Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.mcp_service = McpServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_configs(
            self,
            page_size: Optional[int] = None,
            page_token: Optional[str] = None,
            filter_id: Optional[str] = None,
            filter_provider: Optional[str] = None,
            filter_name: Optional[str] = None,
            filter_mcp_server_url: Optional[str] = None,
            search: Optional[str] = None,
    ) -> ListMcpConfigsResponse:
        """
        Method to list MCP Configurations with optional filters

        :param page_size              : Number of items per page
        :type                         : ``` int ```
        :param page_token             : Token for the page to retrieve
        :type                         : ``` str ```
        :param filter_id              : Filter by MCP Config ID
        :type                         : ``` str ```
        :param filter_provider        : Filter by provider slug
        :type                         : ``` str ```
        :param filter_name            : Filter by config name (exact match)
        :type                         : ``` str ```
        :param filter_mcp_server_url  : Filter configs whose MCP server URL matches this value
        :type                         : ``` str ```
        :param search                 : Free-form search term applied to the name field
        :type                         : ``` str ```

        :returns:
            List MCP Configs Response
        """
        filter_obj = None
        if any(x is not None for x in (filter_id, filter_provider, filter_name, filter_mcp_server_url, search)):
            filter_obj = ListMcpConfigsRequest.Filter(
                id=filter_id or "",
                provider=filter_provider or "",
                name=filter_name or "",
                mcp_server_url=filter_mcp_server_url or "",
            )

        return self.core_client.grpc_exec(
            self.mcp_service.ListMcpConfigs.with_call,
            ListMcpConfigsRequest(
                page_size=page_size or 0,
                page_token=page_token or "",
                filter=filter_obj,
                search=search or ""
            ),
        )

    def create_config(self, mcp_config: McpConfig) -> CreateMcpConfigResponse:
        """
        Method to create a new MCP Configuration

        :param mcp_config        : MCP Configuration to create
        :type                     : ``` McpConfig ```

        :returns:
            Create MCP Config Response
        """
        return self.core_client.grpc_exec(
            self.mcp_service.CreateMcpConfig.with_call,
            CreateMcpConfigRequest(config=mcp_config),
        )

    def update_config(self,
                      config_id: str,
                      description: Optional[str] = None,
                      connection_tool_mappings: Optional[List[McpConfigConnectionToolMapping]] = None) -> UpdateMcpConfigResponse:
        """
        Method to update an existing MCP Configuration
        :param config_id                 : ID of the MCP Configuration to update
        :type                            : ``` str ```
        :param description               : New description for the MCP Configuration
        :type                            : ``` str ```
        :param connection_tool_mappings  : New connection tool mappings for the MCP Configuration
        :type                            : ``` List[McpConfigConnectionToolMapping] ```
        :returns:
            Update MCP Config Response
        """
        request = UpdateMcpConfigRequest(config_id=config_id)
        if description is not None:
            request.description = description
        if connection_tool_mappings is not None:
            request.connection_tool_mappings.extend(connection_tool_mappings)
        return self.core_client.grpc_exec(
            self.mcp_service.UpdateMcpConfig.with_call,
            request,
    )

    def delete_config(self, config_id: str) -> DeleteMcpConfigResponse:
        """
        Method to delete an MCP Configuration by ID

        :param config_id      : ID of the MCP Configuration to delete
        :type                 : ``` str ```

        :returns:
            Delete MCP Config Response
        """
        return self.core_client.grpc_exec(
            self.mcp_service.DeleteMcpConfig.with_call,
            DeleteMcpConfigRequest(config_id=config_id),
        )

    def ensure_instance(
        self,
        name: Optional[str],
        config_name: str,
        user_identifier: str,
    ) -> EnsureMcpInstanceResponse:
        """Create or return an MCP instance for the given config and user."""

        request = EnsureMcpInstanceRequest(
            config_name=config_name,
            user_identifier=user_identifier,
        )
        if name:
            request.name = name

        return self.core_client.grpc_exec(
            self.mcp_service.EnsureMcpInstance.with_call,
            request,
        )

    def update_instance(
        self,
        instance_id: str,
        name: Optional[str] = None,
        config_name: Optional[str] = None,
    ) -> UpdateMcpInstanceResponse:
        """Update attributes for an existing MCP instance."""

        request = UpdateMcpInstanceRequest(instance_id=instance_id)
        if name is not None:
            request.name = name
        if config_name is not None:
            request.config_name = config_name

        return self.core_client.grpc_exec(
            self.mcp_service.UpdateMcpInstance.with_call,
            request,
        )

    def get_instance(self, instance_id: str) -> GetMcpInstanceResponse:
        """Fetch an MCP instance by ID."""

        return self.core_client.grpc_exec(
            self.mcp_service.GetMcpInstance.with_call,
            GetMcpInstanceRequest(instance_id=instance_id),
        )

    def list_instances(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_id: Optional[str] = None,
        filter_name: Optional[str] = None,
        filter_config_name: Optional[str] = None,
        filter_user_identifier: Optional[str] = None,
    ) -> ListMcpInstancesResponse:
        """List MCP instances with optional filters."""

        filter_obj = None
        if any(
            value is not None
            for value in (filter_id, filter_name, filter_config_name, filter_user_identifier)
        ):
            filter_obj = ListMcpInstancesRequest.Filter(
                id=filter_id or "",
                name=filter_name or "",
                config_name=filter_config_name or "",
                user_identifier=filter_user_identifier or "",
            )

        request = ListMcpInstancesRequest(
            page_size=page_size or 0,
            page_token=page_token or "",
            filter=filter_obj,
        )

        return self.core_client.grpc_exec(
            self.mcp_service.ListMcpInstances.with_call,
            request,
        )

    def delete_instance(self, instance_id: str) -> DeleteMcpInstanceResponse:
        """Delete an MCP instance by ID."""

        return self.core_client.grpc_exec(
            self.mcp_service.DeleteMcpInstance.with_call,
            DeleteMcpInstanceRequest(instance_id=instance_id),
        )

    def get_instance_auth_state(
        self,
        instance_id: str,
        include_auth_links: Optional[bool] = None,
    ) -> GetMcpInstanceAuthStateResponse:
        """Retrieve authentication state for connections used by an MCP instance."""

        request = GetMcpInstanceAuthStateRequest(instance_id=instance_id)
        if include_auth_links is not None:
            request.include_auth_links = include_auth_links

        return self.core_client.grpc_exec(
            self.mcp_service.GetMcpInstanceAuthState.with_call,
            request,
        )

    def list_mcp_connected_accounts(
        self,
        config_id: str,
        identifier: str,
        include_auth_link: Optional[bool] = None,
    ) -> ListMcpConnectedAccountsResponse:
        """
        List the connected account auth state for all connections in an MCP config
        for a given user identifier.

        :param config_id          : ID of the MCP configuration whose connections to inspect
        :type                     : ``` str ```
        :param identifier         : End-user identifier (e.g. email or opaque user ID) for
                                    whom the connected account state is being fetched
        :type                     : ``` str ```
        :param include_auth_link  : When True, every connected account in the response will
                                    include an ``authentication_link`` field regardless of its
                                    current status. Set this to True when you are building a
                                    connected-account integration page for an MCP server and
                                    want the end user to see the status of all their connections
                                    and be able to authorise or re-authorise any of them.

                                    When False (default), ``authentication_link`` is omitted.
                                    If a connected account does not exist for a connection,
                                    ``connected_account_id`` will be an empty string. To
                                    generate an auth link in that case, either call
                                    ``get_authorization_link`` for the specific connection or
                                    re-call this method with ``include_auth_link=True``.

                                    Note: generated auth links are valid for 1 minute only.
        :type                     : ``` bool ```

        :returns:
            ListMcpConnectedAccountsResponse
        """
        request = ListMcpConnectedAccountsRequest(
            config_id=config_id,
            identifier=identifier,
        )
        if include_auth_link is not None:
            request.include_auth_link = include_auth_link

        return self.core_client.grpc_exec(
            self.mcp_service.ListMcpConnectedAccounts.with_call,
            request,
        )

    @overload
    def create_session_token(
        self,
        mcp_config_id: str,
        identifier: str,
        expiry: timedelta | None = None,
        access_level: str | None = None,
    ) -> tuple[CreateMcpSessionTokenResponse, grpc.Call]: ...

    @overload
    def create_session_token(
        self,
        *,
        connection_name: str,
        identifier: str,
        expiry: timedelta | None = None,
        access_level: str | None = None,
    ) -> tuple[CreateMcpSessionTokenResponse, grpc.Call]: ...

    def create_session_token(
        self,
        mcp_config_id: str | None | _Unset = _UNSET,
        identifier: str | None = None,
        expiry: timedelta | None = None,
        access_level: str | None = None,
        *,
        connection_name: str | None = None,
    ) -> tuple[CreateMcpSessionTokenResponse, grpc.Call]:
        """Create a short-lived session token for a user to access an MCP server.

        Pass exactly one of ``mcp_config_id`` or ``connection_name``; the
        token works only on the MCP server of that target:

        - ``mcp_config_id``: the MCP configuration's server, at the config's
          ``mcp_server_url``. It serves the tools the configuration exposes.
        - ``connection_name``: the connection's own MCP server, at
          ``<environment_url>/mcp/v3/connections/<connection_name>``. It
          serves every tool of that connection, with no MCP configuration.

        Send the token as a ``Bearer`` token in the ``Authorization`` header
        when calling that URL.

        Args:
            mcp_config_id: ID of the MCP configuration the token grants access
                to, e.g. ``"cfg_01abc123"``.
            identifier: End-user identifier the token acts as, e.g.
                ``"user_123"``: the user of the configuration's instance, or
                the user whose connected account on the connection is used.
                1 to 255 characters. Required.
            expiry: Lifetime of the token. The server accepts 60 seconds to
                24 hours and applies 1 hour when omitted. Fractions of a
                second are dropped.
            access_level: Tools the token can use. ``"READ_ONLY"`` limits it
                to tools annotated read-only: other tools are left out of the
                tool list and refused when called. ``"FULL"``, or omitting it,
                exposes every tool of the target. Values are case-sensitive.
            connection_name: Name of the connection whose MCP server the token
                grants access to, e.g. ``"gmail"``. Keyword-only. Matched
                without regard to case, but the server URL path is
                case-sensitive: connect using the name exactly as stored, e.g.
                copied from the dashboard.

        Returns:
            The ``(response, call)`` tuple, like the other methods of this
            client. ``response.token`` is the bearer token and
            ``response.expires_at`` (Timestamp) is when it expires.

        Raises:
            ValueError: Raised before any request when neither
                ``mcp_config_id`` nor ``connection_name`` is passed, or, with
                ``connection_name``: ``mcp_config_id`` is also given,
                ``connection_name`` is empty, or ``identifier`` is missing or
                empty. With ``mcp_config_id``, the arguments are sent as given
                and the server validates them.
            ScalekitNotFoundException: No active connection has
                ``connection_name``.
            ScalekitBadRequestException: Any other invalid request, e.g. an
                invalid ``identifier``, ``expiry`` or ``access_level``, or a
                connection that is not an AgentKit connection. Depending on
                the environment's configuration, a connection token also
                requires ``identifier`` to have an active connected account on
                the connection; otherwise the server creates a pending
                connected account for ``identifier``, a token is minted, and
                the account is reported as not connected when tools are called.

        Example::

            from datetime import timedelta

            # MCP configuration
            response, _ = client.mcp.create_session_token("cfg_01abc123", "user_123")

            # A connection's MCP server, read-only tools for 15 minutes
            response, _ = client.mcp.create_session_token(
                connection_name="gmail",
                identifier="user_123",
                expiry=timedelta(minutes=15),
                access_level="READ_ONLY",
            )
            headers = {"Authorization": f"Bearer {response.token}"}
        """
        if connection_name is not None:
            identifier = _check_connection_token_args(mcp_config_id, connection_name, identifier)
            request = CreateMcpSessionTokenRequest(key_id=connection_name, identifier=identifier)
        elif mcp_config_id is _UNSET:
            raise ValueError("Either mcp_config_id or connection_name is required")
        else:
            # Built exactly as before connection_name existed: the server
            # validates the configuration ID and identifier.
            request = CreateMcpSessionTokenRequest(
                mcp_config_id=mcp_config_id, identifier=identifier
            )
        return self._mint_session_token(request, expiry, access_level)

    def _mint_session_token(
        self,
        request: CreateMcpSessionTokenRequest,
        expiry: timedelta | None,
        access_level: str | None,
    ) -> tuple[CreateMcpSessionTokenResponse, grpc.Call]:
        """Set the optional fields shared by both session-token targets and send the request."""
        if access_level is not None:
            request.access_level = access_level
        if expiry is not None:
            duration = Duration()
            total_seconds = int(expiry.total_seconds())
            duration.seconds = total_seconds
            request.expiry.CopyFrom(duration)

        return self.core_client.grpc_exec(
            self.mcp_service.CreateMcpSessionToken.with_call,
            request,
        )

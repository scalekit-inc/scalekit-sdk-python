from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.connections.connections_pb2 import *
from scalekit.v1.connections.connections_pb2_grpc import ConnectionServiceStub


class ConnectionClient:
    """Class definition for Connection Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for connection client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.connection_service = ConnectionServiceStub(
            self.core_client.grpc_secure_channel
        )

    def get_connection(
        self, organization_id: str, conn_id: str
    ) -> GetConnectionResponse:
        """
        Method to get connection object

        :param organization_id  : Client organization id to get connection
        :type                   : ``` str ```
        :param conn_id          : Client connection id to get connection
        :type                   : ``` str ```
        :returns
            Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.GetConnection.with_call,
            GetConnectionRequest(organization_id=organization_id, id=conn_id),
        )

    def list_connections_by_domain(self, domain: str, include: Optional[str] = None) -> ListConnectionsResponse:
        """
        Method to get connection object by domain

        :param domain     : Client domain id to get connections
        :type             : ``` str ```
        :param include    : Return active connections or all, E.g. - 'all'
        :type             : ``` str ```

        :returns:
            List Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListConnections.with_call,
            ListConnectionsRequest(domain=domain, include=include),
        )

    def list_connections(self, organization_id: str, include: Optional[str] = None) -> ListConnectionsResponse:
        """
        Method to list connections

        :param organization_id : Client organization id to get connections
        :type                  : ``` str ```
        :param include         : Return active connections or all, E.g. - 'all'
        :type                  : ``` str ```

        :returns:
            List Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListConnections.with_call,
            ListConnectionsRequest(organization_id=organization_id, include=include),
        )

    def enable_connection(
        self, organization_id: str, conn_id: str
    ) -> ToggleConnectionResponse:
        """
        Method to enable connection

        :param organization_id  : Client organization id to enable connection
        :type                   : ``` str ```
        :param conn_id          : Client connection id to enable connection
        :type                   : ``` str ```
        :returns
            Enable Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.EnableConnection.with_call,
            ToggleConnectionRequest(organization_id=organization_id, id=conn_id),
        )

    def disable_connection(
        self, organization_id: str, conn_id: str
    ) -> ToggleConnectionResponse:
        """
        Method to disable connection

        :param organization_id  : Client organization id to disable connection
        :type                   : ``` str ```
        :param conn_id          : Client connection id to disable connection
        :type                   : ``` str ```
        :returns
            Disable Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.DisableConnection.with_call,
            ToggleConnectionRequest(organization_id=organization_id, id=conn_id),
        )

    def create_connection(self, organization_id: str, connection: CreateConnection) -> CreateConnectionResponse:
        """
        Method to create a new connection

        :param organization_id  : Organization id to create connection for
        :type                   : ``` str ```
        :param connection       : CreateConnection object with expected values for conn creation
        :type                   : ``` obj ```

        :returns:
            Create Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.CreateConnection.with_call,
            CreateConnectionRequest(organization_id=organization_id, connection=connection),
        )
    
    def list_app_connections(self, page_size: Optional[int] = None, page_token: Optional[str] = None, provider: Optional[str] = None, query: Optional[str] = None) -> ListAppConnectionsResponse:
        """
        Method to list environment-level app connections

        :param page_size    : Maximum number of connections to return (max 30)
        :type               : ``` int ```
        :param page_token   : Token for pagination
        :type               : ``` str ```
        :param provider     : Filter by provider (e.g. 'HUBSPOT')
        :type               : ``` str ```
        :param query        : Free-text search matching connections by connection name (key ID) or provider (3-100 characters)
        :type               : ``` str ```

        :returns:
            List App Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListAppConnections.with_call,
            ListAppConnectionsRequest(page_size=page_size, page_token=page_token, provider=provider, query=query),
        )

    def get_environment_connection(self, connection_id: str) -> GetConnectionResponse:
        """
        Method to get an environment-level connection by its id

        ``connection.resolved_proxy_url`` is the URL the connector's templated ``proxy_url``
        was resolved to when the connection was created; it is not set when the connector's
        ``proxy_url`` has no template, or the connection is older than the field. For an OAuth
        connection, ``connection.oauth_config.token_endpoint_auth_type`` is not set while the
        connection uses the Default, where Scalekit picks the method per request.

        :param connection_id    : Connection id to retrieve
        :type                   : ``` str ```

        :returns:
            Get Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.GetEnvironmentConnection.with_call,
            GetEnvironmentConnectionRequest(connection_id=connection_id),
        )

    def create_environment_connection(self, connection: CreateConnection, flags: Optional[Flags] = None) -> CreateConnectionResponse:
        """
        Method to create a new environment-level connection

        A connector whose ``proxy_url`` is a template with ``{{domain}}`` or ``{{version}}``
        placeholders, for example an MCP connector with a host per data region, is resolved
        once, when the connection is created. Supply the values in ``CreateConnection.context``,
        a ``google.protobuf.Struct`` such as ``{"domain": "mcp-eu.example.com"}``: ``domain``
        is the host name that replaces ``{{domain}}``, not a region code. Only ``domain`` and
        ``version`` are recognized, and a key the server does not know is rejected with 400. The
        context itself is not stored; the resolved URL is, and ``connection.resolved_proxy_url``
        in the response shows it. If the template needs a value the context does not supply,
        the call fails with 400 ('connection context is missing a value required by provider
        ... proxy_url template').

        :param connection   : CreateConnection object with expected values for conn creation
        :type               : ``` obj ```
        :param flags        : Optional Flags (is_login, is_app)
        :type               : ``` obj ```

        :returns:
            Create Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.CreateEnvironmentConnection.with_call,
            CreateEnvironmentConnectionRequest(connection=connection, flags=flags),
        )

    def update_environment_connection(self, connection_id: str, connection: UpdateConnection) -> UpdateConnectionResponse:
        """
        Method to update an environment-level connection

        To choose how Scalekit authenticates to an OAuth connection's token endpoint, set
        ``UpdateConnection.oauth_config.token_endpoint_auth_type`` to a ``TokenAuthType``:
        ``BASIC_AUTH`` sends client_id and client_secret in an HTTP Basic Authorization
        header (``client_secret_basic``), ``URL_PARAMS`` sends them as POST body parameters
        (``client_secret_post``), and ``NONE`` sends only the client_id, for public (PKCE)
        clients; ``NONE`` is rejected on an OIDC connection. Leave the field unset to keep the
        current value, and send ``TOKEN_AUTH_TYPE_UNSPECIFIED`` to reset it to the Default,
        where Scalekit picks the method per request. It applies to the authorization_code
        exchange, MCP token refresh and OAUTH_M2M client_credentials; refreshing a token on a
        non-MCP OAuth connection always detects the method itself. Set it only when the
        provider's token endpoint documentation requires a specific method: a wrong value
        makes token exchange or refresh fail, and every connected account on the connection
        then has to authenticate again.

        ``oauth_config.token_endpoint_auth_method``, a string (``"client_secret_basic"``,
        ``"client_secret_post"`` or ``"none"``), is deprecated: it maps onto the same stored
        value, and the server rejects any other non-empty string. Send one of the two fields; when both
        are sent with different values, the request is rejected unless one of them equals the
        stored value.

        :param connection_id    : Connection id to update
        :type                   : ``` str ```
        :param connection       : UpdateConnection object with fields to update
        :type                   : ``` obj ```

        :returns:
            Update Connection Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.UpdateEnvironmentConnection.with_call,
            UpdateEnvironmentConnectionRequest(connection_id=connection_id, connection=connection),
        )

    def delete_connection(self, organization_id: str, connection_id: str):
        """
        Method to delete a connection based in given organization and connection id

        :param organization_id  : Organization id to delete connection for
        :type                   : ``` str ```
        :param connection_id    : Connection id of connection to be deleted
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.connection_service.DeleteConnection.with_call,
            DeleteConnectionRequest(organization_id=organization_id, id=connection_id),
        )



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
    
    def list_app_connections(self, page_size: Optional[int] = None, page_token: Optional[str] = None, provider: Optional[str] = None) -> ListAppConnectionsResponse:
        """
        Method to list environment-level app connections

        :param page_size    : Maximum number of connections to return (max 30)
        :type               : ``` int ```
        :param page_token   : Token for pagination
        :type               : ``` str ```
        :param provider     : Filter by provider (e.g. 'HUBSPOT')
        :type               : ``` str ```

        :returns:
            List App Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListAppConnections.with_call,
            ListAppConnectionsRequest(page_size=page_size, page_token=page_token, provider=provider),
        )

    def get_environment_connection(self, connection_id: str) -> GetConnectionResponse:
        """
        Method to get an environment-level connection by its id

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



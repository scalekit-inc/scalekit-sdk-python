
from core import CoreClient
from pkg.scalekit.v1.connections.connections_pb2_grpc import ConnectionServiceStub
from pkg.scalekit.v1.connections.connections_pb2 import *

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

    def list_connections_by_domain(self, domain: str) -> ListConnectionsResponse:
        """
        Method to get connection object by domain

        :param domain     : Client domain id to get connection
        :type             : ``` str ```
        :returns
            List Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListConnections.with_call,
            ListConnectionsRequest(domain=domain),
        )

    def list_connections(self, organization_id: str) -> ListConnectionsResponse:
        """
        Method to list connections

        :param organization_id : Client organization id to get connection
        :type                  : ``` str ```
        :returns:
            List Connections Response
        """
        return self.core_client.grpc_exec(
            self.connection_service.ListConnections.with_call,
            ListConnectionsRequest(organization_id=organization_id),
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
            ToggleConnectionResponse(organization_id=organization_id, id=conn_id),
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
            ToggleConnectionResponse(organization_id=organization_id, id=conn_id),
        )

import grpc

from core import CoreClient
from pkg.scalekit.v1.connections.connections_pb2_grpc import ConnectionServiceStub
from pkg.scalekit.v1.connections.connections_pb2 import *


class ConnectionClient:
    """ Class definition for Connection Client """
    def __init__(self, env_url, client_id, client_secret, custom_headers=None):
        """
        Initializer for connection client
        
        :param env_url        : Environment URL
        :type                 : ``` str ```
        :param client_id      : Client ID
        :type                 : ``` str ```
        :param client_secret  : Client Secret
        :type                 : ``` str ```
        :returns
            None
        """
        try:
            self.custom_headers = custom_headers
            self.host = env_url.split('//')[1]
            self.core_client = CoreClient(env_url, client_id, client_secret)
            self.connection_service = ConnectionServiceStub(
                grpc.secure_channel(
                    self.host, credentials=grpc.compute_engine_channel_credentials(
                        grpc.access_token_call_credentials(self.core_client.authenticate_client())
                    )
                )
            )
        except Exception as exp:
            raise exp

    def get_connection(self, organization_id: str, conn_id: str) -> GetConnectionResponse:
        """
        Method to get connection object
        
        :param organization_id  : Client organization id to get connection
        :type                   : ``` str ```
        :param conn_id          : Client connection id to get connection
        :type                   : ``` str ```
        :returns
            Connection Response
        """
        return CoreClient.grpc_exec(
            self.connection_service.GetConnection,
            GetConnectionRequest(organization_id=organization_id, id=conn_id)
        )

    def list_connections_by_domain(self, domain: str) -> ListConnectionsResponse:
        """
        Method to get connection object by domain

        :param domain     : Client domain id to get connection
        :type             : ``` str ```
        :returns
            List Connections Response
        """
        return CoreClient.grpc_exec(
            self.connection_service.ListConnections,
            ListConnectionsRequest(domain=domain)
        )

    def list_connections(self, organization_id: str) -> ListConnectionsResponse:
        """
        Method to list connections
        
        :param organization_id : Client organization id to get connection
        :type                  : ``` str ```
        :returns:
            List Connections Response
        """
        return CoreClient.grpc_exec(
            self.connection_service.ListConnections,
            ListConnectionsRequest(organization_id=organization_id)
        )

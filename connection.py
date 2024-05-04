import grpc

from core import CoreClient
from scalekit.v1.connections.connections_pb2_grpc import ConnectionServiceStub
from scalekit.v1.connections.connections_pb2 import *


class ConnectionClient:
    """ """
    def __init__(self, env_url, client_id, client_secret):
        """ """
        self.host = env_url.split('//')[1]
        self.core_client = CoreClient(env_url, client_id, client_secret)
        self.connection_service = ConnectionServiceStub(
            grpc.secure_channel(
                self.host, credentials=grpc.compute_engine_channel_credentials(
                    grpc.access_token_call_credentials(self.core_client.authenticate_client())
                )
            )
        )

    async def get_connection(self, organization_id: str, conn_id: str) -> GetConnectionResponse:
        """ """
        return await self.connection_service.GetConnection(
            GetConnectionRequest(organization_id=organization_id, id=conn_id))

    async def get_connection_by_domain(self, domain_id: str) -> GetConnectionByDomainResponse:
        """ """
        return await self.connection_service.GetConnectionByDomain(GetConnectionByDomainRequest(domain=domain_id))

    async def list_connections(self, organization_id: str) -> ListConnectionsResponse:
        """ """
        return await self.connection_service.ListConnections(ListConnectionsRequest(organization_id=organization_id))

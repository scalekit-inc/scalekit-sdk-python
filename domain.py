import grpc

from core import CoreClient
from scalekit.v1.domains.domains_pb2_grpc import DomainServiceStub
from scalekit.v1.domains.domains_pb2 import *


class DomainClient:
    """ """
    def __init__(self, env_url, client_id, client_secret):
        """ """
        self.host = env_url.split('//')[1]
        self.core_client = CoreClient(env_url, client_id, client_secret)
        self.domain_service = DomainServiceStub(
            grpc.secure_channel(
                self.host, credentials=grpc.compute_engine_channel_credentials(
                    grpc.access_token_call_credentials(self.core_client.authenticate_client())
                )
            )
        )

    async def create_domain(self, organization_id: str, domain_name: str) -> GetDomainResponse:
        """ """
        return await self.domain_service.CreateDomain(
            CreateDomainRequest(organization_id=organization_id, domain=CreateDomain(domain=domain_name))
        )

    async def list_domains(self, organization_id: str) -> GetDomainResponse:
        """ """
        return await self.domain_service.ListDomains(ListDomainRequest(organization_id=organization_id))

    async def get_domain(self, organization_id: str, domain_id: str) -> GetDomainResponse:
        """ """
        return await self.domain_service.GetDomain(GetDomainRequest(organization_id=organization_id, id=domain_id))

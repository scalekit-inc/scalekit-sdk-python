import grpc

from core import CoreClient
from scalekit.v1.organizations.organizations_pb2_grpc import OrganizationServiceStub
from scalekit.v1.organizations.organizations_pb2 import *


class OrganizationClient:
    """ """
    def __init__(self, env_url, client_id, client_secret):
        """ """
        self.host = env_url.split('//')[1]
        self.core_client = CoreClient(env_url, client_id, client_secret)
        self.organization_service = OrganizationServiceStub(
            grpc.secure_channel(
                self.host, credentials=grpc.compute_engine_channel_credentials(
                    grpc.access_token_call_credentials(self.core_client.authenticate_client())
                )
            )
        )

    async def list_organizations(self, page_size: int, page_token: str) -> CreateOrganizationResponse:
        """ """
        return await self.organization_service.ListOrganization(
            ListOrganizationsRequest(page_size=page_size, page_token=page_token)
        )

    async def create_organization(self, organization: dict) -> CreateOrganizationResponse:
        """ """
        return await self.organization_service.CreateOrganization(
            CreateOrganizationRequest(
                organization=organization
            )
        )

    async def update_organization(self, org_id: str, organization: UpdateOrganization.MetadataEntry | None) -> (
            UpdateOrganizationResponse):
        """ """
        return await self.organization_service.UpdateOrganization(
            UpdateOrganizationRequest(id=org_id, organization=organization)
        )

    async def update_organization_by_external_id(self, external_id: str) -> UpdateOrganizationResponse:
        """ """
        return await self.organization_service.UpdateOrganization(UpdateOrganizationRequest(external_id=external_id))

    async def get_organization(self, org_id: str) -> GetOrganizationResponse:
        """ """
        return await self.organization_service.GetOrganization(GetOrganizationRequest(id=org_id))

    async def get_organization_by_external_id(self, external_id: str):
        """ """
        return await self.organization_service.GetOrganization(GetOrganizationRequest(external_id=external_id))

    async def generate_customer_portal_link(self, org_id: str) -> CustomerPortalLinksResponse:
        """ """
        return await self.organization_service.GetCustomerPortalLink(CustomerPortalLinkRequest(id=org_id))

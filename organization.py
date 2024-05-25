import grpc

from core import CoreClient
from pkg.scalekit.v1.organizations.organizations_pb2_grpc import OrganizationServiceStub
from pkg.scalekit.v1.organizations.organizations_pb2 import *


class OrganizationClient:
    """ Class definition for Organization Client """
    def __init__(self, env_url, client_id, client_secret):
        """
        Initializer for Organization Client

        :param env_url        : Environment URL
        :type                 : ``` str ```
        :param client_id      : Client ID
        :type                 : ``` str ```
        :param client_secret  : Client Secret
        :type                 : ``` str ```
        :returns
            None
        """
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
        """
        Method to list orgqnizations 

        :param page_size  : page size for org list fetch
        :type             : ``` int ```
        :param page_token : page token for org list fetch
        :type             : ``` str ```
        :returns:
             list of organizations
        """
        return await self.organization_service.ListOrganization(
            ListOrganizationsRequest(page_size=page_size, page_token=page_token)
        )

    async def create_organization(self, organization: dict) -> CreateOrganizationResponse:
        """
        Method to create organization based on given data
         
        :param organization : dictionary containing org details for creation
        :type               : ``` dict ``` 
        :returns:
            Create Organization Response 
        """
        return await self.organization_service.CreateOrganization(
            CreateOrganizationRequest(
                organization=organization
            )
        )

    async def update_organization(self, org_id: str, organization: UpdateOrganization.MetadataEntry | None) -> (
            UpdateOrganizationResponse):
        """
        Method to update organization based on given data
         
        :param org_id       : Organization id to update
        :type               : ``` str ```
        :param organization : Update organization metadata object for org update
        :type               : ``` obj ``` 
        :returns:
            Update Organization Response 
        """
        return await self.organization_service.UpdateOrganization(
            UpdateOrganizationRequest(id=org_id, organization=organization)
        )

    async def update_organization_by_external_id(self, external_id: str) -> UpdateOrganizationResponse:
        """
        Method to update organization based on external id
         
        :param external_id  : External id to update org
        :type               : ``` str ```
        :returns:
            Update Organization Response  
        """
        return await self.organization_service.UpdateOrganization(UpdateOrganizationRequest(external_id=external_id))

    async def get_organization(self, org_id: str) -> GetOrganizationResponse:
        """
        Method to get organization based on given org id
         
        :param org_id  : Organization id
        :type          : ``` str ```
        :returns:
            Get Organization Response 
        """
        return await self.organization_service.GetOrganization(GetOrganizationRequest(id=org_id))

    async def get_organization_by_external_id(self, external_id: str):
        """
        Method to get organization based on given org id
         
        :param external_id  : External id to fetch org details
        :type               : ``` str ```
        :returns:
            Get Organization Response 
        """
        return await self.organization_service.GetOrganization(GetOrganizationRequest(external_id=external_id))

    async def generate_customer_portal_link(self, org_id: str) -> CustomerPortalLinksResponse:
        """
        Method to generate customoer portal link
        
        :param org_id       : Organization id to fetch portal link for
        :type               : ``` str ``` 
        :return: 
        """
        return await self.organization_service.GetCustomerPortalLink(CustomerPortalLinkRequest(id=org_id))

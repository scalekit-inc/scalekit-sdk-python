from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.organizations.organizations_pb2 import *
from scalekit.v1.organizations.organizations_pb2_grpc import OrganizationServiceStub


class OrganizationClient:
    """Class definition for Organization Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Organization Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.organization_service = OrganizationServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_organizations(
        self, page_size: int, page_token: Optional[str] = None
    ) -> CreateOrganizationResponse:
        """
        Method to list organizations

        :param page_size  : page size for org list fetch
        :type             : ``` int ```
        :param page_token : page token for org list fetch
        :type             : ``` str ```
        :returns:
             list of organizations
        """
        return self.core_client.grpc_exec(
            self.organization_service.ListOrganization.with_call,
            ListOrganizationsRequest(page_size=page_size, page_token=page_token),
        )

    def create_organization(
        self, name: str, options: CreateOrganization
    ) -> CreateOrganizationResponse:
        """
        Method to create organization based on given data

        :param name     : Name of the org to be created
        :type           : ``` str ```
        :param options  : Additional details for org to be created
        :type           : ``` obj ```
        :returns:
            Create Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.CreateOrganization.with_call,
            CreateOrganizationRequest(
                organization={"displayName": name, "externalId": options.external_id}
            ),
        )

    def update_organization(
        self, organization_id: str, organization: UpdateOrganization
    ) -> UpdateOrganizationResponse:
        """
        Method to update organization based on given data

        :param organization_id       : Organization id to update
        :type               : ``` str ```
        :param organization : Optional params for update organization operation
        :type               : ``` obj ```
        :returns:
            Update Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.UpdateOrganization.with_call,
            UpdateOrganizationRequest(id=organization_id, organization=organization),
        )

    def update_organization_by_external_id(
        self, external_id: str
    ) -> UpdateOrganizationResponse:
        """
        Method to update organization based on external id

        :param external_id  : External id to update org
        :type               : ``` str ```
        :returns:
            Update Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.UpdateOrganization.with_call,
            UpdateOrganizationRequest(external_id=external_id),
        )

    def get_organization(self, organization_id: str) -> GetOrganizationResponse:
        """
        Method to get organization based on given org id

        :param organization_id  : Organization id
        :type          : ``` str ```
        :returns:
            Get Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.GetOrganization.with_call,
            GetOrganizationRequest(id=organization_id),
        )

    def get_organization_by_external_id(self, external_id: str):
        """
        Method to get organization based on given org id

        :param external_id  : External id to fetch org details
        :type               : ``` str ```
        :returns:
            Get Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.GetOrganization.with_call,
            GetOrganizationRequest(external_id=external_id),
        )

    def delete_organization(self, organization_id: str) -> None:
        """
        Method to delete organization based on given org id

        :param organization_id  : Organization id
        :type          : ``` str ```
        :returns:
            None
        """
        self.core_client.grpc_exec(
            self.organization_service.DeleteOrganization.with_call,
            DeleteOrganizationRequest(id=organization_id),
        )

    def generate_portal_link(self, organization_id: str) -> GeneratePortalLinkResponse:
        """
        Method to generate customer portal link

        :param organization_id       : Organization id to fetch portal link for
        :type               : ``` str ```
        :return:
        """
        response = self.core_client.grpc_exec(
            self.organization_service.GeneratePortalLink.with_call,
            GeneratePortalLinkRequest(id=organization_id),
        )
        if not response.link:
            raise Exception("Error generating portal link")
        return response.link

    def get_portal_links(self, organization_id: str) -> GetPortalLinksResponse:
        """
        Method to get customer portal links

        :param organization_id       : Organization id to fetch portal link for
        :type               : ``` str ```
        :return:
        """
        response = self.core_client.grpc_exec(
            self.organization_service.GetPortalLinks.with_call,
            GetPortalLinkRequest(id=organization_id),
        )
        return response.links

    def delete_portal_link(self, organization_id: str) -> None:
        """
        Method to delete customer portal link

        :param organization_id       : Organization id to delete portal link for
        :type               : ``` str ```
        :returns:
            None
        """
        self.core_client.grpc_exec(
            self.organization_service.DeletePortalLink.with_call,
            DeletePortalLinkRequest(id=organization_id),
        )

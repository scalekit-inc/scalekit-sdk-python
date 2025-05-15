from typing import Optional, List, Dict

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
    ) -> ListOrganizationsResponse:
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
        self, organization: CreateOrganization
    ) -> CreateOrganizationResponse:
        """
        Method to create organization based on given data

        :param organization  : Create Organization obj with details for org creation
        :type                : ``` obj ```
        :returns:
            Create Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.CreateOrganization.with_call,
            CreateOrganizationRequest(organization=organization),
        )

    def update_organization(
        self, organization_id: str, organization: UpdateOrganization
    ) -> UpdateOrganizationResponse:
        """
        Method to update organization based on given data

        :param organization_id       : Organization id to update
        :type               : ``` str ```
        :param organization : params for update organization operation
        :type               : ``` obj ```
        :returns:
            Update Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.UpdateOrganization.with_call,
            UpdateOrganizationRequest(id=organization_id, organization=organization),
        )

    def update_organization_by_external_id(
        self, external_id: str, organization: UpdateOrganization
    ) -> UpdateOrganizationResponse:
        """
        Method to update organization based on external id

        :param external_id  : External id to update org
        :type               : ``` str ```
        :param organization : params for update organization operation
        :type               : ``` obj ```

        :returns:
            Update Organization Response
        """
        return self.core_client.grpc_exec(
            self.organization_service.UpdateOrganization.with_call,
            UpdateOrganizationRequest(external_id=external_id, organization=organization),
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

    def delete_organization(self, organization_id: str):
        """
        Method to delete organization based on given org id

        :param organization_id  : Organization id
        :type          : ``` str ```
        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.organization_service.DeleteOrganization.with_call,
            DeleteOrganizationRequest(id=organization_id),
        )

    def generate_portal_link(self, organization_id: str, features: [Feature] = None) -> GeneratePortalLinkResponse:
        """
        Method to generate customer portal link

        :param organization_id   :  Organization id to fetch portal link for
        :type                    :  ``` str ```
        :param  features         :  Feature list to generate portal link for
        :type                    :  ```dict```
        :return:
        """
        response = self.core_client.grpc_exec(
            self.organization_service.GeneratePortalLink.with_call,
            GeneratePortalLinkRequest(id=organization_id, features=features),
        )
        if not response[0].link:
            raise Exception("Error generating portal link")
        return response[0].link

    def update_organization_settings(self, organization_id: str, settings: List[Dict[str, bool]]):
        """
        Method to update organization settings

        :param organization_id    : Organization id for org update
        :type                     : ``` str ```
        :param settings           : Organization settings
        :type                     : ``` list[dict[str, bool]] ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.organization_service.UpdateOrganizationSettings.with_call,
            UpdateOrganizationSettingsRequest(
                id=organization_id, settings={'features': settings})
        )

from typing import Optional, List, Dict

from google.protobuf import wrappers_pb2
from scalekit.core import CoreClient
from scalekit.v1.organizations.organizations_pb2 import (
    ListOrganizationsRequest,
    ListOrganizationsResponse,
    CreateOrganization,
    CreateOrganizationRequest,
    CreateOrganizationResponse,
    UpdateOrganization,
    UpdateOrganizationRequest,
    UpdateOrganizationResponse,
    GetOrganizationRequest,
    GetOrganizationResponse,
    DeleteOrganizationRequest,
    Feature,
    GeneratePortalLinkRequest,
    GeneratePortalLinkResponse,
    UpdateOrganizationSettingsRequest,
    OrganizationUserManagementSettings,
    UpsertUserManagementSettingsRequest,
    SearchOrganizationsRequest,
    SearchOrganizationsResponse,
    DeletePortalLinkRequest,
    DeletePortalLinkByIdRequest,
    GetPortalLinkRequest,
    GetPortalLinksResponse,
    CreateOrganizationSessionSettingsRequest,
    CreateOrganizationSessionSettingsResponse,
    GetOrganizationSessionSettingsRequest,
    GetOrganizationSessionSettingsResponse,
    UpdateOrganizationSessionSettingsRequest,
    UpdateOrganizationSessionSettingsResponse,
    DeleteOrganizationSessionSettingsRequest,
    OrganizationSessionSettings,
    GetOrganizationUserManagementSettingsRequest,
    GetOrganizationUserManagementSettingsResponse,
)
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
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> ListOrganizationsResponse:
        """
        Method to list organizations

        :param page_size  : page size for org list fetch (optional, uses server default if not provided)
        :type             : ``` int ```
        :param page_token : page token for org list fetch
        :type             : ``` str ```
        :returns:
             list of organizations
        """
        request = ListOrganizationsRequest()
        if page_size is not None:
            request.page_size = page_size
        if page_token is not None:
            request.page_token = page_token
        return self.core_client.grpc_exec(
            self.organization_service.ListOrganization.with_call,
            request,
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
            self.organization_service.GetOrganizationByExternalId.with_call,
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

    def upsert_user_management_settings(self, organization_id: str, max_allowed_users: Optional[int] = None):
        """
        Upsert organization user management settings like maximum allowed users.

        :param organization_id: Organization id for update
        :type organization_id : ``` str ```
        :param max_allowed_users: Maximum allowed users (None to clear)
        :type max_allowed_users: ``` int | None ```
        :returns:
            OrganizationUserManagementSettings
        """
        settings = OrganizationUserManagementSettings()
        if max_allowed_users is not None:
            settings.max_allowed_users.CopyFrom(wrappers_pb2.Int32Value(value=max_allowed_users))
        response = self.core_client.grpc_exec(
            self.organization_service.UpsertUserManagementSettings.with_call,
            UpsertUserManagementSettingsRequest(
                organization_id=organization_id,
                settings=settings
            )
        )
        return response[0].settings

    def search_organizations(
        self,
        query: str,
        page_size: int = 20,
        page_token: Optional[str] = None,
    ) -> SearchOrganizationsResponse:
        """
        Search organizations by name, external ID, or other attributes.

        When to use: Call when building an admin UI that needs to find organizations by
        partial name or external ID rather than paginating through the full list.

        :param query       : Search string matched against organization name, external_id, and metadata
        :type              : ``` str ```
        :param page_size   : Maximum number of results to return per page (default 20)
        :type              : ``` int ```
        :param page_token  : Pagination cursor from a previous response's next_page_token
        :type              : ``` str | None ```

        :returns:
            SearchOrganizationsResponse — organizations (list of matching orgs),
            total_size (total match count), next_page_token and prev_page_token for pagination
        """
        return self.core_client.grpc_exec(
            self.organization_service.SearchOrganization.with_call,
            SearchOrganizationsRequest(
                query=query,
                page_size=page_size,
                page_token=page_token,
            ),
        )

    def delete_portal_link(self, organization_id: str):
        """
        Delete all active portal links for an organization.

        When to use: Call when revoking a customer's admin portal access entirely,
        for example after offboarding or when rotating portal credentials.

        :param organization_id  : ID of the organization whose portal links should be revoked
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.organization_service.DeletePortalLink.with_call,
            DeletePortalLinkRequest(id=organization_id),
        )

    def delete_portal_link_by_id(self, organization_id: str, link_id: str):
        """
        Delete a specific portal link for an organization by its link ID.

        When to use: Call when revoking a single portal link without affecting other
        active links for the same organization.

        :param organization_id  : ID of the organization that owns the link
        :type                   : ``` str ```
        :param link_id          : ID of the specific portal link to delete
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.organization_service.DeletePortalLinkByID.with_call,
            DeletePortalLinkByIdRequest(id=organization_id, link_id=link_id),
        )

    def get_portal_links(self, organization_id: str) -> GetPortalLinksResponse:
        """
        Retrieve all active portal links for an organization.

        When to use: Call when displaying the list of outstanding portal invitations
        in your admin dashboard, or before generating a new link to avoid duplicates.

        :param organization_id  : ID of the organization whose portal links to fetch
        :type                   : ``` str ```

        :returns:
            GetPortalLinksResponse — links (list of Link objects, each with id, location,
            and expire_time)
        """
        return self.core_client.grpc_exec(
            self.organization_service.GetPortalLinks.with_call,
            GetPortalLinkRequest(id=organization_id),
        )

    def create_organization_session_settings(
        self,
        organization_id: str,
        environment_id: str,
        session_management_enabled: Optional[bool] = None,
        absolute_session_timeout: Optional[int] = None,
        idle_session_enabled: Optional[bool] = None,
        idle_session_timeout: Optional[int] = None,
    ) -> UpdateOrganizationSessionSettingsResponse:
        """
        Create session settings for an organization, optionally configuring them in one call.

        When to use: Call during organization onboarding to initialize session policy.
        Pass the desired settings directly rather than following up with a separate update.

        :param organization_id          : ID of the organization
        :type                           : ``` str ```
        :param environment_id           : ID of the environment the settings apply to
        :type                           : ``` str ```
        :param session_management_enabled : Whether custom session management is active
        :type                           : ``` Optional[bool] ```
        :param absolute_session_timeout : Maximum session duration in seconds regardless of activity
        :type                           : ``` Optional[int] ```
        :param idle_session_enabled     : Whether idle timeout is enforced
        :type                           : ``` Optional[bool] ```
        :param idle_session_timeout     : Seconds of inactivity before the session expires
        :type                           : ``` Optional[int] ```

        :returns:
            UpdateOrganizationSessionSettingsResponse — environment_id, organization_id,
            and session_settings reflecting the configured values
        """
        self.core_client.grpc_exec(
            self.organization_service.CreateOrganizationSessionSettings.with_call,
            CreateOrganizationSessionSettingsRequest(
                id=organization_id,
                environment_id=environment_id,
            ),
        )
        settings = OrganizationSessionSettings(
            **({} if session_management_enabled is None else {"session_management_enabled": wrappers_pb2.BoolValue(value=session_management_enabled)}),
            **({} if absolute_session_timeout is None else {"absolute_session_timeout": wrappers_pb2.Int32Value(value=absolute_session_timeout)}),
            **({} if idle_session_enabled is None else {"idle_session_enabled": wrappers_pb2.BoolValue(value=idle_session_enabled)}),
            **({} if idle_session_timeout is None else {"idle_session_timeout": wrappers_pb2.Int32Value(value=idle_session_timeout)}),
        )
        return self.core_client.grpc_exec(
            self.organization_service.UpdateOrganizationSessionSettings.with_call,
            UpdateOrganizationSessionSettingsRequest(
                id=organization_id,
                environment_id=environment_id,
                session_settings=settings,
            ),
        )

    def get_organization_session_settings(
        self, organization_id: str, environment_id: str
    ) -> GetOrganizationSessionSettingsResponse:
        """
        Fetch the current session settings for an organization in a specific environment.

        When to use: Call when rendering an admin settings page that shows session
        timeout and token expiry values configured for a tenant.

        :param organization_id  : ID of the organization whose session settings to fetch
        :type                   : ``` str ```
        :param environment_id   : ID of the environment the settings apply to
        :type                   : ``` str ```

        :returns:
            GetOrganizationSessionSettingsResponse — environment_id, organization_id,
            and session_settings (OrganizationSessionSettings with current token lifetime values)
        """
        return self.core_client.grpc_exec(
            self.organization_service.GetOrganizationSessionSettings.with_call,
            GetOrganizationSessionSettingsRequest(
                id=organization_id,
                environment_id=environment_id,
            ),
        )

    def update_organization_session_settings(
        self,
        organization_id: str,
        environment_id: str,
        session_settings: OrganizationSessionSettings,
    ) -> UpdateOrganizationSessionSettingsResponse:
        """
        Update session settings for an organization in a specific environment.

        When to use: Call when a customer admin changes their session timeout policy
        or token lifetime from the settings UI.

        :param organization_id    : ID of the organization to update
        :type                     : ``` str ```
        :param environment_id     : ID of the environment the settings apply to
        :type                     : ``` str ```
        :param session_settings   : OrganizationSessionSettings object with the new values
        :type                     : ``` OrganizationSessionSettings ```

        :returns:
            UpdateOrganizationSessionSettingsResponse — environment_id, organization_id,
            and session_settings reflecting the updated configuration
        """
        return self.core_client.grpc_exec(
            self.organization_service.UpdateOrganizationSessionSettings.with_call,
            UpdateOrganizationSessionSettingsRequest(
                id=organization_id,
                environment_id=environment_id,
                session_settings=session_settings,
            ),
        )

    def delete_organization_session_settings(
        self, organization_id: str, environment_id: str
    ):
        """
        Delete custom session settings for an organization, reverting to environment defaults.

        When to use: Call when a customer needs to reset their session configuration
        back to the environment-level defaults.

        :param organization_id  : ID of the organization whose session settings to delete
        :type                   : ``` str ```
        :param environment_id   : ID of the environment the settings apply to
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.organization_service.DeleteOrganizationSessionSettings.with_call,
            DeleteOrganizationSessionSettingsRequest(
                id=organization_id,
                environment_id=environment_id,
            ),
        )

    def get_organization_user_management_setting(
        self, organization_id: str
    ) -> GetOrganizationUserManagementSettingsResponse:
        """
        Fetch user management settings for an organization, such as maximum allowed users.

        When to use: Call before adding a new user to check whether the organization
        has reached its user limit.

        :param organization_id  : ID of the organization whose user management settings to fetch
        :type                   : ``` str ```

        :returns:
            GetOrganizationUserManagementSettingsResponse — settings (OrganizationUserManagementSettings
            with max_allowed_users and current user count)
        """
        return self.core_client.grpc_exec(
            self.organization_service.GetOrganizationUserManagementSetting.with_call,
            GetOrganizationUserManagementSettingsRequest(organization_id=organization_id),
        )

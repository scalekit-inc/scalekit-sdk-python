from typing import List, Optional

from google.protobuf.empty_pb2 import Empty
from scalekit.core import CoreClient
from scalekit.v1.users.users_pb2 import (
    AssignUserRolesRequest,
    AssignUserRolesResponse,
    CreateMembership,
    CreateMembershipRequest,
    CreateMembershipResponse,
    CreateUser,
    CreateUserAndMembershipRequest,
    CreateUserAndMembershipResponse,
    DeleteMembershipRequest,
    DeleteUserRequest,
    GetCurrentUserRequest,
    GetCurrentUserResponse,
    GetSupportHashResponse,
    GetUserRequest,
    GetUserResponse,
    ListOrganizationUsersRequest,
    ListOrganizationUsersResponse,
    ListUserPermissionsRequest,
    ListUserPermissionsResponse,
    ListUserRolesRequest,
    ListUserRolesResponse,
    ListUsersRequest,
    ListUsersResponse,
    RemoveUserRoleRequest,
    ResendInviteRequest,
    ResendInviteResponse,
    SearchOrganizationUsersRequest,
    SearchOrganizationUsersResponse,
    SearchUsersRequest,
    SearchUsersResponse,
    UpdateMembership,
    UpdateMembershipRequest,
    UpdateMembershipResponse,
    UpdateUser,
    UpdateUserRequest,
    UpdateUserResponse,
)
from scalekit.v1.users.users_pb2_grpc import UserServiceStub


class UserClient:
    """Class definition for User Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for User Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.user_service = UserServiceStub(
            self.core_client.grpc_secure_channel
        )

    def create_user_and_membership(
        self, 
        organization_id: str, 
        user: CreateUser, 
        send_invitation_email: bool = True
    ) -> CreateUserAndMembershipResponse:
        """
        Method to create a new user and add them to an organization

        :param organization_id      : Organization id to create user for
        :type                       : ``` str ```
        :param user                : CreateUser object with expected values for user creation
        :type                       : ``` obj ```
        :param send_invitation_email: Whether to send invitation email to the user
        :type                       : ``` bool ```

        :returns:
            Create User And Membership Response
        """
        return self.core_client.grpc_exec(
            self.user_service.CreateUserAndMembership.with_call,
            CreateUserAndMembershipRequest(
                organization_id=organization_id,
                user=user,
                send_invitation_email=send_invitation_email
            ),
        )

    def get_user(self, user_id: str) -> GetUserResponse:
        """
        Method to get user by ID

        :param user_id         : User id to get user details
        :type                  : ``` str ```

        :returns:
            Get User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.GetUser.with_call,
            GetUserRequest(id=user_id),
        )

    def get_user_by_external_id(self, external_id: str) -> GetUserResponse:
        """
        Method to get user by external ID

        :param external_id     : External id to get user details
        :type                  : ``` str ```

        :returns:
            Get User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.GetUser.with_call,
            GetUserRequest(external_id=external_id),
        )

    def list_users(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListUsersResponse:
        """
        Method to list all users in environment

        :param page_size       : Page size for pagination
        :type                  : ``` int ```
        :param page_token      : Page token for pagination
        :type                  : ``` str ```

        :returns:
            List Users Response
        """
        return self.core_client.grpc_exec(
            self.user_service.ListUsers.with_call,
            ListUsersRequest(
                page_size=page_size,
                page_token=page_token
            ),
        )

    def list_organization_users(
        self,
        organization_id: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListOrganizationUsersResponse:
        """
        Method to list users for given organization id

        :param organization_id  : Organization id to list users for
        :type                   : ``` str ```
        :param page_size       : Page size for pagination
        :type                   : ``` int ```
        :param page_token      : Page token for pagination
        :type                   : ``` str ```

        :returns:
            List Organization Users Response
        """
        return self.core_client.grpc_exec(
            self.user_service.ListOrganizationUsers.with_call,
            ListOrganizationUsersRequest(
                organization_id=organization_id,
                page_size=page_size,
                page_token=page_token
            ),
        )

    def update_user(self, user_id: str, user: UpdateUser) -> UpdateUserResponse:
        """
        Method to update an existing user by ID

        :param user_id         : User id to update
        :type                  : ``` str ```
        :param user            : UpdateUser object with expected values for user update
        :type                  : ``` obj ```

        :returns:
            Update User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.UpdateUser.with_call,
            UpdateUserRequest(id=user_id, user=user),
        )

    def update_user_by_external_id(self, external_id: str, user: UpdateUser) -> UpdateUserResponse:
        """
        Method to update an existing user by external ID

        :param external_id     : External id to update
        :type                  : ``` str ```
        :param user            : UpdateUser object with expected values for user update
        :type                  : ``` obj ```

        :returns:
            Update User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.UpdateUser.with_call,
            UpdateUserRequest(external_id=external_id, user=user),
        )

    def delete_user(self, user_id: str):
        """
        Method to delete user by ID

        :param user_id         : User id to be deleted
        :type                  : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.user_service.DeleteUser.with_call,
            DeleteUserRequest(id=user_id),
        )

    def delete_user_by_external_id(self, external_id: str):
        """
        Method to delete user by external ID

        :param external_id     : External id to be deleted
        :type                  : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.user_service.DeleteUser.with_call,
            DeleteUserRequest(external_id=external_id),
        )

    def create_membership(
        self,
        organization_id: str,
        user_id: str,
        membership: CreateMembership,
        send_invitation_email: bool = True
    ) -> CreateMembershipResponse:
        """
        Method to create a membership for a user by user ID

        :param organization_id  : Organization id
        :type                   : ``` str ```
        :param user_id          : User id
        :type                   : ``` str ```
        :param membership       : CreateMembership object
        :type                   : ``` obj ```
        :param send_invitation_email: Whether to send invitation email to the user
        :type                       : ``` bool ```

        :returns:
            Create Membership Response
        """
        return self.core_client.grpc_exec(
            self.user_service.CreateMembership.with_call,
            CreateMembershipRequest(
                organization_id=organization_id,
                id=user_id,
                membership=membership,
                send_invitation_email=send_invitation_email
            ),
        )

    def create_membership_by_external_id(
        self,
        organization_id: str,
        external_id: str,
        membership: CreateMembership,
        send_invitation_email: bool = True
    ) -> CreateMembershipResponse:
        """
        Method to create a membership for a user by external ID

        :param organization_id  : Organization id
        :type                   : ``` str ```
        :param external_id      : External id
        :type                   : ``` str ```
        :param membership       : CreateMembership object
        :type                   : ``` obj ```
        :param send_invitation_email: Whether to send invitation email to the user
        :type                       : ``` bool ```

        :returns:
            Create Membership Response
        """
        return self.core_client.grpc_exec(
            self.user_service.CreateMembership.with_call,
            CreateMembershipRequest(
                organization_id=organization_id,
                external_id=external_id,
                membership=membership,
                send_invitation_email=send_invitation_email
            ),
        )

    def update_membership(
        self,
        organization_id: str,
        user_id: str,
        membership: UpdateMembership
    ) -> UpdateMembershipResponse:
        """
        Method to update a membership for a user by user ID

        :param organization_id  : Organization id
        :type                   : ``` str ```
        :param user_id          : User id
        :type                   : ``` str ```
        :param membership       : UpdateMembership object
        :type                   : ``` obj ```

        :returns:
            Update Membership Response
        """
        return self.core_client.grpc_exec(
            self.user_service.UpdateMembership.with_call,
            UpdateMembershipRequest(
                organization_id=organization_id,
                id=user_id,
                membership=membership
            ),
        )

    def update_membership_by_external_id(
        self,
        organization_id: str,
        external_id: str,
        membership: UpdateMembership
    ) -> UpdateMembershipResponse:
        """
        Method to update a membership for a user by external ID

        :param organization_id  : Organization id
        :type                   : ``` str ```
        :param external_id      : External id
        :type                   : ``` str ```
        :param membership       : UpdateMembership object
        :type                   : ``` obj ```

        :returns:
            Update Membership Response
        """
        return self.core_client.grpc_exec(
            self.user_service.UpdateMembership.with_call,
            UpdateMembershipRequest(
                organization_id=organization_id,
                external_id=external_id,
                membership=membership
            ),
        )

    def delete_membership(
        self,
        organization_id: str,
        user_id: str
    ):
        """
        Method to delete a membership for a user by user ID

        :param organization_id  : Organization id
        :type                   : ``` str ```
        :param user_id          : User id
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.user_service.DeleteMembership.with_call,
            DeleteMembershipRequest(
                organization_id=organization_id,
                id=user_id
            ),
        )

    def delete_membership_by_external_id(
        self,
        organization_id: str,
        external_id: str
    ):
        """
        Method to delete a membership for a user by external ID

        :param organization_id  : Organization id
        :type                   : ``` str ```
        :param external_id      : External id
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.user_service.DeleteMembership.with_call,
            DeleteMembershipRequest(
                organization_id=organization_id,
                external_id=external_id
            ),
        )

    def resend_invite(
        self,
        organization_id: str,
        user_id: str
    ) -> ResendInviteResponse:
        """
        Method to resend an invitation email to a user who has a pending invitation

        :param organization_id  : Organization id containing the pending invitation
        :type                   : ``` str ```
        :param user_id          : User id who has a pending invitation
        :type                   : ``` str ```

        :returns:
            Resend Invite Response
        """
        return self.core_client.grpc_exec(
            self.user_service.ResendInvite.with_call,
            ResendInviteRequest(
                organization_id=organization_id,
                id=user_id
            ),
        )

    def list_user_roles(
        self,
        organization_id: str,
        user_id: str
    ) -> ListUserRolesResponse:
        """
        Method to list all roles assigned to a user in an organization

        :param organization_id  : Organization id containing the user
        :type                   : ``` str ```
        :param user_id          : User id to list roles for
        :type                   : ``` str ```

        :returns:
            List User Roles Response
        """
        return self.core_client.grpc_exec(
            self.user_service.ListUserRoles.with_call,
            ListUserRolesRequest(
                organization_id=organization_id,
                user_id=user_id
            ),
        )

    def list_user_permissions(
        self,
        organization_id: str,
        user_id: str
    ) -> ListUserPermissionsResponse:
        """
        Method to list all permissions granted to a user in an organization

        :param organization_id  : Organization id containing the user
        :type                   : ``` str ```
        :param user_id          : User id to list permissions for
        :type                   : ``` str ```

        :returns:
            List User Permissions Response
        """
        return self.core_client.grpc_exec(
            self.user_service.ListUserPermissions.with_call,
            ListUserPermissionsRequest(
                organization_id=organization_id,
                user_id=user_id
            ),
        )

    def get_current_user(self) -> GetCurrentUserResponse:
        """
        Fetch the user associated with the currently authenticated session token.

        When to use: Call immediately after a user signs in to retrieve their profile
        for display in the app or to populate session state.

        :returns:
            GetCurrentUserResponse — user (User object with id, email, and profile fields),
            current_session_id (ID of the active session)
        """
        return self.core_client.grpc_exec(
            self.user_service.GetCurrentUser.with_call,
            GetCurrentUserRequest(),
        )

    def get_support_hash(self) -> GetSupportHashResponse:
        """
        Retrieve a support hash for the current user for use with third-party support widgets.

        When to use: Call when initializing a customer support chat widget (e.g. Intercom)
        that requires an HMAC hash to verify the user's identity.

        :returns:
            GetSupportHashResponse — support_hash (HMAC string to pass to the support widget)
        """
        return self.core_client.grpc_exec(
            self.user_service.GetSupportHash.with_call,
            Empty(),
        )

    def search_users(
        self,
        query: str,
        page_size: int = 20,
        page_token: Optional[str] = None,
    ) -> SearchUsersResponse:
        """
        Search all users in the environment by email, name, or other profile fields.

        When to use: Call when building an admin user lookup UI that needs to find
        users across all organizations by partial email or name.

        :param query       : Search string matched against email, name, and external_id
        :type              : ``` str ```
        :param page_size   : Maximum number of results to return per page (default 20)
        :type              : ``` int ```
        :param page_token  : Pagination cursor from a previous response's next_page_token
        :type              : ``` str | None ```

        :returns:
            SearchUsersResponse — users (list of matching User objects),
            total_size, next_page_token, and prev_page_token for pagination
        """
        return self.core_client.grpc_exec(
            self.user_service.SearchUsers.with_call,
            SearchUsersRequest(
                query=query,
                page_size=page_size,
                page_token=page_token,
            ),
        )

    def search_organization_users(
        self,
        organization_id: str,
        query: str,
        page_size: int = 20,
        page_token: Optional[str] = None,
    ) -> SearchOrganizationUsersResponse:
        """
        Search users within a specific organization by email, name, or other profile fields.

        When to use: Call when an org admin uses the member search box to find a user
        within their tenant without scrolling through a full list.

        :param organization_id  : ID of the organization to search within
        :type                   : ``` str ```
        :param query            : Search string matched against email, name, and external_id
        :type                   : ``` str ```
        :param page_size        : Maximum number of results to return per page (default 20)
        :type                   : ``` int ```
        :param page_token       : Pagination cursor from a previous response's next_page_token
        :type                   : ``` str | None ```

        :returns:
            SearchOrganizationUsersResponse — users (list of matching User objects scoped to the org),
            total_size, next_page_token, and prev_page_token for pagination
        """
        return self.core_client.grpc_exec(
            self.user_service.SearchOrganizationUsers.with_call,
            SearchOrganizationUsersRequest(
                organization_id=organization_id,
                query=query,
                page_size=page_size,
                page_token=page_token,
            ),
        )

    def assign_user_roles(
        self,
        organization_id: str,
        user_id: str,
        roles: List[str],
    ) -> AssignUserRolesResponse:
        """
        Assign one or more roles to a user within an organization.

        When to use: Call when an org admin promotes a member to admin, or when your
        onboarding flow assigns a default role to a newly invited user.

        :param organization_id  : ID of the organization in which to assign the roles
        :type                   : ``` str ```
        :param user_id          : ID of the user to assign roles to
        :type                   : ``` str ```
        :param roles            : List of role name strings to assign (e.g. ["admin", "member"])
        :type                   : ``` list[str] ```

        :returns:
            AssignUserRolesResponse — roles (list of Role objects now active for the user
            in this organization)
        """
        from scalekit.v1.commons.commons_pb2 import Role
        role_objects = [Role(name=r) for r in roles]
        return self.core_client.grpc_exec(
            self.user_service.AssignUserRoles.with_call,
            AssignUserRolesRequest(
                organization_id=organization_id,
                user_id=user_id,
                roles=role_objects,
            ),
        )

    def remove_user_role(
        self,
        organization_id: str,
        user_id: str,
        role_name: str,
    ):
        """
        Remove a single role from a user within an organization.

        When to use: Call when demoting a user from admin to member, or when revoking
        a temporary elevated role after a task is complete.

        :param organization_id  : ID of the organization in which to remove the role
        :type                   : ``` str ```
        :param user_id          : ID of the user to remove the role from
        :type                   : ``` str ```
        :param role_name        : Name of the role to remove (e.g. "admin")
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.user_service.RemoveUserRole.with_call,
            RemoveUserRoleRequest(
                organization_id=organization_id,
                user_id=user_id,
                role_name=role_name,
            ),
        )


from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.users.users_pb2 import *
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
        :param send_invitation_email: Whether to send activation email to the user
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
        :param send_invitation_email: Whether to send activation email to the user
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
        :param send_invitation_email: Whether to send activation email to the user
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

   

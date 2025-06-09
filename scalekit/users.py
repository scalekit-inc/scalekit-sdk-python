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

    def create_user(self, organization_id: str, user: CreateUser) -> CreateUserResponse:
        """
        Method to create a new user

        :param organization_id  : Organization id to create user for
        :type                   : ``` str ```
        :param user            : CreateUser object with expected values for user creation
        :type                   : ``` obj ```

        :returns:
            Create User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.CreateUser.with_call,
            CreateUserRequest(organization_id=organization_id, user=user),
        )

    def update_user(self, organization_id: str, user: UpdateUser) -> UpdateUserResponse:
        """
        Method to update an existing user

        :param organization_id  : Organization id to update user for
        :type                   : ``` str ```
        :param user            : UpdateUser object with expected values for user update
        :type                   : ``` obj ```

        :returns:
            Update User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.UpdateUser.with_call,
            UpdateUserRequest(organization_id=organization_id, user=user),
        )

    def get_user(self, organization_id: str, user_id: str) -> GetUserResponse:
        """
        Method to get user based on given organization and user id

        :param organization_id  : Organization id to get user for
        :type                   : ``` str ```
        :param user_id         : User id to get user details
        :type                   : ``` str ```

        :returns:
            Get User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.GetUser.with_call,
            GetUserRequest(organization_id=organization_id, id=user_id),
        )

    def list_users(
        self,
        organization_id: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListUserResponse:
        """
        Method to list users for given organization id

        :param organization_id  : Organization id to list users for
        :type                   : ``` str ```
        :param page_size       : Page size for pagination
        :type                   : ``` int ```
        :param page_token      : Page token for pagination
        :type                   : ``` str ```

        :returns:
            List User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.ListUsers.with_call,
            ListUserRequest(
                organization_id=organization_id,
                page_size=page_size,
                page_token=page_token
            ),
        )

    def delete_user(self, organization_id: str, user_id: str):
        """
        Method to delete user based on given organization and user id

        :param organization_id  : Organization id to delete user for
        :type                   : ``` str ```
        :param user_id         : User id to be deleted
        :type                   : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.user_service.DeleteUser.with_call,
            DeleteUserRequest(organization_id=organization_id, id=user_id),
        )

    def add_user_to_organization(self, organization_id: str, user_id: str) -> AddUserResponse:
        """
        Method to add user to organization

        :param organization_id  : Organization id to add user to
        :type                   : ``` str ```
        :param user_id         : User id to be added
        :type                   : ``` str ```

        :returns:
            Add User Response
        """
        return self.core_client.grpc_exec(
            self.user_service.AddUserToOrganization.with_call,
            AddUserRequest(
                organization_id=organization_id,
                identities={
                    'case': 'id',
                    'value': user_id
                }
            ),
        ) 
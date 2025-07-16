from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.roles.roles_pb2 import *
from scalekit.v1.roles.roles_pb2_grpc import RolesServiceStub


class RoleClient:
    """Class definition for Role Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Role Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.role_service = RolesServiceStub(
            self.core_client.grpc_secure_channel
        )

    def create_role(
        self, 
        role: CreateRole
    ) -> CreateRoleResponse:
        """
        Method to create a new role

        :param role           : CreateRole object with expected values for role creation
        :type                 : ``` obj ```

        :returns:
            Create Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.CreateRole.with_call,
            CreateRoleRequest(role=role),
        )

    def get_role(self, role_id: str) -> GetRoleResponse:
        """
        Method to get role by ID

        :param role_id        : Role id to get role details
        :type                 : ``` str ```

        :returns:
            Get Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.GetRole.with_call,
            GetRoleRequest(id=role_id),
        )

    def list_roles(self) -> ListRolesResponse:
        """
        Method to list all roles

        :returns:
            List Roles Response
        """
        return self.core_client.grpc_exec(
            self.role_service.ListRoles.with_call,
            ListRolesRequest(),
        )

    def update_role(
        self, 
        role_id: str, 
        role: UpdateRole
    ) -> UpdateRoleResponse:
        """
        Method to update an existing role by ID

        :param role_id        : Role id to update
        :type                 : ``` str ```
        :param role           : UpdateRole object with expected values for role update
        :type                 : ``` obj ```

        :returns:
            Update Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.UpdateRole.with_call,
            UpdateRoleRequest(
                id=role_id,
                role=role
            ),
        )

    def delete_role(
        self, 
        role_id: str, 
        reassign_role_id: Optional[str] = None
    ):
        """
        Method to delete role by ID

        :param role_id        : Role id to be deleted
        :type                 : ``` str ```
        :param reassign_role_id: Role ID to reassign users to when deleting this role
        :type                 : ``` str ```

        :returns:
            None
        """
        request = DeleteRoleRequest(id=role_id)
        if reassign_role_id:
            request.reassign_role_id = reassign_role_id
            
        return self.core_client.grpc_exec(
            self.role_service.DeleteRole.with_call,
            request,
        )

    def get_role_users_count(
        self, 
        role_id: str
    ) -> GetRoleUsersCountResponse:
        """
        Method to get the count of users associated with a role

        :param role_id        : Role id to get user count for
        :type                 : ``` str ```

        :returns:
            Get Role Users Count Response
        """
        return self.core_client.grpc_exec(
            self.role_service.GetRoleUsersCount.with_call,
            GetRoleUsersCountRequest(id=role_id),
        )

 
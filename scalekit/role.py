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
        env_id: str, 
        role: CreateRole
    ) -> CreateRoleResponse:
        """
        Method to create a new role in the environment

        :param env_id         : Environment id to create role for
        :type                 : ``` str ```
        :param role           : CreateRole object with expected values for role creation
        :type                 : ``` obj ```

        :returns:
            Create Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.CreateRole.with_call,
            CreateRoleRequest(
                env_id=env_id,
                role=role
            ),
        )

    def get_role(self, env_id: str, role_id: str) -> GetRoleResponse:
        """
        Method to get role by ID

        :param env_id         : Environment id
        :type                 : ``` str ```
        :param role_id        : Role id to get role details
        :type                 : ``` str ```

        :returns:
            Get Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.GetRole.with_call,
            GetRoleRequest(
                env_id=env_id,
                id=role_id
            ),
        )

    def list_roles(self, env_id: str) -> ListRolesResponse:
        """
        Method to list all roles in environment

        :param env_id         : Environment id to list roles for
        :type                 : ``` str ```

        :returns:
            List Roles Response
        """
        return self.core_client.grpc_exec(
            self.role_service.ListRoles.with_call,
            ListRolesRequest(env_id=env_id),
        )

    def update_role(
        self, 
        env_id: str, 
        role_id: str, 
        role: UpdateRole
    ) -> UpdateRoleResponse:
        """
        Method to update an existing role by ID

        :param env_id         : Environment id
        :type                 : ``` str ```
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
                env_id=env_id,
                id=role_id,
                role=role
            ),
        )

    def delete_role(
        self, 
        env_id: str, 
        role_id: str, 
        reassign_role_id: Optional[str] = None
    ):
        """
        Method to delete role by ID

        :param env_id         : Environment id
        :type                 : ``` str ```
        :param role_id        : Role id to be deleted
        :type                 : ``` str ```
        :param reassign_role_id: Role ID to reassign users to when deleting this role
        :type                 : ``` str ```

        :returns:
            None
        """
        request = DeleteRoleRequest(
            env_id=env_id,
            id=role_id
        )
        if reassign_role_id:
            request.reassign_role_id = reassign_role_id
            
        return self.core_client.grpc_exec(
            self.role_service.DeleteRole.with_call,
            request,
        )

 
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

    def get_role(self, role_name: str) -> GetRoleResponse:
        """
        Method to get role by ID

        :param role_id        : Role id to get role details
        :type                 : ``` str ```

        :returns:
            Get Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.GetRole.with_call,
            GetRoleRequest(role_name=role_name),
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
        role_name: str, 
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
                role_name=role_name,
                role=role
            ),
        )

    def delete_role(
        self, 
        role_name: str, 
        reassign_role_name: Optional[str] = None
    ):
        """
        Method to delete role by ID

        :param role_id        : Role id to be deleted
        :type                 : ``` str ```
        :param reassign_role_name: Role name to reassign users to when deleting this role
        :type                 : ``` str ```

        :returns:
            None
        """
        request = DeleteRoleRequest(role_name=role_name)
        if reassign_role_name:
            request.reassign_role_name = reassign_role_name
            
        return self.core_client.grpc_exec(
            self.role_service.DeleteRole.with_call,
            request,
        )

    def get_role_users_count(
        self, 
        role_name: str
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
            GetRoleUsersCountRequest(role_name=role_name),
        )

 
    # Organization Role CRUD Methods
    
    def create_organization_role(
        self, 
        org_id: str,
        role: CreateOrganizationRole
    ) -> CreateOrganizationRoleResponse:
        """
        Method to create a new organization role

        :param org_id         : Organization ID
        :type                 : ``` str ```
        :param role           : CreateOrganizationRole object with expected values for role creation
        :type                 : ``` obj ```

        :returns:
            Create Organization Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.CreateOrganizationRole.with_call,
            CreateOrganizationRoleRequest(
                org_id=org_id,
                role=role
            ),
        )

    def get_organization_role(
        self, 
        org_id: str, 
        role_name: str
    ) -> GetOrganizationRoleResponse:
        """
        Method to get organization role by name

        :param org_id         : Organization ID
        :type                 : ``` str ```
        :param role_name      : Role name to get role details
        :type                 : ``` str ```

        :returns:
            Get Organization Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.GetOrganizationRole.with_call,
            GetOrganizationRoleRequest(
                org_id=org_id,
                role_name=role_name
            ),
        )

    def list_organization_roles(
        self, 
        org_id: str
    ) -> ListOrganizationRolesResponse:
        """
        Method to list all organization roles

        :param org_id         : Organization ID
        :type                 : ``` str ```

        :returns:
            List Organization Roles Response
        """
        return self.core_client.grpc_exec(
            self.role_service.ListOrganizationRoles.with_call,
            ListOrganizationRolesRequest(org_id=org_id),
        )

    def update_organization_role(
        self, 
        org_id: str,
        role_name: str, 
        role: UpdateRole
    ) -> UpdateOrganizationRoleResponse:
        """
        Method to update an existing organization role by name

        :param org_id         : Organization ID
        :type                 : ``` str ```
        :param role_name      : Role name to update
        :type                 : ``` str ```
        :param role           : UpdateOrganizationRole object with expected values for role update
        :type                 : ``` obj ```

        :returns:
            Update Organization Role Response
        """
        return self.core_client.grpc_exec(
            self.role_service.UpdateOrganizationRole.with_call,
            UpdateOrganizationRoleRequest(
                org_id=org_id,
                role_name=role_name,
                role=role
            ),
        )

    def delete_organization_role(
        self, 
        org_id: str,
        role_name: str, 
        reassign_role_name: Optional[str] = None
    ):
        """
        Method to delete organization role by name

        :param org_id         : Organization ID
        :type                 : ``` str ```
        :param role_name      : Role name to be deleted
        :type                 : ``` str ```
        :param reassign_role_name: Role name to reassign users to when deleting this role
        :type                 : ``` str ```

        :returns:
            None
        """
        request = DeleteOrganizationRoleRequest(
            org_id=org_id,
            role_name=role_name
        )
        if reassign_role_name:
            request.reassign_role_name = reassign_role_name
            
        return self.core_client.grpc_exec(
            self.role_service.DeleteOrganizationRole.with_call,
            request,
        )

    def get_organization_role_users_count(
        self, 
        org_id: str,
        role_name: str
    ) -> GetOrganizationRoleUsersCountResponse:
        """
        Method to get the count of users associated with an organization role

        :param org_id         : Organization ID
        :type                 : ``` str ```
        :param role_name      : Role name to get user count for
        :type                 : ``` str ```

        :returns:
            Get Organization Role Users Count Response
        """
        return self.core_client.grpc_exec(
            self.role_service.GetOrganizationRoleUsersCount.with_call,
            GetOrganizationRoleUsersCountRequest(
                org_id=org_id,
                role_name=role_name
            ),
        )

    def update_default_organization_roles(
        self, 
        org_id: str,
        default_roles: UpdateDefaultOrganizationRolesRequest
    ) -> UpdateDefaultOrganizationRolesResponse:
        """
        Method to update default organization roles

        :param org_id         : Organization ID
        :type                 : ``` str ```
        :param default_roles  : UpdateDefaultOrganizationRoles object with default role settings
        :type                 : ``` obj ```

        :returns:
            Update Default Organization Roles Response
        """
        return self.core_client.grpc_exec(
            self.role_service.UpdateDefaultOrganizationRoles.with_call,
            UpdateDefaultOrganizationRolesRequest(
                org_id=org_id,
                default_member_role=default_roles.default_member_role
            ),
        )

    def delete_organization_role_base(
        self, 
        org_id: str,
        role_name: str
    ):
        """
        Method to delete organization role base relationship by name

        :param org_id         : Organization ID
        :type                 : ``` str ```
        :param role_name      : Role name to remove base relationship for
        :type                 : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.role_service.DeleteOrganizationRoleBase.with_call,
            DeleteOrganizationRoleBaseRequest(
                org_id=org_id,
                role_name=role_name
            ),
        )

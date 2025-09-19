from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.roles.roles_pb2 import *
from scalekit.v1.roles.roles_pb2_grpc import RolesServiceStub


class PermissionClient:
    """Class definition for Permission Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Permission Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.role_service = RolesServiceStub(
            self.core_client.grpc_secure_channel
        )

    def create_permission(
        self, 
        permission: CreatePermission
    ) -> CreatePermissionResponse:
        """
        Method to create a new permission

        :param permission    : CreatePermission object with expected values for permission creation
        :type                : ``` obj ```

        :returns:
            Create Permission Response
        """
        return self.core_client.grpc_exec(
            self.role_service.CreatePermission.with_call,
            CreatePermissionRequest(permission=permission),
        )

    def get_permission(self, permission_name: str) -> GetPermissionResponse:
        """
        Method to get permission by name

        :param permission_name: Permission name to get permission details
        :type                 : ``` str ```

        :returns:
            Get Permission Response
        """
        return self.core_client.grpc_exec(
            self.role_service.GetPermission.with_call,
            GetPermissionRequest(permission_name=permission_name),
        )

    def list_permissions(
        self, 
        page_token: Optional[str] = None, 
        page_size: Optional[int] = None
    ) -> ListPermissionsResponse:
        """
        Method to list all permissions

        :param page_token    : Token for pagination
        :type                : ``` str ```
        :param page_size     : Number of permissions per page
        :type                : ``` int ```

        :returns:
            List Permissions Response
        """
        request = ListPermissionsRequest()
        if page_token:
            request.page_token = page_token
        if page_size:
            request.page_size = page_size
            
        return self.core_client.grpc_exec(
            self.role_service.ListPermissions.with_call,
            request,
        )

    def update_permission(
        self, 
        permission_name: str, 
        permission: CreatePermission
    ) -> UpdatePermissionResponse:
        """
        Method to update an existing permission by name

        :param permission_name: Permission name to update
        :type                 : ``` str ```
        :param permission     : CreatePermission object with expected values for permission update
        :type                 : ``` obj ```

        :returns:
            Update Permission Response
        """
        return self.core_client.grpc_exec(
            self.role_service.UpdatePermission.with_call,
            UpdatePermissionRequest(
                permission_name=permission_name,
                permission=permission
            ),
        )

    def delete_permission(self, permission_name: str):
        """
        Method to delete permission by name

        :param permission_name: Permission name to be deleted
        :type                 : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.role_service.DeletePermission.with_call,
            DeletePermissionRequest(permission_name=permission_name),
        )

    def list_role_permissions(
        self, 
        role_name: str
    ) -> ListRolePermissionsResponse:
        """
        Method to list all permissions associated with a role

        :param role_name      : Role name to get permissions for
        :type                 : ``` str ```

        :returns:
            List Role Permissions Response
        """
        return self.core_client.grpc_exec(
            self.role_service.ListRolePermissions.with_call,
            ListRolePermissionsRequest(role_name=role_name),
        )

    def add_permissions_to_role(
        self, 
        role_name: str, 
        permission_names: list[str]
    ):
        """
        Method to add permissions to a role

        :param role_name       : Role name to add permissions to
        :type                  : ``` str ```
        :param permission_names: List of permission names to add
        :type                  : ``` list[str] ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.role_service.AddPermissionsToRole.with_call,
            AddPermissionsToRoleRequest(
                role_name=role_name,
                permission_names=permission_names
            ),
        )

    def remove_permission_from_role(
        self, 
        role_name: str, 
        permission_name: str
    ):
        """
        Method to remove a permission from a role

        :param role_name       : Role name to remove permission from
        :type                  : ``` str ```
        :param permission_name : Permission name to remove
        :type                  : ``` str ```

        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.role_service.RemovePermissionFromRole.with_call,
            RemovePermissionFromRoleRequest(
                role_name=role_name,
                permission_name=permission_name
            ),
        )

    def list_effective_role_permissions(
        self, 
        role_name: str
    ) -> ListEffectiveRolePermissionsResponse:
        """
        Method to list all effective permissions for a role (including inherited permissions)

        :param role_name      : Role name to get effective permissions for
        :type                 : ``` str ```

        :returns:
            List Effective Role Permissions Response
        """
        return self.core_client.grpc_exec(
            self.role_service.ListEffectiveRolePermissions.with_call,
            ListEffectiveRolePermissionsRequest(role_name=role_name),
        ) 
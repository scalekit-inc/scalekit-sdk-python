from typing import Optional, List, Dict

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
        self.role_client = RolesServiceStub(
            self.core_client.grpc_secure_channel
        )

    def list_organization_roles(
            self, organization_id: str
    ) -> ListOrganizationRolesResponse:
        """
        Method to list organization roles

        :param organization_id  : organization id
        :type             : ``` str ```
        :returns:
             list of organization roles
        """
        return self.core_client.grpc_exec(
            self.role_client.ListOrganizationRoles.with_call,
            ListOrganizationRolesRequest(
                org_id=organization_id
            ),
        )

    def create_organization_role(
            self, organization_id: str, options: CreateRole
    ) -> CreateOrganizationRoleResponse:
        """
        Method to create role in an organization based on given data

        :param organization_id  : organization id
        :type           : ``` str ```
        :param options  : Additional details for org role to be created
        :type           : ``` obj ```
        :returns:
            Create Organization Role Response
        """
        return self.core_client.grpc_exec(
            self.role_client.CreateOrganizationRole.with_call,
            CreateOrganizationRoleRequest(
                role=options,
                org_id=organization_id
            ),
        )

    def update_organization_role(
            self, organization_id: str, role_id: str, role: UpdateRole
    ) -> UpdateOrganizationRoleResponse:
        """
        Method to update role in an organization based on given data

        :param organization_id       : Organization id of the role to update
        :type               : ``` str ```
        :param role_id : Role id to update
        :type               : ``` str ```
        :param role : Role object to update
        :type               : ``` obj ```
        :returns:
            Update Organization Role Response
        """
        return self.core_client.grpc_exec(
            self.role_client.UpdateOrganizationRole.with_call,
            UpdateOrganizationRoleRequest(
                org_id=organization_id,
                id=role_id,
                role=role
            ),
        )

    def delete_organization_role(
            self, organization_id: str, role_id: str
    ) -> UpdateOrganizationRoleResponse:
        """
        Method to delete role from an organization based on given data

        :param organization_id       : Organization id of the role to delete
        :type               : ``` str ```
        :param role_id : Role id to delete
        :type               : ``` str ```
        :returns:
            None
        """
        return self.core_client.grpc_exec(
            self.role_client.DeleteOrganizationRole.with_call,
            DeleteOrganizationRoleRequest(
                org_id=organization_id,
                id=role_id
            ),
        )

    def get_organization_role(
            self, organization_id: str, role_id: str
    ) -> GetOrganizationRoleResponse:
        """
        Method to get role in an organization based on given data

        :param organization_id       : Organization id of the role to delete
        :type               : ``` str ```
        :param role_id : Role id to delete
        :type               : ``` str ```
        :returns:
            Get Organization Response
        """
        return self.core_client.grpc_exec(
            self.role_client.GetOrganizationRole.with_call,
            GetOrganizationRoleRequest(
                org_id=organization_id,
                id=role_id
            ),
        )

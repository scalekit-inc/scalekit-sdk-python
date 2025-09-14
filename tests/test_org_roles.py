from faker import Faker

from scalekit.common.exceptions import ScalekitBadRequestException, ScalekitNotFoundException, ScalekitException
from tests.basetest import BaseTest

from scalekit.v1.roles.roles_pb2 import (
    CreateOrganizationRole,
    UpdateRole,
    UpdateDefaultOrganizationRolesRequest,
)
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestOrganizationRoles(BaseTest):
    """ Tests for Organization Role CRUD and related operations """

    def setUp(self):
        self.faker = Faker()
        self.org_id = None
        self.org_role_names = []

        # Always create a test organization for this test suite
        org_display_name = f"Test Organization {self.faker.unique.random_number()}"
        org = CreateOrganization(
            display_name=org_display_name,
            external_id=f"ext_{self.faker.unique.random_number()}"
        )
        org_response = self.scalekit_client.organization.create_organization(organization=org)
        self.org_id = org_response[0].organization.id

    def _create_org_role(self, role_name: str | None = None, display_name: str | None = None, extends: str | None = None):
        if role_name is None:
            role_name = f"test_org_role_{self.faker.unique.random_number()}"
        if display_name is None:
            display_name = f"Test Org Role {self.faker.unique.random_number()}"

        role = CreateOrganizationRole(
            name=role_name,
            display_name=display_name,
            description="Org role for testing"
        )
        if extends:
            role.extends = extends

        resp = self.scalekit_client.roles.create_organization_role(org_id=self.org_id, role=role)
        self.org_role_names.append(role_name)
        return role_name, resp

    def test_update_organization_role(self):
        # Create an organization role
        role_name, _ = self._create_org_role()

        # Update using UpdateRole (no name field here)
        updated_display_name = f"Updated Org Role {self.faker.unique.random_number()}"
        upd = UpdateRole(
            display_name=updated_display_name,
            description="Updated description"
        )
        resp = self.scalekit_client.roles.update_organization_role(
            org_id=self.org_id,
            role_name=role_name,
            role=upd,
        )
        self.assertEqual(resp[1].code().name, "OK")

        got = self.scalekit_client.roles.get_organization_role(org_id=self.org_id, role_name=role_name)
        self.assertEqual(got[0].role.display_name, updated_display_name)

    def test_update_default_organization_roles(self):
        # Create a role to set as default member
        role_name, _ = self._create_org_role()

        req = UpdateDefaultOrganizationRolesRequest(
            org_id=self.org_id,
            default_member_role=role_name,
        )
        resp = self.scalekit_client.roles.update_default_organization_roles(
            org_id=self.org_id,
            default_roles=req,
        )
        self.assertEqual(resp[1].code().name, "OK")

    # A couple of sanity tests to ensure surrounding APIs work
    def test_create_and_get_org_role(self):
        role_name, _ = self._create_org_role()
        got = self.scalekit_client.roles.get_organization_role(org_id=self.org_id, role_name=role_name)
        self.assertEqual(got[1].code().name, "OK")
        self.assertEqual(got[0].role.name, role_name)

    def test_delete_organization_role(self):
        role_name, _ = self._create_org_role()
        resp = self.scalekit_client.roles.delete_organization_role(org_id=self.org_id, role_name=role_name)
        self.assertEqual(resp[1].code().name, "OK")
        # Remove from cleanup tracker
        try:
            self.org_role_names.remove(role_name)
        except ValueError:
            pass

    def tearDown(self):
        # Cleanup roles then organization
        for rn in list(self.org_role_names):
            try:
                self.scalekit_client.roles.delete_organization_role(org_id=self.org_id, role_name=rn)
            except ScalekitNotFoundException:
                pass
            except Exception as exp:
                raise ScalekitException(f"Unexpected exception during org role cleanup: {exp}") from exp
            finally:
                try:
                    self.org_role_names.remove(rn)
                except ValueError:
                    pass

        if self.org_id:
            try:
                self.scalekit_client.organization.delete_organization(organization_id=self.org_id)
            except ScalekitNotFoundException:
                pass
            except Exception as exp:
                raise ScalekitException(f"Warning: Could not clean up organization {self.org_id}: {exp}")

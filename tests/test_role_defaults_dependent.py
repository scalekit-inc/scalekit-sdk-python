import os

from tests.basetest import BaseTest


class TestRoleDefaultsAndDependent(BaseTest):
    """ Class definition for Test Role Defaults and Dependent Roles """

    def test_update_default_roles_no_params(self):
        """ Method to test update_default_roles with no params (no-op update) """
        response = self.scalekit_client.role.update_default_roles()
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)

    def test_update_default_roles_with_member_role(self):
        """ Method to test update_default_roles setting default_member_role """
        # Restore the default after the test so environment state is not permanently mutated.
        # No getter exists for the current default, so we restore to the known baseline.
        self.addCleanup(
            self.scalekit_client.role.update_default_roles,
            default_member_role="member",
        )
        response = self.scalekit_client.role.update_default_roles(
            default_member_role="member"
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)

    def test_list_dependent_roles_member(self):
        """ Method to test list_dependent_roles for a known base role """
        role_name = os.environ.get("TEST_BASE_ROLE_NAME", "member")

        if not role_name:
            raise EnvironmentError("TEST_BASE_ROLE_NAME env var is required (or default 'member' must exist)")

        response = self.scalekit_client.role.list_dependent_roles(role_name=role_name)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        # roles field may be empty if no roles extend member — just assert the field exists
        self.assertIsInstance(list(response[0].roles), list)

    def test_list_dependent_roles_admin(self):
        """ Method to test list_dependent_roles for the admin base role """
        response = self.scalekit_client.role.list_dependent_roles(role_name="admin")
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertIsInstance(list(response[0].roles), list)

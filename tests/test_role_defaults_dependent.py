import os

from tests.basetest import BaseTest


class TestRoleDefaultsAndDependent(BaseTest):
    """ Class definition for Test Role Defaults and Dependent Roles """

    def test_update_default_roles_requires_both_params(self):
        """ Method to test update_default_roles requires both parameters """
        with self.assertRaises(ValueError) as ctx:
            self.scalekit_client.roles.update_default_roles()
        self.assertEqual(str(ctx.exception), "default_creator_role is required")

    def test_update_default_roles_with_both_roles(self):
        """ Method to test update_default_roles setting both default roles """
        # Restore the defaults after the test so environment state is not permanently mutated.
        # No getter exists for the current defaults, so we restore to the known baseline.
        self.addCleanup(
            self.scalekit_client.roles.update_default_roles,
            default_creator_role="admin",
            default_member_role="member",
        )
        response = self.scalekit_client.roles.update_default_roles(
            default_creator_role="admin",
            default_member_role="member"
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])

    def test_list_dependent_roles_member(self):
        """ Method to test list_dependent_roles for a known base role """
        role_name = os.environ.get("TEST_BASE_ROLE_NAME", "member")

        if not role_name:
            raise EnvironmentError("TEST_BASE_ROLE_NAME env var is required (or default 'member' must exist)")

        response = self.scalekit_client.roles.list_dependent_roles(role_name=role_name)
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        # roles field may be empty if no roles extend member — just assert the field exists
        roles = list(response[0].roles)
        self.assertIsInstance(roles, list)

    def test_list_dependent_roles_admin(self):
        """ Method to test list_dependent_roles for the admin base role """
        response = self.scalekit_client.roles.list_dependent_roles(role_name="admin")
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        roles = list(response[0].roles)
        self.assertIsInstance(roles, list)

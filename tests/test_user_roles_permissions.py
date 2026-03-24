from faker import Faker

from tests.basetest import BaseTest

from scalekit.v1.users.users_pb2 import CreateUser, CreateUserProfile
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization

from scalekit.common.exceptions import ScalekitNotFoundException


class TestUserRolesPermissions(BaseTest):
    """ Class definition for Test User Roles and Permissions Class """

    def setUp(self):
        """ """
        self.org_id = None
        self.user_id = None
        self.faker = Faker()

        # Create a test organization
        org_display_name = f"Test Organization {self.faker.unique.random_number()}"
        org = CreateOrganization(
            display_name=org_display_name,
            external_id=f"ext_{self.faker.uuid4()}"
        )
        org_response = self.scalekit_client.organization.create_organization(organization=org)
        self.org_id = org_response[0].organization.id

        # Create a test user in the organization
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email=f"test.user.{self.faker.unique.random_number()}@example.com",
            user_profile=user_profile,
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id,
            user=user
        )
        self.user_id = create_response[0].user.id

    def test_list_user_roles(self):
        """ Method to test list user roles """
        response = self.scalekit_client.users.list_user_roles(
            organization_id=self.org_id,
            user_id=self.user_id
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        # roles may be an empty list if none are assigned — just assert the field exists
        roles = list(response[0].roles)
        self.assertIsInstance(roles, list)

    def test_list_user_permissions(self):
        """ Method to test list user permissions """
        response = self.scalekit_client.users.list_user_permissions(
            organization_id=self.org_id,
            user_id=self.user_id
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        # permissions may be an empty list if none are granted — just assert the field exists
        permissions = list(response[0].permissions)
        self.assertIsInstance(permissions, list)

    def tearDown(self):
        """ Method to clean up """
        errors = []

        if self.user_id:
            try:
                self.scalekit_client.users.delete_membership(
                    organization_id=self.org_id,
                    user_id=self.user_id
                )
            except ScalekitNotFoundException:
                pass
            except Exception as exp:
                errors.append(exp)

            try:
                self.scalekit_client.users.delete_user(user_id=self.user_id)
            except Exception as exp:
                errors.append(exp)

        if self.org_id:
            try:
                self.scalekit_client.organization.delete_organization(organization_id=self.org_id)
            except Exception as exp:
                errors.append(exp)

        if errors:
            raise Exception(f"Errors during tearDown cleanup: {errors}")

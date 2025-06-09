import os
from faker import Faker
from basetest import BaseTest

from scalekit.v1.users.users_pb2 import User, UpdateUserRequest
from scalekit.v1.commons.commons_pb2 import UserProfile
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestUsers(BaseTest):
    """ Class definition for Test Users Class """

    def setUp(self):
        """ """
        self.org_id = os.getenv('testOrg')
        if not self.org_id:
            raise ValueError("testOrg environment variable is not set")
        self.user_id = None

    def test_create_user(self):
        """ Method to test create user """
        user = User(
            email="test.user@example.com",
            metadata={"source": "test"}
        )
        response = self.scalekit_client.users.create_user(organization_id=self.org_id, user=user)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.email, user.email)
        self.assertEqual(response[0].user.metadata["source"], user.metadata["source"])
        self.user_id = response[0].user.id

    def test_get_user(self):
        """ Method to test get user """
        user = User(
            email="test.user@example.com",
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user(organization_id=self.org_id, user=user)
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.get_user(organization_id=self.org_id, user_id=self.user_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.id, self.user_id)
        self.assertEqual(response[0].user.email, user.email)
        self.assertEqual(response[0].user.metadata["source"], user.metadata["source"])

    def test_update_user(self):
        """ Method to test update user """
        user = User(
            email="test.user@example.com",
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user(organization_id=self.org_id, user=user)
        self.user_id = create_response[0].user.id

        user_profile = UserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        update_user = UpdateUserRequest(user_profile=user_profile)
        response = self.scalekit_client.users.update_user(organization_id=self.org_id, user=update_user)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.id, self.user_id)
        self.assertEqual(response[0].user.user_profile.first_name, "Test")
        self.assertEqual(response[0].user.user_profile.last_name, "User")
        self.assertEqual(response[0].user.user_profile.name, "Test User")
        self.assertEqual(response[0].user.user_profile.locale, "en-US")

    def test_list_users(self):
        """ Method to test list users """
        user = User(
            email="test.user@example.com",
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user(organization_id=self.org_id, user=user)
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.list_users(organization_id=self.org_id, page_size=10)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].users) > 0)
        self.assertEqual(response[0].users[0].id, self.user_id)
        self.assertEqual(response[0].users[0].email, user.email)

        # Test pagination
        if response[0].next_page_token:
            paginated_response = self.scalekit_client.users.list_users(
                organization_id=self.org_id,
                page_size=5,
                page_token=response[0].next_page_token
            )
            self.assertEqual(paginated_response[1].code().name, "OK")
            self.assertTrue(paginated_response[0] is not None)
            self.assertTrue(len(paginated_response[0].users) > 0)

    def test_delete_user(self):
        """ Method to test delete user """
        user = User(
            email="test.user@example.com",
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user(organization_id=self.org_id, user=user)
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.delete_user(organization_id=self.org_id, user_id=self.user_id)
        self.assertEqual(response[1].code().name, "OK")

        try:
            self.scalekit_client.users.get_user(organization_id=self.org_id, user_id=self.user_id)
        except Exception as e:
            self.assertEqual(e.args[0], "user not found")
            self.user_id = None

    def test_add_user_to_organization(self):
        """ Method to test add user to organization """
        user = User(
            email="test.user@example.com",
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user(organization_id=self.org_id, user=user)
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.add_user_to_organization(
            organization_id=self.org_id,
            user_id=self.user_id
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.id, self.user_id)
        self.assertEqual(response[0].user.email, user.email)

    def tearDown(self):
        """ Method to clean up """
        if self.user_id:
            try:
                self.scalekit_client.users.delete_user(organization_id=self.org_id, user_id=self.user_id)
            except Exception:
                pass
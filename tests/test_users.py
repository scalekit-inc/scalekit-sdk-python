import os
from faker import Faker
from basetest import BaseTest

from scalekit.v1.users.users_pb2 import CreateUser, UpdateUser, CreateUserProfile, UpdateUserProfile, CreateMembership
from scalekit.v1.commons.commons_pb2 import UserProfile


class TestUsers(BaseTest):
    """ Class definition for Test Users Class """

    def setUp(self):
        """ """
        self.org_id = os.getenv('testOrg')
        if not self.org_id:
            raise ValueError("testOrg environment variable is not set")
        self.user_id = None

    def test_create_user_and_membership(self):
        """ Method to test create user and membership """
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.email, user.email)
        self.assertEqual(response[0].user.metadata["source"], user.metadata["source"])
        self.user_id = response[0].user.id

    def test_get_user(self):
        """ Method to test get user """
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.get_user(user_id=self.user_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.id, self.user_id)
        self.assertEqual(response[0].user.email, user.email)
        self.assertEqual(response[0].user.metadata["source"], user.metadata["source"])

    def test_get_user_by_external_id(self):
        """ Method to test get user by external ID """
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            external_id="ext_test_123",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        external_id = create_response[0].user.external_id

        response = self.scalekit_client.users.get_user_by_external_id(external_id=external_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.external_id, external_id)
        self.assertEqual(response[0].user.email, user.email)

    def test_update_user(self):
        """ Method to test update user """
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.user_id = create_response[0].user.id

        update_user_profile = UpdateUserProfile(
            first_name="Updated",
            last_name="User",
            name="Updated User",
            locale="en-US"
        )
        update_user = UpdateUser(
            user_profile=update_user_profile,
            metadata={"source": "updated_test"}
        )
        response = self.scalekit_client.users.update_user(user_id=self.user_id, user=update_user)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.id, self.user_id)
        self.assertEqual(response[0].user.user_profile.first_name, "Updated")
        self.assertEqual(response[0].user.user_profile.last_name, "User")
        self.assertEqual(response[0].user.user_profile.name, "Updated User")
        self.assertEqual(response[0].user.user_profile.locale, "en-US")
        self.assertEqual(response[0].user.metadata["source"], "updated_test")

    def test_list_users(self):
        """ Method to test list users """
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.list_users(page_size=10)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].users) > 0)

        # Test pagination
        if response[0].next_page_token:
            paginated_response = self.scalekit_client.users.list_users(
                page_size=5,
                page_token=response[0].next_page_token
            )
            self.assertEqual(paginated_response[1].code().name, "OK")
            self.assertTrue(paginated_response[0] is not None)
            self.assertTrue(len(paginated_response[0].users) > 0)

    def test_list_organization_users(self):
        """ Method to test list organization users """
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.list_organization_users(
            organization_id=self.org_id, 
            page_size=10
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].users) > 0)

        # Test pagination
        if response[0].next_page_token:
            paginated_response = self.scalekit_client.users.list_organization_users(
                organization_id=self.org_id,
                page_size=5,
                page_token=response[0].next_page_token
            )
            self.assertEqual(paginated_response[1].code().name, "OK")
            self.assertTrue(paginated_response[0] is not None)
            self.assertTrue(len(paginated_response[0].users) > 0)

    def test_delete_user(self):
        """ Method to test delete user """
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.user_id = create_response[0].user.id

        response = self.scalekit_client.users.delete_user(user_id=self.user_id)
        self.assertEqual(response[1].code().name, "OK")

        try:
            self.scalekit_client.users.get_user(user_id=self.user_id)
        except Exception as e:
            self.assertEqual(e.args[0], "user not found")
            self.user_id = None

    def test_create_membership(self):
        """ Method to test create membership """
        # First create a user without membership
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email="test.user@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        create_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.user_id = create_response[0].user.id

        # Create membership for the user
        membership = CreateMembership(
            roles=[],
            metadata={"department": "engineering"}
        )
        response = self.scalekit_client.users.create_membership(
            organization_id=self.org_id,
            user_id=self.user_id,
            membership=membership
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].user.id, self.user_id)
   

    def tearDown(self):
        """ Method to clean up """
        if self.user_id:
            try:
                self.scalekit_client.users.delete_user(user_id=self.user_id)
            except Exception:
                pass
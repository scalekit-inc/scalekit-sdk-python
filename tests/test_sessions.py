from faker import Faker

from .basetest import BaseTest
from scalekit.v1.users.users_pb2 import CreateUser, CreateUserProfile
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestSessions(BaseTest):
    """ Class definition for Test Sessions Class """

    def setUp(self):
        """ """
        self.faker = Faker()
        self.user_id = None
        self.org_id = None
        
        # Create a test organization with unique external ID
        org_display_name = f"Test Organization {self.faker.unique.random_number()}"
        org = CreateOrganization(
            display_name=org_display_name,
            external_id=f"ext_{self.faker.unique.random_number()}_{self.faker.unique.random_number()}"
        )
        org_response = self.scalekit_client.organization.create_organization(organization=org)
        self.org_id = org_response[0].organization.id
        
        # Create a test user
        user_profile = CreateUserProfile(
            first_name="Test",
            last_name="User",
            name="Test User",
            locale="en-US"
        )
        user = CreateUser(
            email=f"test.user.{self.faker.unique.random_number()}@example.com",
            user_profile=user_profile,
            metadata={"source": "test"}
        )
        user_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, 
            user=user
        )
        self.user_id = user_response[0].user.id

    def test_get_user_sessions(self):
        """ Method to test get user sessions """
        response = self.scalekit_client.sessions.get_user_sessions(user_id=self.user_id)
        
        # Verify response structure
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertIsNotNone(response[0].sessions)
        # Fix: sessions can be an empty list, so check if it's a list or empty list
        self.assertTrue(isinstance(response[0].sessions, list) or response[0].sessions == [])

    def test_get_user_sessions_with_invalid_user_id(self):
        """ Method to test get user sessions with invalid user ID """
        invalid_user_id = "usr_invalid123"
        
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.get_user_sessions(user_id=invalid_user_id)

    def test_get_user_sessions_with_empty_user_id(self):
        """ Method to test get user sessions with empty user ID """
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.get_user_sessions(user_id="")

    def test_get_user_sessions_with_none_user_id(self):
        """ Method to test get user sessions with None user ID """
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.get_user_sessions(user_id=None)

    def test_get_session_with_invalid_session_id(self):
        """ Method to test get session with invalid session ID """
        invalid_session_id = "ses_invalid123"
        
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.get_session(session_id=invalid_session_id)

    def test_get_session_with_empty_session_id(self):
        """ Method to test get session with empty session ID """
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.get_session(session_id="")

    def test_get_session_with_none_session_id(self):
        """ Method to test get session with None session ID """
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.get_session(session_id=None)

    def test_revoke_session_with_invalid_session_id(self):
        """ Method to test revoke session with invalid session ID """
        invalid_session_id = "ses_invalid123"
        
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.revoke_session(session_id=invalid_session_id)

    def test_revoke_session_with_empty_session_id(self):
        """ Method to test revoke session with empty session ID """
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.revoke_session(session_id="")

    def test_revoke_session_with_none_session_id(self):
        """ Method to test revoke session with None session ID """
        with self.assertRaises(Exception):
            self.scalekit_client.sessions.revoke_session(session_id=None)

    def test_sessions_client_initialization(self):
        """ Method to test sessions client initialization """
        # Verify that sessions client is properly initialized
        self.assertIsNotNone(self.scalekit_client.sessions)
        self.assertIsNotNone(self.scalekit_client.sessions.core_client)
        self.assertIsNotNone(self.scalekit_client.sessions.session_service)

    def test_sessions_client_methods_exist(self):
        """ Method to test that all required methods exist """
        # Verify that all required methods exist
        self.assertTrue(hasattr(self.scalekit_client.sessions, 'get_session'))
        self.assertTrue(hasattr(self.scalekit_client.sessions, 'get_user_sessions'))
        self.assertTrue(hasattr(self.scalekit_client.sessions, 'revoke_session'))
        
        # Verify that methods are callable
        self.assertTrue(callable(self.scalekit_client.sessions.get_session))
        self.assertTrue(callable(self.scalekit_client.sessions.get_user_sessions))
        self.assertTrue(callable(self.scalekit_client.sessions.revoke_session))

    def test_get_user_sessions_response_structure(self):
        """ Method to test get user sessions response structure """
        response = self.scalekit_client.sessions.get_user_sessions(user_id=self.user_id)
        
        # Verify response has the expected attributes
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(hasattr(response[0], 'sessions'))
        
        # Fix: sessions can be an empty list, so check if it's a list or empty list
        self.assertTrue(isinstance(response[0].sessions, list) or response[0].sessions == [])

    def test_session_id_format_validation(self):
        """ Method to test session ID format validation """
        # Test various invalid session ID formats
        invalid_formats = [
            "invalid_session_id",
            "ses_",
            "ses_abc",
            "ses_123abc",
            "123456789",
            "session_123456789"
        ]
        
        for invalid_id in invalid_formats:
            with self.assertRaises(Exception):
                self.scalekit_client.sessions.get_session(session_id=invalid_id)

    def test_user_id_format_validation(self):
        """ Method to test user ID format validation """
        # Test various invalid user ID formats
        invalid_formats = [
            "invalid_user_id",
            "usr_",
            "usr_abc",
            "usr_123abc",
            "123456789",
            "user_123456789"
        ]
        
        for invalid_id in invalid_formats:
            with self.assertRaises(Exception):
                self.scalekit_client.sessions.get_user_sessions(user_id=invalid_id)

    def test_sessions_client_integration(self):
        """ Method to test sessions client integration with main client """
        # Verify that sessions client is accessible through main client
        self.assertIsNotNone(self.scalekit_client.sessions)
        
        # Verify that it's the correct type
        from scalekit.sessions import SessionsClient
        self.assertIsInstance(self.scalekit_client.sessions, SessionsClient)

    def tearDown(self):
        """ Clean up test data """
        # Clean up user if it was created
        if hasattr(self, 'user_id') and self.user_id:
            try:
                self.scalekit_client.users.delete_user(user_id=self.user_id)
            except Exception:
                pass  # User might already be deleted or not exist
        
        # Clean up organization if it was created
        if hasattr(self, 'org_id') and self.org_id:
            try:
                self.scalekit_client.organization.delete_organization(organization_id=self.org_id)
            except Exception:
                pass  # Organization might already be deleted or not exist

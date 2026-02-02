from faker import Faker

from basetest import BaseTest
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestTokens(BaseTest):
    """Class definition for Test Tokens Class"""

    def setUp(self):
        """Set up test fixtures"""
        self.org_id = None
        self.token_id = None
        # Create a test organization for token tests
        organization = CreateOrganization(
            display_name=Faker().company(), external_id=Faker().uuid4()
        )
        org_response = self.scalekit_client.organization.create_organization(
            organization=organization
        )
        self.org_id = org_response[0].organization.id

    def test_create_token(self):
        """Method to test create token"""
        description = "Test API Token"
        custom_claims = {"env": "test", "scope": "read"}

        response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description=description,
            custom_claims=custom_claims,
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(response[0].token is not None)
        self.assertTrue(response[0].token_id is not None)
        self.assertTrue(response[0].token_id.startswith("apit_"))
        self.token_id = response[0].token_id

    def test_create_token_with_user_id(self):
        """Method to test create token scoped to a user"""
        # First create a user
        from scalekit.v1.users.users_pb2 import CreateUser

        user = CreateUser(email=Faker().email())
        user_response = self.scalekit_client.users.create_user(
            organization_id=self.org_id, user=user
        )
        user_id = user_response[0].user.id

        response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            user_id=user_id,
            description="User scoped token",
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(response[0].token is not None)
        self.token_id = response[0].token_id

    def test_validate_token(self):
        """Method to test validate token"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token to validate",
        )
        self.token_id = create_response[0].token_id
        opaque_token = create_response[0].token

        # Validate using opaque token
        response = self.scalekit_client.tokens.validate_token(token=opaque_token)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(response[0].token_info is not None)
        self.assertEqual(response[0].token_info.organization_id, self.org_id)

    def test_validate_token_by_id(self):
        """Method to test validate token by token_id"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token to validate by ID",
        )
        self.token_id = create_response[0].token_id

        # Validate using token_id
        response = self.scalekit_client.tokens.validate_token(token=self.token_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(response[0].token_info is not None)

    def test_list_tokens(self):
        """Method to test list tokens"""
        # Create a token first
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token for list test",
        )
        self.token_id = create_response[0].token_id

        # List tokens for the organization
        response = self.scalekit_client.tokens.list_tokens(
            organization_id=self.org_id, page_size=10
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].tokens) > 0)
        self.assertTrue(response[0].total_count > 0)

    def test_list_tokens_with_pagination(self):
        """Method to test list tokens with pagination"""
        # Create multiple tokens
        for i in range(3):
            self.scalekit_client.tokens.create_token(
                organization_id=self.org_id,
                description=f"Token {i} for pagination test",
            )

        # List with small page size
        response = self.scalekit_client.tokens.list_tokens(
            organization_id=self.org_id, page_size=2
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(len(response[0].tokens) <= 2)

    def test_invalidate_token(self):
        """Method to test invalidate token"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token to invalidate",
        )
        token_id = create_response[0].token_id

        # Invalidate the token
        response = self.scalekit_client.tokens.invalidate_token(token=token_id)
        self.assertEqual(response[1].code().name, "OK")

        # Token should not be in the list anymore
        list_response = self.scalekit_client.tokens.list_tokens(
            organization_id=self.org_id
        )
        token_ids = [t.token_id for t in list_response[0].tokens]
        self.assertNotIn(token_id, token_ids)
        self.token_id = None  # Already invalidated

    def test_invalidate_token_idempotent(self):
        """Method to test invalidate token is idempotent"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token for idempotent test",
        )
        token_id = create_response[0].token_id

        # Invalidate the token twice
        response1 = self.scalekit_client.tokens.invalidate_token(token=token_id)
        self.assertEqual(response1[1].code().name, "OK")

        response2 = self.scalekit_client.tokens.invalidate_token(token=token_id)
        self.assertEqual(response2[1].code().name, "OK")
        self.token_id = None  # Already invalidated

    def tearDown(self):
        """Method to clean up after test"""
        # Invalidate token if it exists
        if self.token_id:
            try:
                self.scalekit_client.tokens.invalidate_token(token=self.token_id)
            except Exception:
                pass
        # Delete the test organization
        if self.org_id:
            self.scalekit_client.organization.delete_organization(
                organization_id=self.org_id
            )

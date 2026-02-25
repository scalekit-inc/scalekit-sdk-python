import logging

from faker import Faker

from basetest import BaseTest
from scalekit.common.exceptions import ScalekitServerException, ScalekitValidateTokenFailureException
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization

logger = logging.getLogger(__name__)


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
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.token)
        self.assertIsNotNone(response.token_id)
        self.assertTrue(response.token_id.startswith("apit_"))
        self.token_id = response.token_id

    def test_create_token_with_custom_claims(self):
        """Method to test create token with custom claims"""
        custom_claims = {"team": "engineering", "environment": "test"}

        response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token with custom claims",
            custom_claims=custom_claims,
        )
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.token)
        self.assertTrue(response.token_id.startswith("apit_"))
        self.assertEqual(
            response.token_info.custom_claims["team"], "engineering"
        )
        self.assertEqual(
            response.token_info.custom_claims["environment"], "test"
        )
        self.token_id = response.token_id

    def test_create_token_with_user_id(self):
        """Method to test create token scoped to a user"""
        # Create a user with active membership (sendInvitationEmail=False)
        from scalekit.v1.users.users_pb2 import CreateUser

        user = CreateUser(email=Faker().email())
        user_response = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user, send_invitation_email=False
        )
        user_id = user_response[0].user.id

        response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            user_id=user_id,
            description="User scoped token",
        )
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.token)
        self.token_id = response.token_id

    def test_validate_token(self):
        """Method to test validate token"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token to validate",
        )
        self.token_id = create_response.token_id
        opaque_token = create_response.token

        # Validate using opaque token
        response = self.scalekit_client.tokens.validate_token(token=opaque_token)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.token_info)
        self.assertEqual(response.token_info.organization_id, self.org_id)

    def test_validate_token_by_id(self):
        """Method to test validate token by token_id"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token to validate by ID",
        )
        self.token_id = create_response.token_id

        # Validate using token_id
        response = self.scalekit_client.tokens.validate_token(token=self.token_id)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.token_info)

    def test_list_tokens(self):
        """Method to test list tokens"""
        # Create a token first
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token for list test",
        )
        self.token_id = create_response.token_id

        # List tokens for the organization
        response = self.scalekit_client.tokens.list_tokens(
            organization_id=self.org_id, page_size=10
        )
        self.assertIsNotNone(response)
        self.assertTrue(len(response.tokens) > 0)
        self.assertTrue(response.total_count > 0)

    def test_list_tokens_with_pagination(self):
        """Method to test list tokens with pagination"""
        # Create multiple tokens
        for i in range(3):
            self.scalekit_client.tokens.create_token(
                organization_id=self.org_id,
                description=f"Token {i} for pagination test",
            )

        # List with page size 1
        page1 = self.scalekit_client.tokens.list_tokens(
            organization_id=self.org_id, page_size=1
        )
        self.assertEqual(len(page1.tokens), 1)
        self.assertTrue(page1.next_page_token)

        # Get next page
        page2 = self.scalekit_client.tokens.list_tokens(
            organization_id=self.org_id,
            page_size=1,
            page_token=page1.next_page_token,
        )
        self.assertEqual(len(page2.tokens), 1)

        # Ensure different tokens on different pages
        self.assertNotEqual(
            page1.tokens[0].token_id, page2.tokens[0].token_id
        )

    def test_invalidate_token(self):
        """Method to test invalidate token"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token to invalidate",
        )
        token_id = create_response.token_id

        # Invalidate the token
        self.scalekit_client.tokens.invalidate_token(token=token_id)

        # Verify token is no longer valid
        with self.assertRaises(ScalekitValidateTokenFailureException):
            self.scalekit_client.tokens.validate_token(token=token_id)
        self.token_id = None  # Already invalidated

    def test_invalidate_token_idempotent(self):
        """Method to test invalidate token is idempotent"""
        # First create a token
        create_response = self.scalekit_client.tokens.create_token(
            organization_id=self.org_id,
            description="Token for idempotent test",
        )
        token_id = create_response.token_id

        # Invalidate the token twice — both should succeed without error
        self.scalekit_client.tokens.invalidate_token(token=token_id)
        self.scalekit_client.tokens.invalidate_token(token=token_id)
        self.token_id = None  # Already invalidated

    # ------------------------------------------------------------------
    # Validation guard tests — no live backend call required
    # ------------------------------------------------------------------

    def test_create_token_raises_on_empty_organization_id(self):
        """create_token should raise ValueError with 'Invalid organization_id' when organization_id is empty"""
        with self.assertRaises(ValueError) as ctx:
            self.scalekit_client.tokens.create_token(organization_id="")
        self.assertEqual(str(ctx.exception), "Invalid organization_id")

    def test_validate_token_raises_on_empty_token(self):
        """validate_token should raise ValueError with 'Invalid token' when token is empty"""
        with self.assertRaises(ValueError) as ctx:
            self.scalekit_client.tokens.validate_token(token="")
        self.assertEqual(str(ctx.exception), "Invalid token")

    def test_invalidate_token_raises_on_empty_token(self):
        """invalidate_token should raise ValueError with 'Invalid token' when token is empty"""
        with self.assertRaises(ValueError) as ctx:
            self.scalekit_client.tokens.invalidate_token(token="")
        self.assertEqual(str(ctx.exception), "Invalid token")

    def test_list_tokens_raises_on_empty_organization_id(self):
        """list_tokens should raise ValueError with 'Invalid organization_id' when organization_id is empty"""
        with self.assertRaises(ValueError) as ctx:
            self.scalekit_client.tokens.list_tokens(organization_id="")
        self.assertEqual(str(ctx.exception), "Invalid organization_id")

    def tearDown(self):
        """Method to clean up after test"""
        # Invalidate token if it exists
        if self.token_id:
            try:
                self.scalekit_client.tokens.invalidate_token(token=self.token_id)
            except ScalekitServerException as e:
                logger.error("tearDown: failed to invalidate token %s: %s", self.token_id, e)
        # Delete the test organization
        if self.org_id:
            try:
                self.scalekit_client.organization.delete_organization(
                    organization_id=self.org_id
                )
            except ScalekitServerException as e:
                logger.error("tearDown: failed to delete organization %s: %s", self.org_id, e)

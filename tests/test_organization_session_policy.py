from faker import Faker

from basetest import BaseTest
from scalekit.v1.organizations.organizations_pb2 import (
    CreateOrganization,
    SessionPolicyType,
)
from scalekit.v1.commons.commons_pb2 import TimeUnit


class TestOrganizationSessionPolicy(BaseTest):
    """Test cases for organization session policy management."""

    def setUp(self):
        self.org_id = None

    def _create_org(self):
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = response[0].organization.id
        return self.org_id

    def test_get_default_policy(self):
        """New org should inherit APPLICATION policy by default."""
        org_id = self._create_org()

        policy = self.scalekit_client.organization.get_organization_session_policy(
            organization_id=org_id
        )[0].policy

        self.assertIsNotNone(policy)
        self.assertEqual(policy.policy_source, SessionPolicyType.APPLICATION)

    def test_set_custom_policy(self):
        """Setting a custom policy should persist and be retrievable."""
        org_id = self._create_org()

        policy = self.scalekit_client.organization.update_organization_session_policy(
            organization_id=org_id,
            policy_source=SessionPolicyType.CUSTOM,
            absolute_session_timeout=360,
            absolute_session_timeout_unit=TimeUnit.MINUTES,
            idle_session_timeout_enabled=True,
            idle_session_timeout=60,
            idle_session_timeout_unit=TimeUnit.MINUTES,
        )[0].policy

        self.assertIsNotNone(policy)
        self.assertEqual(policy.policy_source, SessionPolicyType.CUSTOM)

        fetched = self.scalekit_client.organization.get_organization_session_policy(
            organization_id=org_id
        )[0].policy
        self.assertEqual(fetched.policy_source, SessionPolicyType.CUSTOM)
        self.assertTrue(fetched.HasField("absolute_session_timeout"))
        self.assertEqual(fetched.absolute_session_timeout.value, 360)
        self.assertTrue(fetched.HasField("idle_session_timeout_enabled"))
        self.assertTrue(fetched.idle_session_timeout_enabled.value)

    def test_revert_to_application_policy(self):
        """Setting policy source to APPLICATION should revert to application defaults."""
        org_id = self._create_org()

        self.scalekit_client.organization.update_organization_session_policy(
            organization_id=org_id,
            policy_source=SessionPolicyType.CUSTOM,
            absolute_session_timeout=120,
            absolute_session_timeout_unit=TimeUnit.MINUTES,
        )

        reverted = self.scalekit_client.organization.update_organization_session_policy(
            organization_id=org_id,
            policy_source=SessionPolicyType.APPLICATION,
        )[0].policy

        self.assertIsNotNone(reverted)
        self.assertEqual(reverted.policy_source, SessionPolicyType.APPLICATION)

        fetched = self.scalekit_client.organization.get_organization_session_policy(
            organization_id=org_id
        )[0].policy
        self.assertEqual(fetched.policy_source, SessionPolicyType.APPLICATION)

    def test_set_idle_timeout_disabled(self):
        """Setting idle_session_timeout_enabled=False should persist as false."""
        org_id = self._create_org()

        policy = self.scalekit_client.organization.update_organization_session_policy(
            organization_id=org_id,
            policy_source=SessionPolicyType.CUSTOM,
            absolute_session_timeout=480,
            absolute_session_timeout_unit=TimeUnit.MINUTES,
            idle_session_timeout_enabled=False,
        )[0].policy

        self.assertIsNotNone(policy)
        self.assertEqual(policy.policy_source, SessionPolicyType.CUSTOM)

        fetched = self.scalekit_client.organization.get_organization_session_policy(
            organization_id=org_id
        )[0].policy
        self.assertTrue(fetched.HasField("idle_session_timeout_enabled"))
        self.assertFalse(fetched.idle_session_timeout_enabled.value)

    def tearDown(self):
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

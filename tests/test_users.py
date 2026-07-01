
from faker import Faker
from basetest import BaseTest

from scalekit.v1.users.users_pb2 import (
    CreateUser, UpdateUser, CreateUserProfile, UpdateUserProfile,
    CreateMembership, UpdateMembership,
)
from scalekit.v1.commons.commons_pb2 import Role
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization

from scalekit.common.exceptions import ScalekitNotFoundException, ScalekitBadRequestException


class TestUsers(BaseTest):
    """Integration tests for the Users API.

    Scenario: Acme Corp syncs employees from Workday (their HR system) via SCIM.
    Tests model real provisioning flows: onboarding with full profiles, multi-org
    access grants, role promotions after reorgs, and deprovisioning.
    """

    # Fixed profile constants — deterministic across all tests
    _FIRST_NAME = "Alice"
    _LAST_NAME = "Johnson"
    _FULL_NAME = "Alice Johnson"
    _LOCALE = "en-US"
    _PHONE = "+14155550147"
    _GENDER = "Female"
    _PREFERRED_USERNAME = "alicej"
    _DEPARTMENT = "Engineering"
    _COST_CENTER = "CC-1024"

    def setUp(self):
        self.user_id = None
        self.external_id = None
        self.faker = Faker()

        org = CreateOrganization(
            display_name=f"Acme Corp {self.faker.unique.random_number()}",
            external_id=f"workday_org_{self.faker.uuid4()}",
        )
        self.org_id = self.scalekit_client.organization.create_organization(
            organization=org
        )[0].organization.id

    # -------------------------------------------------------------------------
    # Helpers — request builders
    # -------------------------------------------------------------------------

    def _make_user_profile(self) -> CreateUserProfile:
        return CreateUserProfile(
            first_name=self._FIRST_NAME,
            last_name=self._LAST_NAME,
            given_name=self._FIRST_NAME,
            family_name=self._LAST_NAME,
            name=self._FULL_NAME,
            locale=self._LOCALE,
            phone_number=self._PHONE,
            preferred_username=self._PREFERRED_USERNAME,
            gender=self._GENDER,
            custom_attributes={
                "department": self._DEPARTMENT,
                "cost_center": self._COST_CENTER,
                "employee_type": "full-time",
            },
        )

    def _make_create_user(self, with_external_id: bool = False) -> CreateUser:
        suffix = self.faker.unique.random_number()
        kwargs = dict(
            email=f"alice.johnson.{suffix}@acme-corp.example.com",
            user_profile=self._make_user_profile(),
            metadata={
                "source": "workday_scim",
                "sync_version": "2024-01-15",
                "employee_id": f"EMP-{suffix}",
            },
        )
        if with_external_id:
            kwargs["external_id"] = f"workday_usr_AJ_{suffix}"
        return CreateUser(**kwargs)

    def _make_updated_profile(self) -> UpdateUserProfile:
        """Profile after a department transfer and legal name change."""
        return UpdateUserProfile(
            first_name="Alice",
            last_name="Johnson-Smith",
            given_name="Alice",
            family_name="Johnson-Smith",
            name="Alice Johnson-Smith",
            locale="en-GB",
            phone_number="+442079460101",
            preferred_username="ajohnsonsmith",
            gender="Female",
            custom_attributes={
                "department": "Security",
                "cost_center": "CC-2048",
                "employee_type": "full-time",
            },
        )

    # -------------------------------------------------------------------------
    # Helpers — response assertions
    # -------------------------------------------------------------------------

    def _assert_user_core(self, u, *, email, user_id=None, external_id=None):
        """Assert identity and system fields that every User response must have."""
        self.assertIsNotNone(u.id)
        self.assertIsNotNone(u.environment_id)
        self.assertIsNotNone(u.create_time)
        self.assertEqual(u.email, email)
        if user_id is not None:
            self.assertEqual(u.id, user_id)
        if external_id is not None:
            self.assertEqual(u.external_id, external_id)

    def _assert_original_profile(self, u):
        """Assert all profile fields match the original Alice Johnson onboarding data."""
        self.assertEqual(u.user_profile.first_name, self._FIRST_NAME)
        self.assertEqual(u.user_profile.last_name, self._LAST_NAME)
        self.assertEqual(u.user_profile.name, self._FULL_NAME)
        self.assertEqual(u.user_profile.locale, self._LOCALE)
        self.assertEqual(u.user_profile.phone_number, self._PHONE)
        self.assertEqual(u.user_profile.preferred_username, self._PREFERRED_USERNAME)
        self.assertEqual(u.user_profile.gender, self._GENDER)
        self.assertEqual(u.user_profile.custom_attributes["department"], self._DEPARTMENT)
        self.assertEqual(u.user_profile.custom_attributes["cost_center"], self._COST_CENTER)

    def _assert_updated_profile(self, u):
        """Assert all profile fields match the post-reorg update (Johnson-Smith, Security team)."""
        self.assertEqual(u.user_profile.first_name, "Alice")
        self.assertEqual(u.user_profile.last_name, "Johnson-Smith")
        self.assertEqual(u.user_profile.name, "Alice Johnson-Smith")
        self.assertEqual(u.user_profile.locale, "en-GB")
        self.assertEqual(u.user_profile.phone_number, "+442079460101")
        self.assertEqual(u.user_profile.preferred_username, "ajohnsonsmith")
        self.assertEqual(u.user_profile.gender, "Female")
        self.assertEqual(u.user_profile.custom_attributes["department"], "Security")
        self.assertEqual(u.user_profile.custom_attributes["cost_center"], "CC-2048")

    def _assert_original_metadata(self, u):
        self.assertEqual(u.metadata["source"], "workday_scim")
        self.assertEqual(u.metadata["sync_version"], "2024-01-15")
        self.assertIn("employee_id", u.metadata)

    def _assert_roles(self, org_id: str, user_id: str, expected_role: str):
        """Verify a user's roles in an org via the dedicated list_user_roles endpoint."""
        roles_resp, status = self.scalekit_client.users.list_user_roles(
            organization_id=org_id, user_id=user_id
        )
        self.assertEqual(status.code().name, "OK")
        role_names = [r.name for r in roles_resp.roles]
        self.assertIn(expected_role, role_names)

    def _assert_user_in_org(self, org_id: str, user_id: str):
        """Verify a user appears in an org's user list."""
        list_resp, status = self.scalekit_client.users.list_organization_users(
            organization_id=org_id, page_size=50
        )
        self.assertEqual(status.code().name, "OK")
        self.assertIn(user_id, [u.id for u in list_resp.users])

    def _assert_user_not_in_org(self, org_id: str, user_id: str):
        """Verify a user does not appear in an org's user list."""
        list_resp, status = self.scalekit_client.users.list_organization_users(
            organization_id=org_id, page_size=50
        )
        self.assertEqual(status.code().name, "OK")
        self.assertNotIn(user_id, [u.id for u in list_resp.users])

    # -------------------------------------------------------------------------
    # User CRUD
    # -------------------------------------------------------------------------

    def test_create_user_and_membership(self):
        """Onboarding a fully-populated employee with an initial org membership."""
        user = CreateUser(
            email=f"alice.johnson.{self.faker.unique.random_number()}@acme-corp.example.com",
            user_profile=self._make_user_profile(),
            membership=CreateMembership(
                roles=[Role(name="member")],
                inviter_email="hr-system@acme-corp.example.com",
                metadata={"team": "Platform", "department": "Engineering"},
            ),
            metadata={"source": "workday_scim", "sync_version": "2024-01-15"},
        )
        response, status = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user,
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email)
        self._assert_original_profile(u)
        self.assertEqual(u.metadata["source"], "workday_scim")
        self.assertEqual(u.metadata["sync_version"], "2024-01-15")
        self.user_id = u.id

        # Verify membership and role via list_user_roles (reliable dedicated endpoint)
        self._assert_user_in_org(self.org_id, self.user_id)
        self._assert_roles(self.org_id, self.user_id, "member")

    def test_get_user(self):
        """GET by internal ID returns all persisted profile and metadata fields."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        response, status = self.scalekit_client.users.get_user(user_id=self.user_id)

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, user_id=self.user_id)
        self._assert_original_profile(u)
        self._assert_original_metadata(u)

    def test_get_user_by_external_id(self):
        """GET by Workday external ID resolves the correct employee record."""
        user = self._make_create_user(with_external_id=True)
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.external_id = create_resp.user.external_id
        # Verify the server echoed back the external_id we sent
        self.assertEqual(self.external_id, user.external_id)

        response, status = self.scalekit_client.users.get_user_by_external_id(
            external_id=self.external_id
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, external_id=self.external_id)
        self._assert_original_profile(u)
        self._assert_original_metadata(u)

    def test_update_user(self):
        """Updating profile and metadata after a department transfer and name change."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        update_user = UpdateUser(
            user_profile=self._make_updated_profile(),
            metadata={
                "source": "workday_scim",
                "sync_version": "2024-06-01",
                "transfer_reason": "reorg",
            },
        )
        response, status = self.scalekit_client.users.update_user(
            user_id=self.user_id, user=update_user
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, user_id=self.user_id)
        self.assertIsNotNone(u.update_time)
        self._assert_updated_profile(u)
        self.assertEqual(u.metadata["source"], "workday_scim")
        self.assertEqual(u.metadata["sync_version"], "2024-06-01")
        self.assertEqual(u.metadata["transfer_reason"], "reorg")

    def test_update_user_by_external_id(self):
        """Updating a Workday employee via external ID after a reorg."""
        user = self._make_create_user(with_external_id=True)
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.external_id = create_resp.user.external_id

        update_user = UpdateUser(
            user_profile=self._make_updated_profile(),
            metadata={
                "source": "workday_scim",
                "sync_version": "2024-06-01",
                "transfer_reason": "reorg",
            },
        )
        response, status = self.scalekit_client.users.update_user_by_external_id(
            external_id=self.external_id, user=update_user
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, external_id=self.external_id)
        self.assertIsNotNone(u.update_time)
        self._assert_updated_profile(u)
        self.assertEqual(u.metadata["source"], "workday_scim")
        self.assertEqual(u.metadata["sync_version"], "2024-06-01")
        self.assertEqual(u.metadata["transfer_reason"], "reorg")

    def test_list_users(self):
        """list_users returns a valid paginated envelope with well-formed user objects."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        response, status = self.scalekit_client.users.list_users(page_size=10)

        self.assertEqual(status.code().name, "OK")
        self.assertGreater(response.total_size, 0)
        self.assertGreater(len(response.users), 0)
        for u in response.users:
            self.assertIsNotNone(u.id)
            self.assertIsNotNone(u.environment_id)
            self.assertIsNotNone(u.email)

        # The org-scoped list (single user) gives us a reliable presence check
        self._assert_user_in_org(self.org_id, self.user_id)

        if response.next_page_token:
            page2, page2_status = self.scalekit_client.users.list_users(
                page_size=5, page_token=response.next_page_token
            )
            self.assertEqual(page2_status.code().name, "OK")
            self.assertGreater(len(page2.users), 0)

    def test_list_organization_users(self):
        """list_organization_users returns members of that org with valid user objects."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        response, status = self.scalekit_client.users.list_organization_users(
            organization_id=self.org_id, page_size=10
        )

        self.assertEqual(status.code().name, "OK")
        self.assertGreater(response.total_size, 0)
        self.assertGreater(len(response.users), 0)
        self.assertIn(self.user_id, [u.id for u in response.users])
        for u in response.users:
            self.assertIsNotNone(u.id)
            self.assertIsNotNone(u.email)
            self.assertIsNotNone(u.environment_id)

        if response.next_page_token:
            page2, page2_status = self.scalekit_client.users.list_organization_users(
                organization_id=self.org_id, page_size=5,
                page_token=response.next_page_token
            )
            self.assertEqual(page2_status.code().name, "OK")
            self.assertGreater(len(page2.users), 0)

    def test_delete_user(self):
        """Deleting a user by internal ID removes them from the workspace."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        _, status = self.scalekit_client.users.delete_user(user_id=self.user_id)
        self.assertEqual(status.code().name, "OK")
        self.user_id = None

    def test_delete_user_by_external_id(self):
        """Deleting a Workday employee by external ID deprovisions them."""
        user = self._make_create_user(with_external_id=True)
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.external_id = create_resp.user.external_id

        _, status = self.scalekit_client.users.delete_user_by_external_id(
            external_id=self.external_id
        )
        self.assertEqual(status.code().name, "OK")
        self.external_id = None

    # -------------------------------------------------------------------------
    # Membership CRUD
    # -------------------------------------------------------------------------

    def _create_partner_org(self) -> str:
        partner_org = CreateOrganization(
            display_name=f"PartnerCorp {self.faker.unique.random_number()}",
            external_id=f"workday_org_{self.faker.uuid4()}",
        )
        return self.scalekit_client.organization.create_organization(
            organization=partner_org
        )[0].organization.id

    def test_create_membership(self):
        """Adding an existing employee to a partner org (multi-tenant access grant)."""
        partner_org_id = self._create_partner_org()

        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        membership = CreateMembership(
            roles=[Role(name="member")],
            inviter_email="admin@acme-corp.example.com",
            metadata={"team": "Integrations", "access_level": "read-only"},
        )
        response, status = self.scalekit_client.users.create_membership(
            organization_id=partner_org_id,
            user_id=self.user_id,
            membership=membership,
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, user_id=self.user_id)

        # Verify membership and role via dedicated endpoints
        self._assert_user_in_org(partner_org_id, self.user_id)
        self._assert_roles(partner_org_id, self.user_id, "member")

        try:
            self.scalekit_client.organization.delete_organization(organization_id=partner_org_id)
        except ScalekitNotFoundException:
            pass

    def test_create_membership_by_external_id(self):
        """Adding a Workday employee (by external ID) to a partner org."""
        partner_org_id = self._create_partner_org()

        user = self._make_create_user(with_external_id=True)
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.external_id = create_resp.user.external_id
        created_user_id = create_resp.user.id

        membership = CreateMembership(
            roles=[Role(name="member")],
            inviter_email="admin@acme-corp.example.com",
            metadata={"team": "Integrations", "access_level": "read-only"},
        )
        response, status = self.scalekit_client.users.create_membership_by_external_id(
            organization_id=partner_org_id,
            external_id=self.external_id,
            membership=membership,
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, external_id=self.external_id)

        # Verify membership and role via dedicated endpoints
        self._assert_user_in_org(partner_org_id, created_user_id)
        self._assert_roles(partner_org_id, created_user_id, "member")

        try:
            self.scalekit_client.organization.delete_organization(organization_id=partner_org_id)
        except ScalekitNotFoundException:
            pass

    def test_update_membership(self):
        """Promoting a team member to admin after becoming team lead."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        update_membership = UpdateMembership(
            roles=[Role(name="admin")],
            metadata={
                "promoted_by": "bob.smith@acme-corp.example.com",
                "promotion_date": "2024-06-01",
            },
        )
        response, status = self.scalekit_client.users.update_membership(
            organization_id=self.org_id,
            user_id=self.user_id,
            membership=update_membership,
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, user_id=self.user_id)

        # Verify the role promotion took effect
        self._assert_roles(self.org_id, self.user_id, "admin")

    def test_update_membership_by_external_id(self):
        """Promoting a Workday employee (by external ID) to admin after becoming team lead."""
        user = self._make_create_user(with_external_id=True)
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.external_id = create_resp.user.external_id
        created_user_id = create_resp.user.id

        update_membership = UpdateMembership(
            roles=[Role(name="admin")],
            metadata={
                "promoted_by": "bob.smith@acme-corp.example.com",
                "promotion_date": "2024-06-01",
            },
        )
        response, status = self.scalekit_client.users.update_membership_by_external_id(
            organization_id=self.org_id,
            external_id=self.external_id,
            membership=update_membership,
        )

        self.assertEqual(status.code().name, "OK")
        u = response.user
        self._assert_user_core(u, email=user.email, external_id=self.external_id)

        # Verify the role promotion took effect
        self._assert_roles(self.org_id, created_user_id, "admin")

    def test_delete_membership(self):
        """Removing an employee's org access after leaving a team."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.user_id = create_resp.user.id

        _, status = self.scalekit_client.users.delete_membership(
            organization_id=self.org_id, user_id=self.user_id
        )
        self.assertEqual(status.code().name, "OK")

    def test_delete_membership_by_external_id(self):
        """Revoking a Workday employee's (by external ID) access to a partner org."""
        partner_org_id = self._create_partner_org()

        user = self._make_create_user(with_external_id=True)
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id, user=user
        )
        self.external_id = create_resp.user.external_id
        created_user_id = create_resp.user.id

        self.scalekit_client.users.create_membership_by_external_id(
            organization_id=partner_org_id,
            external_id=self.external_id,
            membership=CreateMembership(
                roles=[Role(name="member")],
                inviter_email="admin@acme-corp.example.com",
                metadata={"team": "Integrations"},
            ),
        )
        # Confirm the user is in the partner org before deleting
        self._assert_user_in_org(partner_org_id, created_user_id)

        _, status = self.scalekit_client.users.delete_membership_by_external_id(
            organization_id=partner_org_id, external_id=self.external_id
        )
        self.assertEqual(status.code().name, "OK")

        # Confirm the user is gone from the partner org
        self._assert_user_not_in_org(partner_org_id, created_user_id)

        try:
            self.scalekit_client.organization.delete_organization(organization_id=partner_org_id)
        except ScalekitNotFoundException:
            pass

    # -------------------------------------------------------------------------
    # Invitations
    # -------------------------------------------------------------------------

    def test_resend_invite(self):
        """Resending an invitation returns updated invite status and resent_count."""
        user = self._make_create_user()
        create_resp, _ = self.scalekit_client.users.create_user_and_membership(
            organization_id=self.org_id,
            user=user,
            send_invitation_email=True,
        )
        self.user_id = create_resp.user.id

        response, status = self.scalekit_client.users.resend_invite(
            organization_id=self.org_id, user_id=self.user_id
        )

        self.assertEqual(status.code().name, "OK")
        invite = response.invite
        self.assertIsNotNone(invite)
        self.assertEqual(invite.user_id, self.user_id)
        self.assertEqual(invite.organization_id, self.org_id)
        self.assertEqual(invite.status, "PENDING_INVITE")
        self.assertIsNotNone(invite.created_at)
        self.assertIsNotNone(invite.expires_at)
        self.assertEqual(invite.resent_count, 1)

    # -------------------------------------------------------------------------
    # Teardown
    # -------------------------------------------------------------------------

    def tearDown(self):
        errors = []

        if self.user_id:
            try:
                self.scalekit_client.users.delete_membership(
                    organization_id=self.org_id, user_id=self.user_id
                )
            except ScalekitNotFoundException:
                pass
            except Exception as exp:
                errors.append(exp)

            try:
                self.scalekit_client.users.delete_user(user_id=self.user_id)
            except Exception as exp:
                errors.append(exp)

        if self.external_id:
            try:
                self.scalekit_client.users.delete_membership_by_external_id(
                    organization_id=self.org_id, external_id=self.external_id
                )
            except (ScalekitNotFoundException, ScalekitBadRequestException):
                pass
            except Exception as exp:
                errors.append(exp)

            try:
                self.scalekit_client.users.delete_user_by_external_id(
                    external_id=self.external_id
                )
            except (ScalekitNotFoundException, ScalekitBadRequestException):
                pass
            except Exception as exp:
                errors.append(exp)

        if self.org_id:
            try:
                self.scalekit_client.organization.delete_organization(
                    organization_id=self.org_id
                )
            except Exception as exp:
                errors.append(exp)

        if errors:
            raise Exception(f"Errors during tearDown cleanup: {errors}")

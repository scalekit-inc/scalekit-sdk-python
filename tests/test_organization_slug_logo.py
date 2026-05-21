from faker import Faker

from basetest import BaseTest
from scalekit.common.exceptions import ScalekitBadRequestException
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization, UpdateOrganization


class TestOrganizationSlugLogo(BaseTest):
    """Test cases for organization slug and logo_url fields."""

    def setUp(self):
        self.org_id = None

    def _create_org(self):
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = response[0].organization.id
        return self.org_id

    def test_create_with_logo_url(self):
        """Creating an org with logo_url should persist the value."""
        logo_url = 'https://logo.debounce.com/microsoft.com'
        organization = CreateOrganization(
            display_name=Faker().company(),
            external_id=Faker().uuid4(),
            logo_url=logo_url,
        )
        try:
            response = self.scalekit_client.organization.create_organization(organization=organization)
        except ScalekitBadRequestException as e:
            if 'logo_url' in str(e):
                self.skipTest(f"logo_url not yet supported by server: {e}")
            raise
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        self.org_id = response[0].organization.id
        self.assertEqual(response[0].organization.logo_url, logo_url)

    def test_create_with_slug(self):
        """Creating an org with a slug should persist the value."""
        slug = 'app.acmecorp.com'
        organization = CreateOrganization(
            display_name=Faker().company(),
            external_id=Faker().uuid4(),
            slug=slug,
        )
        response = self.scalekit_client.organization.create_organization(organization=organization)
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        self.org_id = response[0].organization.id
        self.assertEqual(response[0].organization.slug, slug)

    def test_update_logo_url(self):
        """Updating an existing org's logo_url should persist the new value."""
        org_id = self._create_org()

        logo_url = 'https://logo.debounce.com/microsoft.com'
        update_organization = UpdateOrganization(logo_url=logo_url)
        try:
            response = self.scalekit_client.organization.update_organization(
                organization_id=org_id,
                organization=update_organization,
            )
        except ScalekitBadRequestException as e:
            if 'logo_url' in str(e):
                self.skipTest(f"logo_url not yet supported by server: {e}")
            raise
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        self.assertEqual(response[0].organization.id, org_id)
        self.assertEqual(response[0].organization.logo_url, logo_url)

    def test_update_slug_and_metadata(self):
        """Updating an existing org's slug and metadata should persist both values."""
        org_id = self._create_org()

        slug = 'app.acmecorp.com'
        metadata = {'custom_domain': 'app.acmecorp.com'}
        update_organization = UpdateOrganization(slug=slug, metadata=metadata)
        response = self.scalekit_client.organization.update_organization(
            organization_id=org_id,
            organization=update_organization,
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0])
        self.assertEqual(response[0].organization.id, org_id)
        self.assertEqual(response[0].organization.slug, slug)
        self.assertEqual(response[0].organization.metadata, metadata)

    def tearDown(self):
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

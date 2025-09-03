
from faker import Faker

from .basetest import BaseTest
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization
from scalekit.v1.domains.domains_pb2 import DomainType


class TestDomain(BaseTest):
    """ Class definition for Test Domain Class """
    def setUp(self):
        """ """
        self.org_id = None

    def test_create_domain(self):
        """ Method to test create domain """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        domain_name = Faker().domain_name()
        response = self.scalekit_client.domain.create_domain(organization_id=self.org_id, domain_name=domain_name)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].domain.domain, domain_name)
        self.assertEqual(response[0].domain.organization_id, self.org_id)

    def test_create_domain_with_allowed_email_domain_type(self):
        """ Method to test create domain with ALLOWED_EMAIL_DOMAIN type """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        domain_name = Faker().domain_name()
        response = self.scalekit_client.domain.create_domain(
            organization_id=self.org_id, 
            domain_name=domain_name,
            domain_type=DomainType.ALLOWED_EMAIL_DOMAIN
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].domain.domain, domain_name)
        self.assertEqual(response[0].domain.organization_id, self.org_id)
        self.assertEqual(response[0].domain.domain_type, DomainType.ALLOWED_EMAIL_DOMAIN)

    def test_create_domain_with_organization_domain_type(self):
        """ Method to test create domain with ORGANIZATION_DOMAIN type """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        domain_name = Faker().domain_name()
        response = self.scalekit_client.domain.create_domain(
            organization_id=self.org_id, 
            domain_name=domain_name,
            domain_type=DomainType.ORGANIZATION_DOMAIN
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].domain.domain, domain_name)
        self.assertEqual(response[0].domain.organization_id, self.org_id)
        self.assertEqual(response[0].domain.domain_type, DomainType.ORGANIZATION_DOMAIN)

    def test_create_domain_without_domain_type(self):
        """ Method to test create domain without specifying domain_type (backward compatibility) """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        domain_name = Faker().domain_name()
        response = self.scalekit_client.domain.create_domain(
            organization_id=self.org_id, 
            domain_name=domain_name
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].domain.domain, domain_name)
        self.assertEqual(response[0].domain.organization_id, self.org_id)
        # When domain_type is not specified, it should default to ORGANIZATION_DOMAIN
        self.assertEqual(response[0].domain.domain_type, DomainType.ORGANIZATION_DOMAIN)

    def test_get_domain(self):
        """ Method to test get domain """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        domain_name = Faker().domain_name()
        create_domain_response = self.scalekit_client.domain.create_domain(
            organization_id=self.org_id, domain_name=domain_name)
        domain_id = create_domain_response[0].domain.id

        response = self.scalekit_client.domain.get_domain(organization_id=self.org_id, domain_id=domain_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].domain.id, domain_id)
        self.assertEqual(response[0].domain.domain, domain_name)
        self.assertEqual(response[0].domain.organization_id, self.org_id)

    def test_list_domains(self):
        """ Method to test list domains """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        domain_name = Faker().domain_name()
        create_domain_response = self.scalekit_client.domain.create_domain(
            organization_id=self.org_id, domain_name=domain_name)
        self.assertEqual(create_domain_response[1].code().name, "OK")

        response = self.scalekit_client.domain.list_domains(organization_id=self.org_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].domains) > 0)
        self.assertEqual(response[0].domains[0].id, create_domain_response[0].domain.id)
        self.assertEqual(response[0].domains[0].domain, domain_name)
        self.assertEqual(response[0].domains[0].organization_id, self.org_id)

    def test_delete_domain(self):
        """ Method to test delete domain """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        domain_name = Faker().domain_name()
        create_domain_response = self.scalekit_client.domain.create_domain(
            organization_id=self.org_id, domain_name=domain_name)
        domain_id = create_domain_response[0].domain.id

        # Verify domain was created
        self.assertEqual(create_domain_response[1].code().name, "OK")
        self.assertTrue(create_domain_response[0] is not None)

        # Delete the domain
        delete_response = self.scalekit_client.domain.delete_domain(
            organization_id=self.org_id, domain_id=domain_id)
        self.assertEqual(delete_response[1].code().name, "OK")

        # Verify domain was deleted by trying to get it (should fail)
        try:
            self.scalekit_client.domain.get_domain(organization_id=self.org_id, domain_id=domain_id)
            self.fail("Domain should have been deleted")
        except Exception:
            # Expected behavior - domain should not exist
            pass

        # Verify domain is not in the list
        list_response = self.scalekit_client.domain.list_domains(organization_id=self.org_id)
        self.assertEqual(list_response[1].code().name, "OK")
        self.assertTrue(list_response[0] is not None)
        
        # Check that the deleted domain is not in the list
        domain_ids = [domain.id for domain in list_response[0].domains]
        self.assertNotIn(domain_id, domain_ids)

    def tearDown(self):
        """ Method to clean up """
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

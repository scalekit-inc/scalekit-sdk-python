
from faker import Faker

from basetest import BaseTest
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


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

    def tearDown(self):
        """ Method to clean up """
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

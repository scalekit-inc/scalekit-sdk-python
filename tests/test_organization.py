from datetime import datetime

from faker import Faker

from basetest import BaseTest
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization, UpdateOrganization


class TestOrganization(BaseTest):
    """ Class definition for Test Organization Class """

    def setUp(self):
        """ """
        self.org_id = None

    def test_create_organization(self):
        """ Method to test create organization """
        display_name = Faker().company()
        external_id = Faker().uuid4()
        organization = CreateOrganization(display_name=display_name, external_id=external_id)
        response = self.scalekit_client.organization.create_organization(organization=organization)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].organization.display_name, display_name)
        self.assertEqual(response[0].organization.external_id, external_id)
        self.org_id = response[0].organization.id

    def test_get_organization(self):
        """  Method to test get organization """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        response = self.scalekit_client.organization.get_organization(organization_id=self.org_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].organization.id, self.org_id)
        self.assertEqual(response[0].organization.display_name, organization.display_name)

    def test_get_organization_by_external_id(self):
        """  Method to test get organization by external id """
        display_name = Faker().company()
        external_id = Faker().uuid4()
        organization = CreateOrganization(display_name=display_name, external_id=external_id)
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        response = self.scalekit_client.organization.get_organization_by_external_id(external_id=external_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].organization.id, self.org_id)
        self.assertEqual(response[0].organization.display_name, organization.display_name)

    def test_list_organizations(self):
        """ Method to test list organizations """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        response = self.scalekit_client.organization.list_organizations(page_size=10)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].organizations) > 0)
        self.assertEqual(response[0].organizations[0].id, self.org_id)
        self.assertEqual(response[0].organizations[0].display_name, organization.display_name)

    def test_update_organization(self):
        """ Method to test update organization """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        updated_display_name = Faker().company()
        updated_external_id = Faker().uuid4()
        metadata = {'key1': 'Value1', 'key2': 'Value2'}
        update_organization = UpdateOrganization(
            display_name=updated_display_name, external_id=updated_external_id, metadata=metadata)
        response = self.scalekit_client.organization.update_organization(
            organization_id=self.org_id, organization=update_organization
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].organization.id, self.org_id)
        self.assertEqual(response[0].organization.display_name, updated_display_name)
        self.assertEqual(response[0].organization.metadata, metadata)
        self.assertEqual(response[0].organization.external_id, updated_external_id)

    def test_update_organization_by_external_id(self):
        """ Method to test update organization """
        display_name = Faker().company()
        external_id = Faker().uuid4()
        organization = CreateOrganization(display_name=display_name, external_id=external_id)
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        updated_display_name = Faker().company()
        metadata = {'key1': 'Value1', 'key2': 'Value2'}
        update_organization = UpdateOrganization(display_name=updated_display_name, metadata=metadata)
        response = self.scalekit_client.organization.update_organization_by_external_id(
            external_id=external_id, organization=update_organization
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].organization.id, self.org_id)
        self.assertEqual(response[0].organization.display_name, updated_display_name)
        self.assertEqual(response[0].organization.metadata, metadata)
        self.assertEqual(response[0].organization.external_id, external_id)

    def test_delete_organization(self):
        """ Method to test delete organization """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        response = self.scalekit_client.organization.delete_organization(organization_id=self.org_id)
        self.assertEqual(response[1].code().name, "OK")

        try:
            self.scalekit_client.organization.get_organization(organization_id=self.org_id)
        except Exception as exp:
            self.assertEqual(exp.args[0], "organization with id &{" + f"{self.org_id}" + "} was not found")
            self.org_id = None

    def test_generate_portal_link(self):
        """ Method to test generate portal link """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        response = self.scalekit_client.organization.generate_portal_link(organization_id=self.org_id)
        self.assertIsNotNone(response.id)
        self.assertIsNotNone(response.location)
        assert response.expire_time.seconds > datetime.now().timestamp()

    def test_update_organization_settings(self):
        """ Method to test update organization settings """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        settings = [{"name": "sso", "enabled": True}, {"name": "dir_sync", "enabled": False}]
        response = self.scalekit_client.organization.update_organization_settings(
            organization_id=self.org_id, settings=settings
        )
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(response[0].organization.id, self.org_id)
        if response[0].organization.settings.features[0].name == 'sso':
            self.assertTrue(response[0].organization.settings.features[0].enabled)
            self.assertFalse(response[0].organization.settings.features[1].enabled)
        else:
            self.assertTrue(response[0].organization.settings.features[1].enabled)
            self.assertFalse(response[0].organization.settings.features[0].enabled)

    def tearDown(self):
        """ Method to clean up after test """
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

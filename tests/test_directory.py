
from faker import Faker
from basetest import BaseTest

from scalekit.v1.organizations.organizations_pb2 import CreateOrganization
from scalekit.v1.directories.directories_pb2 import CreateDirectory
from scalekit.v1.directories.directories_pb2 import DirectoryProvider, DirectoryType


class TestDirectory(BaseTest):
    """ Class definition for Test Directory Class """

    def setUp(self):
        """ """
        self.org_id = None
        self.dir_id = None

    def test_create_directory(self):
        """ Method to test create directory """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        directory = CreateDirectory(directory_provider=DirectoryProvider.OKTA, directory_type=DirectoryType.SCIM)
        response = self.scalekit_client.directory.create_directory(organization_id=self.org_id, directory=directory)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].directory.directory_provider, DirectoryProvider.OKTA)
        self.assertEqual(response[0].directory.directory_type, DirectoryType.SCIM)
        self.assertEqual(response[0].directory.organization_id, self.org_id)
        self.assertTrue(response[0].directory.enabled)
        self.dir_id = response[0].directory.id

    def test_get_directory(self):
        """ Method to test get directory """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        directory = CreateDirectory(directory_provider=DirectoryProvider.OKTA, directory_type=DirectoryType.SCIM)
        create_response = self.scalekit_client.directory.create_directory(organization_id=self.org_id, directory=directory)
        self.dir_id = create_response[0].directory.id

        response = self.scalekit_client.directory.get_directory(organization_id=self.org_id, directory_id=self.dir_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertEqual(response[0].directory.id, self.dir_id)

    def test_list_directories(self):
        """ Method to test list directories """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        directory = CreateDirectory(directory_provider=DirectoryProvider.OKTA, directory_type=DirectoryType.SCIM)
        create_response = self.scalekit_client.directory.create_directory(organization_id=self.org_id, directory=directory)
        self.dir_id = create_response[0].directory.id

        response = self.scalekit_client.directory.list_directories(organization_id=self.org_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertTrue(len(response[0].directories) > 0)
        self.assertEqual(response[0].directories[0].id, self.dir_id)
        self.assertEqual(response[0].directories[0].directory_provider, DirectoryProvider.OKTA)
        self.assertEqual(response[0].directories[0].directory_type, DirectoryType.SCIM)
        self.assertEqual(response[0].directories[0].organization_id, self.org_id)

    def test_disable_enable_directory(self):
        """ Method to test enable directory """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        directory = CreateDirectory(directory_provider=DirectoryProvider.OKTA, directory_type=DirectoryType.SCIM)
        create_response = self.scalekit_client.directory.create_directory(
            organization_id=self.org_id, directory=directory)
        self.dir_id = create_response[0].directory.id

        disable_response = self.scalekit_client.directory.disable_directory(organization_id=self.org_id, directory_id=self.dir_id)
        self.assertEqual(disable_response[1].code().name, "OK")

        get_disabled_dir = self.scalekit_client.directory.get_directory(organization_id=self.org_id, directory_id=self.dir_id)
        self.assertFalse(get_disabled_dir[0].directory.enabled)

        enable_response = self.scalekit_client.directory.enable_directory(organization_id=self.org_id, directory_id=self.dir_id)
        self.assertEqual(enable_response[1].code().name, "OK")

        get_enabled_dir = self.scalekit_client.directory.get_directory(organization_id=self.org_id, directory_id=self.dir_id)
        self.assertTrue(get_enabled_dir[0].directory.enabled)

    def test_delete_directory(self):
        """ Method to test delete directory """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        directory = CreateDirectory(directory_provider=DirectoryProvider.OKTA, directory_type=DirectoryType.SCIM)
        create_response = self.scalekit_client.directory.create_directory(organization_id=self.org_id, directory=directory)
        self.dir_id = create_response[0].directory.id

        disable_response = self.scalekit_client.directory.disable_directory(organization_id=self.org_id, directory_id=self.dir_id)
        self.assertEqual(disable_response[1].code().name, "OK")

        response = self.scalekit_client.directory.delete_directory(organization_id=self.org_id, directory_id=self.dir_id)
        self.assertEqual(response[1].code().name, "OK")

        try:
            self.scalekit_client.directory.get_directory(organization_id=self.org_id, directory_id=self.dir_id)
        except Exception as e:
            self.assertEqual(e.args[0], "directory not found")
            self.dir_id = None

    def test_get_primary_directory_by_organization_id(self):
        """ Method to test get primary directory by organization id """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        directory = CreateDirectory(directory_provider=DirectoryProvider.OKTA, directory_type=DirectoryType.SCIM)
        create_response = self.scalekit_client.directory.create_directory(organization_id=self.org_id, directory=directory)
        self.dir_id = create_response[0].directory.id

        response = self.scalekit_client.directory.get_primary_directory_by_organization_id(organization_id=self.org_id)
        self.assertEqual(response.id, self.dir_id)
        self.assertEqual(response.organization_id, self.org_id)

    def tearDown(self):
        """ Method to clean up """
        if self.dir_id:
            self.scalekit_client.directory.disable_directory(organization_id=self.org_id, directory_id=self.dir_id)
            self.scalekit_client.directory.delete_directory(organization_id=self.org_id, directory_id=self.dir_id)
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

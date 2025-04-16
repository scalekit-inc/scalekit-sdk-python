
from faker import Faker
from basetest import BaseTest

from scalekit.v1.connections.connections_pb2 import *
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestConnection(BaseTest):
    """ Class definition for Test Connection Class """
    def setUp(self):
        """ """
        self.org_id = None
        self.conn_id = None

    def test_create_connection(self):
        """ Method to test create connection """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        conn_provider = ConnectionProvider.OKTA
        conn_type = ConnectionType.SAML
        connection = CreateConnection(provider=conn_provider, type=conn_type)
        response = self.scalekit_client.connection.create_connection(organization_id=self.org_id, connection=connection)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0] is not None)
        self.assertEqual(response[0].connection.provider, conn_provider)
        self.assertEqual(response[0].connection.type, conn_type)
        self.assertEqual(response[0].connection.organization_id, self.org_id)
        self.conn_id = response[0].connection.id

    def test_get_connection(self):
        """ Method to test get connection """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        conn_provider = ConnectionProvider.OKTA
        conn_type = ConnectionType.SAML
        connection = CreateConnection(provider=conn_provider, type=conn_type)
        conn_response = self.scalekit_client.connection.create_connection(
            organization_id=self.org_id, connection=connection
        )
        self.conn_id = conn_response[0].connection.id

        response = self.scalekit_client.connection.get_connection(organization_id=self.org_id, conn_id=self.conn_id)
        self.assertEqual(response[1].code().name, "OK")
        self.assertTrue(response[0].connection.id, self.conn_id)
        self.assertEqual(response[0].connection.organization_id, self.org_id)
        self.assertEqual(response[0].connection.provider, conn_provider)
        self.assertEqual(response[0].connection.type, conn_type)

    def test_list_connections_by_organization(self):
        """ Method to test list connections by organization """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        conn_provider = ConnectionProvider.OKTA
        conn_type = ConnectionType.SAML
        connection = CreateConnection(provider=conn_provider, type=conn_type)
        conn_response = self.scalekit_client.connection.create_connection(
            organization_id=self.org_id, connection=connection
        )
        self.conn_id = conn_response[0].connection.id

        response = self.scalekit_client.connection.list_connections(organization_id=self.org_id, include='all')
        self.assertEqual(response[1].code().name, "OK")

    def test_list_connections_by_domain(self):
        """ Method to test list connections by domain """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        conn_provider = ConnectionProvider.OKTA
        conn_type = ConnectionType.SAML
        connection = CreateConnection(provider=conn_provider, type=conn_type)
        conn_response = self.scalekit_client.connection.create_connection(
            organization_id=self.org_id, connection=connection
        )
        self.conn_id = conn_response[0].connection.id

        domain_name = Faker().domain_name()
        self.scalekit_client.domain.create_domain(organization_id=self.org_id, domain_name=domain_name)

        response = self.scalekit_client.connection.list_connections_by_domain(domain=domain_name, include='all')
        self.assertEqual(response[1].code().name, "OK")

    def test_delete_connection(self):
        """ Method to test delete connection """
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id

        conn_provider = ConnectionProvider.OKTA
        conn_type = ConnectionType.SAML
        connection = CreateConnection(provider=conn_provider, type=conn_type)
        conn_response = self.scalekit_client.connection.create_connection(organization_id=self.org_id, connection=connection)
        self.conn_id = conn_response[0].connection.id

        response = self.scalekit_client.connection.delete_connection(organization_id=self.org_id, connection_id=self.conn_id)
        self.assertEqual(response[1].code().name, "OK")

        try:
            self.scalekit_client.connection.get_connection(organization_id=self.org_id, conn_id=self.conn_id)
        except Exception as e:
            self.assertEqual(e.args[0], "connection not found")
            self.conn_id = None

    def tearDown(self):
        """ """
        if self.conn_id:
            self.scalekit_client.connection.delete_connection(organization_id=self.org_id, connection_id=self.conn_id)
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

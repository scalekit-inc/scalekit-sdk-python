
from faker import Faker
from basetest import BaseTest
from scalekit.common.exceptions import ScalekitNotFoundException

from scalekit.v1.connections.connections_pb2 import *
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization


class TestConnection(BaseTest):
    """ Class definition for Test Connection Class """
    def setUp(self):
        """ """
        # self.org_id = None
        organization = CreateOrganization(display_name=Faker().company(), external_id=Faker().uuid4())
        org_response = self.scalekit_client.organization.create_organization(organization=organization)
        self.org_id = org_response[0].organization.id
        self.conn_id = None

    def test_create_connection(self):
        """ Method to test create connection """
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
        conn_provider = ConnectionProvider.OKTA
        conn_type = ConnectionType.SAML
        connection = CreateConnection(provider=conn_provider, type=conn_type)
        conn_response = self.scalekit_client.connection.create_connection(organization_id=self.org_id, connection=connection)
        self.conn_id = conn_response[0].connection.id

        response = self.scalekit_client.connection.delete_connection(organization_id=self.org_id, connection_id=self.conn_id)
        self.assertEqual(response[1].code().name, "OK")

        try:
            self.scalekit_client.connection.get_connection(organization_id=self.org_id, conn_id=self.conn_id)
        except ScalekitNotFoundException:
            self.conn_id = None

    def test_create_environment_connection_with_flags(self):
        """ Method to test create environment connection with flags """
        connection = CreateConnection(provider_key="HUBSPOT", type=ConnectionType.OAUTH)
        flags = Flags(is_app=True)
        response = self.scalekit_client.connection.create_environment_connection(connection=connection, flags=flags)
        self.assertEqual(response[1].code().name, "OK")
        conn = response[0].connection
        self.assertIsNotNone(conn)
        self.assertEqual(conn.type, ConnectionType.OAUTH)
        self.assertEqual(conn.provider_key, "HUBSPOT")
        self.assertTrue(conn.key_id.startswith("hubspot-"))
        self.assertTrue(conn.enabled)
        self.assertIsNotNone(conn.oauth_config)
        self.assertIn("hubspot.com", conn.oauth_config.authorize_uri.value)

    def test_list_app_connections(self):
        """ Method to test list_app_connections returns all env connections """
        response = self.scalekit_client.connection.list_app_connections()
        self.assertEqual(response[1].code().name, "OK")
        self.assertIsNotNone(response[0].connections)
        self.assertIsInstance(response[0].total_size, int)

    def test_list_app_connections_with_provider_filter(self):
        """ Method to test list_app_connections filtered by provider """
        # First create a HubSpot connection so we know at least one exists
        self.scalekit_client.connection.create_environment_connection(
            connection=CreateConnection(provider_key="HUBSPOT", type=ConnectionType.OAUTH),
            flags=Flags(is_app=True)
        )
        response = self.scalekit_client.connection.list_app_connections(provider="HUBSPOT")
        self.assertEqual(response[1].code().name, "OK")
        connections = response[0].connections
        self.assertGreater(len(connections), 0)
        for conn in connections:
            self.assertEqual(conn.provider_key, "HUBSPOT")

    def test_list_app_connections_with_page_size(self):
        """ Method to test list_app_connections respects page_size """
        response = self.scalekit_client.connection.list_app_connections(page_size=2)
        self.assertEqual(response[1].code().name, "OK")
        self.assertLessEqual(len(response[0].connections), 2)

    def test_get_custom_connection(self):
        """ Method to test get_environment_connection - create then get """
        create_response = self.scalekit_client.connection.create_environment_connection(
            connection=CreateConnection(provider_key="HUBSPOT", type=ConnectionType.OAUTH),
            flags=Flags(is_app=True)
        )
        conn_id = create_response[0].connection.id

        response = self.scalekit_client.connection.get_environment_connection(connection_id=conn_id)
        self.assertEqual(response[1].code().name, "OK")
        conn = response[0].connection
        self.assertEqual(conn.id, conn_id)
        self.assertEqual(conn.provider_key, "HUBSPOT")
        self.assertEqual(conn.type, ConnectionType.OAUTH)

    def test_update_environment_connection(self):
        """ Method to test update environment connection - update client_id and client_secret """
        # Create a HubSpot OAuth environment connection
        create_response = self.scalekit_client.connection.create_environment_connection(
            connection=CreateConnection(provider_key="HUBSPOT", type=ConnectionType.OAUTH),
            flags=Flags(is_app=True)
        )
        conn_id = create_response[0].connection.id
        key_id = create_response[0].connection.key_id
        existing_oauth = create_response[0].connection.oauth_config

        update = UpdateConnection(
            provider_key="HUBSPOT",
            key_id=key_id,
            type=ConnectionType.OAUTH,
            oauth_config=OAuthConnectionConfig(
                client_id={"value": "test-client-id"},
                client_secret={"value": "test-client-secret"}
            )
        )
        response = self.scalekit_client.connection.update_environment_connection(
            connection_id=conn_id, connection=update
        )
        self.assertEqual(response[1].code().name, "OK")
        conn = response[0].connection
        self.assertIsNotNone(conn.oauth_config)
        # Verify updated fields
        self.assertEqual(conn.oauth_config.client_id.value, "test-client-id")
        # Verify untouched fields are preserved (PATCH, not PUT)
        self.assertEqual(conn.oauth_config.authorize_uri.value, existing_oauth.authorize_uri.value)
        self.assertEqual(conn.oauth_config.token_uri.value, existing_oauth.token_uri.value)
        self.assertEqual(conn.oauth_config.user_info_uri.value, existing_oauth.user_info_uri.value)

    def test_google_dwd_create_update_get(self):
        """ Test create, update, and get for a GOOGLE_DWD environment connection """
        key_id = f"test-gdwd-{Faker().lexify('??????')}"
        # Step 1: Create
        create_response = self.scalekit_client.connection.create_environment_connection(
            connection=CreateConnection(
                provider_key="GOOGLEDWD",
                type=ConnectionType.GOOGLE_DWD,
                key_id=key_id
            ),
            flags=Flags(is_app=True)
        )
        self.assertEqual(create_response[1].code().name, "OK")
        conn = create_response[0].connection
        conn_id = conn.id
        self.assertEqual(conn.type, ConnectionType.GOOGLE_DWD)
        self.assertEqual(conn.provider_key, "GOOGLEDWD")
        self.assertEqual(conn.key_id, key_id)

        # Step 2: Update - set service_account_json, scopes, token_uri
        fake_sa_json = '{"type":"service_account","project_id":"my-project","client_email":"sa@my-project.iam.gserviceaccount.com","private_key":"-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEA0Z3VS5JJcds3xHn/ygWep4PAtLSDbTHCXHCTvxlHnl0UIFft\\n-----END RSA PRIVATE KEY-----\\n"}'
        update = UpdateConnection(
            provider_key="GOOGLEDWD",
            key_id=key_id,
            type=ConnectionType.GOOGLE_DWD,
            google_dwd_config=GoogleDWDConfig(
                service_account_json={"value": fake_sa_json},
                scopes=["https://www.googleapis.com/auth/admin.directory.user.readonly"],
                token_uri={"value": "https://oauth2.googleapis.com/token"}
            )
        )
        update_response = self.scalekit_client.connection.update_environment_connection(
            connection_id=conn_id, connection=update
        )
        self.assertEqual(update_response[1].code().name, "OK")
        updated_conn = update_response[0].connection
        self.assertIn("https://www.googleapis.com/auth/admin.directory.user.readonly", updated_conn.google_dwd_config.scopes)
        self.assertEqual(updated_conn.google_dwd_config.token_uri.value, "https://oauth2.googleapis.com/token")

        # Step 3: Get and verify
        get_response = self.scalekit_client.connection.get_environment_connection(connection_id=conn_id)
        self.assertEqual(get_response[1].code().name, "OK")
        fetched = get_response[0].connection
        self.assertEqual(fetched.id, conn_id)
        self.assertEqual(fetched.type, ConnectionType.GOOGLE_DWD)
        self.assertEqual(fetched.key_id, key_id)
        self.assertIn("https://www.googleapis.com/auth/admin.directory.user.readonly", fetched.google_dwd_config.scopes)

    def tearDown(self):
        """ """
        if self.conn_id:
            self.scalekit_client.connection.delete_connection(organization_id=self.org_id, connection_id=self.conn_id)
        if self.org_id:
            self.scalekit_client.organization.delete_organization(organization_id=self.org_id)

import uuid

from faker import Faker
from basetest import BaseTest

from scalekit.common.exceptions import ScalekitNotFoundException
from scalekit.actions.types import (
    AuthPattern,
    AuthField,
    OAuthConfig,
    CreateCustomProviderRequest,
    UpdateCustomProviderRequest,
    ListProvidersRequest,
    DeleteCustomProviderRequest,
)
from scalekit.v1.providers.providers_pb2 import ProviderType
from scalekit.v1.connections.connections_pb2 import (
    CreateConnection,
    Flags,
    ConnectionType,
    DeleteEnvironmentConnectionRequest,
)


class TestProviders(BaseTest):
    """Integration tests for ActionProviders — MCP connectors only."""

    def setUp(self):
        self.faker = Faker()
        self.created_identifier = None

    def tearDown(self):
        if self.created_identifier:
            try:
                self.scalekit_client.actions.providers.delete_custom_provider(
                    DeleteCustomProviderRequest(identifier=self.created_identifier)
                )
            except ScalekitNotFoundException:
                pass
            self.created_identifier = None

    # ------------------------------------------------------------------
    # OAuth MCP — create + list (OAuthConfig with pkce_enabled=True by default)
    # ------------------------------------------------------------------

    def test_oauth_mcp_create_and_list(self):
        """Create an OAuth MCP provider and verify all fields including pkce_enabled."""
        suffix = self.faker.unique.random_number(digits=6)

        create_resp = self.scalekit_client.actions.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name=f"Test OAuth MCP Provider {suffix}",
                description="Integration test OAuth MCP connector",
                proxy_url="https://server.example.com/mcp",
                proxy_enabled=True,
                auth_patterns=[
                    AuthPattern(
                        type="OAUTH",
                        display_name="OAuth 2.1/DCR",
                        description="Authenticate with browser OAuth. MCP server handles DCR.",
                        is_mcp=True,
                        oauth_config=OAuthConfig(),  # pkce_enabled=True by default
                    )
                ],
            )
        )
        provider = create_resp.provider
        self.assertIsNotNone(provider)
        self.created_identifier = provider.identifier

        # top-level provider fields
        self.assertEqual(provider.display_name, f"Test OAuth MCP Provider {suffix}")
        self.assertEqual(provider.description, "Integration test OAuth MCP connector")
        self.assertEqual(provider.proxy_url, "https://server.example.com/mcp")
        self.assertTrue(provider.proxy_enabled)
        self.assertTrue(provider.is_custom)
        self.assertTrue(provider.is_custom_mcp)

        # auth_patterns — fully typed, no MessageToDict
        self.assertEqual(len(provider.auth_patterns), 1)
        p = provider.auth_patterns[0]
        self.assertEqual(p.type, "OAUTH")
        self.assertEqual(p.display_name, "OAuth 2.1/DCR")
        self.assertEqual(p.description, "Authenticate with browser OAuth. MCP server handles DCR.")
        self.assertEqual(p.fields, [])
        self.assertTrue(p.is_mcp)
        self.assertIsNotNone(p.oauth_config)
        self.assertTrue(p.oauth_config.pkce_enabled)

        # verify it appears in list
        list_resp = self.scalekit_client.actions.providers.list_providers(
            ListProvidersRequest(provider_type=ProviderType.CUSTOM, page_size=100)
        )
        listed = next(
            (lp for lp in list_resp.providers if lp.identifier == self.created_identifier),
            None,
        )
        self.assertIsNotNone(listed, "Created MCP provider not found in list")
        self.assertEqual(listed.display_name, f"Test OAuth MCP Provider {suffix}")
        self.assertTrue(listed.is_custom_mcp)
        lp = listed.auth_patterns[0]
        self.assertEqual(lp.type, "OAUTH")
        self.assertTrue(lp.is_mcp)
        self.assertIsNotNone(lp.oauth_config)
        self.assertTrue(lp.oauth_config.pkce_enabled)

    # ------------------------------------------------------------------
    # Bearer MCP — create + update + list
    # ------------------------------------------------------------------

    def test_bearer_mcp_create_update_and_list(self):
        """Create Bearer MCP provider, update description and field hint, verify is_mcp preserved."""
        suffix = self.faker.unique.random_number(digits=6)

        create_resp = self.scalekit_client.actions.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name=f"Test Bearer MCP Provider {suffix}",
                description="Integration test Bearer MCP connector",
                proxy_url="https://server.example.com/mcp",
                proxy_enabled=True,
                auth_patterns=[
                    AuthPattern(
                        type="BEARER",
                        display_name="Apify Token",
                        description="Authenticate with Apify using your API Token.",
                        is_mcp=True,
                        fields=[
                            AuthField(
                                field_name="token",
                                label="Apify Token",
                                input_type="password",
                                hint="Your Apify API Token",
                                required=True,
                            )
                        ],
                    )
                ],
            )
        )
        provider = create_resp.provider
        self.assertIsNotNone(provider)
        self.created_identifier = provider.identifier

        # assert create response
        self.assertEqual(provider.description, "Integration test Bearer MCP connector")
        self.assertEqual(provider.proxy_url, "https://server.example.com/mcp")
        self.assertTrue(provider.is_custom_mcp)
        p = provider.auth_patterns[0]
        self.assertEqual(p.type, "BEARER")
        self.assertEqual(p.display_name, "Apify Token")
        self.assertTrue(p.is_mcp)
        self.assertIsNone(p.oauth_config)
        self.assertEqual(len(p.fields), 1)
        self.assertEqual(p.fields[0].field_name, "token")
        self.assertEqual(p.fields[0].hint, "Your Apify API Token")
        self.assertTrue(p.fields[0].required)

        # update description and field hint
        update_resp = self.scalekit_client.actions.providers.update_custom_provider(
            UpdateCustomProviderRequest(
                identifier=self.created_identifier,
                display_name=f"Test Bearer MCP Provider {suffix}",
                proxy_url="https://server.example.com/mcp",
                description="Updated Bearer MCP connector description",
                auth_patterns=[
                    AuthPattern(
                        type="BEARER",
                        display_name="Apify Token",
                        description="Authenticate with Apify using your API Token.",
                        is_mcp=True,
                        fields=[
                            AuthField(
                                field_name="token",
                                label="Apify Token",
                                input_type="password",
                                hint="Your Apify API Token (updated)",
                                required=True,
                            )
                        ],
                    )
                ],
            )
        )
        updated = update_resp.provider
        self.assertIsNotNone(updated)
        self.assertEqual(updated.description, "Updated Bearer MCP connector description")
        self.assertTrue(updated.is_custom_mcp)
        up = updated.auth_patterns[0]
        self.assertTrue(up.is_mcp)
        self.assertEqual(up.fields[0].hint, "Your Apify API Token (updated)")

        # verify update visible in list
        list_resp = self.scalekit_client.actions.providers.list_providers(
            ListProvidersRequest(provider_type=ProviderType.CUSTOM, page_size=100)
        )
        listed = next(
            (lp for lp in list_resp.providers if lp.identifier == self.created_identifier),
            None,
        )
        self.assertIsNotNone(listed, "Updated MCP provider not found in list")
        self.assertEqual(listed.description, "Updated Bearer MCP connector description")
        self.assertTrue(listed.is_custom_mcp)
        lp = listed.auth_patterns[0]
        self.assertEqual(lp.type, "BEARER")
        self.assertTrue(lp.is_mcp)
        self.assertEqual(lp.fields[0].hint, "Your Apify API Token (updated)")

    # ------------------------------------------------------------------
    # API Key MCP — create + delete
    # ------------------------------------------------------------------

    def test_api_key_mcp_create_and_delete(self):
        """Create an API Key MCP provider, delete it, confirm it no longer appears in list."""
        suffix = self.faker.unique.random_number(digits=6)

        create_resp = self.scalekit_client.actions.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name=f"Test API Key MCP Provider {suffix}",
                description="Integration test API Key MCP connector",
                proxy_url="https://server.example.com/mcp",
                proxy_enabled=True,
                auth_patterns=[
                    AuthPattern(
                        type="API_KEY",
                        display_name="API Key",
                        description="Authenticate with a static API key",
                        is_mcp=True,
                        fields=[
                            AuthField(
                                field_name="api_key",
                                label="API Key",
                                input_type="password",
                                hint="Your API key",
                                required=True,
                            )
                        ],
                    )
                ],
            )
        )
        provider = create_resp.provider
        self.assertIsNotNone(provider)
        identifier = provider.identifier

        # assert create response
        self.assertEqual(provider.description, "Integration test API Key MCP connector")
        self.assertEqual(provider.proxy_url, "https://server.example.com/mcp")
        self.assertTrue(provider.is_custom_mcp)
        p = provider.auth_patterns[0]
        self.assertEqual(p.type, "API_KEY")
        self.assertEqual(p.display_name, "API Key")
        self.assertTrue(p.is_mcp)
        self.assertIsNone(p.oauth_config)
        self.assertEqual(p.fields[0].field_name, "api_key")
        self.assertTrue(p.fields[0].required)

        # delete
        self.scalekit_client.actions.providers.delete_custom_provider(
            DeleteCustomProviderRequest(identifier=identifier)
        )
        self.created_identifier = None  # already deleted — skip tearDown

        # confirm gone from list
        list_resp = self.scalekit_client.actions.providers.list_providers(
            ListProvidersRequest(provider_type=ProviderType.CUSTOM, page_size=100)
        )
        identifiers = [lp.identifier for lp in list_resp.providers]
        self.assertNotIn(identifier, identifiers)

    # ------------------------------------------------------------------
    # API Key MCP with auth_header_key_override — create + assert round-trip
    # ------------------------------------------------------------------

    def test_api_key_mcp_with_auth_header_key_override(self):
        """Create an API Key MCP provider that overrides the credential header
        name, and verify auth_header_key_override round-trips in the response."""
        suffix = self.faker.unique.random_number(digits=6)

        create_resp = self.scalekit_client.actions.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name=f"Test Header Override Provider {suffix}",
                description="Integration test API Key connector with header override",
                proxy_url="https://server.example.com/mcp",
                proxy_enabled=True,
                auth_patterns=[
                    AuthPattern(
                        type="API_KEY",
                        display_name="API Key",
                        description="Authenticate with a static API key",
                        is_mcp=True,
                        fields=[
                            AuthField(
                                field_name="api_key",
                                label="API Key",
                                input_type="password",
                                required=True,
                            )
                        ],
                        auth_header_key_override="x-api-key",
                    )
                ],
            )
        )
        provider = create_resp.provider
        self.assertIsNotNone(provider)
        self.created_identifier = provider.identifier

        self.assertTrue(provider.is_custom_mcp)
        self.assertEqual(len(provider.auth_patterns), 1)
        p = provider.auth_patterns[0]
        self.assertEqual(p.type, "API_KEY")
        # the override survives the round-trip through the server
        self.assertEqual(p.auth_header_key_override, "x-api-key")
        self.assertEqual(p.fields[0].field_name, "api_key")
        self.assertTrue(p.fields[0].required)

    # ------------------------------------------------------------------
    # metadata + icon_src — create, update, and list round-trip through
    # the actions.providers facade (CreateCustomProviderRequest /
    # UpdateCustomProviderRequest now expose these fields)
    # ------------------------------------------------------------------

    def test_metadata_and_icon_src_create_update_and_list(self):
        """Create a provider with metadata and icon_src via the facade, verify
        both round-trip in the create response, update them, and confirm the
        new values surface in the create/update responses and in list_providers."""
        suffix = self.faker.unique.random_number(digits=6)
        icon_src = "https://acme.example.com/icon.png"
        metadata = {"team": "integrations", "tier": "premium"}

        create_resp = self.scalekit_client.actions.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name=f"Test Metadata Provider {suffix}",
                description="Integration test metadata/icon_src connector",
                proxy_url="https://server.example.com/mcp",
                proxy_enabled=True,
                icon_src=icon_src,
                metadata=metadata,
                auth_patterns=[
                    AuthPattern(
                        type="NO_AUTH",
                        display_name="Public",
                        description="Connector requires no credentials",
                        is_mcp=True,
                    )
                ],
            )
        )
        provider = create_resp.provider
        self.assertIsNotNone(provider)
        self.created_identifier = provider.identifier

        # metadata + icon_src round-trip on create
        self.assertEqual(provider.icon_src, icon_src)
        self.assertEqual(dict(provider.metadata), metadata)

        # update metadata + icon_src to new values
        new_icon_src = "https://acme.example.com/icon-v2.png"
        new_metadata = {"team": "platform", "region": "us"}
        update_resp = self.scalekit_client.actions.providers.update_custom_provider(
            UpdateCustomProviderRequest(
                identifier=self.created_identifier,
                display_name=f"Test Metadata Provider {suffix}",
                proxy_url="https://server.example.com/mcp",
                icon_src=new_icon_src,
                metadata=new_metadata,
            )
        )
        updated = update_resp.provider
        self.assertIsNotNone(updated)
        self.assertEqual(updated.icon_src, new_icon_src)
        self.assertEqual(dict(updated.metadata), new_metadata)

        # verify the updated metadata + icon_src surface in list_providers
        list_resp = self.scalekit_client.actions.providers.list_providers(
            ListProvidersRequest(provider_type=ProviderType.CUSTOM, page_size=100)
        )
        listed = next(
            (lp for lp in list_resp.providers if lp.identifier == self.created_identifier),
            None,
        )
        self.assertIsNotNone(listed, "Provider with metadata not found in list")
        self.assertEqual(listed.icon_src, new_icon_src)
        self.assertEqual(dict(listed.metadata), new_metadata)


class TestNoAuthCustomProviderFlow(BaseTest):
    """End-to-end NO_AUTH flow: custom provider -> connection -> connected account.

    Exercises the credential-free connector path (e.g. public docs MCP servers):
    a NO_AUTH custom provider, an app connection created from it, and a
    connected account created with empty static_auth. tearDown deletes all
    three in reverse order so the test is self-cleaning even on assertion
    failure.
    """

    def setUp(self):
        self.faker = Faker()
        self.provider_identifier = None
        self.connection_id = None
        self.connection_name = None
        self.account_identifier = None

    def tearDown(self):
        # Reverse order: connected account -> connection -> custom provider.
        # Each guarded independently so one missing resource never masks the
        # cleanup of the others.
        if self.connection_name and self.account_identifier:
            try:
                self.scalekit_client.actions.delete_connected_account(
                    connection_name=self.connection_name,
                    identifier=self.account_identifier,
                )
            except ScalekitNotFoundException:
                pass

        if self.connection_id:
            # No high-level wrapper exists for deleting an environment/app
            # connection, so call the gRPC stub directly. delete_connection()
            # is organization-scoped and would be wrong here.
            try:
                self.scalekit_client.connection.core_client.grpc_exec(
                    self.scalekit_client.connection.connection_service.DeleteEnvironmentConnection.with_call,
                    DeleteEnvironmentConnectionRequest(connection_id=self.connection_id),
                )
            except ScalekitNotFoundException:
                pass

        if self.provider_identifier:
            try:
                self.scalekit_client.actions.providers.delete_custom_provider(
                    DeleteCustomProviderRequest(identifier=self.provider_identifier)
                )
            except ScalekitNotFoundException:
                pass

        super().tearDown()

    def test_no_auth_custom_provider_end_to_end(self):
        """Create a NO_AUTH custom provider, an app connection, and a
        connected account with empty static_auth; assert each step."""
        suffix = self.faker.unique.random_number(digits=6)

        # 1. NO_AUTH custom provider — no credential fields, no oauth_config.
        create_resp = self.scalekit_client.actions.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name=f"Test No Auth Provider {suffix}",
                description="Integration test NO_AUTH connector",
                proxy_url="https://server.example.com/mcp",
                proxy_enabled=True,
                auth_patterns=[
                    AuthPattern(
                        type="NO_AUTH",
                        display_name="Public",
                        description="Connector requires no credentials",
                        is_mcp=True,
                    )
                ],
            )
        )
        provider = create_resp.provider
        self.assertIsNotNone(provider)
        self.provider_identifier = provider.identifier
        self.assertTrue(provider.is_custom)
        self.assertTrue(provider.is_custom_mcp)  # is_mcp=True on the pattern
        self.assertEqual(len(provider.auth_patterns), 1)
        pattern = provider.auth_patterns[0]
        self.assertEqual(pattern.type, "NO_AUTH")
        self.assertEqual(pattern.fields, [])
        self.assertIsNone(pattern.oauth_config)

        # 2. App connection created from the custom provider (provider_key =
        #    provider identifier). key_id is auto-generated into the connector
        #    slug used by connected-account calls.
        conn_resp = self.scalekit_client.connection.create_environment_connection(
            connection=CreateConnection(
                provider_key=self.provider_identifier,
                type=ConnectionType.NO_AUTH,
            ),
            flags=Flags(is_app=True, is_login=False),
        )
        self.assertEqual(conn_resp[1].code().name, "OK")
        connection = conn_resp[0].connection
        self.connection_id = connection.id
        self.connection_name = connection.key_id
        self.assertTrue(self.connection_name, "connection key_id (connector slug) should be set")
        self.assertEqual(connection.type, ConnectionType.NO_AUTH)
        self.assertEqual(connection.provider_key, self.provider_identifier)

        # 3. Connected account with empty static_auth (the NO_AUTH form).
        self.account_identifier = f"noauth-user-{suffix}@example.com"
        acc_resp = self.scalekit_client.actions.create_connected_account(
            connection_name=self.connection_name,
            identifier=self.account_identifier,
            authorization_details={"static_auth": {}},
        )
        self.assertIsNotNone(acc_resp)
        account = acc_resp.connected_account
        self.assertIsNotNone(account)
        self.assertEqual(account.identifier, self.account_identifier)
        # NO_AUTH connectors have no credential step, so the account is active
        # immediately on creation.
        self.assertEqual(account.status, "ACTIVE")
        self.assertEqual(account.authorization_type, "NO_AUTH")
        self.assertEqual(account.connector, self.connection_name)

    def test_no_auth_via_low_level_providers_client(self):
        """Same NO_AUTH flow but driven through the low-level clients directly.

        Some callers bypass the typed ActionProviders wrapper and use
        actions._providers_client.create_custom_provider(...) with keyword
        arguments (which also lets them set metadata, unavailable on the typed
        wrapper). This returns a (proto, call) tuple, so provider is read as
        create_result[0].provider — a proto message, not a typed model.
        """
        suffix = self.faker.unique.random_number(digits=6)
        tenant_id = str(uuid.uuid4())

        # 1. NO_AUTH custom provider via the low-level client (kwargs + metadata).
        create_result = self.scalekit_client.actions._providers_client.create_custom_provider(
            display_name=f"Test No Auth Direct {suffix}",
            description="Integration test NO_AUTH via low-level client",
            proxy_url="https://server.example.com/mcp",
            proxy_enabled=True,
            auth_patterns=[
                AuthPattern(
                    type="NO_AUTH",
                    display_name="Public",
                    description="Connector requires no credentials",
                    is_mcp=True,
                )
            ],
            metadata={"tenant_id": tenant_id},
        )
        self.assertEqual(create_result[1].code().name, "OK")
        provider = create_result[0].provider  # proto Provider, not the typed model
        self.provider_identifier = provider.identifier
        self.assertTrue(provider.is_custom)
        self.assertTrue(provider.is_custom_mcp)  # is_mcp=True on the pattern
        # metadata is supported by the low-level client and should round-trip.
        self.assertEqual(dict(provider.metadata), {"tenant_id": tenant_id})

        # 2. App connection created from the provider.
        conn_resp = self.scalekit_client.connection.create_environment_connection(
            connection=CreateConnection(
                provider_key=self.provider_identifier,
                type=ConnectionType.NO_AUTH,
            ),
            flags=Flags(is_app=True, is_login=False),
        )
        self.assertEqual(conn_resp[1].code().name, "OK")
        connection = conn_resp[0].connection
        self.connection_id = connection.id
        self.connection_name = connection.key_id
        self.assertTrue(self.connection_name, "connection key_id (connector slug) should be set")
        self.assertEqual(connection.type, ConnectionType.NO_AUTH)
        self.assertEqual(connection.provider_key, self.provider_identifier)

        # 3. Connected account with empty static_auth (the NO_AUTH form).
        self.account_identifier = f"noauth-direct-{suffix}@example.com"
        ca_response = self.scalekit_client.actions.create_connected_account(
            connection_name=self.connection_name,
            identifier=self.account_identifier,
            authorization_details={"static_auth": {}},
        )
        self.assertIsNotNone(ca_response)
        account = ca_response.connected_account
        self.assertIsNotNone(account)
        self.assertEqual(account.identifier, self.account_identifier)
        self.assertEqual(account.status, "ACTIVE")
        self.assertEqual(account.authorization_type, "NO_AUTH")
        self.assertEqual(account.connector, self.connection_name)

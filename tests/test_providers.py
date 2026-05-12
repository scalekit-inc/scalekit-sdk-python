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

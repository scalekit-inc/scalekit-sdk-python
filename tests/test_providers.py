import unittest
import uuid

from faker import Faker
from basetest import BaseTest
from google.protobuf.json_format import MessageToDict

from scalekit.common.exceptions import ScalekitNotFoundException
from scalekit.providers import _patterns_to_list_value
from scalekit.actions.types import (
    AuthPattern,
    AuthField,
    AuthFieldOption,
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
                        fields=[],
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
                # auth_patterns is required by the server on every update.
                auth_patterns=[
                    AuthPattern(
                        type="NO_AUTH",
                        display_name="Public",
                        description="Connector requires no credentials",
                        is_mcp=True,
                        fields=[],
                    )
                ],
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
                        fields=[],
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
                    fields=[],
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


class TestAuthPatternDefaults(unittest.TestCase):
    """Pure unit tests (no network) guarding AuthPattern field defaults.

    NO_AUTH connectors collect no credentials, so an AuthPattern of that type
    must carry an empty fields list. This guards the contract at the model level
    so it holds regardless of whether a call site passes fields=[] explicitly.
    """

    def test_no_auth_pattern_defaults_to_empty_fields(self):
        pattern = AuthPattern(type="NO_AUTH", display_name="Public")
        self.assertEqual(pattern.fields, [])

    def test_auth_pattern_fields_default_is_not_shared(self):
        """Each AuthPattern gets its own fields list (no shared mutable default)."""
        first = AuthPattern(type="NO_AUTH", display_name="A")
        second = AuthPattern(type="NO_AUTH", display_name="B")
        self.assertIsNot(first.fields, second.fields)


class TestAuthFieldInputType(unittest.TestCase):
    """Pure unit tests (no network) for AuthField.input_type.

    Regression guard: input_type used to be typed Literal['text', 'password'],
    so decoding a provider whose catalogue serves any other input_type (the
    catalogue also serves 'select' and 'textarea') raised a pydantic
    ValidationError and broke list_providers() for the whole page. The value
    vocabulary is server-owned, so the SDK must accept any string.
    """

    def test_from_dict_accepts_select_and_textarea(self):
        """The response-decoding path must not reject catalogue-served types."""
        for input_type in ("select", "textarea"):
            field = AuthField.from_dict(
                {"field_name": "region", "label": "Region", "input_type": input_type}
            )
            self.assertEqual(field.input_type, input_type)

    def test_from_dict_accepts_unknown_input_type(self):
        """An input_type the SDK has never seen is passed through, not rejected."""
        field = AuthField.from_dict(
            {"field_name": "f", "input_type": "some_future_widget"}
        )
        self.assertEqual(field.input_type, "some_future_widget")

    def test_direct_construction_accepts_select(self):
        self.assertEqual(AuthField(field_name="region", input_type="select").input_type, "select")

    def test_defaults_to_text_when_absent(self):
        """Missing input_type still defaults to 'text' (unchanged behaviour)."""
        self.assertEqual(AuthField.from_dict({"field_name": "f"}).input_type, "text")

    def test_round_trip_preserves_input_type(self):
        """to_dict/from_dict round-trips a select field without loss."""
        original = AuthField(field_name="region", label="Region", input_type="select", required=True)
        restored = AuthField.from_dict(original.to_dict())
        self.assertEqual(restored.input_type, "select")
        self.assertEqual(restored.field_name, "region")
        self.assertTrue(restored.required)

    def test_pattern_with_select_field_decodes(self):
        """AuthPattern.from_dict (the list_providers decode path) accepts a select field."""
        pattern = AuthPattern.from_dict(
            {
                "type": "API_KEY",
                "display_name": "API Key",
                "fields": [
                    {"field_name": "region", "label": "Region", "input_type": "select"},
                    {"field_name": "api_key", "label": "API Key", "input_type": "password"},
                ],
            }
        )
        self.assertEqual([f.input_type for f in pattern.fields], ["select", "password"])



# A provider auth pattern in the shape the API serves one: an OAUTH pattern
# carrying a select field with its options. Values are placeholders — these
# tests pin the SDK's handling of the structure, not any particular connector.
SERVED_OAUTH_PATTERN = {
    "type": "OAUTH",
    "display_name": "OAuth 2.0",
    "description": "",
    "oauth_config": {"pkce_enabled": True},
    "fields": [
        {
            "field_name": "example_choice",
            "label": "Example Choice",
            "hint": "Pick one of the two example values",
            "input_type": "select",
            "required": False,
            "options": [
                {
                    "value": "first",
                    "display_name": "First",
                    "description": "The first example value",
                    "default": True,
                },
                {
                    "value": "second",
                    "display_name": "Second",
                    "description": "The second example value",
                    "default": False,
                },
            ],
        }
    ],
}


class TestServedPatternDecoding(unittest.TestCase):
    """Pure unit tests (no network) for decoding auth patterns off the wire.

    Regression guard for SK-2030. The SDK used to hardcode three constraints
    over auth_patterns, which the server sends as an untyped protobuf ListValue:
    input_type was Literal['text', 'password'], type was
    Literal['OAUTH', 'BEARER', 'API_KEY', 'NO_AUTH'], and fields had to be empty
    on an OAUTH pattern. Real providers satisfy none of the three, so
    list_providers() raised a ValidationError and lost the whole page. The
    server owns these vocabularies and validates almost nothing, so the SDK must
    accept what it is given and pass unknown shapes through.
    """

    def test_oauth_pattern_with_fields_decodes(self):
        """OAUTH patterns do carry fields; the SDK must not reject them."""
        pattern = AuthPattern.from_dict(SERVED_OAUTH_PATTERN)
        self.assertEqual(pattern.type, "OAUTH")
        self.assertEqual([f.field_name for f in pattern.fields], ["example_choice"])

    def test_select_field_options_are_decoded(self):
        """A select field is useless without its choices, so options must survive."""
        field = AuthPattern.from_dict(SERVED_OAUTH_PATTERN).fields[0]
        self.assertEqual([o.value for o in field.options], ["first", "second"])
        self.assertEqual(field.options[0].display_name, "First")
        self.assertEqual(field.options[0].description, "The first example value")
        self.assertTrue(field.options[0].default)
        self.assertFalse(field.options[1].default)

    def test_unknown_pattern_types_decode(self):
        """type is server-owned; an unrecognised one must pass through, not raise."""
        for auth_type in ("OAUTH", "BEARER", "API_KEY", "NO_AUTH", "SOME_FUTURE_TYPE"):
            with self.subTest(type=auth_type):
                pattern = AuthPattern.from_dict(
                    {"type": auth_type, "display_name": "Example", "fields": []}
                )
                self.assertEqual(pattern.type, auth_type)

    def test_oauth_config_on_non_oauth_type_decodes(self):
        """oauth_config is not exclusive to type='OAUTH' on the decode path."""
        pattern = AuthPattern.from_dict(
            {
                "type": "SOME_FUTURE_TYPE",
                "display_name": "Example",
                "fields": [],
                "oauth_config": {"pkce_enabled": False},
            }
        )
        self.assertIsNotNone(pattern.oauth_config)
        self.assertFalse(pattern.oauth_config.pkce_enabled)

    def test_unknown_keys_survive_round_trip(self):
        """A key the SDK does not model is preserved, not silently dropped.

        auth_patterns is an untyped ListValue, so the server can add keys at any
        level. Dropping them is what made SK-2030 recur one level up.
        """
        pattern = AuthPattern.from_dict(
            {
                "type": "API_KEY",
                "display_name": "API Key",
                "some_future_pattern_key": {"a": 1},
                "oauth_config": {"pkce_enabled": True, "some_future_oauth_key": "x"},
                "fields": [
                    {
                        "field_name": "api_key",
                        "input_type": "password",
                        "some_future_field_key": {"b": 2},
                        "options": [{"value": "v", "some_future_option_key": 3}],
                    }
                ],
            }
        )
        encoded = pattern.to_dict()
        self.assertEqual(encoded["some_future_pattern_key"], {"a": 1})
        self.assertEqual(encoded["oauth_config"]["some_future_oauth_key"], "x")
        self.assertEqual(encoded["fields"][0]["some_future_field_key"], {"b": 2})
        self.assertEqual(
            encoded["fields"][0]["options"][0]["some_future_option_key"], 3
        )

    def test_account_fields_and_proxy_domains_decode(self):
        """account_fields and allowed_proxy_domains are modelled, not dropped."""
        pattern = AuthPattern.from_dict(
            {
                "type": "API_KEY",
                "display_name": "API Key",
                "fields": [],
                "account_fields": [{"field_name": "subdomain", "input_type": "text"}],
                "allowed_proxy_domains": ["api.example.com"],
            }
        )
        self.assertEqual([f.field_name for f in pattern.account_fields], ["subdomain"])
        self.assertEqual(pattern.allowed_proxy_domains, ["api.example.com"])

    def test_header_name_and_is_path_param_decode(self):
        """Multi-header API_KEY mode and path-param fields round-trip."""
        field = AuthField.from_dict(
            {"field_name": "region", "is_path_param": True, "header_name": "X-Api-Key"}
        )
        self.assertTrue(field.is_path_param)
        self.assertEqual(field.header_name, "X-Api-Key")
        self.assertEqual(AuthField.from_dict(field.to_dict()).header_name, "X-Api-Key")

    def test_oauth_config_detail_is_preserved(self):
        """OAuthConfig models only pkce_enabled; the rest must not be dropped.

        A caller that lists providers, edits one and writes it back would
        otherwise erase the connector's OAuth endpoints and scopes.
        """
        served = {
            "pkce_enabled": True,
            "authorize_uri": "https://auth.example.com/authorize",
            "token_uri": "https://auth.example.com/token",
            "user_info_uri": "https://api.example.com/userinfo",
            "allow_use_scalekit_credentials": True,
            "available_scopes": [
                {
                    "scope": "example.read",
                    "display_name": "Read",
                    "description": "Read access",
                    "required": True,
                }
            ],
        }
        encoded = AuthPattern.from_dict(
            {
                "type": "OAUTH",
                "display_name": "OAuth 2.0",
                "fields": [],
                "oauth_config": served,
            }
        ).to_dict()["oauth_config"]
        for key, value in served.items():
            with self.subTest(key=key):
                self.assertEqual(encoded[key], value)

    def test_decoded_pattern_stays_editable(self):
        """Editing a decoded pattern must not trip the authoring guardrails.

        validate_assignment=True re-runs the model validator on every attribute
        write, and that re-run carries no validation context. A served shape the
        guardrails would reject must stay editable once decoded.
        """
        pattern = AuthPattern.from_dict(
            {
                "type": "OAUTH",
                "display_name": "Example",
                "fields": [{"field_name": "example_choice", "input_type": "select"}],
            }
        )
        pattern.description = "edited"
        self.assertEqual(pattern.description, "edited")
        self.assertEqual(len(pattern.fields), 1)

    def test_json_nulls_are_tolerated(self):
        """Nullable server fields can arrive as JSON null, not just absent.

        oauth_config, hint and the list fields are all nullable server-side, and
        a null used to raise AttributeError rather than decode.
        """
        pattern = AuthPattern.from_dict(
            {
                "type": "API_KEY",
                "display_name": "Example",
                "fields": None,
                "account_fields": None,
                "allowed_proxy_domains": None,
                "oauth_config": None,
            }
        )
        self.assertEqual(pattern.fields, [])
        self.assertEqual(pattern.account_fields, [])
        self.assertEqual(pattern.allowed_proxy_domains, [])
        self.assertIsNone(pattern.oauth_config)
        self.assertNotIn("oauth_config", pattern.to_dict())

        field = AuthField.from_dict(
            {"field_name": "f", "hint": None, "label": None, "options": None}
        )
        self.assertEqual(field.hint, "")
        self.assertEqual(field.label, "")
        self.assertEqual(field.options, [])

    def test_pattern_without_fields_key_decodes(self):
        """'fields' is not guaranteed present on a served pattern."""
        pattern = AuthPattern.from_dict({"type": "API_KEY", "display_name": "Example"})
        self.assertEqual(pattern.fields, [])

    def test_non_identifier_keys_are_accepted(self):
        """A Struct can carry any string key, including ones that are not identifiers."""
        encoded = AuthField.from_dict(
            {"field_name": "x", "weird-key": 1, "class": 2}
        ).to_dict()
        self.assertEqual(encoded["weird-key"], 1)
        self.assertEqual(encoded["class"], 2)

    def test_defaults_stay_off_the_wire(self):
        """New fields must not bloat the create payload when unset."""
        self.assertEqual(
            AuthField(field_name="api_key", input_type="password").to_dict(),
            {"field_name": "api_key", "label": "", "input_type": "password"},
        )

    def test_round_trip_preserves_the_whole_pattern(self):
        """from_dict -> to_dict returns what came in.

        to_dict() omits keys holding their default ('description' here), so the
        objects are compared rather than the raw dicts.
        """
        once = AuthPattern.from_dict(SERVED_OAUTH_PATTERN)
        self.assertEqual(AuthPattern.from_dict(once.to_dict()), once)
        self.assertEqual(
            set(SERVED_OAUTH_PATTERN) - set(once.to_dict()), {"description"}
        )

    def test_round_trip_survives_the_protobuf_wire(self):
        """The real create/update path must not alter a pattern either.

        _patterns_to_list_value is what create_custom_provider and
        update_custom_provider actually send, so this covers ParseDict into the
        ListValue as well as the model.
        """
        decoded = AuthPattern.from_dict(SERVED_OAUTH_PATTERN)
        wire = MessageToDict(_patterns_to_list_value([decoded]))[0]
        self.assertEqual(AuthPattern.from_dict(wire), decoded)
        self.assertEqual(wire["fields"][0]["options"][0]["value"], "first")


class TestAuthPatternAuthoringGuards(unittest.TestCase):
    """The authoring guardrails that remain on direct construction.

    These are SDK-side help for create_custom_provider, not server rules, so
    they must not run when decoding a response — see TestServedPatternDecoding.
    """

    def test_oauth_requires_oauth_config(self):
        with self.assertRaises(Exception) as ctx:
            AuthPattern(type="OAUTH", display_name="Example")
        self.assertIn("oauth_config is required", str(ctx.exception))

    def test_no_auth_rejects_fields(self):
        with self.assertRaises(Exception) as ctx:
            AuthPattern(
                type="NO_AUTH",
                display_name="Public",
                fields=[AuthField(field_name="token")],
            )
        self.assertIn("fields must be empty", str(ctx.exception))

    def test_oauth_with_fields_is_allowed(self):
        """Dropped guard: OAuth connectors do collect pre-flow options."""
        pattern = AuthPattern(
            type="OAUTH",
            display_name="Example",
            oauth_config=OAuthConfig(),
            fields=[
                AuthField(
                    field_name="example_choice",
                    input_type="select",
                    options=[AuthFieldOption(value="first", display_name="First")],
                )
            ],
        )
        self.assertEqual(pattern.fields[0].options[0].value, "first")

    def test_non_oauth_type_with_oauth_config_is_allowed(self):
        """Dropped guard: other OAuth-family types legitimately carry one."""
        pattern = AuthPattern(
            type="SOME_FUTURE_TYPE", display_name="Example", oauth_config=OAuthConfig()
        )
        self.assertIsNotNone(pattern.oauth_config)

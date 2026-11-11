"""Offline tests for OpenAPI-sourced custom connectors: the gRPC layer is stubbed, no environment needed."""
import unittest
from unittest.mock import MagicMock

from google.protobuf.json_format import MessageToDict, ParseDict
from pydantic import ValidationError

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import (
    AuthField,
    AuthPattern,
    CreateCustomProviderRequest,
    OAuthConfig,
    Provider,
    UpdateCustomProviderRequest,
)
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitConflictException,
)
from scalekit.providers import ProvidersClient, _patterns_to_list_value
from scalekit.v1.providers import providers_pb2 as pb

SPEC_URL = "https://api.example.com/openapi.json"
MCP_URL = "https://mcp.example.com/mcp"


def _server_error(cls, message, code):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


def _api_key_pattern(**kw) -> AuthPattern:
    return AuthPattern(
        type="API_KEY",
        display_name="API Key",
        fields=[AuthField(field_name="api_key", label="API Key", input_type="password", required=True)],
        **kw,
    )


def _proto_provider(**kw) -> pb.Provider:
    patterns = kw.pop("auth_patterns", [])
    provider = pb.Provider(
        id="prvd_1", identifier="PETSTORE:12", display_name="Petstore", is_custom=True, **kw
    )
    if patterns:
        ParseDict(patterns, provider.auth_patterns)
    return provider


class ProvidersTestCase(unittest.TestCase):
    def setUp(self):
        self.core = MagicMock()
        self.calls = []
        self.low = ProvidersClient(self.core)
        self.client = ActionClient(MagicMock(), MagicMock(), providers_client=self.low)

    def _reply(self, *responses):
        """Queue responses for grpc_exec; an exception in the queue is raised."""
        queue = list(responses)

        def grpc_exec(rpc, request, **kwargs):
            self.calls.append((rpc, request, kwargs))
            item = queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return (item, None)

        self.core.grpc_exec.side_effect = grpc_exec


class CreateOpenApiConnectorTest(ProvidersTestCase):
    def test_low_level_create_sends_the_spec_url_and_no_proxy_url(self):
        self._reply(pb.CreateProviderResponse(provider=_proto_provider(openapi_spec_url=SPEC_URL)))
        self.low.create_custom_provider(
            "Petstore", openapi_spec_url=SPEC_URL, auth_patterns=[_api_key_pattern()]
        )
        request = self.calls[0][1]
        self.assertEqual(request.provider.openapi_spec_url, SPEC_URL)
        self.assertEqual(request.provider.proxy_url, "")
        self.assertEqual(request.provider.display_name, "Petstore")
        self.assertTrue(request.provider.proxy_enabled)  # the SDK default, unchanged
        self.assertEqual(MessageToDict(request.provider.auth_patterns)[0]["type"], "API_KEY")

    def test_low_level_create_for_an_mcp_connector_is_unchanged(self):
        """proxy_url used to be the second positional argument; it still is."""
        self._reply(pb.CreateProviderResponse(provider=_proto_provider(proxy_url=MCP_URL)))
        self.low.create_custom_provider("Acme MCP", MCP_URL, auth_patterns=[_api_key_pattern()])
        request = self.calls[0][1]
        self.assertEqual(request.provider.proxy_url, MCP_URL)
        self.assertEqual(request.provider.openapi_spec_url, "")

    def test_a_spec_url_gets_the_longer_deadline_because_the_server_fetches_it(self):
        self._reply(
            pb.CreateProviderResponse(provider=_proto_provider()),
            pb.CreateProviderResponse(provider=_proto_provider()),
        )
        self.low.create_custom_provider("Petstore", openapi_spec_url=SPEC_URL, auth_patterns=[_api_key_pattern()])
        self.low.create_custom_provider("Acme MCP", MCP_URL, auth_patterns=[_api_key_pattern()])
        self.assertIs(self.calls[0][2]["timeout"], self.core.tool_call_timeout_s)
        self.assertIsNone(self.calls[1][2]["timeout"])  # an MCP connector keeps the default deadline

    def test_a_spec_url_create_is_not_retried_when_unavailable(self):
        """The create is not idempotent: a retry after a lost response would hit the duplicate-name 409."""
        self._reply(
            pb.CreateProviderResponse(provider=_proto_provider()),
            pb.CreateProviderResponse(provider=_proto_provider()),
        )
        self.client.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name="Petstore", openapi_spec_url=SPEC_URL, auth_patterns=[_api_key_pattern()]
            )
        )
        self.low.create_custom_provider("Acme MCP", MCP_URL, auth_patterns=[_api_key_pattern()])
        self.assertIs(self.calls[0][2]["retry_on_unavailable"], False)
        self.assertIs(self.calls[1][2]["retry_on_unavailable"], True)  # an MCP create keeps the retry

    def test_typed_create_maps_every_field_and_decodes_the_response(self):
        self._reply(
            pb.CreateProviderResponse(
                provider=_proto_provider(
                    openapi_spec_url=SPEC_URL,
                    proxy_enabled=True,
                    auth_patterns=[
                        {
                            "type": "API_KEY",
                            "display_name": "API Key",
                            "is_open_api": True,
                            "fields": [{"field_name": "api_key", "input_type": "password"}],
                        }
                    ],
                )
            )
        )
        response = self.client.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name="Petstore",
                description="Pets",
                openapi_spec_url=SPEC_URL,
                auth_patterns=[_api_key_pattern()],
                icon_src="https://example.com/icon.svg",
                metadata={"team": "pets"},
            )
        )
        sent = self.calls[0][1].provider
        self.assertEqual(
            (sent.display_name, sent.description, sent.openapi_spec_url, sent.proxy_url, sent.icon_src),
            ("Petstore", "Pets", SPEC_URL, "", "https://example.com/icon.svg"),
        )
        self.assertEqual(dict(sent.metadata), {"team": "pets"})
        provider = response.provider
        self.assertEqual(provider.openapi_spec_url, SPEC_URL)
        self.assertEqual(provider.identifier, "PETSTORE:12")
        self.assertTrue(provider.is_custom)
        self.assertFalse(provider.is_custom_mcp)
        self.assertTrue(provider.auth_patterns[0].is_open_api)

    def test_exactly_one_source_is_required(self):
        patterns = [_api_key_pattern()]
        with self.assertRaises(ValidationError) as both:
            CreateCustomProviderRequest(
                display_name="Petstore", proxy_url=MCP_URL, openapi_spec_url=SPEC_URL, auth_patterns=patterns
            )
        self.assertIn("proxy_url cannot be set together with openapi_spec_url", str(both.exception))
        with self.assertRaises(ValidationError) as neither:
            CreateCustomProviderRequest(display_name="Petstore", auth_patterns=patterns)
        self.assertIn("either proxy_url or openapi_spec_url must be set", str(neither.exception))

    def test_urls_must_be_https(self):
        with self.assertRaises(ValidationError) as ctx:
            CreateCustomProviderRequest(
                display_name="Petstore",
                openapi_spec_url="http://api.example.com/openapi.json",
                auth_patterns=[_api_key_pattern()],
            )
        self.assertIn("openapi_spec_url must be a valid HTTPS URL", str(ctx.exception))
        with self.assertRaises(ValidationError):
            CreateCustomProviderRequest(display_name="Acme", proxy_url="http://mcp.example.com")

    def test_an_mcp_request_still_validates_the_same_way(self):
        request = CreateCustomProviderRequest(display_name="Acme MCP", proxy_url=MCP_URL)
        self.assertEqual(request.proxy_url, MCP_URL)
        self.assertIsNone(request.openapi_spec_url)

    def test_server_rejections_reach_the_caller_unchanged(self):
        patterns = [_api_key_pattern()]
        self._reply(
            _server_error(
                ScalekitBadRequestException,
                "OpenAPI-sourced connectors are not enabled for this environment",
                "FEATURE_NOT_ENABLED",
            ),
            _server_error(
                ScalekitConflictException,
                'an OpenAPI connector named "PETSTORE" already exists in this environment',
                "RESOURCE_ALREADY_EXISTS",
            ),
        )
        request = CreateCustomProviderRequest(
            display_name="Petstore", openapi_spec_url=SPEC_URL, auth_patterns=patterns
        )
        with self.assertRaises(ScalekitBadRequestException) as disabled:
            self.client.providers.create_custom_provider(request)
        self.assertEqual(disabled.exception.error_code, "FEATURE_NOT_ENABLED")
        with self.assertRaises(ScalekitConflictException) as duplicate:
            self.client.providers.create_custom_provider(request)
        self.assertEqual(duplicate.exception.error_code, "RESOURCE_ALREADY_EXISTS")


class UpdateOpenApiConnectorTest(ProvidersTestCase):
    def _stored(self):
        """The provider as list_providers returns it for an OpenAPI-sourced connector."""
        return Provider.from_proto(
            _proto_provider(
                openapi_spec_url=SPEC_URL,
                proxy_url="https://api.example.com/v1",
                proxy_enabled=True,
                metadata={"team": "pets"},
                auth_patterns=[
                    {
                        "type": "OAUTH",
                        "display_name": "OAuth",
                        "is_open_api": True,
                        "fields": [],
                        "oauth_config": {
                            "pkce_enabled": True,
                            "authorize_uri": "https://auth.example.com/authorize",
                            "token_uri": "https://auth.example.com/token",
                        },
                    }
                ],
            )
        )

    def test_a_rename_needs_no_proxy_url_and_sends_the_stored_values_back(self):
        stored = self._stored()
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider(openapi_spec_url=SPEC_URL)))
        self.client.providers.update_custom_provider(
            UpdateCustomProviderRequest(
                identifier=stored.identifier,
                display_name="Petstore Two",
                auth_patterns=stored.auth_patterns,
                proxy_enabled=stored.proxy_enabled,
                metadata=stored.metadata,
            )
        )
        request = self.calls[0][1]
        self.assertEqual(request.identifier, "PETSTORE:12")
        sent = request.provider
        self.assertEqual(sent.display_name, "Petstore Two")
        self.assertEqual(sent.proxy_url, "")  # omitted: the stored base URL is kept
        self.assertEqual(sent.openapi_spec_url, "")
        self.assertTrue(sent.proxy_enabled)
        self.assertEqual(dict(sent.metadata), {"team": "pets"})
        # The pattern goes back as it was read, including the server-derived flag and the
        # URLs the first run filled in, because the server compares patterns by content.
        pattern = MessageToDict(sent.auth_patterns)[0]
        self.assertTrue(pattern["is_open_api"])
        self.assertEqual(pattern["oauth_config"]["authorize_uri"], "https://auth.example.com/authorize")
        self.assertEqual(pattern["oauth_config"]["token_uri"], "https://auth.example.com/token")

    def test_base_url_and_spec_url_changes_are_sent(self):
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider()))
        self.client.providers.update_custom_provider(
            UpdateCustomProviderRequest(
                identifier="PETSTORE:12",
                display_name="Petstore",
                auth_patterns=[_api_key_pattern(is_open_api=True)],
                proxy_url="https://api.example.com/v2",
                openapi_spec_url="https://api.example.com/v2/openapi.json",
                proxy_enabled=True,
            )
        )
        sent = self.calls[0][1].provider
        self.assertEqual(sent.proxy_url, "https://api.example.com/v2")
        self.assertEqual(sent.openapi_spec_url, "https://api.example.com/v2/openapi.json")

    def test_fields_left_as_none_are_not_sent(self):
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider()))
        self.client.providers.update_custom_provider(
            UpdateCustomProviderRequest(
                identifier="ACME:1", display_name="Acme MCP", proxy_url=MCP_URL, auth_patterns=[_api_key_pattern()]
            )
        )
        sent = self.calls[0][1].provider
        self.assertEqual(sent.proxy_url, MCP_URL)
        self.assertEqual((sent.openapi_spec_url, sent.description, sent.icon_src), ("", "", ""))
        self.assertFalse(sent.proxy_enabled)  # not sent: the proto default, which the server applies
        self.assertEqual(dict(sent.metadata), {})

    def test_proxy_enabled_false_is_accepted_by_the_low_level_client(self):
        """proxy_enabled is a plain proto3 bool: False and not sending it are the same bytes."""
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider()))
        self.low.update_custom_provider(
            "ACME:1", "Acme MCP", proxy_url=MCP_URL, proxy_enabled=False, auth_patterns=[_api_key_pattern()]
        )
        self.assertFalse(self.calls[0][1].provider.proxy_enabled)

    def test_typed_update_forwards_proxy_enabled(self):
        self._reply(
            pb.UpdateProviderResponse(provider=_proto_provider()),
            pb.UpdateProviderResponse(provider=_proto_provider()),
        )
        for proxy_enabled in (True, None):
            self.client.providers.update_custom_provider(
                UpdateCustomProviderRequest(
                    identifier="ACME:1",
                    display_name="Acme MCP",
                    proxy_url=MCP_URL,
                    auth_patterns=[_api_key_pattern()],
                    proxy_enabled=proxy_enabled,
                )
            )
        self.assertIs(self.calls[0][1].provider.proxy_enabled, True)
        self.assertIs(self.calls[1][1].provider.proxy_enabled, False)  # None is not sent: the proto default

    def test_an_empty_proxy_url_or_spec_url_is_treated_like_none(self):
        """Provider.proxy_url is "" until the first run fills it in; reading and sending it back must work."""
        stored = Provider.from_proto(_proto_provider(openapi_spec_url=SPEC_URL, proxy_url="", proxy_enabled=True))
        request = UpdateCustomProviderRequest(
            identifier=stored.identifier,
            display_name=stored.display_name,
            auth_patterns=[_api_key_pattern(is_open_api=True)],
            proxy_url=stored.proxy_url,
            openapi_spec_url="",
            proxy_enabled=stored.proxy_enabled,
        )
        self.assertEqual((request.proxy_url, request.openapi_spec_url), ("", ""))
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider()))
        self.client.providers.update_custom_provider(request)
        sent = self.calls[0][1].provider
        self.assertEqual((sent.proxy_url, sent.openapi_spec_url), ("", ""))
        self.assertIsNone(self.calls[0][2]["timeout"])  # no spec URL change, so the default deadline
        with self.assertRaises(ValidationError):
            request.proxy_url = "http://api.example.com"

    def test_only_a_spec_url_change_gets_the_longer_deadline(self):
        self._reply(
            pb.UpdateProviderResponse(provider=_proto_provider()),
            pb.UpdateProviderResponse(provider=_proto_provider()),
        )
        self.low.update_custom_provider("PETSTORE:12", "Petstore", openapi_spec_url=SPEC_URL)
        self.low.update_custom_provider("PETSTORE:12", "Petstore", proxy_url="https://api.example.com/v2")
        self.assertIs(self.calls[0][2]["timeout"], self.core.tool_call_timeout_s)
        self.assertIsNone(self.calls[1][2]["timeout"])

    def test_the_old_positional_call_still_maps(self):
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider()))
        self.low.update_custom_provider("ACME:1", "Acme MCP", MCP_URL, "New description")
        sent = self.calls[0][1].provider
        self.assertEqual((sent.proxy_url, sent.description), (MCP_URL, "New description"))

    def test_urls_must_be_https(self):
        with self.assertRaises(ValidationError):
            UpdateCustomProviderRequest(
                identifier="PETSTORE:12", display_name="Petstore", openapi_spec_url="http://api.example.com/o.json"
            )
        with self.assertRaises(ValidationError):
            UpdateCustomProviderRequest(
                identifier="PETSTORE:12", display_name="Petstore", proxy_url="http://api.example.com"
            )

    def test_server_rejections_reach_the_caller_unchanged(self):
        self._reply(
            _server_error(
                ScalekitBadRequestException,
                "an OpenAPI-sourced connector can only update metadata, display_name, description, "
                "icon_src and proxy_url",
                "INVALID_ARGUMENT",
            ),
            _server_error(
                ScalekitConflictException,
                "base_url was saved, but an ingestion run is already in progress for this connector",
                "RESOURCE_ALREADY_EXISTS",
            ),
        )
        request = UpdateCustomProviderRequest(
            identifier="PETSTORE:12",
            display_name="Petstore",
            proxy_url="https://api.example.com/v2",
            auth_patterns=[_api_key_pattern()],
        )
        with self.assertRaises(ScalekitBadRequestException):
            self.client.providers.update_custom_provider(request)
        with self.assertRaises(ScalekitConflictException) as saved:
            self.client.providers.update_custom_provider(request)
        self.assertIn("was saved", saved.exception.message)


class ReadOpenApiConnectorTest(unittest.TestCase):
    def test_provider_carries_the_spec_url_and_base_url(self):
        provider = Provider.from_proto(
            _proto_provider(openapi_spec_url=SPEC_URL, proxy_url="https://api.example.com/v1")
        )
        self.assertEqual(provider.openapi_spec_url, SPEC_URL)
        self.assertEqual(provider.proxy_url, "https://api.example.com/v1")
        self.assertEqual(provider.model_dump()["openapi_spec_url"], SPEC_URL)

    def test_an_mcp_provider_has_an_empty_spec_url(self):
        self.assertEqual(Provider.from_proto(_proto_provider(proxy_url=MCP_URL)).openapi_spec_url, "")

    def test_is_open_api_round_trips_through_the_wire(self):
        decoded = AuthPattern.from_dict(
            {"type": "OAUTH", "display_name": "OAuth", "is_open_api": True, "oauth_config": {"pkce_enabled": True}}
        )
        self.assertTrue(decoded.is_open_api)
        wire = MessageToDict(_patterns_to_list_value([decoded]))[0]
        self.assertTrue(wire["is_open_api"])
        self.assertEqual(AuthPattern.from_dict(wire), decoded)

    def test_is_open_api_stays_off_the_wire_when_authoring(self):
        pattern = AuthPattern(type="OAUTH", display_name="OAuth", oauth_config=OAuthConfig())
        self.assertFalse(pattern.is_open_api)
        self.assertNotIn("is_open_api", pattern.to_dict())


if __name__ == "__main__":
    unittest.main()

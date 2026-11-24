"""Offline tests for OpenAPI-sourced custom connectors: the gRPC layer is stubbed, no environment needed."""
import inspect
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

    def assertNoDeadlineOverride(self, kwargs):
        """The call passes no per-call deadline (timeout=None), so grpc_exec applies the client's default."""
        self.assertIsNone(kwargs.get("timeout"))


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
        self.assertTrue(request.provider.proxy_enabled)  # a custom connector is always created with True
        self.assertEqual(MessageToDict(request.provider.auth_patterns)[0]["type"], "API_KEY")

    def test_low_level_create_for_an_mcp_connector_is_unchanged(self):
        """proxy_url used to be the second positional argument; it still is."""
        self._reply(pb.CreateProviderResponse(provider=_proto_provider(proxy_url=MCP_URL)))
        self.low.create_custom_provider("Acme MCP", MCP_URL, auth_patterns=[_api_key_pattern()])
        request = self.calls[0][1]
        self.assertEqual(request.provider.proxy_url, MCP_URL)
        self.assertEqual(request.provider.openapi_spec_url, "")

    def test_a_custom_connector_is_always_created_with_proxy_enabled_true(self):
        """Whatever the caller passes: the argument is kept so that existing calls keep working, and ignored."""
        self._reply(*[pb.CreateProviderResponse(provider=_proto_provider())] * 3)
        pattern = [_api_key_pattern()]
        self.low.create_custom_provider("Acme MCP", MCP_URL, auth_patterns=pattern)
        self.low.create_custom_provider("Acme MCP", MCP_URL, proxy_enabled=True, auth_patterns=pattern)
        self.low.create_custom_provider("Acme MCP", MCP_URL, proxy_enabled=False, auth_patterns=pattern)
        self.assertEqual([c[1].provider.proxy_enabled for c in self.calls], [True, True, True])

    def test_the_typed_create_ignores_proxy_enabled_but_still_accepts_it(self):
        self._reply(*[pb.CreateProviderResponse(provider=_proto_provider())] * 2)
        for value in (False, True):
            request = CreateCustomProviderRequest(
                display_name="Acme MCP", proxy_url=MCP_URL, auth_patterns=[_api_key_pattern()], proxy_enabled=value
            )
            self.assertIs(request.proxy_enabled, value)  # the field still exists: no existing code breaks
            self.client.providers.create_custom_provider(request)
        self.assertEqual([c[1].provider.proxy_enabled for c in self.calls], [True, True])

    def test_the_low_level_create_keeps_its_signature_so_positional_calls_keep_working(self):
        parameters = inspect.signature(ProvidersClient.create_custom_provider).parameters
        self.assertEqual(
            list(parameters),
            ["self", "display_name", "proxy_url", "proxy_enabled", "description", "auth_patterns", "icon_src",
             "metadata", "openapi_spec_url"],
        )
        self.assertTrue(all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD for p in parameters.values()))
        # An old call that passes every argument by position, proxy_enabled=False included.
        self._reply(pb.CreateProviderResponse(provider=_proto_provider()))
        self.low.create_custom_provider(
            "Acme MCP", MCP_URL, False, "Desc", [_api_key_pattern()], "https://icons.example.com/a.png", {"team": "x"}
        )
        sent = self.calls[0][1].provider
        self.assertEqual((sent.proxy_url, sent.description, sent.icon_src), (MCP_URL, "Desc", "https://icons.example.com/a.png"))
        self.assertEqual(dict(sent.metadata), {"team": "x"})
        self.assertIs(sent.proxy_enabled, True)

    def test_a_create_passes_no_deadline_override_with_or_without_a_spec_url(self):
        self._reply(
            pb.CreateProviderResponse(provider=_proto_provider()),
            pb.CreateProviderResponse(provider=_proto_provider()),
        )
        self.low.create_custom_provider("Petstore", openapi_spec_url=SPEC_URL, auth_patterns=[_api_key_pattern()])
        self.low.create_custom_provider("Acme MCP", MCP_URL, auth_patterns=[_api_key_pattern()])
        for _, _, kwargs in self.calls:
            self.assertNoDeadlineOverride(kwargs)

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

    def test_a_basic_pattern_sends_username_and_password_and_reads_them_back(self):
        """BASIC is accepted on an OpenAPI-sourced connector; its two credential fields are named username and password."""
        fields = [
            {"field_name": "username", "label": "Username", "input_type": "text", "required": True},
            {"field_name": "password", "label": "Password", "input_type": "password", "required": True},
        ]
        self._reply(
            pb.CreateProviderResponse(
                provider=_proto_provider(
                    openapi_spec_url=SPEC_URL,
                    auth_patterns=[
                        {"type": "BASIC", "display_name": "Basic Auth", "is_open_api": True, "fields": fields}
                    ],
                )
            )
        )
        response = self.client.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name="Petstore",
                openapi_spec_url=SPEC_URL,
                auth_patterns=[
                    AuthPattern(type="BASIC", display_name="Basic Auth", fields=[AuthField(**f) for f in fields])
                ],
            )
        )
        sent = MessageToDict(self.calls[0][1].provider.auth_patterns)[0]
        self.assertEqual(sent["type"], "BASIC")
        self.assertEqual(
            [(f["field_name"], f["input_type"], f["required"]) for f in sent["fields"]],
            [("username", "text", True), ("password", "password", True)],
        )
        read = response.provider.auth_patterns[0]
        self.assertEqual((read.type, read.is_open_api), ("BASIC", True))
        self.assertEqual([(f.field_name, f.input_type) for f in read.fields], [("username", "text"), ("password", "password")])

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
                metadata=stored.metadata,
            )
        )
        request = self.calls[0][1]
        self.assertEqual(request.identifier, "PETSTORE:12")
        sent = request.provider
        self.assertEqual(sent.display_name, "Petstore Two")
        self.assertEqual(sent.proxy_url, "")  # omitted: the stored base URL is kept
        self.assertEqual(sent.openapi_spec_url, "")
        self.assertTrue(sent.proxy_enabled)  # always sent: the value the SDK creates every connector with
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
        self.assertEqual(dict(sent.metadata), {})

    def test_the_low_level_update_has_no_proxy_enabled_argument_and_sends_true(self):
        """The server applies proxy_enabled (a plain bool) on every update and, for an OpenAPI-sourced
        connector, rejects one that differs from the stored value, so the SDK always sends True."""
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider()))
        with self.assertRaises(TypeError):
            self.low.update_custom_provider(
                "ACME:1", "Acme MCP", proxy_url=MCP_URL, proxy_enabled=False, auth_patterns=[_api_key_pattern()]
            )
        self.assertEqual(self.calls, [])  # nothing was sent
        self.low.update_custom_provider("ACME:1", "Acme MCP", proxy_url=MCP_URL, auth_patterns=[_api_key_pattern()])
        self.assertIs(self.calls[0][1].provider.proxy_enabled, True)

    def test_the_typed_update_has_no_proxy_enabled_field_and_sends_true(self):
        self._reply(*[pb.UpdateProviderResponse(provider=_proto_provider())] * 2)
        request = UpdateCustomProviderRequest(
            identifier="ACME:1", display_name="Acme MCP", proxy_url=MCP_URL, auth_patterns=[_api_key_pattern()]
        )
        self.assertFalse(hasattr(request, "proxy_enabled"))
        self.client.providers.update_custom_provider(request)
        # A proxy_enabled passed anyway is dropped by the model and changes nothing on the wire.
        ignored = UpdateCustomProviderRequest(
            identifier="ACME:1", display_name="Acme MCP", proxy_url=MCP_URL, auth_patterns=[_api_key_pattern()],
            proxy_enabled=False,
        )
        self.assertFalse(hasattr(ignored, "proxy_enabled"))
        self.client.providers.update_custom_provider(ignored)
        self.assertEqual([c[1].provider.proxy_enabled for c in self.calls], [True, True])

    def test_an_empty_proxy_url_or_spec_url_is_treated_like_none(self):
        """Provider.proxy_url is "" until the first run fills it in; reading and sending it back must work."""
        stored = Provider.from_proto(_proto_provider(openapi_spec_url=SPEC_URL, proxy_url="", proxy_enabled=True))
        request = UpdateCustomProviderRequest(
            identifier=stored.identifier,
            display_name=stored.display_name,
            auth_patterns=[_api_key_pattern(is_open_api=True)],
            proxy_url=stored.proxy_url,
            openapi_spec_url="",
        )
        self.assertEqual((request.proxy_url, request.openapi_spec_url), ("", ""))
        self._reply(pb.UpdateProviderResponse(provider=_proto_provider()))
        self.client.providers.update_custom_provider(request)
        sent = self.calls[0][1].provider
        self.assertEqual((sent.proxy_url, sent.openapi_spec_url), ("", ""))
        self.assertNoDeadlineOverride(self.calls[0][2])
        with self.assertRaises(ValidationError):
            request.proxy_url = "http://api.example.com"

    def test_an_update_passes_no_deadline_override_with_or_without_a_spec_url(self):
        self._reply(
            pb.UpdateProviderResponse(provider=_proto_provider()),
            pb.UpdateProviderResponse(provider=_proto_provider()),
        )
        self.low.update_custom_provider("PETSTORE:12", "Petstore", openapi_spec_url=SPEC_URL)
        self.low.update_custom_provider("PETSTORE:12", "Petstore", proxy_url="https://api.example.com/v2")
        for _, _, kwargs in self.calls:
            self.assertNoDeadlineOverride(kwargs)

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

"""Offline tests for auth pattern shapes of custom connectors: credential placement and multiple
headers. The gRPC layer is stubbed; no environment is needed."""
import unittest
from unittest.mock import MagicMock

from google.protobuf.json_format import MessageToDict

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import (
    AuthField,
    AuthPattern,
    CreateCustomProviderRequest,
    CredentialPlacement,
)
from scalekit.common.exceptions import ScalekitBadRequestException
from scalekit.providers import ProvidersClient, _patterns_to_list_value
from scalekit.v1.providers import providers_pb2 as pb

SPEC_URL = "https://api.example.com/openapi.json"


def _server_error(cls, message, code):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


def _wire(pattern: AuthPattern) -> dict:
    """The pattern as it reaches the server."""
    return MessageToDict(_patterns_to_list_value([pattern]))[0]


class CredentialPlacementTest(unittest.TestCase):
    def test_a_placement_goes_on_the_wire_as_in_and_name(self):
        pattern = AuthPattern(
            type="API_KEY",
            display_name="API Key",
            fields=[
                AuthField(
                    field_name="api_key",
                    input_type="password",
                    required=True,
                    placement=CredentialPlacement(in_=CredentialPlacement.QUERY, name="token"),
                )
            ],
        )
        self.assertEqual(_wire(pattern)["fields"][0]["placement"], {"in": "query", "name": "token"})

    def test_a_dict_with_the_wire_key_is_accepted(self):
        field = AuthField(field_name="token", input_type="password", placement={"in": "body", "name": "apiKey"})
        self.assertEqual(field.placement, CredentialPlacement(in_="body", name="apiKey"))
        self.assertEqual(field.placement.in_, "body")

    def test_the_constants_are_the_wire_values(self):
        self.assertEqual(
            (CredentialPlacement.PATH, CredentialPlacement.QUERY, CredentialPlacement.BODY),
            ("path", "query", "body"),
        )

    def test_a_placement_is_not_restricted_to_the_known_locations(self):
        """The server owns the vocabulary and answers 400 for an unknown one; the SDK must not pre-empt it."""
        self.assertEqual(CredentialPlacement(in_="Header", name="x").to_dict(), {"in": "Header", "name": "x"})

    def test_no_placement_stays_off_the_wire(self):
        field = AuthField(field_name="api_key", input_type="password")
        self.assertIsNone(field.placement)
        self.assertNotIn("placement", field.to_dict())

    def test_a_served_placement_decodes_and_round_trips(self):
        for location, name in (("path", "bot_token"), ("query", "token"), ("body", "apiKey")):
            with self.subTest(location):
                served = {"field_name": "api_key", "input_type": "password", "placement": {"in": location, "name": name}}
                field = AuthField.from_dict(served)
                self.assertEqual((field.placement.in_, field.placement.name), (location, name))
                self.assertEqual(field.to_dict()["placement"], {"in": location, "name": name})
                self.assertEqual(AuthField.from_dict(field.to_dict()), field)

    def test_unknown_placement_keys_survive_a_round_trip(self):
        field = AuthField.from_dict({"field_name": "k", "placement": {"in": "query", "name": "t", "future": 1}})
        self.assertEqual(field.to_dict()["placement"], {"in": "query", "name": "t", "future": 1})

    def test_a_null_or_odd_placement_decodes_without_raising(self):
        for served in (None, "query", 3):
            with self.subTest(served=served):
                self.assertIsNone(AuthField.from_dict({"field_name": "k", "placement": served}).placement)

    def test_a_basic_pattern_places_both_halves(self):
        pattern = AuthPattern(
            type="BASIC",
            display_name="Basic",
            fields=[
                AuthField(field_name="username", input_type="text", placement={"in": "query", "name": "user"}),
                AuthField(field_name="password", input_type="password", placement={"in": "query", "name": "pass"}),
            ],
        )
        placed = {f["field_name"]: f["placement"] for f in _wire(pattern)["fields"]}
        self.assertEqual(placed, {"username": {"in": "query", "name": "user"}, "password": {"in": "query", "name": "pass"}})

    def test_a_path_placement_and_its_placeholder_in_proxy_url_reach_the_server(self):
        core = MagicMock()
        calls = []
        core.grpc_exec.side_effect = lambda rpc, request, **kw: calls.append(request) or (
            pb.CreateProviderResponse(provider=pb.Provider(identifier="TELEGRAM:1")),
            None,
        )
        client = ActionClient(MagicMock(), MagicMock(), providers_client=ProvidersClient(core))
        client.providers.create_custom_provider(
            CreateCustomProviderRequest(
                display_name="Telegram",
                proxy_url="https://api.telegram.org/bot{{bot_token}}",
                auth_patterns=[
                    AuthPattern(
                        type="BEARER",
                        display_name="Bot token",
                        fields=[
                            AuthField(
                                field_name="token",
                                input_type="password",
                                placement={"in": "path", "name": "bot_token"},
                            )
                        ],
                    )
                ],
            )
        )
        sent = calls[0].provider
        self.assertEqual(sent.proxy_url, "https://api.telegram.org/bot{{bot_token}}")
        self.assertEqual(
            MessageToDict(sent.auth_patterns)[0]["fields"][0]["placement"], {"in": "path", "name": "bot_token"}
        )

    def test_an_invalid_placement_is_a_400_the_caller_can_read(self):
        core = MagicMock()
        core.grpc_exec.side_effect = _server_error(
            ScalekitBadRequestException,
            'invalid credential placement: field "api_key": a placed credential must use input_type "password"',
            "INVALID_ARGUMENT",
        )
        client = ActionClient(MagicMock(), MagicMock(), providers_client=ProvidersClient(core))
        request = CreateCustomProviderRequest(
            display_name="Petstore",
            openapi_spec_url=SPEC_URL,
            auth_patterns=[
                AuthPattern(
                    type="API_KEY",
                    display_name="API Key",
                    fields=[AuthField(field_name="api_key", placement={"in": "query", "name": "k"})],
                )
            ],
        )
        with self.assertRaises(ScalekitBadRequestException) as ctx:
            client.providers.create_custom_provider(request)
        self.assertTrue(ctx.exception.message.startswith("invalid credential placement:"))


class MultipleHeadersTest(unittest.TestCase):
    def test_header_names_go_on_the_wire_and_come_back(self):
        pattern = AuthPattern(
            type="API_KEY",
            display_name="Keys",
            fields=[
                AuthField(field_name="x_api_key", input_type="password", header_name="X-Api-Key"),
                AuthField(field_name="x_tenant", input_type="text", header_name="X-Tenant"),
            ],
        )
        wire = _wire(pattern)
        self.assertEqual([f["header_name"] for f in wire["fields"]], ["X-Api-Key", "X-Tenant"])
        self.assertEqual(AuthPattern.from_dict(wire).to_dict(), pattern.to_dict())

    def test_a_server_derived_field_name_round_trips(self):
        """The server rewrites field_name to a slug of the header name; the SDK keeps what it is given back."""
        served = {
            "type": "API_KEY",
            "display_name": "Keys",
            "fields": [{"field_name": "x_api_key", "input_type": "password", "header_name": "X-Api-Key"}],
        }
        self.assertEqual(AuthPattern.from_dict(served).to_dict()["fields"][0]["field_name"], "x_api_key")

    def test_the_server_rejections_carry_their_codes(self):
        for message, code in (
            ("multi-header API_KEY connectors are not enabled for this environment", "FEATURE_NOT_ENABLED"),
            ('invalid header name "X-Api-Key2": only letters, \'.\', \'-\' and \'_\' are allowed', "INVALID_HEADER_CONFIG"),
        ):
            with self.subTest(code):
                exc = _server_error(ScalekitBadRequestException, message, code)
                self.assertEqual(exc.error_code, code)
                self.assertEqual(exc.message, message)


if __name__ == "__main__":
    unittest.main()

"""Offline tests for the multiple-headers shape of an API_KEY auth pattern of a custom connector.
The gRPC channel is stubbed; the SDK's own error mapping runs; no environment is needed."""
import unittest
from unittest.mock import MagicMock

import grpc
from google.protobuf import any_pb2
from google.protobuf.json_format import MessageToDict
from google.rpc import status_pb2

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import (
    AuthField,
    AuthPattern,
    CreateCustomProviderRequest,
    UpdateCustomProviderRequest,
)
from scalekit.common.exceptions import ScalekitBadRequestException
from scalekit.core import CoreClient
from scalekit.providers import ProvidersClient, _patterns_to_list_value
from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo


def _rejection(message, error_code):
    """What the channel raises when the server answers 400: INVALID_ARGUMENT, and the error code in an ErrorInfo."""
    detail = any_pb2.Any()
    detail.Pack(ErrorInfo(error_code=error_code))
    status = status_pb2.Status(code=grpc.StatusCode.INVALID_ARGUMENT.value[0], message=message, details=[detail])

    class _Rejection(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.INVALID_ARGUMENT

        def details(self):
            return message

        def trailing_metadata(self):
            return (("grpc-status-details-bin", status.SerializeToString()),)

    return _Rejection()


def _providers(error):
    """client.actions.providers over the real CoreClient.grpc_exec; every create and update RPC raises `error`."""
    core = CoreClient.__new__(CoreClient)  # no network: only its grpc_exec and error mapping are used
    core.access_token = "test-token"
    core.call_timeout_s = 20.0
    core.grpc_secure_channel = MagicMock()
    low = ProvidersClient(core)
    low._stub = MagicMock()
    low._stub.CreateCustomProvider.with_call.side_effect = error
    low._stub.UpdateCustomProvider.with_call.side_effect = error
    return ActionClient(MagicMock(), MagicMock(), providers_client=low).providers


def _wire(pattern: AuthPattern) -> dict:
    """The pattern as it reaches the server."""
    return MessageToDict(_patterns_to_list_value([pattern]))[0]


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
        """A create and an update raise what the server answered: the class, the error code and the message."""
        pattern = AuthPattern(
            type="API_KEY",
            display_name="Keys",
            fields=[AuthField(field_name="x_api_key", input_type="password", header_name="X-Api-Key")],
        )
        create = CreateCustomProviderRequest(
            display_name="Acme MCP", proxy_url="https://mcp.example.com/mcp", auth_patterns=[pattern]
        )
        update = UpdateCustomProviderRequest(
            identifier="ACME:1", display_name="Acme MCP", proxy_url="https://mcp.example.com/mcp", auth_patterns=[pattern]
        )
        for message, code in (
            ("multi-header API_KEY connectors are not enabled for this environment", "FEATURE_NOT_ENABLED"),
            (
                "invalid header name \"X-Api-Key2\": only letters, '.', '-' and '_' are allowed (no digits or spaces)",
                "INVALID_HEADER_CONFIG",
            ),
        ):
            providers = _providers(_rejection(message, code))
            for call, send in (("create", lambda: providers.create_custom_provider(create)),
                               ("update", lambda: providers.update_custom_provider(update))):
                with self.subTest(code=code, call=call):
                    with self.assertRaises(ScalekitBadRequestException) as raised:
                        send()
                    self.assertEqual(raised.exception.error_code, code)
                    self.assertEqual(raised.exception.message, message)


if __name__ == "__main__":
    unittest.main()

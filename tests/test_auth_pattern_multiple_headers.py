"""Offline tests for the multiple-headers shape of an API_KEY auth pattern of a custom connector.
The gRPC layer is stubbed; no environment is needed."""
import unittest

from google.protobuf.json_format import MessageToDict

from scalekit.actions.types import AuthField, AuthPattern
from scalekit.common.exceptions import ScalekitBadRequestException
from scalekit.providers import _patterns_to_list_value


def _server_error(cls, message, code):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


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

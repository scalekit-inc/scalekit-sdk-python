"""Offline tests: create_session_token for an MCP configuration or a connection.

``create_session_token`` targets either an MCP configuration (``mcp_config_id``)
or a connection's MCP server (``connection_name``, sent as ``key_id`` on the
wire), and never sets the other field. Only the connection form gets new
client-side checks; the config form behaves exactly as in v2.20.0 (client.mcp
sends it to the server as given, client.actions.mcp keeps its old checks).
"""

import unittest
from datetime import timedelta
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp

from scalekit.actions.actions import ActionClient
from scalekit.common.exceptions import ScalekitNotFoundException
from scalekit.mcp import McpClient
from scalekit.v1.mcp.mcp_pb2 import CreateMcpSessionTokenResponse

# Connection-token argument combinations that fail before any request, on both facades.
INVALID_CONNECTION_ARGS = {
    "both": {"mcp_config_id": "cfg_1", "connection_name": "GMAIL", "identifier": "u1"},
    "both, config empty": {"mcp_config_id": "", "connection_name": "GMAIL", "identifier": "u1"},
    "empty connection": {"connection_name": "", "identifier": "u1"},
    "connection, missing identifier": {"connection_name": "GMAIL"},
    "connection, None identifier": {"connection_name": "GMAIL", "identifier": None},
    "connection, empty identifier": {"connection_name": "GMAIL", "identifier": ""},
}

# Config-ID calls that client.mcp sends to the server unchanged, as in v2.20.0.
# Each case: (args, kwargs, expected mcp_config_id, expected identifier on the wire).
MCP_CLIENT_PASS_THROUGH = {
    "empty config": (("", "u1"), {}, "", "u1"),
    "whitespace config": (("  ", "u1"), {}, "  ", "u1"),
    "explicit None config": ((None, "u1"), {}, "", "u1"),
    "keyword None config": ((), {"mcp_config_id": None, "identifier": "u1"}, "", "u1"),
    "empty identifier": (("cfg_1", ""), {}, "cfg_1", ""),
    "whitespace identifier": (("cfg_1", " "), {}, "cfg_1", " "),
    "None identifier": (("cfg_1", None), {}, "cfg_1", ""),
}

# client.actions.mcp keeps its v2.20.0 checks and messages for the config form.
ACTIONS_CONFIG_ERRORS = {
    "omitted config": ({"identifier": "u1"}, "mcp_config_id is required"),
    "None config": ({"mcp_config_id": None, "identifier": "u1"}, "mcp_config_id is required"),
    "empty config": ({"mcp_config_id": "", "identifier": "u1"}, "mcp_config_id is required"),
    "missing identifier": ({"mcp_config_id": "cfg_1"}, "identifier is required"),
    "empty identifier": ({"mcp_config_id": "cfg_1", "identifier": ""}, "identifier is required"),
}


def _not_found():
    return ScalekitNotFoundException.__new__(ScalekitNotFoundException)


class TestMcpClientSessionTokenTargets(unittest.TestCase):
    def setUp(self):
        self.core_client = MagicMock()
        self.core_client.grpc_exec.return_value = (CreateMcpSessionTokenResponse(token="tok"), None)
        self.mcp = McpClient.__new__(McpClient)
        self.mcp.core_client = self.core_client
        self.mcp.mcp_service = MagicMock()

    def _sent_request(self):
        return self.core_client.grpc_exec.call_args.args[1]

    # Back-compat: every existing config-token call shape keeps working.

    def test_positional_config_and_identifier(self):
        self.mcp.create_session_token("cfg_1", "user_123")
        request = self._sent_request()
        self.assertEqual(request.mcp_config_id, "cfg_1")
        self.assertEqual(request.identifier, "user_123")
        self.assertEqual(request.key_id, "")
        self.assertFalse(request.HasField("expiry"))
        self.assertEqual(request.access_level, "")

    def test_positional_expiry_and_access_level(self):
        self.mcp.create_session_token("cfg_1", "user_123", timedelta(minutes=5), "READ_ONLY")
        request = self._sent_request()
        self.assertEqual(request.mcp_config_id, "cfg_1")
        self.assertEqual(request.expiry.seconds, 300)
        self.assertEqual(request.access_level, "READ_ONLY")
        self.assertEqual(request.key_id, "")

    def test_keyword_config(self):
        self.mcp.create_session_token(
            mcp_config_id="cfg_1", identifier="u1", expiry=timedelta(minutes=5)
        )
        request = self._sent_request()
        self.assertEqual(request.mcp_config_id, "cfg_1")
        self.assertEqual(request.key_id, "")
        self.assertEqual(request.expiry.seconds, 300)

    # Connection tokens.

    def test_connection_sent_as_key_id_not_config(self):
        self.mcp.create_session_token(connection_name="GMAIL", identifier="u1")
        request = self._sent_request()
        self.assertEqual(request.key_id, "GMAIL")
        self.assertEqual(request.mcp_config_id, "")
        self.assertEqual(request.identifier, "u1")

    def test_connection_name_sent_as_given(self):
        # The server matches names without regard to case; the SDK does not rewrite them.
        self.mcp.create_session_token(connection_name="gMail", identifier="u1")
        self.assertEqual(self._sent_request().key_id, "gMail")

    def test_connection_with_positional_identifier(self):
        self.mcp.create_session_token(None, "u1", connection_name="GMAIL")
        request = self._sent_request()
        self.assertEqual(request.key_id, "GMAIL")
        self.assertEqual(request.identifier, "u1")

    def test_calls_create_mcp_session_token_rpc(self):
        self.mcp.create_session_token(connection_name="GMAIL", identifier="u1")
        self.assertIs(
            self.core_client.grpc_exec.call_args.args[0],
            self.mcp.mcp_service.CreateMcpSessionToken.with_call,
        )

    def test_returns_grpc_exec_result(self):
        result = self.mcp.create_session_token(connection_name="GMAIL", identifier="u1")
        self.assertIs(result, self.core_client.grpc_exec.return_value)

    def test_connection_omitted_optionals_stay_unset(self):
        self.mcp.create_session_token(connection_name="GMAIL", identifier="u1")
        request = self._sent_request()
        self.assertFalse(request.HasField("expiry"))
        self.assertEqual(request.access_level, "")

    def test_connection_forwards_expiry_in_seconds(self):
        self.mcp.create_session_token(
            connection_name="GMAIL", identifier="u1", expiry=timedelta(minutes=15)
        )
        request = self._sent_request()
        self.assertTrue(request.HasField("expiry"))
        self.assertEqual(request.expiry.seconds, 900)

    def test_expiry_drops_fractional_seconds(self):
        self.mcp.create_session_token(
            connection_name="GMAIL", identifier="u1", expiry=timedelta(seconds=90, milliseconds=500)
        )
        request = self._sent_request()
        self.assertEqual(request.expiry.seconds, 90)
        self.assertEqual(request.expiry.nanos, 0)

    def test_connection_forwards_access_levels(self):
        for level in ("READ_ONLY", "FULL"):
            with self.subTest(level=level):
                self.mcp.create_session_token(
                    connection_name="GMAIL", identifier="u1", access_level=level
                )
                self.assertEqual(self._sent_request().access_level, level)

    def test_does_not_validate_access_level_client_side(self):
        # The server is the authority on accepted values; the SDK passes them through.
        self.mcp.create_session_token(
            connection_name="GMAIL", identifier="u1", access_level="read_only"
        )
        self.assertEqual(self._sent_request().access_level, "read_only")

    def test_connection_name_is_keyword_only(self):
        # Five positionals would put connection_name in the slot after access_level.
        with self.assertRaises(TypeError):
            self.mcp.create_session_token(None, "u1", None, None, "GMAIL")
        self.core_client.grpc_exec.assert_not_called()

    # Validation happens before any request, only for the connection form.

    def test_invalid_connection_args_rejected_before_request(self):
        for case, kwargs in INVALID_CONNECTION_ARGS.items():
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    self.mcp.create_session_token(**kwargs)
        self.core_client.grpc_exec.assert_not_called()

    def test_no_target_at_all_rejected_before_request(self):
        with self.assertRaisesRegex(ValueError, "mcp_config_id or connection_name is required"):
            self.mcp.create_session_token(identifier="u1")
        self.core_client.grpc_exec.assert_not_called()

    def test_whitespace_connection_name_goes_to_server(self):
        # Like identifier, only an empty name is rejected locally.
        self.mcp.create_session_token(connection_name=" ", identifier="u1")
        self.assertEqual(self._sent_request().key_id, " ")

    def test_whitespace_identifier_goes_to_server_for_connection(self):
        self.mcp.create_session_token(connection_name="GMAIL", identifier=" ")
        self.assertEqual(self._sent_request().identifier, " ")

    def test_connection_error_messages_name_the_problem(self):
        with self.assertRaisesRegex(ValueError, "not both"):
            self.mcp.create_session_token(
                mcp_config_id="cfg_1", connection_name="GMAIL", identifier="u1"
            )
        with self.assertRaisesRegex(ValueError, "connection_name must not be empty"):
            self.mcp.create_session_token(connection_name="", identifier="u1")
        with self.assertRaisesRegex(ValueError, "identifier is required"):
            self.mcp.create_session_token(connection_name="GMAIL", identifier="")

    def test_config_form_passes_through_as_in_v2_20_0(self):
        # No client-side validation for the config form: the server decides.
        for case, (args, kwargs, config_id, identifier) in MCP_CLIENT_PASS_THROUGH.items():
            with self.subTest(case=case):
                self.core_client.grpc_exec.reset_mock()
                self.mcp.create_session_token(*args, **kwargs)
                self.core_client.grpc_exec.assert_called_once()
                request = self._sent_request()
                self.assertEqual(request.mcp_config_id, config_id)
                self.assertEqual(request.identifier, identifier)
                self.assertEqual(request.key_id, "")

    def test_config_form_server_error_propagates(self):
        self.core_client.grpc_exec.side_effect = _not_found()
        with self.assertRaises(ScalekitNotFoundException):
            self.mcp.create_session_token("", "u1")

    def test_server_error_propagates(self):
        self.core_client.grpc_exec.side_effect = _not_found()
        with self.assertRaises(ScalekitNotFoundException):
            self.mcp.create_session_token(connection_name="missing", identifier="u1")


class TestActionsSessionTokenTargets(unittest.TestCase):
    def setUp(self):
        expires_at = Timestamp(seconds=1_800_000_000)
        self.mcp_client = MagicMock()
        self.mcp_client.create_session_token.return_value = (
            CreateMcpSessionTokenResponse(token="tok", expires_at=expires_at),
            None,
        )
        self.actions = ActionClient(MagicMock(), MagicMock(), mcp_client=self.mcp_client)

    def _forwarded(self):
        call = self.mcp_client.create_session_token.call_args
        self.assertEqual(call.args, ())
        return call.kwargs

    def test_positional_config_back_compat(self):
        self.actions.mcp.create_session_token("cfg_1", "user_123", timedelta(minutes=5), "FULL")
        self.assertEqual(
            self._forwarded(),
            {
                "mcp_config_id": "cfg_1",
                "identifier": "user_123",
                "expiry": timedelta(minutes=5),
                "access_level": "FULL",
            },
        )

    def test_keyword_config_does_not_forward_connection_name(self):
        self.actions.mcp.create_session_token(mcp_config_id="cfg_1", identifier="u1")
        kwargs = self._forwarded()
        self.assertEqual(kwargs["mcp_config_id"], "cfg_1")
        self.assertNotIn("connection_name", kwargs)

    def test_connection_forwards_all_arguments(self):
        self.actions.mcp.create_session_token(
            connection_name="GMAIL",
            identifier="u1",
            expiry=timedelta(hours=2),
            access_level="READ_ONLY",
        )
        self.assertEqual(
            self._forwarded(),
            {
                "connection_name": "GMAIL",
                "identifier": "u1",
                "expiry": timedelta(hours=2),
                "access_level": "READ_ONLY",
            },
        )

    def test_connection_omitted_optionals_forward_none(self):
        self.actions.mcp.create_session_token(connection_name="GMAIL", identifier="u1")
        kwargs = self._forwarded()
        self.assertIsNone(kwargs["expiry"])
        self.assertIsNone(kwargs["access_level"])
        self.assertNotIn("mcp_config_id", kwargs)

    def test_returns_parsed_response(self):
        result = self.actions.mcp.create_session_token(connection_name="GMAIL", identifier="u1")
        self.assertEqual(result.token, "tok")
        self.assertEqual(result.expires_at, Timestamp(seconds=1_800_000_000).ToDatetime())

    def test_invalid_connection_args_rejected_before_call(self):
        for case, kwargs in INVALID_CONNECTION_ARGS.items():
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    self.actions.mcp.create_session_token(**kwargs)
        self.mcp_client.create_session_token.assert_not_called()

    def test_config_form_keeps_v2_20_0_messages(self):
        for case, (kwargs, message) in ACTIONS_CONFIG_ERRORS.items():
            with self.subTest(case=case):
                with self.assertRaises(ValueError) as ctx:
                    self.actions.mcp.create_session_token(**kwargs)
                self.assertEqual(str(ctx.exception), message)
        self.mcp_client.create_session_token.assert_not_called()

    def test_config_form_whitespace_goes_to_server(self):
        # v2.20.0 checked emptiness only; whitespace is the server's to reject.
        self.actions.mcp.create_session_token(mcp_config_id=" ", identifier=" ")
        kwargs = self._forwarded()
        self.assertEqual((kwargs["mcp_config_id"], kwargs["identifier"]), (" ", " "))

    def test_config_form_validates_before_needing_mcp_client(self):
        # As in v2.20.0, the argument check comes before the MCP client lookup.
        actions = ActionClient(MagicMock(), MagicMock(), mcp_client=None)
        with self.assertRaisesRegex(ValueError, "^mcp_config_id is required$"):
            actions.mcp.create_session_token(mcp_config_id="", identifier="u1")

    def test_server_error_propagates(self):
        self.mcp_client.create_session_token.side_effect = _not_found()
        with self.assertRaises(ScalekitNotFoundException):
            self.actions.mcp.create_session_token(connection_name="missing", identifier="u1")


class TestEndToEndThroughBothFacades(unittest.TestCase):
    """The actions facade drives the real McpClient: the wire request is right."""

    def setUp(self):
        self.core_client = MagicMock()
        self.core_client.grpc_exec.return_value = (CreateMcpSessionTokenResponse(token="tok"), None)
        mcp = McpClient.__new__(McpClient)
        mcp.core_client = self.core_client
        mcp.mcp_service = MagicMock()
        self.actions = ActionClient(MagicMock(), MagicMock(), mcp_client=mcp)

    def _sent_request(self):
        return self.core_client.grpc_exec.call_args.args[1]

    def test_connection_token_wire_request(self):
        result = self.actions.mcp.create_session_token(
            connection_name="GMAIL", identifier="u1", access_level="READ_ONLY"
        )
        request = self._sent_request()
        self.assertEqual((request.key_id, request.mcp_config_id), ("GMAIL", ""))
        self.assertEqual(request.access_level, "READ_ONLY")
        self.assertEqual(result.token, "tok")

    def test_config_token_wire_request(self):
        self.actions.mcp.create_session_token("cfg_1", "u1")
        request = self._sent_request()
        self.assertEqual((request.key_id, request.mcp_config_id), ("", "cfg_1"))


if __name__ == "__main__":
    unittest.main()

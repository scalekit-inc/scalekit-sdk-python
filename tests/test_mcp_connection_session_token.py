"""Offline tests: session tokens for a connection's MCP server.

create_connection_session_token targets the connection by name (``key_id`` on the
wire) and never sets ``mcp_config_id``: the server requires exactly one of the two.
"""

import unittest
from datetime import timedelta
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp

from scalekit.actions.actions import ActionClient
from scalekit.common.exceptions import ScalekitNotFoundException
from scalekit.mcp import McpClient
from scalekit.v1.mcp.mcp_pb2 import CreateMcpSessionTokenResponse


class TestMcpClientConnectionSessionToken(unittest.TestCase):
    def setUp(self):
        self.core_client = MagicMock()
        self.core_client.grpc_exec.return_value = (CreateMcpSessionTokenResponse(token="tok"), None)
        self.mcp = McpClient.__new__(McpClient)
        self.mcp.core_client = self.core_client
        self.mcp.mcp_service = MagicMock()

    def _sent_request(self):
        return self.core_client.grpc_exec.call_args.args[1]

    def test_targets_connection_not_config(self):
        self.mcp.create_connection_session_token("GMAIL", "u1")
        request = self._sent_request()
        self.assertEqual(request.key_id, "GMAIL")
        self.assertEqual(request.mcp_config_id, "")
        self.assertEqual(request.identifier, "u1")

    def test_calls_create_mcp_session_token_rpc(self):
        self.mcp.create_connection_session_token("GMAIL", "u1")
        self.assertIs(
            self.core_client.grpc_exec.call_args.args[0],
            self.mcp.mcp_service.CreateMcpSessionToken.with_call,
        )

    def test_returns_grpc_exec_result(self):
        result = self.mcp.create_connection_session_token("GMAIL", "u1")
        self.assertIs(result, self.core_client.grpc_exec.return_value)

    def test_omitted_optionals_stay_unset(self):
        self.mcp.create_connection_session_token("GMAIL", "u1")
        request = self._sent_request()
        self.assertFalse(request.HasField("expiry"))
        self.assertEqual(request.access_level, "")

    def test_forwards_expiry_in_seconds(self):
        self.mcp.create_connection_session_token("GMAIL", "u1", expiry=timedelta(minutes=15))
        request = self._sent_request()
        self.assertTrue(request.HasField("expiry"))
        self.assertEqual(request.expiry.seconds, 900)

    def test_expiry_drops_fractional_seconds(self):
        self.mcp.create_connection_session_token(
            "GMAIL", "u1", expiry=timedelta(seconds=90, milliseconds=500)
        )
        request = self._sent_request()
        self.assertEqual(request.expiry.seconds, 90)
        self.assertEqual(request.expiry.nanos, 0)

    def test_forwards_access_levels(self):
        for level in ("READ_ONLY", "FULL"):
            with self.subTest(level=level):
                self.mcp.create_connection_session_token("GMAIL", "u1", access_level=level)
                self.assertEqual(self._sent_request().access_level, level)

    def test_does_not_validate_access_level_client_side(self):
        # The server is the authority on accepted values; the SDK passes them through.
        self.mcp.create_connection_session_token("GMAIL", "u1", access_level="read_only")
        self.assertEqual(self._sent_request().access_level, "read_only")

    def test_optionals_are_keyword_only(self):
        with self.assertRaises(TypeError):
            self.mcp.create_connection_session_token("GMAIL", "u1", timedelta(hours=1))
        self.core_client.grpc_exec.assert_not_called()

    def test_server_error_propagates(self):
        self.core_client.grpc_exec.side_effect = ScalekitNotFoundException.__new__(
            ScalekitNotFoundException
        )
        with self.assertRaises(ScalekitNotFoundException):
            self.mcp.create_connection_session_token("missing", "u1")

    def test_config_token_still_targets_config(self):
        self.mcp.create_session_token(
            mcp_config_id="cfg_1", identifier="u1", expiry=timedelta(minutes=5)
        )
        request = self._sent_request()
        self.assertEqual(request.mcp_config_id, "cfg_1")
        self.assertEqual(request.key_id, "")
        self.assertEqual(request.expiry.seconds, 300)


class TestActionsConnectionSessionToken(unittest.TestCase):
    def setUp(self):
        expires_at = Timestamp(seconds=1_800_000_000)
        self.mcp_client = MagicMock()
        self.mcp_client.create_connection_session_token.return_value = (
            CreateMcpSessionTokenResponse(token="tok", expires_at=expires_at),
            None,
        )
        self.actions = ActionClient(MagicMock(), MagicMock(), mcp_client=self.mcp_client)

    def test_forwards_all_arguments(self):
        self.actions.mcp.create_connection_session_token(
            "GMAIL", "u1", expiry=timedelta(hours=2), access_level="READ_ONLY"
        )
        call = self.mcp_client.create_connection_session_token.call_args
        self.assertEqual(call.args, ("GMAIL", "u1"))
        self.assertEqual(call.kwargs, {"expiry": timedelta(hours=2), "access_level": "READ_ONLY"})
        self.mcp_client.create_session_token.assert_not_called()

    def test_omitted_optionals_forward_none(self):
        self.actions.mcp.create_connection_session_token(connection_name="GMAIL", identifier="u1")
        call = self.mcp_client.create_connection_session_token.call_args
        self.assertIsNone(call.kwargs["expiry"])
        self.assertIsNone(call.kwargs["access_level"])

    def test_returns_parsed_response(self):
        result = self.actions.mcp.create_connection_session_token("GMAIL", "u1")
        self.assertEqual(result.token, "tok")
        self.assertEqual(result.expires_at, Timestamp(seconds=1_800_000_000).ToDatetime())

    def test_blank_connection_name_rejected_before_call(self):
        with self.assertRaises(ValueError):
            self.actions.mcp.create_connection_session_token("", "u1")
        self.mcp_client.create_connection_session_token.assert_not_called()

    def test_blank_identifier_rejected_before_call(self):
        with self.assertRaises(ValueError):
            self.actions.mcp.create_connection_session_token("GMAIL", "")
        self.mcp_client.create_connection_session_token.assert_not_called()

    def test_server_error_propagates(self):
        self.mcp_client.create_connection_session_token.side_effect = (
            ScalekitNotFoundException.__new__(ScalekitNotFoundException)
        )
        with self.assertRaises(ScalekitNotFoundException):
            self.actions.mcp.create_connection_session_token("missing", "u1")


if __name__ == "__main__":
    unittest.main()

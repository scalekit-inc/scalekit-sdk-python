"""Offline tests: create_session_token sends access_level only when the caller sets it.

An omitted access level leaves the field empty on the wire, which the server treats
as full access, so existing callers keep every tool.
"""

import unittest
from datetime import timedelta
from unittest.mock import MagicMock

from scalekit.actions.actions import ActionClient
from scalekit.mcp import McpClient
from scalekit.v1.mcp.mcp_pb2 import CreateMcpSessionTokenResponse


class TestMcpClientSessionTokenAccessLevel(unittest.TestCase):
    def setUp(self):
        self.core_client = MagicMock()
        self.core_client.grpc_exec.return_value = (CreateMcpSessionTokenResponse(token="tok"), None)
        self.mcp = McpClient.__new__(McpClient)
        self.mcp.core_client = self.core_client
        self.mcp.mcp_service = MagicMock()

    def _sent_request(self):
        return self.core_client.grpc_exec.call_args.args[1]

    def test_omitted_access_level_stays_empty(self):
        self.mcp.create_session_token(mcp_config_id="cfg_1", identifier="u1")
        request = self._sent_request()
        self.assertEqual(request.access_level, "")
        self.assertEqual(request.mcp_config_id, "cfg_1")
        self.assertEqual(request.identifier, "u1")

    def test_sends_read_only(self):
        self.mcp.create_session_token(mcp_config_id="cfg_1", identifier="u1", access_level="READ_ONLY")
        self.assertEqual(self._sent_request().access_level, "READ_ONLY")

    def test_sends_full(self):
        self.mcp.create_session_token(mcp_config_id="cfg_1", identifier="u1", access_level="FULL")
        self.assertEqual(self._sent_request().access_level, "FULL")

    def test_sends_access_level_with_expiry(self):
        self.mcp.create_session_token(
            mcp_config_id="cfg_1",
            identifier="u1",
            expiry=timedelta(minutes=15),
            access_level="READ_ONLY",
        )
        request = self._sent_request()
        self.assertEqual(request.access_level, "READ_ONLY")
        self.assertEqual(request.expiry.seconds, 900)


class TestActionsSessionTokenAccessLevel(unittest.TestCase):
    def setUp(self):
        self.mcp_client = MagicMock()
        self.mcp_client.create_session_token.return_value = (CreateMcpSessionTokenResponse(token="tok"), None)
        self.actions = ActionClient(MagicMock(), MagicMock(), mcp_client=self.mcp_client)

    def test_forwards_access_level(self):
        result = self.actions.mcp.create_session_token(
            mcp_config_id="cfg_1", identifier="u1", access_level="READ_ONLY"
        )
        kwargs = self.mcp_client.create_session_token.call_args.kwargs
        self.assertEqual(kwargs["access_level"], "READ_ONLY")
        self.assertEqual(result.token, "tok")

    def test_omitted_access_level_forwards_none(self):
        self.actions.mcp.create_session_token(mcp_config_id="cfg_1", identifier="u1")
        kwargs = self.mcp_client.create_session_token.call_args.kwargs
        self.assertIsNone(kwargs["access_level"])


if __name__ == "__main__":
    unittest.main()

"""Offline tests for get_config on McpClient, ActionMcp and ActionClient.

No credentials and no network: the ``McpClient`` test runs the real
``CoreClient.grpc_exec`` against a mocked gRPC stub method, and the action-layer
tests mock ``McpClient`` itself.
"""

import unittest
from unittest.mock import MagicMock

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import GetMcpConfigResponse
from scalekit.core import DEFAULT_CALL_TIMEOUT_S, DEFAULT_TOOL_CALL_TIMEOUT_S
from scalekit.mcp import McpClient
from scalekit.v1.mcp import mcp_pb2 as pb

try:  # `make test` / `unittest discover -s tests` puts tests/ on sys.path
    from test_sk819_retry_behavior import _make_core_client
except ModuleNotFoundError:  # `python -m unittest tests.<module>` from the repo root
    from tests.test_sk819_retry_behavior import _make_core_client

BLANK_CONFIG_IDS = ["", None]


def _mcp_client():
    """An McpClient wired to a real CoreClient and a mocked gRPC stub."""
    client = McpClient.__new__(McpClient)
    client.core_client = _make_core_client()
    client.mcp_service = MagicMock()
    return client


def _config_proto():
    return pb.GetMcpConfigResponse(
        config=pb.McpConfig(
            id="cfg_123",
            name="meeting-manager",
            description="Summarises email and creates calendar events",
            mcp_server_url="https://mcp.example.com/sse",
            connection_tool_mappings=[
                pb.McpConfigConnectionToolMapping(
                    connection_name="MY_CALENDAR",
                    tools=["googlecalendar_create_event"],
                )
            ],
        )
    )


class TestMcpClientGetConfig(unittest.TestCase):
    """McpClient.get_config: request mapping, deadline, return shape."""

    def setUp(self):
        self.client = _mcp_client()
        self.rpc = self.client.mcp_service.GetMcpConfig.with_call
        self.rpc.return_value = (_config_proto(), None)

    def test_sets_config_id_on_the_request(self):
        self.client.get_config("cfg_123")
        request = self.rpc.call_args.args[0]
        self.assertIsInstance(request, pb.GetMcpConfigRequest)
        self.assertEqual(request.config_id, "cfg_123")
        self.assertEqual([field.name for field, _ in request.ListFields()], ["config_id"])

    def test_passes_no_explicit_timeout_so_the_control_plane_default_applies(self):
        """Fetching a config does not proxy a third-party API, so it keeps the
        default control-plane deadline rather than the longer tool deadline."""
        self.client.get_config("cfg_123")
        self.assertEqual(self.rpc.call_args.kwargs["timeout"], DEFAULT_CALL_TIMEOUT_S)
        self.assertNotEqual(DEFAULT_CALL_TIMEOUT_S, DEFAULT_TOOL_CALL_TIMEOUT_S)

    def test_returns_the_response_and_call_tuple_unchanged(self):
        sentinel_call = object()
        response = _config_proto()
        self.rpc.return_value = (response, sentinel_call)
        result = self.client.get_config("cfg_123")
        self.assertIs(result[0], response)
        self.assertIs(result[1], sentinel_call)


class TestActionMcpGetConfig(unittest.TestCase):
    """ActionMcp.get_config: validation, forwarding, mapping."""

    def setUp(self):
        self.mcp = MagicMock()
        self.mcp.get_config.return_value = (_config_proto(), None)
        self.actions = ActionClient(MagicMock(), MagicMock(), mcp_client=self.mcp)

    def test_forwards_config_id(self):
        self.actions.mcp.get_config("cfg_123")
        self.mcp.get_config.assert_called_once_with(config_id="cfg_123")

    def test_blank_config_id_raises_before_any_call(self):
        for config_id in BLANK_CONFIG_IDS:
            with (
                self.subTest(config_id=config_id),
                self.assertRaisesRegex(ValueError, "config_id is required"),
            ):
                self.actions.mcp.get_config(config_id)
        self.mcp.get_config.assert_not_called()

    def test_missing_mcp_client_raises_before_any_call(self):
        actions = ActionClient(MagicMock(), MagicMock())
        with self.assertRaisesRegex(ValueError, "MCP client not initialized"):
            actions.mcp.get_config("cfg_123")

    def test_maps_response(self):
        result = self.actions.mcp.get_config("cfg_123")
        self.assertIsInstance(result, GetMcpConfigResponse)
        self.assertEqual(result.config.id, "cfg_123")
        self.assertEqual(result.config.name, "meeting-manager")
        self.assertEqual(result.config.mcp_server_url, "https://mcp.example.com/sse")
        self.assertEqual(
            [mapping.connection_name for mapping in result.config.connection_tool_mappings],
            ["MY_CALENDAR"],
        )
        self.assertEqual(
            result.config.connection_tool_mappings[0].tools, ["googlecalendar_create_event"]
        )

    def test_absent_config_maps_to_none(self):
        """An unset singular message field reads as a truthy default instance in
        protobuf for Python, so presence must come from HasField."""
        self.mcp.get_config.return_value = (pb.GetMcpConfigResponse(), None)
        result = self.actions.mcp.get_config("cfg_123")
        self.assertIsNone(result.config)
        self.assertIsNone(result.to_dict()["config"])

    def test_to_dict(self):
        result = self.actions.mcp.get_config("cfg_123").to_dict()
        self.assertEqual(set(result), {"config"})
        self.assertEqual(result["config"]["name"], "meeting-manager")
        self.assertEqual(result["config"]["mcp_server_url"], "https://mcp.example.com/sse")

    def test_empty_mappings_map_to_empty_list(self):
        self.mcp.get_config.return_value = (
            pb.GetMcpConfigResponse(config=pb.McpConfig(id="cfg_456", name="bare")),
            None,
        )
        result = self.actions.mcp.get_config("cfg_456")
        self.assertEqual(result.config.connection_tool_mappings, [])
        self.assertIsNone(result.config.description)
        self.assertIsNone(result.config.mcp_server_url)


class TestActionClientGetConfigPassthrough(unittest.TestCase):
    """ActionClient.get_config delegates to ActionMcp.get_config."""

    def setUp(self):
        self.mcp = MagicMock()
        self.mcp.get_config.return_value = (_config_proto(), None)
        self.actions = ActionClient(MagicMock(), MagicMock(), mcp_client=self.mcp)

    def test_forwards_config_id_and_returns_the_model(self):
        result = self.actions.get_config("cfg_123")
        self.mcp.get_config.assert_called_once_with(config_id="cfg_123")
        self.assertIsInstance(result, GetMcpConfigResponse)
        self.assertEqual(result.config.id, "cfg_123")

    def test_blank_config_id_raises_before_any_call(self):
        with self.assertRaisesRegex(ValueError, "config_id is required"):
            self.actions.get_config("")
        self.mcp.get_config.assert_not_called()

    def test_missing_mcp_client_raises_before_any_call(self):
        actions = ActionClient(MagicMock(), MagicMock())
        with self.assertRaisesRegex(ValueError, "MCP client not initialized"):
            actions.get_config("cfg_123")


if __name__ == "__main__":
    unittest.main()

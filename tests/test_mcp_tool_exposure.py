import unittest

from scalekit.actions.models.mcp_config import McpConfig, tool_exposure_to_proto
from scalekit.v1.mcp.mcp_pb2 import ToolExposure


class TestMcpConfigToolExposure(unittest.TestCase):
    """Offline tests for the vMCP tool_exposure field (no environment needed)."""

    def test_unset_is_not_sent(self):
        proto = McpConfig.to_proto_static(name="cfg")
        self.assertFalse(proto.HasField("tool_exposure"))
        self.assertIsNone(McpConfig.from_proto(proto).tool_exposure)

    def test_meta_round_trip(self):
        proto = McpConfig.to_proto_static(name="cfg", tool_exposure="META")
        self.assertEqual(proto.tool_exposure, ToolExposure.META)
        self.assertEqual(McpConfig.from_proto(proto).tool_exposure, "META")

    def test_case_insensitive_and_trimmed(self):
        self.assertEqual(tool_exposure_to_proto(" direct "), ToolExposure.DIRECT)

    def test_invalid_value_raises(self):
        with self.assertRaises(ValueError):
            McpConfig.to_proto_static(name="cfg", tool_exposure="ALL")

    def test_model_to_proto_and_dict(self):
        config = McpConfig(name="cfg", tool_exposure="META")
        self.assertEqual(config.to_proto().tool_exposure, ToolExposure.META)
        self.assertEqual(config.to_dict()["tool_exposure"], "META")


if __name__ == "__main__":
    unittest.main()

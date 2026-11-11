"""Offline tests for the tool methods that serve custom connectors: the gRPC layer is stubbed."""
import unittest
from unittest.mock import MagicMock

from scalekit.actions.actions import ActionClient
from scalekit.common.exceptions import ScalekitNotFoundException
from scalekit.tools import ToolsClient
from scalekit.v1.tools import tools_pb2 as pb


def _server_error(cls, message, code):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


def _tool(name: str, provider: str = "PETSTORE:12") -> pb.Tool:
    return pb.Tool(id="tol_" + name, provider=provider)


class ToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.core = MagicMock()
        self.calls = []
        self.tools = ToolsClient(self.core)

    def _reply(self, *responses):
        queue = list(responses)

        def grpc_exec(rpc, request, **kwargs):
            self.calls.append((rpc, request, kwargs))
            item = queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return (item, None)

        self.core.grpc_exec.side_effect = grpc_exec


class ListToolsForCustomConnectorsTest(ToolsTestCase):
    def setUp(self):
        super().setUp()
        self.client = ActionClient(self.tools, MagicMock())

    def test_a_connector_is_listed_by_its_identifier(self):
        self._reply(
            pb.ListToolsResponse(
                tool_names=["a-petstore_listpets", "a-petstore_getpet"], tools=[_tool("1"), _tool("2")], total_size=2
            )
        )
        response = self.client.list_tools(provider="PETSTORE:12", summary=False)
        request = self.calls[0][1]
        self.assertEqual(request.filter.provider, "PETSTORE:12")
        self.assertEqual(response.tool_names, ["a-petstore_listpets", "a-petstore_getpet"])
        self.assertEqual(response.total_count, 2)

    def test_a_custom_mcp_connectors_tools_need_the_account(self):
        self._reply(pb.ListToolsResponse(tool_names=["c-acme_search"]))
        self.client.list_tools(connection_name="acme-mcp", identifier="user@example.com")
        filter_ = self.calls[0][1].filter
        self.assertEqual((filter_.connector, filter_.identifier), ("acme-mcp", "user@example.com"))

    def test_page_size_is_sent_as_given_and_left_to_the_server_when_omitted(self):
        self._reply(pb.ListToolsResponse(), pb.ListToolsResponse(), pb.ListToolsResponse())
        self.client.list_tools(provider="PETSTORE:12", page_size=1000)
        self.client.list_tools(provider="PETSTORE:12", page_size=5000)  # the server lowers it to 1000
        self.client.list_tools(provider="PETSTORE:12")  # the server uses 300
        self.assertEqual([c[1].page_size for c in self.calls], [1000, 5000, 0])

    def test_a_connected_account_that_matches_nothing_is_a_404(self):
        self._reply(_server_error(ScalekitNotFoundException, "connected account not found", "NOT_FOUND"))
        with self.assertRaises(ScalekitNotFoundException):
            self.client.list_tools(connection_name="acme-mcp", identifier="nobody@example.com")


if __name__ == "__main__":
    unittest.main()

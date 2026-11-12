"""
client.actions.list_scoped_tools / list_available_tools / search_tools, and
client.tools.list_available_tools.

The actions methods take plain keyword arguments and return typed models (like
actions.list_tools). The list methods ask for definitions as JSON text and restore
them (SK-3047), so a deeply nested definition no longer breaks the page.

These tests never touch the network: grpc_exec is replaced by a stub.
"""
import json
import unittest
from unittest.mock import MagicMock

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import (
    ConnectionReadiness, ListAvailableToolsResponse, ListScopedToolsResponse, ScopedTool,
    SearchedTool, SearchToolsResponse, Tool,
)
from scalekit.tools import ToolsClient
from scalekit.v1.tools import tools_pb2

DEFINITION = {"name": "gmail_send", "input_schema": {"type": "object", "properties": {"to": {"type": "string"}}}}


def deep_definition(depth):
    value = {"leaf": "x"}
    for _ in range(depth - 2):
        value = {"k": value}
    return {"name": "deep_tool", "input_schema": value}


def json_tool(tool_id, definition, provider="GMAIL"):
    return tools_pb2.Tool(id=tool_id, provider=provider, definition_json=json.dumps(definition))


def make(response):
    """ActionClient over a real ToolsClient whose grpc_exec returns (response, call)."""
    core = MagicMock()
    core.tool_call_timeout_s = 60
    core.grpc_exec.return_value = (response, MagicMock())
    tools = ToolsClient.__new__(ToolsClient)
    tools.core_client = core
    tools.tool_service = MagicMock()
    return ActionClient(tools, MagicMock()), tools, core


def sent(core):
    return core.grpc_exec.call_args[0][1]


class TestToolsListAvailableTools(unittest.TestCase):
    def test_requests_json_string_and_restores_definitions(self):
        _, tools, core = make(tools_pb2.ListAvailableToolsResponse(tools=[json_tool("tol_1", DEFINITION)], total_size=1))
        resp, _call = tools.list_available_tools("user_1", page_size=50, page_token="tok")

        req = sent(core)
        self.assertIsInstance(req, tools_pb2.ListAvailableToolsRequest)
        self.assertEqual((req.identifier, req.page_size, req.page_token), ("user_1", 50, "tok"))
        self.assertEqual(req.definition_format, tools_pb2.DEFINITION_FORMAT_JSON_STRING)
        self.assertFalse(resp.tools[0].HasField("definition_json"))
        self.assertEqual(resp.tools[0].definition["name"], "gmail_send")

    def test_deep_definition_decodes(self):
        deep = deep_definition(60)
        _, tools, _ = make(tools_pb2.ListAvailableToolsResponse(tools=[json_tool("tol_deep", deep)]))
        resp, _ = tools.list_available_tools("user_1")
        self.assertEqual(resp.tools[0].definition["name"], "deep_tool")


class TestActionsListScopedTools(unittest.TestCase):
    def response(self):
        return tools_pb2.ListScopedToolsResponse(
            tools=[tools_pb2.ScopedTool(tool=json_tool("tol_1", DEFINITION), identifier="user_1",
                                        connected_account_id="ca_1")],
            total_size=7, next_page_token="next", prev_page_token="prev",
        )

    def test_maps_keyword_arguments_to_the_request(self):
        actions, _, core = make(self.response())
        actions.list_scoped_tools("user_1", providers=["GMAIL"], tool_names=["gmail_send"],
                                  connection_names=["gmail-ab12"], page_size=10, page_token="tok")
        req = sent(core)
        self.assertIsInstance(req, tools_pb2.ListScopedToolsRequest)
        self.assertEqual(req.identifier, "user_1")
        self.assertEqual(list(req.filter.providers), ["GMAIL"])
        self.assertEqual(list(req.filter.tool_names), ["gmail_send"])
        self.assertEqual(list(req.filter.connection_names), ["gmail-ab12"])
        self.assertEqual((req.page_size, req.page_token), (10, "tok"))
        self.assertEqual(req.definition_format, tools_pb2.DEFINITION_FORMAT_JSON_STRING)

    def test_no_filter_arguments_send_an_empty_filter(self):
        actions, _, core = make(self.response())
        actions.list_scoped_tools("user_1")
        req = sent(core)
        self.assertTrue(req.HasField("filter"))
        self.assertEqual(req.filter, tools_pb2.ScopedToolFilter())

    def test_returns_typed_model(self):
        actions, _, _ = make(self.response())
        resp = actions.list_scoped_tools("user_1", providers=["GMAIL"])
        self.assertIsInstance(resp, ListScopedToolsResponse)
        self.assertIsInstance(resp.tools[0], ScopedTool)
        self.assertIsInstance(resp.tools[0].tool, Tool)
        self.assertEqual(resp.tools[0].tool.definition, DEFINITION)
        self.assertEqual((resp.tools[0].identifier, resp.tools[0].connected_account_id), ("user_1", "ca_1"))
        self.assertEqual((resp.total_count, resp.next_page_token, resp.previous_page_token), (7, "next", "prev"))

    def test_last_page_has_no_next_token(self):
        actions, _, _ = make(tools_pb2.ListScopedToolsResponse())
        resp = actions.list_scoped_tools("user_1")
        self.assertEqual((resp.tools, resp.next_page_token), ([], None))

    def test_deep_definition_decodes(self):
        deep = deep_definition(60)
        actions, _, _ = make(tools_pb2.ListScopedToolsResponse(
            tools=[tools_pb2.ScopedTool(tool=json_tool("tol_deep", deep))]))
        self.assertEqual(actions.list_scoped_tools("user_1").tools[0].tool.definition, deep)

    def test_identifier_required(self):
        actions, _, core = make(self.response())
        with self.assertRaises(ValueError):
            actions.list_scoped_tools("")
        core.grpc_exec.assert_not_called()


class TestActionsListAvailableTools(unittest.TestCase):
    def test_maps_arguments_and_returns_typed_model(self):
        actions, _, core = make(tools_pb2.ListAvailableToolsResponse(
            tools=[json_tool("tol_1", DEFINITION)], total_size=3, next_page_token="next"))
        resp = actions.list_available_tools("user_1", page_size=99, page_token="tok")

        req = sent(core)
        self.assertIsInstance(req, tools_pb2.ListAvailableToolsRequest)
        self.assertEqual((req.identifier, req.page_size, req.page_token), ("user_1", 99, "tok"))
        self.assertEqual(req.definition_format, tools_pb2.DEFINITION_FORMAT_JSON_STRING)
        self.assertIsInstance(resp, ListAvailableToolsResponse)
        self.assertIsInstance(resp.tools[0], Tool)
        self.assertEqual(resp.tools[0].definition, DEFINITION)
        self.assertEqual((resp.total_count, resp.next_page_token, resp.previous_page_token), (3, "next", None))

    def test_deep_definition_decodes(self):
        deep = deep_definition(60)
        actions, _, _ = make(tools_pb2.ListAvailableToolsResponse(tools=[json_tool("tol_deep", deep)]))
        self.assertEqual(actions.list_available_tools("user_1").tools[0].definition, deep)

    def test_identifier_required(self):
        actions, _, core = make(tools_pb2.ListAvailableToolsResponse())
        with self.assertRaises(ValueError):
            actions.list_available_tools("")
        core.grpc_exec.assert_not_called()


class TestActionsSearchTools(unittest.TestCase):
    def response(self):
        return tools_pb2.SearchToolsResponse(tools=[
            tools_pb2.SearchedTool(
                name="gmail_send_email", provider="GMAIL", description="Send an email", score=0.92,
                connections=[
                    tools_pb2.ConnectionReadiness(connection_name="gmail-ab12", connected_account_id="ca_1",
                                                  readiness_state=tools_pb2.TOOL_READINESS_STATE_READY),
                    tools_pb2.ConnectionReadiness(connection_name="gmail-cd34", connected_account_id="ca_2",
                                                  readiness_state=tools_pb2.TOOL_READINESS_STATE_NEEDS_REAUTH),
                ]),
            tools_pb2.SearchedTool(name="outlook_send_email", provider="OUTLOOK", score=0.5),
        ])

    def test_maps_arguments(self):
        actions, _, core = make(self.response())
        actions.search_tools("send an email", identifier="user_1", top_k=5)
        req = sent(core)
        self.assertIsInstance(req, tools_pb2.SearchToolsRequest)
        self.assertEqual((req.query, req.identifier, req.top_k), ("send an email", "user_1", 5))

    def test_returns_typed_model_with_readiness_names(self):
        actions, _, _ = make(self.response())
        resp = actions.search_tools("send an email", identifier="user_1")
        self.assertIsInstance(resp, SearchToolsResponse)
        first, second = resp.tools
        self.assertIsInstance(first, SearchedTool)
        self.assertEqual((first.name, first.provider, first.description), ("gmail_send_email", "GMAIL", "Send an email"))
        self.assertAlmostEqual(first.score, 0.92, places=5)
        self.assertIsInstance(first.connections[0], ConnectionReadiness)
        self.assertEqual([(c.connection_name, c.connected_account_id, c.readiness_state) for c in first.connections],
                         [("gmail-ab12", "ca_1", "READY"), ("gmail-cd34", "ca_2", "NEEDS_REAUTH")])
        self.assertEqual(second.connections, [])

    def test_unknown_readiness_value_is_kept(self):
        resp = tools_pb2.SearchToolsResponse(tools=[tools_pb2.SearchedTool(
            name="t", connections=[tools_pb2.ConnectionReadiness(readiness_state=99)])])
        actions, _, _ = make(resp)
        self.assertEqual(actions.search_tools("x").tools[0].connections[0].readiness_state, "99")

    def test_query_required(self):
        actions, _, core = make(self.response())
        with self.assertRaises(ValueError):
            actions.search_tools("")
        core.grpc_exec.assert_not_called()

    def test_to_dict(self):
        actions, _, _ = make(self.response())
        d = actions.search_tools("send an email").to_dict()
        self.assertEqual(d["tools"][0]["connections"][0]["readiness_state"], "READY")
        self.assertEqual(d["tools"][1]["connections"], [])


if __name__ == "__main__":
    unittest.main()

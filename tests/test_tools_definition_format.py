"""
SK-3047: list RPCs ask for each tool definition as JSON text.

As a google.protobuf.Struct, a definition nested 34+ JSON levels deep exceeds
Python protobuf's (upb) 100-level decode limit, and the whole list page fails
with "Exception deserializing response!". The SDK sends
definition_format=JSON_STRING and rebuilds `definition` from
`definition_json`, so callers get the same Tool as before.

These tests never touch the network: grpc_exec is replaced by a stub.
"""
import copy
import json
import unittest
from unittest.mock import MagicMock

from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToDict

from scalekit.actions.types import ListToolsResponse as ActionsListToolsResponse
from scalekit.common.exceptions import ScalekitException
from scalekit.tools import ToolsClient
from scalekit.v1.tools import tools_pb2

DEFINITION = {
    "name": "gmail_send",
    "input_schema": {"type": "object", "properties": {"to": {"type": "string"}}},
}


def _deep_definition(depth):
    value = {"leaf": "x"}
    for _ in range(depth - 2):
        value = {"k": value}
    return {"name": "deep_tool", "input_schema": value}


def _json_tool(tool_id, definition):
    return tools_pb2.Tool(id=tool_id, provider="GMAIL", definition_json=json.dumps(definition))


def _struct_tool(tool_id, definition):
    tool = tools_pb2.Tool(id=tool_id, provider="GMAIL")
    tool.definition.update(definition)
    return tool


def _client(response):
    """A ToolsClient whose grpc_exec returns (response, call) like with_call."""
    core = MagicMock()
    core.tool_call_timeout_s = 60
    core.grpc_exec.return_value = (response, MagicMock())
    client = ToolsClient.__new__(ToolsClient)
    client.core_client = core
    client.tool_service = MagicMock()
    return client, core


def _sent_request(core):
    return core.grpc_exec.call_args[0][1]


class TestListToolsDefinitionFormat(unittest.TestCase):
    def test_requests_json_string_and_restores_definition(self):
        client, core = _client(tools_pb2.ListToolsResponse(tools=[_json_tool("tol_1", DEFINITION)], total_size=1))

        response, _call = client.list_tools(page_size=5)

        request = _sent_request(core)
        self.assertEqual(request.definition_format, tools_pb2.DEFINITION_FORMAT_JSON_STRING)
        self.assertEqual(request.page_size, 5)
        tool = response.tools[0]
        self.assertEqual(MessageToDict(tool.definition), DEFINITION)
        self.assertFalse(tool.HasField("definition_json"))
        self.assertEqual(response.total_size, 1)

    def test_struct_from_older_server_is_untouched(self):
        client, _ = _client(tools_pb2.ListToolsResponse(tools=[_struct_tool("tol_1", DEFINITION)]))

        response, _ = client.list_tools()

        self.assertEqual(MessageToDict(response.tools[0].definition), DEFINITION)
        self.assertFalse(response.tools[0].HasField("definition_json"))

    def test_result_equals_a_struct_response(self):
        from_json, _ = _client(tools_pb2.ListToolsResponse(tools=[_json_tool("tol_1", DEFINITION)]))[0].list_tools()
        from_struct, _ = _client(tools_pb2.ListToolsResponse(tools=[_struct_tool("tol_1", DEFINITION)]))[0].list_tools()

        self.assertEqual(from_json, from_struct)

    def test_returns_the_grpc_exec_tuple(self):
        client, core = _client(tools_pb2.ListToolsResponse())

        result = client.list_tools()

        self.assertIs(result, core.grpc_exec.return_value)

    def test_deep_definition_page_decodes(self):
        deep = _deep_definition(60)
        struct_page = tools_pb2.ListToolsResponse()
        struct_page.tools.add(id="tol_1").definition.update(deep)  # built in place: copying would re-parse
        # The bug. upb says "MaxDepth"; the pure-Python backend says "too many levels of nesting".
        with self.assertRaises(Exception):
            tools_pb2.ListToolsResponse.FromString(struct_page.SerializeToString())

        as_string = tools_pb2.ListToolsResponse(tools=[_json_tool("tol_1", deep)]).SerializeToString()
        client, _ = _client(tools_pb2.ListToolsResponse.FromString(as_string))

        response, _ = client.list_tools()

        self.assertEqual(MessageToDict(response.tools[0].definition), deep)

    def test_deep_definition_supports_read_and_copy_operations(self):
        deep = _deep_definition(60)
        page = tools_pb2.ListToolsResponse(tools=[_json_tool("tol_1", deep)])
        client, _ = _client(tools_pb2.ListToolsResponse.FromString(page.SerializeToString()))

        response, _ = client.list_tools()
        tool = response.tools[0]

        self.assertEqual(MessageToDict(copy.deepcopy(tool).definition), deep)
        copied = tools_pb2.Tool()
        copied.CopyFrom(tool)
        self.assertEqual(copied, tool)
        self.assertEqual(ActionsListToolsResponse.from_proto(response).tools[0].definition, deep)

    def test_invalid_definition_names_the_tool(self):
        bad = tools_pb2.Tool(id="tol_bad", definition_json="{not json")
        client, _ = _client(tools_pb2.ListToolsResponse(tools=[bad]))

        with self.assertRaisesRegex(ScalekitException, "tol_bad"):
            client.list_tools()

    def test_non_object_definition_names_the_tool(self):
        for text in ("[1, 2]", '"x"', "3", "null", "NaN"):
            with self.subTest(text=text):
                bad = tools_pb2.Tool(id="tol_bad", definition_json=text)
                client, _ = _client(tools_pb2.ListToolsResponse(tools=[bad]))

                with self.assertRaisesRegex(ScalekitException, "tol_bad"):
                    client.list_tools()

    def test_actions_model_is_unchanged(self):
        from_json, _ = _client(tools_pb2.ListToolsResponse(tools=[_json_tool("tol_1", DEFINITION)]))[0].list_tools()
        from_struct, _ = _client(tools_pb2.ListToolsResponse(tools=[_struct_tool("tol_1", DEFINITION)]))[0].list_tools()

        self.assertEqual(
            ActionsListToolsResponse.from_proto(from_json).model_dump(),
            ActionsListToolsResponse.from_proto(from_struct).model_dump(),
        )


class TestListScopedToolsDefinitionFormat(unittest.TestCase):
    def test_requests_json_string_and_restores_each_tool(self):
        response = tools_pb2.ListScopedToolsResponse(tools=[
            tools_pb2.ScopedTool(tool=_json_tool("tol_1", DEFINITION), identifier="user_1"),
            tools_pb2.ScopedTool(identifier="user_2"),
        ])
        client, core = _client(response)

        result, _ = client.list_scoped_tools("user_1", tools_pb2.ScopedToolFilter(providers=["GMAIL"]))

        self.assertEqual(_sent_request(core).definition_format, tools_pb2.DEFINITION_FORMAT_JSON_STRING)
        self.assertEqual(MessageToDict(result.tools[0].tool.definition), DEFINITION)
        self.assertFalse(result.tools[0].tool.HasField("definition_json"))
        self.assertFalse(result.tools[1].HasField("tool"))


if __name__ == "__main__":
    unittest.main()

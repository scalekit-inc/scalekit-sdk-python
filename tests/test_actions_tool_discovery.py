"""Offline tests for the tool-discovery methods added for the AgentKit reference.

No credentials and no network: the ``ActionClient`` tests mock ``ToolsClient``,
and the ``ToolsClient`` test runs the real ``CoreClient.grpc_exec`` against a
mocked gRPC stub method so the request message and the deadline it is sent with
are both observable.

Covers ``tools.list_available_tools``, ``actions.list_available_tools``,
``actions.list_scoped_tools`` and ``actions.search_tools``.
"""

import unittest
from unittest.mock import MagicMock

from google.protobuf import struct_pb2

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import (
    ConnectionReadiness,
    ListAvailableToolsResponse,
    ListScopedToolsResponse,
    SearchToolsResponse,
)
from scalekit.core import DEFAULT_CALL_TIMEOUT_S, DEFAULT_TOOL_CALL_TIMEOUT_S
from scalekit.tools import ToolsClient
from scalekit.v1.tools import tools_pb2 as pb

try:  # `make test` / `unittest discover -s tests` puts tests/ on sys.path
    from test_sk819_retry_behavior import _make_core_client
except ModuleNotFoundError:  # `python -m unittest tests.<module>` from the repo root
    from tests.test_sk819_retry_behavior import _make_core_client

# A readiness value the vendored stubs do not know, standing in for a state the
# backend ships before the SDK is regenerated.
UNKNOWN_READINESS_VALUE = 99


def _tools_client():
    """A ToolsClient wired to a real CoreClient and a mocked gRPC stub."""
    client = ToolsClient.__new__(ToolsClient)
    client.core_client = _make_core_client()
    client.tool_service = MagicMock()
    return client


def _definition(name):
    """A tool definition Struct, as the server sends it."""
    definition = struct_pb2.Struct()
    definition.update({"name": name})
    return definition


def _available_page():
    return pb.ListAvailableToolsResponse(
        tools=[
            pb.Tool(id="tool_1", provider="slack", definition=_definition("slack_post_message")),
            pb.Tool(id="tool_2", provider="gmail"),
        ],
        total_size=7,
        next_page_token="next-2",
        prev_page_token="prev-0",
    )


def _scoped_page():
    return pb.ListScopedToolsResponse(
        tools=[
            pb.ScopedTool(
                tool=pb.Tool(id="tool_1", provider="slack"),
                identifier="user@example.com",
                connected_account_id="ca_111",
            ),
            pb.ScopedTool(identifier="user@example.com"),
        ],
        total_size=2,
        next_page_token="next-2",
        prev_page_token="prev-0",
    )


def _search_results():
    return pb.SearchToolsResponse(
        tools=[
            pb.SearchedTool(
                name="slack_post_message",
                provider="slack",
                description="Post a message to a Slack channel",
                score=0.93,
                connections=[
                    pb.ConnectionReadiness(
                        connection_name="slack-prod",
                        connected_account_id="ca_111",
                        readiness_state=pb.TOOL_READINESS_STATE_READY,
                    ),
                    pb.ConnectionReadiness(
                        connection_name="slack-staging",
                        connected_account_id="ca_222",
                        readiness_state=pb.TOOL_READINESS_STATE_NEEDS_REAUTH,
                    ),
                ],
            ),
            pb.SearchedTool(name="gmail_send_email", provider="gmail", score=0.41),
        ]
    )


class TestToolsListAvailableTools(unittest.TestCase):
    """ToolsClient.list_available_tools: request mapping, deadline, return shape."""

    def setUp(self):
        self.client = _tools_client()
        self.rpc = self.client.tool_service.ListAvailableTools.with_call
        self.rpc.return_value = (_available_page(), None)

    def _request(self):
        return self.rpc.call_args.args[0]

    def test_sets_every_field_the_caller_passed(self):
        self.client.list_available_tools("user@example.com", page_size=20, page_token="tok-1")
        request = self._request()
        self.assertIsInstance(request, pb.ListAvailableToolsRequest)
        self.assertEqual(request.identifier, "user@example.com")
        self.assertEqual(request.page_size, 20)
        self.assertEqual(request.page_token, "tok-1")

    def test_omitted_optionals_are_left_out_of_the_request(self):
        self.client.list_available_tools("user@example.com")
        self.assertEqual(
            [field.name for field, _ in self._request().ListFields()],
            ["identifier"],
        )

    def test_uses_the_tool_call_timeout(self):
        """Tool discovery proxies third-party APIs, so it gets the tool deadline,
        like every other ToolsClient method -- not the shorter control-plane one."""
        self.client.list_available_tools("user@example.com")
        self.assertEqual(self.rpc.call_args.kwargs["timeout"], DEFAULT_TOOL_CALL_TIMEOUT_S)
        self.assertNotEqual(DEFAULT_TOOL_CALL_TIMEOUT_S, DEFAULT_CALL_TIMEOUT_S)

    def test_returns_the_response_and_call_tuple_unchanged(self):
        sentinel_call = object()
        response = _available_page()
        self.rpc.return_value = (response, sentinel_call)
        result = self.client.list_available_tools("user@example.com")
        self.assertIs(result[0], response)
        self.assertIs(result[1], sentinel_call)

    def test_optionals_are_keyword_only(self):
        with self.assertRaises(TypeError):
            self.client.list_available_tools("user@example.com", 20)  # type: ignore[misc]
        self.rpc.assert_not_called()


class TestActionsListAvailableTools(unittest.TestCase):
    """ActionClient.list_available_tools: forwarding and response mapping."""

    def setUp(self):
        self.tools = MagicMock()
        self.tools.list_available_tools.return_value = (_available_page(), None)
        self.actions = ActionClient(self.tools, MagicMock())

    def test_forwards_all_arguments(self):
        self.actions.list_available_tools("user@example.com", page_size=20, page_token="tok-1")
        self.tools.list_available_tools.assert_called_once_with(
            identifier="user@example.com", page_size=20, page_token="tok-1"
        )

    def test_omitted_optionals_are_forwarded_as_none(self):
        self.actions.list_available_tools("user@example.com")
        kwargs = self.tools.list_available_tools.call_args.kwargs
        self.assertIsNone(kwargs["page_size"])
        self.assertIsNone(kwargs["page_token"])

    def test_optionals_are_keyword_only(self):
        with self.assertRaises(TypeError):
            self.actions.list_available_tools("user@example.com", 20)  # type: ignore[misc]
        self.tools.list_available_tools.assert_not_called()

    def test_unknown_keyword_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.actions.list_available_tools("user@example.com", page_sise=20)  # type: ignore[call-arg]
        self.tools.list_available_tools.assert_not_called()

    def test_maps_response(self):
        result = self.actions.list_available_tools("user@example.com")
        self.assertIsInstance(result, ListAvailableToolsResponse)
        self.assertEqual(result.total_count, 7)
        self.assertEqual(result.next_page_token, "next-2")
        self.assertEqual(result.previous_page_token, "prev-0")
        self.assertEqual([tool.id for tool in result.tools], ["tool_1", "tool_2"])
        self.assertEqual(result.tools[0].provider, "slack")
        self.assertEqual(result.tools[0].definition, {"name": "slack_post_message"})
        # Unset Struct fields are absent, not an empty dict.
        self.assertIsNone(result.tools[1].definition)

    def test_to_dict(self):
        result = self.actions.list_available_tools("user@example.com").to_dict()
        self.assertEqual(
            set(result),
            {"tools", "total_count", "next_page_token", "previous_page_token"},
        )
        self.assertEqual(result["tools"][0]["id"], "tool_1")

    def test_empty_page_maps_to_empty_list_zero_total_and_no_tokens(self):
        """total_size is a uint32 with no presence on the wire, so zero stays 0 --
        like ListToolsResponse. Only the page tokens, which are strings where ""
        means "no further page", map to None."""
        self.tools.list_available_tools.return_value = (pb.ListAvailableToolsResponse(), None)
        result = self.actions.list_available_tools("user@example.com")
        self.assertEqual(result.tools, [])
        self.assertEqual(result.total_count, 0)
        self.assertIsNone(result.next_page_token)
        self.assertIsNone(result.previous_page_token)

    def test_model_accepts_wire_aliases(self):
        model = ListAvailableToolsResponse(total_size=3, prev_page_token="p")
        self.assertEqual(model.total_count, 3)
        self.assertEqual(model.previous_page_token, "p")


class TestActionsListScopedTools(unittest.TestCase):
    """ActionClient.list_scoped_tools: required filter, forwarding, response mapping."""

    def setUp(self):
        self.tools = MagicMock()
        self.tools.list_scoped_tools.return_value = (_scoped_page(), None)
        self.actions = ActionClient(self.tools, MagicMock())
        self.filter = pb.ScopedToolFilter(providers=["slack"])

    def _list(self, **kwargs):
        """Call the method, supplying the required filter unless a test overrides it."""
        kwargs.setdefault("filter", self.filter)
        return self.actions.list_scoped_tools("user@example.com", **kwargs)

    def test_forwards_all_arguments(self):
        self._list(page_size=20, page_token="tok-1")
        self.tools.list_scoped_tools.assert_called_once_with(
            identifier="user@example.com",
            filter=self.filter,
            page_size=20,
            page_token="tok-1",
        )

    def test_filter_is_required(self):
        """ScopedToolFilter is `(buf.validate.field).required = true` on the wire,
        so a request without one is rejected server-side after a round trip. The
        signature rejects it locally instead."""
        with self.assertRaises(TypeError):
            self.actions.list_scoped_tools("user@example.com")  # type: ignore[call-arg]
        self.tools.list_scoped_tools.assert_not_called()

    def test_explicit_none_filter_raises_value_error_before_any_call(self):
        """The annotation is enforced by nothing at runtime, and most callers do
        not run a type checker, so `filter=None` reaches the method. The older
        `ToolsClient.list_scoped_tools` still defaults `filter=None`, which makes
        this a likely mistake when moving to the facade -- fail locally with a
        clear message instead of sending a request the server rejects."""
        with self.assertRaises(ValueError) as caught:
            self.actions.list_scoped_tools("user@example.com", filter=None)  # type: ignore[arg-type]
        self.assertEqual(str(caught.exception), "filter is required")
        self.tools.list_scoped_tools.assert_not_called()

    def test_empty_filter_is_forwarded_as_given(self):
        """An empty ScopedToolFilter() narrows nothing and is the way to ask for
        every scoped tool -- it must reach the wire, not be dropped."""
        empty = pb.ScopedToolFilter()
        self._list(filter=empty)
        self.assertIs(self.tools.list_scoped_tools.call_args.kwargs["filter"], empty)

    def test_omitted_optionals_are_forwarded_as_none(self):
        self._list()
        kwargs = self.tools.list_scoped_tools.call_args.kwargs
        self.assertIs(kwargs["filter"], self.filter)
        self.assertIsNone(kwargs["page_size"])
        self.assertIsNone(kwargs["page_token"])

    def test_arguments_after_identifier_are_keyword_only(self):
        with self.assertRaises(TypeError):
            self.actions.list_scoped_tools("user@example.com", pb.ScopedToolFilter())  # type: ignore[misc]
        self.tools.list_scoped_tools.assert_not_called()

    def test_maps_response(self):
        result = self._list()
        self.assertIsInstance(result, ListScopedToolsResponse)
        self.assertEqual(result.total_count, 2)
        self.assertEqual(result.next_page_token, "next-2")
        self.assertEqual(result.previous_page_token, "prev-0")
        first = result.tools[0]
        self.assertEqual(first.identifier, "user@example.com")
        self.assertEqual(first.connected_account_id, "ca_111")
        self.assertEqual(first.tool.id, "tool_1")
        self.assertEqual(first.tool.provider, "slack")

    def test_absent_tool_message_maps_to_none(self):
        """An unset singular message field reads as a truthy default instance in
        protobuf for Python, so presence must come from HasField."""
        second = self._list().tools[1]
        self.assertIsNone(second.tool)
        self.assertIsNone(second.connected_account_id)
        self.assertIsNone(second.to_dict()["tool"])

    def test_to_dict(self):
        result = self._list().to_dict()
        self.assertEqual(
            set(result),
            {"tools", "total_count", "next_page_token", "previous_page_token"},
        )
        self.assertEqual(result["tools"][0]["connected_account_id"], "ca_111")
        self.assertEqual(result["tools"][0]["tool"]["id"], "tool_1")

    def test_empty_page_maps_to_empty_list_zero_total_and_no_tokens(self):
        """Zero scoped tools is total_count == 0, never None: total_size has no
        presence on the wire, so None would invent a distinction the server
        cannot express and would answer differently from actions.list_tools()."""
        self.tools.list_scoped_tools.return_value = (pb.ListScopedToolsResponse(), None)
        result = self._list()
        self.assertEqual(result.tools, [])
        self.assertEqual(result.total_count, 0)
        self.assertIsNone(result.next_page_token)
        self.assertIsNone(result.previous_page_token)


class TestActionsSearchTools(unittest.TestCase):
    """ActionClient.search_tools: forwarding, mapping and unknown readiness states."""

    def setUp(self):
        self.tools = MagicMock()
        self.tools.search_tools.return_value = (_search_results(), None)
        self.actions = ActionClient(self.tools, MagicMock())

    def test_forwards_all_arguments(self):
        self.actions.search_tools("send a slack message", identifier="user@example.com", top_k=5)
        self.tools.search_tools.assert_called_once_with(
            query="send a slack message", identifier="user@example.com", top_k=5
        )

    def test_omitted_optionals_are_forwarded_as_none(self):
        self.actions.search_tools("send a slack message")
        kwargs = self.tools.search_tools.call_args.kwargs
        self.assertIsNone(kwargs["identifier"])
        self.assertIsNone(kwargs["top_k"])

    def test_blank_identifier_is_forwarded_as_none(self):
        """A blank identifier means "no identifier" to the caller, so it must not
        be forwarded as an empty string -- see TestActionsSearchToolsOnTheWire."""
        self.actions.search_tools("send a slack message", identifier="")
        self.assertIsNone(self.tools.search_tools.call_args.kwargs["identifier"])

    def test_optionals_are_keyword_only(self):
        with self.assertRaises(TypeError):
            self.actions.search_tools("send a slack message", "user@example.com")  # type: ignore[misc]
        self.tools.search_tools.assert_not_called()

    def test_unknown_keyword_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.actions.search_tools("query", top_key=5)  # type: ignore[call-arg]
        self.tools.search_tools.assert_not_called()

    def test_maps_response(self):
        result = self.actions.search_tools("send a slack message")
        self.assertIsInstance(result, SearchToolsResponse)
        self.assertEqual(
            [tool.name for tool in result.tools], ["slack_post_message", "gmail_send_email"]
        )
        first = result.tools[0]
        self.assertEqual(first.provider, "slack")
        self.assertEqual(first.description, "Post a message to a Slack channel")
        self.assertAlmostEqual(first.score, 0.93, places=5)
        self.assertEqual(
            [connection.readiness_state for connection in first.connections],
            ["TOOL_READINESS_STATE_READY", "TOOL_READINESS_STATE_NEEDS_REAUTH"],
        )
        self.assertEqual(first.connections[0].connection_name, "slack-prod")
        self.assertEqual(first.connections[0].connected_account_id, "ca_111")

    def test_result_without_connections_maps_to_empty_list(self):
        """An empty connections list means no connection exists for the provider.
        It is not an error, and must never be None."""
        second = self.actions.search_tools("send an email").tools[1]
        self.assertEqual(second.connections, [])
        self.assertIsNone(second.description)

    def test_unknown_readiness_state_does_not_raise(self):
        """ToolReadinessState.Name raises ValueError for a value these stubs do
        not know. A new server-side state must not crash the caller."""
        self.tools.search_tools.return_value = (
            pb.SearchToolsResponse(
                tools=[
                    pb.SearchedTool(
                        name="slack_post_message",
                        connections=[
                            pb.ConnectionReadiness(
                                connection_name="slack-prod",
                                readiness_state=UNKNOWN_READINESS_VALUE,
                            )
                        ],
                    )
                ]
            ),
            None,
        )
        with self.assertRaises(ValueError):
            pb.ToolReadinessState.Name(UNKNOWN_READINESS_VALUE)

        result = self.actions.search_tools("send a slack message")
        self.assertEqual(
            result.tools[0].connections[0].readiness_state,
            str(UNKNOWN_READINESS_VALUE),
        )

    def test_unspecified_readiness_state_keeps_its_name(self):
        readiness = ConnectionReadiness.from_proto(pb.ConnectionReadiness())
        self.assertEqual(readiness.readiness_state, "TOOL_READINESS_STATE_UNSPECIFIED")
        self.assertIsNone(readiness.connection_name)

    def test_to_dict(self):
        result = self.actions.search_tools("send a slack message").to_dict()
        self.assertEqual(set(result), {"tools"})
        first = result["tools"][0]
        self.assertEqual(first["name"], "slack_post_message")
        self.assertEqual(first["connections"][0]["readiness_state"], "TOOL_READINESS_STATE_READY")

    def test_no_results_maps_to_empty_list(self):
        self.tools.search_tools.return_value = (pb.SearchToolsResponse(), None)
        self.assertEqual(self.actions.search_tools("nothing matches").tools, [])


class TestActionsSearchToolsOnTheWire(unittest.TestCase):
    """ActionClient.search_tools over a real ToolsClient: what reaches the stub."""

    def setUp(self):
        self.tools = _tools_client()
        self.rpc = self.tools.tool_service.SearchTools.with_call
        self.rpc.return_value = (_search_results(), None)
        self.actions = ActionClient(self.tools, MagicMock())

    def _request(self):
        return self.rpc.call_args.args[0]

    def test_blank_identifier_never_reaches_the_wire(self):
        """SearchToolsRequest.identifier is `optional string`, so an empty string
        serialises as *present* and the server branches on presence -- readiness
        is only meaningful when an identifier was supplied. Omit it instead."""
        self.assertTrue(pb.SearchToolsRequest(identifier="").HasField("identifier"))

        self.actions.search_tools("send a slack message", identifier="")

        request = self._request()
        self.assertFalse(request.HasField("identifier"))
        self.assertEqual([field.name for field, _ in request.ListFields()], ["query"])

    def test_identifier_reaches_the_wire_when_supplied(self):
        self.actions.search_tools("send a slack message", identifier="user@example.com")
        request = self._request()
        self.assertTrue(request.HasField("identifier"))
        self.assertEqual(request.identifier, "user@example.com")

    def test_maps_the_response_from_the_wire(self):
        result = self.actions.search_tools("send a slack message", identifier="")
        self.assertIsInstance(result, SearchToolsResponse)
        self.assertEqual(
            [tool.name for tool in result.tools], ["slack_post_message", "gmail_send_email"]
        )


if __name__ == "__main__":
    unittest.main()

"""Offline tests for the tool methods that serve custom connectors: the gRPC layer is stubbed."""
import unittest
from unittest.mock import MagicMock

from scalekit.actions.actions import ActionClient
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitNotFoundException,
    ScalekitTooManyRequestsException,
)
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


class RefreshToolsTest(ToolsTestCase):
    def test_a_connected_account_id_alone_is_enough(self):
        self._reply(pb.RefreshToolsResponse(tools=[_tool("c-acme_a"), _tool("c-acme_b")], total_size=2))
        response, _ = self.tools.refresh_tools(connected_account_id="ca_123")
        request = self.calls[0][1]
        self.assertEqual(request.connected_account_id, "ca_123")
        self.assertEqual((request.connector, request.identifier), ("", ""))
        self.assertEqual((len(response.tools), response.total_size), (2, 2))

    def test_connection_name_is_sent_as_the_connector_with_the_identifier(self):
        self._reply(pb.RefreshToolsResponse())
        self.tools.refresh_tools(
            identifier="user@example.com", connection_name="acme-mcp", organization_id="org_1", user_id="usr_1"
        )
        request = self.calls[0][1]
        self.assertEqual(
            (request.connector, request.identifier, request.organization_id, request.user_id),
            ("acme-mcp", "user@example.com", "org_1", "usr_1"),
        )
        self.assertEqual(request.connected_account_id, "")

    def test_a_selector_that_names_no_account_is_refused_before_anything_is_sent(self):
        """The server resolves an account from its ID, or from the connection name plus an identifier (or an
        organization, for an account created without one); every other combination is a 400 there."""
        partial = (
            {},
            {"connection_name": "acme-mcp"},
            {"identifier": "user@example.com"},
            {"organization_id": "org_1"},
            {"user_id": "usr_1"},
            {"organization_id": "org_1", "user_id": "usr_1"},
            {"identifier": "user@example.com", "organization_id": "org_1", "user_id": "usr_1"},  # no connection
            {"connection_name": "acme-mcp", "user_id": "usr_1"},  # a user alone names no account
            {"connection_name": "", "identifier": "user@example.com"},
            {"connection_name": "acme-mcp", "identifier": ""},
            {"connected_account_id": ""},
        )
        for kwargs in partial:
            with self.subTest(kwargs):
                with self.assertRaises(ValueError) as ctx:
                    self.tools.refresh_tools(**kwargs)
                self.assertIn(
                    "connected_account_id, or connection_name together with identifier", str(ctx.exception)
                )
        self.assertEqual(self.calls, [], "nothing is sent when the selector is refused")

    def test_every_selector_the_server_resolves_is_sent_as_given(self):
        selectors = (
            {"connected_account_id": "ca_123"},
            {"connection_name": "acme-mcp", "identifier": "user@example.com"},
            {"connection_name": "acme-mcp", "identifier": "user@example.com", "organization_id": "org_1"},
            {"connection_name": "acme-mcp", "identifier": "user@example.com", "user_id": "usr_1"},
            {
                "connection_name": "acme-mcp",
                "identifier": "user@example.com",
                "organization_id": "org_1",
                "user_id": "usr_1",
            },
            # an account created with an organization (and a user) and no identifier
            {"connection_name": "acme-mcp", "organization_id": "org_1"},
            {"connection_name": "acme-mcp", "organization_id": "org_1", "user_id": "usr_1"},
        )
        for kwargs in selectors:
            with self.subTest(kwargs):
                self._reply(pb.RefreshToolsResponse())
                before = len(self.calls)
                self.tools.refresh_tools(**kwargs)
                self.assertEqual(len(self.calls), before + 1)
                request = self.calls[-1][1]
                self.assertEqual(
                    (
                        request.connected_account_id,
                        request.connector,
                        request.identifier,
                        request.organization_id,
                        request.user_id,
                    ),
                    (
                        kwargs.get("connected_account_id", ""),
                        kwargs.get("connection_name", ""),
                        kwargs.get("identifier", ""),
                        kwargs.get("organization_id", ""),
                        kwargs.get("user_id", ""),
                    ),
                )

    def test_uses_the_tool_call_deadline_and_the_default_retry(self):
        """A refresh only upserts and removes stale rows, so repeating it is safe."""
        self._reply(pb.RefreshToolsResponse())
        self.tools.refresh_tools(connected_account_id="ca_123")
        kwargs = self.calls[0][2]
        self.assertIs(kwargs["timeout"], self.core.tool_call_timeout_s)
        self.assertNotIn("retry_on_unavailable", kwargs)

    def test_server_rejections_reach_the_caller_unchanged(self):
        self._reply(
            _server_error(
                ScalekitBadRequestException, "connected account is not a custom MCP connector", "INVALID_ARGUMENT"
            ),
            _server_error(ScalekitNotFoundException, "connected account not found", "NOT_FOUND"),
            _server_error(
                ScalekitTooManyRequestsException,
                "a tool refresh is already in progress for this connected account; please retry in a few seconds",
                "DISCOVERY_IN_PROGRESS",
            ),
        )
        with self.assertRaises(ScalekitBadRequestException) as not_mcp:
            self.tools.refresh_tools(connected_account_id="ca_1")
        self.assertIn("not a custom MCP connector", not_mcp.exception.message)
        with self.assertRaises(ScalekitNotFoundException):
            self.tools.refresh_tools(connected_account_id="ca_2")
        with self.assertRaises(ScalekitTooManyRequestsException) as busy:
            self.tools.refresh_tools(connected_account_id="ca_3")
        self.assertEqual(busy.exception.error_code, "DISCOVERY_IN_PROGRESS")


class ListAvailableToolsTest(ToolsTestCase):
    def test_maps_the_identifier_and_paging(self):
        self._reply(
            pb.ListAvailableToolsResponse(
                tools=[_tool("a-petstore_listpets")], total_size=1, next_page_token="next"
            )
        )
        response, _ = self.tools.list_available_tools("user@example.com", page_size=50, page_token="tok")
        request = self.calls[0][1]
        self.assertEqual((request.identifier, request.page_size, request.page_token), ("user@example.com", 50, "tok"))
        self.assertIs(self.calls[0][2]["timeout"], self.core.tool_call_timeout_s)
        self.assertEqual((len(response.tools), response.next_page_token), (1, "next"))

    def test_paging_is_optional(self):
        self._reply(pb.ListAvailableToolsResponse())
        self.tools.list_available_tools("user@example.com")
        request = self.calls[0][1]
        self.assertEqual((request.page_size, request.page_token), (0, ""))


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

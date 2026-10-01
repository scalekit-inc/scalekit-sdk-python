"""Offline tests for search_connected_accounts on ActionClient and ConnectedAccountsClient.

No credentials or network: the ActionClient tests mock ConnectedAccountsClient, and
the ConnectedAccountsClient tests run the real CoreClient.grpc_exec against a mocked
gRPC stub method.
"""

import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from google.protobuf.timestamp_pb2 import Timestamp
from grpc import StatusCode

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import ListConnectedAccountsResponse, SearchConnectedAccountsResponse
from scalekit.common.exceptions import ScalekitBadRequestException
from scalekit.connected_accounts import ConnectedAccountsClient
from scalekit.v1.connected_accounts import connected_accounts_pb2 as pb

try:  # `make test` / `unittest discover -s tests` puts tests/ on sys.path
    from test_sk819_retry_behavior import _make_core_client, _make_rpc_error
except ModuleNotFoundError:  # `python -m unittest tests.<module>` from the repo root
    from tests.test_sk819_retry_behavior import _make_core_client, _make_rpc_error

ConnectedAccountForListProto = pb.ConnectedAccountForList
ConnectorStatus = pb.ConnectorStatus
ConnectorType = pb.ConnectorType
SearchConnectedAccountsRequest = pb.SearchConnectedAccountsRequest
SearchConnectedAccountsResponseProto = pb.SearchConnectedAccountsResponse

BLANK_QUERIES = ["", "   ", "\t\n", None]


UPDATED_AT = datetime(2026, 9, 1, 12, 30, 0, tzinfo=timezone.utc)


def _proto_page():
    updated_at = Timestamp()
    updated_at.FromDatetime(UPDATED_AT)
    return SearchConnectedAccountsResponseProto(
        connected_accounts=[
            ConnectedAccountForListProto(
                identifier="alice@example.com",
                provider="google",
                connector="gmail",
                status=ConnectorStatus.ACTIVE,
                authorization_type=ConnectorType.OAUTH,
                updated_at=updated_at,
                id="ca_111",
                connection_id="conn_111",
                is_org_wide_credential=True,
            ),
            ConnectedAccountForListProto(
                identifier="bob@example.com",
                provider="google",
                connector="googlecalendar",
                status=ConnectorStatus.EXPIRED,
                authorization_type=ConnectorType.OAUTH,
            ),
        ],
        total_size=7,
        next_page_token="next-2",
        prev_page_token="prev-0",
    )


class TestActionsSearchConnectedAccounts(unittest.TestCase):
    """ActionClient.search_connected_accounts: validation, forwarding, mapping."""

    def setUp(self):
        self.connected_accounts = MagicMock()
        self.connected_accounts.search_connected_accounts.return_value = (_proto_page(), None)
        self.actions = ActionClient(MagicMock(), self.connected_accounts)

    def test_forwards_all_arguments(self):
        self.actions.search_connected_accounts(
            query="alice", page_size=10, page_token="tok-1", connection_id="conn_123"
        )
        self.connected_accounts.search_connected_accounts.assert_called_once_with(
            query="alice", page_size=10, page_token="tok-1", connection_id="conn_123"
        )

    def test_omitted_optionals_are_forwarded_as_none(self):
        self.actions.search_connected_accounts("alice")
        self.connected_accounts.search_connected_accounts.assert_called_once_with(
            query="alice", page_size=None, page_token=None, connection_id=None
        )

    def test_query_and_connection_id_are_trimmed(self):
        self.actions.search_connected_accounts("  Alice ", connection_id=" conn_123\n")
        kwargs = self.connected_accounts.search_connected_accounts.call_args.kwargs
        self.assertEqual(kwargs["query"], "Alice")
        self.assertEqual(kwargs["connection_id"], "conn_123")

    def test_blank_connection_id_is_forwarded_as_none(self):
        for connection_id in ["", "   "]:
            with self.subTest(connection_id=connection_id):
                self.actions.search_connected_accounts("alice", connection_id=connection_id)
                kwargs = self.connected_accounts.search_connected_accounts.call_args.kwargs
                self.assertIsNone(kwargs["connection_id"])

    def test_blank_query_raises_before_any_call(self):
        for query in BLANK_QUERIES:
            with self.subTest(query=query), self.assertRaisesRegex(ValueError, "query is required"):
                self.actions.search_connected_accounts(query)
        self.connected_accounts.search_connected_accounts.assert_not_called()

    def test_optionals_are_keyword_only(self):
        with self.assertRaises(TypeError):
            self.actions.search_connected_accounts("alice", 10)  # type: ignore[misc]
        self.connected_accounts.search_connected_accounts.assert_not_called()

    def test_unknown_keyword_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.actions.search_connected_accounts("alice", page_sise=10)  # type: ignore[call-arg]
        self.connected_accounts.search_connected_accounts.assert_not_called()

    def test_maps_response(self):
        result = self.actions.search_connected_accounts("google")

        self.assertIsInstance(result, SearchConnectedAccountsResponse)
        self.assertIsInstance(result, ListConnectedAccountsResponse)
        self.assertEqual(result.total_count, 7)
        self.assertEqual(result.next_page_token, "next-2")
        self.assertEqual(result.previous_page_token, "prev-0")
        self.assertEqual(
            [a.identifier for a in result.connected_accounts],
            ["alice@example.com", "bob@example.com"],
        )
        first = result.connected_accounts[0]
        self.assertEqual(first.provider, "google")
        self.assertEqual(first.connector, "gmail")
        self.assertEqual(first.status, "ACTIVE")
        self.assertEqual(first.authorization_type, "OAUTH")
        # Inherited mapping returns naive UTC datetimes (python standard section 16, gap 24).
        self.assertEqual(first.updated_at, UPDATED_AT.replace(tzinfo=None))
        self.assertEqual(first.id, "ca_111")
        self.assertEqual(first.connection_id, "conn_111")
        self.assertIs(first.is_org_wide_credential, True)
        second = result.connected_accounts[1]
        self.assertEqual(second.status, "EXPIRED")
        # Unset strings become None; the plain proto bool has no presence, so it reads False.
        self.assertIsNone(second.id)
        self.assertIsNone(second.connection_id)
        self.assertIs(second.is_org_wide_credential, False)

    def test_to_dict_uses_list_response_keys(self):
        result = self.actions.search_connected_accounts("google").to_dict()
        self.assertEqual(
            set(result),
            {"connected_accounts", "total_count", "next_page_token", "previous_page_token"},
        )
        self.assertEqual(result["total_count"], 7)
        first = result["connected_accounts"][0]
        self.assertEqual(first["connector"], "gmail")
        self.assertEqual(first["id"], "ca_111")
        self.assertEqual(first["connection_id"], "conn_111")
        self.assertIs(first["is_org_wide_credential"], True)
        self.assertIsNone(result["connected_accounts"][1]["id"])

    def test_empty_page_maps_to_empty_list_and_none(self):
        self.connected_accounts.search_connected_accounts.return_value = (
            SearchConnectedAccountsResponseProto(),
            None,
        )
        result = self.actions.search_connected_accounts("nomatch")
        self.assertEqual(result.connected_accounts, [])
        self.assertIsNone(result.total_count)
        self.assertIsNone(result.next_page_token)
        self.assertIsNone(result.previous_page_token)

    def test_model_accepts_wire_aliases(self):
        model = SearchConnectedAccountsResponse(total_size=3, prev_page_token="p")
        self.assertEqual(model.total_count, 3)
        self.assertEqual(model.previous_page_token, "p")

    def test_server_error_propagates(self):
        self.connected_accounts.search_connected_accounts.side_effect = ScalekitBadRequestException(
            _make_rpc_error(StatusCode.INVALID_ARGUMENT)
        )
        with self.assertRaises(ScalekitBadRequestException):
            self.actions.search_connected_accounts("ab")

    # Known gaps inherited from ConnectedAccountForList.from_proto, shared with
    # list_connected_accounts (python standard section 16, gaps 24 and 25). Fixing
    # them changes list_connected_accounts output too, so it is a separate change.
    # When it lands these start passing and the decorators must be removed.
    @unittest.expectedFailure
    def test_unset_timestamp_maps_to_none(self):
        result = self.actions.search_connected_accounts("google")
        self.assertIsNone(result.connected_accounts[1].updated_at)

    @unittest.expectedFailure
    def test_unknown_status_does_not_raise(self):
        self.connected_accounts.search_connected_accounts.return_value = (
            SearchConnectedAccountsResponseProto(
                connected_accounts=[ConnectedAccountForListProto(identifier="x", status=999)]
            ),
            None,
        )
        result = self.actions.search_connected_accounts("xyz")
        self.assertEqual(len(result.connected_accounts), 1)


class TestConnectedAccountsClientSearch(unittest.TestCase):
    """ConnectedAccountsClient.search_connected_accounts through the real grpc_exec."""

    def setUp(self):
        self.core = _make_core_client()
        self.core.grpc_secure_channel = MagicMock()
        self.client = ConnectedAccountsClient(self.core)
        self.with_call = MagicMock()
        self.client.connected_accounts_service = MagicMock()
        self.client.connected_accounts_service.SearchConnectedAccounts.with_call = self.with_call
        self.call = MagicMock()
        self.response = _proto_page()
        self.with_call.return_value = (self.response, self.call)

    def _sent_request(self):
        self.assertEqual(self.with_call.call_count, 1)
        request = self.with_call.call_args.args[0]
        self.assertIsInstance(request, SearchConnectedAccountsRequest)
        return request

    def test_builds_request_and_returns_response_call_tuple(self):
        result = self.client.search_connected_accounts(
            query="alice", page_size=30, page_token="tok-1", connection_id="conn_123"
        )

        self.assertEqual(result, (self.response, self.call))
        request = self._sent_request()
        self.assertEqual(request.query, "alice")
        self.assertEqual(request.page_size, 30)
        self.assertEqual(request.page_token, "tok-1")
        self.assertEqual(request.connection_id, "conn_123")
        kwargs = self.with_call.call_args.kwargs
        self.assertEqual(kwargs["timeout"], self.core.call_timeout_s)
        self.assertIn(("authorization", "Bearer test-token"), kwargs["metadata"])

    def test_omitted_optionals_are_not_sent(self):
        self.client.search_connected_accounts("alice")
        request = self._sent_request()
        self.assertEqual([field.name for field, _ in request.ListFields()], ["query"])

    def test_blank_query_raises_before_any_call(self):
        for query in BLANK_QUERIES:
            with self.subTest(query=query), self.assertRaisesRegex(ValueError, "query is required"):
                self.client.search_connected_accounts(query)
        self.with_call.assert_not_called()

    def test_optionals_are_keyword_only(self):
        with self.assertRaises(TypeError):
            self.client.search_connected_accounts("alice", 10, "tok-1")  # type: ignore[misc]
        self.with_call.assert_not_called()

    def test_query_and_connection_id_are_trimmed_and_blank_filter_not_sent(self):
        self.client.search_connected_accounts(" alice ", connection_id="  ")
        request = self._sent_request()
        self.assertEqual(request.query, "alice")
        self.assertEqual([field.name for field, _ in request.ListFields()], ["query"])

        self.with_call.reset_mock()
        self.client.search_connected_accounts("alice", connection_id=" conn_123 ")
        self.assertEqual(self._sent_request().connection_id, "conn_123")

    def test_negative_page_size_raises_before_any_call(self):
        with self.assertRaises(ValueError):
            self.client.search_connected_accounts("alice", page_size=-1)
        self.with_call.assert_not_called()

    def test_invalid_argument_maps_to_bad_request_without_retry(self):
        self.with_call.side_effect = _make_rpc_error(
            StatusCode.INVALID_ARGUMENT, message="query must be at least 3 characters"
        )
        with self.assertRaises(ScalekitBadRequestException):
            self.client.search_connected_accounts("ab")
        self.assertEqual(self.with_call.call_count, 1)

    def test_unavailable_is_retried_because_search_is_a_read(self):
        self.with_call.side_effect = [
            _make_rpc_error(StatusCode.UNAVAILABLE),
            (self.response, self.call),
        ]
        with patch("scalekit.core.time.sleep"):
            result = self.client.search_connected_accounts("alice")
        self.assertEqual(result, (self.response, self.call))
        self.assertEqual(self.with_call.call_count, 2)


if __name__ == "__main__":
    unittest.main()

"""Offline tests: list_connected_accounts sends `query` and `is_org_wide_credential` to the API."""

import unittest
from unittest.mock import MagicMock

from scalekit.actions.actions import ActionClient
from scalekit.connected_accounts import ConnectedAccountsClient
from scalekit.v1.connected_accounts.connected_accounts_pb2 import ListConnectedAccountsResponse


def _client():
    core = MagicMock()
    core.grpc_exec.return_value = (ListConnectedAccountsResponse(), None)
    client = ConnectedAccountsClient.__new__(ConnectedAccountsClient)
    client.core_client = core
    client.connected_accounts_service = MagicMock()
    return client, core


def _sent_request(core):
    return core.grpc_exec.call_args.args[1]


class TestConnectedAccountsClientRequest(unittest.TestCase):
    def test_query_is_sent(self):
        client, core = _client()
        client.list_connected_accounts(query="linear")
        self.assertEqual(_sent_request(core).query, "linear")

    def test_org_wide_filter_true_and_false_are_both_sent(self):
        for value in (True, False):
            client, core = _client()
            client.list_connected_accounts(is_org_wide_credential=value)
            request = _sent_request(core)
            self.assertTrue(request.HasField("is_org_wide_credential"))
            self.assertEqual(request.is_org_wide_credential, value)

    def test_omitted_options_stay_unset(self):
        client, core = _client()
        client.list_connected_accounts(identifier="user@example.com")
        request = _sent_request(core)
        self.assertEqual(request.query, "")
        self.assertFalse(request.HasField("is_org_wide_credential"))


class TestActionClientForwarding(unittest.TestCase):
    def setUp(self):
        self.connected_accounts = MagicMock()
        self.connected_accounts.list_connected_accounts.return_value = (
            ListConnectedAccountsResponse(total_size=1),
            None,
        )
        self.actions = ActionClient(MagicMock(), self.connected_accounts)

    def test_query_and_org_wide_filter_are_forwarded(self):
        self.actions.list_connected_accounts(query="slack", is_org_wide_credential=True)
        kwargs = self.connected_accounts.list_connected_accounts.call_args.kwargs
        self.assertEqual(kwargs["query"], "slack")
        self.assertIs(kwargs["is_org_wide_credential"], True)

    def test_omitted_options_are_forwarded_as_unset(self):
        self.actions.list_connected_accounts(identifier="user@example.com")
        kwargs = self.connected_accounts.list_connected_accounts.call_args.kwargs
        self.assertIsNone(kwargs["query"])
        self.assertIsNone(kwargs["is_org_wide_credential"])

    def test_existing_positional_order_is_unchanged(self):
        self.actions.list_connected_accounts("gmail", "user_1", "google", ["a"], 10, "tok")
        kwargs = self.connected_accounts.list_connected_accounts.call_args.kwargs
        self.assertEqual(
            (kwargs["connector"], kwargs["identifier"], kwargs["provider"],
             kwargs["connection_names"], kwargs["page_size"], kwargs["page_token"]),
            ("gmail", "user_1", "google", ["a"], 10, "tok"),
        )


if __name__ == "__main__":
    unittest.main()

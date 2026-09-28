"""Offline tests: actions.list_connected_accounts forwards pagination to the connected accounts client."""

import unittest
from unittest.mock import MagicMock

from scalekit.actions.actions import ActionClient
from scalekit.v1.connected_accounts.connected_accounts_pb2 import ListConnectedAccountsResponse


class TestListConnectedAccountsPagination(unittest.TestCase):
    def setUp(self):
        self.connected_accounts = MagicMock()
        self.connected_accounts.list_connected_accounts.return_value = (
            ListConnectedAccountsResponse(next_page_token="next-1", total_size=42),
            None,
        )
        self.actions = ActionClient(MagicMock(), self.connected_accounts)

    def test_forwards_page_size_and_page_token(self):
        self.actions.list_connected_accounts(
            connection_name="gmail", page_size=25, page_token="tok-abc"
        )
        kwargs = self.connected_accounts.list_connected_accounts.call_args.kwargs
        self.assertEqual(kwargs["page_size"], 25)
        self.assertEqual(kwargs["page_token"], "tok-abc")
        self.assertEqual(kwargs["connector"], "gmail")

    def test_omitted_pagination_stays_unset(self):
        self.actions.list_connected_accounts(identifier="user_123")
        kwargs = self.connected_accounts.list_connected_accounts.call_args.kwargs
        self.assertIsNone(kwargs["page_size"])
        self.assertIsNone(kwargs["page_token"])

    def test_returns_next_page_token(self):
        result = self.actions.list_connected_accounts(page_size=1)
        self.assertEqual(result.next_page_token, "next-1")
        self.assertEqual(result.total_count, 42)


if __name__ == "__main__":
    unittest.main()

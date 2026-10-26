"""Offline tests: connected_accounts.refresh_connected_account_tokens request mapping and validation."""

import unittest
from unittest.mock import MagicMock

from scalekit.connected_accounts import ConnectedAccountsClient
from scalekit.v1.connected_accounts.connected_accounts_pb2 import (
    RefreshConnectedAccountTokensRequest,
    RefreshConnectedAccountTokensResponse,
)


class TestRefreshConnectedAccountTokens(unittest.TestCase):
    def setUp(self):
        self.core_client = MagicMock()
        self.response = (RefreshConnectedAccountTokensResponse(), None)
        self.core_client.grpc_exec.return_value = self.response
        self.client = ConnectedAccountsClient(self.core_client)
        self.client.connected_accounts_service = MagicMock()

    def _sent_request(self):
        args = self.core_client.grpc_exec.call_args.args
        self.assertIs(
            args[0],
            self.client.connected_accounts_service.RefreshConnectedAccountTokens.with_call,
        )
        return args[1]

    def test_maps_request(self):
        cases = [
            (
                "id only",
                dict(connected_account_id="ca_1"),
                RefreshConnectedAccountTokensRequest(connected_account_id="ca_1"),
            ),
            (
                "name and identifier",
                dict(connection_name="gmail", identifier="user_1"),
                RefreshConnectedAccountTokensRequest(connection_name="gmail", identifier="user_1"),
            ),
            (
                "id wins when all are sent",
                dict(connected_account_id="ca_1", connection_name="gmail", identifier="user_1"),
                RefreshConnectedAccountTokensRequest(connected_account_id="ca_1"),
            ),
            (
                "id plus only name",
                dict(connected_account_id="ca_1", connection_name="gmail"),
                RefreshConnectedAccountTokensRequest(connected_account_id="ca_1"),
            ),
        ]
        for name, kwargs, expected in cases:
            with self.subTest(name):
                self.core_client.grpc_exec.reset_mock()
                result = self.client.refresh_connected_account_tokens(**kwargs)
                self.assertIs(result, self.response)
                self.assertEqual(self._sent_request(), expected)

    def test_requires_id_or_name_and_identifier(self):
        cases = [
            ("nothing", dict()),
            ("only name", dict(connection_name="gmail")),
            ("only identifier", dict(identifier="user_1")),
            ("empty strings", dict(connected_account_id="", connection_name="", identifier="")),
            ("name and empty identifier", dict(connection_name="gmail", identifier="")),
        ]
        for name, kwargs in cases:
            with self.subTest(name):
                self.core_client.grpc_exec.reset_mock()
                with self.assertRaises(ValueError):
                    self.client.refresh_connected_account_tokens(**kwargs)
                self.core_client.grpc_exec.assert_not_called()

    def test_propagates_errors(self):
        self.core_client.grpc_exec.side_effect = RuntimeError("REAUTHENTICATION_NEEDED")
        with self.assertRaises(RuntimeError):
            self.client.refresh_connected_account_tokens(connected_account_id="ca_1")


if __name__ == "__main__":
    unittest.main()

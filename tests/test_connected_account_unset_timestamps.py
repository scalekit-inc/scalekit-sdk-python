"""Unset optional timestamps on connected-account responses convert to None, not the Unix epoch.

A protobuf message field is always truthy in Python, so a `if proto.field:` check turned an unset
`token_expires_at` into 1970-01-01. An imported OAuth token without `expires_at` has no expiry, so
`token_expires_at` must read back as None.
"""
import unittest
from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp

from scalekit.actions.models.responses.get_connected_account_auth_response import (
    ConnectedAccount,
    GetConnectedAccountAuthResponse,
)
from scalekit.actions.models.responses.list_connected_accounts_response import (
    ConnectedAccountForList,
    ListConnectedAccountsResponse,
)
from scalekit.v1.connected_accounts import connected_accounts_pb2 as pb

WHEN = datetime(2026, 12, 1, 12, 0, tzinfo=timezone.utc)
FIELDS = ("token_expires_at", "updated_at", "last_used_at")


def _ts(dt):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


class TestUnsetTimestamps(unittest.TestCase):
    def test_get_account_unset_timestamps_are_none(self):
        account = ConnectedAccount.from_proto(pb.ConnectedAccount(id="ca_1", identifier="user_123"))
        for field in FIELDS:
            with self.subTest(field=field):
                self.assertIsNone(getattr(account, field))

    def test_get_account_set_timestamps_are_kept(self):
        proto = pb.ConnectedAccount(id="ca_1", identifier="user_123")
        for field in FIELDS:
            getattr(proto, field).CopyFrom(_ts(WHEN))
        account = ConnectedAccount.from_proto(proto)
        for field in FIELDS:
            with self.subTest(field=field):
                self.assertEqual(getattr(account, field).replace(tzinfo=timezone.utc), WHEN)

    def test_get_response_without_expiry(self):
        resp = GetConnectedAccountAuthResponse.from_proto(
            pb.GetConnectedAccountByIdentifierResponse(connected_account=pb.ConnectedAccount(id="ca_1"))
        )
        self.assertIsNone(resp.connected_account.token_expires_at)

    def test_list_account_unset_timestamps_are_none(self):
        account = ConnectedAccountForList.from_proto(pb.ConnectedAccountForList(id="ca_1"))
        for field in FIELDS:
            with self.subTest(field=field):
                self.assertIsNone(getattr(account, field))
        self.assertIsNone(account.to_dict()["token_expires_at"])

    def test_list_account_set_expiry_is_kept(self):
        proto = pb.ConnectedAccountForList(id="ca_1")
        proto.token_expires_at.CopyFrom(_ts(WHEN))
        resp = ListConnectedAccountsResponse.from_proto(pb.ListConnectedAccountsResponse(connected_accounts=[proto]))
        self.assertEqual(resp.connected_accounts[0].token_expires_at.replace(tzinfo=timezone.utc), WHEN)


if __name__ == "__main__":
    unittest.main()

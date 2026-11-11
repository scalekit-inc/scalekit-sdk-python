"""
OauthToken.expires_at on client.actions create / update / get-or-create connected account.

authorization_details["oauth_token"]["expires_at"] accepts a timezone-aware datetime, an
RFC 3339 string, or epoch seconds, and is sent as a google.protobuf.Timestamp. Absent or None
leaves the field unset; a naive datetime or an unparseable value raises ValueError.

These tests never touch the network: the connected-accounts client is a stub.
"""
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp

from scalekit.actions.actions import ActionClient
from scalekit.actions.models.requests.create_connected_account_request import CreateConnectedAccountRequest
from scalekit.actions.models.requests.oauth_token import build_oauth_token, expires_at_to_timestamp
from scalekit.actions.models.requests.update_connected_account_request import UpdateConnectedAccountRequest
from scalekit.common.exceptions import ScalekitNotFoundException
from scalekit.v1.connected_accounts import connected_accounts_pb2 as pb

# 2026-12-01T10:00:00Z
EPOCH = 1796119200
IST = timezone(timedelta(hours=5, minutes=30))


def ts(seconds, nanos=0):
    return Timestamp(seconds=seconds, nanos=nanos)


def oauth(**extra):
    return {"oauth_token": {"access_token": "at", "refresh_token": "rt", "scopes": ["a", "b"], **extra}}


class TestExpiresAtConversion(unittest.TestCase):
    def test_accepted_forms(self):
        cases = [
            ("aware datetime, UTC", datetime(2026, 12, 1, 10, 0, tzinfo=timezone.utc), ts(EPOCH)),
            ("aware datetime, +05:30 offset", datetime(2026, 12, 1, 15, 30, tzinfo=IST), ts(EPOCH)),
            ("aware datetime with microseconds", datetime(2026, 12, 1, 10, 0, 0, 250000, tzinfo=timezone.utc), ts(EPOCH, 250_000_000)),
            ("RFC 3339 string with Z", "2026-12-01T10:00:00Z", ts(EPOCH)),
            ("RFC 3339 string with lowercase z", "2026-12-01T10:00:00z", ts(EPOCH)),
            ("RFC 3339 string with offset", "2026-12-01T15:30:00+05:30", ts(EPOCH)),
            ("RFC 3339 string with negative offset", "2026-12-01T05:00:00-05:00", ts(EPOCH)),
            ("RFC 3339 string with fraction", "2026-12-01T10:00:00.5Z", ts(EPOCH, 500_000_000)),
            ("RFC 3339 string with nanoseconds", "2026-12-01T10:00:00.123456789Z", ts(EPOCH, 123_456_789)),
            ("epoch int", EPOCH, ts(EPOCH)),
            ("epoch float", EPOCH + 0.25, ts(EPOCH, 250_000_000)),
            ("epoch float, whole", float(EPOCH), ts(EPOCH)),
            ("epoch at the Timestamp minimum", -62135596800, ts(-62135596800)),
            ("epoch at the Timestamp maximum", 253402300799, ts(253402300799)),
            ("RFC 3339 string with largest valid offset", "2026-12-02T09:59:00+23:59", ts(EPOCH)),
        ]
        for name, value, want in cases:
            with self.subTest(name):
                self.assertEqual(expires_at_to_timestamp(value), want)

    def test_rejected_forms(self):
        cases = [
            ("naive datetime", datetime(2026, 12, 1, 10, 0)),
            ("string without timezone", "2026-12-01T10:00:00"),
            ("garbage string", "next tuesday"),
            ("date only", "2026-12-01"),
            ("impossible date", "2026-13-45T10:00:00Z"),
            ("offset minutes 60", "2026-12-01T10:00:00+00:60"),
            ("offset hours 24", "2026-12-01T10:00:00+24:00"),
            ("offset without colon", "2026-12-01T10:00:00+0530"),
            ("space instead of T", "2026-12-01 10:00:00Z"),
            ("epoch just below the Timestamp minimum", -62135596801),
            ("epoch just above the Timestamp maximum", 253402300800),
            ("empty string", ""),
            ("bool", True),
            ("NaN", float("nan")),
            ("infinity", float("inf")),
            ("list", [EPOCH]),
            ("dict", {"seconds": EPOCH}),
        ]
        for name, value in cases:
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    expires_at_to_timestamp(value)

    def test_absent_or_none_leaves_field_unset(self):
        for name, data in [("absent", {"access_token": "at"}), ("None", {"access_token": "at", "expires_at": None})]:
            with self.subTest(name):
                token = build_oauth_token(data)
                self.assertFalse(token.HasField("expires_at"))
                self.assertEqual(token.access_token, "at")

    def test_other_oauth_fields_unchanged(self):
        token = build_oauth_token(oauth(expires_at=EPOCH)["oauth_token"])
        self.assertEqual(token.access_token, "at")
        self.assertEqual(token.refresh_token, "rt")
        self.assertEqual(list(token.scopes), ["a", "b"])
        self.assertEqual(token.expires_at, ts(EPOCH))


class TestRequestModels(unittest.TestCase):
    def test_create_and_update_carry_expires_at(self):
        for name, model in [("create", CreateConnectedAccountRequest), ("update", UpdateConnectedAccountRequest)]:
            with self.subTest(name):
                proto = model(connection_name="gmail", identifier="u1",
                              authorization_details=oauth(expires_at="2026-12-01T10:00:00Z")).to_proto()
                token = proto.authorization_details.oauth_token
                self.assertTrue(token.HasField("expires_at"))
                self.assertEqual(token.expires_at, ts(EPOCH))
                self.assertEqual((token.access_token, token.refresh_token, list(token.scopes)), ("at", "rt", ["a", "b"]))

    def test_create_and_update_without_expires_at_are_unchanged(self):
        for name, model in [("create", CreateConnectedAccountRequest), ("update", UpdateConnectedAccountRequest)]:
            with self.subTest(name):
                proto = model(connection_name="gmail", identifier="u1", authorization_details=oauth()).to_proto()
                want = pb.OauthToken(access_token="at", refresh_token="rt", scopes=["a", "b"])
                self.assertEqual(proto.authorization_details.oauth_token, want)
                self.assertFalse(proto.authorization_details.oauth_token.HasField("expires_at"))

    def test_invalid_expires_at_raises_value_error(self):
        for name, model in [("create", CreateConnectedAccountRequest), ("update", UpdateConnectedAccountRequest)]:
            with self.subTest(name):
                req = model(connection_name="gmail", identifier="u1",
                            authorization_details=oauth(expires_at=datetime(2026, 12, 1, 10, 0)))
                with self.assertRaises(ValueError):
                    req.to_proto()

    def test_static_auth_unaffected(self):
        for name, model in [("create", CreateConnectedAccountRequest), ("update", UpdateConnectedAccountRequest)]:
            with self.subTest(name):
                details = {"static_auth": {"api_key": "k", "expires_at": "not-a-timestamp"}}
                proto = model(connection_name="zendesk", identifier="u1", authorization_details=details).to_proto()
                self.assertTrue(proto.authorization_details.HasField("static_auth"))
                self.assertFalse(proto.authorization_details.HasField("oauth_token"))
                self.assertEqual(dict(proto.authorization_details.static_auth.details),
                                 {"api_key": "k", "expires_at": "not-a-timestamp"})


class TestActionsClientSendsExpiresAt(unittest.TestCase):
    """client.actions.* builds the request and hands the proto to the connected-accounts client."""

    def setUp(self):
        self.ca = MagicMock()
        self.ca.create_connected_account.return_value = (pb.CreateConnectedAccountResponse(), None)
        self.ca.update_connected_account.return_value = (pb.UpdateConnectedAccountResponse(), None)
        self.actions = ActionClient(MagicMock(), self.ca)
        self.details = oauth(expires_at=datetime(2026, 12, 1, 10, 0, tzinfo=timezone.utc))

    def sent(self, method):
        return getattr(self.ca, method).call_args.kwargs["connected_account"].authorization_details.oauth_token

    def test_create(self):
        self.actions.create_connected_account(connection_name="gmail", identifier="u1",
                                              authorization_details=self.details)
        self.assertEqual(self.sent("create_connected_account").expires_at, ts(EPOCH))

    def test_update(self):
        self.actions.update_connected_account(connection_name="gmail", identifier="u1",
                                              authorization_details=self.details)
        self.assertEqual(self.sent("update_connected_account").expires_at, ts(EPOCH))

    def test_get_or_create_when_missing_creates_with_expires_at(self):
        self.ca.get_connected_account_by_identifier.side_effect = ScalekitNotFoundException(MagicMock())
        self.actions.get_or_create_connected_account(connection_name="gmail", identifier="u1",
                                                     authorization_details=self.details)
        self.assertEqual(self.sent("create_connected_account").expires_at, ts(EPOCH))


if __name__ == "__main__":
    unittest.main()

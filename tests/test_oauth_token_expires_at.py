"""
OauthToken.expires_at on client.actions create / update / get-or-create connected account.

authorization_details["oauth_token"]["expires_at"] is a timezone-aware datetime, sent as a UTC
google.protobuf.Timestamp (scalekit._convert.datetime_to_timestamp). Absent or None leaves the
field unset; a naive datetime raises ValueError and any other type raises TypeError.

These tests never touch the network: the connected-accounts client is a stub.
"""
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp

from scalekit.actions.actions import ActionClient
from scalekit.actions.models.requests.create_connected_account_request import CreateConnectedAccountRequest
from scalekit.actions.models.requests.oauth_token import build_oauth_token
from scalekit.actions.models.requests.update_connected_account_request import UpdateConnectedAccountRequest
from scalekit.common.exceptions import ScalekitNotFoundException
from scalekit.v1.connected_accounts import connected_accounts_pb2 as pb

# 2026-12-01T10:00:00Z
EPOCH = 1796119200
UTC_INSTANT = datetime(2026, 12, 1, 10, 0, tzinfo=timezone.utc)
IST_INSTANT = datetime(2026, 12, 1, 15, 30, tzinfo=timezone(timedelta(hours=5, minutes=30)))  # same instant
MODELS = [("create", CreateConnectedAccountRequest), ("update", UpdateConnectedAccountRequest)]


def oauth(**extra):
    return {"oauth_token": {"access_token": "at", "refresh_token": "rt", "scopes": ["a", "b"], **extra}}


class TestBuildOauthToken(unittest.TestCase):
    def test_aware_datetime_in_any_zone_is_sent_as_the_same_utc_timestamp(self):
        for name, value in [("UTC", UTC_INSTANT), ("+05:30", IST_INSTANT)]:
            with self.subTest(name):
                token = build_oauth_token(oauth(expires_at=value)["oauth_token"])
                self.assertEqual(token.expires_at, Timestamp(seconds=EPOCH))
        self.assertEqual(build_oauth_token({"expires_at": UTC_INSTANT}).expires_at,
                         build_oauth_token({"expires_at": IST_INSTANT}).expires_at)

    def test_absent_or_none_leaves_field_unset(self):
        for name, data in [("absent", {"access_token": "at"}), ("None", {"access_token": "at", "expires_at": None})]:
            with self.subTest(name):
                token = build_oauth_token(data)
                self.assertFalse(token.HasField("expires_at"))
                self.assertEqual(token.access_token, "at")

    def test_naive_datetime_raises_value_error(self):
        with self.assertRaises(ValueError):
            build_oauth_token({"access_token": "at", "expires_at": datetime(2026, 12, 1, 10, 0)})

    def test_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            build_oauth_token({"access_token": "at", "expires_at": "2026-12-01T10:00:00Z"})

    def test_other_oauth_fields_unchanged(self):
        token = build_oauth_token(oauth(expires_at=UTC_INSTANT)["oauth_token"])
        self.assertEqual((token.access_token, token.refresh_token, list(token.scopes)), ("at", "rt", ["a", "b"]))


class TestRequestModels(unittest.TestCase):
    def test_create_and_update_carry_expires_at(self):
        for name, model in MODELS:
            with self.subTest(name):
                proto = model(connection_name="gmail", identifier="u1",
                              authorization_details=oauth(expires_at=IST_INSTANT)).to_proto()
                token = proto.authorization_details.oauth_token
                self.assertTrue(token.HasField("expires_at"))
                self.assertEqual(token.expires_at, Timestamp(seconds=EPOCH))
                self.assertEqual((token.access_token, token.refresh_token, list(token.scopes)), ("at", "rt", ["a", "b"]))

    def test_create_and_update_without_expires_at_are_unchanged(self):
        for name, model in MODELS:
            with self.subTest(name):
                proto = model(connection_name="gmail", identifier="u1", authorization_details=oauth()).to_proto()
                want = pb.OauthToken(access_token="at", refresh_token="rt", scopes=["a", "b"])
                self.assertEqual(proto.authorization_details.oauth_token, want)
                self.assertFalse(proto.authorization_details.oauth_token.HasField("expires_at"))

    def test_static_auth_unaffected(self):
        for name, model in MODELS:
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
        self.details = oauth(expires_at=UTC_INSTANT)

    def sent(self, method):
        return getattr(self.ca, method).call_args.kwargs["connected_account"].authorization_details.oauth_token

    def test_create(self):
        self.actions.create_connected_account(connection_name="gmail", identifier="u1",
                                              authorization_details=self.details)
        self.assertEqual(self.sent("create_connected_account").expires_at, Timestamp(seconds=EPOCH))

    def test_update(self):
        self.actions.update_connected_account(connection_name="gmail", identifier="u1",
                                              authorization_details=self.details)
        self.assertEqual(self.sent("update_connected_account").expires_at, Timestamp(seconds=EPOCH))

    def test_get_or_create_when_missing_creates_with_expires_at(self):
        self.ca.get_connected_account_by_identifier.side_effect = ScalekitNotFoundException(MagicMock())
        self.actions.get_or_create_connected_account(connection_name="gmail", identifier="u1",
                                                     authorization_details=self.details)
        self.assertEqual(self.sent("create_connected_account").expires_at, Timestamp(seconds=EPOCH))


if __name__ == "__main__":
    unittest.main()

"""Credential-free tests for trigger event verification and parsing.

The JSON bodies under tests/fixtures/trigger_events/ are shared test vectors. The
tests sign each fixture at runtime with a fixed test secret and a fresh timestamp.
"""

import base64
import binascii
import hashlib
import hmac
import json
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

import scalekit
from scalekit import (
    DeliveryScope,
    DetectionMode,
    PayloadState,
    ScalekitClient,
    TriggerEvent,
    verify_trigger_event,
)
from scalekit.actions import ActionClient
from scalekit.common.exceptions import (
    ScalekitException,
    ScalekitTriggerEventParseException,
    WebhookVerificationError,
)

FIXTURES = Path(__file__).parent / "fixtures" / "trigger_events"
# Test-only secret: base64 of b"scalekit-trigger-test-secret-32b".
SECRET = "whsec_" + base64.b64encode(b"scalekit-trigger-test-secret-32b").decode()
MALFORMED_SECRET = "whsec_" + "abc"  # base64 with bad padding
NO_PREFIX_SECRET = "no" + "underscore"
OTHER_SECRET = "whsec_" + base64.b64encode(b"a-different-test-secret-32bytes!").decode()
MSG_ID = "msg_2abc"


def load(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def sign(
    body: bytes | str, *, secret: str = SECRET, msg_id: str = MSG_ID, timestamp: int | None = None
) -> dict:
    ts = int(time.time()) if timestamp is None else timestamp
    text = body.decode("utf-8") if isinstance(body, bytes) else body
    key = base64.b64decode(secret.split("_")[1])
    digest = hmac.new(key, f"{msg_id}.{ts}.{text}".encode(), hashlib.sha256).digest()
    return {
        "webhook-id": msg_id,
        "webhook-timestamp": str(ts),
        "webhook-signature": "v1," + base64.b64encode(digest).decode(),
    }


def verify(body: bytes | str, headers: dict | None = None) -> TriggerEvent:
    return verify_trigger_event(
        body, headers=sign(body) if headers is None else headers, secret=SECRET
    )


class CaseInsensitiveHeaders:
    """Mimics Flask/Werkzeug and Django headers: case-insensitive get(), Title-Case items()."""

    def __init__(self, data: dict):
        self._data = {k.title(): v for k, v in data.items()}

    def get(self, key, default=None):
        for k, v in self._data.items():
            if k.lower() == key.lower():
                return v
        return default

    def items(self):
        return self._data.items()


class TestParse(unittest.TestCase):
    def test_valid_account_scope(self):
        event = verify(load("valid_account.json"))
        self.assertIsInstance(event, TriggerEvent)
        self.assertEqual(event.version, "1")
        self.assertEqual(event.trigger_type, "example.item.created")
        self.assertEqual(event.subscription_id, "sub_123")
        self.assertIs(event.delivery_scope, DeliveryScope.ACCOUNT)
        self.assertEqual(event.delivery_scope, "account")
        self.assertEqual(event.connection_id, "conn_123")
        self.assertEqual(event.connected_account_id, "ca_123")
        self.assertEqual(event.resource_type, "message")
        self.assertEqual(event.resource_id, "msg_123")
        # 12:30:45.123+05:30 normalised to aware UTC.
        self.assertEqual(
            event.occurred_at, datetime(2026, 10, 1, 7, 0, 45, 123000, tzinfo=timezone.utc)
        )
        self.assertEqual(event.occurred_at.utcoffset().total_seconds(), 0)
        self.assertIs(event.detection_mode, DetectionMode.WEBHOOK)
        self.assertIs(event.payload_state, PayloadState.FULL)
        self.assertEqual(
            event.payload,
            {"subject": "Hello", "labels": ["INBOX", "UNREAD"], "size": 42, "starred": False},
        )
        self.assertEqual(event.dedupe_key, "dk_123")
        self.assertEqual(event.correlation_id, "corr_123")
        self.assertEqual(event.model_extra, {})

    def test_valid_connection_scope_empty_account(self):
        event = verify(load("valid_connection_empty_account.json"))
        self.assertIs(event.delivery_scope, DeliveryScope.CONNECTION)
        self.assertEqual(event.connected_account_id, "")
        self.assertEqual(event.resource_id, "")  # "" stays "", not None
        self.assertIs(event.detection_mode, DetectionMode.POLL)
        self.assertEqual(event.occurred_at, datetime(2026, 10, 1, 7, 0, 45, tzinfo=timezone.utc))

    def test_extra_fields_are_kept(self):
        event = verify(load("extra_field.json"))
        self.assertEqual(event.model_extra["delivery_attempt"], 2)
        self.assertEqual(event.model_extra["metadata"], {"region": "test", "tags": ["a", "b"]})
        self.assertEqual(event.dedupe_key, "dk_123")

    def test_unknown_enum_values_pass_through(self):
        event = verify(load("unknown_enum.json"))
        for value, expected in (
            (event.delivery_scope, "organization"),
            (event.detection_mode, "stream"),
            (event.payload_state, "partial"),
        ):
            self.assertEqual(value, expected)
            self.assertIs(type(value), str)

    def test_null_payload_reference(self):
        event = verify(load("null_payload_reference.json"))
        self.assertIs(event.payload_state, PayloadState.REFERENCE)
        self.assertIsNone(event.payload)
        self.assertIsNone(event.occurred_at)

    def test_absent_optional_fields_default_to_none(self):
        data = json.loads(load("valid_account.json"))
        for key in ("payload", "resource_id", "occurred_at"):
            del data[key]
        event = verify(json.dumps(data))
        self.assertIsNone(event.payload)
        self.assertIsNone(event.resource_id)
        self.assertIsNone(event.occurred_at)

    def test_null_resource_id_and_empty_occurred_at_are_none(self):
        data = json.loads(load("valid_account.json"))
        data["resource_id"] = None
        data["occurred_at"] = ""
        event = verify(json.dumps(data))
        self.assertIsNone(event.resource_id)
        self.assertIsNone(event.occurred_at)

    def test_empty_required_strings_are_allowed(self):
        data = json.loads(load("valid_account.json"))
        data["version"] = ""
        data["correlation_id"] = ""
        event = verify(json.dumps(data))
        self.assertEqual(event.version, "")
        self.assertEqual(event.correlation_id, "")

    def test_unpinned_version(self):
        data = json.loads(load("valid_account.json"))
        data["version"] = "2"
        self.assertEqual(verify(json.dumps(data)).version, "2")

    def test_missing_required_field(self):
        with self.assertRaises(ScalekitTriggerEventParseException) as ctx:
            verify(load("missing_required.json"))
        self.assertIn("'dedupe_key' is required", str(ctx.exception))
        self.assertIsInstance(ctx.exception, WebhookVerificationError)
        self.assertIsInstance(ctx.exception.__cause__, ValidationError)

    def test_wrong_type(self):
        with self.assertRaises(ScalekitTriggerEventParseException) as ctx:
            verify(load("wrong_type.json"))
        self.assertIn("'version'", str(ctx.exception))
        self.assertIsInstance(ctx.exception, WebhookVerificationError)
        self.assertIsNotNone(ctx.exception.__cause__)

    def test_required_field_null_is_wrong_type(self):
        data = json.loads(load("valid_account.json"))
        data["subscription_id"] = None
        with self.assertRaises(ScalekitTriggerEventParseException):
            verify(json.dumps(data))

    def test_wrong_type_enum_field(self):
        data = json.loads(load("valid_account.json"))
        data["delivery_scope"] = 1
        with self.assertRaises(ScalekitTriggerEventParseException) as ctx:
            verify(json.dumps(data))
        self.assertIn("'delivery_scope'", str(ctx.exception))

    def test_wrong_type_resource_id(self):
        data = json.loads(load("valid_account.json"))
        data["resource_id"] = 123
        with self.assertRaises(ScalekitTriggerEventParseException):
            verify(json.dumps(data))

    def test_bad_timestamp_without_offset(self):
        with self.assertRaises(ScalekitTriggerEventParseException) as ctx:
            verify(load("bad_timestamp.json"))
        self.assertIn("occurred_at", str(ctx.exception))

    def test_occurred_at_rejects_other_shapes(self):
        for bad in (
            1727766045,
            1727766045.5,
            "2026-10-01",
            "2026-10-01 07:00:45Z",
            "2026-13-01T07:00:45Z",
            "2026-10-01T07:00:45+24:00",
            "yesterday",
            "\uff12\uff10\uff12\uff16-10-01T07:00:45Z",  # full-width digits
            True,
            {"seconds": 1},
        ):
            data = json.loads(load("valid_account.json"))
            data["occurred_at"] = bad
            with (
                self.subTest(occurred_at=bad),
                self.assertRaises(ScalekitTriggerEventParseException),
            ):
                verify(json.dumps(data))

    def test_occurred_at_accepts_rfc3339_variants(self):
        cases = {
            "2026-10-01T07:00:45Z": datetime(2026, 10, 1, 7, 0, 45, tzinfo=timezone.utc),
            "2026-10-01t07:00:45z": datetime(2026, 10, 1, 7, 0, 45, tzinfo=timezone.utc),
            "2026-10-01T02:00:45.5-05:00": datetime(
                2026, 10, 1, 7, 0, 45, 500000, tzinfo=timezone.utc
            ),
            "2026-10-01T07:00:45.123456789+00:00": datetime(
                2026, 10, 1, 7, 0, 45, 123456, tzinfo=timezone.utc
            ),
        }
        for raw, expected in cases.items():
            data = json.loads(load("valid_account.json"))
            data["occurred_at"] = raw
            with self.subTest(occurred_at=raw):
                parsed = verify(json.dumps(data)).occurred_at
                self.assertEqual(parsed, expected)
                self.assertEqual(parsed.tzinfo, timezone.utc)

    def test_body_not_json(self):
        with self.assertRaises(ScalekitTriggerEventParseException) as ctx:
            verify(b"not json")
        self.assertIsInstance(ctx.exception.__cause__, ValueError)

    def test_body_json_but_not_object(self):
        for body in (b"[]", b'"x"', b"null", b"42"):
            with self.subTest(body=body), self.assertRaises(ScalekitTriggerEventParseException):
                verify(body)

    def test_nan_literal_rejected(self):
        data = load("valid_account.json").replace(b'"size": 42', b'"size": NaN')
        with self.assertRaises(ScalekitTriggerEventParseException):
            verify(data)

    def test_error_messages_never_contain_body_or_secret(self):
        data = json.loads(load("valid_account.json"))
        data["version"] = 1
        data["payload"] = {"canary": "BODY-CANARY-123"}
        with self.assertRaises(ScalekitTriggerEventParseException) as ctx:
            verify(json.dumps(data))
        for exc in (ctx.exception, ctx.exception.__cause__):
            self.assertNotIn("BODY-CANARY-123", str(exc))
            self.assertNotIn(SECRET, str(exc))
            self.assertNotIn(SECRET.split("_")[1], str(exc))

    def test_model_is_frozen(self):
        event = verify(load("valid_account.json"))
        with self.assertRaises(ValidationError):
            event.dedupe_key = "other"

    def test_str_body_equals_bytes_body(self):
        raw = load("valid_account.json")
        self.assertEqual(verify(raw), verify(raw.decode("utf-8")))


class TestSignature(unittest.TestCase):
    def test_bad_signature(self):
        body = load("valid_account.json")
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event(body, headers=sign(body, secret=OTHER_SECRET), secret=SECRET)
        self.assertNotIsInstance(ctx.exception, ScalekitTriggerEventParseException)

    def test_tampered_body(self):
        body = load("valid_account.json")
        headers = sign(body)
        with self.assertRaises(WebhookVerificationError):
            verify_trigger_event(body.replace(b"dk_123", b"dk_999"), headers=headers, secret=SECRET)

    def test_signature_checked_before_parsing(self):
        # An unsigned invalid body must fail verification, not parsing.
        body = load("missing_required.json")
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event(body, headers=sign(body, secret=OTHER_SECRET), secret=SECRET)
        self.assertNotIsInstance(ctx.exception, ScalekitTriggerEventParseException)

    def test_stale_timestamp(self):
        body = load("valid_account.json")
        headers = sign(body, timestamp=int(time.time()) - 6 * 60)
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event(body, headers=headers, secret=SECRET)
        self.assertEqual(str(ctx.exception), "Message timestamp too old")

    def test_future_timestamp(self):
        body = load("valid_account.json")
        headers = sign(body, timestamp=int(time.time()) + 6 * 60)
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event(body, headers=headers, secret=SECRET)
        self.assertEqual(str(ctx.exception), "Message timestamp too new")

    def test_timestamp_within_tolerance(self):
        body = load("valid_account.json")
        headers = sign(body, timestamp=int(time.time()) - 4 * 60)
        self.assertEqual(
            verify_trigger_event(body, headers=headers, secret=SECRET).dedupe_key, "dk_123"
        )

    def test_missing_headers(self):
        body = load("valid_account.json")
        for missing in ("webhook-id", "webhook-timestamp", "webhook-signature"):
            headers = sign(body)
            del headers[missing]
            with self.subTest(missing=missing), self.assertRaises(WebhookVerificationError):
                verify_trigger_event(body, headers=headers, secret=SECRET)
        with self.assertRaises(WebhookVerificationError):
            verify_trigger_event(body, headers={}, secret=SECRET)

    def test_mixed_case_headers_plain_dict(self):
        body = load("valid_account.json")
        headers = {k.title(): v for k, v in sign(body).items()}  # "Webhook-Id", ...
        headers["WEBHOOK-SIGNATURE"] = headers.pop("Webhook-Signature")
        event = verify_trigger_event(body, headers=headers, secret=SECRET)
        self.assertEqual(event.dedupe_key, "dk_123")

    def test_framework_style_headers(self):
        body = load("valid_account.json")
        headers = CaseInsensitiveHeaders(sign(body))
        self.assertEqual(
            verify_trigger_event(body, headers=headers, secret=SECRET).dedupe_key, "dk_123"
        )

    def test_multiple_signatures_one_valid(self):
        body = load("valid_account.json")
        headers = sign(body)
        wrong = sign(body, secret=OTHER_SECRET)["webhook-signature"]
        headers["webhook-signature"] = f"{wrong} v2,abcd {headers['webhook-signature']}"
        self.assertEqual(verify_trigger_event(body, headers=headers, secret=SECRET).version, "1")

    def test_invalid_utf8_body(self):
        body = b'{"version": "\xff"}'
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event(body, headers=sign(b"{}"), secret=SECRET)
        self.assertIsInstance(ctx.exception.__cause__, UnicodeDecodeError)
        self.assertNotIsInstance(ctx.exception, ScalekitTriggerEventParseException)

    def test_lone_surrogate_str_body(self):
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event('{"a": "\ud800"}', headers=sign("{}"), secret=SECRET)
        self.assertIsInstance(ctx.exception.__cause__, UnicodeEncodeError)

    def test_malformed_secret_is_wrapped(self):
        body = load("valid_account.json")
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event(body, headers=sign(body), secret=MALFORMED_SECRET)
        self.assertIsInstance(ctx.exception.__cause__, binascii.Error)
        self.assertNotIn(MALFORMED_SECRET, str(ctx.exception))

    def test_malformed_signature_header_is_wrapped(self):
        body = load("valid_account.json")
        headers = sign(body)
        headers["webhook-signature"] = "v1,abc"
        with self.assertRaises(WebhookVerificationError) as ctx:
            verify_trigger_event(body, headers=headers, secret=SECRET)
        self.assertIsInstance(ctx.exception.__cause__, binascii.Error)

    def test_secret_without_prefix(self):
        body = load("valid_account.json")
        with self.assertRaises(WebhookVerificationError):
            verify_trigger_event(body, headers=sign(body), secret=NO_PREFIX_SECRET)

    def test_wrong_argument_types_raise_type_error(self):
        body = load("valid_account.json")
        with self.assertRaises(TypeError):
            verify_trigger_event(json.loads(body), headers=sign(body), secret=SECRET)
        with self.assertRaises(TypeError):
            verify_trigger_event(body, headers=sign(body), secret=None)
        headers = sign(body)
        headers["webhook-id"] = ["msg_2abc"]
        with self.assertRaises(TypeError):
            verify_trigger_event(body, headers=headers, secret=SECRET)

    def test_body_is_positional_only_and_options_keyword_only(self):
        body = load("valid_account.json")
        with self.assertRaises(TypeError):
            verify_trigger_event(body=body, headers=sign(body), secret=SECRET)
        with self.assertRaises(TypeError):
            verify_trigger_event(body, sign(body), SECRET)


class TestClientEntryPoint(unittest.TestCase):
    def setUp(self):
        self.actions = ActionClient(tools_client=None, connected_accounts_client=None)

    def test_client_method_matches_standalone(self):
        for name in (
            "valid_account.json",
            "valid_connection_empty_account.json",
            "extra_field.json",
            "unknown_enum.json",
            "null_payload_reference.json",
        ):
            body = load(name)
            headers = sign(body)
            with self.subTest(fixture=name):
                self.assertEqual(
                    self.actions.triggers.verify_event(body, headers=headers, secret=SECRET),
                    verify_trigger_event(body, headers=headers, secret=SECRET),
                )

    def test_client_method_raises_same_errors(self):
        for name in ("missing_required.json", "wrong_type.json", "bad_timestamp.json"):
            body = load(name)
            with self.subTest(fixture=name), self.assertRaises(ScalekitTriggerEventParseException):
                self.actions.triggers.verify_event(body, headers=sign(body), secret=SECRET)
        body = load("valid_account.json")
        with self.assertRaises(WebhookVerificationError):
            self.actions.triggers.verify_event(body, headers={}, secret=SECRET)

    def test_triggers_namespace_is_cached(self):
        self.assertIs(self.actions.triggers, self.actions.triggers)

    def test_exports(self):
        self.assertIn("verify_trigger_event", scalekit.__all__)
        self.assertIn("TriggerEvent", scalekit.__all__)
        self.assertTrue(issubclass(ScalekitTriggerEventParseException, WebhookVerificationError))
        self.assertTrue(issubclass(ScalekitTriggerEventParseException, ScalekitException))


class TestModelDirectConstruction(unittest.TestCase):
    def _fields(self):
        return json.loads(load("valid_account.json"))

    def test_naive_datetime_rejected(self):
        fields = self._fields()
        fields["occurred_at"] = datetime(2026, 10, 1, 7, 0, 45)  # noqa: DTZ001
        with self.assertRaises(ValidationError):
            TriggerEvent(**fields)

    def test_aware_datetime_normalised(self):
        fields = self._fields()
        fields["occurred_at"] = datetime.fromisoformat("2026-10-01T12:30:45+05:30")
        event = TriggerEvent(**fields)
        self.assertEqual(event.occurred_at, datetime(2026, 10, 1, 7, 0, 45, tzinfo=timezone.utc))
        self.assertIs(event.occurred_at.tzinfo, timezone.utc)

    def test_enum_member_accepted(self):
        fields = self._fields()
        fields["delivery_scope"] = DeliveryScope.CONNECTION
        self.assertIs(TriggerEvent(**fields).delivery_scope, DeliveryScope.CONNECTION)


class TestExistingWebhookVerifiersUnchanged(unittest.TestCase):
    """Regression: verify_webhook_payload / verify_interceptor_payload behave as before."""

    def setUp(self):
        # The verifiers use no client state; skip __init__ (it authenticates over the network).
        self.client = ScalekitClient.__new__(ScalekitClient)
        self.body = load("valid_account.json")

    def test_valid_bytes_and_str(self):
        headers = sign(self.body)
        self.assertIs(self.client.verify_webhook_payload(SECRET, headers, self.body), True)
        self.assertIs(self.client.verify_webhook_payload(SECRET, headers, self.body.decode()), True)

    def test_invalid_signature_message(self):
        headers = sign(self.body, secret=OTHER_SECRET)
        with self.assertRaises(WebhookVerificationError) as ctx:
            self.client.verify_webhook_payload(SECRET, headers, self.body)
        self.assertEqual(str(ctx.exception), "Invalid signature")

    def test_header_lookup_is_case_sensitive(self):
        headers = {k.title(): v for k, v in sign(self.body).items()}
        with self.assertRaises(WebhookVerificationError) as ctx:
            self.client.verify_webhook_payload(SECRET, headers, self.body)
        self.assertEqual(str(ctx.exception), "Missing required headers")

    def test_stale_and_future_timestamp_messages(self):
        for offset, message in (
            (-6 * 60, "Message timestamp too old"),
            (6 * 60, "Message timestamp too new"),
        ):
            headers = sign(self.body, timestamp=int(time.time()) + offset)
            with self.subTest(offset=offset), self.assertRaises(WebhookVerificationError) as ctx:
                self.client.verify_webhook_payload(SECRET, headers, self.body)
            self.assertEqual(str(ctx.exception), message)

    def test_non_numeric_timestamp_message(self):
        headers = sign(self.body)
        headers["webhook-timestamp"] = "not-a-number"
        with self.assertRaises(WebhookVerificationError) as ctx:
            self.client.verify_webhook_payload(SECRET, headers, self.body)
        self.assertEqual(str(ctx.exception), "Invalid Signature Headers")

    def test_float_timestamp_is_accepted(self):
        ts = int(time.time())
        headers = sign(self.body, timestamp=ts)
        headers["webhook-timestamp"] = f"{ts}.9"  # parsed as float, signed over floor()
        self.assertIs(self.client.verify_webhook_payload(SECRET, headers, self.body), True)

    def test_malformed_secret_raises_raw_binascii_error(self):
        with self.assertRaises(binascii.Error) as ctx:
            self.client.verify_webhook_payload(MALFORMED_SECRET, sign(self.body), self.body)
        self.assertNotIsInstance(ctx.exception, WebhookVerificationError)

    def test_secret_without_underscore(self):
        with self.assertRaises(WebhookVerificationError) as ctx:
            self.client.verify_webhook_payload(NO_PREFIX_SECRET, sign(self.body), self.body)
        self.assertEqual(str(ctx.exception), "Invalid secret")

    def test_empty_header_counts_as_missing(self):
        headers = sign(self.body)
        headers["webhook-id"] = ""
        with self.assertRaises(WebhookVerificationError) as ctx:
            self.client.verify_webhook_payload(SECRET, headers, self.body)
        self.assertEqual(str(ctx.exception), "Missing required headers")

    def test_interceptor_headers_and_fallback(self):
        signed = sign(self.body)
        interceptor = {
            "interceptor-id": signed["webhook-id"],
            "interceptor-timestamp": signed["webhook-timestamp"],
            "interceptor-signature": signed["webhook-signature"],
        }
        self.assertIs(self.client.verify_interceptor_payload(SECRET, interceptor, self.body), True)
        self.assertIs(self.client.verify_interceptor_payload(SECRET, signed, self.body), True)
        with self.assertRaises(WebhookVerificationError) as ctx:
            self.client.verify_interceptor_payload(OTHER_SECRET, interceptor, self.body)
        self.assertEqual(str(ctx.exception), "Invalid signature")

    def test_does_not_parse_body(self):
        # The legacy verifiers only check the signature; any signed body is accepted.
        body = b"not json at all"
        self.assertIs(self.client.verify_webhook_payload(SECRET, sign(body), body), True)


if __name__ == "__main__":
    unittest.main()

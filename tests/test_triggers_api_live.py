"""Live negative tests for client.actions.triggers against a Scalekit environment.

Skipped unless these are set (tests/.env is loaded like BaseTest does):
  SCALEKIT_ENVIRONMENT_URL (or SCALEKIT_ENV_URL), SCALEKIT_CLIENT_ID, SCALEKIT_CLIENT_SECRET

Nothing else is needed. Every case sends IDs that name nothing, or arguments the server
refuses, so no test creates, changes or delivers anything in the environment.

- Arguments the server refuses on their own (a batch that is too long, a signing secret that
  is too short, a usage range and a period together) are refused whether or not triggers are
  enabled for the environment, so those cases always run.
- An environment without triggers answers every other call with 404 ``RESOURCE_NOT_FOUND``
  ("not found"). One case checks exactly that and runs only there; the cases that need
  triggers enabled skip there.

Positive behaviour (subscriptions, signing secrets, deliveries) needs connections and a
delivery endpoint to exist, so it is covered offline in test_triggers_api.py.
"""

import os
import unittest
from datetime import date, datetime, timedelta, timezone

from scalekit import ScalekitClient
from scalekit.actions import TriggerSubscriptionDeleteOutcome
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitNotFoundException,
)

try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:  # pragma: no cover - dotenv is a dev dependency
    pass

# Well formed, and outside the range of IDs any environment issues.
UNKNOWN_CONNECTION = "conn_912345678901234567"
UNKNOWN_ACCOUNT = "ca_912345678901234567"
UNKNOWN_SUBSCRIPTION = "trgs_912345678901234567"
UNKNOWN_ENDPOINT = "ep_sdklivetestunknown"


def _env(name):
    return os.environ.get(name) or None


class TestTriggersApiLiveNegative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env_url = _env("SCALEKIT_ENVIRONMENT_URL") or _env("SCALEKIT_ENV_URL")
        client_id = _env("SCALEKIT_CLIENT_ID")
        client_secret = _env("SCALEKIT_CLIENT_SECRET")
        missing = [
            name
            for name, value in (
                ("SCALEKIT_ENVIRONMENT_URL (or SCALEKIT_ENV_URL)", env_url),
                ("SCALEKIT_CLIENT_ID", client_id),
                ("SCALEKIT_CLIENT_SECRET", client_secret),
            )
            if not value
        ]
        if missing:
            raise unittest.SkipTest(f"live trigger tests need {', '.join(missing)}")
        cls.client = ScalekitClient(env_url, client_id, client_secret)
        # get_activity takes no IDs, so a 404 RESOURCE_NOT_FOUND from it can only mean
        # triggers are not enabled for the environment. Any other error fails the setup.
        try:
            cls.client.actions.triggers.get_activity()
            cls.enabled = True
        except ScalekitNotFoundException as exc:
            if exc.error_code != "RESOURCE_NOT_FOUND":
                raise
            cls.enabled = False

    def _needs_triggers(self):
        if not self.enabled:
            self.skipTest("triggers are not enabled for this environment")

    def assert_refused(self, exception_class, error_code, call, message=None):
        """``call`` raises ``exception_class`` with ``error_code`` (and ``message`` in its text)."""
        with self.assertRaises(exception_class) as ctx:
            call()
        self.assertEqual(ctx.exception.error_code, error_code, ctx.exception.message)
        if message is not None:
            self.assertIn(message, ctx.exception.message)
        return ctx.exception

    # Triggers not enabled for the environment

    def test_environment_without_triggers_answers_not_found(self):
        if self.enabled:
            self.skipTest("triggers are enabled for this environment")
        triggers = self.client.actions.triggers
        for name, call in (
            ("get_activity", triggers.get_activity),
            ("get_usage", lambda: triggers.get_usage(period="24h")),
            ("list_available", lambda: triggers.list_available(UNKNOWN_CONNECTION)),
            ("lookup_delivery", lambda: triggers.lookup_delivery("msg_sdklivetestunknown")),
        ):
            with self.subTest(name):
                exc = self.assert_refused(ScalekitNotFoundException, "RESOURCE_NOT_FOUND", call)
                self.assertEqual(exc.http_status, 404)
                # "connection not found" would mean triggers are enabled after all.
                self.assertNotIn("connection", exc.message)

    # Arguments refused before triggers are looked at (run in every environment)

    def test_batch_create_with_more_than_100_accounts_is_refused(self):
        exc = self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.batch_create_subscriptions(
                UNKNOWN_CONNECTION,
                "example.item.created",
                connected_account_ids=[f"ca_{i}" for i in range(1, 102)],
            ),
        )
        self.assertEqual(exc.http_status, 400)

    def test_batch_create_with_a_repeated_account_is_refused(self):
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.batch_create_subscriptions(
                UNKNOWN_CONNECTION,
                "example.item.created",
                connected_account_ids=[UNKNOWN_ACCOUNT, UNKNOWN_ACCOUNT],
            ),
        )

    def test_get_usage_with_a_period_and_a_range_is_refused(self):
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.get_usage(
                period="7d", from_date="2026-10-01", to_date="2026-10-02"
            ),
        )

    def test_get_usage_without_a_period_or_range_is_refused(self):
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.get_usage(),
        )

    def test_get_usage_with_an_unsupported_period_is_refused(self):
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.get_usage(period="1d"),
        )

    def test_signing_secret_shorter_than_8_characters_is_refused(self):
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.set_signing_secret(
                UNKNOWN_CONNECTION, signing_secret="abc"
            ),
        )

    def test_malformed_message_id_is_refused(self):
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.list_delivery_attempts_by_message(
                UNKNOWN_ENDPOINT, "not-a-message-id"
            ),
        )

    def test_batch_lookup_of_more_than_25_ids_is_refused(self):
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.batch_lookup_deliveries(
                [f"msg_sdklivetest{i}" for i in range(26)]
            ),
        )

    # Unknown or malformed IDs (need triggers enabled)

    def test_unknown_connection_is_not_found(self):
        self._needs_triggers()
        triggers = self.client.actions.triggers
        for name, call in (
            ("list_available", lambda: triggers.list_available(UNKNOWN_CONNECTION)),
            (
                "list_eligible_accounts",
                lambda: triggers.list_eligible_accounts(UNKNOWN_CONNECTION, "example.item.created"),
            ),
            ("list_subscriptions", lambda: triggers.list_subscriptions(UNKNOWN_CONNECTION)),
            (
                "create_subscription",
                lambda: triggers.create_subscription(
                    UNKNOWN_CONNECTION,
                    "example.item.created",
                    connected_account_id=UNKNOWN_ACCOUNT,
                ),
            ),
            (
                "batch_create_subscriptions",
                lambda: triggers.batch_create_subscriptions(
                    UNKNOWN_CONNECTION,
                    "example.item.created",
                    connected_account_ids=[UNKNOWN_ACCOUNT],
                ),
            ),
            ("get_ingress_endpoint", lambda: triggers.get_ingress_endpoint(UNKNOWN_CONNECTION)),
            (
                "create_ingress_endpoint",
                lambda: triggers.create_ingress_endpoint(UNKNOWN_CONNECTION),
            ),
            (
                "set_signing_secret",
                lambda: triggers.set_signing_secret(
                    UNKNOWN_CONNECTION, signing_secret="sdk-live-test-secret"
                ),
            ),
            (
                "confirm_signing_secret_rotation",
                lambda: triggers.confirm_signing_secret_rotation(UNKNOWN_CONNECTION),
            ),
            (
                "generate_signing_secret",
                lambda: triggers.generate_signing_secret(UNKNOWN_CONNECTION),
            ),
        ):
            with self.subTest(name):
                exc = self.assert_refused(
                    ScalekitNotFoundException,
                    "RESOURCE_NOT_FOUND",
                    call,
                    message="connection not found",
                )
                self.assertEqual(exc.http_status, 404)

    def test_malformed_connection_id_is_refused(self):
        self._needs_triggers()
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.list_available("conn_not-a-number"),
            message="invalid connection_id",
        )

    def test_delete_unknown_subscription_is_not_found(self):
        self._needs_triggers()
        self.assert_refused(
            ScalekitNotFoundException,
            "RESOURCE_NOT_FOUND",
            lambda: self.client.actions.triggers.delete_subscription(
                UNKNOWN_CONNECTION, UNKNOWN_SUBSCRIPTION
            ),
            message="trigger subscription not found",
        )

    def test_delete_malformed_subscription_id_is_refused(self):
        self._needs_triggers()
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.delete_subscription(
                UNKNOWN_CONNECTION, "trgs_not-a-number"
            ),
            message="invalid subscription_id",
        )

    def test_batch_delete_reports_unknown_subscriptions_per_item(self):
        self._needs_triggers()
        batch = self.client.actions.triggers.batch_delete_subscriptions(
            UNKNOWN_CONNECTION, subscription_ids=[UNKNOWN_SUBSCRIPTION]
        )
        self.assertEqual(batch.deleted_count, 0)
        self.assertEqual(len(batch.results), 1)
        self.assertEqual(batch.results[0].subscription_id, UNKNOWN_SUBSCRIPTION)
        self.assertEqual(batch.results[0].outcome, TriggerSubscriptionDeleteOutcome.NOT_FOUND)

    def test_batch_delete_needs_exactly_one_selector(self):
        self._needs_triggers()
        triggers = self.client.actions.triggers
        for name, call in (
            (
                "both",
                lambda: triggers.batch_delete_subscriptions(
                    UNKNOWN_CONNECTION,
                    subscription_ids=[UNKNOWN_SUBSCRIPTION],
                    trigger_name="example.item.created",
                ),
            ),
            ("neither", lambda: triggers.batch_delete_subscriptions(UNKNOWN_CONNECTION)),
        ):
            with self.subTest(name):
                self.assert_refused(
                    ScalekitBadRequestException, "INVALID_ARGUMENT", call, message="selector"
                )

    def test_get_usage_with_from_after_to_is_refused(self):
        self._needs_triggers()
        today = datetime.now(timezone.utc).date()
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.get_usage(
                from_date=today - timedelta(days=1), to_date=today - timedelta(days=5)
            ),
        )

    def test_get_usage_starting_in_the_future_is_refused(self):
        self._needs_triggers()
        today = datetime.now(timezone.utc).date()
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.get_usage(
                from_date=today + timedelta(days=3), to_date=today + timedelta(days=4)
            ),
        )

    def test_list_deliveries_refuses_bad_filters(self):
        # Checked before the delivery endpoint is looked up, so the endpoint need not exist.
        self._needs_triggers()
        triggers = self.client.actions.triggers
        now = datetime.now(timezone.utc)
        for name, call in (
            (
                "after later than before",
                lambda: triggers.list_deliveries(
                    UNKNOWN_ENDPOINT, after=now, before=now - timedelta(hours=1)
                ),
            ),
            (
                "malformed page_token",
                lambda: triggers.list_deliveries(UNKNOWN_ENDPOINT, page_token="not-a-token"),
            ),
            (
                "channel that is not a connection or subscription",
                lambda: triggers.list_deliveries(UNKNOWN_ENDPOINT, channel="slack"),
            ),
        ):
            with self.subTest(name):
                self.assert_refused(ScalekitBadRequestException, "INVALID_ARGUMENT", call)

    def test_lookup_by_attempt_id_is_refused(self):
        self._needs_triggers()
        triggers = self.client.actions.triggers
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: triggers.lookup_delivery("atmpt_sdklivetest"),
            message="attempt ids are not accepted",
        )
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: triggers.batch_lookup_deliveries(["atmpt_sdklivetest"]),
            message="attempt ids are not accepted",
        )

    def test_batch_resend_with_a_repeated_target_is_refused(self):
        self._needs_triggers()
        target = {"msg_id": "msg_sdklivetest", "endpoint_id": UNKNOWN_ENDPOINT}
        self.assert_refused(
            ScalekitBadRequestException,
            "INVALID_ARGUMENT",
            lambda: self.client.actions.triggers.batch_resend_deliveries([target, dict(target)]),
            message="duplicate target",
        )

    def test_recover_deliveries_refuses_a_bad_window(self):
        # The window is checked before the delivery endpoint is looked up.
        self._needs_triggers()
        triggers = self.client.actions.triggers
        now = datetime.now(timezone.utc)
        for name, call in (
            (
                "since in the future",
                lambda: triggers.recover_deliveries(UNKNOWN_ENDPOINT, since=now + timedelta(hours=1)),
            ),
            (
                "until before since",
                lambda: triggers.recover_deliveries(
                    UNKNOWN_ENDPOINT,
                    since=now - timedelta(hours=1),
                    until=now - timedelta(hours=2),
                ),
            ),
            (
                "longer than 14 days",
                lambda: triggers.recover_deliveries(UNKNOWN_ENDPOINT, since=now - timedelta(days=15)),
            ),
        ):
            with self.subTest(name):
                self.assert_refused(ScalekitBadRequestException, "INVALID_ARGUMENT", call)


if __name__ == "__main__":
    unittest.main()

"""Live tests for client.actions.triggers against a Scalekit environment.

Skipped unless these are set (tests/.env is loaded like BaseTest does):
  SCALEKIT_ENVIRONMENT_URL (or SCALEKIT_ENV_URL), SCALEKIT_CLIENT_ID, SCALEKIT_CLIENT_SECRET
and also skipped when triggers are not available for that environment (checked once).

Optional fixtures; each case that needs one is skipped when it is missing:
  SCALEKIT_TEST_TRIGGER_CONNECTION_ID       a connection that offers a webhook trigger whose
                                            provider signs its own events (no webhook trigger
                                            has provides_bearer_secret); the secret-generation
                                            case skips otherwise, so it never replaces the
                                            fixture's secret
  SCALEKIT_TEST_TRIGGER_POLL_CONNECTION_ID  a connection that offers a poll trigger
  SCALEKIT_TEST_TRIGGER_POLL_ACCOUNT_ID     a connected account (ca_...) on that connection
  SCALEKIT_TEST_TRIGGER_POLL_TRIGGER        the poll trigger name (default: the first usable one)
  SCALEKIT_TEST_TRIGGER_POLL_CONFIG         JSON object of config values for that trigger
  SCALEKIT_TEST_TRIGGER_ENDPOINT_ID         a delivery endpoint (ep_...)

Every subscription a test creates is deleted afterwards, even when the test fails.

Not run live, on purpose: set_signing_secret, confirm_signing_secret_rotation,
batch_resend_deliveries and recover_deliveries. The first two change the signing secret
of the shared fixture connection (a rotation that is not finished leaves the provider's
events failing verification for everyone using it); the last two make real redelivery
attempts to the fixture endpoint. Their request mapping, retry policy and error mapping
are covered offline in test_triggers_api.py.
"""

import contextlib
import json
import os
import secrets
import string
import unittest
from datetime import timedelta
from urllib.parse import urlsplit

from scalekit import ScalekitClient
from scalekit.actions import (
    DetectionMode,
    TriggerDeliveryLookupOutcome,
    TriggerSubscribeOutcome,
    TriggerSubscription,
    TriggerSubscriptionDeleteOutcome,
    TriggerUsageBucket,
)
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitConflictException,
    ScalekitNotFoundException,
)

try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:  # pragma: no cover - dotenv is a dev dependency
    pass


def _env(name):
    return os.environ.get(name) or None


def _unknown_msg_id():
    """A message ID with a valid shape that no environment holds."""
    alphabet = string.ascii_letters + string.digits
    return "msg_" + "".join(secrets.choice(alphabet) for _ in range(27))


def _unknown_numeric_id(prefix):
    """An ID with a valid shape that no environment holds."""
    return f"{prefix}{secrets.randbelow(10**17) + 9 * 10**17}"


class TestTriggersApiLive(unittest.TestCase):
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
        cls.triggers = ScalekitClient(env_url, client_id, client_secret).actions.triggers
        # An environment without triggers answers every trigger call with 404
        # RESOURCE_NOT_FOUND. get_activity takes no IDs, so that answer from it can only
        # mean triggers are not available here; any other error fails the class setup.
        try:
            cls.triggers.get_activity()
        except ScalekitNotFoundException as exc:
            if exc.error_code != "RESOURCE_NOT_FOUND":
                raise
            raise unittest.SkipTest(
                "live trigger tests need triggers to be available for this environment"
            ) from exc
        cls.webhook_connection = _env("SCALEKIT_TEST_TRIGGER_CONNECTION_ID")
        cls.poll_connection = _env("SCALEKIT_TEST_TRIGGER_POLL_CONNECTION_ID")
        cls.poll_account = _env("SCALEKIT_TEST_TRIGGER_POLL_ACCOUNT_ID")
        cls.poll_trigger = _env("SCALEKIT_TEST_TRIGGER_POLL_TRIGGER")
        raw_config = _env("SCALEKIT_TEST_TRIGGER_POLL_CONFIG")
        cls.poll_config = json.loads(raw_config) if raw_config else None
        cls.endpoint = _env("SCALEKIT_TEST_TRIGGER_ENDPOINT_ID")

    # Fixture helpers

    def _need(self, **values):
        missing = [name for name, value in values.items() if not value]
        if missing:
            self.skipTest(f"needs {', '.join(missing)}")

    def _poll_fixture(self):
        self._need(
            SCALEKIT_TEST_TRIGGER_POLL_CONNECTION_ID=self.poll_connection,
            SCALEKIT_TEST_TRIGGER_POLL_ACCOUNT_ID=self.poll_account,
        )
        if self.poll_trigger:
            return self.poll_trigger
        catalogue = self.triggers.list_available(self.poll_connection)
        for trigger in catalogue.triggers:
            if trigger.mode == DetectionMode.POLL and trigger.available:
                return trigger.name
        self.skipTest("the poll connection offers no usable poll trigger")
        return None  # unreachable; skipTest raises

    def _delete_later(self, connection_id, subscription_id):
        def cleanup():
            with contextlib.suppress(ScalekitNotFoundException):  # the test deleted it
                self.triggers.delete_subscription(connection_id, subscription_id)

        self.addCleanup(cleanup)

    def _subscribe(self, trigger_name):
        subscription = self.triggers.create_subscription(
            self.poll_connection,
            trigger_name,
            connected_account_id=self.poll_account,
            config=self.poll_config,
        )
        self._delete_later(self.poll_connection, subscription.id)
        return subscription

    def _account_subscription_ids(self, trigger_name):
        """IDs of the fixture account's subscriptions to `trigger_name` (every page)."""
        ids, token = [], None
        for _ in range(50):  # bounded: 5,000 subscriptions
            page = self.triggers.list_subscriptions(
                self.poll_connection, trigger_name=trigger_name, page_size=100, page_token=token
            )
            ids += [s.id for s in page.subscriptions if s.connected_account_id == self.poll_account]
            token = page.next_page_token
            if not token:
                break
        return ids

    # Catalogue

    def test_list_available_webhook_connection(self):
        self._need(SCALEKIT_TEST_TRIGGER_CONNECTION_ID=self.webhook_connection)
        page = self.triggers.list_available(self.webhook_connection)
        self.assertTrue(page.triggers, "the connection offers no triggers")
        self.assertTrue(any(t.mode == DetectionMode.WEBHOOK for t in page.triggers))
        for trigger in page.triggers:
            self.assertTrue(trigger.name)

    def test_unknown_connection_is_not_found(self):
        with self.assertRaises(ScalekitNotFoundException) as ctx:
            self.triggers.list_available(_unknown_numeric_id("conn_"))
        self.assertEqual(ctx.exception.error_code, "RESOURCE_NOT_FOUND")

    def test_list_eligible_accounts(self):
        trigger_name = self._poll_fixture()
        page = self.triggers.list_eligible_accounts(
            self.poll_connection, trigger_name, page_size=100
        )
        self.assertGreaterEqual(page.total_size, len(page.accounts))
        ids = [a.id for a in page.accounts]
        while page.next_page_token and self.poll_account not in ids:
            page = self.triggers.list_eligible_accounts(
                self.poll_connection, trigger_name, page_size=100, page_token=page.next_page_token
            )
            ids += [a.id for a in page.accounts]
        self.assertIn(self.poll_account, ids)

    def test_list_subscriptions(self):
        self._need(SCALEKIT_TEST_TRIGGER_POLL_CONNECTION_ID=self.poll_connection)
        page = self.triggers.list_subscriptions(self.poll_connection, page_size=10)
        self.assertLessEqual(len(page.subscriptions), 10)
        self.assertGreaterEqual(page.total_size, len(page.subscriptions))
        self.assertTrue(all(isinstance(s, TriggerSubscription) for s in page.subscriptions))

    # Subscriptions

    def test_create_list_and_delete_subscription(self):
        trigger_name = self._poll_fixture()
        subscription = self._subscribe(trigger_name)
        self.assertTrue(subscription.id.startswith("trgs_"))
        self.assertEqual(subscription.connected_account_id, self.poll_account)
        self.assertEqual(subscription.trigger_name, trigger_name)
        self.assertIsInstance(subscription.effective_interval, timedelta)
        self.assertIsNotNone(subscription.created_at)
        self.assertEqual(subscription.created_at.utcoffset(), timedelta(0))

        page = self.triggers.list_subscriptions(
            self.poll_connection, trigger_name=trigger_name, page_size=100
        )
        ids = [s.id for s in page.subscriptions]
        while page.next_page_token and subscription.id not in ids:
            page = self.triggers.list_subscriptions(
                self.poll_connection,
                trigger_name=trigger_name,
                page_size=100,
                page_token=page.next_page_token,
            )
            ids += [s.id for s in page.subscriptions]
        self.assertIn(subscription.id, ids)

        self.triggers.delete_subscription(self.poll_connection, subscription.id)
        with self.assertRaises(ScalekitNotFoundException):
            self.triggers.delete_subscription(self.poll_connection, subscription.id)

    def test_duplicate_subscription_conflicts(self):
        trigger_name = self._poll_fixture()
        self._subscribe(trigger_name)
        with self.assertRaises(ScalekitConflictException) as ctx:
            self._subscribe(trigger_name)
        self.assertEqual(ctx.exception.error_code, "RESOURCE_ALREADY_EXISTS")

    def test_batch_create_reports_unknown_account_per_item(self):
        trigger_name = self._poll_fixture()
        unknown = _unknown_numeric_id("ca_")
        batch = self.triggers.batch_create_subscriptions(
            self.poll_connection,
            trigger_name,
            connected_account_ids=[self.poll_account, unknown],
            config=self.poll_config,
        )
        for result in batch.results:
            # ALREADY_SUBSCRIBED returns a subscription that may predate this test; leave it.
            if (
                result.outcome == TriggerSubscribeOutcome.CREATED
                and result.subscription is not None
            ):
                self._delete_later(self.poll_connection, result.subscription.id)
        outcomes = {r.connected_account_id: r.outcome for r in batch.results}
        self.assertEqual(outcomes[unknown], TriggerSubscribeOutcome.NOT_FOUND)
        self.assertIn(
            outcomes[self.poll_account],
            (TriggerSubscribeOutcome.CREATED, TriggerSubscribeOutcome.ALREADY_SUBSCRIBED),
        )

    def test_batch_delete_by_trigger_and_account(self):
        trigger_name = self._poll_fixture()
        if self._account_subscription_ids(trigger_name):
            # This selector deletes every subscription the account holds to the trigger.
            self.skipTest("the fixture account already holds subscriptions to this trigger")
        subscription = self._subscribe(trigger_name)  # cleanup registered as a fallback

        batch = self.triggers.batch_delete_subscriptions(
            self.poll_connection,
            trigger_name=trigger_name,
            connected_account_ids=[self.poll_account],
        )
        self.assertEqual(batch.deleted_count, 1)
        self.assertEqual(
            [(r.subscription_id, r.outcome) for r in batch.results],
            [(subscription.id, TriggerSubscriptionDeleteOutcome.DELETED)],
        )

        again = self.triggers.batch_delete_subscriptions(
            self.poll_connection,
            trigger_name=trigger_name,
            connected_account_ids=[self.poll_account],
        )
        self.assertEqual(again.deleted_count, 0)
        self.assertEqual(len(again.results), 1)
        self.assertEqual(again.results[0].connected_account_id, self.poll_account)
        self.assertEqual(again.results[0].outcome, TriggerSubscriptionDeleteOutcome.NOT_FOUND)

    # Ingress endpoint, signing secret, activity, usage

    def test_create_then_get_ingress_endpoint(self):
        self._need(SCALEKIT_TEST_TRIGGER_CONNECTION_ID=self.webhook_connection)
        created = self.triggers.create_ingress_endpoint(self.webhook_connection)
        again = self.triggers.create_ingress_endpoint(self.webhook_connection)  # idempotent
        fetched = self.triggers.get_ingress_endpoint(self.webhook_connection)
        self.assertEqual(created.id, again.id)
        self.assertEqual(created.id, fetched.id)
        self.assertEqual(fetched.connection_id, self.webhook_connection)
        # The scheme depends on the environment (a local stack may serve plain http).
        url = urlsplit(fetched.url)
        self.assertIn(url.scheme, ("http", "https"))
        self.assertTrue(url.netloc)
        self.assertGreater(len(url.path.strip("/")), 0)  # ends in the connection's token
        self.assertEqual(fetched.url, created.url)
        self.assertNotIn(fetched.url, repr(fetched))

    def test_generate_signing_secret_refused_for_self_signing_provider(self):
        self._need(SCALEKIT_TEST_TRIGGER_CONNECTION_ID=self.webhook_connection)
        # On a provider whose secret Scalekit generates, this call would succeed and replace the
        # shared fixture's secret. The server refuses exactly when the provider's webhook
        # verification does not use a generated secret, which the catalogue reports per webhook
        # trigger as provides_bearer_secret (requires_signing_secret is a different predicate).
        catalogue = self.triggers.list_available(self.webhook_connection)
        webhook = [t for t in catalogue.triggers if t.mode == DetectionMode.WEBHOOK]
        if not webhook:
            self.skipTest("the webhook fixture connection lists no webhook trigger")
        if any(t.provides_bearer_secret for t in webhook):
            self.skipTest(
                "the webhook fixture's provider uses a Scalekit-generated secret; generating one "
                "would replace it"
            )
        self.triggers.create_ingress_endpoint(self.webhook_connection)  # idempotent
        try:
            generated = self.triggers.generate_signing_secret(self.webhook_connection)
        except ScalekitBadRequestException as exc:
            self.assertEqual(exc.error_code, "TRIGGER_SIGNING_SECRET_NOT_GENERATABLE")
        else:
            endpoint_id = generated.endpoint.id if generated.endpoint else "?"
            self.fail(
                "generate_signing_secret succeeded on SCALEKIT_TEST_TRIGGER_CONNECTION_ID, whose "
                "provider should sign its own events; the fixture connection now has a "
                f"Scalekit-generated secret (endpoint {endpoint_id}) and its provider "
                "configuration must be checked"
            )

    def test_get_usage_24h(self):
        try:
            usage = self.triggers.get_usage(period="24h")
        except ScalekitNotFoundException as exc:
            self.assertEqual(exc.error_code, "TRIGGER_USAGE_NOT_METERED")
            return
        self.assertEqual(usage.period, "24h")
        self.assertEqual(usage.bucket, TriggerUsageBucket.HOUR)
        self.assertEqual(usage.days, [])
        self.assertIsNotNone(usage.today)
        self.assertEqual(usage.to_date, usage.today)
        self.assertIsNotNone(usage.current_hour)
        self.assertEqual(usage.current_hour.utcoffset(), timedelta(0))
        self.assertLessEqual(len(usage.hours), 24)
        for hour in usage.hours:
            self.assertEqual(hour.start.utcoffset(), timedelta(0))
            self.assertLessEqual(hour.start, usage.current_hour)
            self.assertGreater(hour.units, 0)

    def test_get_activity(self):
        activity = self.triggers.get_activity()
        self.assertGreater(activity.window, timedelta(0))
        self.assertIn("received", activity.counts)
        self.assertFalse(activity.explains_individual_events)

    # Deliveries

    def test_lookup_unknown_delivery_is_not_found(self):
        with self.assertRaises(ScalekitNotFoundException) as ctx:
            self.triggers.lookup_delivery(_unknown_msg_id())
        self.assertEqual(ctx.exception.error_code, "NOT_FOUND")

    def test_batch_lookup_reports_per_item_outcomes(self):
        unknown = _unknown_msg_id()
        known = None
        if self.endpoint:
            page = self.triggers.list_deliveries(self.endpoint, page_size=1)
            if page.deliveries:
                known = page.deliveries[0].msg_id
        ids = [unknown] if known is None else [unknown, known]

        batch = self.triggers.batch_lookup_deliveries(ids)  # per-item outcomes never raise

        outcomes = {r.id: r for r in batch.results}
        self.assertEqual(set(outcomes), set(ids))
        self.assertEqual(outcomes[unknown].outcome, TriggerDeliveryLookupOutcome.NOT_FOUND)
        self.assertIsNone(outcomes[unknown].delivery)
        if known is None:
            self.assertEqual(batch.found_count, 0)
            return
        self.assertEqual(outcomes[known].outcome, TriggerDeliveryLookupOutcome.FOUND)
        self.assertIsNotNone(outcomes[known].delivery)
        self.assertEqual(outcomes[known].delivery.msg_id, known)
        self.assertEqual(batch.found_count, 1)

    def test_deliveries_on_endpoint(self):
        self._need(SCALEKIT_TEST_TRIGGER_ENDPOINT_ID=self.endpoint)
        page = self.triggers.list_deliveries(self.endpoint, page_size=5)
        self.assertLessEqual(len(page.deliveries), 5)
        attempts = self.triggers.list_delivery_attempts_by_endpoint(self.endpoint, page_size=5)
        self.assertLessEqual(len(attempts.attempts), 5)
        if not page.deliveries:
            return
        delivery = page.deliveries[0]
        by_message = self.triggers.list_delivery_attempts_by_message(self.endpoint, delivery.msg_id)
        self.assertTrue(all(a.msg_id == delivery.msg_id for a in by_message.attempts))
        found = self.triggers.lookup_delivery(delivery.msg_id)
        self.assertEqual(found.msg_id, delivery.msg_id)


if __name__ == "__main__":
    unittest.main()

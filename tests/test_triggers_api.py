"""Offline tests for client.actions.triggers: request mapping, models, retries, errors.

No network: the low-level TriggersClient runs against a mocked CoreClient (request
mapping) or a real CoreClient over a mocked stub (retry and error promotion).
"""

import unittest
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from unittest.mock import MagicMock, patch

from google.protobuf.empty_pb2 import Empty
from google.protobuf.message_factory import GetMessageClass
from google.protobuf.timestamp_pb2 import Timestamp
from grpc import StatusCode
from test_sk819_retry_behavior import _make_core_client, _make_rpc_error

from scalekit.actions import (
    AccountHealthAction,
    AccountHealthState,
    ActionClient,
    ActionTriggers,
    DeliveryScope,
    DetectionMode,
    TriggerDeliveryAttemptStatus,
    TriggerDeliveryAttemptTriggerType,
    TriggerDeliveryLookupOutcome,
    TriggerDeliveryResendOutcome,
    TriggerDeliveryResendTarget,
    TriggerDeliveryStatus,
    TriggerPlatformCredentials,
    TriggerPollErrorCode,
    TriggerRefusalCode,
    TriggerSubscribeOutcome,
    TriggerSubscriptionDeleteOutcome,
    TriggerSubscriptionStatus,
    TriggerUsageBucket,
)
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitCancelledException,
    ScalekitConflictException,
    ScalekitGatewayTimeoutException,
    ScalekitInternalServerException,
    ScalekitNotFoundException,
    ScalekitServiceUnavailableException,
    ScalekitTooManyRequestsException,
)
from scalekit.triggers import TriggersClient
from scalekit.v1.triggers import triggers_pb2 as pb

UTC = timezone.utc
T0 = datetime(2026, 10, 28, 12, 30, 15, 250000, tzinfo=UTC)


def _ts(value):
    ts = Timestamp()
    ts.FromDatetime(value)
    return ts


_SERVICE = pb.DESCRIPTOR.services_by_name["TriggerService"]


def _empty_response(func, *_args, **_kwargs):
    """An empty message of the RPC's own response type (`func` is the mocked `.with_call`)."""
    method = _SERVICE.methods_by_name[func._mock_parent._mock_name]
    return (GetMessageClass(method.output_type)(), None)


def _mocked(response=None):
    """Facade over a TriggersClient whose CoreClient is a MagicMock.

    Every call returns `response`, or an empty message of the RPC's response type.
    """
    core = MagicMock()
    if response is None:
        core.grpc_exec.side_effect = _empty_response
    else:
        core.grpc_exec.return_value = (response, None)
    low = TriggersClient.__new__(TriggersClient)
    low.core_client = core
    low.trigger_service = MagicMock()
    return ActionTriggers(triggers_client=low), core


def _sent(core):
    return core.grpc_exec.call_args.args[1]


def _rpc(core):
    """Name of the stub method the call went to (the mocked `.with_call` parent)."""
    return core.grpc_exec.call_args.args[0]._mock_parent._mock_name


class TestRequestMapping(unittest.TestCase):
    def test_list_available(self):
        triggers, core = _mocked(pb.ListAvailableTriggersResponse())
        triggers.list_available("conn_1")
        self.assertEqual(_rpc(core), "ListAvailableTriggers")
        self.assertEqual(_sent(core), pb.ListAvailableTriggersRequest(connection_id="conn_1"))

    def test_list_eligible_accounts_all_and_unset(self):
        triggers, core = _mocked(pb.ListEligibleAccountsResponse())
        triggers.list_eligible_accounts(
            "conn_1", "item.created", query="bob", page_size=0, page_token="tok"
        )
        self.assertEqual(_rpc(core), "ListEligibleAccounts")
        self.assertEqual(
            _sent(core),
            pb.ListEligibleAccountsRequest(
                connection_id="conn_1", trigger_name="item.created", query="bob", page_token="tok"
            ),
        )
        triggers.list_eligible_accounts("conn_1", "item.created")
        self.assertEqual(
            _sent(core),
            pb.ListEligibleAccountsRequest(connection_id="conn_1", trigger_name="item.created"),
        )

    def test_list_eligible_accounts_page_size_above_cap_is_sent(self):
        triggers, core = _mocked(pb.ListEligibleAccountsResponse())
        triggers.list_eligible_accounts("conn_1", "t", page_size=500)
        self.assertEqual(_sent(core).page_size, 500)  # the server caps it

    def test_list_subscriptions_statuses_member_name_and_int(self):
        triggers, core = _mocked(pb.ListTriggerSubscriptionsResponse())
        triggers.list_subscriptions(
            "conn_1",
            trigger_name="t",
            statuses=[TriggerSubscriptionStatus.PAUSED, "ACTIVE", 77],
            page_size=10,
            page_token="tok",
        )
        request = _sent(core)
        self.assertEqual(_rpc(core), "ListTriggerSubscriptions")
        self.assertEqual(list(request.statuses), [pb.PAUSED, pb.ACTIVE, 77])
        self.assertEqual(
            (request.trigger_name, request.page_size, request.page_token), ("t", 10, "tok")
        )

    def test_list_subscriptions_unset(self):
        triggers, core = _mocked(pb.ListTriggerSubscriptionsResponse())
        triggers.list_subscriptions("conn_1")
        self.assertEqual(_sent(core), pb.ListTriggerSubscriptionsRequest(connection_id="conn_1"))

    def test_create_subscription(self):
        triggers, core = _mocked(pb.TriggerSubscription())
        triggers.create_subscription(
            "conn_1",
            "poll.items",
            connected_account_id="ca_1",
            interval=timedelta(minutes=5),
            config={"folder": "inbox"},
        )
        self.assertEqual(_rpc(core), "CreateTriggerSubscription")
        self.assertEqual(
            _sent(core),
            pb.CreateTriggerSubscriptionRequest(
                connection_id="conn_1",
                trigger_name="poll.items",
                connected_account_id="ca_1",
                interval_seconds=300,
                config={"folder": "inbox"},
            ),
        )

    def test_create_subscription_unset_optionals(self):
        triggers, core = _mocked(pb.TriggerSubscription())
        triggers.create_subscription("conn_1", "t")
        self.assertEqual(
            _sent(core),
            pb.CreateTriggerSubscriptionRequest(connection_id="conn_1", trigger_name="t"),
        )

    def test_batch_create_subscriptions(self):
        triggers, core = _mocked(pb.BatchCreateTriggerSubscriptionsResponse())
        triggers.batch_create_subscriptions(
            "conn_1",
            "t",
            connected_account_ids=("ca_1", "ca_2"),
            interval=timedelta(seconds=60),
            config={"k": "v"},
        )
        self.assertEqual(_rpc(core), "BatchCreateTriggerSubscriptions")
        self.assertEqual(
            _sent(core),
            pb.BatchCreateTriggerSubscriptionsRequest(
                connection_id="conn_1",
                trigger_name="t",
                connected_account_ids=["ca_1", "ca_2"],
                interval_seconds=60,
                config={"k": "v"},
            ),
        )

    def test_batch_create_subscriptions_connection_scoped_sends_no_accounts(self):
        triggers, core = _mocked(pb.BatchCreateTriggerSubscriptionsResponse())
        triggers.batch_create_subscriptions("conn_1", "t")
        self.assertEqual(
            _sent(core),
            pb.BatchCreateTriggerSubscriptionsRequest(connection_id="conn_1", trigger_name="t"),
        )

    def test_delete_subscription(self):
        triggers, core = _mocked(Empty())
        self.assertIsNone(triggers.delete_subscription("conn_1", "trgs_1"))
        self.assertEqual(_rpc(core), "DeleteTriggerSubscription")
        self.assertEqual(
            _sent(core),
            pb.DeleteTriggerSubscriptionRequest(connection_id="conn_1", subscription_id="trgs_1"),
        )

    def test_batch_delete_by_ids_and_by_trigger(self):
        triggers, core = _mocked(pb.BatchDeleteTriggerSubscriptionsResponse())
        triggers.batch_delete_subscriptions("conn_1", subscription_ids=["trgs_1"])
        self.assertEqual(_rpc(core), "BatchDeleteTriggerSubscriptions")
        self.assertEqual(
            _sent(core),
            pb.BatchDeleteTriggerSubscriptionsRequest(
                connection_id="conn_1", subscription_ids=["trgs_1"]
            ),
        )
        triggers.batch_delete_subscriptions(
            "conn_1", trigger_name="t", connected_account_ids=["ca_1"]
        )
        self.assertEqual(
            _sent(core),
            pb.BatchDeleteTriggerSubscriptionsRequest(
                connection_id="conn_1", trigger_name="t", connected_account_ids=["ca_1"]
            ),
        )

    def test_batch_delete_no_selector_is_left_to_the_server(self):
        triggers, core = _mocked(pb.BatchDeleteTriggerSubscriptionsResponse())
        triggers.batch_delete_subscriptions("conn_1")
        self.assertEqual(
            _sent(core), pb.BatchDeleteTriggerSubscriptionsRequest(connection_id="conn_1")
        )

    def test_get_activity(self):
        triggers, core = _mocked(pb.GetTriggerActivityResponse())
        triggers.get_activity()
        self.assertEqual(_rpc(core), "GetTriggerActivity")
        self.assertEqual(_sent(core), pb.GetTriggerActivityRequest())

    def test_get_usage_period(self):
        triggers, core = _mocked(pb.GetTriggerUsageResponse())
        triggers.get_usage(period="24h")
        self.assertEqual(_rpc(core), "GetTriggerUsage")
        request = _sent(core)
        self.assertEqual(request.period, "24h")
        self.assertEqual((getattr(request, "from"), request.to), ("", ""))

    def test_get_usage_dates_from_date_datetime_and_str(self):
        triggers, core = _mocked(pb.GetTriggerUsageResponse())
        late_utc = datetime(2026, 10, 2, 23, 30, tzinfo=timezone(timedelta(hours=-5)))
        triggers.get_usage(from_date=date(2026, 10, 1), to_date=late_utc)
        request = _sent(core)
        self.assertEqual(
            (getattr(request, "from"), request.to, request.period), ("2026-10-01", "2026-10-03", "")
        )
        triggers.get_usage(from_date="2026-10-01", to_date="2026-10-31")
        self.assertEqual(
            (getattr(_sent(core), "from"), _sent(core).to), ("2026-10-01", "2026-10-31")
        )

    def test_get_usage_combination_is_left_to_the_server(self):
        triggers, core = _mocked(pb.GetTriggerUsageResponse())
        triggers.get_usage(period="7d", from_date="2026-10-01")
        self.assertEqual((_sent(core).period, getattr(_sent(core), "from")), ("7d", "2026-10-01"))
        triggers.get_usage()
        self.assertEqual(_sent(core), pb.GetTriggerUsageRequest())

    def test_ingress_endpoint_methods(self):
        for method, rpc in (
            ("get_ingress_endpoint", "GetTriggerIngressEndpoint"),
            ("create_ingress_endpoint", "CreateTriggerIngressEndpoint"),
        ):
            triggers, core = _mocked(pb.TriggerIngressEndpoint())
            getattr(triggers, method)("conn_1")
            self.assertEqual(_rpc(core), rpc)
            self.assertEqual(_sent(core).connection_id, "conn_1")

    def test_set_signing_secret(self):
        triggers, core = _mocked(pb.TriggerIngressEndpoint())
        triggers.set_signing_secret("conn_1", signing_secret="  s3cret-value  ")
        self.assertEqual(_rpc(core), "SetTriggerSigningSecret")
        # Sent as given: trimming and length checks are the server's.
        self.assertEqual(
            _sent(core),
            pb.SetTriggerSigningSecretRequest(
                connection_id="conn_1", signing_secret="  s3cret-value  "
            ),
        )

    def test_confirm_rotation_with_and_without_id(self):
        triggers, core = _mocked(pb.TriggerIngressEndpoint())
        triggers.confirm_signing_secret_rotation("conn_1", signing_secret_rotation_id=3)
        self.assertEqual(_rpc(core), "ConfirmTriggerSigningSecretRotation")
        self.assertEqual(_sent(core).signing_secret_rotation_id, 3)
        triggers.confirm_signing_secret_rotation("conn_1")
        self.assertEqual(
            _sent(core), pb.ConfirmTriggerSigningSecretRotationRequest(connection_id="conn_1")
        )

    def test_generate_signing_secret(self):
        triggers, core = _mocked(pb.GenerateTriggerSigningSecretResponse())
        triggers.generate_signing_secret("conn_1")
        self.assertEqual(_rpc(core), "GenerateTriggerSigningSecret")
        self.assertEqual(_sent(core).connection_id, "conn_1")

    def test_list_delivery_attempts_by_endpoint(self):
        triggers, core = _mocked(pb.ListTriggerDeliveryAttemptsByEndpointResponse())
        triggers.list_delivery_attempts_by_endpoint("ep_1", page_size=5)
        self.assertEqual(_rpc(core), "ListTriggerDeliveryAttemptsByEndpoint")
        self.assertEqual(
            _sent(core),
            pb.ListTriggerDeliveryAttemptsByEndpointRequest(endpoint_id="ep_1", page_size=5),
        )

    def test_endpoint_id_without_ep_prefix_is_sent(self):
        triggers, core = _mocked(pb.ListTriggerDeliveryAttemptsByEndpointResponse())
        triggers.list_delivery_attempts_by_endpoint("custom.endpoint-1")
        self.assertEqual(_sent(core).endpoint_id, "custom.endpoint-1")

    def test_list_deliveries_all_filters(self):
        triggers, core = _mocked(pb.ListTriggerDeliveriesByEndpointResponse())
        ist = timezone(timedelta(hours=5, minutes=30))
        triggers.list_deliveries(
            "ep_1",
            page_size=50,
            page_token="tok",
            status=TriggerDeliveryStatus.FAILED,
            channel="conn_1",
            after=datetime(2026, 10, 27, 17, 30, tzinfo=ist),
            before=T0,
        )
        request = _sent(core)
        self.assertEqual(_rpc(core), "ListTriggerDeliveriesByEndpoint")
        self.assertEqual(request.status, pb.TRIGGER_DELIVERY_STATUS_FAILED)
        self.assertEqual(
            request.after.ToDatetime(tzinfo=UTC), datetime(2026, 10, 27, 12, 0, tzinfo=UTC)
        )
        self.assertEqual(request.before.ToDatetime(tzinfo=UTC), T0)
        self.assertEqual(
            (request.page_size, request.page_token, request.channel), (50, "tok", "conn_1")
        )

    def test_list_deliveries_unset_and_status_spellings(self):
        triggers, core = _mocked(pb.ListTriggerDeliveriesByEndpointResponse())
        triggers.list_deliveries("ep_1")
        request = _sent(core)
        self.assertEqual(request, pb.ListTriggerDeliveriesByEndpointRequest(endpoint_id="ep_1"))
        self.assertFalse(request.HasField("after"))
        self.assertFalse(request.HasField("before"))
        for status, number in (
            ("DELIVERED", 1),
            ("TRIGGER_DELIVERY_STATUS_RETRYING", 4),
            (42, 42),
        ):
            triggers.list_deliveries("ep_1", status=status)
            self.assertEqual(_sent(core).status, number)

    def test_list_delivery_attempts_by_message(self):
        triggers, core = _mocked(pb.ListTriggerDeliveryAttemptsByMessageResponse())
        triggers.list_delivery_attempts_by_message("ep_1", "msg_1")
        self.assertEqual(_rpc(core), "ListTriggerDeliveryAttemptsByMessage")
        self.assertEqual(
            _sent(core),
            pb.ListTriggerDeliveryAttemptsByMessageRequest(endpoint_id="ep_1", msg_id="msg_1"),
        )

    def test_lookup_delivery_sends_id(self):
        triggers, core = _mocked(pb.LookupTriggerDeliveryResponse())
        triggers.lookup_delivery("evt_abc")
        self.assertEqual(_rpc(core), "LookupTriggerDelivery")
        self.assertEqual(_sent(core), pb.LookupTriggerDeliveryRequest(id="evt_abc"))

    def test_batch_lookup_deliveries(self):
        triggers, core = _mocked(pb.BatchLookupTriggerDeliveriesResponse())
        triggers.batch_lookup_deliveries(["msg_1", "evt_2"])
        self.assertEqual(_rpc(core), "BatchLookupTriggerDeliveries")
        self.assertEqual(list(_sent(core).ids), ["msg_1", "evt_2"])

    def test_batch_resend_accepts_models_and_dicts(self):
        triggers, core = _mocked(pb.BatchResendTriggerDeliveriesResponse())
        triggers.batch_resend_deliveries(
            [
                TriggerDeliveryResendTarget(msg_id="msg_1", endpoint_id="ep_1"),
                {"msg_id": "msg_2", "endpoint_id": "ep_2"},
            ]
        )
        self.assertEqual(_rpc(core), "BatchResendTriggerDeliveries")
        self.assertEqual(
            [(t.msg_id, t.endpoint_id) for t in _sent(core).targets],
            [("msg_1", "ep_1"), ("msg_2", "ep_2")],
        )

    def test_recover_deliveries(self):
        triggers, core = _mocked(pb.RecoverTriggerDeliveriesResponse())
        triggers.recover_deliveries("ep_1", since=T0 - timedelta(hours=1), until=T0)
        request = _sent(core)
        self.assertEqual(_rpc(core), "RecoverTriggerDeliveries")
        self.assertEqual(request.since.ToDatetime(tzinfo=UTC), T0 - timedelta(hours=1))
        self.assertEqual(request.until.ToDatetime(tzinfo=UTC), T0)
        triggers.recover_deliveries("ep_1", since=T0)
        self.assertFalse(_sent(core).HasField("until"))


class TestValidation(unittest.TestCase):
    """Arguments that cannot be sent fail before any request."""

    def _assert_no_call(self, exc, fn):
        triggers, core = _mocked()
        with self.assertRaises(exc):
            fn(triggers)
        core.grpc_exec.assert_not_called()

    def test_empty_required_ids_raise_value_error(self):
        cases = {
            "connection_id": [
                lambda t: t.list_available(""),
                lambda t: t.list_eligible_accounts("", "t"),
                lambda t: t.list_subscriptions(""),
                lambda t: t.create_subscription("", "t"),
                lambda t: t.batch_create_subscriptions("", "t"),
                lambda t: t.delete_subscription("", "trgs_1"),
                lambda t: t.batch_delete_subscriptions("", subscription_ids=["trgs_1"]),
                lambda t: t.get_ingress_endpoint(""),
                lambda t: t.create_ingress_endpoint(""),
                lambda t: t.set_signing_secret("", signing_secret="s"),
                lambda t: t.confirm_signing_secret_rotation(""),
                lambda t: t.generate_signing_secret(""),
            ],
            "trigger_name": [
                lambda t: t.list_eligible_accounts("conn_1", ""),
                lambda t: t.create_subscription("conn_1", ""),
                lambda t: t.batch_create_subscriptions("conn_1", ""),
            ],
            "subscription_id": [lambda t: t.delete_subscription("conn_1", "")],
            "endpoint_id": [
                lambda t: t.list_delivery_attempts_by_endpoint(""),
                lambda t: t.list_deliveries(""),
                lambda t: t.list_delivery_attempts_by_message("", "msg_1"),
                lambda t: t.recover_deliveries("", since=T0),
            ],
            "msg_id": [lambda t: t.list_delivery_attempts_by_message("ep_1", "")],
            "delivery_id": [lambda t: t.lookup_delivery("")],
            "since": [lambda t: t.recover_deliveries("ep_1", since=None)],
        }
        for name, calls in cases.items():
            for call in calls:
                with self.subTest(name=name):
                    triggers, core = _mocked()
                    with self.assertRaisesRegex(ValueError, f"{name} is required"):
                        call(triggers)
                    core.grpc_exec.assert_not_called()

    def test_naive_datetimes_raise(self):
        naive = T0.replace(tzinfo=None)
        for call in (
            lambda t: t.list_deliveries("ep_1", after=naive),
            lambda t: t.list_deliveries("ep_1", before=naive),
            lambda t: t.recover_deliveries("ep_1", since=naive),
            lambda t: t.recover_deliveries("ep_1", since=T0, until=naive),
            lambda t: t.get_usage(from_date=naive, to_date="2026-10-28"),
        ):
            with self.subTest():
                self._assert_no_call(ValueError, call)

    def test_fractional_interval_raises(self):
        for call in (
            lambda t: t.create_subscription("conn_1", "t", interval=timedelta(seconds=1.5)),
            lambda t: t.batch_create_subscriptions(
                "conn_1", "t", interval=timedelta(milliseconds=10)
            ),
        ):
            with self.subTest():
                self._assert_no_call(ValueError, call)

    def test_interval_below_floor_is_left_to_the_server(self):
        triggers, core = _mocked(pb.TriggerSubscription())
        triggers.create_subscription("conn_1", "t", interval=timedelta(seconds=1))
        self.assertEqual(_sent(core).interval_seconds, 1)

    def test_unknown_enum_names_raise(self):
        self._assert_no_call(
            ValueError, lambda t: t.list_subscriptions("conn_1", statuses=["NOPE"])
        )
        self._assert_no_call(ValueError, lambda t: t.list_deliveries("ep_1", status="delivered"))

    def test_bool_is_not_an_enum_value(self):
        self._assert_no_call(TypeError, lambda t: t.list_deliveries("ep_1", status=True))

    def test_bare_string_lists_raise_type_error(self):
        for call in (
            lambda t: t.list_subscriptions("conn_1", statuses="ACTIVE"),
            lambda t: t.batch_create_subscriptions("conn_1", "t", connected_account_ids="ca_1"),
            lambda t: t.batch_delete_subscriptions("conn_1", subscription_ids="trgs_1"),
            lambda t: t.batch_lookup_deliveries("msg_1"),
        ):
            with self.subTest():
                self._assert_no_call(TypeError, call)

    def test_bad_usage_dates_raise(self):
        for bad in ("2026-13-01", "20261001", "2026-1-1", "yesterday"):
            with self.subTest(bad=bad):
                self._assert_no_call(
                    ValueError, lambda t, b=bad: t.get_usage(from_date=b, to_date="2026-10-02")
                )

    def test_resend_target_dict_missing_a_key_raises(self):
        self._assert_no_call(TypeError, lambda t: t.batch_resend_deliveries([{"msg_id": "msg_1"}]))

    def test_bad_resend_target_raises(self):
        self._assert_no_call(TypeError, lambda t: t.batch_resend_deliveries([("msg_1", "ep_1")]))

    def test_prefixes_and_list_sizes_are_not_checked(self):
        triggers, core = _mocked(pb.BatchLookupTriggerDeliveriesResponse())
        triggers.batch_lookup_deliveries([f"id{i}" for i in range(30)])  # server allows 25
        self.assertEqual(len(_sent(core).ids), 30)
        triggers, core = _mocked(pb.TriggerSubscription())
        triggers.create_subscription("not-a-conn", "t", connected_account_id="not-a-ca")
        self.assertEqual(_sent(core).connected_account_id, "not-a-ca")


class TestResponseMapping(unittest.TestCase):
    def test_available_trigger(self):
        response = pb.ListAvailableTriggersResponse(
            connection_uses_shared_app=True,
            triggers=[
                pb.AvailableTrigger(
                    name="poll.items",
                    mode=pb.POLL,
                    required_scopes=[pb.RequiredScope(scope="read", grant="user")],
                    min_interval_seconds=60,
                    default_interval_seconds=0,
                    config_fields=[pb.ConfigField(key="folder", required=True)],
                    available=False,
                    reason="shared app",
                    delivery_scope=pb.CONNECTION,
                    platform_credentials=pb.UNSUPPORTED,
                    refusal_code=pb.SHARED_APP,
                    requires_signing_secret=True,
                ),
                pb.AvailableTrigger(name="bare"),
            ],
        )
        triggers, _ = _mocked(response)
        page = triggers.list_available("conn_1")
        self.assertTrue(page.connection_uses_shared_app)
        first, bare = page.triggers
        self.assertIs(first.mode, DetectionMode.POLL)
        self.assertIs(first.delivery_scope, DeliveryScope.CONNECTION)
        self.assertIs(first.platform_credentials, TriggerPlatformCredentials.UNSUPPORTED)
        self.assertIs(first.refusal_code, TriggerRefusalCode.SHARED_APP)
        self.assertEqual(first.min_interval, timedelta(seconds=60))
        self.assertIsNone(first.default_interval)  # 0 = not set
        self.assertEqual(first.required_scopes[0].scope, "read")
        self.assertTrue(first.config_fields[0].required)
        # UNSPECIFIED -> None; lists default to empty
        self.assertIsNone(bare.mode)
        self.assertIsNone(bare.delivery_scope)
        self.assertIsNone(bare.refusal_code)
        self.assertEqual(bare.required_scopes, [])

    def test_unknown_enum_numbers_come_through_as_strings(self):
        sub = pb.TriggerSubscription(
            id="trgs_1", status=999, delivery_scope=998, account_health=997
        )
        triggers, _ = _mocked(sub)
        result = triggers.create_subscription("conn_1", "t")
        self.assertEqual(result.status, "999")
        self.assertEqual(result.delivery_scope, "998")
        self.assertEqual(result.account_health, "997")

    def test_every_new_enum_field_survives_an_unknown_value(self):
        cases = [
            (
                pb.AvailableTrigger,
                ("mode", "delivery_scope", "platform_credentials", "refusal_code"),
            ),
            (pb.AccountHealth, ("state", "action")),
            (pb.TriggerPollState, ("last_error_code",)),
            (pb.TriggerDelivery, ("status", "trigger_mode")),
            (pb.TriggerDeliveryAttempt, ("status", "trigger_type")),
            (pb.BatchCreateTriggerSubscriptionResult, ("outcome",)),
            (pb.BatchDeleteTriggerSubscriptionResult, ("outcome",)),
            (pb.BatchLookupTriggerDeliveryResult, ("outcome",)),
            (pb.BatchResendTriggerDeliveryResult, ("outcome",)),
            (pb.GetTriggerUsageResponse, ("bucket",)),
        ]
        from scalekit.actions.models import triggers as models

        for proto_cls, fields in cases:
            model_cls = getattr(models, proto_cls.DESCRIPTOR.name)
            message = proto_cls(**dict.fromkeys(fields, 999))
            model = model_cls.from_proto(message)
            for field in fields:
                with self.subTest(model=model_cls.__name__, field=field):
                    self.assertEqual(getattr(model, field), "999")

    def test_known_name_missing_from_sdk_enum_is_kept_as_name(self):
        from scalekit._convert import enum_from_proto

        class Narrow(str, Enum):
            ACTIVE = "ACTIVE"

        self.assertEqual(enum_from_proto(Narrow, pb.TriggerSubscriptionStatus, pb.PAUSED), "PAUSED")
        self.assertEqual(
            enum_from_proto(Narrow, pb.TriggerDeliveryStatus, pb.TRIGGER_DELIVERY_STATUS_FAILED),
            "FAILED",
        )

    def test_subscription_timestamps_intervals_and_presence(self):
        sub = pb.TriggerSubscription(
            id="trgs_1",
            connected_account_id="ca_1",
            status=pb.PAUSED_CREDENTIAL,
            requested_interval_seconds=0,
            effective_interval_seconds=0,
            config={"k": "v"},
            delivery_scope=pb.ACCOUNT,
            created_at=_ts(T0),
            poll_state=pb.TriggerPollState(
                last_run_at=_ts(T0), consecutive_failures=2, last_error_code=pb.TIMED_OUT
            ),
            account_health=pb.READY,
        )
        triggers, _ = _mocked(sub)
        result = triggers.create_subscription("conn_1", "t")
        self.assertIs(result.status, TriggerSubscriptionStatus.PAUSED_CREDENTIAL)
        self.assertIs(result.delivery_scope, DeliveryScope.ACCOUNT)
        self.assertIsNone(result.requested_interval)
        self.assertIsNone(result.effective_interval)
        self.assertEqual(result.created_at, T0)
        self.assertEqual(result.created_at.utcoffset(), timedelta(0))
        self.assertEqual(result.config, {"k": "v"})
        self.assertIs(result.poll_state.last_error_code, TriggerPollErrorCode.TIMED_OUT)
        self.assertEqual(result.poll_state.last_run_at, T0)
        self.assertIsNone(result.poll_state.backoff_until)  # unset timestamp
        self.assertIsNone(result.poll_state.watermark_updated_at)
        self.assertIs(result.account_health, AccountHealthState.READY)

    def test_subscription_absent_fields(self):
        triggers, _ = _mocked(pb.TriggerSubscription(effective_interval_seconds=300))
        result = triggers.create_subscription("conn_1", "t")
        self.assertIsNone(result.created_at)
        self.assertIsNone(result.poll_state)
        self.assertIsNone(result.account_health)
        self.assertIsNone(result.status)
        self.assertEqual(result.effective_interval, timedelta(minutes=5))
        self.assertEqual(result.config, {})

    def test_account_health_explicitly_unspecified_is_none(self):
        triggers, _ = _mocked(pb.TriggerSubscription(account_health=0))
        self.assertIsNone(triggers.create_subscription("conn_1", "t").account_health)

    def test_eligible_accounts_and_empty_tokens(self):
        response = pb.ListEligibleAccountsResponse(
            accounts=[
                pb.EligibleAccount(
                    id="ca_1",
                    eligible=False,
                    health=pb.AccountHealth(
                        state=pb.NEEDS_REAUTHENTICATION, action=pb.RECONNECT, blocks_tool_calls=True
                    ),
                ),
                pb.EligibleAccount(id="ca_2", eligible=True),
            ],
            next_page_token="",
            prev_page_token="",
            total_size=2,
        )
        triggers, _ = _mocked(response)
        page = triggers.list_eligible_accounts("conn_1", "t")
        self.assertIsNone(page.next_page_token)
        self.assertIsNone(page.prev_page_token)
        self.assertEqual(page.total_size, 2)
        self.assertIs(page.accounts[0].health.state, AccountHealthState.NEEDS_REAUTHENTICATION)
        self.assertIs(page.accounts[0].health.action, AccountHealthAction.RECONNECT)
        self.assertIsNone(page.accounts[1].health)

    def test_subscriptions_page(self):
        response = pb.ListTriggerSubscriptionsResponse(
            subscriptions=[pb.TriggerSubscription(id="trgs_1")],
            next_page_token="n",
            prev_page_token="p",
            total_size=7,
            status_counts={"ACTIVE": 5, "PAUSED": 2},
        )
        triggers, _ = _mocked(response)
        page = triggers.list_subscriptions("conn_1")
        self.assertEqual((page.next_page_token, page.prev_page_token), ("n", "p"))
        self.assertEqual(page.status_counts, {"ACTIVE": 5, "PAUSED": 2})
        self.assertEqual(page.subscriptions[0].id, "trgs_1")

    def test_activity(self):
        response = pb.GetTriggerActivityResponse(
            counts={"received": 3, "filtered": 0}, window_hours=24, signature_banner=True
        )
        triggers, _ = _mocked(response)
        activity = triggers.get_activity()
        self.assertEqual(activity.window, timedelta(hours=24))
        self.assertEqual(activity.counts, {"received": 3, "filtered": 0})
        self.assertTrue(activity.signature_banner)

    def test_usage_hourly(self):
        response = pb.GetTriggerUsageResponse(
            **{"from": "2026-10-27"},
            to="2026-10-28",
            today="2026-10-28",
            period="24h",
            bucket=pb.TRIGGER_USAGE_BUCKET_HOUR,
            hours=[pb.TriggerUsageHour(start="2026-10-28T11:00:00Z", units=4)],
            current_hour="2026-10-28T12:00:00Z",
        )
        triggers, _ = _mocked(response)
        usage = triggers.get_usage(period="24h")
        self.assertEqual(usage.from_date, date(2026, 10, 27))
        self.assertEqual(usage.to_date, date(2026, 10, 28))
        self.assertEqual(usage.today, date(2026, 10, 28))
        self.assertEqual(usage.period, "24h")
        self.assertIs(usage.bucket, TriggerUsageBucket.HOUR)
        self.assertEqual(usage.hours[0].start, datetime(2026, 10, 28, 11, tzinfo=UTC))
        self.assertEqual(usage.hours[0].units, 4)
        self.assertEqual(usage.current_hour, datetime(2026, 10, 28, 12, tzinfo=UTC))
        self.assertEqual(usage.days, [])

    def test_usage_date_range(self):
        response = pb.GetTriggerUsageResponse(
            **{"from": "2026-10-01"},
            to="2026-10-03",
            days=[pb.TriggerUsageDay(date="2026-10-02", units=9)],
        )
        triggers, _ = _mocked(response)
        usage = triggers.get_usage(from_date="2026-10-01", to_date="2026-10-03")
        self.assertIsNone(usage.period)  # empty -> None
        self.assertIsNone(usage.bucket)  # UNSPECIFIED -> None (counted by day)
        self.assertIsNone(usage.current_hour)  # empty -> None
        self.assertIsNone(usage.today)
        self.assertEqual(usage.days[0].date, date(2026, 10, 2))

    def test_ingress_endpoint(self):
        response = pb.TriggerIngressEndpoint(
            id="tie_1",
            url="https://example.test/triggers/v1/token",
            signing_secret_configured=True,
            masked_signing_secret="****a4f9",
            rotation_in_progress=True,
            previous_signing_secret_expires_at=_ts(T0),
            signing_secret_rotation_id=3,
        )
        triggers, _ = _mocked(response)
        endpoint = triggers.get_ingress_endpoint("conn_1")
        self.assertEqual(endpoint.previous_signing_secret_expires_at, T0)
        self.assertEqual(endpoint.url, "https://example.test/triggers/v1/token")
        self.assertNotIn("triggers/v1/token", repr(endpoint))  # confidential URL
        self.assertEqual(endpoint.signing_secret_rotation_id, 3)
        triggers, _ = _mocked(pb.TriggerIngressEndpoint(id="tie_1"))
        self.assertIsNone(
            triggers.get_ingress_endpoint("conn_1").previous_signing_secret_expires_at
        )

    def test_generated_secret_is_hidden_from_repr(self):
        response = pb.GenerateTriggerSigningSecretResponse(
            endpoint=pb.TriggerIngressEndpoint(id="tie_1"),
            signing_secret="supersecretvalue123",
            url_with_secret="https://example.test/x?secret=supersecretvalue123",
        )
        triggers, _ = _mocked(response)
        generated = triggers.generate_signing_secret("conn_1")
        self.assertEqual(generated.signing_secret, "supersecretvalue123")
        self.assertNotIn("supersecretvalue123", repr(generated))
        self.assertNotIn("supersecretvalue123", str(generated))
        self.assertEqual(generated.endpoint.id, "tie_1")

    def test_deliveries_and_attempts(self):
        response = pb.ListTriggerDeliveriesByEndpointResponse(
            deliveries=[
                pb.TriggerDelivery(
                    msg_id="msg_1",
                    status=pb.TRIGGER_DELIVERY_STATUS_RETRYING,
                    trigger_mode=pb.WEBHOOK,
                    message_timestamp=_ts(T0),
                )
            ],
        )
        triggers, _ = _mocked(response)
        page = triggers.list_deliveries("ep_1")
        self.assertIsNone(page.next_page_token)
        delivery = page.deliveries[0]
        self.assertIs(delivery.status, TriggerDeliveryStatus.RETRYING)
        self.assertIs(delivery.trigger_mode, DetectionMode.WEBHOOK)
        self.assertEqual(delivery.message_timestamp, T0)
        self.assertIsNone(delivery.next_attempt_at)

        attempts = pb.ListTriggerDeliveryAttemptsByMessageResponse(
            attempts=[
                pb.TriggerDeliveryAttempt(
                    status=pb.FAIL,
                    trigger_type=pb.TRIGGER_DELIVERY_ATTEMPT_TRIGGER_TYPE_MANUAL,
                    response_duration_ms=250,
                    timestamp=_ts(T0),
                ),
                pb.TriggerDeliveryAttempt(status=pb.SUCCESS),
            ],
            truncated=True,
        )
        triggers, _ = _mocked(attempts)
        result = triggers.list_delivery_attempts_by_message("ep_1", "msg_1")
        self.assertTrue(result.truncated)
        first, second = result.attempts
        self.assertIs(first.status, TriggerDeliveryAttemptStatus.FAIL)
        self.assertIs(first.trigger_type, TriggerDeliveryAttemptTriggerType.MANUAL)
        self.assertEqual(first.response_duration, timedelta(milliseconds=250))
        self.assertEqual(second.response_duration, timedelta(0))  # 0 is a value here
        self.assertIsNone(second.timestamp)
        self.assertIsNone(second.trigger_type)

    def test_lookup_and_recover(self):
        triggers, _ = _mocked(
            pb.LookupTriggerDeliveryResponse(
                msg_id="msg_1", trigger_mode=pb.POLL, attempts=[pb.TriggerDeliveryAttempt(id="a")]
            )
        )
        found = triggers.lookup_delivery("msg_1")
        self.assertIs(found.trigger_mode, DetectionMode.POLL)
        self.assertEqual(found.attempts[0].id, "a")
        self.assertIsNone(found.message_timestamp)
        triggers, _ = _mocked(pb.RecoverTriggerDeliveriesResponse(task_id="t1", status="running"))
        task = triggers.recover_deliveries("ep_1", since=T0)
        self.assertEqual((task.task_id, task.status), ("t1", "running"))

    def test_models_are_frozen_and_keep_unknown_fields(self):
        from pydantic import ValidationError

        from scalekit.actions import TriggerSubscription

        triggers, _ = _mocked(pb.TriggerSubscription(id="trgs_1"))
        result = triggers.create_subscription("conn_1", "t")
        with self.assertRaises(ValidationError):
            result.id = "other"
        extended = TriggerSubscription(id="trgs_1", added_later="x")
        self.assertEqual(extended.model_extra, {"added_later": "x"})


class TestBatchOutcomes(unittest.TestCase):
    """Per-item failures come back in `results`; they never raise."""

    def test_batch_create_outcomes(self):
        response = pb.BatchCreateTriggerSubscriptionsResponse(
            created_count=1,
            results=[
                pb.BatchCreateTriggerSubscriptionResult(
                    connected_account_id="ca_1",
                    outcome=pb.CREATED,
                    subscription=pb.TriggerSubscription(id="trgs_1"),
                ),
                pb.BatchCreateTriggerSubscriptionResult(
                    connected_account_id="ca_missing", outcome=pb.NOT_FOUND, reason="not found"
                ),
                pb.BatchCreateTriggerSubscriptionResult(
                    connected_account_id="ca_3", outcome=pb.REFUSED, reason="missing scope"
                ),
                pb.BatchCreateTriggerSubscriptionResult(
                    connected_account_id="ca_4", outcome=pb.FAILED
                ),
            ],
        )
        triggers, _ = _mocked(response)
        batch = triggers.batch_create_subscriptions("conn_1", "t", connected_account_ids=["ca_1"])
        self.assertEqual(batch.created_count, 1)
        self.assertEqual(
            [r.outcome for r in batch.results],
            [
                TriggerSubscribeOutcome.CREATED,
                TriggerSubscribeOutcome.NOT_FOUND,
                TriggerSubscribeOutcome.REFUSED,
                TriggerSubscribeOutcome.FAILED,
            ],
        )
        self.assertEqual(batch.results[0].subscription.id, "trgs_1")
        self.assertIsNone(batch.results[1].subscription)
        self.assertEqual(batch.results[1].reason, "not found")

    def test_batch_delete_outcomes(self):
        response = pb.BatchDeleteTriggerSubscriptionsResponse(
            deleted_count=1,
            results=[
                pb.BatchDeleteTriggerSubscriptionResult(
                    subscription_id="trgs_1", outcome=pb.BATCH_DELETE_OUTCOME_DELETED
                ),
                pb.BatchDeleteTriggerSubscriptionResult(
                    subscription_id="trgs_2", outcome=pb.BATCH_DELETE_OUTCOME_NOT_ATTEMPTED
                ),
            ],
        )
        triggers, _ = _mocked(response)
        batch = triggers.batch_delete_subscriptions("conn_1", subscription_ids=["trgs_1", "trgs_2"])
        self.assertEqual(
            [r.outcome for r in batch.results],
            [
                TriggerSubscriptionDeleteOutcome.DELETED,
                TriggerSubscriptionDeleteOutcome.NOT_ATTEMPTED,
            ],
        )

    def test_batch_lookup_and_resend_outcomes(self):
        triggers, _ = _mocked(
            pb.BatchLookupTriggerDeliveriesResponse(
                found_count=1,
                results=[
                    pb.BatchLookupTriggerDeliveryResult(
                        id="msg_1",
                        outcome=pb.BATCH_LOOKUP_OUTCOME_FOUND,
                        delivery=pb.LookupTriggerDeliveryResponse(msg_id="msg_1"),
                    ),
                    pb.BatchLookupTriggerDeliveryResult(
                        id="msg_2", outcome=pb.BATCH_LOOKUP_OUTCOME_RATE_LIMITED
                    ),
                ],
            )
        )
        batch = triggers.batch_lookup_deliveries(["msg_1", "msg_2"])
        self.assertIs(batch.results[0].outcome, TriggerDeliveryLookupOutcome.FOUND)
        self.assertEqual(batch.results[0].delivery.msg_id, "msg_1")
        self.assertIs(batch.results[1].outcome, TriggerDeliveryLookupOutcome.RATE_LIMITED)
        self.assertIsNone(batch.results[1].delivery)

        triggers, _ = _mocked(
            pb.BatchResendTriggerDeliveriesResponse(
                queued_count=0,
                results=[
                    pb.BatchResendTriggerDeliveryResult(
                        msg_id="msg_1",
                        endpoint_id="ep_1",
                        outcome=pb.BATCH_RESEND_OUTCOME_NOT_FOUND,
                    )
                ],
            )
        )
        batch = triggers.batch_resend_deliveries([{"msg_id": "msg_1", "endpoint_id": "ep_1"}])
        self.assertIs(batch.results[0].outcome, TriggerDeliveryResendOutcome.NOT_FOUND)
        self.assertEqual(batch.queued_count, 0)


NOT_RETRIED = {
    "CreateTriggerSubscription": lambda t: t.create_subscription("conn_1", "t"),
    "SetTriggerSigningSecret": lambda t: t.set_signing_secret("conn_1", signing_secret="s" * 8),
    "GenerateTriggerSigningSecret": lambda t: t.generate_signing_secret("conn_1"),
    "BatchResendTriggerDeliveries": lambda t: t.batch_resend_deliveries(
        [{"msg_id": "msg_1", "endpoint_id": "ep_1"}]
    ),
    "RecoverTriggerDeliveries": lambda t: t.recover_deliveries("ep_1", since=T0),
}
RETRIED = {
    "ListAvailableTriggers": lambda t: t.list_available("conn_1"),
    "ListEligibleAccounts": lambda t: t.list_eligible_accounts("conn_1", "t"),
    "ListTriggerSubscriptions": lambda t: t.list_subscriptions("conn_1"),
    "BatchCreateTriggerSubscriptions": lambda t: t.batch_create_subscriptions("conn_1", "t"),
    "DeleteTriggerSubscription": lambda t: t.delete_subscription("conn_1", "trgs_1"),
    "BatchDeleteTriggerSubscriptions": lambda t: t.batch_delete_subscriptions("conn_1"),
    "GetTriggerActivity": lambda t: t.get_activity(),
    "GetTriggerUsage": lambda t: t.get_usage(period="7d"),
    "GetTriggerIngressEndpoint": lambda t: t.get_ingress_endpoint("conn_1"),
    "CreateTriggerIngressEndpoint": lambda t: t.create_ingress_endpoint("conn_1"),
    "ConfirmTriggerSigningSecretRotation": lambda t: t.confirm_signing_secret_rotation("conn_1"),
    "ListTriggerDeliveryAttemptsByEndpoint": lambda t: t.list_delivery_attempts_by_endpoint("ep_1"),
    "ListTriggerDeliveriesByEndpoint": lambda t: t.list_deliveries("ep_1"),
    "ListTriggerDeliveryAttemptsByMessage": lambda t: t.list_delivery_attempts_by_message(
        "ep_1", "msg_1"
    ),
    "LookupTriggerDelivery": lambda t: t.lookup_delivery("msg_1"),
    "BatchLookupTriggerDeliveries": lambda t: t.batch_lookup_deliveries(["msg_1"]),
}


def _real_core(rpc_name, side_effect):
    """Facade over a real CoreClient (no network) whose stub method raises/returns."""
    core = _make_core_client()
    low = TriggersClient.__new__(TriggersClient)
    low.core_client = core
    low.trigger_service = MagicMock()
    with_call = getattr(low.trigger_service, rpc_name).with_call
    with_call.side_effect = side_effect
    return ActionTriggers(triggers_client=low), with_call


class TestRetry(unittest.TestCase):
    def test_every_public_rpc_is_classified(self):
        stub_methods = {m.name for m in pb.DESCRIPTOR.services_by_name["TriggerService"].methods}
        wrapped = set(NOT_RETRIED) | set(RETRIED)
        self.assertEqual(len(wrapped), 21)
        self.assertTrue(wrapped <= stub_methods)

    def test_non_idempotent_calls_opt_out_of_unavailable_retry(self):
        for rpc, call in NOT_RETRIED.items():
            with self.subTest(rpc=rpc):
                triggers, core = _mocked()
                call(triggers)
                self.assertIs(core.grpc_exec.call_args.kwargs.get("retry_on_unavailable"), False)

    def test_other_calls_keep_the_default_retry(self):
        for rpc, call in RETRIED.items():
            with self.subTest(rpc=rpc):
                triggers, core = _mocked()
                call(triggers)
                self.assertNotIn("retry_on_unavailable", core.grpc_exec.call_args.kwargs)

    def test_unavailable_on_non_idempotent_call_is_sent_once(self):
        for rpc, call in NOT_RETRIED.items():
            with self.subTest(rpc=rpc):
                triggers, with_call = _real_core(rpc, _make_rpc_error(StatusCode.UNAVAILABLE))
                with (
                    patch("scalekit.core.time.sleep") as sleep,
                    self.assertRaises(ScalekitServiceUnavailableException),
                ):
                    call(triggers)
                self.assertEqual(with_call.call_count, 1)
                sleep.assert_not_called()

    def test_unavailable_on_idempotent_call_is_retried(self):
        response = (pb.GetTriggerActivityResponse(window_hours=24), MagicMock())
        triggers, with_call = _real_core(
            "GetTriggerActivity", [_make_rpc_error(StatusCode.UNAVAILABLE), response]
        )
        with patch("scalekit.core.time.sleep"):
            activity = triggers.get_activity()
        self.assertEqual(with_call.call_count, 2)
        self.assertEqual(activity.window, timedelta(hours=24))


class TestErrorPromotion(unittest.TestCase):
    CASES = (
        (
            "ListAvailableTriggers",
            lambda t: t.list_available("conn_x"),
            StatusCode.NOT_FOUND,
            "RESOURCE_NOT_FOUND",
            ScalekitNotFoundException,
        ),
        (
            "ListAvailableTriggers",
            lambda t: t.list_available("bad"),
            StatusCode.INVALID_ARGUMENT,
            "INVALID_ARGUMENT",
            ScalekitBadRequestException,
        ),
        (
            "CreateTriggerSubscription",
            lambda t: t.create_subscription("conn_1", "t"),
            StatusCode.ALREADY_EXISTS,
            "RESOURCE_ALREADY_EXISTS",
            ScalekitConflictException,
        ),
        (
            "CreateTriggerSubscription",
            lambda t: t.create_subscription("conn_1", "t"),
            StatusCode.UNAVAILABLE,
            None,
            ScalekitServiceUnavailableException,
        ),
        (
            "CreateTriggerIngressEndpoint",
            lambda t: t.create_ingress_endpoint("conn_1"),
            StatusCode.INVALID_ARGUMENT,
            "TRIGGER_INGRESS_NOT_APPLICABLE",
            ScalekitBadRequestException,
        ),
        (
            "CreateTriggerIngressEndpoint",
            lambda t: t.create_ingress_endpoint("conn_1"),
            StatusCode.FAILED_PRECONDITION,
            "TRIGGER_INGRESS_DEFINITIONS_UNAVAILABLE",
            ScalekitBadRequestException,
        ),
        (
            "GetTriggerIngressEndpoint",
            lambda t: t.get_ingress_endpoint("conn_1"),
            StatusCode.NOT_FOUND,
            "TRIGGER_INGRESS_ENDPOINT_NOT_CREATED",
            ScalekitNotFoundException,
        ),
        (
            "SetTriggerSigningSecret",
            lambda t: t.set_signing_secret("conn_1", signing_secret="x" * 8),
            StatusCode.INVALID_ARGUMENT,
            "TRIGGER_SIGNING_SECRET_GENERATED_ONLY",
            ScalekitBadRequestException,
        ),
        (
            "SetTriggerSigningSecret",
            lambda t: t.set_signing_secret("conn_1", signing_secret="x" * 8),
            StatusCode.ALREADY_EXISTS,
            "RESOURCE_ALREADY_EXISTS",
            ScalekitConflictException,
        ),
        (
            "GenerateTriggerSigningSecret",
            lambda t: t.generate_signing_secret("conn_1"),
            StatusCode.INVALID_ARGUMENT,
            "TRIGGER_SIGNING_SECRET_NOT_GENERATABLE",
            ScalekitBadRequestException,
        ),
        (
            "GetTriggerUsage",
            lambda t: t.get_usage(period="24h"),
            StatusCode.NOT_FOUND,
            "TRIGGER_USAGE_NOT_METERED",
            ScalekitNotFoundException,
        ),
        (
            "GetTriggerUsage",
            lambda t: t.get_usage(period="24h"),
            StatusCode.UNAVAILABLE,
            None,
            ScalekitServiceUnavailableException,
        ),
        (
            "BatchDeleteTriggerSubscriptions",
            lambda t: t.batch_delete_subscriptions("conn_1"),
            StatusCode.RESOURCE_EXHAUSTED,
            "RATE_LIMITED",
            ScalekitTooManyRequestsException,
        ),
        (
            "LookupTriggerDelivery",
            lambda t: t.lookup_delivery("msg_x"),
            StatusCode.NOT_FOUND,
            "NOT_FOUND",
            ScalekitNotFoundException,
        ),
        (
            "ListTriggerDeliveriesByEndpoint",
            lambda t: t.list_deliveries("ep_x"),
            StatusCode.INVALID_ARGUMENT,
            "INVALID_ARGUMENT",
            ScalekitBadRequestException,
        ),
        (
            "RecoverTriggerDeliveries",
            lambda t: t.recover_deliveries("ep_x", since=T0),
            StatusCode.NOT_FOUND,
            "RESOURCE_NOT_FOUND",
            ScalekitNotFoundException,
        ),
        (
            "RecoverTriggerDeliveries",
            lambda t: t.recover_deliveries("ep_1", since=T0),
            StatusCode.INTERNAL,
            "INTERNAL_ERROR",
            ScalekitInternalServerException,
        ),
        (
            "GetTriggerActivity",
            lambda t: t.get_activity(),
            StatusCode.DEADLINE_EXCEEDED,
            None,
            ScalekitGatewayTimeoutException,
        ),
        (
            "GetTriggerActivity",
            lambda t: t.get_activity(),
            StatusCode.CANCELLED,
            None,
            ScalekitCancelledException,
        ),
    )

    def test_server_errors_are_promoted_with_error_code(self):
        for rpc, call, status, error_code, exc in self.CASES:
            with self.subTest(rpc=rpc, status=status.name, error_code=error_code):
                triggers, with_call = _real_core(
                    rpc, _make_rpc_error(status, error_code=error_code)
                )
                with patch("scalekit.core.time.sleep"), self.assertRaises(exc) as ctx:
                    call(triggers)
                self.assertEqual(ctx.exception.error_code, error_code)
                if status != StatusCode.UNAVAILABLE:
                    self.assertEqual(with_call.call_count, 1)  # never retried

    def test_rate_limit_is_not_retried(self):
        triggers, with_call = _real_core(
            "ListTriggerDeliveriesByEndpoint",
            _make_rpc_error(StatusCode.RESOURCE_EXHAUSTED, error_code="RATE_LIMITED"),
        )
        with self.assertRaises(ScalekitTooManyRequestsException):
            triggers.list_deliveries("ep_1")
        self.assertEqual(with_call.call_count, 1)


class TestWiring(unittest.TestCase):
    def test_facade_without_client_raises_value_error(self):
        triggers = ActionClient(MagicMock(), MagicMock()).triggers
        with self.assertRaisesRegex(ValueError, "Triggers client not initialized"):
            triggers.list_available("conn_1")
        with self.assertRaises(ValueError):
            ActionTriggers().get_activity()

    def test_verify_event_still_works_without_client(self):
        from scalekit.common.exceptions import WebhookVerificationError

        with self.assertRaises(WebhookVerificationError):
            ActionTriggers().verify_event(b"{}", headers={}, secret="whsec_AAAA")

    def test_action_client_positional_arguments_unchanged(self):
        tools, accounts, mcp, providers = MagicMock(), MagicMock(), MagicMock(), MagicMock()
        actions = ActionClient(tools, accounts, mcp, providers)
        self.assertIs(actions.tools, tools)
        self.assertIs(actions.connected_accounts, accounts)
        self.assertIs(actions._mcp_client, mcp)
        self.assertIs(actions._providers_client, providers)

    def test_triggers_client_is_keyword_only(self):
        with self.assertRaises(TypeError):
            ActionClient(MagicMock(), MagicMock(), None, None, MagicMock())

    def test_scalekit_client_wires_one_triggers_client(self):
        from scalekit import ScalekitClient

        with patch("scalekit.client.CoreClient") as core_cls:
            core_cls.return_value = MagicMock()
            client = ScalekitClient("https://example.test", "cid", "secret")
        low = client.actions.triggers._triggers_client
        self.assertIsInstance(low, TriggersClient)
        self.assertIs(client.connect.triggers._triggers_client, low)
        self.assertFalse(hasattr(client, "triggers"))  # the low-level client stays private

    def test_api_version_header(self):
        from scalekit.core import CoreClient

        self.assertEqual(CoreClient.api_version, "20261029")


if __name__ == "__main__":
    unittest.main()

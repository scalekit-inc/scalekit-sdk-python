"""Low-level gRPC client for AgentKit triggers.

Use ``client.actions.triggers`` instead: it validates arguments, converts enums,
times and durations, and returns typed models. This class returns the generated
``(response, call)`` tuples and is wired privately into ``ActionClient``.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import cast

import grpc
from google.protobuf.empty_pb2 import Empty

from scalekit._convert import datetime_to_timestamp, require, str_list
from scalekit.core import CoreClient
from scalekit.v1.triggers import triggers_pb2 as pb
from scalekit.v1.triggers.triggers_pb2_grpc import TriggerServiceStub

__all__ = ["TriggersClient"]


class TriggersClient:
    """Low-level client for the trigger catalogue, subscriptions, ingress and deliveries.

    Every method returns ``(proto_response, grpc.Call)`` and raises the
    ``ScalekitServerException`` subclass that matches the server status. Required
    identifiers are checked before any request (``ValueError`` when empty). Create,
    set-secret, generate-secret, resend and recover calls are never retried on
    ``UNAVAILABLE``, because a retry could run them twice.

    Example:
        >>> response, _ = triggers_client.list_available_triggers("conn_123")
        >>> [t.name for t in response.triggers]
    """

    def __init__(self, core_client: CoreClient) -> None:
        self.core_client = core_client
        self.trigger_service = TriggerServiceStub(core_client.grpc_secure_channel)

    # Catalogue and subscriptions

    def list_available_triggers(
        self, connection_id: str
    ) -> tuple[pb.ListAvailableTriggersResponse, grpc.Call]:
        """List the triggers a connection offers. See ``ActionTriggers.list_available``."""
        require("connection_id", connection_id)
        return self.core_client.grpc_exec(
            self.trigger_service.ListAvailableTriggers.with_call,
            pb.ListAvailableTriggersRequest(connection_id=connection_id),
        )

    def list_eligible_accounts(
        self,
        connection_id: str,
        trigger_name: str,
        *,
        query: str | None = None,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> tuple[pb.ListEligibleAccountsResponse, grpc.Call]:
        """List connected accounts and whether each can subscribe to a trigger."""
        require("connection_id", connection_id)
        require("trigger_name", trigger_name)
        request = pb.ListEligibleAccountsRequest(
            connection_id=connection_id, trigger_name=trigger_name
        )
        if query is not None:
            request.query = query
        if page_size is not None:
            request.page_size = page_size
        if page_token is not None:
            request.page_token = page_token
        return self.core_client.grpc_exec(
            self.trigger_service.ListEligibleAccounts.with_call,
            request,
        )

    def list_trigger_subscriptions(
        self,
        connection_id: str,
        *,
        trigger_name: str | None = None,
        statuses: Sequence[int] | None = None,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> tuple[pb.ListTriggerSubscriptionsResponse, grpc.Call]:
        """List a connection's trigger subscriptions, one page at a time."""
        require("connection_id", connection_id)
        request = pb.ListTriggerSubscriptionsRequest(connection_id=connection_id)
        if trigger_name is not None:
            request.trigger_name = trigger_name
        if statuses is not None:
            request.statuses.extend(cast("Sequence[pb.TriggerSubscriptionStatus]", statuses))
        if page_size is not None:
            request.page_size = page_size
        if page_token is not None:
            request.page_token = page_token
        return self.core_client.grpc_exec(
            self.trigger_service.ListTriggerSubscriptions.with_call,
            request,
        )

    def create_trigger_subscription(
        self,
        connection_id: str,
        trigger_name: str,
        *,
        connected_account_id: str | None = None,
        interval_seconds: int | None = None,
        config: Mapping[str, str] | None = None,
    ) -> tuple[pb.TriggerSubscription, grpc.Call]:
        """Subscribe a connected account (or the connection) to a trigger. Not retried."""
        require("connection_id", connection_id)
        require("trigger_name", trigger_name)
        request = pb.CreateTriggerSubscriptionRequest(
            connection_id=connection_id, trigger_name=trigger_name
        )
        if connected_account_id is not None:
            request.connected_account_id = connected_account_id
        if interval_seconds is not None:
            request.interval_seconds = interval_seconds
        if config is not None:
            request.config.update(config)
        return self.core_client.grpc_exec(
            self.trigger_service.CreateTriggerSubscription.with_call,
            request,
            retry_on_unavailable=False,
        )

    def batch_create_trigger_subscriptions(
        self,
        connection_id: str,
        trigger_name: str,
        *,
        connected_account_ids: Sequence[str] | None = None,
        interval_seconds: int | None = None,
        config: Mapping[str, str] | None = None,
    ) -> tuple[pb.BatchCreateTriggerSubscriptionsResponse, grpc.Call]:
        """Subscribe many connected accounts to a trigger; outcomes are per account."""
        require("connection_id", connection_id)
        require("trigger_name", trigger_name)
        request = pb.BatchCreateTriggerSubscriptionsRequest(
            connection_id=connection_id, trigger_name=trigger_name
        )
        if connected_account_ids is not None:
            request.connected_account_ids.extend(
                str_list("connected_account_ids", connected_account_ids)
            )
        if interval_seconds is not None:
            request.interval_seconds = interval_seconds
        if config is not None:
            request.config.update(config)
        return self.core_client.grpc_exec(
            self.trigger_service.BatchCreateTriggerSubscriptions.with_call,
            request,
        )

    def delete_trigger_subscription(
        self, connection_id: str, subscription_id: str
    ) -> tuple[Empty, grpc.Call]:
        """Delete one trigger subscription."""
        require("connection_id", connection_id)
        require("subscription_id", subscription_id)
        return self.core_client.grpc_exec(
            self.trigger_service.DeleteTriggerSubscription.with_call,
            pb.DeleteTriggerSubscriptionRequest(
                connection_id=connection_id, subscription_id=subscription_id
            ),
        )

    def batch_delete_trigger_subscriptions(
        self,
        connection_id: str,
        *,
        subscription_ids: Sequence[str] | None = None,
        trigger_name: str | None = None,
        connected_account_ids: Sequence[str] | None = None,
    ) -> tuple[pb.BatchDeleteTriggerSubscriptionsResponse, grpc.Call]:
        """Delete many trigger subscriptions; outcomes are per subscription."""
        require("connection_id", connection_id)
        request = pb.BatchDeleteTriggerSubscriptionsRequest(connection_id=connection_id)
        if subscription_ids is not None:
            request.subscription_ids.extend(str_list("subscription_ids", subscription_ids))
        if trigger_name is not None:
            request.trigger_name = trigger_name
        if connected_account_ids is not None:
            request.connected_account_ids.extend(
                str_list("connected_account_ids", connected_account_ids)
            )
        return self.core_client.grpc_exec(
            self.trigger_service.BatchDeleteTriggerSubscriptions.with_call,
            request,
        )

    # Activity and usage

    def get_trigger_activity(self) -> tuple[pb.GetTriggerActivityResponse, grpc.Call]:
        """Read the environment's trigger event counts for the recent window."""
        return self.core_client.grpc_exec(
            self.trigger_service.GetTriggerActivity.with_call,
            pb.GetTriggerActivityRequest(),
        )

    def get_trigger_usage(
        self,
        *,
        period: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> tuple[pb.GetTriggerUsageResponse, grpc.Call]:
        """Read metered trigger deliveries for a preset period or a date range."""
        request = pb.GetTriggerUsageRequest()
        if period is not None:
            request.period = period
        if from_date is not None:
            setattr(request, "from", from_date)  # `from` is a Python keyword
        if to_date is not None:
            request.to = to_date
        return self.core_client.grpc_exec(
            self.trigger_service.GetTriggerUsage.with_call,
            request,
        )

    # Ingress endpoint and signing secret

    def get_trigger_ingress_endpoint(
        self, connection_id: str
    ) -> tuple[pb.TriggerIngressEndpoint, grpc.Call]:
        """Read a connection's webhook URL and signing-secret state."""
        require("connection_id", connection_id)
        return self.core_client.grpc_exec(
            self.trigger_service.GetTriggerIngressEndpoint.with_call,
            pb.GetTriggerIngressEndpointRequest(connection_id=connection_id),
        )

    def create_trigger_ingress_endpoint(
        self, connection_id: str
    ) -> tuple[pb.TriggerIngressEndpoint, grpc.Call]:
        """Create a connection's webhook URL, or return the existing one."""
        require("connection_id", connection_id)
        return self.core_client.grpc_exec(
            self.trigger_service.CreateTriggerIngressEndpoint.with_call,
            pb.CreateTriggerIngressEndpointRequest(connection_id=connection_id),
        )

    def set_trigger_signing_secret(
        self, connection_id: str, *, signing_secret: str
    ) -> tuple[pb.TriggerIngressEndpoint, grpc.Call]:
        """Store the provider's signing secret, or start a rotation. Not retried."""
        require("connection_id", connection_id)
        return self.core_client.grpc_exec(
            self.trigger_service.SetTriggerSigningSecret.with_call,
            pb.SetTriggerSigningSecretRequest(
                connection_id=connection_id, signing_secret=signing_secret
            ),
            retry_on_unavailable=False,
        )

    def confirm_trigger_signing_secret_rotation(
        self, connection_id: str, *, signing_secret_rotation_id: int | None = None
    ) -> tuple[pb.TriggerIngressEndpoint, grpc.Call]:
        """Confirm a signing-secret rotation so the previous secret stops being accepted."""
        require("connection_id", connection_id)
        request = pb.ConfirmTriggerSigningSecretRotationRequest(connection_id=connection_id)
        if signing_secret_rotation_id is not None:
            request.signing_secret_rotation_id = signing_secret_rotation_id
        return self.core_client.grpc_exec(
            self.trigger_service.ConfirmTriggerSigningSecretRotation.with_call,
            request,
        )

    def generate_trigger_signing_secret(
        self, connection_id: str
    ) -> tuple[pb.GenerateTriggerSigningSecretResponse, grpc.Call]:
        """Generate a signing secret for providers that use one Scalekit creates. Not retried."""
        require("connection_id", connection_id)
        return self.core_client.grpc_exec(
            self.trigger_service.GenerateTriggerSigningSecret.with_call,
            pb.GenerateTriggerSigningSecretRequest(connection_id=connection_id),
            retry_on_unavailable=False,
        )

    # Deliveries

    def list_trigger_delivery_attempts_by_endpoint(
        self, endpoint_id: str, *, page_size: int | None = None
    ) -> tuple[pb.ListTriggerDeliveryAttemptsByEndpointResponse, grpc.Call]:
        """List the most recent delivery attempts to one of your endpoints."""
        require("endpoint_id", endpoint_id)
        request = pb.ListTriggerDeliveryAttemptsByEndpointRequest(endpoint_id=endpoint_id)
        if page_size is not None:
            request.page_size = page_size
        return self.core_client.grpc_exec(
            self.trigger_service.ListTriggerDeliveryAttemptsByEndpoint.with_call,
            request,
        )

    def list_trigger_deliveries_by_endpoint(
        self,
        endpoint_id: str,
        *,
        page_size: int | None = None,
        page_token: str | None = None,
        status: int | None = None,
        channel: str | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
    ) -> tuple[pb.ListTriggerDeliveriesByEndpointResponse, grpc.Call]:
        """List trigger events sent to one of your endpoints, newest first."""
        require("endpoint_id", endpoint_id)
        request = pb.ListTriggerDeliveriesByEndpointRequest(endpoint_id=endpoint_id)
        if page_size is not None:
            request.page_size = page_size
        if page_token is not None:
            request.page_token = page_token
        if status is not None:
            request.status = cast("pb.TriggerDeliveryStatus", status)
        if channel is not None:
            request.channel = channel
        if after is not None:
            request.after.CopyFrom(datetime_to_timestamp(after, "after"))
        if before is not None:
            request.before.CopyFrom(datetime_to_timestamp(before, "before"))
        return self.core_client.grpc_exec(
            self.trigger_service.ListTriggerDeliveriesByEndpoint.with_call,
            request,
        )

    def list_trigger_delivery_attempts_by_message(
        self, endpoint_id: str, msg_id: str
    ) -> tuple[pb.ListTriggerDeliveryAttemptsByMessageResponse, grpc.Call]:
        """List every attempt to deliver one message to one endpoint."""
        require("endpoint_id", endpoint_id)
        require("msg_id", msg_id)
        return self.core_client.grpc_exec(
            self.trigger_service.ListTriggerDeliveryAttemptsByMessage.with_call,
            pb.ListTriggerDeliveryAttemptsByMessageRequest(endpoint_id=endpoint_id, msg_id=msg_id),
        )

    def lookup_trigger_delivery(
        self, delivery_id: str
    ) -> tuple[pb.LookupTriggerDeliveryResponse, grpc.Call]:
        """Look up one delivery by its ``msg_`` ID or its event ID."""
        require("delivery_id", delivery_id)
        return self.core_client.grpc_exec(
            self.trigger_service.LookupTriggerDelivery.with_call,
            pb.LookupTriggerDeliveryRequest(id=delivery_id),
        )

    def batch_lookup_trigger_deliveries(
        self, delivery_ids: Sequence[str]
    ) -> tuple[pb.BatchLookupTriggerDeliveriesResponse, grpc.Call]:
        """Look up several deliveries; outcomes are per ID."""
        request = pb.BatchLookupTriggerDeliveriesRequest()
        request.ids.extend(str_list("delivery_ids", delivery_ids))
        return self.core_client.grpc_exec(
            self.trigger_service.BatchLookupTriggerDeliveries.with_call,
            request,
        )

    def batch_resend_trigger_deliveries(
        self, targets: Sequence[pb.TriggerDeliveryResendTarget]
    ) -> tuple[pb.BatchResendTriggerDeliveriesResponse, grpc.Call]:
        """Send messages to endpoints again; outcomes are per target. Not retried."""
        request = pb.BatchResendTriggerDeliveriesRequest()
        request.targets.extend(targets)
        return self.core_client.grpc_exec(
            self.trigger_service.BatchResendTriggerDeliveries.with_call,
            request,
            retry_on_unavailable=False,
        )

    def recover_trigger_deliveries(
        self, endpoint_id: str, *, since: datetime, until: datetime | None = None
    ) -> tuple[pb.RecoverTriggerDeliveriesResponse, grpc.Call]:
        """Resend every failed message to an endpoint in a time range. Not retried."""
        require("endpoint_id", endpoint_id)
        require("since", since)
        request = pb.RecoverTriggerDeliveriesRequest(endpoint_id=endpoint_id)
        request.since.CopyFrom(datetime_to_timestamp(since, "since"))
        if until is not None:
            request.until.CopyFrom(datetime_to_timestamp(until, "until"))
        return self.core_client.grpc_exec(
            self.trigger_service.RecoverTriggerDeliveries.with_call,
            request,
            retry_on_unavailable=False,
        )

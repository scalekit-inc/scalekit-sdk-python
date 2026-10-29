"""Typed models returned by ``client.actions.triggers``.

Every model is frozen (fields cannot be reassigned; nested lists and dicts, such as
``TriggerSubscription.config``, are ordinary mutable copies) and keeps fields this SDK version does not know in
``model.model_extra``. Conventions shared by all of them:

* Enum fields hold the enum member for known values. A value added after this SDK
  version arrives as its name (a plain ``str``, for example ``"ARCHIVED"``), or as
  the decimal number when even the name is unknown, so compare with ``==`` and keep
  a default branch. The ``*_UNSPECIFIED`` value is ``None``.
* Instants are timezone-aware UTC ``datetime``; ``None`` when the server sent none.
* Durations are ``timedelta``. Intervals the server reports as ``0`` (not set) are
  ``None``.
* Empty page tokens are ``None``. Lists and maps are never ``None``.
"""

from __future__ import annotations

import datetime as _dt
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field

from scalekit._convert import enum_from_proto, seconds_from_proto, timestamp_from_proto
from scalekit.actions.models.trigger_event import DeliveryScope, DetectionMode, _parse_rfc3339
from scalekit.v1.triggers import triggers_pb2 as pb

__all__ = [
    "AccountHealth",
    "AccountHealthAction",
    "AccountHealthState",
    "AvailableTrigger",
    "BatchCreateTriggerSubscriptionResult",
    "BatchCreateTriggerSubscriptionsResponse",
    "BatchDeleteTriggerSubscriptionResult",
    "BatchDeleteTriggerSubscriptionsResponse",
    "BatchLookupTriggerDeliveriesResponse",
    "BatchLookupTriggerDeliveryResult",
    "BatchResendTriggerDeliveriesResponse",
    "BatchResendTriggerDeliveryResult",
    "ConfigField",
    "EligibleAccount",
    "GenerateTriggerSigningSecretResponse",
    "GetTriggerActivityResponse",
    "GetTriggerUsageResponse",
    "ListAvailableTriggersResponse",
    "ListEligibleAccountsResponse",
    "ListTriggerDeliveriesByEndpointResponse",
    "ListTriggerDeliveryAttemptsByEndpointResponse",
    "ListTriggerDeliveryAttemptsByMessageResponse",
    "ListTriggerSubscriptionsResponse",
    "LookupTriggerDeliveryResponse",
    "RecoverTriggerDeliveriesResponse",
    "RequiredScope",
    "TriggerDelivery",
    "TriggerDeliveryAttempt",
    "TriggerDeliveryAttemptStatus",
    "TriggerDeliveryAttemptTriggerType",
    "TriggerDeliveryLookupOutcome",
    "TriggerDeliveryResendOutcome",
    "TriggerDeliveryResendTarget",
    "TriggerDeliveryResendTargetParam",
    "TriggerDeliveryStatus",
    "TriggerIngressEndpoint",
    "TriggerPlatformCredentials",
    "TriggerPollErrorCode",
    "TriggerPollState",
    "TriggerRefusalCode",
    "TriggerSubscribeOutcome",
    "TriggerSubscription",
    "TriggerSubscriptionDeleteOutcome",
    "TriggerSubscriptionStatus",
    "TriggerUsageBucket",
    "TriggerUsageDay",
    "TriggerUsageHour",
    "TriggerUsagePeriod",
]

TriggerUsagePeriod = Literal["24h", "7d", "30d"]
"""A preset usage period ending now: ``"24h"`` (hourly), ``"7d"`` or ``"30d"`` (daily)."""


# Enums. Values are the proto value names without the enum-name prefix.


class TriggerPlatformCredentials(str, Enum):
    """Whether a trigger works on a connection that uses Scalekit's shared app."""

    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"


class TriggerRefusalCode(str, Enum):
    """Why a trigger is not available on a connection (``AvailableTrigger.refusal_code``)."""

    SHARED_APP = "SHARED_APP"
    POLL_CONNECTION_SCOPE = "POLL_CONNECTION_SCOPE"


class AccountHealthState(str, Enum):
    """Whether a connected account can receive trigger events."""

    READY = "READY"
    AWAITING_CONFIRMATION = "AWAITING_CONFIRMATION"
    WRONG_APP = "WRONG_APP"
    DISCONNECTED = "DISCONNECTED"
    NEEDS_REAUTHENTICATION = "NEEDS_REAUTHENTICATION"


class AccountHealthAction(str, Enum):
    """What to do to make an unhealthy connected account ready again."""

    RECONNECT = "RECONNECT"
    COMPLETE_SETUP = "COMPLETE_SETUP"


class TriggerSubscriptionStatus(str, Enum):
    """State of a trigger subscription. Also accepted as a filter by ``list_subscriptions``."""

    ACTIVE = "ACTIVE"
    THROTTLED = "THROTTLED"
    PAUSED = "PAUSED"
    PAUSED_CREDENTIAL = "PAUSED_CREDENTIAL"


class TriggerPollErrorCode(str, Enum):
    """Why the last poll of a poll-mode subscription failed."""

    RATE_LIMITED = "RATE_LIMITED"
    CREDENTIAL_REVOKED = "CREDENTIAL_REVOKED"
    INVALID_CONFIGURATION = "INVALID_CONFIGURATION"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    DELIVERY_FAILED = "DELIVERY_FAILED"
    TIMED_OUT = "TIMED_OUT"
    POLL_FAILED = "POLL_FAILED"


class TriggerSubscribeOutcome(str, Enum):
    """Per-account outcome of ``batch_create_subscriptions``."""

    CREATED = "CREATED"
    ALREADY_SUBSCRIBED = "ALREADY_SUBSCRIBED"
    REFUSED = "REFUSED"
    NOT_FOUND = "NOT_FOUND"
    FAILED = "FAILED"
    """Could not be created this time; safe to retry."""


class TriggerSubscriptionDeleteOutcome(str, Enum):
    """Per-subscription outcome of ``batch_delete_subscriptions``."""

    DELETED = "DELETED"
    NOT_FOUND = "NOT_FOUND"
    FAILED = "FAILED"
    NOT_ATTEMPTED = "NOT_ATTEMPTED"
    """The request ran out of time before this one; call again to delete it."""


class TriggerUsageBucket(str, Enum):
    """What each usage entry counts: a UTC day (``days``) or a UTC hour (``hours``)."""

    DAY = "DAY"
    HOUR = "HOUR"


class TriggerDeliveryStatus(str, Enum):
    """Delivery state of a message sent to one of your endpoints. Also a filter."""

    DELIVERED = "DELIVERED"
    PENDING = "PENDING"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


class TriggerDeliveryLookupOutcome(str, Enum):
    """Per-ID outcome of ``batch_lookup_deliveries``."""

    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    RATE_LIMITED = "RATE_LIMITED"
    FAILED = "FAILED"
    NOT_ATTEMPTED = "NOT_ATTEMPTED"


class TriggerDeliveryResendOutcome(str, Enum):
    """Per-target outcome of ``batch_resend_deliveries``."""

    QUEUED = "QUEUED"
    NOT_FOUND = "NOT_FOUND"
    RATE_LIMITED = "RATE_LIMITED"
    FAILED = "FAILED"
    NOT_ATTEMPTED = "NOT_ATTEMPTED"


class TriggerDeliveryAttemptTriggerType(str, Enum):
    """Whether a delivery attempt was scheduled automatically or started manually."""

    SCHEDULED = "SCHEDULED"
    MANUAL = "MANUAL"


class TriggerDeliveryAttemptStatus(str, Enum):
    """Result of one delivery attempt."""

    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    FAIL = "FAIL"
    SENDING = "SENDING"
    CANCELED = "CANCELED"


def _date_or_none(value: str) -> date | None:
    """A ``YYYY-MM-DD`` string as ``date``; ``None`` when empty or not a date."""
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _instant_or_none(value: str) -> datetime | None:
    """An RFC 3339 string as aware UTC ``datetime``; ``None`` when empty or malformed."""
    if not value:
        return None
    try:
        return _parse_rfc3339(value)
    except (ValueError, OverflowError):
        return None


class _TriggerModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")


# Catalogue


class RequiredScope(_TriggerModel):
    """An OAuth scope a trigger needs, and the grant it is checked against.

    Example:
        >>> [s.scope for s in trigger.required_scopes]
    """

    scope: str = ""
    grant: str = ""

    @classmethod
    def from_proto(cls, proto: pb.RequiredScope) -> RequiredScope:
        """Build from the generated message."""
        return cls(scope=proto.scope, grant=proto.grant)


class ConfigField(_TriggerModel):
    """A configuration value a trigger accepts in ``create_subscription(config=...)``.

    Example:
        >>> required = [f.key for f in trigger.config_fields if f.required]
    """

    key: str = ""
    display_name: str = ""
    help_text: str = ""
    placeholder: str = ""
    required: bool = False

    @classmethod
    def from_proto(cls, proto: pb.ConfigField) -> ConfigField:
        """Build from the generated message."""
        return cls(
            key=proto.key,
            display_name=proto.display_name,
            help_text=proto.help_text,
            placeholder=proto.placeholder,
            required=proto.required,
        )


class AvailableTrigger(_TriggerModel):
    """A trigger a connection offers, and whether it can be used there.

    Attributes:
        name: Pass this as ``trigger_name``.
        mode: ``DetectionMode.WEBHOOK`` (the provider pushes events) or
            ``DetectionMode.POLL`` (Scalekit polls on an interval).
        min_interval: Shortest poll interval allowed; ``None`` for webhook triggers.
        default_interval: Poll interval used when none is requested; ``None`` for
            webhook triggers.
        available: ``False`` when the trigger cannot be used on this connection;
            ``reason``, ``remedy`` and ``refusal_code`` say why.
        delivery_scope: Whether events are delivered per connected account or for the
            whole connection.
        requires_signing_secret: The provider signs its events with a secret you set
            with ``set_signing_secret``.

    Example:
        >>> page = client.actions.triggers.list_available("conn_123")
        >>> usable = [t.name for t in page.triggers if t.available]
    """

    name: str = ""
    display_name: str = ""
    description: str = ""
    provider: str = ""
    mode: DetectionMode | str | None = None
    required_scopes: list[RequiredScope] = Field(default_factory=list)
    min_interval: timedelta | None = None
    default_interval: timedelta | None = None
    config_fields: list[ConfigField] = Field(default_factory=list)
    available: bool = False
    reason: str = ""
    remedy: str = ""
    delivery_scope: DeliveryScope | str | None = None
    platform_credentials: TriggerPlatformCredentials | str | None = None
    refusal_code: TriggerRefusalCode | str | None = None
    requires_signing_secret: bool = False
    register_hint: str = ""
    secret_hint: str = ""
    provides_bearer_secret: bool = False

    @classmethod
    def from_proto(cls, proto: pb.AvailableTrigger) -> AvailableTrigger:
        """Build from the generated message."""
        return cls(
            name=proto.name,
            display_name=proto.display_name,
            description=proto.description,
            provider=proto.provider,
            mode=enum_from_proto(DetectionMode, pb.TriggerMode, proto.mode),
            required_scopes=[RequiredScope.from_proto(s) for s in proto.required_scopes],
            min_interval=seconds_from_proto(proto.min_interval_seconds),
            default_interval=seconds_from_proto(proto.default_interval_seconds),
            config_fields=[ConfigField.from_proto(f) for f in proto.config_fields],
            available=proto.available,
            reason=proto.reason,
            remedy=proto.remedy,
            delivery_scope=enum_from_proto(
                DeliveryScope, pb.TriggerDeliveryScope, proto.delivery_scope
            ),
            platform_credentials=enum_from_proto(
                TriggerPlatformCredentials,
                pb.TriggerPlatformCredentials,
                proto.platform_credentials,
            ),
            refusal_code=enum_from_proto(
                TriggerRefusalCode, pb.TriggerRefusalCode, proto.refusal_code
            ),
            requires_signing_secret=proto.requires_signing_secret,
            register_hint=proto.register_hint,
            secret_hint=proto.secret_hint,
            provides_bearer_secret=proto.provides_bearer_secret,
        )


class ListAvailableTriggersResponse(_TriggerModel):
    """Every trigger a connection offers (not paginated).

    Example:
        >>> page = client.actions.triggers.list_available("conn_123")
        >>> page.connection_uses_shared_app
    """

    triggers: list[AvailableTrigger] = Field(default_factory=list)
    connection_uses_shared_app: bool = False

    @classmethod
    def from_proto(cls, proto: pb.ListAvailableTriggersResponse) -> ListAvailableTriggersResponse:
        """Build from the generated message."""
        return cls(
            triggers=[AvailableTrigger.from_proto(t) for t in proto.triggers],
            connection_uses_shared_app=proto.connection_uses_shared_app,
        )


class AccountHealth(_TriggerModel):
    """Whether a connected account can receive trigger events, and how to fix it.

    Example:
        >>> if account.health and account.health.action == AccountHealthAction.RECONNECT:
        ...     prompt_reconnect(account.id)
    """

    state: AccountHealthState | str | None = None
    reason: str = ""
    remedy: str = ""
    action: AccountHealthAction | str | None = None
    blocks_tool_calls: bool = False

    @classmethod
    def from_proto(cls, proto: pb.AccountHealth) -> AccountHealth:
        """Build from the generated message."""
        return cls(
            state=enum_from_proto(AccountHealthState, pb.AccountHealthState, proto.state),
            reason=proto.reason,
            remedy=proto.remedy,
            action=enum_from_proto(AccountHealthAction, pb.AccountHealthAction, proto.action),
            blocks_tool_calls=proto.blocks_tool_calls,
        )


class EligibleAccount(_TriggerModel):
    """A connected account and whether it can subscribe to the trigger.

    Example:
        >>> ids = [a.id for a in page.accounts if a.eligible]
    """

    id: str = ""
    identifier: str = ""
    eligible: bool = False
    reason: str = ""
    remedy: str = ""
    health: AccountHealth | None = None

    @classmethod
    def from_proto(cls, proto: pb.EligibleAccount) -> EligibleAccount:
        """Build from the generated message."""
        return cls(
            id=proto.id,
            identifier=proto.identifier,
            eligible=proto.eligible,
            reason=proto.reason,
            remedy=proto.remedy,
            health=AccountHealth.from_proto(proto.health) if proto.HasField("health") else None,
        )


class ListEligibleAccountsResponse(_TriggerModel):
    """One page of connected accounts for a trigger.

    Example:
        >>> page = client.actions.triggers.list_eligible_accounts("conn_123", "item.created")
        >>> if page.next_page_token:
        ...     page = client.actions.triggers.list_eligible_accounts(
        ...         "conn_123", "item.created", page_token=page.next_page_token)
    """

    accounts: list[EligibleAccount] = Field(default_factory=list)
    next_page_token: str | None = None
    prev_page_token: str | None = None
    total_size: int = 0

    @classmethod
    def from_proto(cls, proto: pb.ListEligibleAccountsResponse) -> ListEligibleAccountsResponse:
        """Build from the generated message."""
        return cls(
            accounts=[EligibleAccount.from_proto(a) for a in proto.accounts],
            next_page_token=proto.next_page_token or None,
            prev_page_token=proto.prev_page_token or None,
            total_size=proto.total_size,
        )


# Subscriptions


class TriggerPollState(_TriggerModel):
    """Progress of a poll-mode subscription.

    Example:
        >>> if sub.poll_state and sub.poll_state.consecutive_failures:
        ...     print(sub.poll_state.last_error_code, sub.poll_state.last_error)
    """

    last_run_at: datetime | None = None
    last_error: str = ""
    consecutive_failures: int = 0
    backoff_until: datetime | None = None
    watermark_updated_at: datetime | None = None
    last_error_code: TriggerPollErrorCode | str | None = None

    @classmethod
    def from_proto(cls, proto: pb.TriggerPollState) -> TriggerPollState:
        """Build from the generated message."""
        return cls(
            last_run_at=timestamp_from_proto(proto, "last_run_at"),
            last_error=proto.last_error,
            consecutive_failures=proto.consecutive_failures,
            backoff_until=timestamp_from_proto(proto, "backoff_until"),
            watermark_updated_at=timestamp_from_proto(proto, "watermark_updated_at"),
            last_error_code=enum_from_proto(
                TriggerPollErrorCode, pb.TriggerPollErrorCode, proto.last_error_code
            ),
        )


class TriggerSubscription(_TriggerModel):
    """A connected account (or a whole connection) subscribed to a trigger.

    Attributes:
        connected_account_id: ``""`` for a connection-scoped subscription.
        requested_interval: The poll interval asked for; ``None`` when none was.
        effective_interval: The poll interval in use; ``None`` for webhook triggers.
        account_health: ``None`` when the server did not report one.

    Example:
        >>> sub = client.actions.triggers.create_subscription(
        ...     "conn_123", "item.created", connected_account_id="ca_123")
        >>> sub.id, sub.status
    """

    id: str = ""
    connected_account_id: str = ""
    connection_id: str = ""
    provider: str = ""
    trigger_name: str = ""
    status: TriggerSubscriptionStatus | str | None = None
    requested_interval: timedelta | None = None
    effective_interval: timedelta | None = None
    config: dict[str, str] = Field(default_factory=dict)
    delivery_scope: DeliveryScope | str | None = None
    connected_account_identifier: str = ""
    created_at: datetime | None = None
    poll_state: TriggerPollState | None = None
    account_health: AccountHealthState | str | None = None

    @classmethod
    def from_proto(cls, proto: pb.TriggerSubscription) -> TriggerSubscription:
        """Build from the generated message."""
        return cls(
            id=proto.id,
            connected_account_id=proto.connected_account_id,
            connection_id=proto.connection_id,
            provider=proto.provider,
            trigger_name=proto.trigger_name,
            status=enum_from_proto(
                TriggerSubscriptionStatus, pb.TriggerSubscriptionStatus, proto.status
            ),
            requested_interval=seconds_from_proto(proto.requested_interval_seconds),
            effective_interval=seconds_from_proto(proto.effective_interval_seconds),
            config=dict(proto.config),
            delivery_scope=enum_from_proto(
                DeliveryScope, pb.TriggerDeliveryScope, proto.delivery_scope
            ),
            connected_account_identifier=proto.connected_account_identifier,
            created_at=timestamp_from_proto(proto, "created_at"),
            poll_state=(
                TriggerPollState.from_proto(proto.poll_state)
                if proto.HasField("poll_state")
                else None
            ),
            account_health=(
                enum_from_proto(AccountHealthState, pb.AccountHealthState, proto.account_health)
                if proto.HasField("account_health")
                else None
            ),
        )


class ListTriggerSubscriptionsResponse(_TriggerModel):
    """One page of a connection's trigger subscriptions.

    Attributes:
        status_counts: Subscriptions per status name (for example ``"ACTIVE"``) for
            the connection and trigger, ignoring the ``statuses`` filter.

    Example:
        >>> page = client.actions.triggers.list_subscriptions("conn_123")
        >>> page.total_size, page.status_counts.get("ACTIVE", 0)
    """

    subscriptions: list[TriggerSubscription] = Field(default_factory=list)
    next_page_token: str | None = None
    prev_page_token: str | None = None
    total_size: int = 0
    status_counts: dict[str, int] = Field(default_factory=dict)

    @classmethod
    def from_proto(
        cls, proto: pb.ListTriggerSubscriptionsResponse
    ) -> ListTriggerSubscriptionsResponse:
        """Build from the generated message."""
        return cls(
            subscriptions=[TriggerSubscription.from_proto(s) for s in proto.subscriptions],
            next_page_token=proto.next_page_token or None,
            prev_page_token=proto.prev_page_token or None,
            total_size=proto.total_size,
            status_counts=dict(proto.status_counts),
        )


class BatchCreateTriggerSubscriptionResult(_TriggerModel):
    """Outcome for one connected account in ``batch_create_subscriptions``.

    Attributes:
        connected_account_id: ``""`` for a connection-scoped trigger.
        subscription: Set when ``outcome`` is ``CREATED`` or ``ALREADY_SUBSCRIBED``.

    Example:
        >>> failed = [r.connected_account_id for r in batch.results
        ...           if r.outcome == TriggerSubscribeOutcome.FAILED]
    """

    connected_account_id: str = ""
    outcome: TriggerSubscribeOutcome | str | None = None
    subscription: TriggerSubscription | None = None
    reason: str = ""

    @classmethod
    def from_proto(
        cls, proto: pb.BatchCreateTriggerSubscriptionResult
    ) -> BatchCreateTriggerSubscriptionResult:
        """Build from the generated message."""
        return cls(
            connected_account_id=proto.connected_account_id,
            outcome=enum_from_proto(
                TriggerSubscribeOutcome, pb.BatchSubscribeOutcome, proto.outcome
            ),
            subscription=(
                TriggerSubscription.from_proto(proto.subscription)
                if proto.HasField("subscription")
                else None
            ),
            reason=proto.reason,
        )


class BatchCreateTriggerSubscriptionsResponse(_TriggerModel):
    """Per-account outcomes of ``batch_create_subscriptions``.

    Example:
        >>> batch.created_count, [r.outcome for r in batch.results]
    """

    results: list[BatchCreateTriggerSubscriptionResult] = Field(default_factory=list)
    created_count: int = 0

    @classmethod
    def from_proto(
        cls, proto: pb.BatchCreateTriggerSubscriptionsResponse
    ) -> BatchCreateTriggerSubscriptionsResponse:
        """Build from the generated message."""
        return cls(
            results=[BatchCreateTriggerSubscriptionResult.from_proto(r) for r in proto.results],
            created_count=proto.created_count,
        )


class BatchDeleteTriggerSubscriptionResult(_TriggerModel):
    """Outcome for one subscription in ``batch_delete_subscriptions``.

    Example:
        >>> retry = [r.subscription_id for r in batch.results
        ...          if r.outcome == TriggerSubscriptionDeleteOutcome.NOT_ATTEMPTED]
    """

    subscription_id: str = ""
    connected_account_id: str = ""
    outcome: TriggerSubscriptionDeleteOutcome | str | None = None
    reason: str = ""

    @classmethod
    def from_proto(
        cls, proto: pb.BatchDeleteTriggerSubscriptionResult
    ) -> BatchDeleteTriggerSubscriptionResult:
        """Build from the generated message."""
        return cls(
            subscription_id=proto.subscription_id,
            connected_account_id=proto.connected_account_id,
            outcome=enum_from_proto(
                TriggerSubscriptionDeleteOutcome, pb.BatchDeleteOutcome, proto.outcome
            ),
            reason=proto.reason,
        )


class BatchDeleteTriggerSubscriptionsResponse(_TriggerModel):
    """Per-subscription outcomes of ``batch_delete_subscriptions``.

    Example:
        >>> batch.deleted_count
    """

    results: list[BatchDeleteTriggerSubscriptionResult] = Field(default_factory=list)
    deleted_count: int = 0

    @classmethod
    def from_proto(
        cls, proto: pb.BatchDeleteTriggerSubscriptionsResponse
    ) -> BatchDeleteTriggerSubscriptionsResponse:
        """Build from the generated message."""
        return cls(
            results=[BatchDeleteTriggerSubscriptionResult.from_proto(r) for r in proto.results],
            deleted_count=proto.deleted_count,
        )


# Activity and usage


class GetTriggerActivityResponse(_TriggerModel):
    """What happened to this environment's trigger events in the recent window.

    Attributes:
        counts: Event counts keyed by outcome (``received``, ``filtered``,
            ``unresolved``, ``delivered``, ``delivery_failed``, ``duplicate``,
            ``signature_failed``, ``discarded``); every key is present.
        window: How far back the counts reach, ending now.
        signature_banner: Many recent events failed signature verification; the
            signing secret probably does not match the provider's.
        degraded: Some counts could not be read; do not read zeroes as "nothing".

    Example:
        >>> activity = client.actions.triggers.get_activity()
        >>> activity.counts["delivered"], activity.window
    """

    counts: dict[str, int] = Field(default_factory=dict)
    window: timedelta = timedelta(0)
    signature_banner: bool = False
    degraded: bool = False
    explains_individual_events: bool = False
    delivery_details_path: str = ""

    @classmethod
    def from_proto(cls, proto: pb.GetTriggerActivityResponse) -> GetTriggerActivityResponse:
        """Build from the generated message."""
        return cls(
            counts=dict(proto.counts),
            window=timedelta(hours=proto.window_hours),
            signature_banner=proto.signature_banner,
            degraded=proto.degraded,
            explains_individual_events=proto.explains_individual_events,
            delivery_details_path=proto.delivery_details_path,
        )


class TriggerUsageDay(_TriggerModel):
    """Metered trigger deliveries on one UTC calendar day.

    ``date`` is ``None`` when absent or unparseable.

    Example:
        >>> {d.date: d.units for d in usage.days}
    """

    date: _dt.date | None = None
    units: int = 0

    @classmethod
    def from_proto(cls, proto: pb.TriggerUsageDay) -> TriggerUsageDay:
        """Build from the generated message."""
        return cls(date=_date_or_none(proto.date), units=proto.units)


class TriggerUsageHour(_TriggerModel):
    """Metered trigger deliveries in one UTC clock hour starting at ``start``.

    ``start`` is an aware UTC ``datetime``, or ``None`` when absent or unparseable.

    Example:
        >>> {h.start: h.units for h in usage.hours}
    """

    start: datetime | None = None
    units: int = 0

    @classmethod
    def from_proto(cls, proto: pb.TriggerUsageHour) -> TriggerUsageHour:
        """Build from the generated message."""
        return cls(start=_instant_or_none(proto.start), units=proto.units)


class GetTriggerUsageResponse(_TriggerModel):
    """Metered trigger deliveries per UTC day, or per hour for ``period="24h"``.

    Days or hours without deliveries are absent, not zero.

    Attributes:
        from_date: First UTC date of the range read (the proto field ``from``);
            ``None`` when absent or unparseable.
        to_date: Last UTC date of the range read (the proto field ``to``); ``None``
            when absent or unparseable.
        today: The server's current UTC date, whose count is still growing; ``None``
            when absent or unparseable.
        period: The ``period`` requested, or ``None`` for a date-range request.
        bucket: ``HOUR`` for ``24h``, ``DAY`` for ``7d``/``30d``, ``None`` for a
            date-range request (counted by day).
        current_hour: For ``24h``, the start of the hour in progress (aware UTC);
            ``None`` for other requests, or when absent or unparseable.

    Example:
        >>> usage = client.actions.triggers.get_usage(period="7d")
        >>> sum(d.units for d in usage.days)
    """

    from_date: date | None = None
    to_date: date | None = None
    today: date | None = None
    days: list[TriggerUsageDay] = Field(default_factory=list)
    period: str | None = None
    bucket: TriggerUsageBucket | str | None = None
    hours: list[TriggerUsageHour] = Field(default_factory=list)
    current_hour: datetime | None = None

    @classmethod
    def from_proto(cls, proto: pb.GetTriggerUsageResponse) -> GetTriggerUsageResponse:
        """Build from the generated message."""
        return cls(
            from_date=_date_or_none(getattr(proto, "from")),
            to_date=_date_or_none(proto.to),
            today=_date_or_none(proto.today),
            days=[TriggerUsageDay.from_proto(d) for d in proto.days],
            period=proto.period or None,
            bucket=enum_from_proto(TriggerUsageBucket, pb.TriggerUsageBucket, proto.bucket),
            hours=[TriggerUsageHour.from_proto(h) for h in proto.hours],
            current_hour=_instant_or_none(proto.current_hour),
        )


# Ingress endpoint and signing secret


class TriggerIngressEndpoint(_TriggerModel):
    """The webhook URL a provider sends a connection's events to.

    Never carries the signing secret itself.

    Attributes:
        url: Paste into the provider's app configuration. It ends in a token unique to
            the connection, so treat it as confidential; it is left out of ``repr()``.
        masked_signing_secret: The stored secret with all but its last four characters
            hidden, or ``""`` when none is stored.
        rotation_in_progress: The previous secret is still accepted.
        previous_signing_secret_expires_at: When the previous secret stops being
            accepted; ``None`` when no rotation is in progress.
        signing_secret_rotation_id: The latest rotation; pass it to
            ``confirm_signing_secret_rotation``. ``0`` when none ever started.

    Example:
        >>> endpoint = client.actions.triggers.create_ingress_endpoint("conn_123")
        >>> endpoint.signing_secret_configured
    """

    id: str = ""
    connection_id: str = ""
    url: str = Field(default="", repr=False)
    signing_secret_configured: bool = False
    masked_signing_secret: str = ""
    rotation_in_progress: bool = False
    previous_signing_secret_expires_at: datetime | None = None
    signing_secret_rotation_id: int = 0

    @classmethod
    def from_proto(cls, proto: pb.TriggerIngressEndpoint) -> TriggerIngressEndpoint:
        """Build from the generated message."""
        return cls(
            id=proto.id,
            connection_id=proto.connection_id,
            url=proto.url,
            signing_secret_configured=proto.signing_secret_configured,
            masked_signing_secret=proto.masked_signing_secret,
            rotation_in_progress=proto.rotation_in_progress,
            previous_signing_secret_expires_at=timestamp_from_proto(
                proto, "previous_signing_secret_expires_at"
            ),
            signing_secret_rotation_id=proto.signing_secret_rotation_id,
        )


class GenerateTriggerSigningSecretResponse(_TriggerModel):
    """A signing secret Scalekit generated, returned in plaintext this once.

    ``signing_secret`` and ``url_with_secret`` are left out of ``repr()`` so they do
    not end up in logs by accident; read them explicitly and store them securely.

    Example:
        >>> generated = client.actions.triggers.generate_signing_secret("conn_123")
        >>> store_secret(generated.signing_secret)
    """

    endpoint: TriggerIngressEndpoint | None = None
    signing_secret: str = Field(default="", repr=False)
    url_with_secret: str = Field(default="", repr=False)

    @classmethod
    def from_proto(
        cls, proto: pb.GenerateTriggerSigningSecretResponse
    ) -> GenerateTriggerSigningSecretResponse:
        """Build from the generated message."""
        return cls(
            endpoint=(
                TriggerIngressEndpoint.from_proto(proto.endpoint)
                if proto.HasField("endpoint")
                else None
            ),
            signing_secret=proto.signing_secret,
            url_with_secret=proto.url_with_secret,
        )


# Deliveries


class TriggerDeliveryAttempt(_TriggerModel):
    """One attempt to deliver a message to one of your endpoints.

    Attributes:
        response: Your endpoint's response body, possibly truncated
            (``response_truncated``).
        response_duration: How long your endpoint took to answer.

    Example:
        >>> [(a.status, a.response_status_code) for a in page.attempts]
    """

    id: str = ""
    endpoint_id: str = ""
    msg_id: str = ""
    status: TriggerDeliveryAttemptStatus | str | None = None
    response_status_code: int = 0
    response: str = ""
    timestamp: datetime | None = None
    response_duration: timedelta = timedelta(0)
    trigger_type: TriggerDeliveryAttemptTriggerType | str | None = None
    response_truncated: bool = False
    endpoint_url: str = ""

    @classmethod
    def from_proto(cls, proto: pb.TriggerDeliveryAttempt) -> TriggerDeliveryAttempt:
        """Build from the generated message."""
        return cls(
            id=proto.id,
            endpoint_id=proto.endpoint_id,
            msg_id=proto.msg_id,
            status=enum_from_proto(
                TriggerDeliveryAttemptStatus, pb.TriggerDeliveryAttemptStatus, proto.status
            ),
            response_status_code=proto.response_status_code,
            response=proto.response,
            timestamp=timestamp_from_proto(proto, "timestamp"),
            response_duration=timedelta(milliseconds=proto.response_duration_ms),
            trigger_type=enum_from_proto(
                TriggerDeliveryAttemptTriggerType,
                pb.TriggerDeliveryAttemptTriggerType,
                proto.trigger_type,
            ),
            response_truncated=proto.response_truncated,
            endpoint_url=proto.endpoint_url,
        )


class TriggerDelivery(_TriggerModel):
    """A trigger event message sent to one of your endpoints.

    Example:
        >>> failed = [d.msg_id for d in page.deliveries
        ...           if d.status == TriggerDeliveryStatus.FAILED]
    """

    msg_id: str = ""
    event_id: str = ""
    message_timestamp: datetime | None = None
    status: TriggerDeliveryStatus | str | None = None
    next_attempt_at: datetime | None = None
    subscription_id: str = ""
    trigger_name: str = ""
    trigger_mode: DetectionMode | str | None = None
    connection_id: str = ""
    connection_provider: str = ""
    connection_key_id: str = ""
    endpoint_id: str = ""

    @classmethod
    def from_proto(cls, proto: pb.TriggerDelivery) -> TriggerDelivery:
        """Build from the generated message."""
        return cls(
            msg_id=proto.msg_id,
            event_id=proto.event_id,
            message_timestamp=timestamp_from_proto(proto, "message_timestamp"),
            status=enum_from_proto(TriggerDeliveryStatus, pb.TriggerDeliveryStatus, proto.status),
            next_attempt_at=timestamp_from_proto(proto, "next_attempt_at"),
            subscription_id=proto.subscription_id,
            trigger_name=proto.trigger_name,
            trigger_mode=enum_from_proto(DetectionMode, pb.TriggerMode, proto.trigger_mode),
            connection_id=proto.connection_id,
            connection_provider=proto.connection_provider,
            connection_key_id=proto.connection_key_id,
            endpoint_id=proto.endpoint_id,
        )


class ListTriggerDeliveriesByEndpointResponse(_TriggerModel):
    """One page of messages sent to an endpoint, newest first.

    Example:
        >>> page = client.actions.triggers.list_deliveries("ep_123", page_size=50)
        >>> page.next_page_token
    """

    deliveries: list[TriggerDelivery] = Field(default_factory=list)
    next_page_token: str | None = None

    @classmethod
    def from_proto(
        cls, proto: pb.ListTriggerDeliveriesByEndpointResponse
    ) -> ListTriggerDeliveriesByEndpointResponse:
        """Build from the generated message."""
        return cls(
            deliveries=[TriggerDelivery.from_proto(d) for d in proto.deliveries],
            next_page_token=proto.next_page_token or None,
        )


class ListTriggerDeliveryAttemptsByEndpointResponse(_TriggerModel):
    """The most recent delivery attempts to an endpoint (one page, no token).

    Example:
        >>> page = client.actions.triggers.list_delivery_attempts_by_endpoint("ep_123")
        >>> len(page.attempts)
    """

    attempts: list[TriggerDeliveryAttempt] = Field(default_factory=list)

    @classmethod
    def from_proto(
        cls, proto: pb.ListTriggerDeliveryAttemptsByEndpointResponse
    ) -> ListTriggerDeliveryAttemptsByEndpointResponse:
        """Build from the generated message."""
        return cls(attempts=[TriggerDeliveryAttempt.from_proto(a) for a in proto.attempts])


class ListTriggerDeliveryAttemptsByMessageResponse(_TriggerModel):
    """Every attempt to deliver one message to one endpoint, oldest first.

    Attributes:
        truncated: More attempts exist than were returned.

    Example:
        >>> page = client.actions.triggers.list_delivery_attempts_by_message("ep_1", "msg_1")
        >>> page.attempts[-1].status
    """

    attempts: list[TriggerDeliveryAttempt] = Field(default_factory=list)
    truncated: bool = False

    @classmethod
    def from_proto(
        cls, proto: pb.ListTriggerDeliveryAttemptsByMessageResponse
    ) -> ListTriggerDeliveryAttemptsByMessageResponse:
        """Build from the generated message."""
        return cls(
            attempts=[TriggerDeliveryAttempt.from_proto(a) for a in proto.attempts],
            truncated=proto.truncated,
        )


class LookupTriggerDeliveryResponse(_TriggerModel):
    """One delivered message and its attempts, found by message ID or event ID.

    Example:
        >>> found = client.actions.triggers.lookup_delivery("msg_123")
        >>> found.trigger_name, [a.status for a in found.attempts]
    """

    msg_id: str = ""
    event_id: str = ""
    message_timestamp: datetime | None = None
    subscription_id: str = ""
    trigger_name: str = ""
    trigger_mode: DetectionMode | str | None = None
    connection_id: str = ""
    connection_provider: str = ""
    connection_key_id: str = ""
    attempts: list[TriggerDeliveryAttempt] = Field(default_factory=list)
    truncated: bool = False

    @classmethod
    def from_proto(cls, proto: pb.LookupTriggerDeliveryResponse) -> LookupTriggerDeliveryResponse:
        """Build from the generated message."""
        return cls(
            msg_id=proto.msg_id,
            event_id=proto.event_id,
            message_timestamp=timestamp_from_proto(proto, "message_timestamp"),
            subscription_id=proto.subscription_id,
            trigger_name=proto.trigger_name,
            trigger_mode=enum_from_proto(DetectionMode, pb.TriggerMode, proto.trigger_mode),
            connection_id=proto.connection_id,
            connection_provider=proto.connection_provider,
            connection_key_id=proto.connection_key_id,
            attempts=[TriggerDeliveryAttempt.from_proto(a) for a in proto.attempts],
            truncated=proto.truncated,
        )


class BatchLookupTriggerDeliveryResult(_TriggerModel):
    """Outcome for one ID in ``batch_lookup_deliveries``.

    Example:
        >>> found = [r.delivery for r in batch.results if r.delivery is not None]
    """

    id: str = ""
    outcome: TriggerDeliveryLookupOutcome | str | None = None
    reason: str = ""
    delivery: LookupTriggerDeliveryResponse | None = None

    @classmethod
    def from_proto(
        cls, proto: pb.BatchLookupTriggerDeliveryResult
    ) -> BatchLookupTriggerDeliveryResult:
        """Build from the generated message."""
        return cls(
            id=proto.id,
            outcome=enum_from_proto(
                TriggerDeliveryLookupOutcome, pb.BatchLookupOutcome, proto.outcome
            ),
            reason=proto.reason,
            delivery=(
                LookupTriggerDeliveryResponse.from_proto(proto.delivery)
                if proto.HasField("delivery")
                else None
            ),
        )


class BatchLookupTriggerDeliveriesResponse(_TriggerModel):
    """Per-ID outcomes of ``batch_lookup_deliveries``.

    Example:
        >>> batch.found_count
    """

    results: list[BatchLookupTriggerDeliveryResult] = Field(default_factory=list)
    found_count: int = 0

    @classmethod
    def from_proto(
        cls, proto: pb.BatchLookupTriggerDeliveriesResponse
    ) -> BatchLookupTriggerDeliveriesResponse:
        """Build from the generated message."""
        return cls(
            results=[BatchLookupTriggerDeliveryResult.from_proto(r) for r in proto.results],
            found_count=proto.found_count,
        )


class TriggerDeliveryResendTarget(_TriggerModel):
    """A message to send again to an endpoint, for ``batch_resend_deliveries``.

    A ``TriggerDeliveryResendTargetParam`` dict is accepted too.

    Example:
        >>> TriggerDeliveryResendTarget(msg_id="msg_123", endpoint_id="ep_123")
    """

    msg_id: str
    endpoint_id: str


class TriggerDeliveryResendTargetParam(TypedDict):
    """``{"msg_id": ..., "endpoint_id": ...}``, the dict form of a resend target.

    Example:
        >>> target: TriggerDeliveryResendTargetParam = {"msg_id": "msg_1", "endpoint_id": "ep_1"}
    """

    msg_id: str
    endpoint_id: str


class BatchResendTriggerDeliveryResult(_TriggerModel):
    """Outcome for one target in ``batch_resend_deliveries``.

    Example:
        >>> queued = [r.msg_id for r in batch.results
        ...           if r.outcome == TriggerDeliveryResendOutcome.QUEUED]
    """

    msg_id: str = ""
    endpoint_id: str = ""
    outcome: TriggerDeliveryResendOutcome | str | None = None
    reason: str = ""

    @classmethod
    def from_proto(
        cls, proto: pb.BatchResendTriggerDeliveryResult
    ) -> BatchResendTriggerDeliveryResult:
        """Build from the generated message."""
        return cls(
            msg_id=proto.msg_id,
            endpoint_id=proto.endpoint_id,
            outcome=enum_from_proto(
                TriggerDeliveryResendOutcome, pb.BatchResendOutcome, proto.outcome
            ),
            reason=proto.reason,
        )


class BatchResendTriggerDeliveriesResponse(_TriggerModel):
    """Per-target outcomes of ``batch_resend_deliveries``.

    Example:
        >>> batch.queued_count
    """

    results: list[BatchResendTriggerDeliveryResult] = Field(default_factory=list)
    queued_count: int = 0

    @classmethod
    def from_proto(
        cls, proto: pb.BatchResendTriggerDeliveriesResponse
    ) -> BatchResendTriggerDeliveriesResponse:
        """Build from the generated message."""
        return cls(
            results=[BatchResendTriggerDeliveryResult.from_proto(r) for r in proto.results],
            queued_count=proto.queued_count,
        )


class RecoverTriggerDeliveriesResponse(_TriggerModel):
    """A started recovery of failed messages.

    Attributes:
        status: ``"running"`` or ``"finished"``.

    Example:
        >>> task = client.actions.triggers.recover_deliveries("ep_123", since=since)
        >>> task.task_id, task.status
    """

    task_id: str = ""
    status: str = ""

    @classmethod
    def from_proto(
        cls, proto: pb.RecoverTriggerDeliveriesResponse
    ) -> RecoverTriggerDeliveriesResponse:
        """Build from the generated message."""
        return cls(task_id=proto.task_id, status=proto.status)

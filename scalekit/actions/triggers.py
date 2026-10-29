"""Manage AgentKit triggers, and verify the trigger events Scalekit delivers to you."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime, timedelta
from typing import Protocol

from pydantic import ValidationError

from scalekit._convert import date_to_str, enum_to_proto, str_list, timedelta_to_seconds
from scalekit.actions.models.trigger_event import TriggerEvent
from scalekit.actions.models.triggers import (
    BatchCreateTriggerSubscriptionsResponse,
    BatchDeleteTriggerSubscriptionsResponse,
    BatchLookupTriggerDeliveriesResponse,
    BatchResendTriggerDeliveriesResponse,
    GenerateTriggerSigningSecretResponse,
    GetTriggerActivityResponse,
    GetTriggerUsageResponse,
    ListAvailableTriggersResponse,
    ListEligibleAccountsResponse,
    ListTriggerDeliveriesByEndpointResponse,
    ListTriggerDeliveryAttemptsByEndpointResponse,
    ListTriggerDeliveryAttemptsByMessageResponse,
    ListTriggerSubscriptionsResponse,
    LookupTriggerDeliveryResponse,
    RecoverTriggerDeliveriesResponse,
    TriggerDeliveryResendTarget,
    TriggerDeliveryResendTargetParam,
    TriggerDeliveryStatus,
    TriggerIngressEndpoint,
    TriggerSubscription,
    TriggerSubscriptionStatus,
    TriggerUsagePeriod,
)
from scalekit.common._webhook_signature import verify_payload_signature
from scalekit.common.exceptions import (
    ScalekitTriggerEventParseException,
    WebhookVerificationError,
)
from scalekit.triggers import TriggersClient
from scalekit.v1.triggers import triggers_pb2 as pb

__all__ = ["ActionTriggers", "HeadersLike", "verify_trigger_event"]

_ID_HEADER = "webhook-id"
_TIMESTAMP_HEADER = "webhook-timestamp"
_SIGNATURE_HEADER = "webhook-signature"


class HeadersLike(Protocol):
    """Any request-headers object: ``get(name)`` plus ``items()``.

    Satisfied by ``dict[str, str]``, any ``Mapping[str, str]``, and the
    ``request.headers`` objects of Flask/Werkzeug, Starlette/FastAPI and Django. Pass
    the object as is; no conversion to ``dict`` is needed.
    """

    def get(self, key: str, /) -> str | None:
        """Return the value of header ``key``, or ``None`` when it is absent."""
        ...

    def items(self) -> Iterable[tuple[str, str]]:
        """Return ``(name, value)`` pairs for every header."""
        ...


# Separator a server or proxy puts between repeated header values it joins into one
# line: "," plus the spaces or tabs after it. Values are not otherwise trimmed, so
# " 1" stays " 1" (and fails the timestamp check).
_VALUE_SEPARATOR = re.compile(r",[ \t]*")


def _header_values(headers: HeadersLike, name: str) -> list[str]:
    """Every value of header ``name`` (lower-case), matched case-insensitively.

    ``items()`` yields repeated headers once per value on Werkzeug and Starlette;
    ``get()`` is the fallback for objects whose ``items()`` does not list the header.
    """
    found: list[object] = [
        value for key, value in headers.items() if isinstance(key, str) and key.lower() == name
    ]
    if not found:
        fallback = headers.get(name)
        if fallback is not None:
            found.append(fallback)
    values: list[str] = []
    for value in found:
        if not isinstance(value, str):
            raise TypeError(f"headers[{name!r}] must be a str, got {type(value).__name__}")
        values.append(value)
    return values


def _single_header(headers: HeadersLike, name: str) -> str | None:
    """A header that must have one value; identical repeats are accepted.

    Repeated headers arrive as separate values or joined with ``", "``, so each value
    is split on ``","`` (and the spaces after it) before the values are compared;
    empty parts are ignored. Returns ``None`` when the header is absent and ``""``
    when it is present but empty.
    """
    values = _header_values(headers, name)
    if not values:
        return None
    distinct: list[str] = []
    for value in values:
        for part in _VALUE_SEPARATOR.split(value):
            if part and part not in distinct:
                distinct.append(part)
    if len(distinct) > 1:
        raise WebhookVerificationError(f"Multiple {name} headers with different values")
    return distinct[0] if distinct else ""


def _joined_header(headers: HeadersLike, name: str) -> str | None:
    """``webhook-signature``: every value holds candidates; join them with ``" "``."""
    values = _header_values(headers, name)
    return " ".join(values) if values else None


def _reject_constant(name: str) -> None:
    # json.loads accepts NaN/Infinity by default; JSON (RFC 8259) does not.
    raise ValueError(f"{name} is not valid JSON")


def _describe(exc: ValidationError) -> str:
    problems = []
    for error in exc.errors(include_url=False, include_input=False, include_context=False):
        field = ".".join(str(part) for part in error["loc"]) or "body"
        if error["type"] == "missing":
            problems.append(f"'{field}' is required")
        else:
            message = error["msg"].removeprefix("Value error, ")
            problems.append(f"'{field}': {message}")
    return "Invalid trigger event: " + "; ".join(problems)


def verify_trigger_event(
    body: str | bytes,
    /,
    *,
    headers: HeadersLike,
    secret: str,
) -> TriggerEvent:
    """Verify a trigger event's signature, then parse it into a ``TriggerEvent``.

    Pass the raw request body exactly as received (before any JSON parsing) and the
    request headers. The signature is checked first: the ``webhook-signature`` header
    must hold a ``v1`` HMAC-SHA256 of ``"{webhook-id}.{webhook-timestamp}.{body}"``
    keyed with your ``whsec_`` secret, and ``webhook-timestamp`` must be within five
    minutes of now. Header names are matched case-insensitively. Every
    ``webhook-signature`` value is a candidate; ``webhook-id`` and
    ``webhook-timestamp`` may repeat only with identical values (also when joined with
    ``","``), and ``webhook-timestamp`` must be Unix seconds as plain digits. Only then
    is the body parsed. This is a local check: no network call and no client
    credentials.

    Delivery is at least once, so the same event can arrive more than once. Use
    ``event.dedupe_key`` plus the connected account your handler acts as as the
    idempotency key. Branch on ``event.delivery_scope``, and when
    ``event.payload_state`` is ``PayloadState.REFERENCE`` fetch the resource yourself
    (``event.payload`` is ``None``).

    Args:
        body: The raw request body, as ``bytes`` (UTF-8) or ``str``.
        headers: The request headers: ``request.headers`` from Flask/Werkzeug,
            Starlette/FastAPI or Django, or a ``dict``/``Mapping``.
        secret: The trigger signing secret (starts with ``whsec_``).

    Returns:
        The parsed, immutable event.

    Raises:
        WebhookVerificationError: Missing signature headers, a ``webhook-id`` or
            ``webhook-timestamp`` repeated with different values, a timestamp that is
            not plain digits, a secret whose key after ``whsec_`` is not non-empty
            padded standard base64 ("Invalid secret"), a
            timestamp outside the five-minute window, no signature candidate that
            matches (malformed candidates are skipped, so a later valid one still
            verifies), or a body that is not valid UTF-8. Respond ``400``.
        ScalekitTriggerEventParseException: The signature is valid but the body is not
            a valid trigger event (including a body that starts with a byte order
            mark). Subclass of ``WebhookVerificationError``.
        TypeError: ``headers`` has no callable ``items()`` and ``get()``, ``body`` is
            not ``str``/``bytes``, ``secret`` is not a ``str``, or a signature header
            value is not a ``str``.

    Example:
        >>> from scalekit import verify_trigger_event
        >>> from scalekit.common.exceptions import WebhookVerificationError
        >>> try:
        ...     event = verify_trigger_event(request.get_data(), headers=request.headers,
        ...                                  secret=os.environ["SCALEKIT_TRIGGER_SECRET"])
        ... except WebhookVerificationError:
        ...     abort(400)
    """
    if not (callable(getattr(headers, "items", None)) and callable(getattr(headers, "get", None))):
        raise TypeError(
            "headers must be a request-headers object or mapping with items() and get(), "
            f"got {type(headers).__name__}"
        )
    if not isinstance(body, (str, bytes)):
        raise TypeError(f"body must be str or bytes, got {type(body).__name__}")
    if not isinstance(secret, str):
        raise TypeError(f"secret must be a str, got {type(secret).__name__}")
    # Argument type errors win over request-content errors: the header readers raise
    # TypeError for non-str values, so they run before the body is decoded.
    webhook_id = _single_header(headers, _ID_HEADER)
    webhook_timestamp = _single_header(headers, _TIMESTAMP_HEADER)
    webhook_signature = _joined_header(headers, _SIGNATURE_HEADER)

    if isinstance(body, bytes):
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise WebhookVerificationError("Trigger event body is not valid UTF-8") from exc
    else:
        text = body
        try:
            text.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise WebhookVerificationError("Trigger event body is not valid UTF-8") from exc

    try:
        verify_payload_signature(
            secret,
            webhook_id,
            webhook_timestamp,
            webhook_signature,
            text,
            skip_malformed_signatures=True,
            strict_timestamp=True,
            strict_secret=True,
        )
    except WebhookVerificationError:
        raise
    except ValueError as exc:
        # UnicodeEncodeError (header text that is not valid UTF-8) is a ValueError
        # subclass. A malformed secret is already "Invalid secret" (strict_secret), and
        # malformed signature candidates are skipped, so they end as "Invalid signature".
        raise WebhookVerificationError("Malformed webhook secret or webhook headers") from exc

    if text.startswith("\ufeff"):
        # JSON text must not start with a byte order mark (RFC 8259 section 8.1).
        # Defensive: json.loads rejects it too, but this keeps the rule independent of
        # the stdlib decoder.
        raise ScalekitTriggerEventParseException("Invalid trigger event: body is not valid JSON")
    try:
        data = json.loads(text, parse_constant=_reject_constant)
    except (ValueError, RecursionError) as exc:  # RecursionError: absurdly deep nesting
        raise ScalekitTriggerEventParseException(
            "Invalid trigger event: body is not valid JSON"
        ) from exc
    if not isinstance(data, dict):
        raise ScalekitTriggerEventParseException(
            "Invalid trigger event: body must be a JSON object"
        )
    try:
        return TriggerEvent.model_validate(data)
    except ValidationError as exc:
        raise ScalekitTriggerEventParseException(_describe(exc)) from exc


def _resend_target(
    target: TriggerDeliveryResendTarget | TriggerDeliveryResendTargetParam,
) -> pb.TriggerDeliveryResendTarget:
    if isinstance(target, TriggerDeliveryResendTarget):
        return pb.TriggerDeliveryResendTarget(msg_id=target.msg_id, endpoint_id=target.endpoint_id)
    if isinstance(target, Mapping):
        missing = [key for key in ("msg_id", "endpoint_id") if key not in target]
        if missing:
            raise TypeError(f"resend target is missing {', '.join(missing)}: {dict(target)!r}")
        return pb.TriggerDeliveryResendTarget(
            msg_id=target["msg_id"], endpoint_id=target["endpoint_id"]
        )
    raise TypeError(
        "each target must be a TriggerDeliveryResendTarget or a dict with msg_id and "
        f"endpoint_id, got {type(target).__name__}"
    )


class ActionTriggers:
    """AgentKit triggers, available as ``client.actions.triggers``.

    ``verify_event`` is local (no network call), so it is safe in both sync and async
    request handlers. Every other method calls Scalekit and blocks the calling thread;
    inside ``async def`` run it with ``await asyncio.to_thread(...)``.

    Server errors raise the ``ScalekitServerException`` subclass for the status, with
    a stable ``error_code``: ``ScalekitBadRequestException`` (400),
    ``ScalekitNotFoundException`` (404, including ``RESOURCE_NOT_FOUND`` when triggers
    are not enabled for the environment), ``ScalekitConflictException`` (409),
    ``ScalekitTooManyRequestsException`` (429, never retried),
    ``ScalekitServiceUnavailableException`` (503) and
    ``ScalekitInternalServerException`` (500). Batch methods report per-item outcomes
    in ``results`` instead of raising. Arguments that cannot be sent (an empty required
    ID, a naive ``datetime``, a fractional-second interval, an unknown enum name) raise
    ``ValueError`` before any request.

    Example:
        >>> triggers = client.actions.triggers
        >>> for trigger in triggers.list_available("conn_123").triggers:
        ...     print(trigger.name, trigger.available)
    """

    def __init__(self, *, triggers_client: TriggersClient | None = None) -> None:
        self._triggers_client = triggers_client

    def _client(self) -> TriggersClient:
        if self._triggers_client is None:
            raise ValueError("Triggers client not initialized.")
        return self._triggers_client

    # Catalogue and subscriptions

    def list_available(self, connection_id: str) -> ListAvailableTriggersResponse:
        """List every trigger a connection offers and whether each is usable there.

        Args:
            connection_id: The connection (``conn_...``).

        Returns:
            All triggers (not paginated), plus ``connection_uses_shared_app``.

        Raises:
            ValueError: ``connection_id`` is empty.
            ScalekitNotFoundException: The connection does not exist in this
                environment (``RESOURCE_NOT_FOUND``).
            ScalekitBadRequestException: ``connection_id`` is malformed.

        Example:
            >>> page = client.actions.triggers.list_available("conn_123")
            >>> [t.name for t in page.triggers if t.available]
        """
        response = self._client().list_available_triggers(connection_id)
        return ListAvailableTriggersResponse.from_proto(response[0])

    def list_eligible_accounts(
        self,
        connection_id: str,
        trigger_name: str,
        *,
        query: str | None = None,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> ListEligibleAccountsResponse:
        """List a connection's connected accounts and whether each can subscribe.

        Args:
            connection_id: The connection (``conn_...``).
            trigger_name: ``AvailableTrigger.name``.
            query: Filter accounts by identifier.
            page_size: Accounts per page; the server default is 10 and values above
                100 are capped.
            page_token: ``next_page_token`` or ``prev_page_token`` of a previous page.

        Returns:
            One page of accounts with their eligibility and health.

        Raises:
            ValueError: ``connection_id`` or ``trigger_name`` is empty.
            ScalekitNotFoundException: Unknown connection or trigger.
            ScalekitBadRequestException: Malformed page token.

        Example:
            >>> page = client.actions.triggers.list_eligible_accounts(
            ...     "conn_123", "item.created", page_size=50)
            >>> ids = [a.id for a in page.accounts if a.eligible]
        """
        response = self._client().list_eligible_accounts(
            connection_id,
            trigger_name,
            query=query,
            page_size=page_size,
            page_token=page_token,
        )
        return ListEligibleAccountsResponse.from_proto(response[0])

    def list_subscriptions(
        self,
        connection_id: str,
        *,
        trigger_name: str | None = None,
        statuses: Sequence[TriggerSubscriptionStatus | str | int] | None = None,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> ListTriggerSubscriptionsResponse:
        """List a connection's trigger subscriptions, one page at a time.

        Args:
            connection_id: The connection (``conn_...``).
            trigger_name: Only subscriptions to this trigger.
            statuses: Only subscriptions in these states: ``TriggerSubscriptionStatus``
                members, their names, or raw numbers.
            page_size: Subscriptions per page; the server caps it at 100.
            page_token: ``next_page_token`` or ``prev_page_token`` of a previous page.

        Returns:
            One page of subscriptions, ``total_size`` and ``status_counts``.

        Raises:
            ValueError: ``connection_id`` is empty or a status name is unknown.
            ScalekitNotFoundException: Unknown connection.
            ScalekitBadRequestException: A status the server does not accept.

        Example:
            >>> page = client.actions.triggers.list_subscriptions(
            ...     "conn_123", statuses=[TriggerSubscriptionStatus.PAUSED_CREDENTIAL])
            >>> [s.connected_account_id for s in page.subscriptions]
        """
        encoded: list[int] | None = None
        if statuses is not None:
            if isinstance(statuses, (str, bytes)):
                raise TypeError("statuses must be a list, not a single string")
            encoded = [enum_to_proto(pb.TriggerSubscriptionStatus, s, "statuses") for s in statuses]
        response = self._client().list_trigger_subscriptions(
            connection_id,
            trigger_name=trigger_name,
            statuses=encoded,
            page_size=page_size,
            page_token=page_token,
        )
        return ListTriggerSubscriptionsResponse.from_proto(response[0])

    def create_subscription(
        self,
        connection_id: str,
        trigger_name: str,
        *,
        connected_account_id: str | None = None,
        interval: timedelta | None = None,
        config: Mapping[str, str] | None = None,
    ) -> TriggerSubscription:
        """Subscribe a connected account, or the whole connection, to a trigger.

        Not retried on ``UNAVAILABLE``: a retry could create the subscription twice.
        Creating the same subscription again raises ``ScalekitConflictException``.

        Args:
            connection_id: The connection (``conn_...``).
            trigger_name: ``AvailableTrigger.name``.
            connected_account_id: The account (``ca_...``). Leave out only for a
                connection-scoped trigger.
            interval: Poll interval for a poll trigger, in whole seconds; at least the
                trigger's ``min_interval``. Leave out for the default and for webhook
                triggers.
            config: Values for the trigger's ``config_fields``.

        Returns:
            The new subscription.

        Raises:
            ValueError: An empty ID, or ``interval`` is not whole seconds.
            ScalekitConflictException: The same subscription already exists
                (``RESOURCE_ALREADY_EXISTS``).
            ScalekitNotFoundException: Unknown connection, trigger or account.
            ScalekitBadRequestException: The account is refused (missing scopes,
                unhealthy, no consent; the message says how to fix it), the account
                is missing for an account-scoped trigger, or ``interval``/``config``
                is invalid.
            ScalekitServiceUnavailableException: The subscription may or may not have
                been created (the call is not retried); check ``list_subscriptions``
                before calling again.

        Example:
            >>> sub = client.actions.triggers.create_subscription(
            ...     "conn_123", "item.created", connected_account_id="ca_123",
            ...     interval=timedelta(minutes=5))
            >>> sub.id, sub.effective_interval
        """
        interval_seconds = None if interval is None else timedelta_to_seconds(interval, "interval")
        response = self._client().create_trigger_subscription(
            connection_id,
            trigger_name,
            connected_account_id=connected_account_id,
            interval_seconds=interval_seconds,
            config=config,
        )
        return TriggerSubscription.from_proto(response[0])

    def batch_create_subscriptions(
        self,
        connection_id: str,
        trigger_name: str,
        *,
        connected_account_ids: Sequence[str] | None = None,
        interval: timedelta | None = None,
        config: Mapping[str, str] | None = None,
    ) -> BatchCreateTriggerSubscriptionsResponse:
        """Subscribe up to 100 connected accounts to a trigger in one call.

        Not atomic: each account gets its own outcome in ``results`` (``CREATED``,
        ``ALREADY_SUBSCRIBED``, ``REFUSED``, ``NOT_FOUND``, ``FAILED``), and those never
        raise. Safe to call again for the ``FAILED`` ones. For a connection-scoped
        trigger, leave ``connected_account_ids`` out.

        Args:
            connection_id: The connection (``conn_...``).
            trigger_name: ``AvailableTrigger.name``.
            connected_account_ids: The accounts (``ca_...``), unique.
            interval: Poll interval, in whole seconds (see ``create_subscription``).
            config: Values for the trigger's ``config_fields``.

        Returns:
            Per-account results and ``created_count``.

        Raises:
            ValueError: An empty ID, or ``interval`` is not whole seconds.
            ScalekitNotFoundException: Unknown connection or trigger.
            ScalekitBadRequestException: A malformed or repeated account ID, no
                accounts for an account-scoped trigger, or invalid ``interval``/``config``.

        Example:
            >>> batch = client.actions.triggers.batch_create_subscriptions(
            ...     "conn_123", "item.created", connected_account_ids=["ca_1", "ca_2"])
            >>> [(r.connected_account_id, r.outcome) for r in batch.results]
        """
        interval_seconds = None if interval is None else timedelta_to_seconds(interval, "interval")
        response = self._client().batch_create_trigger_subscriptions(
            connection_id,
            trigger_name,
            connected_account_ids=connected_account_ids,
            interval_seconds=interval_seconds,
            config=config,
        )
        return BatchCreateTriggerSubscriptionsResponse.from_proto(response[0])

    def delete_subscription(self, connection_id: str, subscription_id: str) -> None:
        """Delete one trigger subscription.

        Retried on ``UNAVAILABLE``, so a ``ScalekitNotFoundException`` can also mean an
        earlier attempt of this same call already deleted it.

        Args:
            connection_id: The connection (``conn_...``).
            subscription_id: The subscription (``trgs_...``).

        Raises:
            ValueError: An empty ID.
            ScalekitNotFoundException: No such subscription on this connection.
            ScalekitBadRequestException: Malformed ``subscription_id``.

        Example:
            >>> client.actions.triggers.delete_subscription("conn_123", "trgs_123")
        """
        self._client().delete_trigger_subscription(connection_id, subscription_id)

    def batch_delete_subscriptions(
        self,
        connection_id: str,
        *,
        subscription_ids: Sequence[str] | None = None,
        trigger_name: str | None = None,
        connected_account_ids: Sequence[str] | None = None,
    ) -> BatchDeleteTriggerSubscriptionsResponse:
        """Delete many trigger subscriptions in one call.

        Choose one selector: ``subscription_ids`` (up to 100), or ``trigger_name`` with
        ``connected_account_ids`` (up to 100). Each subscription gets its own outcome
        in ``results`` (``DELETED``, ``NOT_FOUND``, ``FAILED``, ``NOT_ATTEMPTED``), and
        those never raise. Safe to call again.

        Args:
            connection_id: The connection (``conn_...``).
            subscription_ids: The subscriptions to delete (``trgs_...``).
            trigger_name: With ``connected_account_ids``: the trigger to unsubscribe.
            connected_account_ids: With ``trigger_name``: the accounts (``ca_...``).

        Returns:
            Per-subscription results and ``deleted_count``.

        Raises:
            ValueError: ``connection_id`` is empty.
            ScalekitBadRequestException: Not exactly one selector, or a malformed or
                repeated ID.
            ScalekitTooManyRequestsException: Rate limited (``RATE_LIMITED``).

        Example:
            >>> batch = client.actions.triggers.batch_delete_subscriptions(
            ...     "conn_123", subscription_ids=["trgs_1", "trgs_2"])
            >>> batch.deleted_count
        """
        response = self._client().batch_delete_trigger_subscriptions(
            connection_id,
            subscription_ids=subscription_ids,
            trigger_name=trigger_name,
            connected_account_ids=connected_account_ids,
        )
        return BatchDeleteTriggerSubscriptionsResponse.from_proto(response[0])

    # Activity and usage

    def get_activity(self) -> GetTriggerActivityResponse:
        """Count what happened to this environment's trigger events recently.

        Returns:
            Counts per outcome over ``window``, plus signature and degraded flags.

        Raises:
            ScalekitNotFoundException: Triggers are not enabled for the environment.

        Example:
            >>> activity = client.actions.triggers.get_activity()
            >>> if activity.signature_banner:
            ...     print("check the signing secret")
        """
        response = self._client().get_trigger_activity()
        return GetTriggerActivityResponse.from_proto(response[0])

    def get_usage(
        self,
        *,
        period: TriggerUsagePeriod | str | None = None,
        from_date: date | str | None = None,
        to_date: date | str | None = None,
    ) -> GetTriggerUsageResponse:
        """Read metered trigger deliveries for a preset period or a UTC date range.

        Pass either ``period`` or both ``from_date`` and ``to_date``. The server
        checks the combination and clamps the range to the last 30 days.

        Args:
            period: ``"24h"`` (hourly counts) or ``"7d"``/``"30d"`` (daily counts).
            from_date: First UTC date, inclusive: a ``date``, an aware ``datetime``
                (its UTC date is used) or a ``"YYYY-MM-DD"`` string.
            to_date: Last UTC date, inclusive, in the same forms.

        Returns:
            Daily or hourly counts and the range actually read.

        Raises:
            ValueError: A date that is not a real ``YYYY-MM-DD`` date or a naive
                ``datetime``.
            ScalekitBadRequestException: An invalid combination or range.
            ScalekitNotFoundException: Usage is not metered for this environment
                (``TRIGGER_USAGE_NOT_METERED``).
            ScalekitServiceUnavailableException: Usage cannot be read right now.

        Example:
            >>> usage = client.actions.triggers.get_usage(period="24h")
            >>> [(h.start, h.units) for h in usage.hours]
        """
        response = self._client().get_trigger_usage(
            period=period,
            from_date=None if from_date is None else date_to_str(from_date, "from_date"),
            to_date=None if to_date is None else date_to_str(to_date, "to_date"),
        )
        return GetTriggerUsageResponse.from_proto(response[0])

    # Ingress endpoint and signing secret

    def get_ingress_endpoint(self, connection_id: str) -> TriggerIngressEndpoint:
        """Read the webhook URL a provider sends a connection's events to.

        Args:
            connection_id: The connection (``conn_...``).

        Returns:
            The URL and the state of its signing secret (never the secret itself).

        Raises:
            ValueError: ``connection_id`` is empty.
            ScalekitNotFoundException: No webhook URL yet
                (``TRIGGER_INGRESS_ENDPOINT_NOT_CREATED``; call
                ``create_ingress_endpoint``), or unknown connection
                (``RESOURCE_NOT_FOUND``).

        Example:
            >>> endpoint = client.actions.triggers.get_ingress_endpoint("conn_123")
            >>> endpoint.signing_secret_configured
        """
        response = self._client().get_trigger_ingress_endpoint(connection_id)
        return TriggerIngressEndpoint.from_proto(response[0])

    def create_ingress_endpoint(self, connection_id: str) -> TriggerIngressEndpoint:
        """Create a connection's webhook URL, or return the existing one.

        Args:
            connection_id: The connection (``conn_...``).

        Returns:
            The URL to paste into the provider's app configuration.

        Raises:
            ValueError: ``connection_id`` is empty.
            ScalekitBadRequestException: The connection has no webhook trigger
                (``TRIGGER_INGRESS_NOT_APPLICABLE``), or its trigger definitions are
                unavailable (``TRIGGER_INGRESS_DEFINITIONS_UNAVAILABLE``).
            ScalekitNotFoundException: Unknown connection.

        Example:
            >>> endpoint = client.actions.triggers.create_ingress_endpoint("conn_123")
            >>> print("paste into the provider:", endpoint.url)
        """
        response = self._client().create_trigger_ingress_endpoint(connection_id)
        return TriggerIngressEndpoint.from_proto(response[0])

    def set_signing_secret(
        self, connection_id: str, *, signing_secret: str
    ) -> TriggerIngressEndpoint:
        """Store the signing secret the provider signs its events with.

        The first call stores it. A call with a different secret starts a rotation:
        both secrets are accepted until ``confirm_signing_secret_rotation`` or for 24
        hours. Not retried on ``UNAVAILABLE``, because a retry could advance the
        rotation.

        Args:
            connection_id: The connection (``conn_...``).
            signing_secret: The secret from the provider's app configuration (8-4096
                characters; surrounding whitespace is trimmed by the server).

        Returns:
            The endpoint, with ``masked_signing_secret`` and rotation state.

        Raises:
            ValueError: ``connection_id`` is empty.
            ScalekitBadRequestException: The secret is too short, or this provider uses
                a secret Scalekit generates (``TRIGGER_SIGNING_SECRET_GENERATED_ONLY``;
                call ``generate_signing_secret``).
            ScalekitConflictException: A rotation is already in progress.
            ScalekitNotFoundException: No webhook URL yet
                (``TRIGGER_INGRESS_ENDPOINT_NOT_CREATED``).

        Example:
            >>> endpoint = client.actions.triggers.set_signing_secret(
            ...     "conn_123", signing_secret=os.environ["PROVIDER_SIGNING_SECRET"])
            >>> endpoint.rotation_in_progress
        """
        response = self._client().set_trigger_signing_secret(
            connection_id, signing_secret=signing_secret
        )
        return TriggerIngressEndpoint.from_proto(response[0])

    def confirm_signing_secret_rotation(
        self, connection_id: str, *, signing_secret_rotation_id: int | None = None
    ) -> TriggerIngressEndpoint:
        """Finish a signing-secret rotation so only the new secret is accepted.

        Args:
            connection_id: The connection (``conn_...``).
            signing_secret_rotation_id: ``TriggerIngressEndpoint.signing_secret_rotation_id``
                of the rotation to confirm. Required while a rotation is in progress;
                ignored when none is.

        Returns:
            The endpoint after the confirmation.

        Raises:
            ValueError: ``connection_id`` is empty.
            ScalekitBadRequestException: The rotation ID is missing or names an older
                rotation.
            ScalekitNotFoundException: No webhook URL yet.

        Example:
            >>> endpoint = client.actions.triggers.get_ingress_endpoint("conn_123")
            >>> client.actions.triggers.confirm_signing_secret_rotation(
            ...     "conn_123", signing_secret_rotation_id=endpoint.signing_secret_rotation_id)
        """
        response = self._client().confirm_trigger_signing_secret_rotation(
            connection_id, signing_secret_rotation_id=signing_secret_rotation_id
        )
        return TriggerIngressEndpoint.from_proto(response[0])

    def generate_signing_secret(self, connection_id: str) -> GenerateTriggerSigningSecretResponse:
        """Generate a signing secret, for providers that use one Scalekit creates.

        The secret is returned in plaintext only in this response; it is left out of
        ``repr()``. Not retried on ``UNAVAILABLE``: a retry would replace the secret.

        Args:
            connection_id: The connection (``conn_...``).

        Returns:
            The endpoint, the secret and the URL that includes it.

        Raises:
            ValueError: ``connection_id`` is empty.
            ScalekitBadRequestException: The provider signs its own events
                (``TRIGGER_SIGNING_SECRET_NOT_GENERATABLE``; use ``set_signing_secret``).
            ScalekitConflictException: A rotation is in progress.
            ScalekitNotFoundException: No webhook URL yet.

        Example:
            >>> generated = client.actions.triggers.generate_signing_secret("conn_123")
            >>> save_to_provider(generated.url_with_secret)
        """
        response = self._client().generate_trigger_signing_secret(connection_id)
        return GenerateTriggerSigningSecretResponse.from_proto(response[0])

    # Deliveries

    def list_delivery_attempts_by_endpoint(
        self, endpoint_id: str, *, page_size: int | None = None
    ) -> ListTriggerDeliveryAttemptsByEndpointResponse:
        """List the most recent attempts to deliver trigger events to one of your endpoints.

        Args:
            endpoint_id: Your delivery endpoint.
            page_size: Attempts to return; the server default is 20, capped at 100.

        Returns:
            The attempts (one page; there is no page token).

        Raises:
            ValueError: ``endpoint_id`` is empty.
            ScalekitBadRequestException: Unknown or malformed endpoint (this method
                answers an unknown endpoint with 400, not 404).

        Example:
            >>> page = client.actions.triggers.list_delivery_attempts_by_endpoint("ep_123")
            >>> [(a.msg_id, a.status) for a in page.attempts]
        """
        response = self._client().list_trigger_delivery_attempts_by_endpoint(
            endpoint_id, page_size=page_size
        )
        return ListTriggerDeliveryAttemptsByEndpointResponse.from_proto(response[0])

    def list_deliveries(
        self,
        endpoint_id: str,
        *,
        page_size: int | None = None,
        page_token: str | None = None,
        status: TriggerDeliveryStatus | str | int | None = None,
        channel: str | None = None,
        after: datetime | None = None,
        before: datetime | None = None,
    ) -> ListTriggerDeliveriesByEndpointResponse:
        """List trigger events sent to one of your endpoints, newest first.

        Args:
            endpoint_id: Your delivery endpoint.
            page_size: Messages per page; the server default is 20, capped at 100.
            page_token: ``next_page_token`` of a previous page (with the same filters).
            status: Only messages in this delivery state.
            channel: Only messages for this connection (``conn_...``) or subscription
                (``trgs_...``).
            after: Only messages after this aware instant (at most 90 days back).
            before: Only messages before this aware instant.

        Returns:
            One page of messages and ``next_page_token``.

        Raises:
            ValueError: ``endpoint_id`` is empty, a naive ``datetime``, or an unknown
                status name.
            ScalekitBadRequestException: Unknown endpoint (400, not 404), unknown
                ``channel``, or ``after`` later than ``before``.
            ScalekitTooManyRequestsException: Rate limited.

        Example:
            >>> page = client.actions.triggers.list_deliveries(
            ...     "ep_123", status=TriggerDeliveryStatus.FAILED,
            ...     after=datetime.now(timezone.utc) - timedelta(days=1))
            >>> [d.msg_id for d in page.deliveries]
        """
        encoded = (
            None if status is None else enum_to_proto(pb.TriggerDeliveryStatus, status, "status")
        )
        response = self._client().list_trigger_deliveries_by_endpoint(
            endpoint_id,
            page_size=page_size,
            page_token=page_token,
            status=encoded,
            channel=channel,
            after=after,
            before=before,
        )
        return ListTriggerDeliveriesByEndpointResponse.from_proto(response[0])

    def list_delivery_attempts_by_message(
        self, endpoint_id: str, msg_id: str
    ) -> ListTriggerDeliveryAttemptsByMessageResponse:
        """List every attempt to deliver one message to one of your endpoints.

        Args:
            endpoint_id: Your delivery endpoint.
            msg_id: The message (``msg_...``).

        Returns:
            Up to 50 attempts, oldest first, and ``truncated``.

        Raises:
            ValueError: An empty ID.
            ScalekitBadRequestException: Unknown endpoint or message (400, not 404).

        Example:
            >>> page = client.actions.triggers.list_delivery_attempts_by_message(
            ...     "ep_123", "msg_123")
            >>> [a.response_status_code for a in page.attempts]
        """
        response = self._client().list_trigger_delivery_attempts_by_message(endpoint_id, msg_id)
        return ListTriggerDeliveryAttemptsByMessageResponse.from_proto(response[0])

    def lookup_delivery(self, delivery_id: str) -> LookupTriggerDeliveryResponse:
        """Look up one delivered message by its message ID or by its event ID.

        Args:
            delivery_id: A message ID (``msg_...``) or the event ID your endpoint
                received (``TriggerEvent.dedupe_key``).

        Returns:
            The message, its trigger and up to 50 attempts.

        Raises:
            ValueError: ``delivery_id`` is empty.
            ScalekitNotFoundException: Not found (``error_code`` is ``NOT_FOUND``).
            ScalekitBadRequestException: Malformed ID (an attempt ID is refused).
            ScalekitTooManyRequestsException: Rate limited.

        Example:
            >>> found = client.actions.triggers.lookup_delivery(event.dedupe_key)
            >>> [a.status for a in found.attempts]
        """
        response = self._client().lookup_trigger_delivery(delivery_id)
        return LookupTriggerDeliveryResponse.from_proto(response[0])

    def batch_lookup_deliveries(
        self, delivery_ids: Sequence[str]
    ) -> BatchLookupTriggerDeliveriesResponse:
        """Look up 1 to 25 delivered messages by message ID or event ID.

        Each ID gets its own outcome in ``results`` (``FOUND``, ``NOT_FOUND``,
        ``RATE_LIMITED``, ``FAILED``, ``NOT_ATTEMPTED``), and those never raise.
        Attempts in the results carry no response bodies.

        Args:
            delivery_ids: Message IDs (``msg_...``) or event IDs, unique.

        Returns:
            Per-ID results and ``found_count``.

        Raises:
            ScalekitBadRequestException: An empty, repeated or malformed list.
            ScalekitTooManyRequestsException: Rate limited.

        Example:
            >>> batch = client.actions.triggers.batch_lookup_deliveries(["msg_1", "msg_2"])
            >>> batch.found_count
        """
        response = self._client().batch_lookup_trigger_deliveries(
            str_list("delivery_ids", delivery_ids)
        )
        return BatchLookupTriggerDeliveriesResponse.from_proto(response[0])

    def batch_resend_deliveries(
        self, targets: Sequence[TriggerDeliveryResendTarget | TriggerDeliveryResendTargetParam]
    ) -> BatchResendTriggerDeliveriesResponse:
        """Send 1 to 50 messages to endpoints again.

        Each target makes a real delivery attempt and gets its own outcome in
        ``results`` (``QUEUED``, ``NOT_FOUND``, ``RATE_LIMITED``, ``FAILED``,
        ``NOT_ATTEMPTED``), which never raise. Not retried on ``UNAVAILABLE``: a retry
        could deliver the messages twice.

        Args:
            targets: ``TriggerDeliveryResendTarget`` models or
                ``{"msg_id": "msg_...", "endpoint_id": "ep_..."}`` dicts.

        Returns:
            Per-target results and ``queued_count``.

        Raises:
            TypeError: A target is neither a model nor a dict.
            ScalekitBadRequestException: An empty, repeated or malformed target list.
            ScalekitTooManyRequestsException: Rate limited.

        Example:
            >>> batch = client.actions.triggers.batch_resend_deliveries(
            ...     [{"msg_id": "msg_123", "endpoint_id": "ep_123"}])
            >>> batch.queued_count
        """
        response = self._client().batch_resend_trigger_deliveries(
            [_resend_target(t) for t in targets]
        )
        return BatchResendTriggerDeliveriesResponse.from_proto(response[0])

    def recover_deliveries(
        self, endpoint_id: str, *, since: datetime, until: datetime | None = None
    ) -> RecoverTriggerDeliveriesResponse:
        """Resend every message that failed to reach an endpoint in a time range.

        Not retried on ``UNAVAILABLE``. A ``ScalekitInternalServerException`` here
        means the recovery may be running anyway: check the endpoint's deliveries
        before calling again.

        Args:
            endpoint_id: Your delivery endpoint (``ep_...``).
            since: Start of the range, an aware instant not in the future.
            until: End of the range (default now), at most 14 days after ``since``.

        Returns:
            The recovery task and its status (``"running"`` or ``"finished"``).

        Raises:
            ValueError: ``endpoint_id`` or ``since`` is missing, or a naive ``datetime``.
            ScalekitBadRequestException: An invalid range.
            ScalekitNotFoundException: Unknown endpoint (``RESOURCE_NOT_FOUND``).
            ScalekitTooManyRequestsException: Rate limited.
            ScalekitInternalServerException: The start was not confirmed; it may be
                running.

        Example:
            >>> task = client.actions.triggers.recover_deliveries(
            ...     "ep_123", since=datetime.now(timezone.utc) - timedelta(hours=6))
            >>> task.status
        """
        response = self._client().recover_trigger_deliveries(endpoint_id, since=since, until=until)
        return RecoverTriggerDeliveriesResponse.from_proto(response[0])

    # Local verification

    def verify_event(
        self,
        body: str | bytes,
        /,
        *,
        headers: HeadersLike,
        secret: str,
    ) -> TriggerEvent:
        """Verify a trigger event's signature, then parse it into a ``TriggerEvent``.

        Same as ``scalekit.verify_trigger_event``; see it for the full contract.

        Args:
            body: The raw request body, as ``bytes`` (UTF-8) or ``str``.
            headers: The request headers, for example ``request.headers``.
            secret: The trigger signing secret (starts with ``whsec_``).

        Returns:
            The parsed, immutable event.

        Raises:
            WebhookVerificationError: The signature, timestamp or encoding check failed.
            ScalekitTriggerEventParseException: The signature is valid but the body is
                not a valid trigger event (subclass of ``WebhookVerificationError``).
            TypeError: An argument has the wrong type.

        Example:
            >>> event = client.actions.triggers.verify_event(
            ...     request.get_data(), headers=request.headers, secret=secret)
            >>> event.dedupe_key
            'dk_123'
        """
        return verify_trigger_event(body, headers=headers, secret=secret)

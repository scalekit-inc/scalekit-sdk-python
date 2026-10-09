"""Typed model for trigger events that Scalekit delivers to your endpoint."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Annotated, TypeVar

from pydantic import BaseModel, ConfigDict, JsonValue, SkipValidation, StrictStr, field_validator
from pydantic_core import PydanticCustomError

__all__ = ["DeliveryScope", "DetectionMode", "PayloadState", "TriggerEvent"]


class DeliveryScope(str, Enum):
    """Who a trigger event was delivered for.

    Values the SDK does not know yet arrive as plain ``str``; compare with ``==``.
    """

    ACCOUNT = "account"
    """Delivered for one connected account; ``connected_account_id`` is set."""
    CONNECTION = "connection"
    """Delivered for the whole connection; ``connected_account_id`` is ``""``."""


class DetectionMode(str, Enum):
    """How Scalekit detected the change. Unknown values arrive as plain ``str``."""

    WEBHOOK = "webhook"
    POLL = "poll"


class PayloadState(str, Enum):
    """Whether ``payload`` carries the resource. Unknown values arrive as plain ``str``."""

    FULL = "full"
    """``payload`` holds the resource data."""
    REFERENCE = "reference"
    """``payload`` is ``None``; fetch the resource by ``resource_type`` and ``resource_id``."""


_E = TypeVar("_E", bound=Enum)

# RFC 3339 date-time (section 5.6): a "T" separator and a mandatory offset ("Z" or +hh:mm).
_RFC3339 = re.compile(
    r"(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})[Tt]"
    r"(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})(?:\.(?P<fraction>[0-9]+))?"
    r"(?:(?P<utc>[Zz])|(?P<sign>[+-])(?P<off_hour>[0-9]{2}):(?P<off_minute>[0-5][0-9]))",
)
_MIN_YEAR, _MAX_YEAR = 1, 9999


def _enum_or_raw(enum_cls: type[_E], value: object, field: str) -> _E | str:
    if not isinstance(value, str):
        raise PydanticCustomError("string_type", f"{field} must be a string")
    try:
        return enum_cls(value)
    except ValueError:
        return value


def _parse_rfc3339(value: str) -> datetime:
    match = _RFC3339.fullmatch(value)
    if match is None or not _MIN_YEAR <= int(match["year"]) <= _MAX_YEAR:
        raise ValueError("occurred_at must be an RFC 3339 timestamp with a UTC offset")
    # Python datetimes hold microseconds: digits past the sixth are truncated.
    fraction = (match["fraction"] or "")[:6].ljust(6, "0")
    if match["utc"]:
        tz = timezone.utc
    else:
        offset = timedelta(hours=int(match["off_hour"]), minutes=int(match["off_minute"]))
        tz = timezone(-offset if match["sign"] == "-" else offset)
    parsed = datetime(
        int(match["year"]),
        int(match["month"]),
        int(match["day"]),
        int(match["hour"]),
        int(match["minute"]),
        int(match["second"]),
        int(fraction),
        tzinfo=tz,
    )
    # Raises OverflowError when the UTC instant falls outside years 0001-9999,
    # for example "0001-01-01T00:00:00+01:00"; the caller reports it as a parse error.
    return parsed.astimezone(timezone.utc)


class TriggerEvent(BaseModel):
    """A verified trigger event: a change in a third-party app that Scalekit forwards to you.

    Get one from ``scalekit.verify_trigger_event`` (or
    ``client.actions.triggers.verify_event``), which checks the signature before it
    parses the body. The model is immutable. Fields this SDK version does not know
    are kept and readable through ``event.model_extra``.

    Handling rules:

    * **Delivery is at least once.** The same event can arrive more than once. Use
      ``dedupe_key`` together with the connected account your handler acts as as the
      idempotency key, and skip events you have already processed.
    * **Branch on** ``delivery_scope``. ``DeliveryScope.ACCOUNT`` events belong to one
      connected account (``connected_account_id``); ``DeliveryScope.CONNECTION``
      events belong to the whole connection and have ``connected_account_id == ""``.
    * **Reference payloads.** When ``payload_state`` is ``PayloadState.REFERENCE``,
      ``payload`` is ``None``: fetch the resource identified by ``resource_type`` and
      ``resource_id`` yourself.
    * Enum fields hold the enum member for known values and the raw ``str`` for values
      added after this SDK version, so compare with ``==`` and keep a default branch.

    Attributes:
        version: Event format version, for example ``"1"``.
        trigger_type: The trigger that fired, for example ``"example.item.created"``.
        subscription_id: The trigger subscription that produced the event.
        delivery_scope: ``DeliveryScope`` member, or the raw string for an unknown value.
        connection_id: The connection the event came from.
        connected_account_id: The connected account, or ``""`` for connection scope.
        resource_type: Type of the changed resource in the third-party app.
        resource_id: ID of the changed resource; ``None`` when the event has none.
        occurred_at: When the change happened (timezone-aware UTC), or ``None``.
            Fractional seconds are truncated to microseconds.
        detection_mode: ``DetectionMode`` member, or the raw string for an unknown value.
        payload_state: ``PayloadState`` member, or the raw string for an unknown value.
        payload: The resource data as parsed JSON (``dict``, ``list``, ``str``, number,
            ``bool``); ``None`` for reference payloads. Any nesting depth the JSON decoder
            accepts is kept as is. On Python 3.10 and 3.11 the stdlib decoder fails at
            about 1000 levels, so such a body raises ``ScalekitTriggerEventParseException``.
        dedupe_key: Stable key for this change; identical across redeliveries.
        correlation_id: Links work that follows from this event back to it; carry it
            through to anything your handler triggers.

    Example:
        >>> event = scalekit.verify_trigger_event(body, headers=headers, secret=secret)
        >>> if event.delivery_scope == DeliveryScope.ACCOUNT:
        ...     handle_for_account(event.connected_account_id, event)
    """

    model_config = ConfigDict(frozen=True, extra="allow", hide_input_in_errors=True)

    version: StrictStr
    trigger_type: StrictStr
    subscription_id: StrictStr
    delivery_scope: DeliveryScope | str
    connection_id: StrictStr
    connected_account_id: StrictStr
    resource_type: StrictStr
    resource_id: StrictStr | None = None
    occurred_at: datetime | None = None
    detection_mode: DetectionMode | str
    payload_state: PayloadState | str
    # The JSON value exactly as json.loads produced it. SkipValidation: no re-validation,
    # so payloads nested deeper than pydantic's JsonValue recursion limit still parse.
    payload: Annotated[JsonValue, SkipValidation] = None
    dedupe_key: StrictStr
    correlation_id: StrictStr

    @field_validator("delivery_scope", mode="before")
    @classmethod
    def _delivery_scope(cls, value: object) -> DeliveryScope | str:
        return _enum_or_raw(DeliveryScope, value, "delivery_scope")

    @field_validator("detection_mode", mode="before")
    @classmethod
    def _detection_mode(cls, value: object) -> DetectionMode | str:
        return _enum_or_raw(DetectionMode, value, "detection_mode")

    @field_validator("payload_state", mode="before")
    @classmethod
    def _payload_state(cls, value: object) -> PayloadState | str:
        return _enum_or_raw(PayloadState, value, "payload_state")

    @field_validator("occurred_at", mode="before")
    @classmethod
    def _occurred_at(cls, value: object) -> datetime | None:
        if value is None or value == "":
            return None
        if isinstance(value, datetime):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError("occurred_at must be timezone-aware")
            return value.astimezone(timezone.utc)
        if not isinstance(value, str):
            raise PydanticCustomError("string_type", "occurred_at must be an RFC 3339 string")
        try:
            return _parse_rfc3339(value)
        except (ValueError, OverflowError) as exc:
            # datetime() rejects out-of-range parts (month 13, offset >= 24h, ...).
            raise ValueError("occurred_at must be an RFC 3339 timestamp with a UTC offset") from exc

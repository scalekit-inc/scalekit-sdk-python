"""Private converters between protobuf values and SDK types.

One place for the rules every SDK-owned model follows: timestamps are read only when
the field is present and come out as timezone-aware UTC ``datetime``; inputs must be
timezone-aware; enum values the SDK does not know never raise; durations are
``timedelta``. Nothing here imports the rest of the SDK, so any module can use it.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import TypeVar

from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
from google.protobuf.message import Message
from google.protobuf.timestamp_pb2 import Timestamp

__all__ = [
    "date_to_str",
    "datetime_to_timestamp",
    "enum_from_proto",
    "enum_to_proto",
    "require",
    "seconds_from_proto",
    "str_list",
    "timedelta_to_seconds",
    "timestamp_from_proto",
]

_E = TypeVar("_E", bound=Enum)
_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")
_ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_ONE_SECOND = timedelta(seconds=1)


def require(name: str, value: object) -> None:
    """Raise ``ValueError`` when a required identifier is missing or empty."""
    if value is None or value == "":
        raise ValueError(f"{name} is required")


def str_list(name: str, values: Sequence[str]) -> list[str]:
    """Copy ``values`` into a list, refusing a bare ``str`` (which would split into characters)."""
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{name} must be a list of strings, not a single string")
    return list(values)


def _enum_prefix(wrapper: EnumTypeWrapper) -> str:
    """``TriggerDeliveryStatus`` -> ``"TRIGGER_DELIVERY_STATUS_"``."""
    return _CAMEL_BOUNDARY.sub("_", wrapper.DESCRIPTOR.name).upper() + "_"


def enum_from_proto(enum_cls: type[_E], wrapper: EnumTypeWrapper, value: int) -> _E | str | None:
    """Convert a proto enum number to an SDK enum member.

    ``0`` (the ``*_UNSPECIFIED`` value) becomes ``None``. A value the generated code
    knows is looked up by its name without the ``<ENUM_NAME>_`` prefix; when the SDK
    enum has no such member, that name is returned as a plain ``str``. A number the
    generated code does not know is returned as ``str(value)``. Never raises.
    """
    if value == 0:
        return None
    try:
        name: str = wrapper.Name(value)
    except ValueError:
        return str(value)
    name = name.removeprefix(_enum_prefix(wrapper))
    try:
        return enum_cls[name]
    except KeyError:
        return name


def enum_to_proto(wrapper: EnumTypeWrapper, value: Enum | str | int, field: str) -> int:
    """Encode an enum member, a value name or a raw number as a proto enum number.

    Names are accepted with or without the ``<ENUM_NAME>_`` prefix. A raw ``int`` is
    sent as is, so values newer than this SDK can still be sent. Raises ``ValueError``
    for a name the generated code does not know (it cannot be encoded).
    """
    if isinstance(value, bool):
        raise TypeError(f"{field} must be an enum member, a name or an int, not bool")
    if isinstance(value, Enum):
        name = value.name
    elif isinstance(value, str):
        name = value
    elif isinstance(value, int):
        return value
    else:
        raise TypeError(f"{field} must be an enum member, a name or an int")
    prefix = _enum_prefix(wrapper)
    for candidate in (name, prefix + name):
        try:
            number: int = wrapper.Value(candidate)
        except ValueError:
            continue
        return number
    known = ", ".join(
        v.name.removeprefix(prefix) for v in wrapper.DESCRIPTOR.values if v.number != 0
    )
    raise ValueError(f"unknown {field} {value!r}; expected one of: {known}, or an int")


def timestamp_from_proto(message: Message, field: str) -> datetime | None:
    """Read a ``Timestamp`` field as aware UTC ``datetime``; ``None`` when it is unset."""
    if not message.HasField(field):
        return None
    result: datetime = getattr(message, field).ToDatetime(tzinfo=timezone.utc)
    return result


def datetime_to_timestamp(value: datetime, field: str) -> Timestamp:
    """Encode an aware ``datetime`` as a ``Timestamp``; naive values raise ``ValueError``."""
    if not isinstance(value, datetime):
        raise TypeError(f"{field} must be a datetime, got {type(value).__name__}")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware, for example datetime.now(timezone.utc)")
    timestamp = Timestamp()
    timestamp.FromDatetime(value.astimezone(timezone.utc))
    return timestamp


def seconds_from_proto(seconds: int) -> timedelta | None:
    """A whole-seconds proto integer as ``timedelta``; ``0`` (not set) becomes ``None``."""
    return timedelta(seconds=seconds) if seconds else None


def timedelta_to_seconds(value: timedelta, field: str) -> int:
    """Encode a ``timedelta`` as whole seconds; a fractional second raises ``ValueError``."""
    if not isinstance(value, timedelta):
        raise TypeError(f"{field} must be a timedelta, got {type(value).__name__}")
    if value % _ONE_SECOND:
        raise ValueError(f"{field} must be a whole number of seconds, got {value!r}")
    return value // _ONE_SECOND


def date_to_str(value: date | str, field: str) -> str:
    """Encode a calendar date as ``YYYY-MM-DD``.

    A ``date`` is used as is; an aware ``datetime`` is converted to its UTC date (a
    naive one raises ``ValueError``); a ``str`` must already be a real ``YYYY-MM-DD``
    date.
    """
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(f"{field} must be a date or a timezone-aware datetime")
        return value.astimezone(timezone.utc).date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        if _ISO_DATE.fullmatch(value):
            try:
                date.fromisoformat(value)
            except ValueError:
                pass
            else:
                return value
        raise ValueError(f"{field} must be a YYYY-MM-DD date, got {value!r}")
    raise TypeError(f"{field} must be a date or a YYYY-MM-DD string, got {type(value).__name__}")

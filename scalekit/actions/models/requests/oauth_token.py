"""Build an ``OauthToken`` proto from the ``authorization_details["oauth_token"]`` dict."""

import math
import re
from datetime import datetime, timezone
from typing import Any, Dict, Union

from google.protobuf.timestamp_pb2 import Timestamp

from scalekit.v1.connected_accounts.connected_accounts_pb2 import OauthToken

ExpiresAt = Union[datetime, str, int, float]

# Range a google.protobuf.Timestamp can hold: 0001-01-01T00:00:00Z to 9999-12-31T23:59:59Z.
_MIN_SECONDS = -62135596800
_MAX_SECONDS = 253402300799

# RFC 3339 date-time with a mandatory timezone. protobuf's FromJsonString checks the date and
# time but applies an offset without bounds-checking it (it would turn "+00:60" into -1 hour),
# so the offset is validated here first.
_RFC3339 = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?(?:Z|[+-](?P<oh>\d{2}):(?P<om>\d{2}))$"
)


def expires_at_to_timestamp(value: ExpiresAt) -> Timestamp:
    """Convert ``oauth_token["expires_at"]`` to a protobuf ``Timestamp``.

    Accepts a timezone-aware ``datetime``, an RFC 3339 string (``Z`` or a UTC offset), or
    epoch seconds as an int or float.

    :raises ValueError: for a naive ``datetime`` (its timezone is unknown), a string that is
        not RFC 3339 with a timezone, or any other type.
    """
    if isinstance(value, bool):  # bool is an int subclass; True is not a timestamp
        raise ValueError("oauth_token.expires_at must be a datetime, an RFC 3339 string or epoch seconds, not bool")
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        # protobuf's RFC 3339 parser: requires "Z" or an offset, keeps up to 9 fractional
        # digits, and behaves the same on every Python version (fromisoformat does not).
        text = value.strip().upper()
        match = _RFC3339.match(text)
        ts = Timestamp()
        try:
            if not match or int(match.group("oh") or 0) > 23 or int(match.group("om") or 0) > 59:
                raise ValueError("not RFC 3339")
            ts.FromJsonString(text)
        except ValueError as exc:
            raise ValueError(
                f"oauth_token.expires_at must be an RFC 3339 timestamp with a timezone "
                f"(e.g. 2026-12-01T10:00:00Z): {value!r}"
            ) from exc
        return ts
    elif isinstance(value, (int, float)):
        if not math.isfinite(value):
            raise ValueError(f"oauth_token.expires_at is not a finite number: {value!r}")
        seconds = math.floor(value)
        nanos = int(round((value - seconds) * 1e9))
        if nanos >= 1_000_000_000:
            seconds, nanos = seconds + 1, 0
        if not _MIN_SECONDS <= seconds <= _MAX_SECONDS:
            raise ValueError(
                f"oauth_token.expires_at epoch seconds must be between {_MIN_SECONDS} and {_MAX_SECONDS}: {value!r}"
            )
        return Timestamp(seconds=int(seconds), nanos=nanos)
    else:
        raise ValueError(
            "oauth_token.expires_at must be a datetime, an RFC 3339 string or epoch seconds, "
            f"got {type(value).__name__}"
        )

    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("oauth_token.expires_at datetime must be timezone-aware; naive datetimes are ambiguous")
    ts = Timestamp()
    ts.FromDatetime(dt.astimezone(timezone.utc))
    return ts


def build_oauth_token(oauth_data: Dict[str, Any]) -> OauthToken:
    """Build the ``OauthToken`` proto sent on create/update connected account.

    ``expires_at`` is optional; it is left unset when absent or ``None``.
    """
    oauth_token = OauthToken(
        access_token=oauth_data.get("access_token", ""),
        refresh_token=oauth_data.get("refresh_token", ""),
        scopes=oauth_data.get("scopes", []),
    )
    expires_at = oauth_data.get("expires_at")
    if expires_at is not None:
        oauth_token.expires_at.CopyFrom(expires_at_to_timestamp(expires_at))
    return oauth_token

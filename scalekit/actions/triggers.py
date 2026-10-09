"""Verify and parse trigger events that Scalekit delivers to your endpoint."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from typing import Protocol

from pydantic import ValidationError

from scalekit.actions.models.trigger_event import TriggerEvent
from scalekit.common._webhook_signature import verify_payload_signature
from scalekit.common.exceptions import (
    ScalekitTriggerEventParseException,
    WebhookVerificationError,
)

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


class ActionTriggers:
    """Trigger event helpers, available as ``client.actions.triggers``.

    Every method is local (no network call), so it is safe to call from both sync
    and async request handlers.
    """

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

        Example:
            >>> event = client.actions.triggers.verify_event(
            ...     request.get_data(), headers=request.headers, secret=secret)
            >>> event.dedupe_key
            'dk_123'
        """
        return verify_trigger_event(body, headers=headers, secret=secret)

"""Verify and parse trigger events that Scalekit delivers to your endpoint."""

from __future__ import annotations

import json
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

    Satisfied by ``dict[str, str]`` and by the header objects of common frameworks:
    Flask/Werkzeug ``request.headers``, Django ``request.headers``, Starlette/FastAPI
    ``request.headers`` and aiohttp ``request.headers``. Pass the object as is; no
    conversion to ``dict`` is needed.
    """

    def get(self, key: str, /) -> str | None:
        """Return the value of header ``key``, or ``None`` when it is absent."""
        ...

    def items(self) -> Iterable[tuple[str, str]]:
        """Return ``(name, value)`` pairs for every header."""
        ...


def _header(headers: HeadersLike, name: str) -> str | None:
    """Look a header up by exact name, then case-insensitively."""
    value = headers.get(name)
    if value is None:
        for key, candidate in headers.items():
            if isinstance(key, str) and key.lower() == name:
                value = candidate
                break
    if value is not None and not isinstance(value, str):
        raise TypeError(f"headers[{name!r}] must be a str, got {type(value).__name__}")
    return value


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
    minutes of now. Header names are matched case-insensitively. Only then is the body
    parsed. This is a local check: no network call and no client credentials.

    Delivery is at least once, so the same event can arrive more than once. Use
    ``event.dedupe_key`` plus the connected account your handler acts as as the
    idempotency key. Branch on ``event.delivery_scope``, and when
    ``event.payload_state`` is ``PayloadState.REFERENCE`` fetch the resource yourself
    (``event.payload`` is ``None``).

    Args:
        body: The raw request body, as ``bytes`` (UTF-8) or ``str``.
        headers: The request headers, for example ``request.headers`` from Flask,
            Django, Starlette/FastAPI or aiohttp, or a ``dict``.
        secret: The trigger signing secret (starts with ``whsec_``).

    Returns:
        The parsed, immutable event.

    Raises:
        WebhookVerificationError: Missing signature headers, a malformed secret or
            signature, a timestamp outside the five-minute window, a signature that
            does not match, or a body that is not valid UTF-8. Respond ``400``.
        ScalekitTriggerEventParseException: The signature is valid but the body is not
            a valid trigger event. Subclass of ``WebhookVerificationError``.
        TypeError: ``body`` is not ``str``/``bytes``, ``secret`` is not a ``str``, or a
            signature header value is not a ``str``.

    Example:
        >>> from scalekit import verify_trigger_event
        >>> from scalekit.common.exceptions import WebhookVerificationError
        >>> try:
        ...     event = verify_trigger_event(request.get_data(), headers=request.headers,
        ...                                  secret=os.environ["SCALEKIT_TRIGGER_SECRET"])
        ... except WebhookVerificationError:
        ...     abort(400)
    """
    if isinstance(body, bytes):
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise WebhookVerificationError("Trigger event body is not valid UTF-8") from exc
    elif isinstance(body, str):
        text = body
        try:
            text.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise WebhookVerificationError("Trigger event body is not valid UTF-8") from exc
    else:
        raise TypeError(f"body must be str or bytes, got {type(body).__name__}")
    if not isinstance(secret, str):
        raise TypeError(f"secret must be a str, got {type(secret).__name__}")

    try:
        verify_payload_signature(
            secret,
            _header(headers, _ID_HEADER),
            _header(headers, _TIMESTAMP_HEADER),
            _header(headers, _SIGNATURE_HEADER),
            text,
        )
    except WebhookVerificationError:
        raise
    except ValueError as exc:
        # binascii.Error (malformed base64 in the secret or signature header) and
        # UnicodeEncodeError (non-UTF-8 header text) are ValueError subclasses.
        raise WebhookVerificationError(
            "Malformed webhook secret or webhook-signature header"
        ) from exc

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

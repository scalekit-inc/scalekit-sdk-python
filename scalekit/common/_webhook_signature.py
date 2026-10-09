"""Shared signature check for Scalekit webhook-style deliveries (private).

Used by ``ScalekitClient.verify_webhook_payload``,
``ScalekitClient.verify_interceptor_payload`` and
``scalekit.verify_trigger_event``. The behaviour of this module is relied on by
the first two, so changes here must keep their messages, raised types and
header handling exactly as they are.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from math import floor

from scalekit.common.exceptions import WebhookVerificationError

WEBHOOK_TOLERANCE = timedelta(minutes=5)
WEBHOOK_SIGNATURE_VERSION = "v1"


def compute_signature(secret: bytes, data: str) -> str:
    """Return the ``v1`` HMAC-SHA256 signature of ``data`` as ``"v1, <base64>"``."""
    signature = hmac.new(secret, data.encode(), hashlib.sha256).digest()
    return f"v1, {base64.b64encode(signature).decode('utf-8')}"


def verify_timestamp(timestamp_str: str, *, tolerance: timedelta = WEBHOOK_TOLERANCE) -> datetime:
    """Parse a Unix-seconds timestamp header and check it is within ``tolerance`` of now.

    Raises:
        WebhookVerificationError: The value is not a number, or is too old or too new.
    """
    now = datetime.now(tz=timezone.utc)
    try:
        timestamp = datetime.fromtimestamp(float(timestamp_str), tz=timezone.utc)
    except (ValueError, TypeError, OverflowError, OSError) as exc:
        # Everything float() and fromtimestamp() raise for a bad value.
        raise WebhookVerificationError("Invalid Signature Headers") from exc

    if timestamp < (now - tolerance):
        raise WebhookVerificationError("Message timestamp too old")

    if timestamp > (now + tolerance):
        raise WebhookVerificationError("Message timestamp too new")

    return timestamp


def verify_payload_signature(
    secret: str,
    webhook_id: str | None,
    webhook_timestamp: str | None,
    webhook_signature: str | None,
    payload: str,
    *,
    tolerance: timedelta = WEBHOOK_TOLERANCE,
    signature_version: str = WEBHOOK_SIGNATURE_VERSION,
    skip_malformed_signatures: bool = False,
) -> bool:
    """Verify a ``whsec_`` HMAC signature over ``"{id}.{timestamp}.{payload}"``.

    Returns ``True`` or raises. A malformed base64 secret raises ``binascii.Error``.
    With ``skip_malformed_signatures=False`` (the historical behaviour of the public
    verifiers, which must not change) a malformed base64 signature candidate raises
    ``binascii.Error`` too. With ``True``, a candidate that has no comma, another
    version, invalid base64 or the wrong decoded length is skipped, so a later valid
    candidate still verifies.

    Raises:
        WebhookVerificationError: Missing headers, a secret without ``_``, a stale or
            future timestamp, or no matching signature.
    """
    if not webhook_id or not webhook_timestamp or not webhook_signature:
        raise WebhookVerificationError("Missing required headers")

    secret_parts = secret.split("_")
    if len(secret_parts) < 2:
        raise WebhookVerificationError("Invalid secret")

    secret_bytes = base64.b64decode(secret_parts[1])

    timestamp = verify_timestamp(webhook_timestamp, tolerance=tolerance)

    timestamp_str = str(floor(timestamp.replace(tzinfo=timezone.utc).timestamp()))
    data = f"{webhook_id}.{timestamp_str}.{payload}"
    computed_signature = base64.b64decode(compute_signature(secret_bytes, data).split(",")[1])

    for versioned_signature in webhook_signature.split(" "):
        signature_parts = versioned_signature.split(",")
        if len(signature_parts) < 2:
            continue

        version = signature_parts[0]
        if skip_malformed_signatures:
            if version != signature_version:
                continue
            try:
                signature = base64.b64decode(signature_parts[1], validate=True)
            except binascii.Error:
                continue
            if len(signature) != len(computed_signature):
                continue
        else:
            signature = base64.b64decode(signature_parts[1])
            if version != signature_version:
                continue

        if hmac.compare_digest(signature, computed_signature):
            return True

    raise WebhookVerificationError("Invalid signature")

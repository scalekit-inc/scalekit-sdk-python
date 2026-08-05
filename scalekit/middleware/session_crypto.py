from __future__ import annotations

import base64
import json
import os
from typing import Any, Dict

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Bumped whenever the wire format changes. Older versions must fail gracefully
# (InvalidSessionError, forcing re-login) rather than crash -- see decrypt_session.
_SESSION_FORMAT_VERSION = 1
_NONCE_SIZE = 12  # bytes, standard for AES-GCM

# Fixed, non-secret HKDF salt/info: cookie_encryption_secret itself is expected to be a
# high-entropy, developer-generated secret (not a low-entropy password), so a fast KDF
# derivation is appropriate here -- this is not password storage.
_HKDF_SALT = b"scalekit-session-v1"
_HKDF_INFO = b"scalekit-encrypted-session"

_SECRET_HELP = (
    "cookie_encryption_secret is required. Generate a strong random secret, e.g.:\n"
    '  python3 -c "import secrets; print(secrets.token_urlsafe(32))"\n'
    "and keep it identical across every server instance -- there is intentionally no "
    "default, since a shared default secret would let any deployment decrypt or forge "
    "any other deployment's sessions."
)


class InvalidSessionError(Exception):
    """
    Raised when an encrypted session cannot be decrypted -- missing, malformed,
    tampered with, or produced by an unsupported format version. Always raised
    instead of returning a partially-decrypted or unauthenticated payload.
    """


def _derive_key(secret: str) -> bytes:
    if not secret:
        raise ValueError(_SECRET_HELP)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=_HKDF_SALT, info=_HKDF_INFO)
    return hkdf.derive(secret.encode("utf-8"))


def encrypt_session(payload: Dict[str, Any], secret: str) -> str:
    """
    Encrypt a session payload (access_token, refresh_token, user claims,
    expires_at, ...) into a single opaque, tamper-proof string suitable for
    storing in a cookie.

    :param payload: JSON-serializable session data.
    :param secret: cookie_encryption_secret -- required, no default (see module docstring).
    :returns: base64url-encoded, versioned ciphertext string.
    """
    key = _derive_key(secret)
    nonce = os.urandom(_NONCE_SIZE)
    plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)
    raw = bytes([_SESSION_FORMAT_VERSION]) + nonce + ciphertext
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decrypt_session(token: str, secret: str) -> Dict[str, Any]:
    """
    Decrypt a session cookie value produced by encrypt_session().

    This only performs cryptographic verification -- it does NOT check
    `expires_at`. Callers (SessionRefreshManager) decide what to do with an
    expired-but-cryptographically-valid session (e.g. attempt a refresh using
    the refresh_token still present in the payload).

    :raises InvalidSessionError: if token is missing, malformed, tampered
        with, or uses an unsupported format version. Never raises any other
        exception type for these cases.
    """
    if not token:
        raise InvalidSessionError("no session cookie provided")

    key = _derive_key(secret)

    try:
        padding = "=" * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(token + padding)
        if len(raw) < 1 + _NONCE_SIZE:
            raise InvalidSessionError("session cookie is truncated")

        version = raw[0]
        if version != _SESSION_FORMAT_VERSION:
            raise InvalidSessionError(f"unsupported session format version: {version}")

        nonce = raw[1 : 1 + _NONCE_SIZE]
        ciphertext = raw[1 + _NONCE_SIZE :]
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
        payload = json.loads(plaintext)
    except InvalidSessionError:
        raise
    except Exception as exc:
        raise InvalidSessionError(
            "session cookie is invalid or has been tampered with"
        ) from exc

    if not isinstance(payload, dict):
        raise InvalidSessionError("decrypted session payload is not an object")

    return payload

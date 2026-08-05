from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from scalekit.middleware.protocol import RequestAdapter, ResponseAdapter
from scalekit.middleware.session_crypto import (
    InvalidSessionError,
    decrypt_session,
    encrypt_session,
)

DEFAULT_COOKIE_NAME = "sk_session"

# Refresh a little before the stored expiry so a request doesn't race the exact
# expiry instant against network latency to the token endpoint.
_EXPIRY_LEEWAY_SECONDS = 10

# How long a completed refresh outcome stays cached for singleflight coalescing
# before it's swept. Comfortably longer than Scalekit's server-side refresh-token
# rotation grace window (~30s) so same-process concurrent callers racing within
# that window all land on the cached result rather than each hitting the network.
_REFRESH_CACHE_TTL_SECONDS = 60


@dataclass
class SessionResult:
    """Outcome of processing one request through SessionRefreshManager.check()."""

    authenticated: bool
    user: Optional[Dict[str, Any]] = None
    new_cookie_value: Optional[str] = None  # set when the session was refreshed
    should_clear_cookie: bool = False
    reason: Optional[str] = None  # "no_session" | "invalid_session" | "refresh_failed"


@dataclass
class _RefreshOutcome:
    session_result: SessionResult
    created_at: float


class SessionRefreshManager:
    """
    Framework-agnostic session state machine: decrypts the session cookie,
    checks expiry, transparently refreshes via the Scalekit client when
    needed, and reports what the framework adapter should do next (proceed /
    set a new cookie / clear the cookie and redirect to login).

    Concurrent requests for the *same* session within one process are
    coalesced so only one actual refresh call is made -- see check().
    Framework adapters (Flask, FastAPI, Django, ...) call `check()` on every
    request and `apply()` to translate the result into cookie side effects on
    the outgoing response; they never implement this state machine themselves.
    """

    def __init__(
        self,
        client: Any,  # scalekit.ScalekitClient -- untyped to avoid a circular import
        cookie_encryption_secret: str,
        cookie_name: str = DEFAULT_COOKIE_NAME,
    ):
        if not cookie_encryption_secret:
            raise ValueError(
                "cookie_encryption_secret is required. Generate a strong random "
                'secret, e.g. `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`, '
                "and keep it identical across every server instance -- there is "
                "intentionally no default, since a shared default secret would let "
                "any deployment decrypt or forge any other deployment's sessions."
            )
        self._client = client
        self._secret = cookie_encryption_secret
        self.cookie_name = cookie_name

        self._locks_guard = threading.Lock()
        self._session_locks: Dict[str, threading.Lock] = {}
        self._refresh_cache: Dict[str, _RefreshOutcome] = {}

    def _lock_for(self, key: str) -> threading.Lock:
        with self._locks_guard:
            lock = self._session_locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._session_locks[key] = lock
            return lock

    def _sweep_expired_locked(self) -> None:
        """Evict refresh-cache/lock entries older than the TTL. Caller must hold no lock."""
        now = time.time()
        with self._locks_guard:
            stale = [
                key
                for key, outcome in self._refresh_cache.items()
                if now - outcome.created_at > _REFRESH_CACHE_TTL_SECONDS
            ]
            for key in stale:
                self._refresh_cache.pop(key, None)
                self._session_locks.pop(key, None)

    def check(self, request: RequestAdapter) -> SessionResult:
        """Decide what to do with the incoming request's session cookie."""
        cookie_value = request.get_cookie(self.cookie_name)
        if not cookie_value:
            return SessionResult(authenticated=False, reason="no_session")

        try:
            payload = decrypt_session(cookie_value, self._secret)
        except InvalidSessionError:
            return SessionResult(
                authenticated=False, should_clear_cookie=True, reason="invalid_session"
            )

        expires_at = payload.get("expires_at", 0)
        if expires_at - _EXPIRY_LEEWAY_SECONDS > time.time():
            return SessionResult(authenticated=True, user=payload.get("user"))

        refresh_token = payload.get("refresh_token")
        if not refresh_token:
            return SessionResult(
                authenticated=False, should_clear_cookie=True, reason="invalid_session"
            )

        return self._refresh(refresh_token, payload)

    def _refresh(self, refresh_token: str, old_payload: Dict[str, Any]) -> SessionResult:
        self._sweep_expired_locked()
        lock = self._lock_for(refresh_token)
        with lock:
            cached = self._refresh_cache.get(refresh_token)
            if cached is not None:
                return cached.session_result

            try:
                result = self._client.refresh_access_token(refresh_token)
                new_payload = dict(old_payload)
                new_payload["access_token"] = result["access_token"]
                new_payload["refresh_token"] = result["refresh_token"]
                new_payload["expires_at"] = time.time() + result.get("expires_in", 300)
                new_cookie_value = encrypt_session(new_payload, self._secret)
                session_result = SessionResult(
                    authenticated=True,
                    user=new_payload.get("user"),
                    new_cookie_value=new_cookie_value,
                )
            except Exception:
                session_result = SessionResult(
                    authenticated=False,
                    should_clear_cookie=True,
                    reason="refresh_failed",
                )

            self._refresh_cache[refresh_token] = _RefreshOutcome(
                session_result=session_result, created_at=time.time()
            )
            return session_result

    def create_session_cookie(self, payload: Dict[str, Any]) -> str:
        """Encrypt a fresh session payload (e.g. right after authenticate_with_code)."""
        return encrypt_session(payload, self._secret)

    def apply(self, result: SessionResult, response: ResponseAdapter) -> None:
        """Apply a SessionResult's cookie side effects to an outgoing response."""
        if result.new_cookie_value:
            response.set_cookie(self.cookie_name, result.new_cookie_value)
        elif result.should_clear_cookie:
            response.delete_cookie(self.cookie_name)

from __future__ import annotations

import logging
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

logger = logging.getLogger("scalekit.middleware.session_manager")


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


@dataclass
class _LockEntry:
    lock: threading.Lock
    # Number of callers currently holding a reference to `lock` between
    # `_lock_for()` returning and them finishing their `with lock:` block --
    # see `_sweep_expired_locked` for why eviction must respect this.
    ref_count: int = 0


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
        self._session_locks: Dict[str, _LockEntry] = {}
        self._refresh_cache: Dict[str, _RefreshOutcome] = {}

    def _lock_for(self, key: str) -> threading.Lock:
        with self._locks_guard:
            entry = self._session_locks.get(key)
            if entry is None:
                entry = _LockEntry(lock=threading.Lock())
                self._session_locks[key] = entry
            entry.ref_count += 1
            return entry.lock

    def _release_lock_ref(self, key: str) -> None:
        with self._locks_guard:
            entry = self._session_locks.get(key)
            if entry is not None:
                entry.ref_count -= 1

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
                entry = self._session_locks.get(key)
                if entry is not None and entry.ref_count > 0:
                    # A caller already holds a reference to this lock (got it from
                    # _lock_for but hasn't reached `with lock:` yet) and may still
                    # rely on reading this cached outcome once it does -- evicting
                    # out from under it would force a redundant, possibly-failing
                    # refresh call for an already-rotated token. Leave both entries
                    # in place; a later sweep will clean them up once ref_count
                    # drops back to 0.
                    continue
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
        try:
            with lock:
                cached = self._refresh_cache.get(refresh_token)
                if cached is not None:
                    return cached.session_result

                try:
                    result = self._client.refresh_access_token(refresh_token)
                    new_access_token = result["access_token"]
                    # Re-derive user/claims from the freshly-issued access token rather
                    # than carrying the old cached values forward. Access token claims
                    # (not id_token claims) are the source of truth here -- customers can
                    # configure custom access-token claims in the Scalekit dashboard, and
                    # unlike the id_token, the access token IS reissued on every refresh,
                    # so this keeps `user` genuinely current instead of stale-until-next-login.
                    claims = self._client.validate_access_token_and_get_claims(new_access_token)
                    new_payload = dict(old_payload)
                    new_payload["access_token"] = new_access_token
                    new_payload["refresh_token"] = result["refresh_token"]
                    new_payload["user"] = claims
                    new_payload["expires_at"] = claims.get("exp", time.time() + 300)
                    new_cookie_value = encrypt_session(new_payload, self._secret)
                    session_result = SessionResult(
                        authenticated=True,
                        user=new_payload.get("user"),
                        new_cookie_value=new_cookie_value,
                    )
                    self._refresh_cache[refresh_token] = _RefreshOutcome(
                        session_result=session_result, created_at=time.time()
                    )
                except Exception:
                    # Deliberately caught broadly -- any failure here means "treat as
                    # logged out," never a 500. But it must still be visible to
                    # whoever operates this app, so log it rather than swallow it.
                    logger.exception("token refresh failed; clearing session")
                    session_result = SessionResult(
                        authenticated=False,
                        should_clear_cookie=True,
                        reason="refresh_failed",
                    )
                    # Deliberately NOT cached: a failure here may be a transient
                    # network error (timeout, 503), not proof the refresh_token is
                    # actually dead. Caching it for the full TTL would pin every
                    # concurrent caller of this session to "logged out" for up to
                    # 60s with no chance to retry. Concurrent callers already in
                    # this `with lock:` block are still coalesced onto this single
                    # attempt; only a *later*, non-overlapping call gets to retry.

                return session_result
        finally:
            self._release_lock_ref(refresh_token)

    def create_session_cookie(self, payload: Dict[str, Any]) -> str:
        """Encrypt a fresh session payload (e.g. right after authenticate_with_code)."""
        return encrypt_session(payload, self._secret)

    def read_session(self, cookie_value: str) -> Optional[Dict[str, Any]]:
        """
        Decrypt a session cookie for read-only inspection (e.g. logout reading
        `id_token` for the logout hint), without going through the full
        expiry/refresh state machine in `check()`. Returns None instead of
        raising if the cookie is missing, malformed, or tampered with --
        framework adapters should never need to import InvalidSessionError
        or reach into this manager's internals to get at the payload.
        """
        try:
            return decrypt_session(cookie_value, self._secret)
        except InvalidSessionError:
            return None

    def apply(self, result: SessionResult, response: ResponseAdapter) -> None:
        """Apply a SessionResult's cookie side effects to an outgoing response."""
        if result.new_cookie_value:
            response.set_cookie(self.cookie_name, result.new_cookie_value)
        elif result.should_clear_cookie:
            response.delete_cookie(self.cookie_name)

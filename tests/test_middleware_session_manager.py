import threading
import time
import unittest
from unittest.mock import MagicMock

from scalekit.middleware.session_crypto import decrypt_session, encrypt_session
from scalekit.middleware.session_manager import SessionRefreshManager


class _FakeRequest:
    def __init__(self, cookie_value=None):
        self._cookie_value = cookie_value

    def get_cookie(self, name):
        return self._cookie_value

    def get_request_url(self):
        return "https://app.example.com/account"


class TestSessionRefreshManagerConstruction(unittest.TestCase):
    def test_missing_secret_raises_immediately(self):
        with self.assertRaises(ValueError):
            SessionRefreshManager(client=MagicMock(), cookie_encryption_secret="")


class TestSessionRefreshManagerCheck(unittest.TestCase):
    def setUp(self):
        self.secret = "test-secret-for-manager"
        self.client = MagicMock()
        self.manager = SessionRefreshManager(self.client, self.secret)

    def _cookie_for(self, expires_at, refresh_token="rt_original"):
        payload = {
            "user": {"email": "user@example.com"},
            "access_token": "at_old",
            "refresh_token": refresh_token,
            "expires_at": expires_at,
        }
        return encrypt_session(payload, self.secret)

    def test_no_cookie_present(self):
        result = self.manager.check(_FakeRequest(cookie_value=None))
        self.assertFalse(result.authenticated)
        self.assertEqual(result.reason, "no_session")
        self.assertFalse(result.should_clear_cookie)

    def test_malformed_cookie_is_invalid_session(self):
        result = self.manager.check(_FakeRequest(cookie_value="garbage-not-a-real-token"))
        self.assertFalse(result.authenticated)
        self.assertEqual(result.reason, "invalid_session")
        self.assertTrue(result.should_clear_cookie)

    def test_valid_unexpired_session_passes_through_without_refresh(self):
        cookie = self._cookie_for(expires_at=time.time() + 3600)
        result = self.manager.check(_FakeRequest(cookie_value=cookie))

        self.assertTrue(result.authenticated)
        self.assertEqual(result.user, {"email": "user@example.com"})
        self.assertIsNone(result.new_cookie_value)
        self.client.refresh_access_token.assert_not_called()

    def test_expired_session_triggers_refresh_and_returns_new_cookie(self):
        self.client.refresh_access_token.return_value = {
            "access_token": "at_new",
            "refresh_token": "rt_new",
        }
        fresh_expiry = time.time() + 300
        self.client.validate_access_token_and_get_claims.return_value = {
            "email": "user@example.com",
            "exp": fresh_expiry,
        }
        cookie = self._cookie_for(expires_at=time.time() - 10)  # already expired

        result = self.manager.check(_FakeRequest(cookie_value=cookie))

        self.assertTrue(result.authenticated)
        self.assertIsNotNone(result.new_cookie_value)
        self.client.refresh_access_token.assert_called_once_with("rt_original")
        self.client.validate_access_token_and_get_claims.assert_called_once_with("at_new")

        new_payload = decrypt_session(result.new_cookie_value, self.secret)
        self.assertEqual(new_payload["access_token"], "at_new")
        self.assertEqual(new_payload["refresh_token"], "rt_new")
        # user/claims must come from the freshly-issued access token, not the old cache
        self.assertEqual(new_payload["user"], {"email": "user@example.com", "exp": fresh_expiry})
        self.assertEqual(new_payload["expires_at"], fresh_expiry)

    def test_refresh_failure_clears_cookie_and_redirects(self):
        self.client.refresh_access_token.side_effect = Exception("invalid_grant")
        cookie = self._cookie_for(expires_at=time.time() - 10)

        result = self.manager.check(_FakeRequest(cookie_value=cookie))

        self.assertFalse(result.authenticated)
        self.assertTrue(result.should_clear_cookie)
        self.assertEqual(result.reason, "refresh_failed")

    def test_expired_session_with_no_refresh_token_is_invalid(self):
        payload_cookie = encrypt_session(
            {"user": {}, "access_token": "at_old", "refresh_token": None, "expires_at": time.time() - 10},
            self.secret,
        )
        result = self.manager.check(_FakeRequest(cookie_value=payload_cookie))

        self.assertFalse(result.authenticated)
        self.assertTrue(result.should_clear_cookie)
        self.client.refresh_access_token.assert_not_called()


class TestSessionRefreshManagerConcurrency(unittest.TestCase):
    """
    Proves the singleflight lock actually coalesces concurrent refresh attempts
    for the same (expired) session into a single real network call -- this is
    the exact race condition behind the forced-logout investigation this
    feature was motivated by.
    """

    def test_concurrent_requests_for_same_session_trigger_one_refresh_call(self):
        secret = "concurrency-test-secret"
        client = MagicMock()
        call_count_lock = threading.Lock()
        call_count = {"n": 0}

        def slow_refresh(refresh_token):
            with call_count_lock:
                call_count["n"] += 1
            time.sleep(0.05)  # simulate network latency, widening the race window
            return {"access_token": "at_new", "refresh_token": "rt_new", "expires_in": 300}

        client.refresh_access_token.side_effect = slow_refresh
        client.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }
        manager = SessionRefreshManager(client, secret)

        cookie = encrypt_session(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_old",
                "refresh_token": "rt_shared",
                "expires_at": time.time() - 10,
            },
            secret,
        )

        results = []
        results_lock = threading.Lock()

        def worker():
            result = manager.check(_FakeRequest(cookie_value=cookie))
            with results_lock:
                results.append(result)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)

        self.assertEqual(len(results), 20)
        self.assertEqual(
            call_count["n"], 1, "expected exactly one real refresh call across 20 concurrent requests"
        )
        for result in results:
            self.assertTrue(result.authenticated)
            self.assertIsNotNone(result.new_cookie_value)

    def test_sweep_does_not_evict_a_lock_a_caller_is_still_waiting_on(self):
        """
        A caller can obtain a lock reference from `_lock_for()` and pause before
        entering `with lock:`. If the TTL sweep then evicts that key's cache
        entry/lock out from under it, the paused caller misses the cached
        success and redundantly re-hits the (already-rotated) refresh_token --
        which can fail outside Scalekit's rotation grace window and force a
        needless logout. The sweep must not evict a key while ref_count > 0.
        """
        manager = SessionRefreshManager(MagicMock(), "sweep-race-secret")
        key = "rt_paused_caller"

        # Simulate a paused caller: it already called _lock_for() (ref_count=1)
        # but hasn't reached `with lock:` yet.
        manager._lock_for(key)

        # Simulate a completed refresh for this same key, stale enough to be
        # swept (older than the TTL).
        from scalekit.middleware.session_manager import _RefreshOutcome, SessionResult

        manager._refresh_cache[key] = _RefreshOutcome(
            session_result=SessionResult(authenticated=True, user={"email": "user@example.com"}),
            created_at=time.time() - 1000,  # well past the TTL
        )

        manager._sweep_expired_locked()

        self.assertIn(
            key,
            manager._refresh_cache,
            "cache entry must survive the sweep while a caller still holds a lock reference",
        )
        self.assertIn(key, manager._session_locks)

        # Once the paused caller finishes (releases its reference), a later
        # sweep is free to clean it up.
        manager._release_lock_ref(key)
        manager._sweep_expired_locked()
        self.assertNotIn(key, manager._refresh_cache)
        self.assertNotIn(key, manager._session_locks)

    def test_retries_after_a_transient_refresh_failure(self):
        """
        A failed refresh must not be cached for the full TTL -- only a
        successful rotation should be. Otherwise a transient network error
        (timeout, 503) pins every caller of this session to "logged out" for
        up to 60s with no chance to retry.
        """
        client = MagicMock()
        attempts = {"n": 0}

        def flaky_refresh(refresh_token):
            attempts["n"] += 1
            if attempts["n"] == 1:
                raise Exception("ETIMEDOUT")
            return {"access_token": "at_new", "refresh_token": "rt_new"}

        client.refresh_access_token.side_effect = flaky_refresh
        client.validate_access_token_and_get_claims.return_value = {
            "email": "user@example.com",
            "exp": time.time() + 300,
        }
        secret = "retry-after-failure-secret"
        manager = SessionRefreshManager(client, secret)
        cookie = encrypt_session(
            {
                "user": {"email": "user@example.com"},
                "access_token": "at_old",
                "refresh_token": "rt_shared",
                "expires_at": time.time() - 10,
            },
            secret,
        )

        first = manager.check(_FakeRequest(cookie_value=cookie))
        self.assertFalse(first.authenticated)
        self.assertEqual(first.reason, "refresh_failed")

        second = manager.check(_FakeRequest(cookie_value=cookie))
        self.assertTrue(second.authenticated)
        self.assertIsNotNone(second.new_cookie_value)
        self.assertEqual(attempts["n"], 2, "the second check() must actually retry, not reuse a cached failure")

    def test_lock_entry_is_cleaned_up_after_an_uncached_failed_refresh(self):
        """
        A failed refresh is deliberately never cached (see _refresh). Without
        also removing the lock entry once the last holder releases it,
        _sweep_expired_locked would never clean it up either -- it only
        considers keys present in _refresh_cache -- so every distinct
        refresh_token that ever fails would leak a _LockEntry forever.
        """
        client = MagicMock()
        client.refresh_access_token.side_effect = Exception("invalid_grant")
        secret = "lock-leak-secret"
        manager = SessionRefreshManager(client, secret)
        cookie = encrypt_session(
            {
                "user": {},
                "access_token": "at_old",
                "refresh_token": "rt_dead",
                "expires_at": time.time() - 10,
            },
            secret,
        )

        result = manager.check(_FakeRequest(cookie_value=cookie))

        self.assertFalse(result.authenticated)
        self.assertNotIn("rt_dead", manager._refresh_cache)
        self.assertNotIn(
            "rt_dead",
            manager._session_locks,
            "the lock entry for a permanently-failed, uncached refresh must not leak",
        )


class TestSessionRefreshManagerReadSession(unittest.TestCase):
    def test_read_session_returns_payload_for_valid_cookie(self):
        secret = "read-session-secret"
        manager = SessionRefreshManager(MagicMock(), secret)
        cookie = encrypt_session({"id_token": "idt_1"}, secret)

        payload = manager.read_session(cookie)

        self.assertEqual(payload, {"id_token": "idt_1"})

    def test_read_session_returns_none_for_invalid_cookie(self):
        manager = SessionRefreshManager(MagicMock(), "read-session-secret")

        self.assertIsNone(manager.read_session("not-a-valid-cookie"))


if __name__ == "__main__":
    unittest.main()

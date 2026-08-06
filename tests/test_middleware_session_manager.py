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


if __name__ == "__main__":
    unittest.main()

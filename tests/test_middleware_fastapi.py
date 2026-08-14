import time
import unittest
from unittest.mock import MagicMock

from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient

from scalekit.frameworks.fastapi import ScalekitAuth
from scalekit.middleware.session_crypto import decrypt_session


def _build_app(client=None, secret="fastapi-test-secret", **auth_kwargs):
    app = FastAPI()
    mock_client = client or MagicMock()
    auth = ScalekitAuth(
        client=mock_client,
        redirect_uri="https://app.example.com/callback",
        cookie_encryption_secret=secret,
        **auth_kwargs,
    )
    auth.install(app)

    @app.get("/account")
    async def account(user: dict = Depends(auth.requires_auth)):
        return {"email": user["email"]}

    return app, auth, mock_client


def _https_client(app):
    # httpx's cookie jar (unlike Flask's test client) correctly refuses to
    # resend a Secure cookie over a plain http:// request -- our state/session
    # cookies are Secure by default, matching real deployment behind TLS, so
    # the test client must actually be https to exercise that round trip.
    return TestClient(app, base_url="https://testserver")


def _login_and_get_state(tc):
    """Drive /login through the test client to obtain a valid state cookie,
    exactly as a real browser would before hitting /callback."""
    tc.get("/login", follow_redirects=False)
    return tc.cookies.get("sk_oauth_state")


class TestScalekitAuthFastAPI(unittest.TestCase):
    def test_login_redirects_to_authorization_url(self):
        app, auth, client = _build_app()
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize?client_id=x"

        with _https_client(app) as tc:
            resp = tc.get("/login", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_login_with_idp_initiated_login_uses_claims_for_authorization_url(self):
        app, auth, client = _build_app()
        client.get_idp_initiated_login_claims.return_value = {
            "connection_id": "conn_123",
            "organization_id": "org_456",
            "login_hint": "user@example.com",
        }
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize?client_id=x"

        with _https_client(app) as tc:
            resp = tc.get("/login?idp_initiated_login=some.jwt.token", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        client.get_idp_initiated_login_claims.assert_called_once_with("some.jwt.token")
        call_options = client.get_authorization_url.call_args[0][1]
        self.assertEqual(call_options.connection_id, "conn_123")
        self.assertEqual(call_options.organization_id, "org_456")
        self.assertEqual(call_options.login_hint, "user@example.com")

    def test_login_with_invalid_idp_initiated_login_falls_back_to_normal_login(self):
        app, auth, client = _build_app()
        client.get_idp_initiated_login_claims.side_effect = Exception("invalid token")
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize?client_id=x"

        with _https_client(app) as tc:
            resp = tc.get("/login?idp_initiated_login=garbage", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_callback_sets_encrypted_cookie_and_redirects(self):
        app, auth, client = _build_app(secret="callback-secret")
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"
        client.authenticate_with_code.return_value = {
            "user": {"email": "test.user@example.com"},
            "access_token": "at_1",
            "refresh_token": "rt_1",
            "id_token": "idt_1",
            "expires_in": 300,
        }
        client.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }

        with _https_client(app) as tc:
            state = _login_and_get_state(tc)
            resp = tc.get(f"/callback?code=abc123&state={state}", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = resp.headers.get("set-cookie", "")
        self.assertIn("sk_session=", set_cookie_header)
        self.assertIn("HttpOnly", set_cookie_header)
        self.assertIn("Secure", set_cookie_header)

    def test_callback_with_provider_error_redirects_to_login_not_500(self):
        app, auth, client = _build_app()

        with _https_client(app) as tc:
            resp = tc.get("/callback?error=access_denied", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

    def test_callback_with_missing_code_redirects_to_login(self):
        app, auth, client = _build_app()

        with _https_client(app) as tc:
            resp = tc.get("/callback", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

    def test_callback_with_missing_state_redirects_to_login(self):
        # No /login call at all -- no state cookie exists, simulating a
        # forged callback URL sent directly to a victim.
        app, auth, client = _build_app()

        with _https_client(app) as tc:
            resp = tc.get("/callback?code=abc123&state=whatever", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

    def test_callback_with_mismatched_state_redirects_to_login(self):
        app, auth, client = _build_app()
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"

        with _https_client(app) as tc:
            _login_and_get_state(tc)
            resp = tc.get("/callback?code=abc123&state=attacker-supplied", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

    def test_protected_route_without_cookie_redirects_to_login_not_json_401(self):
        # Same property tested for Flask: "no valid session" must be a real
        # redirect a browser follows, not a JSON 401 a background fetch would
        # silently swallow -- that's exactly the failure mode behind the
        # forced-logout incident this feature was motivated by.
        app, auth, client = _build_app()

        with _https_client(app) as tc:
            resp = tc.get("/account", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login?returnTo=%2Faccount")
        self.assertNotEqual(resp.headers.get("content-type"), "application/json")

    def test_protected_route_with_valid_session_succeeds(self):
        app, auth, client = _build_app(secret="valid-session-secret")
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with _https_client(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/account")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["email"], "test.user@example.com")
        client.refresh_access_token.assert_not_called()

    def test_protected_route_with_expired_session_refreshes_transparently(self):
        app, auth, client = _build_app(secret="expired-session-secret")
        client.refresh_access_token.return_value = {
            "access_token": "at_new",
            "refresh_token": "rt_new",
        }
        client.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_old",
                "refresh_token": "rt_old",
                "expires_at": time.time() - 10,
            }
        )

        with _https_client(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/account")

        self.assertEqual(resp.status_code, 200)
        client.refresh_access_token.assert_called_once_with("rt_old")

        set_cookie_header = resp.headers.get("set-cookie", "")
        self.assertIn("sk_session=", set_cookie_header)
        new_cookie_value = resp.cookies.get("sk_session")  # this response's cookie, not the client-wide jar
        new_payload = decrypt_session(new_cookie_value, "expired-session-secret")
        self.assertEqual(new_payload["access_token"], "at_new")

    def test_protected_route_with_failed_refresh_clears_cookie_and_redirects(self):
        app, auth, client = _build_app(secret="failed-refresh-secret")
        client.refresh_access_token.side_effect = Exception("invalid_grant")
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "user@example.com"},
                "access_token": "at_old",
                "refresh_token": "rt_old",
                "expires_at": time.time() - 10,
            }
        )

        with _https_client(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/account", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login?returnTo=%2Faccount")

    def test_logout_with_invalid_cookie_falls_back_to_local_redirect(self):
        app, auth, client = _build_app()

        with _https_client(app) as tc:
            tc.cookies.set("sk_session", "some-value")
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = resp.headers.get("set-cookie", "")
        self.assertIn('sk_session=""', set_cookie_header)
        self.assertIn("Max-Age=0", set_cookie_header)
        client.get_logout_url.assert_not_called()

    def test_logout_without_any_cookie_falls_back_to_local_redirect(self):
        app, auth, client = _build_app()

        with _https_client(app) as tc:
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        client.get_logout_url.assert_not_called()

    def test_logout_with_valid_session_does_full_logout_via_id_token_hint(self):
        app, auth, client = _build_app(secret="full-logout-secret")
        client.get_logout_url.return_value = "https://auth.example.com/oidc/logout?id_token_hint=abc"
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "id_token": "idt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with _https_client(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oidc/logout?id_token_hint=abc")
        set_cookie_header = resp.headers.get("set-cookie", "")
        # local cookie is actually cleared too, not just present/reissued
        self.assertIn('sk_session=""', set_cookie_header)
        self.assertIn("Max-Age=0", set_cookie_header)

        call_options = client.get_logout_url.call_args[0][0]
        self.assertEqual(call_options.id_token_hint, "idt_1")
        self.assertTrue(call_options.post_logout_redirect_uri.startswith("https://"))

    def test_full_logout_disabled_does_local_only_logout(self):
        app, auth, client = _build_app(secret="local-only-secret", full_logout=False)
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "id_token": "idt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with _https_client(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        client.get_logout_url.assert_not_called()
        set_cookie_header = resp.headers.get("set-cookie", "")
        self.assertIn('sk_session=""', set_cookie_header)
        self.assertIn("Max-Age=0", set_cookie_header)


class TestScalekitAuthFastAPIConstruction(unittest.TestCase):
    def test_missing_cookie_secret_raises_immediately(self):
        with self.assertRaises(ValueError):
            ScalekitAuth(
                client=MagicMock(),
                redirect_uri="https://app.example.com/callback",
                cookie_encryption_secret="",
            )

    def test_missing_redirect_uri_raises_immediately(self):
        with self.assertRaises(ValueError):
            ScalekitAuth(client=MagicMock(), cookie_encryption_secret="some-secret")


class TestScalekitAuthFastAPIReturnTo(unittest.TestCase):
    def test_login_redirect_round_trips_back_to_originally_requested_page(self):
        app, auth, client = _build_app(secret="return-to-secret")
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"
        client.authenticate_with_code.return_value = {
            "user": {"email": "test.user@example.com"},
            "access_token": "at_1",
            "refresh_token": "rt_1",
            "id_token": "idt_1",
            "expires_in": 300,
        }
        client.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }

        with _https_client(app) as tc:
            gate_resp = tc.get("/account", follow_redirects=False)
            self.assertEqual(gate_resp.headers["Location"], "/login?returnTo=%2Faccount")

            tc.get(gate_resp.headers["Location"], follow_redirects=False)
            state = tc.cookies.get("sk_oauth_state")
            self.assertEqual(tc.cookies.get("sk_return_to").strip(chr(34)), "/account")

            callback_resp = tc.get(f"/callback?code=abc123&state={state}", follow_redirects=False)

        self.assertEqual(callback_resp.status_code, 302)
        self.assertEqual(callback_resp.headers["Location"], "/account")

    def test_login_rejects_absolute_url_return_to_falls_back_to_default(self):
        app, auth, client = _build_app(secret="open-redirect-secret")
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"
        client.authenticate_with_code.return_value = {
            "user": {"email": "test.user@example.com"},
            "access_token": "at_1",
            "expires_in": 300,
        }
        client.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }

        with _https_client(app) as tc:
            tc.get("/login?returnTo=https://evil.com", follow_redirects=False)
            self.assertIsNone(tc.cookies.get("sk_return_to"))
            state = tc.cookies.get("sk_oauth_state")
            resp = tc.get(f"/callback?code=abc123&state={state}", follow_redirects=False)

        self.assertEqual(resp.headers["Location"], "/")


class TestScalekitAuthFastAPIGetSession(unittest.TestCase):
    def test_get_session_returns_curated_user_and_expiry_for_valid_cookie(self):
        app, auth, client = _build_app(secret="get-session-secret")
        expires_at = time.time() + 3600
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "id_token": "idt_1",
                "expires_at": expires_at,
            }
        )

        @app.get("/whoami")
        async def whoami(request: Request):
            return {"session": auth.get_session(request)}

        with _https_client(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/whoami")

        self.assertEqual(
            resp.json()["session"],
            {"user": {"email": "test.user@example.com"}, "expires_at": expires_at},
        )

    def test_get_session_returns_none_for_missing_cookie(self):
        app, auth, client = _build_app(secret="get-session-secret-2")

        @app.get("/whoami")
        async def whoami(request: Request):
            return {"session": auth.get_session(request)}

        with _https_client(app) as tc:
            resp = tc.get("/whoami")

        self.assertIsNone(resp.json()["session"])


class TestScalekitAuthFastAPICookieSecure(unittest.TestCase):
    def test_cookie_secure_false_omits_secure_attribute_for_local_http_dev(self):
        app, auth, client = _build_app(secret="cookie-secure-secret", cookie_secure=False)
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"

        with _https_client(app) as tc:
            resp = tc.get("/login", follow_redirects=False)

        set_cookie_header = resp.headers.get("set-cookie", "")
        self.assertNotIn("Secure", set_cookie_header)


if __name__ == "__main__":
    unittest.main()

import time
import unittest
from unittest.mock import MagicMock

from fastapi import Depends, FastAPI
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


class TestScalekitAuthFastAPI(unittest.TestCase):
    def test_login_redirects_to_authorization_url(self):
        app, auth, client = _build_app()
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize?client_id=x"

        with TestClient(app) as tc:
            resp = tc.get("/login", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_callback_sets_encrypted_cookie_and_redirects(self):
        app, auth, client = _build_app(secret="callback-secret")
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

        with TestClient(app) as tc:
            resp = tc.get("/callback?code=abc123", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = resp.headers.get("set-cookie", "")
        self.assertIn("sk_session=", set_cookie_header)
        self.assertIn("HttpOnly", set_cookie_header)
        self.assertIn("Secure", set_cookie_header)

    def test_protected_route_without_cookie_redirects_to_login_not_json_401(self):
        # Same property tested for Flask: "no valid session" must be a real
        # redirect a browser follows, not a JSON 401 a background fetch would
        # silently swallow -- that's exactly the failure mode behind the
        # forced-logout incident this feature was motivated by.
        app, auth, client = _build_app()

        with TestClient(app) as tc:
            resp = tc.get("/account", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
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

        with TestClient(app) as tc:
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

        with TestClient(app) as tc:
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

        with TestClient(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/account", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")

    def test_logout_with_invalid_cookie_falls_back_to_local_redirect(self):
        app, auth, client = _build_app()

        with TestClient(app) as tc:
            tc.cookies.set("sk_session", "some-value")
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        client.get_logout_url.assert_not_called()

    def test_logout_without_any_cookie_falls_back_to_local_redirect(self):
        app, auth, client = _build_app()

        with TestClient(app) as tc:
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

        with TestClient(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oidc/logout?id_token_hint=abc")
        set_cookie_header = resp.headers.get("set-cookie", "")
        self.assertIn("sk_session=", set_cookie_header)

        call_options = client.get_logout_url.call_args[0][0]
        self.assertEqual(call_options.id_token_hint, "idt_1")
        self.assertTrue(call_options.post_logout_redirect_uri.startswith("http://"))

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

        with TestClient(app) as tc:
            tc.cookies.set("sk_session", cookie_value)
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        client.get_logout_url.assert_not_called()


class TestScalekitAuthFastAPIConstruction(unittest.TestCase):
    def test_missing_cookie_secret_raises_immediately(self):
        with self.assertRaises(ValueError):
            ScalekitAuth(
                client=MagicMock(),
                redirect_uri="https://app.example.com/callback",
                cookie_encryption_secret="",
            )


if __name__ == "__main__":
    unittest.main()

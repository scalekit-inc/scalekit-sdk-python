import time
import unittest
from unittest.mock import MagicMock

from flask import Flask

from scalekit.frameworks.flask import ScalekitAuth
from scalekit.middleware.session_crypto import decrypt_session


def _build_app(client=None, secret="flask-test-secret"):
    app = Flask(__name__)
    app.testing = True
    mock_client = client or MagicMock()
    auth = ScalekitAuth(
        app,
        client=mock_client,
        redirect_uri="https://app.example.com/callback",
        cookie_encryption_secret=secret,
    )

    @app.route("/account")
    @auth.requires_auth
    def account():
        return f"hello {auth.current_user['email']}"

    return app, auth, mock_client


class TestScalekitAuthFlask(unittest.TestCase):
    def test_login_redirects_to_authorization_url(self):
        app, auth, client = _build_app()
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize?client_id=x"

        with app.test_client() as tc:
            resp = tc.get("/login", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_callback_sets_encrypted_cookie_and_redirects(self):
        app, auth, client = _build_app(secret="callback-secret")
        client.authenticate_with_code.return_value = {
            "user": {"email": "alper.gondiken@bloomreach.com"},
            "access_token": "at_1",
            "refresh_token": "rt_1",
            "expires_in": 300,
        }

        with app.test_client() as tc:
            resp = tc.get("/callback?code=abc123", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = resp.headers.get("Set-Cookie", "")
        self.assertIn("sk_session=", set_cookie_header)
        self.assertIn("HttpOnly", set_cookie_header)
        self.assertIn("Secure", set_cookie_header)
        self.assertIn("SameSite=Lax", set_cookie_header)

    def test_protected_route_without_cookie_redirects_to_login_not_json_401(self):
        # This is the exact property whose absence caused the forced-logout
        # incident this feature is motivated by: on "no valid session," the
        # response must be a real redirect a browser will follow, not a JSON
        # 401 a background fetch/XHR would silently swallow.
        app, auth, client = _build_app()

        with app.test_client() as tc:
            resp = tc.get("/account", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        self.assertNotEqual(resp.content_type, "application/json")

    def test_protected_route_with_valid_session_succeeds(self):
        app, auth, client = _build_app(secret="valid-session-secret")
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "alper.gondiken@bloomreach.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account")

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"alper.gondiken@bloomreach.com", resp.data)
        client.refresh_access_token.assert_not_called()

    def test_protected_route_with_expired_session_refreshes_transparently(self):
        app, auth, client = _build_app(secret="expired-session-secret")
        client.refresh_access_token.return_value = {
            "access_token": "at_new",
            "refresh_token": "rt_new",
            "expires_in": 300,
        }
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "alper.gondiken@bloomreach.com"},
                "access_token": "at_old",
                "refresh_token": "rt_old",
                "expires_at": time.time() - 10,
            }
        )

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account")

        self.assertEqual(resp.status_code, 200)
        client.refresh_access_token.assert_called_once_with("rt_old")

        set_cookie_header = resp.headers.get("Set-Cookie", "")
        self.assertIn("sk_session=", set_cookie_header)
        new_cookie_value = tc.get_cookie("sk_session").value
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

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")

    def test_logout_clears_cookie_and_redirects(self):
        app, auth, client = _build_app()

        with app.test_client() as tc:
            tc.set_cookie("sk_session", "some-value")
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = resp.headers.get("Set-Cookie", "")
        self.assertIn("sk_session=", set_cookie_header)


class TestScalekitAuthConstruction(unittest.TestCase):
    def test_missing_cookie_secret_raises_immediately(self):
        app = Flask(__name__)
        with self.assertRaises(ValueError):
            ScalekitAuth(
                app,
                client=MagicMock(),
                redirect_uri="https://app.example.com/callback",
                cookie_encryption_secret="",
            )


if __name__ == "__main__":
    unittest.main()

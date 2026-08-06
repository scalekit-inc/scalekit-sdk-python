import time
import unittest
from unittest.mock import MagicMock

from flask import Flask, jsonify, redirect

from scalekit.frameworks.flask import ScalekitAuth
from scalekit.middleware.session_crypto import decrypt_session


def _build_app(client=None, secret="flask-test-secret", **auth_kwargs):
    app = Flask(__name__)
    app.testing = True
    mock_client = client or MagicMock()
    auth = ScalekitAuth(
        app,
        client=mock_client,
        redirect_uri="https://app.example.com/callback",
        cookie_encryption_secret=secret,
        **auth_kwargs,
    )

    @app.route("/account")
    @auth.requires_auth
    def account():
        return f"hello {auth.current_user['email']}"

    @app.route("/account-json")
    @auth.requires_auth
    def account_json():
        return {"email": auth.current_user["email"]}

    @app.route("/account-tuple")
    @auth.requires_auth
    def account_tuple():
        return "created", 201

    @app.route("/account-jsonify")
    @auth.requires_auth
    def account_jsonify():
        return jsonify(email=auth.current_user["email"])

    @app.route("/account-redirect")
    @auth.requires_auth
    def account_redirect():
        return redirect("/somewhere-else")

    return app, auth, mock_client


def _login_and_get_state(tc):
    """Drive /login through the test client to obtain a valid state cookie,
    exactly as a real browser would before hitting /callback."""
    tc.get("/login", follow_redirects=False)
    return tc.get_cookie("sk_oauth_state").value


class TestScalekitAuthFlask(unittest.TestCase):
    def test_login_redirects_to_authorization_url(self):
        app, auth, client = _build_app()
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize?client_id=x"

        with app.test_client() as tc:
            resp = tc.get("/login", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_login_with_idp_initiated_login_uses_claims_for_authorization_url(self):
        # /login doubles as the dashboard-registered "Initiate Login URL" --
        # Scalekit can land users here with an idp_initiated_login JWT (e.g.
        # an IdP portal tile click with an active session) instead of the
        # plain no-params hit.
        app, auth, client = _build_app()
        client.get_idp_initiated_login_claims.return_value = {
            "connection_id": "conn_123",
            "organization_id": "org_456",
            "login_hint": "user@example.com",
        }
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize?client_id=x"

        with app.test_client() as tc:
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

        with app.test_client() as tc:
            resp = tc.get("/login?idp_initiated_login=garbage", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")
        call_options = client.get_authorization_url.call_args[0][1]
        self.assertIsNone(call_options.connection_id)

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

        with app.test_client() as tc:
            state = _login_and_get_state(tc)
            resp = tc.get(f"/callback?code=abc123&state={state}", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = resp.headers.get("Set-Cookie", "")
        self.assertIn("sk_session=", set_cookie_header)
        self.assertIn("HttpOnly", set_cookie_header)
        self.assertIn("Secure", set_cookie_header)
        self.assertIn("SameSite=Lax", set_cookie_header)

    def test_callback_with_provider_error_redirects_to_login_not_500(self):
        app, auth, client = _build_app()

        with app.test_client() as tc:
            resp = tc.get("/callback?error=access_denied", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

    def test_callback_with_missing_code_redirects_to_login(self):
        app, auth, client = _build_app()

        with app.test_client() as tc:
            resp = tc.get("/callback", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

    def test_callback_with_missing_state_redirects_to_login(self):
        # No /login call at all -- no state cookie exists, simulating a
        # forged callback URL sent directly to a victim.
        app, auth, client = _build_app()

        with app.test_client() as tc:
            resp = tc.get("/callback?code=abc123&state=whatever", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

    def test_callback_with_mismatched_state_redirects_to_login(self):
        app, auth, client = _build_app()
        client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"

        with app.test_client() as tc:
            _login_and_get_state(tc)
            resp = tc.get("/callback?code=abc123&state=attacker-supplied", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        client.authenticate_with_code.assert_not_called()

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
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account")

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"test.user@example.com", resp.data)
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

    def test_logout_with_invalid_cookie_falls_back_to_local_redirect(self):
        app, auth, client = _build_app()

        with app.test_client() as tc:
            tc.set_cookie("sk_session", "some-value")  # undecryptable garbage
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = resp.headers.get("Set-Cookie", "")
        # Assert the cookie is actually cleared, not merely present -- "sk_session="
        # alone would also match a freshly re-issued valid cookie.
        self.assertIn("sk_session=;", set_cookie_header)
        self.assertIn("Expires=Thu, 01 Jan 1970", set_cookie_header)
        client.get_logout_url.assert_not_called()

    def test_logout_without_any_cookie_falls_back_to_local_redirect(self):
        app, auth, client = _build_app()

        with app.test_client() as tc:
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

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oidc/logout?id_token_hint=abc")
        set_cookie_header = resp.headers.get("Set-Cookie", "")
        # local cookie is actually cleared too, not just present/reissued
        self.assertIn("sk_session=;", set_cookie_header)
        self.assertIn("Expires=Thu, 01 Jan 1970", set_cookie_header)

        call_options = client.get_logout_url.call_args[0][0]
        self.assertEqual(call_options.id_token_hint, "idt_1")
        # Scalekit requires an absolute, allow-listed post-logout redirect URI --
        # a bare "/" gets absolutized against the request's own host.
        self.assertEqual(call_options.post_logout_redirect_uri, "http://localhost/")

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

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/logout", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        client.get_logout_url.assert_not_called()
        set_cookie_header = resp.headers.get("Set-Cookie", "")
        self.assertIn("sk_session=;", set_cookie_header)
        self.assertIn("Expires=Thu, 01 Jan 1970", set_cookie_header)

    def test_requires_auth_preserves_dict_return_as_json(self):
        app, auth, client = _build_app(secret="return-type-secret")
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account-json")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"email": "test.user@example.com"})

    def test_requires_auth_preserves_status_code_tuple_return(self):
        app, auth, client = _build_app(secret="return-type-secret-2")
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account-tuple")

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data, b"created")

    def test_requires_auth_preserves_jsonify_content_type(self):
        app, auth, client = _build_app(secret="return-type-secret-3")
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account-jsonify")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, "application/json")
        self.assertEqual(resp.json, {"email": "test.user@example.com"})

    def test_requires_auth_preserves_redirect_return(self):
        app, auth, client = _build_app(secret="return-type-secret-4")
        cookie_value = auth.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )

        with app.test_client() as tc:
            tc.set_cookie("sk_session", cookie_value)
            resp = tc.get("/account-redirect", follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/somewhere-else")


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

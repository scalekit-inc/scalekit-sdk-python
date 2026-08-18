import time
import unittest
from unittest.mock import MagicMock

import django
from django.conf import settings as django_settings

if not django_settings.configured:
    django_settings.configure(
        DEBUG=True,
        SECRET_KEY="django-test-secret-key",
        ALLOWED_HOSTS=["testserver"],
        ROOT_URLCONF="tests.test_middleware_django",  # this module doubles as urlconf below
        MIDDLEWARE=["scalekit.frameworks.django.ScalekitAuthMiddleware"],
        SCALEKIT_REDIRECT_URI="https://app.example.com/callback",
        SCALEKIT_COOKIE_ENCRYPTION_SECRET="django-test-cookie-secret",
        SCALEKIT_CLIENT=MagicMock(),
    )
    django.setup()

from django.http import HttpResponse
from django.test import Client
from django.urls import include, path

from scalekit.frameworks.django import get_config, get_session, login_required
from scalekit.middleware.session_crypto import decrypt_session


def account_view(request):
    return HttpResponse(f"hello {request.scalekit_user['email']}")


account_view = login_required(account_view)


def whoami_view(request):
    import json

    return HttpResponse(json.dumps({"session": get_session(request)}), content_type="application/json")


urlpatterns = [
    path("account", account_view),
    path("whoami", whoami_view),
    path("", include("scalekit.frameworks.django")),
]


def _reconfigure(secret=None, full_logout=None):
    """Force ScalekitAuthConfig to rebuild with fresh settings for this test."""
    get_config.cache_clear()
    if secret is not None:
        django_settings.SCALEKIT_COOKIE_ENCRYPTION_SECRET = secret
    if full_logout is not None:
        django_settings.SCALEKIT_FULL_LOGOUT = full_logout
    django_settings.SCALEKIT_CLIENT = MagicMock()
    return get_config()


def _login_and_get_state(tc):
    """Drive /login through the test client to obtain a valid state cookie,
    exactly as a real browser would before hitting /callback."""
    tc.get("/login")
    return tc.cookies["sk_oauth_state"].value


class TestScalekitAuthDjango(unittest.TestCase):
    def setUp(self):
        django_settings.SCALEKIT_FULL_LOGOUT = True
        self.config = _reconfigure(secret="django-test-cookie-secret")
        self.client_mock = self.config.client

    def tearDown(self):
        get_config.cache_clear()

    def test_login_redirects_to_authorization_url(self):
        self.client_mock.get_authorization_url.return_value = (
            "https://auth.example.com/oauth/authorize?client_id=x"
        )
        resp = Client().get("/login")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_login_with_idp_initiated_login_uses_claims_for_authorization_url(self):
        self.client_mock.get_idp_initiated_login_claims.return_value = {
            "connection_id": "conn_123",
            "organization_id": "org_456",
            "login_hint": "user@example.com",
        }
        self.client_mock.get_authorization_url.return_value = (
            "https://auth.example.com/oauth/authorize?client_id=x"
        )

        resp = Client().get("/login?idp_initiated_login=some.jwt.token")

        self.assertEqual(resp.status_code, 302)
        self.client_mock.get_idp_initiated_login_claims.assert_called_once_with("some.jwt.token")
        call_options = self.client_mock.get_authorization_url.call_args[0][1]
        self.assertEqual(call_options.connection_id, "conn_123")
        self.assertEqual(call_options.organization_id, "org_456")
        self.assertEqual(call_options.login_hint, "user@example.com")

    def test_login_with_invalid_idp_initiated_login_falls_back_to_normal_login(self):
        self.client_mock.get_idp_initiated_login_claims.side_effect = Exception("invalid token")
        self.client_mock.get_authorization_url.return_value = (
            "https://auth.example.com/oauth/authorize?client_id=x"
        )

        resp = Client().get("/login?idp_initiated_login=garbage")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_callback_sets_encrypted_cookie_and_redirects(self):
        self.client_mock.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"
        self.client_mock.authenticate_with_code.return_value = {
            "user": {"email": "test.user@example.com"},
            "access_token": "at_1",
            "refresh_token": "rt_1",
            "id_token": "idt_1",
            "expires_in": 300,
        }
        self.client_mock.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }

        tc = Client()
        state = _login_and_get_state(tc)
        resp = tc.get(f"/callback?code=abc123&state={state}")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = str(resp.cookies.get("sk_session", ""))
        self.assertIn("sk_session=", set_cookie_header)
        self.assertIn("HttpOnly", set_cookie_header)
        self.assertIn("Secure", set_cookie_header)

    def test_callback_with_provider_error_redirects_to_login_not_500(self):
        resp = Client().get("/callback?error=access_denied")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        self.client_mock.authenticate_with_code.assert_not_called()

    def test_callback_with_missing_code_redirects_to_login(self):
        resp = Client().get("/callback")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        self.client_mock.authenticate_with_code.assert_not_called()

    def test_callback_with_missing_state_redirects_to_login(self):
        # No /login call at all -- no state cookie exists, simulating a
        # forged callback URL sent directly to a victim.
        resp = Client().get("/callback?code=abc123&state=whatever")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        self.client_mock.authenticate_with_code.assert_not_called()

    def test_callback_with_mismatched_state_redirects_to_login(self):
        self.client_mock.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"
        tc = Client()
        _login_and_get_state(tc)
        resp = tc.get("/callback?code=abc123&state=attacker-supplied")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
        self.client_mock.authenticate_with_code.assert_not_called()

    def test_protected_route_without_cookie_redirects_to_login_not_json_401(self):
        # Same property tested for Flask/FastAPI: "no valid session" must be a
        # real redirect a browser follows, not a JSON 401 a background fetch
        # would silently swallow.
        resp = Client().get("/account")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login?returnTo=%2Faccount")
        self.assertNotEqual(resp.headers.get("Content-Type"), "application/json")

    def test_protected_route_with_valid_session_succeeds(self):
        cookie_value = self.config.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "expires_at": time.time() + 3600,
            }
        )
        tc = Client()
        tc.cookies["sk_session"] = cookie_value

        resp = tc.get("/account")

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"test.user@example.com", resp.content)
        self.client_mock.refresh_access_token.assert_not_called()

    def test_protected_route_with_expired_session_refreshes_transparently(self):
        self.client_mock.refresh_access_token.return_value = {
            "access_token": "at_new",
            "refresh_token": "rt_new",
        }
        self.client_mock.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }
        cookie_value = self.config.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_old",
                "refresh_token": "rt_old",
                "expires_at": time.time() - 10,
            }
        )
        tc = Client()
        tc.cookies["sk_session"] = cookie_value

        resp = tc.get("/account")

        self.assertEqual(resp.status_code, 200)
        self.client_mock.refresh_access_token.assert_called_once_with("rt_old")

        new_cookie_value = resp.cookies["sk_session"].value
        new_payload = decrypt_session(new_cookie_value, "django-test-cookie-secret")
        self.assertEqual(new_payload["access_token"], "at_new")

    def test_protected_route_with_failed_refresh_clears_cookie_and_redirects(self):
        self.client_mock.refresh_access_token.side_effect = Exception("invalid_grant")
        cookie_value = self.config.manager.create_session_cookie(
            {
                "user": {"email": "user@example.com"},
                "access_token": "at_old",
                "refresh_token": "rt_old",
                "expires_at": time.time() - 10,
            }
        )
        tc = Client()
        tc.cookies["sk_session"] = cookie_value

        resp = tc.get("/account")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login?returnTo=%2Faccount")

    def test_logout_without_any_cookie_falls_back_to_local_redirect(self):
        resp = Client().get("/logout")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        self.client_mock.get_logout_url.assert_not_called()

    def test_logout_with_valid_session_does_full_logout_via_id_token_hint(self):
        self.client_mock.get_logout_url.return_value = (
            "https://auth.example.com/oidc/logout?id_token_hint=abc"
        )
        cookie_value = self.config.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "id_token": "idt_1",
                "expires_at": time.time() + 3600,
            }
        )
        tc = Client()
        tc.cookies["sk_session"] = cookie_value

        resp = tc.get("/logout")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oidc/logout?id_token_hint=abc")

        call_options = self.client_mock.get_logout_url.call_args[0][0]
        self.assertEqual(call_options.id_token_hint, "idt_1")
        self.assertTrue(call_options.post_logout_redirect_uri.startswith("http://"))

    def test_full_logout_disabled_does_local_only_logout(self):
        self.config = _reconfigure(secret="django-test-cookie-secret", full_logout=False)
        self.client_mock = self.config.client
        cookie_value = self.config.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "id_token": "idt_1",
                "expires_at": time.time() + 3600,
            }
        )
        tc = Client()
        tc.cookies["sk_session"] = cookie_value

        resp = tc.get("/logout")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        self.client_mock.get_logout_url.assert_not_called()


class TestScalekitAuthDjangoConstruction(unittest.TestCase):
    def tearDown(self):
        get_config.cache_clear()

    def test_missing_cookie_secret_raises_immediately(self):
        get_config.cache_clear()
        # Restore via addCleanup, not a bare post-assertion line -- if the
        # assertion below ever failed, the setting would stay "" for every
        # later test in the run for an unrelated reason.
        self.addCleanup(
            setattr, django_settings, "SCALEKIT_COOKIE_ENCRYPTION_SECRET", "django-test-cookie-secret"
        )
        django_settings.SCALEKIT_COOKIE_ENCRYPTION_SECRET = ""
        django_settings.SCALEKIT_CLIENT = MagicMock()
        with self.assertRaises(ValueError):
            get_config()


class TestScalekitAuthDjangoReturnTo(unittest.TestCase):
    def setUp(self):
        self.config = _reconfigure(secret="django-test-cookie-secret")
        self.client_mock = self.config.client

    def tearDown(self):
        get_config.cache_clear()

    def test_login_redirect_round_trips_back_to_originally_requested_page(self):
        self.client_mock.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"
        self.client_mock.authenticate_with_code.return_value = {
            "user": {"email": "test.user@example.com"},
            "access_token": "at_1",
            "refresh_token": "rt_1",
            "id_token": "idt_1",
            "expires_in": 300,
        }
        self.client_mock.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }

        tc = Client()
        gate_resp = tc.get("/account")
        self.assertEqual(gate_resp.headers["Location"], "/login?returnTo=%2Faccount")

        tc.get(gate_resp.headers["Location"])
        state = tc.cookies["sk_oauth_state"].value
        self.assertEqual(tc.cookies["sk_return_to"].value, "/account")

        callback_resp = tc.get(f"/callback?code=abc123&state={state}")

        self.assertEqual(callback_resp.status_code, 302)
        self.assertEqual(callback_resp.headers["Location"], "/account")

    def test_login_rejects_absolute_url_return_to_falls_back_to_default(self):
        self.client_mock.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"
        self.client_mock.authenticate_with_code.return_value = {
            "user": {"email": "test.user@example.com"},
            "access_token": "at_1",
            "expires_in": 300,
        }
        self.client_mock.validate_access_token_and_get_claims.return_value = {
            "email": "test.user@example.com",
            "exp": time.time() + 300,
        }

        tc = Client()
        tc.get("/login?returnTo=https://evil.com")
        self.assertNotIn("sk_return_to", tc.cookies)
        state = tc.cookies["sk_oauth_state"].value
        resp = tc.get(f"/callback?code=abc123&state={state}")

        self.assertEqual(resp.headers["Location"], "/")


class TestScalekitAuthDjangoGetSession(unittest.TestCase):
    def setUp(self):
        self.config = _reconfigure(secret="django-test-cookie-secret")

    def tearDown(self):
        get_config.cache_clear()

    def test_get_session_returns_curated_user_and_expiry_for_valid_cookie(self):
        expires_at = time.time() + 3600
        cookie_value = self.config.manager.create_session_cookie(
            {
                "user": {"email": "test.user@example.com"},
                "access_token": "at_1",
                "refresh_token": "rt_1",
                "id_token": "idt_1",
                "expires_at": expires_at,
            }
        )
        tc = Client()
        tc.cookies["sk_session"] = cookie_value

        resp = tc.get("/whoami")

        self.assertEqual(
            resp.json()["session"],
            {"user": {"email": "test.user@example.com"}, "expires_at": expires_at},
        )

    def test_get_session_returns_none_for_missing_cookie(self):
        resp = Client().get("/whoami")

        self.assertIsNone(resp.json()["session"])


class TestScalekitAuthDjangoCookieSecure(unittest.TestCase):
    def tearDown(self):
        get_config.cache_clear()

    def test_cookie_secure_false_omits_secure_attribute_for_local_http_dev(self):
        get_config.cache_clear()
        django_settings.SCALEKIT_COOKIE_SECURE = False
        self.addCleanup(setattr, django_settings, "SCALEKIT_COOKIE_SECURE", True)
        config = get_config()
        config.client.get_authorization_url.return_value = "https://auth.example.com/oauth/authorize"

        resp = Client().get("/login")

        set_cookie_header = str(resp.cookies.get("sk_oauth_state", ""))
        self.assertNotIn("Secure", set_cookie_header)


if __name__ == "__main__":
    unittest.main()

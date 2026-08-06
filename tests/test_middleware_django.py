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

from scalekit.frameworks.django import get_config, login_required
from scalekit.middleware.session_crypto import decrypt_session


def account_view(request):
    return HttpResponse(f"hello {request.scalekit_user['email']}")


account_view = login_required(account_view)

urlpatterns = [
    path("account", account_view),
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
        resp = Client().get("/login/")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://auth.example.com/oauth/authorize?client_id=x")

    def test_callback_sets_encrypted_cookie_and_redirects(self):
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

        resp = Client().get("/callback/?code=abc123")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        set_cookie_header = str(resp.cookies.get("sk_session", ""))
        self.assertIn("sk_session=", set_cookie_header)
        self.assertIn("HttpOnly", set_cookie_header)
        self.assertIn("Secure", set_cookie_header)

    def test_protected_route_without_cookie_redirects_to_login_not_json_401(self):
        # Same property tested for Flask/FastAPI: "no valid session" must be a
        # real redirect a browser follows, not a JSON 401 a background fetch
        # would silently swallow.
        resp = Client().get("/account")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/login")
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
        self.assertEqual(resp.headers["Location"], "/login")

    def test_logout_without_any_cookie_falls_back_to_local_redirect(self):
        resp = Client().get("/logout/")

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

        resp = tc.get("/logout/")

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

        resp = tc.get("/logout/")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "/")
        self.client_mock.get_logout_url.assert_not_called()


class TestScalekitAuthDjangoConstruction(unittest.TestCase):
    def tearDown(self):
        get_config.cache_clear()

    def test_missing_cookie_secret_raises_immediately(self):
        get_config.cache_clear()
        django_settings.SCALEKIT_COOKIE_ENCRYPTION_SECRET = ""
        django_settings.SCALEKIT_CLIENT = MagicMock()
        with self.assertRaises(ValueError):
            get_config()
        django_settings.SCALEKIT_COOKIE_ENCRYPTION_SECRET = "django-test-cookie-secret"


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import time
from functools import lru_cache, wraps
from typing import Any, Callable, Optional

try:
    from django.conf import settings as django_settings
    from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
    from django.urls import path
except ImportError as exc:  # pragma: no cover -- exercised only without the extra installed
    raise ImportError(
        "Django integration requires the 'django' extra: "
        "pip install scalekit-sdk-python[django]"
    ) from exc

from scalekit.client import ScalekitClient
from scalekit.common.scalekit import (
    AuthorizationUrlOptions,
    CodeAuthenticationOptions,
    LogoutUrlOptions,
)
from scalekit.middleware.protocol import RequestAdapter, ResponseAdapter
from scalekit.middleware.session_crypto import InvalidSessionError, decrypt_session
from scalekit.middleware.session_manager import DEFAULT_COOKIE_NAME, SessionRefreshManager


class _DjangoRequestAdapter:
    """RequestAdapter implementation backed by a Django HttpRequest."""

    def __init__(self, request: HttpRequest):
        self._request = request

    def get_cookie(self, name: str) -> Optional[str]:
        return self._request.COOKIES.get(name)

    def get_request_url(self) -> str:
        return self._request.build_absolute_uri()


class _DjangoResponseAdapter:
    """ResponseAdapter implementation that mutates a Django HttpResponse in place."""

    def __init__(self, response: HttpResponse):
        self.response = response

    def set_cookie(
        self,
        name: str,
        value: str,
        *,
        max_age: Optional[int] = None,
        secure: bool = True,
        http_only: bool = True,
        same_site: str = "Lax",
        domain: Optional[str] = None,
        path: str = "/",
    ) -> None:
        self.response.set_cookie(
            name,
            value,
            max_age=max_age,
            secure=secure,
            httponly=http_only,
            samesite=same_site,
            domain=domain,
            path=path,
        )

    def delete_cookie(
        self, name: str, *, path: str = "/", domain: Optional[str] = None
    ) -> None:
        self.response.delete_cookie(name, path=path, domain=domain)


def _setting(name: str, default: Any = None, required: bool = False) -> Any:
    value = getattr(django_settings, name, default)
    if required and not value:
        raise ValueError(
            f"Django setting {name} is required to use scalekit.frameworks.django"
        )
    return value


class ScalekitAuthConfig:
    """
    Holds the shared ScalekitClient + SessionRefreshManager, built once from
    Django settings (all read with an SCALEKIT_ prefix, matching Django
    convention for third-party app config):

        SCALEKIT_CLIENT_ID, SCALEKIT_CLIENT_SECRET, SCALEKIT_ENV_URL,
        SCALEKIT_REDIRECT_URI, SCALEKIT_COOKIE_ENCRYPTION_SECRET (required --
        see scalekit.middleware.session_crypto for why there is intentionally
        no default), SCALEKIT_COOKIE_NAME (optional), SCALEKIT_LOGIN_PATH
        (optional, default "/login"), SCALEKIT_POST_LOGIN_REDIRECT (optional,
        default "/"), SCALEKIT_POST_LOGOUT_REDIRECT_URI (optional, falls back
        to SCALEKIT_POST_LOGIN_REDIRECT), SCALEKIT_FULL_LOGOUT (optional
        bool, default True).

    SCALEKIT_CLIENT (an already-constructed ScalekitClient) can be set
    directly, primarily for tests -- normal usage constructs one from the
    ID/secret/env_url settings above.
    """

    def __init__(self):
        client = _setting("SCALEKIT_CLIENT", None)
        if client is None:
            client = ScalekitClient(
                env_url=_setting("SCALEKIT_ENV_URL", required=True),
                client_id=_setting("SCALEKIT_CLIENT_ID", required=True),
                client_secret=_setting("SCALEKIT_CLIENT_SECRET", required=True),
            )
        self.client = client
        self.redirect_uri = _setting("SCALEKIT_REDIRECT_URI", required=True)
        self.login_path = _setting("SCALEKIT_LOGIN_PATH", "/login")
        self.post_login_redirect = _setting("SCALEKIT_POST_LOGIN_REDIRECT", "/")
        self.post_logout_redirect_uri = (
            _setting("SCALEKIT_POST_LOGOUT_REDIRECT_URI") or self.post_login_redirect
        )
        self.full_logout = _setting("SCALEKIT_FULL_LOGOUT", True)

        # Raises immediately if the secret is missing.
        self.manager = SessionRefreshManager(
            self.client,
            _setting("SCALEKIT_COOKIE_ENCRYPTION_SECRET", required=True),
            cookie_name=_setting("SCALEKIT_COOKIE_NAME", DEFAULT_COOKIE_NAME),
        )


@lru_cache(maxsize=1)
def get_config() -> ScalekitAuthConfig:
    return ScalekitAuthConfig()


class ScalekitAuthMiddleware:
    """
    Add to MIDDLEWARE in settings.py. Populates `request.scalekit_user` (None
    if not authenticated) and transparently refreshes the session cookie on
    every request. Mirrors Django's own convention (AuthenticationMiddleware
    populates `request.user`, `login_required` enforces it) -- this
    middleware does NOT itself enforce authentication; use `login_required`
    on individual views for that.
    """

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        config = get_config()
        result = config.manager.check(_DjangoRequestAdapter(request))
        request.scalekit_user = result.user if result.authenticated else None
        request.scalekit_session_result = result

        response = self.get_response(request)

        if result.new_cookie_value:
            _DjangoResponseAdapter(response).set_cookie(
                config.manager.cookie_name, result.new_cookie_value
            )
        elif result.should_clear_cookie:
            _DjangoResponseAdapter(response).delete_cookie(config.manager.cookie_name)

        return response


def login_required(view_func: Callable) -> Callable:
    """
    View decorator: redirects to SCALEKIT_LOGIN_PATH with a real 302 if
    `request.scalekit_user` isn't set. Requires ScalekitAuthMiddleware to be
    installed. Same "real redirect, never a JSON 401" guarantee as the
    Flask/FastAPI integrations -- a JSON 401 is exactly what a background
    fetch/XHR would silently swallow, which is the failure mode this whole
    design exists to avoid.
    """

    @wraps(view_func)
    def wrapped(request: HttpRequest, *args, **kwargs):
        if getattr(request, "scalekit_user", None) is None:
            return HttpResponseRedirect(get_config().login_path)
        return view_func(request, *args, **kwargs)

    return wrapped


def login_view(request: HttpRequest) -> HttpResponse:
    config = get_config()
    options = AuthorizationUrlOptions()
    # offline_access is required to get a refresh_token back at all -- see
    # scalekit.frameworks.flask for the full explanation.
    options.scopes = ["openid", "profile", "email", "offline_access"]
    url = config.client.get_authorization_url(config.redirect_uri, options)
    return HttpResponseRedirect(url)


def callback_view(request: HttpRequest) -> HttpResponse:
    config = get_config()
    code = request.GET.get("code")
    result = config.client.authenticate_with_code(
        code, config.redirect_uri, CodeAuthenticationOptions()
    )
    # Access-token claims (not id_token claims) are the source of truth for
    # `user` -- see scalekit.frameworks.flask for the full reasoning.
    claims = config.client.validate_access_token_and_get_claims(result["access_token"])
    payload = {
        "user": claims,
        "access_token": result["access_token"],
        "refresh_token": result.get("refresh_token"),
        "id_token": result.get("id_token"),
        "expires_at": claims.get("exp", time.time() + (result.get("expires_in") or 300)),
    }
    cookie_value = config.manager.create_session_cookie(payload)
    response = HttpResponseRedirect(config.post_login_redirect)
    _DjangoResponseAdapter(response).set_cookie(config.manager.cookie_name, cookie_value)
    return response


def logout_view(request: HttpRequest) -> HttpResponse:
    config = get_config()
    cookie_value = request.COOKIES.get(config.manager.cookie_name)
    id_token = None
    if cookie_value:
        try:
            payload = decrypt_session(cookie_value, config.manager._secret)
            id_token = payload.get("id_token")
        except InvalidSessionError:
            pass  # nothing usable to hint with -- fall through to local-only redirect

    redirect_url = config.post_logout_redirect_uri
    if config.full_logout and id_token:
        # Scalekit requires an absolute, dashboard-registered post-logout
        # redirect URI -- absolutize a relative default against the current
        # request, same as the Flask/FastAPI adapters.
        absolute_redirect_uri = config.post_logout_redirect_uri
        if not absolute_redirect_uri.startswith(("http://", "https://")):
            absolute_redirect_uri = request.build_absolute_uri(absolute_redirect_uri)
        options = LogoutUrlOptions()
        options.id_token_hint = id_token
        options.post_logout_redirect_uri = absolute_redirect_uri
        redirect_url = config.client.get_logout_url(options)

    response = HttpResponseRedirect(redirect_url)
    _DjangoResponseAdapter(response).delete_cookie(config.manager.cookie_name)
    return response


# Include via: path("auth/", include("scalekit.frameworks.django"))
urlpatterns = [
    path("login/", login_view, name="scalekit_login"),
    path("callback/", callback_view, name="scalekit_callback"),
    path("logout/", logout_view, name="scalekit_logout"),
]

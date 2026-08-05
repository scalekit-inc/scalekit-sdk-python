from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable, Dict, Optional

try:
    from flask import Flask, Response, g
    from flask import redirect as flask_redirect
    from flask import request as flask_request
except ImportError as exc:  # pragma: no cover -- exercised only without the extra installed
    raise ImportError(
        "Flask integration requires the 'flask' extra: "
        "pip install scalekit-sdk-python[flask]"
    ) from exc

from scalekit.client import ScalekitClient
from scalekit.common.scalekit import AuthorizationUrlOptions, CodeAuthenticationOptions
from scalekit.middleware.protocol import RequestAdapter, ResponseAdapter
from scalekit.middleware.session_manager import DEFAULT_COOKIE_NAME, SessionRefreshManager


class _FlaskRequestAdapter:
    """RequestAdapter implementation backed by Flask's request context."""

    def get_cookie(self, name: str) -> Optional[str]:
        return flask_request.cookies.get(name)

    def get_request_url(self) -> str:
        return flask_request.url


class _FlaskResponseAdapter:
    """ResponseAdapter implementation that mutates a Flask Response in place."""

    def __init__(self, response: Response):
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


class ScalekitAuth:
    """
    Flask extension wiring Scalekit Full Stack Auth into a Flask app with
    secure defaults out of the box: an encrypted session cookie, transparent
    token refresh on every request, and a `requires_auth` decorator to
    protect routes -- so the developer never hand-rolls cookie attributes,
    refresh timing, or expired/invalid/missing-session branching themselves.

    Usage:
        auth = ScalekitAuth(
            app,
            client_id=..., client_secret=..., env_url=...,
            redirect_uri="https://myapp.com/callback",
            cookie_encryption_secret=...,
        )

        @app.route("/account")
        @auth.requires_auth
        def account():
            return f"Hello {auth.current_user['email']}"
    """

    def __init__(
        self,
        app: Optional[Flask] = None,
        *,
        client: Optional[ScalekitClient] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        env_url: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        cookie_encryption_secret: Optional[str] = None,
        cookie_name: str = DEFAULT_COOKIE_NAME,
        login_path: str = "/login",
        callback_path: str = "/callback",
        logout_path: str = "/logout",
        post_login_redirect: str = "/",
    ):
        if client is None:
            client = ScalekitClient(env_url=env_url, client_id=client_id, client_secret=client_secret)
        self.client = client
        self.redirect_uri = redirect_uri
        self.login_path = login_path
        self.callback_path = callback_path
        self.logout_path = logout_path
        self.post_login_redirect = post_login_redirect

        # Raises immediately if cookie_encryption_secret is missing -- see
        # SessionRefreshManager and scalekit.middleware.session_crypto for why
        # there is intentionally no default.
        self.manager = SessionRefreshManager(
            self.client, cookie_encryption_secret, cookie_name=cookie_name
        )

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.add_url_rule(self.login_path, "scalekit_login", self._login_view)
        app.add_url_rule(self.callback_path, "scalekit_callback", self._callback_view)
        app.add_url_rule(self.logout_path, "scalekit_logout", self._logout_view)

    @property
    def current_user(self) -> Optional[Dict[str, Any]]:
        return getattr(g, "scalekit_user", None)

    def _login_view(self):
        url = self.client.get_authorization_url(self.redirect_uri, AuthorizationUrlOptions())
        return flask_redirect(url)

    def _callback_view(self):
        code = flask_request.args.get("code")
        result = self.client.authenticate_with_code(
            code, self.redirect_uri, CodeAuthenticationOptions()
        )
        payload = {
            "user": result.get("user"),
            "access_token": result["access_token"],
            "refresh_token": result.get("refresh_token"),
            "expires_at": time.time() + (result.get("expires_in") or 300),
        }
        cookie_value = self.manager.create_session_cookie(payload)
        response = Response(status=302, headers={"Location": self.post_login_redirect})
        adapter = _FlaskResponseAdapter(response)
        adapter.set_cookie(self.manager.cookie_name, cookie_value)
        return response

    def _logout_view(self):
        response = Response(status=302, headers={"Location": self.post_login_redirect})
        _FlaskResponseAdapter(response).delete_cookie(self.manager.cookie_name)
        return response

    def requires_auth(self, view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            result = self.manager.check(_FlaskRequestAdapter())

            if not result.authenticated:
                response = Response(status=302, headers={"Location": self.login_path})
                if result.should_clear_cookie:
                    _FlaskResponseAdapter(response).delete_cookie(self.manager.cookie_name)
                return response

            g.scalekit_user = result.user
            response = Response(response=view_func(*args, **kwargs))
            self.manager.apply(result, _FlaskResponseAdapter(response))
            return response

        return wrapped

from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional
from urllib.parse import quote

try:
    from flask import Flask, Response, g, make_response
    from flask import redirect as flask_redirect
    from flask import request as flask_request
except ImportError as exc:  # pragma: no cover -- exercised only without the extra installed
    raise ImportError(
        "Flask integration requires the 'flask' extra: "
        "pip install scalekit-sdk-python[flask]"
    ) from exc

from scalekit.client import ScalekitClient
from scalekit.common.scalekit import (
    AuthorizationUrlOptions,
    CodeAuthenticationOptions,
    LogoutUrlOptions,
)
from scalekit.middleware.csrf_state import (
    RETURN_TO_COOKIE_NAME,
    STATE_COOKIE_MAX_AGE,
    STATE_COOKIE_NAME,
    generate_state,
    sanitize_return_to,
    verify_state,
)
from scalekit.middleware.protocol import RequestAdapter, ResponseAdapter
from scalekit.middleware.session_manager import DEFAULT_COOKIE_NAME, SessionRefreshManager

logger = logging.getLogger("scalekit.frameworks.flask")


class _FlaskRequestAdapter:
    """RequestAdapter implementation backed by Flask's request context."""

    def get_cookie(self, name: str) -> Optional[str]:
        return flask_request.cookies.get(name)

    def get_request_url(self) -> str:
        return flask_request.url


class _FlaskResponseAdapter:
    """ResponseAdapter implementation that mutates a Flask Response in place."""

    def __init__(self, response: Response, *, secure: bool = True):
        self.response = response
        # Default for callers that don't pass `secure` explicitly (e.g.
        # SessionRefreshManager.apply(), which only knows the ResponseAdapter
        # interface, not this app's cookie_secure setting) -- every
        # ScalekitAuth call site now constructs this with secure=self.cookie_secure.
        self._default_secure = secure

    def set_cookie(
        self,
        name: str,
        value: str,
        *,
        max_age: Optional[int] = None,
        secure: Optional[bool] = None,
        http_only: bool = True,
        same_site: str = "Lax",
        domain: Optional[str] = None,
        path: str = "/",
    ) -> None:
        self.response.set_cookie(
            name,
            value,
            max_age=max_age,
            secure=self._default_secure if secure is None else secure,
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
            # `current_user` is access-token claims, not a full id_token profile --
            # `sub` is always present; `email` only shows up if it's configured as
            # a custom access-token claim in the Scalekit dashboard.
            return f"Hello {auth.current_user['sub']}"
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
        cookie_secure: bool = True,
        login_path: str = "/login",
        callback_path: str = "/callback",
        logout_path: str = "/logout",
        post_login_redirect: str = "/",
        post_logout_redirect_uri: Optional[str] = None,
        full_logout: bool = True,
    ):
        if not redirect_uri:
            raise ValueError(
                "redirect_uri is required. Pass the exact Redirect URI registered "
                "for this app in the Scalekit dashboard (Authentication > Redirects), "
                "e.g. redirect_uri=\"https://yourapp.com/callback\"."
            )
        if client is None:
            client = ScalekitClient(env_url=env_url, client_id=client_id, client_secret=client_secret)
        self.client = client
        self.redirect_uri = redirect_uri
        # Right default for production. Chrome (and some other browsers) silently
        # drop a Secure cookie set over plain http://localhost, which looks like a
        # session that never sticks -- set cookie_secure=False for local HTTP dev.
        self.cookie_secure = cookie_secure
        self.login_path = login_path
        self.callback_path = callback_path
        self.logout_path = logout_path
        self.post_login_redirect = post_login_redirect
        # Must be separately allow-listed in the Scalekit dashboard (Authentication >
        # Redirects > Post Logout URL) -- it's a different allow-list than the
        # OAuth redirect_uri, so this is intentionally not just reused from
        # post_login_redirect even though it defaults to the same value.
        self.post_logout_redirect_uri = post_logout_redirect_uri or post_login_redirect
        # Default to full logout (end the Scalekit-side session too, via
        # id_token_hint) rather than local-only -- local-only silently leaves the
        # user's Scalekit session alive, so a subsequent /login silently
        # re-authenticates them with no visible login step at all, which is a
        # confusing default for most apps. Set full_logout=False to opt out.
        self.full_logout = full_logout

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

    def get_session(self) -> Optional[Dict[str, Any]]:
        """
        Read-only session lookup -- for use outside a `requires_auth`-wrapped
        view (e.g. a homepage that wants to show a logged-in/logged-out
        state without gating the whole route). Never refreshes or writes a
        new cookie -- only `requires_auth` does that.

        Returns `{"user": ..., "expires_at": ...}`, or `None` if there's no
        valid session. `user` is the access-token claims (not tokens
        themselves) -- this method never returns `access_token`,
        `refresh_token`, or `id_token`.
        """
        cookie_value = flask_request.cookies.get(self.manager.cookie_name)
        if not cookie_value:
            return None
        payload = self.manager.read_session(cookie_value)
        if payload is None:
            return None
        return {"user": payload.get("user"), "expires_at": payload.get("expires_at")}

    def _login_view(self):
        options = AuthorizationUrlOptions()
        # offline_access is required to get a refresh_token back at all -- without
        # it, Scalekit only issues an access_token and transparent refresh has
        # nothing to work with (confirmed: a normal FSA client does NOT get
        # offline_access added automatically -- that auto-add only applies to
        # MCP/agent clients on the backend).
        options.scopes = ["openid", "profile", "email", "offline_access"]

        # This view doubles as the dashboard-registered "Initiate Login URL":
        # Scalekit lands users here (not /callback) for a bookmarked/direct
        # login-page hit, an IdP portal tile, or an invite/magic link. If
        # there's an active session at that moment, Scalekit attaches an
        # idp_initiated_login JWT so the flow can jump straight to the
        # right connection/org instead of a generic login. relay_state is
        # intentionally not forwarded as our OAuth `state` -- we use our own
        # random value for CSRF cookie-binding instead (see below).
        idp_initiated_login = flask_request.args.get("idp_initiated_login")
        if idp_initiated_login:
            try:
                claims = self.client.get_idp_initiated_login_claims(idp_initiated_login)
                options.connection_id = claims.get("connection_id")
                options.organization_id = claims.get("organization_id")
                options.login_hint = claims.get("login_hint")
            except Exception:
                logger.exception(
                    "idp_initiated_login claim validation failed; falling back to normal login"
                )

        # Bind this authorization request to the browser that started it, so
        # /callback can reject a forged callback carrying an attacker's own
        # authorization code (CSRF).
        state = generate_state()
        options.state = state
        url = self.client.get_authorization_url(self.redirect_uri, options)
        response = Response(status=302, headers={"Location": url})
        adapter = _FlaskResponseAdapter(response, secure=self.cookie_secure)
        adapter.set_cookie(STATE_COOKIE_NAME, state, max_age=STATE_COOKIE_MAX_AGE)

        # Preserve the page the caller was trying to reach (set by
        # requires_auth's redirect below) so _callback_view can send them
        # back there instead of the fixed post_login_redirect -- re-validated
        # here since query strings are always attacker-influenceable, even if
        # requires_auth's own value was somehow bypassed by a direct
        # /login?returnTo= hit.
        return_to = sanitize_return_to(flask_request.args.get("returnTo"))
        if return_to:
            adapter.set_cookie(RETURN_TO_COOKIE_NAME, return_to, max_age=STATE_COOKIE_MAX_AGE)
        return response

    def _callback_view(self):
        def _redirect_to_login():
            resp = Response(status=302, headers={"Location": self.login_path})
            adapter = _FlaskResponseAdapter(resp, secure=self.cookie_secure)
            adapter.delete_cookie(STATE_COOKIE_NAME)
            adapter.delete_cookie(RETURN_TO_COOKIE_NAME)
            return resp

        # The provider redirects here with `error` (no `code`) if the user
        # cancels consent or the request is otherwise rejected -- never reflect
        # error/error_description into the response, it's attacker-influenced.
        error = flask_request.args.get("error")
        code = flask_request.args.get("code")
        if error or not code:
            return _redirect_to_login()

        stored_state = flask_request.cookies.get(STATE_COOKIE_NAME)
        returned_state = flask_request.args.get("state")
        if not verify_state(stored_state, returned_state):
            # Missing or mismatched state -- this callback did not originate
            # from a /login this browser actually made. Refuse the exchange.
            return _redirect_to_login()

        try:
            result = self.client.authenticate_with_code(
                code, self.redirect_uri, CodeAuthenticationOptions()
            )
            access_token = result["access_token"]
            # Access-token claims (not id_token claims) are the source of truth for
            # `user` -- customers can configure custom access-token claims in the
            # Scalekit dashboard, and this is also what stays fresh on every refresh
            # (see SessionRefreshManager._refresh). id_token is kept separately, only
            # for use as id_token_hint on logout.
            claims = self.client.validate_access_token_and_get_claims(access_token)
            payload = {
                "user": claims,
                "access_token": access_token,
                "refresh_token": result.get("refresh_token"),
                "id_token": result.get("id_token"),
                "expires_at": claims.get("exp", time.time() + (result.get("expires_in") or 300)),
            }
            # create_session_cookie raises if the encrypted payload exceeds the
            # browser cookie size limit (e.g. several custom access-token claims
            # configured) -- must stay inside this try, not just the network
            # calls above, or this view raises with no wrapper around it.
            cookie_value = self.manager.create_session_cookie(payload)
        except Exception:
            logger.exception("login callback failed; redirecting to login")
            return _redirect_to_login()

        return_to = sanitize_return_to(flask_request.cookies.get(RETURN_TO_COOKIE_NAME))
        response = Response(
            status=302, headers={"Location": return_to or self.post_login_redirect}
        )
        adapter = _FlaskResponseAdapter(response, secure=self.cookie_secure)
        adapter.set_cookie(self.manager.cookie_name, cookie_value)
        adapter.delete_cookie(STATE_COOKIE_NAME)
        adapter.delete_cookie(RETURN_TO_COOKIE_NAME)
        return response

    def _logout_view(self):
        cookie_value = flask_request.cookies.get(self.manager.cookie_name)
        id_token = None
        if cookie_value:
            payload = self.manager.read_session(cookie_value)
            if payload:
                id_token = payload.get("id_token")

        redirect_url = self.post_logout_redirect_uri
        if self.full_logout and id_token:
            # Scalekit requires an absolute, dashboard-registered post-logout
            # redirect URI (a relative path like "/" is rejected as
            # invalid_request) -- absolutize it against the current request's
            # host so a developer can still just pass a simple path.
            absolute_redirect_uri = self.post_logout_redirect_uri
            if not absolute_redirect_uri.startswith(("http://", "https://")):
                absolute_redirect_uri = flask_request.host_url.rstrip("/") + absolute_redirect_uri
            options = LogoutUrlOptions()
            options.id_token_hint = id_token
            options.post_logout_redirect_uri = absolute_redirect_uri
            # A real top-level redirect to Scalekit's own domain is required here --
            # same reason a background fetch/XHR can't do this: Scalekit needs the
            # request to actually carry its own session cookie to end that session.
            redirect_url = self.client.get_logout_url(options)

        response = Response(status=302, headers={"Location": redirect_url})
        _FlaskResponseAdapter(response).delete_cookie(self.manager.cookie_name)
        return response

    def requires_auth(self, view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            result = self.manager.check(_FlaskRequestAdapter())

            if not result.authenticated:
                # Send the caller back to where they were trying to go once
                # login completes, instead of always landing on
                # post_login_redirect -- full_path includes the query string
                # (e.g. "/account?tab=billing"), matching what sanitize_return_to
                # validates on the receiving end (_login_view/_callback_view).
                current_path = flask_request.full_path.rstrip("?")
                location = f"{self.login_path}?returnTo={quote(current_path, safe='')}"
                response = Response(status=302, headers={"Location": location})
                if result.should_clear_cookie:
                    _FlaskResponseAdapter(response).delete_cookie(self.manager.cookie_name)
                return response

            g.scalekit_user = result.user
            # make_response applies Flask's normal view-return handling (dict ->
            # JSON, (body, status) tuples, an existing Response passed through
            # unchanged, ...) -- a bare Response(response=...) bypasses all of
            # that and silently mangles anything but a plain string return.
            response = make_response(view_func(*args, **kwargs))
            self.manager.apply(result, _FlaskResponseAdapter(response, secure=self.cookie_secure))
            return response

        return wrapped

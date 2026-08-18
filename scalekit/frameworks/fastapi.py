from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional
from urllib.parse import quote

try:
    from fastapi import APIRouter, FastAPI, Request, Response
    from fastapi.responses import RedirectResponse
    from starlette.concurrency import run_in_threadpool
except ImportError as exc:  # pragma: no cover -- exercised only without the extra installed
    raise ImportError(
        "FastAPI integration requires the 'fastapi' extra: "
        "pip install scalekit-sdk-python[fastapi]"
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

logger = logging.getLogger("scalekit.frameworks.fastapi")


class _FastAPIRequestAdapter:
    """RequestAdapter implementation backed by a Starlette/FastAPI Request."""

    def __init__(self, request: Request):
        self._request = request

    def get_cookie(self, name: str) -> Optional[str]:
        return self._request.cookies.get(name)

    def get_request_url(self) -> str:
        return str(self._request.url)


class _FastAPIResponseAdapter:
    """ResponseAdapter implementation that mutates a Starlette/FastAPI Response in place."""

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
        same_site: str = "lax",
        domain: Optional[str] = None,
        path: str = "/",
    ) -> None:
        self.response.set_cookie(
            key=name,
            value=value,
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
        self.response.delete_cookie(key=name, path=path, domain=domain)


class _RequiresLoginRedirect(Exception):
    """
    Internal signal raised by `requires_auth` when there's no valid session.

    FastAPI dependencies can't directly return an alternate Response the way a
    Flask decorator can wrap a whole view -- raising this and handling it via
    an app-level exception handler (registered by `ScalekitAuth.install`) is
    what lets "no valid session" produce a real 302 redirect instead of the
    JSON 401 a raised HTTPException would otherwise produce. That JSON-401
    default is exactly the failure mode a background fetch/XHR would silently
    swallow -- the property this whole design exists to avoid.
    """

    def __init__(
        self,
        location: str,
        clear_cookie: bool,
        cookie_name: str,
        *,
        return_to: Optional[str] = None,
    ):
        self.location = location
        self.clear_cookie = clear_cookie
        self.cookie_name = cookie_name
        self.return_to = return_to


class ScalekitAuth:
    """
    FastAPI integration wiring Scalekit Full Stack Auth with the same secure
    defaults as the Flask extension: encrypted session cookie, transparent
    token refresh, full logout via id_token_hint. Protect routes with the
    `requires_auth` dependency -- FastAPI's idiomatic protection mechanism is
    `Depends()`, not a decorator:

        auth = ScalekitAuth(
            client_id=..., client_secret=..., env_url=...,
            redirect_uri="https://myapp.com/callback",
            cookie_encryption_secret=...,
        )
        auth.install(app)

        @app.get("/account")
        async def account(user: dict = Depends(auth.requires_auth)):
            # `user` is access-token claims, not a full id_token profile -- `sub`
            # is always present; `email` only shows up if it's configured as a
            # custom access-token claim in the Scalekit dashboard.
            return {"sub": user["sub"]}

    Note: `requires_auth` sets the refreshed session cookie on the injected
    `response` parameter. If a protected endpoint returns a `Response`
    instance directly instead of a plain value, FastAPI uses that returned
    response instead of the injected one, and the refreshed cookie is
    discarded. If you need to return a `Response` directly from a protected
    endpoint, copy `response.raw_headers` (or re-apply the cookie) onto the
    response you return.
    """

    def __init__(
        self,
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
        self.post_logout_redirect_uri = post_logout_redirect_uri or post_login_redirect
        self.full_logout = full_logout

        # Raises immediately if cookie_encryption_secret is missing -- see
        # SessionRefreshManager and scalekit.middleware.session_crypto for why
        # there is intentionally no default.
        self.manager = SessionRefreshManager(
            self.client, cookie_encryption_secret, cookie_name=cookie_name
        )

        self.router = APIRouter()
        self.router.add_api_route(self.login_path, self._login_view, methods=["GET"])
        self.router.add_api_route(self.callback_path, self._callback_view, methods=["GET"])
        self.router.add_api_route(self.logout_path, self._logout_view, methods=["GET"])

    def install(self, app: FastAPI) -> None:
        """Register the login/callback/logout routes and the redirect exception handler."""
        app.include_router(self.router)
        app.add_exception_handler(_RequiresLoginRedirect, self._redirect_exception_handler)

    async def _redirect_exception_handler(self, request: Request, exc: _RequiresLoginRedirect):
        location = exc.location
        if exc.return_to:
            location = f"{location}?returnTo={quote(exc.return_to, safe='')}"
        response = RedirectResponse(location, status_code=302)
        if exc.clear_cookie:
            _FastAPIResponseAdapter(response, secure=self.cookie_secure).delete_cookie(exc.cookie_name)
        return response

    def get_session(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Read-only session lookup -- for use outside a `requires_auth`-gated
        endpoint (e.g. a homepage that wants to show a logged-in/logged-out
        state without gating the whole route). Never refreshes or writes a
        new cookie -- only `requires_auth` does that.

        Returns `{"user": ..., "expires_at": ...}`, or `None` if there's no
        valid session. `user` is the access-token claims (not tokens
        themselves) -- this method never returns `access_token`,
        `refresh_token`, or `id_token`.
        """
        cookie_value = request.cookies.get(self.manager.cookie_name)
        if not cookie_value:
            return None
        payload = self.manager.read_session(cookie_value)
        if payload is None:
            return None
        return {"user": payload.get("user"), "expires_at": payload.get("expires_at")}

    async def _login_view(self, request: Request):
        options = AuthorizationUrlOptions()
        # offline_access is required to get a refresh_token back at all -- see
        # scalekit.frameworks.flask for the full explanation (same reasoning
        # applies here; the backend behavior isn't framework-specific).
        options.scopes = ["openid", "profile", "email", "offline_access"]

        # This view doubles as the dashboard-registered "Initiate Login URL"
        # -- see scalekit.frameworks.flask for the full reasoning.
        idp_initiated_login = request.query_params.get("idp_initiated_login")
        if idp_initiated_login:
            try:
                claims = await run_in_threadpool(
                    self.client.get_idp_initiated_login_claims, idp_initiated_login
                )
                options.connection_id = claims.get("connection_id")
                options.organization_id = claims.get("organization_id")
                options.login_hint = claims.get("login_hint")
            except Exception:
                logger.exception(
                    "idp_initiated_login claim validation failed; falling back to normal login"
                )

        # Bind this authorization request to the browser that started it, so
        # /callback can reject a forged callback carrying an attacker's own
        # authorization code (CSRF) -- see scalekit.frameworks.flask.
        state = generate_state()
        options.state = state
        url = await run_in_threadpool(self.client.get_authorization_url, self.redirect_uri, options)
        response = RedirectResponse(url, status_code=302)
        adapter = _FastAPIResponseAdapter(response, secure=self.cookie_secure)
        adapter.set_cookie(STATE_COOKIE_NAME, state, max_age=STATE_COOKIE_MAX_AGE)

        # Preserve the page the caller was trying to reach (set by
        # requires_auth's redirect) so _callback_view can send them back there
        # instead of the fixed post_login_redirect -- re-validated here since
        # query strings are always attacker-influenceable.
        return_to = sanitize_return_to(request.query_params.get("returnTo"))
        if return_to:
            adapter.set_cookie(RETURN_TO_COOKIE_NAME, return_to, max_age=STATE_COOKIE_MAX_AGE)
        return response

    async def _callback_view(self, request: Request):
        def _redirect_to_login():
            resp = RedirectResponse(self.login_path, status_code=302)
            adapter = _FastAPIResponseAdapter(resp, secure=self.cookie_secure)
            adapter.delete_cookie(STATE_COOKIE_NAME)
            adapter.delete_cookie(RETURN_TO_COOKIE_NAME)
            return resp

        # The provider redirects here with `error` (no `code`) if the user
        # cancels consent or the request is otherwise rejected -- never reflect
        # error/error_description into the response, it's attacker-influenced.
        error = request.query_params.get("error")
        code = request.query_params.get("code")
        if error or not code:
            return _redirect_to_login()

        stored_state = request.cookies.get(STATE_COOKIE_NAME)
        returned_state = request.query_params.get("state")
        if not verify_state(stored_state, returned_state):
            # Missing or mismatched state -- this callback did not originate
            # from a /login this browser actually made. Refuse the exchange.
            return _redirect_to_login()

        try:
            result = await run_in_threadpool(
                self.client.authenticate_with_code, code, self.redirect_uri, CodeAuthenticationOptions()
            )
            access_token = result["access_token"]
            # Access-token claims (not id_token claims) are the source of truth for
            # `user` -- see scalekit.frameworks.flask for the full reasoning.
            claims = await run_in_threadpool(
                self.client.validate_access_token_and_get_claims, access_token
            )
            payload = {
                "user": claims,
                "access_token": access_token,
                "refresh_token": result.get("refresh_token"),
                "id_token": result.get("id_token"),
                "expires_at": claims.get("exp", time.time() + (result.get("expires_in") or 300)),
            }
            # create_session_cookie raises if the encrypted payload exceeds the
            # browser cookie size limit -- must stay inside this try, not just
            # the network calls above, or this view raises with no wrapper.
            cookie_value = self.manager.create_session_cookie(payload)
        except Exception:
            logger.exception("login callback failed; redirecting to login")
            return _redirect_to_login()

        return_to = sanitize_return_to(request.cookies.get(RETURN_TO_COOKIE_NAME))
        response = RedirectResponse(return_to or self.post_login_redirect, status_code=302)
        adapter = _FastAPIResponseAdapter(response, secure=self.cookie_secure)
        adapter.set_cookie(self.manager.cookie_name, cookie_value)
        adapter.delete_cookie(STATE_COOKIE_NAME)
        adapter.delete_cookie(RETURN_TO_COOKIE_NAME)
        return response

    async def _logout_view(self, request: Request):
        cookie_value = request.cookies.get(self.manager.cookie_name)
        id_token = None
        if cookie_value:
            payload = self.manager.read_session(cookie_value)
            if payload:
                id_token = payload.get("id_token")

        redirect_url = self.post_logout_redirect_uri
        if self.full_logout and id_token:
            # Scalekit requires an absolute, dashboard-registered post-logout
            # redirect URI -- absolutize a relative default against the
            # current request's host, same as the Flask adapter.
            absolute_redirect_uri = self.post_logout_redirect_uri
            if not absolute_redirect_uri.startswith(("http://", "https://")):
                absolute_redirect_uri = str(request.base_url).rstrip("/") + absolute_redirect_uri
            options = LogoutUrlOptions()
            options.id_token_hint = id_token
            options.post_logout_redirect_uri = absolute_redirect_uri
            redirect_url = await run_in_threadpool(self.client.get_logout_url, options)

        response = RedirectResponse(redirect_url, status_code=302)
        _FastAPIResponseAdapter(response).delete_cookie(self.manager.cookie_name)
        return response

    async def requires_auth(self, request: Request, response: Response) -> Optional[Dict[str, Any]]:
        """
        FastAPI dependency: `user: dict = Depends(auth.requires_auth)`.

        Session check/refresh runs in a thread pool since the underlying
        client calls are blocking network I/O -- this avoids stalling the
        event loop on every protected request.
        """
        result = await run_in_threadpool(self.manager.check, _FastAPIRequestAdapter(request))

        if not result.authenticated:
            # request.url.path + query preserves the page the caller was
            # trying to reach so _login_view/_callback_view can send them
            # back there instead of always landing on post_login_redirect.
            current_path = request.url.path
            if request.url.query:
                current_path = f"{current_path}?{request.url.query}"
            raise _RequiresLoginRedirect(
                location=self.login_path,
                clear_cookie=result.should_clear_cookie,
                cookie_name=self.manager.cookie_name,
                return_to=current_path,
            )

        if result.new_cookie_value:
            _FastAPIResponseAdapter(response, secure=self.cookie_secure).set_cookie(
                self.manager.cookie_name, result.new_cookie_value
            )

        return result.user

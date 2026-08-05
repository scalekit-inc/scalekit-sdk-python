from __future__ import annotations

from typing import Optional, Protocol, runtime_checkable


@runtime_checkable
class RequestAdapter(Protocol):
    """
    Framework-agnostic view of an incoming HTTP request.

    Framework integrations (Flask, FastAPI, Django, ...) implement this protocol
    so the core session/refresh logic (`scalekit.middleware.session_manager`)
    never imports a specific web framework.
    """

    def get_cookie(self, name: str) -> Optional[str]:
        """Return the named cookie's value, or None if not present."""
        ...

    def get_request_url(self) -> str:
        """Return the full URL of the current request."""
        ...


@runtime_checkable
class ResponseAdapter(Protocol):
    """
    Framework-agnostic view of an outgoing HTTP response.

    Cookie attributes are set here, not left to the developer -- callers of
    `set_cookie` always get `HttpOnly`, `Secure`, and `SameSite` applied by the
    adapter implementation, using the defaults documented on each parameter.
    """

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
        ...

    def delete_cookie(
        self,
        name: str,
        *,
        path: str = "/",
        domain: Optional[str] = None,
    ) -> None:
        ...

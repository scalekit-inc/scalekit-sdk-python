"""Keep ``ActionClient.request`` and its credentials inside the Scalekit HTTP proxy.

``ActionClient.request`` sends every call to ``{env_url}/proxy{path}`` with the
client's bearer token and the connection headers. This module

* verifies, before anything is sent, that the server will route the path under
  ``<env base path>/proxy/`` (``ensure_under_proxy_prefix``), and
* removes those credentials from any redirect hop whose target is outside that
  prefix (``ProxySession``), while following redirects exactly as ``requests``
  does.

It never rewrites a URL: a request that passes is sent exactly as built.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import cast
from urllib.parse import unquote

import requests

_PROXY_PREFIX = "/proxy/"

_VALID_ESCAPE_RE = re.compile(r"%[0-9A-Fa-f]{2}")

# Headers request() adds that identify the caller to Scalekit. Header names are
# case-insensitive in requests, so "Connection_name" is covered too.
_CREDENTIAL_HEADERS = ("Authorization", "connection_name", "identifier")

# Typed handles on two requests.Session methods. Some stub distributions
# (types-requests) declare them without annotations; calling them through these
# keeps strict type checking without suppressions.
_session_rebuild_auth = cast(
    "Callable[[requests.Session, requests.PreparedRequest, requests.Response], None]",
    requests.Session.rebuild_auth,
)
_session_should_strip_auth = cast(
    "Callable[[requests.Session, str, str], bool]",
    requests.Session.should_strip_auth,
)

_OUTSIDE_PROXY_MESSAGE = (
    "path must resolve under the proxy prefix: start it with '/' and do not let '..' "
    "segments (including percent-encoded or backslash forms) climb above it"
)


def ensure_under_proxy_prefix(env_url: str, url: str) -> None:
    r"""Raise ``ValueError`` if the server would route ``url`` outside ``<base>/proxy/``.

    The check starts from the path ``requests`` actually sends for ``url``
    (``requests`` and ``urllib3`` may already have removed dot segments or
    decoded ``%2e``). That path is percent-decoded once and cleaned as Go
    routers clean it (``clean_path``): runs of ``/`` collapse and dot
    segments are resolved. This is done twice, as is and with ``\`` treated as
    ``/``, and each result must equal ``<base>/proxy`` or start with
    ``<base>/proxy/``. ``<base>`` is the path of ``env_url``, usually empty.

    Args:
        env_url: The environment URL the client was configured with, for
            example ``"https://acme.scalekit.cloud"`` or
            ``"https://host/base"``.
        url: The full URL ``request()`` is about to send, built as
            ``env_url.rstrip("/") + "/proxy" + path``.

    Raises:
        ValueError: If either server view falls outside the proxy prefix. The
            message does not include the path.

    Example:
        >>> ensure_under_proxy_prefix("https://h", "https://h/proxy/gmail/v1/users/me")
        >>> ensure_under_proxy_prefix("https://h", "https://h/proxy/x/../../outside")
        Traceback (most recent call last):
        ...
        ValueError: path must resolve under the proxy prefix: ...
    """
    if not _path_is_under_prefix(env_url, _wire_path(url)):
        raise ValueError(_OUTSIDE_PROXY_MESSAGE)


class ProxySession(requests.Session):
    """A ``requests.Session`` that keeps proxy credentials inside the proxy prefix.

    Redirects are followed exactly as ``requests`` follows them. On each hop,
    ``requests`` calls ``rebuild_auth``; before deferring to it, this removes
    ``Authorization``, ``connection_name`` and ``identifier`` when the hop's
    target is outside ``<env base path>/proxy/``: a different origin (as
    ``requests.Session.should_strip_auth`` decides) or the same origin with a
    path the server would route outside the prefix (the rule
    ``ensure_under_proxy_prefix`` applies). Once removed, they stay
    removed for later hops. Hops that stay under the prefix are untouched.

    Example:
        >>> with ProxySession("https://acme.scalekit.cloud") as session:
        ...     response = session.request("GET", "https://acme.scalekit.cloud/proxy/x")
    """

    def __init__(self, env_url: str) -> None:
        """Create a session for proxy calls to ``env_url``."""
        super().__init__()
        self._env_url = env_url
        self._prefix_url = env_url.rstrip("/") + _PROXY_PREFIX

    def rebuild_auth(
        self, prepared_request: requests.PreparedRequest, response: requests.Response
    ) -> None:
        """Drop proxy credentials when a redirect leaves the proxy prefix, then defer."""
        if not self._stays_in_proxy(prepared_request):
            for name in _CREDENTIAL_HEADERS:
                prepared_request.headers.pop(name, None)
        _session_rebuild_auth(self, prepared_request, response)

    def _stays_in_proxy(self, prepared_request: requests.PreparedRequest) -> bool:
        url = prepared_request.url
        if not url or _session_should_strip_auth(self, self._prefix_url, url):
            return False
        # requests sets a hop's URL directly, without urllib3's URL parser, so
        # urllib3 still re-encodes its path when sending.
        sent = _as_sent(prepared_request.path_url.split("?", 1)[0])
        return _path_is_under_prefix(self._env_url, sent)


def _path_is_under_prefix(env_url: str, sent: str) -> bool:
    """Return whether the server will route ``sent`` under ``<base>/proxy/``.

    ``sent`` is the path as ``requests`` puts it on the wire, so any
    normalisation ``requests``/``urllib3`` applied is already included. Each of
    its server views (``_server_views``) must equal ``<base>/proxy`` or start
    with ``<base>/proxy/``. Equality admits inputs that leave the prefix and
    come back to exactly ``<base>/proxy`` (``/..%2fproxy``): they were sent the
    same way before this check existed, and no proxy route matches them.
    Sibling paths such as ``<base>/proxyx`` are rejected.
    """
    prefix = _wire_path(env_url.rstrip("/") + _PROXY_PREFIX)
    for prefix_view, cleaned in zip(_server_views(prefix), _server_views(sent), strict=True):
        bare = prefix_view.rstrip("/")
        if cleaned != bare and not cleaned.startswith(bare + "/"):
            return False
    return True


def _wire_path(url: str) -> str:
    """Return the path (without the query) that ``requests`` sends for ``url``.

    Preparing the URL runs it through ``urllib3``'s URL parser, which already
    applies the encoding ``_as_sent`` describes, so this is the wire form.
    """
    path_url: str = requests.Request(method="GET", url=url).prepare().path_url
    return path_url.split("?", 1)[0]


def _as_sent(path: str) -> str:
    """Return a redirect hop's ``path`` as ``urllib3`` writes it in the request line.

    When any ``%`` in the path does not start a valid ``%XX`` escape, ``urllib3``
    encodes every ``%`` as ``%25``, so the server decodes ``%2F`` back to the
    literal text ``%2F``, not to ``/``. ``urllib3`` escapes other characters as
    well, but one decode restores those, so they do not change the server view.
    """
    if path.count("%") != len(_VALID_ESCAPE_RE.findall(path)):
        return path.replace("%", "%25")
    return path


def _server_views(path: str) -> tuple[str, str]:
    r"""Return how a server may route ``path``: decoded once, then cleaned.

    The first view is what a Go router sees (``clean_path`` of the decoded
    path). The second also treats ``\`` as ``/``, as some servers and proxies
    do. Both are checked: neither view alone is stricter than the other.
    """
    decoded = unquote(path)
    return clean_path(decoded), clean_path(decoded.replace("\\", "/"))


def clean_path(path: str) -> str:
    """Return ``path`` cleaned the way Go HTTP routers clean a request path.

    This is Go's ``path.Clean`` on the rooted path, with a trailing slash put
    back when ``path`` had one, which is how common Go routers clean the decoded
    path before matching routes (and redirect to the cleaned path when it
    differs). Empty and ``.`` segments are dropped, so runs of ``/`` collapse;
    each ``..`` removes the segment before it, and a ``..`` at the root is
    dropped.

    Args:
        path: A decoded URL path. A missing leading ``/`` is treated as present.

    Returns:
        The cleaned path, always starting with ``/``.

    Example:
        >>> clean_path("/proxy//../x/./y/")
        '/x/y/'
    """
    segments: list[str] = []
    for segment in path.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if segments:
                segments.pop()
            continue
        segments.append(segment)
    cleaned = "/" + "/".join(segments)
    if path.endswith("/") and cleaned != "/":
        cleaned += "/"
    return cleaned

"""Keep ``ActionClient.request`` and its credentials inside the Scalekit HTTP proxy.

``ActionClient.request`` sends every call to ``{env_url}/proxy{path}`` with the
client's bearer token and the connection headers. This module

* verifies, before anything is sent, that the path the server will act on stays
  under ``<env base path>/proxy/`` (``ensure_under_proxy_prefix``), and
* removes those credentials from any redirect hop whose target is outside that
  prefix (``ProxySession``), while following redirects exactly as ``requests``
  does.

It never rewrites a URL: a request that passes is sent exactly as built.
"""

from __future__ import annotations

from urllib.parse import unquote

import requests

_PROXY_PREFIX = "/proxy/"

# Headers request() adds that identify the caller to Scalekit. Header names are
# case-insensitive in requests, so "Connection_name" is covered too.
_CREDENTIAL_HEADERS = ("Authorization", "connection_name", "identifier")

_OUTSIDE_PROXY_MESSAGE = (
    "path must start with '/' and resolve under the proxy prefix; "
    "'..' segments (including percent-encoded or backslash forms) must not climb above it"
)


def ensure_under_proxy_prefix(env_url: str, url: str) -> None:
    r"""Raise ``ValueError`` if ``url`` resolves outside ``<env base path>/proxy/``.

    Two views of the path are checked, and both must start with the prefix:

    1. The path ``requests`` will put on the wire. ``requests`` already removes
       literal dot segments and decodes some escapes (``%2e``) while preparing a
       URL, so this is computed by preparing the URL the same way.
    2. The path a server is likely to act on: the wire path percent-decoded
       once, with ``\`` treated as ``/``, and dot segments removed per
       RFC 3986 section 5.2.4.

    Args:
        env_url: The environment URL the client was configured with, for
            example ``"https://acme.scalekit.cloud"`` or
            ``"https://host/base"``.
        url: The full URL ``request()`` is about to send, built as
            ``env_url.rstrip("/") + "/proxy" + path``.

    Raises:
        ValueError: If either view of the path falls outside the proxy prefix.
            ``<base>/proxy`` without a trailing slash also counts as outside.
            The message does not include the path.

    Example:
        >>> ensure_under_proxy_prefix("https://h", "https://h/proxy/gmail/v1/users/me")
        >>> ensure_under_proxy_prefix("https://h", "https://h/proxy/x/../../api")
        Traceback (most recent call last):
        ...
        ValueError: path must start with '/' and resolve under the proxy prefix; ...
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
    path that fails ``ensure_under_proxy_prefix``. Once removed, they stay
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
        super().rebuild_auth(prepared_request, response)

    def _stays_in_proxy(self, prepared_request: requests.PreparedRequest) -> bool:
        url = prepared_request.url
        if not url or self.should_strip_auth(self._prefix_url, url):
            return False
        # The hop's URL was resolved by requests and is sent as-is (path_url).
        sent = prepared_request.path_url.split("?", 1)[0]
        return _path_is_under_prefix(self._env_url, sent)


def _path_is_under_prefix(env_url: str, sent: str) -> bool:
    """Return whether both views of the sent path start with ``<base>/proxy/``."""
    prefix = _wire_path(env_url.rstrip("/") + _PROXY_PREFIX)
    return sent.startswith(prefix) and _server_view(sent).startswith(_server_view(prefix))


def _wire_path(url: str) -> str:
    """Return the path (without the query) that ``requests`` sends for ``url``."""
    path_url: str = requests.Request(method="GET", url=url).prepare().path_url
    return path_url.split("?", 1)[0]


def _server_view(path: str) -> str:
    r"""Decode ``path`` once, treat ``\`` as ``/`` and remove dot segments."""
    return remove_dot_segments(unquote(path).replace("\\", "/"))


def remove_dot_segments(path: str) -> str:
    """Remove ``.`` and ``..`` segments from ``path`` per RFC 3986 section 5.2.4.

    Args:
        path: A URI path. It is not decoded here.

    Returns:
        The path with dot segments removed. A ``..`` above the root is dropped,
        and a trailing ``.`` or ``..`` leaves a trailing ``/``.

    Example:
        >>> remove_dot_segments("/a/b/c/./../../g")
        '/a/g'
    """
    output: list[str] = []
    rest = path
    while rest:
        if rest.startswith("../"):
            rest = rest[3:]
        elif rest.startswith(("./", "/./")):
            # "./" is dropped (rule A); "/./" becomes "/" (rule B).
            rest = rest[2:]
        elif rest == "/.":
            rest = "/"
        elif rest.startswith("/../"):
            rest = rest[3:]
            if output:
                output.pop()
        elif rest == "/..":
            rest = "/"
            if output:
                output.pop()
        elif rest in (".", ".."):
            rest = ""
        else:
            end = rest.find("/", 1)
            if end == -1:
                end = len(rest)
            output.append(rest[:end])
            rest = rest[end:]
    return "".join(output)

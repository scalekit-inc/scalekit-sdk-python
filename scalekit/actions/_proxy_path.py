"""Containment check for URLs sent through the Scalekit HTTP proxy.

``ActionClient.request`` sends every call to ``{env_url}/proxy{path}`` with the
client's bearer token. This module verifies, before anything is sent, that the
path the server will act on stays under ``<env base path>/proxy/``. It never
rewrites the URL: a path that passes is sent exactly as the caller built it.
"""

from __future__ import annotations

from urllib.parse import unquote

import requests

_PROXY_PREFIX = "/proxy/"

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
    prefix = _wire_path(env_url.rstrip("/") + _PROXY_PREFIX)
    sent = _wire_path(url)
    if not sent.startswith(prefix) or not _server_view(sent).startswith(_server_view(prefix)):
        raise ValueError(_OUTSIDE_PROXY_MESSAGE)


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

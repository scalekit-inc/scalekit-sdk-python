"""Keep ``ActionClient.request`` and its credentials inside the Scalekit HTTP proxy.

``ActionClient.request`` sends every call to ``{env_url}/proxy{path}`` with the
client's bearer token and the connection headers. This module

* builds the headers that name the connected account
  (``proxy_account_headers``),
* verifies, before anything is sent, that the server will route the path under
  ``<env base path>/proxy/`` (``ensure_under_proxy_prefix``), and
* removes those credentials from any redirect hop whose target is outside that
  prefix (``ProxySession``), while following redirects exactly as ``requests``
  does.

It never rewrites a URL: a request that passes is sent exactly as built.
"""

from __future__ import annotations

import contextlib
import re
from collections.abc import Callable, Mapping
from typing import cast
from urllib.parse import unquote

import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import LocationParseError
from urllib3.util import parse_url

_PROXY_PREFIX = "/proxy/"

_VALID_ESCAPE_RE = re.compile(r"%[0-9A-Fa-f]{2}")

# The headers that name the connected account, as (original name, X-Scalekit
# name) pairs. Both names of a pair carry the same value. The X-Scalekit names
# have no underscore, so they survive proxies and load balancers that drop
# headers containing one (ingress-nginx does by default).
_CONNECTION_NAME_HEADERS = ("connection_name", "X-Scalekit-Connection-Name")
_IDENTIFIER_HEADERS = ("identifier", "X-Scalekit-Identifier")
_ACCOUNT_HEADER_KEYS = frozenset(
    name.lower() for name in (*_CONNECTION_NAME_HEADERS, *_IDENTIFIER_HEADERS)
)

# Headers request() adds that identify the caller to Scalekit. Header names are
# case-insensitive in requests, so "Connection_name" is covered too.
_CREDENTIAL_HEADERS = ("Authorization", *_CONNECTION_NAME_HEADERS, *_IDENTIFIER_HEADERS)

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
# Only asked for request-targets (request_url); it never sends anything.
_URL_ADAPTER = HTTPAdapter()

# A proxy for every URL: request_url uses only whether one applies and its scheme.
_ANY_FORWARD_PROXY = {"all": "http://forward-proxy.invalid"}

_OUTSIDE_PROXY_MESSAGE = (
    "path must resolve under the proxy prefix: start it with '/' and do not let '..' "
    "segments (including percent-encoded or backslash forms) climb above it"
)


def proxy_account_headers(
    connection_name: str,
    identifier: str,
    headers: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Return the headers of a proxy request: the connected account plus ``headers``.

    The connection name is sent as ``connection_name`` (also written
    ``Connection_name``) and ``X-Scalekit-Connection-Name``; the identifier as
    ``identifier`` and ``X-Scalekit-Identifier``. The two names of a pair always
    carry the same value: the server rejects a request where they differ.

    ``headers`` are the caller's extra headers. Names are matched without
    regard to case, as HTTP and ``requests`` match them. For each pair:

    * A caller header with the original name (``identifier``, ``Identifier``,
      ...) overrides the argument, as it always has, even when blank. If it
      appears in several casings, the last one wins, as ``requests`` sends it.
    * A caller header with the ``X-Scalekit-*`` name sets the value when the
      original name is not given. A blank one (empty or whitespace) is
      ignored, as the server ignores it.
    * Both given with different non-blank values (compared with surrounding
      whitespace removed, as the server compares them) raise ``ValueError``.
      When they agree, the original-name value is sent under both names.

    The caller's keys for these names are replaced by the names above, so no
    two keys that differ only in case carry different values. Every other
    caller header, ``X-Identifier`` included, is passed through unchanged.

    Args:
        connection_name: The connection name passed to the SDK method.
        identifier: The connected account identifier passed to the SDK method.
        headers: The caller's extra headers, or ``None``. Anything
            ``dict.update`` accepts, as before.

    Returns:
        A new dict: the account headers followed by the caller's other headers.

    Raises:
        ValueError: The caller passed different values for the two names of a
            pair. The message names the headers, never their values.

    Example:
        >>> h = proxy_account_headers("gmail", "user_1", {"Identifier": "user_2"})
        >>> h["identifier"], h["X-Scalekit-Identifier"]
        ('user_2', 'user_2')
    """
    extra: dict[str, str] = {}
    if headers:
        extra.update(headers)
    connection_value = _account_value(connection_name, extra, _CONNECTION_NAME_HEADERS)
    identifier_value = _account_value(identifier, extra, _IDENTIFIER_HEADERS)
    result = {
        "connection_name": connection_value,
        "Connection_name": connection_value,
        "X-Scalekit-Connection-Name": connection_value,
        "identifier": identifier_value,
        "X-Scalekit-Identifier": identifier_value,
    }
    result.update(
        (name, value) for name, value in extra.items() if _key(name) not in _ACCOUNT_HEADER_KEYS
    )
    return result


def _account_value(argument: str, headers: Mapping[str, str], names: tuple[str, str]) -> str:
    """Return the value to send under both ``names`` (rules: ``proxy_account_headers``)."""
    original_name, scalekit_name = names
    original = _last_value(headers, original_name)
    scalekit = _last_value(headers, scalekit_name)
    if scalekit is not None and not _trimmed(scalekit):
        scalekit = None
    if original is not None and _trimmed(original):
        if scalekit is not None and _trimmed(scalekit) != _trimmed(original):
            raise ValueError(
                f"headers {original_name!r} and {scalekit_name!r} have different values; "
                "pass only one of them, or the same value for both"
            )
        return original
    if scalekit is not None:
        return scalekit
    if original is not None:
        return original
    return argument


def _last_value(headers: Mapping[str, str], name: str) -> str | None:
    """Return the value of the last key in ``headers`` equal to ``name`` in any case."""
    wanted = name.lower()
    found: str | None = None
    for key, value in headers.items():
        if _key(key) == wanted:
            found = value
    return found


def _key(name: object) -> object:
    """Return a header name for case-insensitive comparison."""
    return name.lower() if isinstance(name, str) else name


def _trimmed(value: object) -> str:
    """Return a header value without surrounding whitespace, for comparison only.

    ``requests`` sends ``str`` values as Latin-1 and also accepts ``bytes``, so
    both compare equal here when they would go on the wire the same way. Any
    other type is compared as text; ``requests`` rejects it when sending.
    """
    if isinstance(value, bytes):
        return value.decode("latin-1").strip()
    return str(value).strip()


def ensure_under_proxy_prefix(env_url: str, url: str) -> None:
    r"""Raise ``ValueError`` if the server would route ``url`` outside ``<base>/proxy/``.

    The check starts from the path ``requests`` actually sends for ``url``
    (``requests`` and ``urllib3`` may already have removed dot segments or
    decoded ``%2e``). For a URL that is not ``https``, a forward proxy may be
    used: ``requests`` then hands ``urllib3`` the absolute URL, and both
    rebuild it (dropping an empty ``;`` parameter, removing dot segments
    again), so that path is checked as well.
    Each path is percent-decoded once and cleaned as Go
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
        ValueError: If any server view falls outside the proxy prefix. The
            message does not include the path.

    Example:
        >>> ensure_under_proxy_prefix("https://h", "https://h/proxy/gmail/v1/users/me")
        >>> ensure_under_proxy_prefix("https://h", "https://h/proxy/x/../../outside")
        Traceback (most recent call last):
        ...
        ValueError: path must resolve under the proxy prefix: ...
    """
    prepared = requests.Request(method="GET", url=url).prepare()
    if not all(_path_is_under_prefix(env_url, sent) for sent in _sent_paths(prepared)):
        raise ValueError(_OUTSIDE_PROXY_MESSAGE)


class ProxySession(requests.Session):
    """A ``requests.Session`` that keeps proxy credentials inside the proxy prefix.

    Redirects are followed exactly as ``requests`` follows them. On each hop,
    ``requests`` calls ``rebuild_auth``; before deferring to it, this removes
    ``Authorization``, ``connection_name``, ``identifier``,
    ``X-Scalekit-Connection-Name`` and ``X-Scalekit-Identifier`` (in any case)
    when the hop's target is outside ``<env base path>/proxy/``: a different
    origin (as ``requests.Session.should_strip_auth`` decides) or the same
    origin with a path the server would route outside the prefix (the rule
    ``ensure_under_proxy_prefix`` applies). Once removed, they stay removed for
    later hops. Hops that stay under the prefix are untouched.

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
        return all(
            _path_is_under_prefix(self._env_url, sent) for sent in _sent_paths(prepared_request)
        )


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


def _sent_paths(prepared: requests.PreparedRequest) -> list[str]:
    """Return the path of every request line ``prepared`` may be sent with.

    ``requests`` decides the request-target (``HTTPAdapter.request_url``), and
    this asks it for both cases: without a proxy (also a SOCKS proxy or an
    ``https`` tunnel) and through a forward proxy, whether or not one is
    configured. ``urllib3`` then writes the target as follows.

    * A path (``/...``) is sent as is, except that ``urllib3`` may re-encode a
      redirect hop's path (``_as_sent``); for a first request ``requests``
      already did, and ``_as_sent`` changes nothing.
    * An absolute URL (through a forward proxy, for any URL that is not
      ``https``) is sent as ``urllib3.util.parse_url`` rebuilds it. That
      removes dot segments again and treats ``%2F`` as part of a segment;
      ``requests`` may already have dropped an empty ``;`` parameter from the
      last segment, which can leave a ``..`` behind.
    """
    paths: list[str] = []
    for proxies in (None, _ANY_FORWARD_PROXY):
        target = _URL_ADAPTER.request_url(prepared, proxies)
        if target.startswith("/"):
            paths.append(_as_sent(target.split("?", 1)[0]))
            continue
        # Like urllib3's urlopen, parse any other target as an absolute URL.
        # If that fails here, the send fails the same way before writing
        # anything, so there is no further path to check.
        with contextlib.suppress(LocationParseError):
            paths.append(parse_url(target).path or "/")
    return paths


def _wire_path(url: str) -> str:
    """Return the path (without the query) that ``requests`` sends for ``url``.

    Preparing the URL runs it through ``urllib3``'s URL parser, which already
    applies the encoding ``_as_sent`` describes, so this is the wire form.
    """
    path_url: str = requests.Request(method="GET", url=url).prepare().path_url
    return path_url.split("?", 1)[0]


def _as_sent(path: str) -> str:
    """Return ``path`` as ``urllib3`` writes it in an origin-form request line.

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

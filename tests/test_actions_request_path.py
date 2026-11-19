"""Offline tests: ``ActionClient.request`` keeps every call under ``{env_url}/proxy/``.

A real HTTP server on 127.0.0.1 records the request-target of everything it
receives, so these tests assert what is actually sent on the wire, not what the
SDK meant to send. No credentials or network access beyond loopback are needed.
"""

import http.server
import os
import random
import threading
import unittest
from unittest import mock

import requests

from scalekit.actions._proxy_path import clean_path, proxy_account_headers
from scalekit.actions.actions import ActionClient

_AUTH_HEADER = "Bearer test-token"
_PROXY_ENV_KEYS = tuple(
    name
    for base in ("http_proxy", "https_proxy", "all_proxy", "no_proxy")
    for name in (base, base.upper())
)


class _RecordingServer(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _RecordingHandler)
        self.received = []  # (method, request-target, Authorization header)
        self.hops = []  # (method, request-target, {lower-cased header: value})
        self.header_lines = []  # [(name, value), ...] per request, as received
        self.statuses = []  # statuses to answer with, in order; then routes or 200
        self.redirects = {}  # request-target -> (status, Location)

    def reset(self):
        self.received.clear()
        self.hops.clear()
        self.header_lines.clear()
        self.statuses.clear()
        self.redirects.clear()


class _RecordingHandler(http.server.BaseHTTPRequestHandler):
    def _handle(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        self.server.received.append((self.command, self.path, self.headers.get("Authorization")))
        self.server.hops.append(
            (self.command, self.path, {k.lower(): v for k, v in self.headers.items()})
        )
        self.server.header_lines.append(list(self.headers.items()))
        status = self.server.statuses.pop(0) if self.server.statuses else 200
        location = None
        if status == 200 and self.path in self.server.redirects:
            status, location = self.server.redirects[self.path]
        self.send_response(status)
        if location is not None:
            self.send_header("Location", location)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"{}")

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _handle

    def log_message(self, *args):
        pass


class _ProxyServerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = _RecordingServer()
        cls.origin = f"http://127.0.0.1:{cls.server.server_port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def setUp(self):
        self.server.reset()
        # Talk to the loopback server directly even when the runner sets a proxy.
        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        for key in _PROXY_ENV_KEYS:
            os.environ.pop(key, None)

    def _client(self, env_url):
        core = mock.MagicMock()
        core.env_url = env_url
        core.get_headers.side_effect = lambda extra: {**extra, "Authorization": _AUTH_HEADER}
        tools = mock.MagicMock()
        tools.core_client = core
        return ActionClient(tools_client=tools, connected_accounts_client=mock.MagicMock()), core

    def assert_rejected(self, env_url, path, method="GET", **kwargs):
        with self.subTest(env_url=env_url, path=path, method=method):
            self.server.received.clear()
            client, core = self._client(env_url)
            with self.assertRaises(ValueError) as ctx:
                client.request("googledrive", "user@example.com", path, method=method, **kwargs)
            self.assertIn("proxy prefix", str(ctx.exception))
            self.assertNotIn(path, str(ctx.exception))
            self.assertEqual(self.server.received, [], "nothing may reach the server")
            core.get_headers.assert_not_called()

    def assert_sent(self, env_url, path, expected_target, **kwargs):
        with self.subTest(env_url=env_url, path=path):
            self.server.received.clear()
            client, _ = self._client(env_url)
            response = client.request("googledrive", "user@example.com", path, **kwargs)
            self.assertEqual(response.status_code, 200)
            method = kwargs.get("method", "GET").upper()
            self.assertEqual(self.server.received, [(method, expected_target, _AUTH_HEADER)])


class TestRequestRejectsPathsOutsideProxy(_ProxyServerTestCase):
    """Without the check, each path is sent (or routed by a server) outside ``/proxy/``."""

    def test_literal_dot_segments(self):
        # requests/urllib3 resolve these before sending: the wire target is /outside.
        for path in ["/x/../../outside", "/../outside", "/..", "/a;b/../../outside"]:
            self.assert_rejected(self.origin, path)

    def test_percent_encoded_dot_segments(self):
        # Sent as /proxy/x/../../outside; a server that cleans the path leaves /proxy/.
        for path in ["/x/%2e%2e/%2e%2e/outside", "/x/%2E%2e/%2e%2E/outside", "/%2e%2e/outside"]:
            self.assert_rejected(self.origin, path)

    def test_percent_encoded_slash_joined_dots(self):
        # Sent as /proxy/x%2F..%2F..%2Foutside; decoded once it is /proxy/x/../../outside.
        for path in ["/x%2f..%2f..%2foutside", "/x/..%2f..%2foutside"]:
            self.assert_rejected(self.origin, path)

    def test_empty_segments_collapse_before_dot_segments(self):
        # Servers clean "//" to "/" first, so the ".." removes "proxy" itself:
        # /proxy//../outside and /proxy///../outside both clean to /outside.
        for path in [
            "//..%2foutside/x",
            "/%2f..%2foutside/x",
            "//x/%2e%2e/%2e%2e/outside",
            "/%2F/..%2F..%2Foutside",
        ]:
            self.assert_rejected(self.origin, path)

    def test_backslash_dot_segments(self):
        # Sent as /proxy/x%5C..%5C..%5Coutside; servers that treat '\' as '/' leave /proxy/.
        for path in ["/x\\..\\..\\outside", "/x/..%5c..%5coutside"]:
            self.assert_rejected(self.origin, path)

    def test_backslash_inside_a_segment_name(self):
        # Decoded: /proxy/../proxy\/x. Treating '\' as '/' would give /proxy/x, but a
        # server that keeps '\' routes it as /proxy\/x, outside the prefix.
        self.assert_rejected(self.origin, "/..%2fproxy%5c/x")

    def test_control_characters_do_not_hide_a_real_escape(self):
        self.assert_rejected(self.origin, "/x/.\t./../../../outside")

    def test_sibling_of_the_proxy_prefix(self):
        # These clean to /proxyx and /proxy-other: next to the prefix, not under it.
        for path in ["/..%2fproxyx", "/..%2fproxy-other"]:
            self.assert_rejected(self.origin, path)

    def test_invalid_escape_keeps_encoded_slash_literal(self):
        # With an invalid escape in the path, urllib3 sends every '%' as '%25', so
        # the server reads "%2F" as text: /proxy%2Fx%2. is a sibling of /proxy/.
        for path in ["%2Fx%2.", "%2Fgmail/v1/users/me%"]:
            self.assert_rejected(self.origin, path)

    def test_path_without_leading_slash(self):
        # The path is glued onto "proxy" and goes to /proxygmail/..., outside the prefix.
        self.assert_rejected(self.origin, "gmail/v1/users/me/profile")

    def test_rejected_for_every_method(self):
        for method in ["POST", "put", "DELETE"]:
            self.assert_rejected(self.origin, "/x/../../outside", method=method)

    def test_rejected_before_the_401_retry(self):
        self.server.statuses.extend([401, 200])
        self.assert_rejected(self.origin, "/x/%2e%2e/%2e%2e/outside")


class TestRequestSendsInPrefixPathsUnchanged(_ProxyServerTestCase):
    """Paths that stay under ``/proxy/`` go on the wire exactly as they did before the check."""

    def test_plain_path(self):
        self.assert_sent(
            self.origin, "/gmail/v1/users/me/profile", "/proxy/gmail/v1/users/me/profile"
        )

    def test_root_path(self):
        self.assert_sent(self.origin, "/", "/proxy/")

    def test_space_is_percent_encoded(self):
        self.assert_sent(self.origin, "/a b/c", "/proxy/a%20b/c")

    def test_dot_segments_inside_prefix(self):
        self.assert_sent(self.origin, "/a/../drive/v3/files", "/proxy/drive/v3/files")
        self.assert_sent(self.origin, "/x/..", "/proxy/")

    def test_encoded_slash_inside_a_segment(self):
        self.assert_sent(self.origin, "/a%2Fb/c", "/proxy/a%2Fb/c")

    def test_encoded_leading_slash(self):
        # Sent as /proxy%2Fgmail/...; decoded once it is /proxy/gmail/..., which is
        # under the prefix.
        self.assert_sent(self.origin, "%2Fgmail/v1/users/me", "/proxy%2Fgmail/v1/users/me")

    def test_paths_that_clean_to_exactly_the_proxy_prefix(self):
        # These leave the prefix and come back to exactly /proxy, where no proxy
        # route matches. They are sent as before rather than rejected.
        self.assert_sent(self.origin, "/..%2fproxy", "/proxy/..%2Fproxy")
        self.assert_sent(self.origin, "/x%2f..", "/proxy/x%2F..")
        self.assert_sent(self.origin, "?alt=json", "/proxy?alt=json")

    def test_invalid_escape_inside_prefix(self):
        # urllib3 re-encodes '%' here too, but the path stays under /proxy/.
        self.assert_sent(self.origin, "/x%2./y", "/proxy/x%252./y")

    def test_trailing_newline(self):
        self.assert_sent(self.origin, "/gmail/v1\n", "/proxy/gmail/v1%0A")

    def test_control_character_split_dots(self):
        # requests percent-encodes TAB, LF and CR, so ".\t." reaches the server as
        # ".%09." and decodes to ".<TAB>.": an ordinary segment, not "..". The path
        # stays under /proxy/, so it is sent unchanged.
        self.assert_sent(self.origin, "/x/.\t./.\t./y", "/proxy/x/.%09./.%09./y")
        self.assert_sent(self.origin, "/x/.\n./.\n./y", "/proxy/x/.%0A./.%0A./y")
        self.assert_sent(self.origin, "/x/.\r./.\r./y", "/proxy/x/.%0D./.%0D./y")

    def test_double_encoded_dots_decode_once(self):
        # One decode yields "%2e%2e", which is not a dot segment.
        self.assert_sent(self.origin, "/x/%252e%252e/y", "/proxy/x/%252e%252e/y")

    def test_dots_in_query_string_are_not_path(self):
        self.assert_sent(self.origin, "/search?q=a/../../b", "/proxy/search?q=a/../../b")

    def test_query_params_and_post(self):
        self.assert_sent(
            self.origin,
            "/drive/v3/about",
            "/proxy/drive/v3/about?fields=user",
            query_params={"fields": "user"},
        )
        self.assert_sent(
            self.origin, "/drive/v3/files", "/proxy/drive/v3/files", method="post", body={"a": 1}
        )

    def test_401_retry_resends_the_same_path(self):
        self.server.statuses.extend([401, 200])
        client, core = self._client(self.origin)
        response = client.request("googledrive", "user@example.com", "/drive/v3/about")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [target for _, target, _ in self.server.received],
            ["/proxy/drive/v3/about", "/proxy/drive/v3/about"],
        )
        core._CoreClient__authenticate_client.assert_called_once_with()

    def test_401_retry_sends_the_same_body_for_an_empty_raw_body(self):
        # raw_body takes priority whenever it is given, even when empty, on both sends.
        self.server.statuses.extend([401, 200])
        client, _ = self._client(self.origin)
        client.request(
            "googledrive", "user@example.com", "/drive/v3/files",
            method="post", raw_body=b"", form_data={"a": "1"},
        )
        lengths = [headers.get("content-length", "0") for _, _, headers in self.server.hops]
        self.assertEqual(lengths, ["0", "0"])


class TestRequestWithBasePathInEnvUrl(_ProxyServerTestCase):
    """The prefix is ``<env base path>/proxy/`` when the env URL has a path."""

    def test_escape_above_base_proxy_is_rejected(self):
        env_url = self.origin + "/base"
        for path in [
            "/../x",
            "/%2e%2e/x",
            "/../../proxy/x",
            "/x/../../../base/x",
            "//..%2fx",
            "/..%2fproxyx",
        ]:
            self.assert_rejected(env_url, path)

    def test_paths_under_base_proxy_are_sent_unchanged(self):
        for env_url in [self.origin + "/base", self.origin + "/base/"]:
            self.assert_sent(
                env_url, "/gmail/v1/users/me/profile", "/base/proxy/gmail/v1/users/me/profile"
            )
            self.assert_sent(env_url, "/a/../b", "/base/proxy/b")
            self.assert_sent(env_url, "/a b/c", "/base/proxy/a%20b/c")
            self.assert_sent(env_url, "/..%2fproxy", "/base/proxy/..%2Fproxy")


_CREDENTIAL_HEADERS = (
    "authorization",
    "connection_name",
    "identifier",
    "x-scalekit-connection-name",
    "x-scalekit-identifier",
)


class TestRedirectsKeepCredentialsInsideProxy(_ProxyServerTestCase):
    """Redirects are followed as before; credentials never go outside ``/proxy/``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other = _RecordingServer()  # same host, different port: another origin
        cls.other_origin = f"http://127.0.0.1:{cls.other.server_port}"
        cls.other_thread = threading.Thread(target=cls.other.serve_forever, daemon=True)
        cls.other_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.other.shutdown()
        cls.other.server_close()
        cls.other_thread.join(timeout=5)
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.other.reset()

    def _request(self, env_url=None, path="/start", **kwargs):
        client, core = self._client(env_url or self.origin)
        return client.request("googledrive", "user@example.com", path, **kwargs), core

    def assert_credentials(self, headers, *, present):
        for name in _CREDENTIAL_HEADERS:
            if present:
                self.assertIn(name, headers)
            else:
                self.assertNotIn(name, headers)

    def test_same_host_redirect_outside_prefix_drops_credentials(self):
        for location, target in [
            ("/outside", "/outside"),
            (self.origin + "/outside", "/outside"),
            ("/proxy/x/../../outside", "/outside"),
            (self.origin + "/proxy/x/%2e%2e/%2e%2e/outside", "/proxy/x/../../outside"),
            ("/proxy/x%2f..%2f..%2foutside", "/proxy/x%2F..%2F..%2Foutside"),
            ("/proxy//..%2fx", "/proxy//..%2Fx"),
            (self.origin + "/proxy//x/%2e%2e/%2e%2e/outside", "/proxy//x/../../outside"),
            ("/proxyx", "/proxyx"),
            ("/proxy%2F%2.", "/proxy%252F%252."),
        ]:
            with self.subTest(location=location):
                self.server.reset()
                self.server.redirects["/proxy/start"] = (302, location)
                response, _ = self._request()

                self.assertEqual(response.status_code, 200)
                self.assertEqual([h[1] for h in self.server.hops], ["/proxy/start", target])
                self.assert_credentials(self.server.hops[0][2], present=True)
                self.assert_credentials(self.server.hops[1][2], present=False)
                # The response the caller gets is unchanged, including the record
                # of what the first hop sent.
                self.assertEqual([r.status_code for r in response.history], [302])
                self.assertEqual(response.history[0].request.headers["Authorization"], _AUTH_HEADER)

    def test_redirect_inside_prefix_keeps_credentials(self):
        for location, target in [
            ("/proxy/drive/v3/files", "/proxy/drive/v3/files"),
            (self.origin + "/proxy/drive/v3/about", "/proxy/drive/v3/about"),
            ("sibling", "/proxy/sibling"),
            ("/proxy/a/../b", "/proxy/b"),
            ("/proxy%2Fdrive/v3/files", "/proxy%2Fdrive/v3/files"),
            ("/proxy/x%2./y", "/proxy/x%252./y"),
        ]:
            with self.subTest(location=location):
                self.server.reset()
                self.server.redirects["/proxy/start"] = (302, location)
                response, _ = self._request()

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    self.server.received,
                    [("GET", "/proxy/start", _AUTH_HEADER), ("GET", target, _AUTH_HEADER)],
                )
                self.assert_credentials(self.server.hops[1][2], present=True)

    def test_redirect_to_another_origin_drops_credentials(self):
        # requests already drops Authorization when the port changes; the
        # connection headers are now dropped as well.
        self.server.redirects["/proxy/start"] = (302, self.other_origin + "/proxy/anything")
        response, _ = self._request()

        self.assertEqual(response.status_code, 200)
        self.assertEqual([h[1] for h in self.server.hops], ["/proxy/start"])
        self.assertEqual([h[1] for h in self.other.hops], ["/proxy/anything"])
        self.assert_credentials(self.other.hops[0][2], present=False)

    def test_method_preserving_redirect_outside_prefix(self):
        self.server.redirects["/proxy/start"] = (307, "/outside")
        response, _ = self._request(method="POST", body={"name": "x"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [h[:2] for h in self.server.hops],
            [("POST", "/proxy/start"), ("POST", "/outside")],
        )
        self.assert_credentials(self.server.hops[1][2], present=False)

    def test_credentials_stay_dropped_after_leaving_prefix(self):
        self.server.redirects["/proxy/start"] = (302, "/outside/a")
        self.server.redirects["/outside/a"] = (302, "/proxy/back")
        response, _ = self._request()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [h[1] for h in self.server.hops], ["/proxy/start", "/outside/a", "/proxy/back"]
        )
        self.assert_credentials(self.server.hops[1][2], present=False)
        self.assert_credentials(self.server.hops[2][2], present=False)

    def test_base_path_in_env_url(self):
        env_url = self.origin + "/base"
        for location, present in [
            ("/base/proxy/other", True),
            ("/proxy/other", False),
            ("/base/x", False),
            ("/base/proxy//..%2Fx", False),
        ]:
            with self.subTest(location=location):
                self.server.reset()
                self.server.redirects["/base/proxy/start"] = (302, location)
                response, _ = self._request(env_url=env_url)

                self.assertEqual(response.status_code, 200)
                self.assertEqual([h[1] for h in self.server.hops], ["/base/proxy/start", location])
                self.assert_credentials(self.server.hops[1][2], present=present)

    def test_other_caller_headers_follow_a_redirect_outside_prefix(self):
        # Only the account headers are credentials; X-Identifier is a provider
        # header and is never treated as one.
        self.server.redirects["/proxy/start"] = (302, "/outside")
        response, _ = self._request(headers={"X-Identifier": "provider-value"})

        self.assertEqual(response.status_code, 200)
        self.assert_credentials(self.server.hops[1][2], present=False)
        self.assertEqual(self.server.hops[1][2]["x-identifier"], "provider-value")

    def test_401_retry_then_redirect_outside_prefix(self):
        self.server.statuses.append(401)
        self.server.redirects["/proxy/start"] = (302, "/outside")
        response, core = self._request()

        self.assertEqual(response.status_code, 200)
        core._CoreClient__authenticate_client.assert_called_once_with()
        self.assertEqual(
            [h[1] for h in self.server.hops],
            ["/proxy/start", "/proxy/start", "/outside"],
        )
        self.assert_credentials(self.server.hops[0][2], present=True)
        self.assert_credentials(self.server.hops[1][2], present=True)
        self.assert_credentials(self.server.hops[2][2], present=False)


_PROXIED_ENV = "http://scalekit-env.invalid"


class TestRequestThroughForwardProxy(_ProxyServerTestCase):
    """With an ``http://`` env URL, a forward proxy gets the absolute URL.

    ``self.server`` plays the forward proxy: it records the absolute-form
    request-target and answers itself, so the env host is never resolved.
    ``urllib3`` re-parses that URL before sending and removes dot segments a
    second time, in which ``%2F`` does not split a segment.
    """

    def _proxies(self):
        return {"proxies": {"http": self.origin}}

    def test_escape_after_reparse_is_rejected_before_sending(self):
        for env_url, path in [
            # Sent directly as /proxy/a%2Fb/../../outside, which the server routes
            # under the prefix; re-parsed for the proxy it becomes /outside.
            (_PROXIED_ENV, "/a%2Fb/%2e%2e/%2e%2e/outside"),
            (_PROXIED_ENV, "/a%2fb%2Fc/%2E%2E/%2e%2e/outside"),
            # requests drops an empty ";" parameter from the last segment, which
            # leaves a ".." for the re-parse.
            (_PROXIED_ENV, "/..;"),
            (_PROXIED_ENV, "/%2e%2e;?alt=json"),
            (_PROXIED_ENV + "/base", "/a%2Fb%2Fc/%2e%2e/%2e%2e/%2e%2e/outside"),
        ]:
            self.assert_rejected(env_url, path, **self._proxies())

    def test_in_prefix_paths_are_sent_unchanged(self):
        for path, target in [
            ("/gmail/v1/users/me/profile", "/proxy/gmail/v1/users/me/profile"),
            ("%2Fgmail/v1/users/me", "/proxy%2Fgmail/v1/users/me"),
            ("/", "/proxy/"),
            ("?alt=json", "/proxy?alt=json"),
            ("/a%2Fb/c", "/proxy/a%2Fb/c"),
            ("/a%2Fb/%2e%2e/c", "/proxy/c"),
            ("/x/..;", "/proxy/"),
        ]:
            self.assert_sent(_PROXIED_ENV, path, _PROXIED_ENV + target, **self._proxies())

    def test_redirect_hop(self):
        # A relative Location is resolved by urljoin before it is sent, so the
        # re-parse only matters for an absolute one.
        start = _PROXIED_ENV + "/proxy/start"
        for location, target, present in [
            (_PROXIED_ENV + "/proxy/a%2Fb/%2e%2e/%2e%2e/outside", "/outside", False),
            ("/proxy/drive/v3/files", "/proxy/drive/v3/files", True),
            ("/proxy/a%2Fb/%2e%2e/c", "/proxy/c", True),
        ]:
            with self.subTest(location=location):
                self.server.reset()
                self.server.redirects[start] = (302, location)
                client, _ = self._client(_PROXIED_ENV)
                response = client.request(
                    "googledrive", "user@example.com", "/start", **self._proxies()
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual([h[1] for h in self.server.hops], [start, _PROXIED_ENV + target])
                for name in _CREDENTIAL_HEADERS:
                    self.assertIn(name, self.server.hops[0][2])
                    self.assertEqual(name in self.server.hops[1][2], present, name)

    def test_proxy_from_environment(self):
        proxy_env = {"HTTP_PROXY": self.origin, "http_proxy": self.origin}
        with mock.patch.dict(os.environ, proxy_env):
            # patch.dict restores the whole environment on exit, these included.
            for name in ("NO_PROXY", "no_proxy", "ALL_PROXY", "all_proxy"):
                os.environ.pop(name, None)
            self.assert_rejected(_PROXIED_ENV, "/a%2Fb/%2e%2e/%2e%2e/outside")
            self.assert_sent(
                _PROXIED_ENV, "%2Fgmail/v1/users/me", _PROXIED_ENV + "/proxy%2Fgmail/v1/users/me"
            )


_ARG_CONNECTION = "googledrive"
_ARG_IDENTIFIER = "user@example.com"


def _sent_by_earlier_versions(headers):
    """Return (connection name, identifier) as earlier SDK versions sent them.

    Those versions built this dict, merged the caller's headers over it with
    dict.update, and let requests turn it into the request's headers. A value of
    None means the header was not sent.
    """
    legacy = {
        "connection_name": _ARG_CONNECTION,
        "Connection_name": _ARG_CONNECTION,
        "identifier": _ARG_IDENTIFIER,
    }
    legacy.update(headers)
    prepared = requests.Session().prepare_request(
        requests.Request("GET", "http://h/proxy/x", headers=legacy)
    )
    return prepared.headers.get("connection_name"), prepared.headers.get("identifier")


def _text(value):
    return value.decode("ascii") if isinstance(value, bytes) else value


class TestRequestConnectedAccountHeaders(_ProxyServerTestCase):
    """The account goes out under the original and the X-Scalekit names, with equal values.

    Proxies that drop headers containing '_' remove connection_name and
    identifier; the X-Scalekit names carry the account through them. The server
    rejects a request whose two names differ, so they must always agree, and
    the value must be the one earlier versions sent.
    """

    def _send(self, headers=None):
        client, core = self._client(self.origin)
        response = client.request(
            _ARG_CONNECTION, _ARG_IDENTIFIER, "/drive/v3/about", headers=headers
        )
        self.assertEqual(response.status_code, 200)
        return core

    def assert_account(self, hop_headers, connection_name, identifier):
        """Check both names of each pair; None means neither name was sent."""
        for names, expected in (
            (("connection_name", "x-scalekit-connection-name"), connection_name),
            (("identifier", "x-scalekit-identifier"), identifier),
        ):
            for name in names:
                self.assertEqual(hop_headers.get(name), _text(expected), name)

    def assert_one_line_per_header(self):
        for lines in self.server.header_lines:
            names = [name.lower() for name, _ in lines]
            self.assertEqual(len(names), len(set(names)), names)

    def assert_sent_as_before(self, headers, connection_name, identifier):
        self.assertEqual(_sent_by_earlier_versions(headers), (connection_name, identifier))
        self.server.reset()
        self._send(headers)
        self.assert_account(self.server.hops[0][2], connection_name, identifier)
        self.assert_one_line_per_header()

    def test_sends_both_names_with_equal_values(self):
        self._send()
        self.assertEqual(len(self.server.hops), 1)
        self.assert_account(self.server.hops[0][2], _ARG_CONNECTION, _ARG_IDENTIFIER)
        self.assert_one_line_per_header()

    def test_401_retry_sends_both_names(self):
        self.server.statuses.extend([401, 200])
        core = self._send()
        core._CoreClient__authenticate_client.assert_called_once_with()
        self.assertEqual(len(self.server.hops), 2)
        for _, _, headers in self.server.hops:
            self.assert_account(headers, _ARG_CONNECTION, _ARG_IDENTIFIER)
        self.assert_one_line_per_header()

    def test_caller_override_sends_what_earlier_versions_sent(self):
        for headers, connection_name, identifier in [
            ({"identifier": "u2"}, _ARG_CONNECTION, "u2"),
            ({"Identifier": "u2"}, _ARG_CONNECTION, "u2"),
            ({"IDENTIFIER": "u2"}, _ARG_CONNECTION, "u2"),
            ({"Connection_name": "gmail"}, "gmail", _ARG_IDENTIFIER),
            ({"Connection_Name": "gmail"}, "gmail", _ARG_IDENTIFIER),
            ({"Connection_name": "gmail", "identifier": "u2"}, "gmail", "u2"),
            # The exact key "connection_name" is updated in place, ahead of the
            # "Connection_name" key that follows it, so the argument wins.
            ({"connection_name": "gmail"}, _ARG_CONNECTION, _ARG_IDENTIFIER),
            ({"Identifier": "a", "identifier": "b"}, _ARG_CONNECTION, "a"),
            ({"Connection_name": "y", "connection_name": "x"}, "y", _ARG_IDENTIFIER),
            ({"CONNECTION_NAME": "z", "connection_name": "x"}, "z", _ARG_IDENTIFIER),
            ({"identifier": ""}, _ARG_CONNECTION, ""),
        ]:
            with self.subTest(headers=headers):
                self.assert_sent_as_before(headers, connection_name, identifier)

    def test_bytes_header_names_match_like_str_names(self):
        for headers, connection_name, identifier in [
            ({b"identifier": b"u2"}, _ARG_CONNECTION, b"u2"),
            ({b"Connection_name": b"gmail"}, b"gmail", _ARG_IDENTIFIER),
            # requests keeps str and bytes names apart until it prepares the
            # request, so the bytes key, merged later, wins here.
            ({b"identifier": b"u2", "Identifier": "u3"}, _ARG_CONNECTION, b"u2"),
            ({"Identifier": None, b"identifier": b"x"}, _ARG_CONNECTION, b"x"),
        ]:
            with self.subTest(headers=headers):
                self.assert_sent_as_before(headers, connection_name, identifier)

    def test_none_value_sends_neither_name(self):
        for headers, connection_name, identifier in [
            ({"identifier": None}, _ARG_CONNECTION, None),
            ({"Identifier": None}, _ARG_CONNECTION, None),
            ({"Connection_name": None}, None, _ARG_IDENTIFIER),
            ({"identifier": None, "X-Scalekit-Identifier": "u9"}, _ARG_CONNECTION, None),
            # "connection_name" is followed by "Connection_name", which still
            # carries the argument.
            ({"connection_name": None}, _ARG_CONNECTION, _ARG_IDENTIFIER),
        ]:
            with self.subTest(headers=headers):
                self.assert_sent_as_before(headers, connection_name, identifier)

    def test_caller_x_scalekit_headers_are_replaced(self):
        for headers, connection_name, identifier in [
            ({"X-Scalekit-Identifier": "u9"}, _ARG_CONNECTION, _ARG_IDENTIFIER),
            ({"x-scalekit-identifier": "u9"}, _ARG_CONNECTION, _ARG_IDENTIFIER),
            ({"X-SCALEKIT-IDENTIFIER": ""}, _ARG_CONNECTION, _ARG_IDENTIFIER),
            ({"X-Scalekit-Identifier": None}, _ARG_CONNECTION, _ARG_IDENTIFIER),
            ({b"X-Scalekit-Identifier": b"u9"}, _ARG_CONNECTION, _ARG_IDENTIFIER),
            ({"X-Scalekit-Connection-Name": "slack"}, _ARG_CONNECTION, _ARG_IDENTIFIER),
            ({"identifier": "u2", "X-Scalekit-Identifier": "u3"}, _ARG_CONNECTION, "u2"),
            (
                {"x-scalekit-connection-name": "slack", "Connection_name": "gmail"},
                "gmail",
                _ARG_IDENTIFIER,
            ),
        ]:
            with self.subTest(headers=headers):
                self.assert_sent_as_before(headers, connection_name, identifier)

    def test_x_identifier_passes_through_untouched(self):
        self._send({"X-Identifier": "provider-value"})
        hop = self.server.hops[0][2]
        self.assertEqual(hop["x-identifier"], "provider-value")
        self.assert_account(hop, _ARG_CONNECTION, _ARG_IDENTIFIER)

    def test_no_case_variants_with_different_values_reach_requests(self):
        client, core = self._client(self.origin)
        client.request(
            _ARG_CONNECTION,
            _ARG_IDENTIFIER,
            "/drive/v3/about",
            headers={
                "Identifier": "u2",
                "CONNECTION_NAME": "gmail",
                "x-scalekit-identifier": "other",
                "Accept": "text/csv",
            },
        )
        (sent,), _ = core.get_headers.call_args
        values_by_name = {}
        for name, value in sent.items():
            values_by_name.setdefault(name.lower(), set()).add(value)
        self.assertEqual(values_by_name["connection_name"], {"gmail"})
        self.assertEqual(values_by_name["x-scalekit-connection-name"], {"gmail"})
        self.assertEqual(values_by_name["identifier"], {"u2"})
        self.assertEqual(values_by_name["x-scalekit-identifier"], {"u2"})
        self.assertEqual(values_by_name["accept"], {"text/csv"})


class TestProxyAccountHeaders(unittest.TestCase):
    """The helper both request() and upload_resumable() build their headers with."""

    def test_default_headers(self):
        self.assertEqual(
            proxy_account_headers("gmail", "u1"),
            {
                "connection_name": "gmail",
                "Connection_name": "gmail",
                "X-Scalekit-Connection-Name": "gmail",
                "identifier": "u1",
                "X-Scalekit-Identifier": "u1",
            },
        )

    def test_matches_earlier_versions_for_many_combinations(self):
        # Random combinations of case variants, bytes names, None and bytes
        # values: the original names carry what earlier versions sent, and the
        # X-Scalekit names carry the same value (or are absent with it).
        names = [
            "connection_name",
            "Connection_name",
            "CONNECTION_NAME",
            b"connection_name",
            b"Connection_Name",
            "identifier",
            "Identifier",
            b"identifier",
            b"IDENTIFIER",
            "X-Scalekit-Identifier",
            "x-scalekit-connection-name",
        ]
        values = ["a", "b", "", None, b"c"]
        rng = random.Random(3343)
        for _ in range(500):
            chosen = rng.sample(names, rng.randint(1, 5))
            headers = {name: rng.choice(values) for name in chosen}
            with self.subTest(headers=headers):
                built = proxy_account_headers(_ARG_CONNECTION, _ARG_IDENTIFIER, headers)
                request = requests.Request("GET", "http://h/proxy/x", headers=built)
                prepared = requests.Session().prepare_request(request).headers
                connection_name, identifier = _sent_by_earlier_versions(headers)
                self.assertEqual(prepared.get("connection_name"), connection_name)
                self.assertEqual(prepared.get("X-Scalekit-Connection-Name"), connection_name)
                self.assertEqual(prepared.get("identifier"), identifier)
                self.assertEqual(prepared.get("X-Scalekit-Identifier"), identifier)

    def test_blank_override_is_sent_as_before(self):
        headers = proxy_account_headers("gmail", "u1", {"identifier": ""})
        self.assertEqual((headers["identifier"], headers["X-Scalekit-Identifier"]), ("", ""))

    def test_none_value_drops_both_names_of_the_pair(self):
        headers = proxy_account_headers("gmail", "u1", {"Identifier": None})
        for name in ("identifier", "X-Scalekit-Identifier", "Identifier"):
            self.assertNotIn(name, headers)
        self.assertEqual(headers["X-Scalekit-Connection-Name"], "gmail")

    def test_accepts_what_dict_update_accepts(self):
        headers = proxy_account_headers("gmail", "u1", [("Identifier", "u2"), ("Accept", "x")])
        self.assertEqual(headers["X-Scalekit-Identifier"], "u2")
        self.assertEqual(headers["Accept"], "x")

    def test_bytes_name_and_value(self):
        value = b"u2"
        headers = proxy_account_headers("gmail", "u1", {b"identifier": value})
        self.assertIs(headers["identifier"], value)
        self.assertIs(headers["X-Scalekit-Identifier"], value)
        self.assertNotIn(b"identifier", headers)

    def test_similar_names_are_not_account_headers(self):
        extra = {
            "X-Identifier": "a",
            "identifier-x": "b",
            "Connection": "keep-alive",
            "X-Scalekit-Other": "c",
            b"X-Bytes-Name": b"d",
        }
        headers = proxy_account_headers("gmail", "u1", extra)
        for name, value in extra.items():
            self.assertEqual(headers[name], value)
        self.assertEqual(headers["identifier"], "u1")

    def test_does_not_modify_the_callers_headers(self):
        extra = {"Identifier": "u2", "X-Scalekit-Identifier": "u3"}
        proxy_account_headers("gmail", "u1", extra)
        self.assertEqual(extra, {"Identifier": "u2", "X-Scalekit-Identifier": "u3"})


class TestCleanPath(unittest.TestCase):
    """The server-side model cleans paths as Go routers do."""

    def test_clean_path(self):
        cases = {
            "": "/",
            "/": "/",
            "//": "/",
            "/a//b": "/a/b",
            "/a/b/": "/a/b/",
            "/a/./b/.": "/a/b",
            "/a/b/c/./../../g": "/a/g",
            "/proxy//../x": "/x",
            "/proxy//../x/./y/": "/x/y/",
            "/../g": "/g",
            "/..": "/",
            "/proxy/x/..": "/proxy",
            "/proxy/x/../": "/proxy/",
            "/g..": "/g..",
            "/..g": "/..g",
            "a/b": "/a/b",
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(clean_path(path), expected)


if __name__ == "__main__":
    unittest.main()

"""Offline tests: ``ActionClient.request`` keeps every call under ``{env_url}/proxy/``.

A real HTTP server on 127.0.0.1 records the request-target of everything it
receives, so these tests assert what is actually sent on the wire, not what the
SDK meant to send. No credentials or network access beyond loopback are needed.
"""

import http.server
import threading
import unittest
from unittest import mock

from scalekit.actions._proxy_path import remove_dot_segments
from scalekit.actions.actions import ActionClient

_AUTH_HEADER = "Bearer test-token"


class _RecordingServer(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _RecordingHandler)
        self.received = []  # (method, request-target, Authorization header)
        self.hops = []  # (method, request-target, {lower-cased header: value})
        self.statuses = []  # statuses to answer with, in order; then routes or 200
        self.redirects = {}  # request-target -> (status, Location)

    def reset(self):
        self.received.clear()
        self.hops.clear()
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

    def _client(self, env_url):
        core = mock.MagicMock()
        core.env_url = env_url
        core.get_headers.side_effect = lambda extra: {**extra, "Authorization": _AUTH_HEADER}
        tools = mock.MagicMock()
        tools.core_client = core
        return ActionClient(tools_client=tools, connected_accounts_client=mock.MagicMock()), core

    def assert_rejected(self, env_url, path, method="GET"):
        with self.subTest(env_url=env_url, path=path, method=method):
            self.server.received.clear()
            client, core = self._client(env_url)
            with self.assertRaises(ValueError) as ctx:
                client.request("googledrive", "user@example.com", path, method=method)
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
    """Without the check, each path is sent (or read by a server) outside ``/proxy/``."""

    def test_literal_dot_segments(self):
        # requests/urllib3 resolve these before sending: the wire target is /api/... .
        for path in ["/x/../../api/v1/organizations", "/../api", "/..", "/a;b/../../c"]:
            self.assert_rejected(self.origin, path)

    def test_percent_encoded_dot_segments(self):
        # Sent as /proxy/x/../../api; a server that normalises the path leaves /proxy/.
        for path in ["/x/%2e%2e/%2e%2e/api", "/x/%2E%2e/%2e%2E/api", "/%2e%2e/api"]:
            self.assert_rejected(self.origin, path)

    def test_percent_encoded_slash_joined_dots(self):
        # Sent as /proxy/x%2F..%2F..%2Fapi; decoded once it is /proxy/x/../../api.
        for path in ["/x%2f..%2f..%2fapi", "/x/..%2f..%2fapi"]:
            self.assert_rejected(self.origin, path)

    def test_backslash_dot_segments(self):
        # Sent as /proxy/x%5C..%5C..%5Capi; servers that treat '\' as '/' leave /proxy/.
        for path in ["/x\\..\\..\\api", "/x/..%5c..%5capi"]:
            self.assert_rejected(self.origin, path)

    def test_control_characters_do_not_hide_a_real_escape(self):
        self.assert_rejected(self.origin, "/x/.\t./../../../api")

    def test_path_that_never_enters_proxy_prefix(self):
        # Without a leading '/', the path is glued onto "proxy": /proxygmail/... .
        # A bare query targets /proxy itself. Neither is under /proxy/.
        for path in ["gmail/v1/users/me/profile", "?alt=json"]:
            self.assert_rejected(self.origin, path)

    def test_rejected_for_every_method(self):
        for method in ["POST", "put", "DELETE"]:
            self.assert_rejected(self.origin, "/x/../../api/v1/organizations", method=method)

    def test_rejected_before_the_401_retry(self):
        self.server.statuses.extend([401, 200])
        self.assert_rejected(self.origin, "/x/%2e%2e/%2e%2e/api")


class TestRequestSendsInPrefixPathsUnchanged(_ProxyServerTestCase):
    """Paths that stay under ``/proxy/`` go on the wire exactly as they did before the check."""

    def test_plain_path(self):
        self.assert_sent(
            self.origin, "/gmail/v1/users/me/profile", "/proxy/gmail/v1/users/me/profile"
        )

    def test_space_is_percent_encoded(self):
        self.assert_sent(self.origin, "/a b/c", "/proxy/a%20b/c")

    def test_dot_segments_inside_prefix(self):
        self.assert_sent(self.origin, "/a/../drive/v3/files", "/proxy/drive/v3/files")
        self.assert_sent(self.origin, "/x/..", "/proxy/")

    def test_encoded_slash_inside_a_segment(self):
        self.assert_sent(self.origin, "/a%2Fb/c", "/proxy/a%2Fb/c")

    def test_trailing_newline(self):
        self.assert_sent(self.origin, "/gmail/v1\n", "/proxy/gmail/v1%0A")

    def test_control_character_split_dots(self):
        # requests percent-encodes TAB, LF and CR, so ".\t." reaches the server as
        # ".%09." and decodes to ".<TAB>.": an ordinary segment, not "..". The path
        # stays under /proxy/, so it is sent unchanged.
        self.assert_sent(self.origin, "/x/.\t./.\t./api", "/proxy/x/.%09./.%09./api")
        self.assert_sent(self.origin, "/x/.\n./.\n./api", "/proxy/x/.%0A./.%0A./api")
        self.assert_sent(self.origin, "/x/.\r./.\r./api", "/proxy/x/.%0D./.%0D./api")

    def test_double_encoded_dots_decode_once(self):
        # One decode yields "%2e%2e", which is not a dot segment.
        self.assert_sent(self.origin, "/x/%252e%252e/api", "/proxy/x/%252e%252e/api")

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


class TestRequestWithBasePathInEnvUrl(_ProxyServerTestCase):
    """The prefix is ``<env base path>/proxy/`` when the env URL has a path."""

    def test_escape_above_base_proxy_is_rejected(self):
        env_url = self.origin + "/base"
        for path in ["/../x", "/%2e%2e/x", "/../../proxy/x", "/x/../../../base/x"]:
            self.assert_rejected(env_url, path)

    def test_paths_under_base_proxy_are_sent_unchanged(self):
        for env_url in [self.origin + "/base", self.origin + "/base/"]:
            self.assert_sent(
                env_url, "/gmail/v1/users/me/profile", "/base/proxy/gmail/v1/users/me/profile"
            )
            self.assert_sent(env_url, "/a/../b", "/base/proxy/b")
            self.assert_sent(env_url, "/a b/c", "/base/proxy/a%20b/c")


_CREDENTIAL_HEADERS = ("authorization", "connection_name", "identifier")


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
            ("/api/v1/organizations", "/api/v1/organizations"),
            (self.origin + "/api/v1/organizations", "/api/v1/organizations"),
            ("/proxy/x/../../api", "/api"),
            (self.origin + "/proxy/x/%2e%2e/%2e%2e/api", "/proxy/x/../../api"),
            ("/proxy/x%2f..%2f..%2fapi", "/proxy/x%2F..%2F..%2Fapi"),
            ("/proxy", "/proxy"),
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
        self.server.redirects["/proxy/start"] = (307, "/api/v1/organizations")
        response, _ = self._request(method="POST", body={"name": "x"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [h[:2] for h in self.server.hops],
            [("POST", "/proxy/start"), ("POST", "/api/v1/organizations")],
        )
        self.assert_credentials(self.server.hops[1][2], present=False)

    def test_credentials_stay_dropped_after_leaving_prefix(self):
        self.server.redirects["/proxy/start"] = (302, "/api/a")
        self.server.redirects["/api/a"] = (302, "/proxy/back")
        response, _ = self._request()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [h[1] for h in self.server.hops], ["/proxy/start", "/api/a", "/proxy/back"]
        )
        self.assert_credentials(self.server.hops[1][2], present=False)
        self.assert_credentials(self.server.hops[2][2], present=False)

    def test_base_path_in_env_url(self):
        env_url = self.origin + "/base"
        for location, present in [
            ("/base/proxy/other", True),
            ("/proxy/other", False),
            ("/base/x", False),
        ]:
            with self.subTest(location=location):
                self.server.reset()
                self.server.redirects["/base/proxy/start"] = (302, location)
                response, _ = self._request(env_url=env_url)

                self.assertEqual(response.status_code, 200)
                self.assertEqual([h[1] for h in self.server.hops], ["/base/proxy/start", location])
                self.assert_credentials(self.server.hops[1][2], present=present)

    def test_401_retry_then_redirect_outside_prefix(self):
        self.server.statuses.append(401)
        self.server.redirects["/proxy/start"] = (302, "/api/v1/organizations")
        response, core = self._request()

        self.assertEqual(response.status_code, 200)
        core._CoreClient__authenticate_client.assert_called_once_with()
        self.assertEqual(
            [h[1] for h in self.server.hops],
            ["/proxy/start", "/proxy/start", "/api/v1/organizations"],
        )
        self.assert_credentials(self.server.hops[0][2], present=True)
        self.assert_credentials(self.server.hops[1][2], present=True)
        self.assert_credentials(self.server.hops[2][2], present=False)


class TestRemoveDotSegments(unittest.TestCase):
    """The server-side model follows RFC 3986 section 5.2.4."""

    def test_rfc_3986_examples(self):
        cases = {
            "/a/b/c/./../../g": "/a/g",
            "mid/content=5/../6": "mid/6",
            "/a/b/c/..": "/a/b/",
            "/a/b/c/.": "/a/b/c/",
            "/../g": "/g",
            "/./g": "/g",
            "/g..": "/g..",
            "/..g": "/..g",
            "/": "/",
            "": "",
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(remove_dot_segments(path), expected)


if __name__ == "__main__":
    unittest.main()

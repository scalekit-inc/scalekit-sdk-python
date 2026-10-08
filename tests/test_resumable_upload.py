"""Offline tests for ActionClient.upload_resumable (Google resumable uploads via the proxy).

A scripted fake replaces requests.request, so no network or credentials are needed.
"""

import io
import json
import logging
import os
import tempfile
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests
from requests.structures import CaseInsensitiveDict

from scalekit.actions import _resumable_upload as ru
from scalekit.actions.actions import ActionClient
from scalekit.actions.types import UploadProgress
from scalekit.common.exceptions import (
    ScalekitException,
    ScalekitUploadException,
    ScalekitUploadProtocolException,
    ScalekitUploadSessionExpiredException,
)
from scalekit.core import CoreClient

KIB = 1024
CHUNK = 256 * KIB
CANARY = "canary-token-7f3a9c"
ROTATED = "rotated-credential-2b81"
UPLOAD_ID = "up-123"
LOCATION = (
    f"https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&upload_id={UPLOAD_ID}"
)
SCALEKIT_401 = {"detail": "token expired", "code": "UNAUTHORIZED"}


def resp(status, headers=None, body=b""):
    r = requests.Response()
    r.status_code = status
    r.headers = CaseInsensitiveDict(headers or {})
    if isinstance(body, (dict, list)):
        body = json.dumps(body).encode()
        r.headers.setdefault("Content-Type", "application/json")
    elif isinstance(body, str):
        body = body.encode()
    r._content = body
    return r


def started():
    return resp(200, {"Location": LOCATION})


def incomplete(last_byte=None):
    return resp(308, {"Range": f"bytes=0-{last_byte}"} if last_byte is not None else {})


def done(body=None):
    return resp(200, body=body if body is not None else {"id": "file-1", "name": "x"})


class FakeTransport:
    """Records every request and answers from a script.

    Each script entry is a Response, an exception instance (raised), or a
    callable taking the call record and returning either.
    """

    def __init__(self, *script):
        self.script = list(script)
        self.calls = []

    def __call__(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        timeout=None,
        allow_redirects=True,
        **kwargs,
    ):
        self.calls.append(
            {
                "method": method,
                "url": url,
                "params": list(params or []),
                "data": data,
                "headers": dict(headers or {}),
                "timeout": timeout,
                "allow_redirects": allow_redirects,
                "extra": kwargs,
            }
        )
        if not self.script:
            raise AssertionError(f"unexpected request #{len(self.calls)}: {method} {params}")
        item = self.script.pop(0)
        if callable(item) and not isinstance(item, requests.Response):
            item = item(self.calls[-1])
        if isinstance(item, BaseException):
            raise item
        return item

    @property
    def chunks(self):
        return [c for c in self.calls if c["method"] == "PUT"]

    def ranges(self):
        return [c["headers"].get("Content-Range") for c in self.chunks]


def make_core(token=CANARY):
    core = CoreClient.__new__(CoreClient)
    core.env_url = "https://env.example.com/"
    core.access_token = token
    core.tool_call_timeout_s = 60
    return core


class NonSeekable(io.RawIOBase):
    """A binary stream with no size and no seek, recording every read size."""

    def __init__(self, payload, max_read=None):
        self._data = io.BytesIO(payload)
        self.read_sizes = []
        self._max_read = max_read

    def readable(self):
        return True

    def read(self, size=-1):
        self.read_sizes.append(size)
        if self._max_read is not None and size > self._max_read:
            size = self._max_read
        return self._data.read(size)


class UploadTestCase(unittest.TestCase):
    def setUp(self):
        self.core = make_core()
        tools = MagicMock()
        tools.core_client = self.core
        self.client = ActionClient(tools, MagicMock())
        self.sleeps = []
        self.random_value = 0.5
        for target, value in (
            ("_sleep", self.sleeps.append),
            ("_random", lambda: self.random_value),
        ):
            p = patch.object(ru, target, value)
            p.start()
            self.addCleanup(p.stop)

    def upload(self, fake, data=b"x", **kwargs):
        kwargs.setdefault("chunk_size", CHUNK)
        with patch("scalekit.actions._resumable_upload.requests.request", fake):
            return self.client.upload_resumable(
                kwargs.pop("connection_name", "googledrive"),
                kwargs.pop("identifier", "user_1"),
                kwargs.pop("path", "/upload/drive/v3/files"),
                data=data,
                **kwargs,
            )


class TestValidation(UploadTestCase):
    """Invalid input fails before any network call."""

    def assert_rejected(self, exc_type, data=b"x", **kwargs):
        fake = FakeTransport()
        with self.assertRaises(exc_type):
            self.upload(fake, data=data, **kwargs)
        self.assertEqual(fake.calls, [])

    def test_required_strings(self):
        self.assert_rejected(ValueError, connection_name="")
        self.assert_rejected(ValueError, identifier="")
        self.assert_rejected(ValueError, path="")
        self.assert_rejected(TypeError, identifier=None)

    def test_path_rejects_query_fragment_and_dot_segments(self):
        for path in (
            "/upload/drive/v3/files?uploadType=resumable",
            "/upload/drive/v3/files#x",
            "/upload/../drive/v3/files",
            "/upload/./drive",
            "..",
            "/upload/%2e%2e/drive",
            "/upload/drive/.",
        ):
            with self.subTest(path=path):
                self.assert_rejected(ValueError, path=path)

    def test_method(self):
        self.assert_rejected(ValueError, method="GET")
        self.assert_rejected(ValueError, method="DELETE")
        self.assert_rejected(TypeError, method=None)

    def test_chunk_size(self):
        for size in (0, -CHUNK, CHUNK + 1, 100):
            with self.subTest(size=size):
                self.assert_rejected(ValueError, chunk_size=size)
        self.assert_rejected(TypeError, chunk_size=True)
        self.assert_rejected(TypeError, chunk_size=float(CHUNK))

    def test_max_retries_timeout_total_bytes(self):
        self.assert_rejected(ValueError, max_retries=-1)
        self.assert_rejected(TypeError, max_retries=True)
        self.assert_rejected(ValueError, timeout=0)
        self.assert_rejected(ValueError, timeout=float("inf"))
        self.assert_rejected(ValueError, total_bytes=-1)
        self.assert_rejected(ValueError, data=b"abc", total_bytes=4)

    def test_content_type(self):
        self.assert_rejected(ValueError, content_type="")
        self.assert_rejected(ValueError, content_type="text/plain\r\nX-Evil: 1")

    def test_query_params(self):
        self.assert_rejected(ValueError, query_params={"uploadType": "multipart"})
        self.assert_rejected(TypeError, query_params={"fields": ["id"]})
        self.assert_rejected(TypeError, query_params=[("a", "b")])

    def test_metadata(self):
        self.assert_rejected(TypeError, metadata={"when": datetime.now(timezone.utc)})
        self.assert_rejected(TypeError, metadata=["name"])
        self.assert_rejected(ValueError, metadata={"n": float("nan")})

    def test_data_types(self):
        self.assert_rejected(TypeError, data="text")
        self.assert_rejected(TypeError, data=io.StringIO("text"))
        self.assert_rejected(TypeError, data=12345)

    def test_on_progress_must_be_callable(self):
        self.assert_rejected(TypeError, on_progress="nope")

    def test_seekable_stream_length_mismatch(self):
        self.assert_rejected(ValueError, data=io.BytesIO(b"abcd"), total_bytes=3)


class TestSessionStart(UploadTestCase):
    def test_start_request_shape(self):
        fake = FakeTransport(started(), done())
        result = self.upload(
            fake,
            data=b"hello",
            content_type="text/plain",
            metadata={"name": "hello.txt", "parents": ["f1"]},
            query_params={
                "supportsAllDrives": True,
                "keepRevisionForever": False,
                "n": 3,
                "part": "snippet,status",
            },
            path="upload/drive/v3/files",
        )
        self.assertEqual(result, {"id": "file-1", "name": "x"})
        start = fake.calls[0]
        self.assertEqual(start["method"], "POST")
        self.assertEqual(start["url"], "https://env.example.com/proxy/upload/drive/v3/files")
        self.assertEqual(
            start["params"],
            [
                ("uploadType", "resumable"),
                ("supportsAllDrives", "true"),
                ("keepRevisionForever", "false"),
                ("n", "3"),
                ("part", "snippet,status"),
            ],
        )
        h = start["headers"]
        self.assertEqual(h["X-Upload-Content-Type"], "text/plain")
        self.assertEqual(h["X-Upload-Content-Length"], "5")
        self.assertEqual(h["Content-Type"], "application/json; charset=UTF-8")
        self.assertEqual(h["identifier"], "user_1")
        self.assertEqual(h["Connection_name"], "googledrive")
        self.assertEqual(h["authorization"], f"Bearer {CANARY}")
        self.assertEqual(json.loads(start["data"]), {"name": "hello.txt", "parents": ["f1"]})
        self.assertFalse(start["allow_redirects"])
        self.assertEqual(start["timeout"], 60)
        for call in fake.calls:
            self.assertFalse(call["allow_redirects"])

    def test_no_metadata_means_no_body(self):
        fake = FakeTransport(started(), done())
        self.upload(fake, data=b"hello")
        self.assertIsNone(fake.calls[0]["data"])
        self.assertNotIn("Content-Type", fake.calls[0]["headers"])
        self.assertEqual(
            fake.calls[0]["headers"]["X-Upload-Content-Type"], "application/octet-stream"
        )

    def test_method_case_insensitive_and_timeout_override(self):
        fake = FakeTransport(started(), done())
        self.upload(fake, method="patch", timeout=12.5, path="/upload/drive/v3/files/abc")
        self.assertEqual(fake.calls[0]["method"], "PATCH")
        self.assertTrue(all(c["timeout"] == 12.5 for c in fake.calls))
        self.assertEqual(fake.calls[1]["method"], "PUT")

    def test_default_timeout_follows_client_tool_timeout(self):
        self.core.tool_call_timeout_s = 45
        fake = FakeTransport(started(), done())
        self.upload(fake)
        self.assertEqual(fake.calls[0]["timeout"], 45)

    def test_missing_location_is_protocol_error(self):
        for headers in ({}, {"Location": "https://www.googleapis.com/upload/drive/v3/files"}):
            with self.subTest(headers=headers):
                fake = FakeTransport(resp(200, headers))
                with self.assertRaises(ScalekitUploadProtocolException) as ctx:
                    self.upload(fake)
                self.assertNotIsInstance(ctx.exception, ScalekitUploadException)
                self.assertEqual(ctx.exception.status_code, 200)
                self.assertIsNone(ctx.exception.upload_id)

    def test_start_redirects_are_protocol_errors(self):
        for status in (308, 302, 301):
            with self.subTest(status=status):
                fake = FakeTransport(resp(status, {"Location": LOCATION}))
                with self.assertRaises(ScalekitUploadProtocolException):
                    self.upload(fake)
                self.assertEqual(len(fake.calls), 1)

    def test_start_failure_is_never_retried(self):
        fake = FakeTransport(resp(503, {"Retry-After": "1"}, "busy"))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake)
        self.assertEqual(len(fake.calls), 1)
        e = ctx.exception
        self.assertEqual(e.status_code, 503)
        self.assertEqual(e.body, "busy")
        self.assertIsNone(e.upload_id)
        self.assertEqual(e.bytes_committed, 0)
        self.assertNotIsInstance(e, ScalekitUploadSessionExpiredException)
        self.assertEqual(self.sleeps, [])

    def test_start_404_is_not_session_expired(self):
        fake = FakeTransport(resp(404, body={"error": {"code": 404}}))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake, method="PATCH", path="/upload/drive/v3/files/doesnotexist")
        self.assertNotIsInstance(ctx.exception, ScalekitUploadSessionExpiredException)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_start_timeout_not_retried_and_wrapped(self):
        fake = FakeTransport(requests.exceptions.ReadTimeout("slow"))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake)
        self.assertEqual(len(fake.calls), 1)
        self.assertIsNone(ctx.exception.status_code)
        self.assertIsInstance(ctx.exception.__cause__, requests.exceptions.Timeout)
        self.assertIn("timed out", str(ctx.exception))

    def test_start_connection_error_wrapped(self):
        fake = FakeTransport(requests.exceptions.ConnectionError("refused"))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake)
        self.assertIsInstance(ctx.exception.__cause__, requests.exceptions.ConnectionError)


class TestTokenRefresh(UploadTestCase):
    def refresh_to(self, new_token):
        calls = []

        def refresh():
            calls.append(1)
            self.core.access_token = new_token

        self.core._CoreClient__authenticate_client = refresh
        return calls

    def test_scalekit_401_refreshes_and_resends_once(self):
        refreshes = self.refresh_to("fresh-token")
        fake = FakeTransport(resp(401, body=SCALEKIT_401), started(), done())
        self.upload(fake)
        self.assertEqual(len(refreshes), 1)
        self.assertEqual(fake.calls[0]["headers"]["authorization"], f"Bearer {CANARY}")
        self.assertEqual(fake.calls[1]["headers"]["authorization"], "Bearer fresh-token")
        self.assertEqual(fake.calls[1]["method"], "POST")

    def test_scalekit_401_on_chunk_refreshes(self):
        refreshes = self.refresh_to("fresh-token")
        fake = FakeTransport(started(), resp(401, body=SCALEKIT_401), done())
        self.upload(fake)
        self.assertEqual(len(refreshes), 1)
        self.assertEqual(fake.ranges(), ["bytes 0-0/1", "bytes 0-0/1"])

    def test_second_401_is_not_resent_again(self):
        refreshes = self.refresh_to("fresh-token")
        fake = FakeTransport(resp(401, body=SCALEKIT_401), resp(401, body=SCALEKIT_401))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake)
        self.assertEqual(len(refreshes), 1)
        self.assertEqual(len(fake.calls), 2)
        self.assertEqual(ctx.exception.status_code, 401)

    def test_provider_401_is_not_refreshed(self):
        refreshes = self.refresh_to("fresh-token")
        for body in (
            {"error": {"code": 401, "message": "Invalid Credentials"}},
            {"detail": "x", "code": "UNAUTHORIZED", "extra": 1},
            {"detail": "x", "code": "FORBIDDEN"},
        ):
            with self.subTest(body=body):
                fake = FakeTransport(started(), resp(401, body=body))
                with self.assertRaises(ScalekitUploadException) as ctx:
                    self.upload(fake)
                self.assertEqual(ctx.exception.status_code, 401)
                self.assertEqual(len(fake.calls), 2)
        self.assertEqual(refreshes, [])

    def test_401_without_json_content_type_is_not_refreshed(self):
        refreshes = self.refresh_to("fresh-token")
        fake = FakeTransport(resp(401, {"Content-Type": "text/plain"}, json.dumps(SCALEKIT_401)))
        with self.assertRaises(ScalekitUploadException):
            self.upload(fake)
        self.assertEqual(refreshes, [])
        self.assertEqual(len(fake.calls), 1)

    def test_unchanged_token_is_not_resent(self):
        refreshes = self.refresh_to(CANARY)
        fake = FakeTransport(resp(401, body=SCALEKIT_401))
        with self.assertRaises(ScalekitUploadException):
            self.upload(fake)
        self.assertEqual(len(refreshes), 1)
        self.assertEqual(len(fake.calls), 1)

    def test_refresh_failure_raises_upload_exception(self):
        def refresh():
            raise ScalekitException("token endpoint down")

        self.core._CoreClient__authenticate_client = refresh
        fake = FakeTransport(resp(401, body=SCALEKIT_401))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIsInstance(ctx.exception.__cause__, ScalekitException)


class TestChunks(UploadTestCase):
    def test_three_chunks_known_size(self):
        payload = os.urandom(2 * CHUNK + 1000)
        progress = []
        fake = FakeTransport(
            started(), incomplete(CHUNK - 1), incomplete(2 * CHUNK - 1), resp(201, body={"id": "f"})
        )
        result = self.upload(
            fake, data=payload, content_type="video/mp4", on_progress=progress.append
        )
        self.assertEqual(result, {"id": "f"})
        total = len(payload)
        self.assertEqual(
            fake.ranges(),
            [
                f"bytes 0-{CHUNK - 1}/{total}",
                f"bytes {CHUNK}-{2 * CHUNK - 1}/{total}",
                f"bytes {2 * CHUNK}-{total - 1}/{total}",
            ],
        )
        self.assertEqual(b"".join(c["data"] for c in fake.chunks), payload)
        for call in fake.chunks:
            self.assertEqual(
                call["params"], [("uploadType", "resumable"), ("upload_id", UPLOAD_ID)]
            )
            self.assertEqual(call["headers"]["Content-Type"], "video/mp4")
            self.assertNotIn("X-Upload-Content-Type", call["headers"])
        self.assertEqual(
            progress,
            [
                UploadProgress(CHUNK, total),
                UploadProgress(2 * CHUNK, total),
                UploadProgress(total, total),
            ],
        )

    def test_progress_is_frozen(self):
        p = UploadProgress(1, 2)
        with self.assertRaises(AttributeError):
            p.bytes_committed = 5

    def test_query_params_not_repeated_on_chunks(self):
        fake = FakeTransport(started(), done())
        self.upload(fake, query_params={"supportsAllDrives": True})
        self.assertEqual(
            fake.chunks[0]["params"], [("uploadType", "resumable"), ("upload_id", UPLOAD_ID)]
        )

    def test_308_without_range_resends_from_zero(self):
        payload = os.urandom(CHUNK + 10)
        fake = FakeTransport(started(), incomplete(None), incomplete(CHUNK - 1), done())
        self.upload(fake, data=payload)
        self.assertEqual(
            fake.ranges(),
            [
                f"bytes 0-{CHUNK - 1}/{CHUNK + 10}",
                f"bytes 0-{CHUNK - 1}/{CHUNK + 10}",
                f"bytes {CHUNK}-{CHUNK + 9}/{CHUNK + 10}",
            ],
        )

    def test_partial_commit_resends_the_rest(self):
        payload = os.urandom(4 * CHUNK)
        fake = FakeTransport(started(), incomplete(CHUNK - 1), incomplete(3 * CHUNK - 1), done())
        self.upload(fake, data=payload, chunk_size=2 * CHUNK)
        total = 4 * CHUNK
        self.assertEqual(
            fake.ranges(),
            [
                f"bytes 0-{2 * CHUNK - 1}/{total}",
                f"bytes {CHUNK}-{3 * CHUNK - 1}/{total}",
                f"bytes {3 * CHUNK}-{total - 1}/{total}",
            ],
        )
        self.assertEqual(fake.chunks[1]["data"], payload[CHUNK : 3 * CHUNK])
        self.assertEqual(fake.chunks[2]["data"], payload[3 * CHUNK :])

    def test_unknown_total_uses_star_until_the_end(self):
        payload = os.urandom(2 * CHUNK + 7)
        progress = []
        fake = FakeTransport(started(), incomplete(CHUNK - 1), incomplete(2 * CHUNK - 1), done())
        self.upload(fake, data=NonSeekable(payload), on_progress=progress.append)
        total = len(payload)
        self.assertNotIn("X-Upload-Content-Length", fake.calls[0]["headers"])
        self.assertEqual(
            fake.ranges(),
            [
                f"bytes 0-{CHUNK - 1}/*",
                f"bytes {CHUNK}-{2 * CHUNK - 1}/*",
                f"bytes {2 * CHUNK}-{total - 1}/{total}",
            ],
        )
        self.assertEqual(
            progress,
            [
                UploadProgress(CHUNK, None),
                UploadProgress(2 * CHUNK, None),
                UploadProgress(total, total),
            ],
        )

    def test_unknown_total_exact_multiple_ends_with_total(self):
        payload = os.urandom(2 * CHUNK)
        fake = FakeTransport(started(), incomplete(CHUNK - 1), done())
        self.upload(fake, data=NonSeekable(payload))
        self.assertEqual(
            fake.ranges(),
            [
                f"bytes 0-{CHUNK - 1}/*",
                f"bytes {CHUNK}-{2 * CHUNK - 1}/{2 * CHUNK}",
            ],
        )

    def test_unknown_stream_fitting_one_chunk_sends_length(self):
        fake = FakeTransport(started(), done())
        self.upload(fake, data=NonSeekable(b"abc"))
        self.assertEqual(fake.calls[0]["headers"]["X-Upload-Content-Length"], "3")
        self.assertEqual(fake.ranges(), ["bytes 0-2/3"])

    def test_short_reads_are_assembled_into_full_chunks(self):
        payload = os.urandom(CHUNK + 5)
        fake = FakeTransport(started(), incomplete(CHUNK - 1), done())
        self.upload(fake, data=NonSeekable(payload, max_read=1000))
        self.assertEqual(len(fake.chunks[0]["data"]), CHUNK)

    def test_zero_length(self):
        for data in (b"", NonSeekable(b"")):
            with self.subTest(data=type(data).__name__):
                progress = []
                fake = FakeTransport(started(), done())
                self.upload(fake, data=data, on_progress=progress.append)
                self.assertEqual(fake.calls[0]["headers"]["X-Upload-Content-Length"], "0")
                self.assertEqual(fake.ranges(), ["bytes */0"])
                self.assertEqual(fake.chunks[0]["data"], b"")
                self.assertEqual(progress, [UploadProgress(0, 0)])

    def test_path_input_is_read_and_closed(self):
        payload = os.urandom(CHUNK + 3)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "f.bin"
            path.write_bytes(payload)
            opened = []
            real_open = open

            def spy_open(*args, **kwargs):
                handle = real_open(*args, **kwargs)
                opened.append(handle)
                return handle

            fake = FakeTransport(started(), incomplete(CHUNK - 1), done())
            with patch("builtins.open", spy_open):
                self.upload(fake, data=path)
        self.assertEqual(fake.calls[0]["headers"]["X-Upload-Content-Length"], str(len(payload)))
        self.assertEqual(b"".join(c["data"] for c in fake.chunks), payload)
        self.assertTrue(opened and all(h.closed for h in opened))

    def test_path_closed_on_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "f.bin"
            path.write_bytes(b"abc")
            opened = []
            real_open = open

            def spy_open(*args, **kwargs):
                handle = real_open(*args, **kwargs)
                opened.append(handle)
                return handle

            fake = FakeTransport(resp(500))
            with patch("builtins.open", spy_open), self.assertRaises(ScalekitUploadException):
                self.upload(fake, data=path)
        self.assertTrue(opened and all(h.closed for h in opened))

    def test_seekable_stream_reads_from_current_position(self):
        stream = io.BytesIO(b"0123456789abcdef")
        stream.seek(10)
        fake = FakeTransport(started(), done())
        self.upload(fake, data=stream)
        self.assertEqual(fake.calls[0]["headers"]["X-Upload-Content-Length"], "6")
        self.assertEqual(fake.chunks[0]["data"], b"abcdef")

    def test_memory_is_bounded_by_one_chunk(self):
        stream = NonSeekable(os.urandom(5 * CHUNK + 1))
        fake = FakeTransport(
            started(), *[incomplete((i + 1) * CHUNK - 1) for i in range(5)], done()
        )
        self.upload(fake, data=stream)
        self.assertTrue(stream.read_sizes)
        self.assertLessEqual(max(stream.read_sizes), CHUNK)
        self.assertTrue(all(len(c["data"]) <= CHUNK for c in fake.chunks))

    def test_declared_total_for_unsized_stream(self):
        fake = FakeTransport(started(), done())
        self.upload(fake, data=NonSeekable(b"abcd"), total_bytes=4)
        self.assertEqual(fake.calls[0]["headers"]["X-Upload-Content-Length"], "4")
        self.assertEqual(fake.ranges(), ["bytes 0-3/4"])

    def test_stream_shorter_than_total_bytes(self):
        payload = os.urandom(CHUNK + 10)
        fake = FakeTransport(started(), incomplete(CHUNK - 1))
        with self.assertRaises(ValueError):
            self.upload(fake, data=NonSeekable(payload), total_bytes=2 * CHUNK)
        # The short final chunk is never sent.
        self.assertEqual(len(fake.chunks), 1)

    def test_stream_longer_than_total_bytes(self):
        payload = os.urandom(CHUNK + 10)
        fake = FakeTransport(started(), incomplete(CHUNK - 1))
        with self.assertRaises(ValueError):
            self.upload(fake, data=NonSeekable(payload), total_bytes=CHUNK + 5)
        # Detected before the final chunk would have completed a truncated file.
        self.assertEqual(len(fake.chunks), 1)

    def test_stream_longer_than_total_bytes_within_first_chunk(self):
        fake = FakeTransport()
        with self.assertRaises(ValueError):
            self.upload(fake, data=NonSeekable(b"abcdef"), total_bytes=3)
        self.assertEqual(fake.calls, [])

    def test_stream_read_errors_propagate_unchanged(self):
        class Broken(io.RawIOBase):
            def readable(self):
                return True

            def read(self, size=-1):
                raise OSError("disk gone")

        with self.assertRaises(OSError):
            self.upload(FakeTransport(), data=Broken())

    def test_empty_final_body_returns_empty_dict(self):
        fake = FakeTransport(started(), resp(200, body=b""))
        self.assertEqual(self.upload(fake), {})

    def test_final_body_must_be_json_object(self):
        for body in (b"<html>", b"[1, 2]", b"\xff\xfe"):
            with self.subTest(body=body):
                fake = FakeTransport(started(), resp(200, body=body))
                with self.assertRaises(ScalekitUploadProtocolException) as ctx:
                    self.upload(fake)
                self.assertEqual(ctx.exception.upload_id, UPLOAD_ID)

    def test_completion_before_all_data_is_protocol_error(self):
        fake = FakeTransport(started(), done())
        with self.assertRaises(ScalekitUploadProtocolException):
            self.upload(fake, data=os.urandom(CHUNK + 1))

    def test_callback_exception_aborts(self):
        class StopUploadError(Exception):
            pass

        def on_progress(p):
            raise StopUploadError()

        fake = FakeTransport(started(), incomplete(CHUNK - 1))
        with self.assertRaises(StopUploadError):
            self.upload(fake, data=os.urandom(2 * CHUNK), on_progress=on_progress)
        self.assertEqual(len(fake.calls), 2)


class TestProtocolErrors(UploadTestCase):
    def test_offset_backwards(self):
        payload = os.urandom(3 * CHUNK)
        fake = FakeTransport(started(), incomplete(2 * CHUNK - 1), incomplete(CHUNK - 1))
        with self.assertRaises(ScalekitUploadProtocolException) as ctx:
            self.upload(fake, data=payload, chunk_size=2 * CHUNK)
        self.assertEqual(ctx.exception.bytes_committed, 2 * CHUNK)

    def test_missing_range_after_progress_is_backwards(self):
        fake = FakeTransport(started(), incomplete(CHUNK - 1), incomplete(None))
        with self.assertRaises(ScalekitUploadProtocolException):
            self.upload(fake, data=os.urandom(3 * CHUNK))

    def test_offset_past_bytes_sent(self):
        fake = FakeTransport(started(), incomplete(CHUNK))
        with self.assertRaises(ScalekitUploadProtocolException):
            self.upload(fake, data=os.urandom(2 * CHUNK))

    def test_malformed_range(self):
        for header in ("bytes=5-10", "bytes 0-10", "0-10", "bytes=0-"):
            with self.subTest(header=header):
                fake = FakeTransport(started(), resp(308, {"Range": header}))
                with self.assertRaises(ScalekitUploadProtocolException):
                    self.upload(fake, data=os.urandom(2 * CHUNK))

    def test_other_redirect_on_chunk(self):
        fake = FakeTransport(started(), resp(302, {"Location": "https://elsewhere.example"}))
        with self.assertRaises(ScalekitUploadProtocolException) as ctx:
            self.upload(fake)
        self.assertEqual(ctx.exception.status_code, 302)

    def test_no_progress_308_gives_up_after_max_retries(self):
        fake = FakeTransport(started(), incomplete(None), incomplete(None), incomplete(None))
        with self.assertRaises(ScalekitUploadProtocolException):
            self.upload(fake, data=os.urandom(2 * CHUNK), max_retries=2)
        self.assertEqual(len(fake.chunks), 3)


class TestRetries(UploadTestCase):
    def test_503_then_status_query_then_resume(self):
        payload = os.urandom(2 * CHUNK + 5)
        total = len(payload)
        fake = FakeTransport(
            started(),
            incomplete(CHUNK - 1),
            resp(503, {"Retry-After": "7"}),
            incomplete(CHUNK + 1000 - 1),  # status query: part of chunk 2 stored
            done(),
        )
        progress = []
        self.upload(fake, data=payload, on_progress=progress.append)
        self.assertEqual(
            fake.ranges(),
            [
                f"bytes 0-{CHUNK - 1}/{total}",
                f"bytes {CHUNK}-{2 * CHUNK - 1}/{total}",
                f"bytes */{total}",
                f"bytes {CHUNK + 1000}-{total - 1}/{total}",
            ],
        )
        self.assertEqual(fake.chunks[2]["data"], b"")
        self.assertNotIn("Content-Type", fake.chunks[2]["headers"])
        self.assertEqual(fake.chunks[3]["data"], payload[CHUNK + 1000 :])
        self.assertEqual(self.sleeps, [7.0])
        self.assertIn(UploadProgress(CHUNK + 1000, total), progress)

    def test_status_query_uses_star_when_total_unknown(self):
        fake = FakeTransport(
            started(),
            resp(500),
            incomplete(None),
            incomplete(CHUNK - 1),
            incomplete(2 * CHUNK - 1),
            done(),
        )
        self.upload(fake, data=NonSeekable(os.urandom(2 * CHUNK + 1)))
        self.assertEqual(fake.ranges()[1], "bytes */*")
        self.assertEqual(fake.ranges()[-1], f"bytes {2 * CHUNK}-{2 * CHUNK}/{2 * CHUNK + 1}")

    def test_timeout_then_query_reports_complete(self):
        fake = FakeTransport(
            started(), requests.exceptions.ReadTimeout("slow"), resp(201, body={"id": "f"})
        )
        progress = []
        result = self.upload(fake, data=b"abc", on_progress=progress.append)
        self.assertEqual(result, {"id": "f"})
        self.assertEqual(fake.ranges(), ["bytes 0-2/3", "bytes */3"])
        self.assertEqual(progress, [UploadProgress(3, 3)])

    def test_connection_error_is_retried(self):
        fake = FakeTransport(
            started(), requests.exceptions.ConnectionError("reset"), incomplete(None), done()
        )
        self.upload(fake, data=b"abc")
        self.assertEqual(fake.ranges(), ["bytes 0-2/3", "bytes */3", "bytes 0-2/3"])

    def test_first_backoff_delay_ceiling_is_base(self):
        self.random_value = 0.5
        fake = FakeTransport(started(), resp(500), resp(500), resp(500), incomplete(None), done())
        self.upload(fake, data=b"abc")
        # Full jitter: random() * min(1 s * 2**n, 30 s), n starting at 0.
        self.assertEqual(self.sleeps, [0.5, 1.0, 2.0])

    def test_backoff_caps_at_30s(self):
        self.random_value = 0.999
        self.assertAlmostEqual(ru._retry_delay(10, None), 0.999 * 30)

    def test_retry_after_variants(self):
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        with patch.object(ru, "_now", lambda: now):
            cases = [
                (429, "120", 30.0),
                (503, "-5", 0.0),
                (429, format_datetime(now + timedelta(seconds=12), usegmt=True), 12.0),
                (429, format_datetime(now - timedelta(seconds=12), usegmt=True), 0.0),
                (503, "soon", 0.5),  # unparseable: backoff (random 0.5 * 1 s)
                (500, "9", 0.5),  # only 429 and 503 honour Retry-After
                (502, None, 0.5),
            ]
            for status, header, expected in cases:
                with self.subTest(status=status, header=header):
                    headers = {"Retry-After": header} if header is not None else {}
                    self.assertAlmostEqual(ru._retry_delay(0, resp(status, headers)), expected)

    def test_exhausted_retries_raise_last_error(self):
        fake = FakeTransport(started(), resp(503), resp(503), resp(504, body="gateway"))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake, data=b"abc", max_retries=2)
        e = ctx.exception
        self.assertEqual(e.status_code, 504)
        self.assertEqual(e.body, "gateway")
        self.assertEqual(e.upload_id, UPLOAD_ID)
        self.assertEqual(len(fake.chunks), 3)
        self.assertEqual(len(self.sleeps), 2)

    def test_exhausted_after_timeouts_keeps_cause(self):
        fake = FakeTransport(
            started(), requests.exceptions.ReadTimeout("a"), requests.exceptions.ReadTimeout("b")
        )
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake, data=b"abc", max_retries=1)
        self.assertIsNone(ctx.exception.status_code)
        self.assertIsInstance(ctx.exception.__cause__, requests.exceptions.Timeout)

    def test_max_retries_zero_fails_on_first_error(self):
        fake = FakeTransport(started(), resp(503))
        with self.assertRaises(ScalekitUploadException):
            self.upload(fake, data=b"abc", max_retries=0)
        self.assertEqual(len(fake.chunks), 1)
        self.assertEqual(self.sleeps, [])

    def test_counter_resets_when_offset_advances(self):
        payload = os.urandom(3 * CHUNK)
        fake = FakeTransport(
            started(),
            resp(503),
            incomplete(CHUNK - 1),  # failure 1, then progress
            resp(503),
            incomplete(2 * CHUNK - 1),  # failure 1 again, then progress
            resp(503),
            done(),  # failure 1 again, query says done
        )
        result = self.upload(fake, data=payload, max_retries=1)
        self.assertEqual(result, {"id": "file-1", "name": "x"})
        self.assertEqual(len(self.sleeps), 3)

    def test_session_expired_on_chunk_and_query(self):
        for script in (
            [started(), incomplete(CHUNK - 1), resp(404)],
            [started(), incomplete(CHUNK - 1), resp(410)],
            [started(), incomplete(CHUNK - 1), resp(503), resp(404)],
        ):
            with self.subTest(statuses=[r.status_code for r in script]):
                fake = FakeTransport(*script)
                with self.assertRaises(ScalekitUploadSessionExpiredException) as ctx:
                    self.upload(fake, data=os.urandom(2 * CHUNK))
                self.assertIsInstance(ctx.exception, ScalekitUploadException)
                self.assertEqual(ctx.exception.upload_id, UPLOAD_ID)
                self.assertEqual(ctx.exception.bytes_committed, CHUNK)
                # Never restarts a new session on its own.
                self.assertEqual(sum(1 for c in fake.calls if c["method"] == "POST"), 1)

    def test_other_4xx_fails_immediately_with_details(self):
        fake = FakeTransport(started(), resp(403, {"X-Reason": "quota"}, {"error": "forbidden"}))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake, data=b"abc")
        e = ctx.exception
        self.assertNotIsInstance(e, ScalekitUploadSessionExpiredException)
        self.assertEqual(e.status_code, 403)
        self.assertEqual(e.headers["X-Reason"], "quota")
        self.assertEqual(e.headers["x-reason"], "quota")
        self.assertEqual(json.loads(e.body), {"error": "forbidden"})
        self.assertEqual(e.upload_id, UPLOAD_ID)
        self.assertEqual(e.bytes_committed, 0)
        self.assertEqual(self.sleeps, [])
        self.assertIn("403", str(e))
        self.assertIn(UPLOAD_ID, str(e))


class TestRedaction(UploadTestCase):
    def test_token_never_in_errors_or_logs(self):
        scripts = [
            [resp(500, body="server error")],
            [started(), resp(403, body="denied")],
            [started(), resp(503), resp(503)],
            [
                started(),
                requests.exceptions.ReadTimeout(f"timeout with {CANARY}?"),
                requests.exceptions.ReadTimeout("again"),
            ],
            [resp(200)],
        ]
        logger = logging.getLogger("scalekit")
        with self.assertLogs(logger, level=logging.DEBUG) as logs:
            logger.debug("start")
            for script in scripts:
                with self.subTest(script=script), self.assertRaises(ScalekitException) as ctx:
                    self.upload(FakeTransport(*script), data=b"abc", max_retries=1)
                e = ctx.exception
                text = " ".join([str(e), repr(e), str(e.headers), str(e.body)])
                self.assertNotIn(CANARY, text)
        self.assertNotIn(CANARY, "\n".join(logs.output))
        self.assertTrue(any("retry 1 of 1" in line for line in logs.output))


class TestEdgeCases(UploadTestCase):
    """Retry classification, single-flight refresh, stream bounds and redaction."""

    # a 2xx other than 200/201 on a chunk is an HTTP error
    def test_unexpected_2xx_on_chunk_is_upload_exception(self):
        for status in (202, 204):
            with self.subTest(status=status):
                self.sleeps.clear()
                fake = FakeTransport(started(), resp(status))
                with self.assertRaises(ScalekitUploadException) as ctx:
                    self.upload(fake, data=b"abc")
                self.assertEqual(ctx.exception.status_code, status)
                self.assertEqual(len(fake.chunks), 1)
                self.assertEqual(self.sleeps, [])

    # single-flight refresh across threads sharing one client
    def test_concurrent_scalekit_401_refreshes_once(self):
        threads_count = 8
        barrier = threading.Barrier(threads_count, timeout=10)
        refresh_lock = threading.Lock()
        refreshes = []

        def refresh():
            with refresh_lock:
                refreshes.append(1)
            time.sleep(0.05)
            self.core.access_token = ROTATED

        self.core._CoreClient__authenticate_client = refresh

        def transport(method, url, params=None, data=None, headers=None, **kwargs):
            if headers["authorization"] == f"Bearer {CANARY}":
                barrier.wait()  # every thread holds a 401 before anyone refreshes
                return resp(401, body=SCALEKIT_401)
            return started() if method == "POST" else done()

        results, errors = [], []

        def worker():
            try:
                results.append(
                    self.client.upload_resumable(
                        "googledrive", "user_1", "/upload/drive/v3/files", data=b"abc"
                    )
                )
            except ScalekitException as exc:
                errors.append(exc)

        with patch("scalekit.actions._resumable_upload.requests.request", transport):
            workers = [threading.Thread(target=worker) for _ in range(threads_count)]
            for w in workers:
                w.start()
            for w in workers:
                w.join(timeout=20)
        self.assertEqual(errors, [])
        self.assertEqual(len(results), threads_count)
        self.assertEqual(len(refreshes), 1)

    def test_token_already_changed_by_another_caller_is_not_refreshed(self):
        refreshes = []
        self.core._CoreClient__authenticate_client = lambda: refreshes.append(1)

        def rotated_while_in_flight(call):
            self.core.access_token = ROTATED
            return resp(401, body=SCALEKIT_401)

        fake = FakeTransport(rotated_while_in_flight, started(), done())
        self.upload(fake)
        self.assertEqual(refreshes, [])
        starts = [c for c in fake.calls if c["method"] == "POST"]
        self.assertEqual(len(starts), 2)
        self.assertEqual(starts[0]["headers"]["authorization"], f"Bearer {CANARY}")
        self.assertEqual(starts[1]["headers"]["authorization"], f"Bearer {ROTATED}")

    # non-retryable transport errors
    def test_non_retryable_transport_error_on_chunk(self):
        fake = FakeTransport(started(), requests.exceptions.TooManyRedirects("loop"))
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.upload(fake, data=b"abc")
        self.assertIsNone(ctx.exception.status_code)
        self.assertIsInstance(ctx.exception.__cause__, requests.exceptions.TooManyRedirects)
        self.assertEqual(len(fake.chunks), 1)
        self.assertEqual(self.sleeps, [])

    def test_chunked_encoding_error_is_retried_with_status_query(self):
        fake = FakeTransport(
            started(), requests.exceptions.ChunkedEncodingError("cut"), resp(201, body={"id": "f"})
        )
        self.assertEqual(self.upload(fake, data=b"abc"), {"id": "f"})
        self.assertEqual(fake.ranges(), ["bytes 0-2/3", "bytes */3"])
        self.assertEqual(len(self.sleeps), 1)

    def test_every_retryable_status_triggers_status_query_and_resume(self):
        for status in (408, 429, 500, 502, 503, 504):
            with self.subTest(status=status):
                self.sleeps.clear()
                fake = FakeTransport(started(), resp(status), incomplete(None), done())
                self.upload(fake, data=b"abc")
                self.assertEqual(fake.ranges(), ["bytes 0-2/3", "bytes */3", "bytes 0-2/3"])
                self.assertEqual(len(self.sleeps), 1)

    # a stream returning more than asked must not produce oversized chunks
    def test_stream_that_over_returns_keeps_chunks_bounded(self):
        class IgnoresSize(io.RawIOBase):
            def __init__(self, payload):
                self._data = io.BytesIO(payload)

            def readable(self):
                return True

            def read(self, size=-1):
                return self._data.read()  # returns everything left, whatever size is

        payload = os.urandom(3 * CHUNK + 5)
        total = len(payload)
        fake = FakeTransport(
            started(),
            incomplete(CHUNK - 1),
            incomplete(2 * CHUNK - 1),
            incomplete(3 * CHUNK - 1),
            done(),
        )
        self.upload(fake, data=IgnoresSize(payload))
        self.assertTrue(all(len(c["data"]) <= CHUNK for c in fake.chunks))
        self.assertEqual(b"".join(c["data"] for c in fake.chunks), payload)
        self.assertEqual(
            fake.ranges(),
            [
                f"bytes 0-{CHUNK - 1}/*",
                f"bytes {CHUNK}-{2 * CHUNK - 1}/*",
                f"bytes {2 * CHUNK}-{3 * CHUNK - 1}/*",
                f"bytes {3 * CHUNK}-{total - 1}/{total}",
            ],
        )

    # header values are checked locally
    def test_line_breaks_in_connection_name_or_identifier(self):
        for kwargs in (
            {"connection_name": "googledrive\r\nX-Evil: 1"},
            {"identifier": "user\n1"},
        ):
            with self.subTest(**kwargs):
                fake = FakeTransport()
                with self.assertRaises(ValueError):
                    self.upload(fake, **kwargs)
                self.assertEqual(fake.calls, [])

    # the requests error kept as __cause__ must not carry the Authorization header
    def test_cause_chain_carries_no_token(self):
        def prepared():
            return requests.Request(
                "PUT",
                "https://env.example.com/proxy/x",
                headers={"authorization": f"Bearer {CANARY}"},
            ).prepare()

        def redirect_error():
            r = resp(302)
            r.request = prepared()
            return requests.exceptions.TooManyRedirects("loop", response=r)

        cases = [
            [requests.exceptions.ReadTimeout("slow", request=prepared())],
            [started(), redirect_error()],
            [
                started(),
                requests.exceptions.ConnectionError("reset", request=prepared()),
                requests.exceptions.ConnectionError("reset", request=prepared()),
            ],
        ]
        for script in cases:
            with self.subTest(script=script):
                with self.assertRaises(ScalekitUploadException) as ctx:
                    self.upload(FakeTransport(*script), data=b"abc", max_retries=1)
                cause = ctx.exception.__cause__
                self.assertIsInstance(cause, requests.RequestException)
                self.assertIsNone(cause.request)
                dumped = [repr(cause), repr(cause.args), repr(vars(cause))]
                if cause.response is not None:
                    self.assertIsNone(cause.response.request)
                    dumped.append(repr(vars(cause.response)))
                self.assertNotIn(CANARY, " ".join(dumped))


class TestExports(unittest.TestCase):
    def test_public_names(self):
        import scalekit.actions.types as types
        import scalekit.common.exceptions as exc

        self.assertIs(types.UploadProgress, UploadProgress)
        self.assertIn("UploadProgress", types.__all__)
        self.assertTrue(
            issubclass(exc.ScalekitUploadSessionExpiredException, exc.ScalekitUploadException)
        )
        self.assertTrue(issubclass(exc.ScalekitUploadException, exc.ScalekitException))
        self.assertTrue(issubclass(exc.ScalekitUploadProtocolException, exc.ScalekitException))
        self.assertFalse(
            issubclass(exc.ScalekitUploadProtocolException, exc.ScalekitUploadException)
        )


if __name__ == "__main__":
    unittest.main()

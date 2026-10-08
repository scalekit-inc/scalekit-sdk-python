"""Live tests for ActionClient.upload_resumable against Google Drive through the proxy.

Skipped unless these are set (tests/.env is loaded like BaseTest does):
  SCALEKIT_ENV_URL, SCALEKIT_CLIENT_ID, SCALEKIT_CLIENT_SECRET
  TEST_AGENTKIT_UPLOAD_IDENTIFIER   identifier of a connected Google Drive account
  TEST_AGENTKIT_UPLOAD_CONNECTION   connection name (default "googledrive")

Every file is named sdk-parity-python-<run>-* and deleted afterwards. Untitled
files created during the run (left behind when the provider creates a file but
the response is lost) are swept as well.
"""

import io
import os
import unittest
import uuid
from datetime import datetime, timedelta, timezone

from scalekit import ScalekitClient
from scalekit.actions.types import UploadProgress
from scalekit.common.exceptions import (
    ScalekitUploadException,
    ScalekitUploadSessionExpiredException,
)

try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:  # pragma: no cover - dotenv is a dev dependency
    pass

KIB = 1024
CHUNK = 256 * KIB


class NonSeekableStream(io.RawIOBase):
    """A binary stream whose size the SDK cannot determine."""

    def __init__(self, payload):
        self._data = io.BytesIO(payload)

    def readable(self):
        return True

    def read(self, size=-1):
        return self._data.read(size)


def _env(name, default=None):
    value = os.environ.get(name, default)
    return value or None


class TestResumableUploadLive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env_url = _env("SCALEKIT_ENV_URL") or _env("SCALEKIT_ENVIRONMENT_URL")
        client_id = _env("SCALEKIT_CLIENT_ID")
        client_secret = _env("SCALEKIT_CLIENT_SECRET")
        cls.identifier = _env("TEST_AGENTKIT_UPLOAD_IDENTIFIER")
        cls.connection = _env("TEST_AGENTKIT_UPLOAD_CONNECTION", "googledrive")
        missing = [
            name
            for name, value in (
                ("SCALEKIT_ENV_URL", env_url),
                ("SCALEKIT_CLIENT_ID", client_id),
                ("SCALEKIT_CLIENT_SECRET", client_secret),
                ("TEST_AGENTKIT_UPLOAD_IDENTIFIER", cls.identifier),
            )
            if not value
        ]
        if missing:
            raise unittest.SkipTest(f"live upload tests need {', '.join(missing)}")
        cls.client = ScalekitClient(env_url, client_id, client_secret)
        cls.actions = cls.client.actions
        cls.run_id = uuid.uuid4().hex[:10]
        cls.prefix = f"sdk-parity-python-{cls.run_id}"
        # Small margin for clock skew between this machine and the provider.
        cls.started_at = datetime.now(timezone.utc) - timedelta(seconds=30)

    @classmethod
    def tearDownClass(cls):
        if not hasattr(cls, "actions"):
            return
        since = cls.started_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        for query in (
            f"name contains '{cls.prefix}' and trashed = false",
            f"name = 'Untitled' and createdTime > '{since}' and trashed = false",
        ):
            for file_id in cls._find(query):
                cls._delete(file_id)

    # -- Drive helpers (through the plain proxy request) ---------------------

    @classmethod
    def _find(cls, query):
        response = cls.actions.request(
            cls.connection,
            cls.identifier,
            "/drive/v3/files",
            query_params={"q": query, "fields": "files(id)", "pageSize": 100},
        )
        if response.status_code != 200:
            return []
        return [f["id"] for f in response.json().get("files", [])]

    @classmethod
    def _delete(cls, file_id):
        cls.actions.request(cls.connection, cls.identifier, f"/drive/v3/files/{file_id}", "DELETE")

    def _metadata(self, file_id):
        response = self.actions.request(
            self.connection,
            self.identifier,
            f"/drive/v3/files/{file_id}",
            query_params={"fields": "id,name,size"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def _upload(self, suffix, data, **kwargs):
        name = f"{self.prefix}-{suffix}"
        kwargs.setdefault("metadata", {"name": name})
        result = self.actions.upload_resumable(
            self.connection,
            self.identifier,
            kwargs.pop("path", "/upload/drive/v3/files"),
            data=data,
            **kwargs,
        )
        self.assertIn("id", result)
        self.addCleanup(self._delete, result["id"])
        return result

    # -- the shared live set ---------------------------------------------------

    def test_known_size_in_256_kib_chunks(self):
        payload = os.urandom(600 * KIB)
        progress = []
        result = self._upload(
            "known.bin",
            payload,
            content_type="application/octet-stream",
            chunk_size=CHUNK,
            on_progress=progress.append,
        )
        total = len(payload)
        self.assertEqual(progress[0], UploadProgress(CHUNK, total))
        self.assertEqual(progress[-1], UploadProgress(total, total))
        committed = [p.bytes_committed for p in progress]
        self.assertEqual(committed, sorted(committed))
        self.assertEqual(int(self._metadata(result["id"])["size"]), total)

    def test_non_seekable_stream_of_unknown_size(self):
        payload = os.urandom(700_000)
        progress = []
        result = self._upload(
            "stream.bin",
            NonSeekableStream(payload),
            chunk_size=CHUNK,
            on_progress=progress.append,
        )
        self.assertIsNone(progress[0].total_bytes)
        self.assertEqual(progress[-1], UploadProgress(len(payload), len(payload)))
        self.assertEqual(int(self._metadata(result["id"])["size"]), len(payload))

    def test_zero_bytes(self):
        progress = []
        result = self._upload("empty.bin", b"", on_progress=progress.append)
        self.assertEqual(progress, [UploadProgress(0, 0)])
        self.assertEqual(int(self._metadata(result["id"]).get("size", "0")), 0)

    def test_patch_replaces_content(self):
        created = self._upload("replace.bin", b"first version")
        replacement = os.urandom(300 * KIB)
        result = self.actions.upload_resumable(
            self.connection,
            self.identifier,
            f"/upload/drive/v3/files/{created['id']}",
            data=replacement,
            method="PATCH",
            chunk_size=CHUNK,
        )
        self.assertEqual(result["id"], created["id"])
        self.assertEqual(int(self._metadata(created["id"])["size"]), len(replacement))

    def test_patch_unknown_file_raises_404(self):
        with self.assertRaises(ScalekitUploadException) as ctx:
            self.actions.upload_resumable(
                self.connection,
                self.identifier,
                "/upload/drive/v3/files/doesnotexist",
                data=b"never stored",
                method="PATCH",
            )
        # The session never started, so this is not a session-expired error.
        self.assertNotIsInstance(ctx.exception, ScalekitUploadSessionExpiredException)
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertIsNone(ctx.exception.upload_id)


if __name__ == "__main__":
    unittest.main()

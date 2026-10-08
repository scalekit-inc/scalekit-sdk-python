"""Google resumable uploads through the Scalekit proxy.

Private module: callers use ``ActionClient.upload_resumable``. The protocol is
Google's resumable upload protocol (Drive v3, the Cloud Storage JSON API,
YouTube Data API): one request starts a session, then the content is sent in
``PUT`` chunks to the same proxy path with the session's ``upload_id``.
"""

from __future__ import annotations

import io
import json
import logging
import os
import random
import re
import stat
import threading
import time
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import IO, Any, Protocol, Union
from urllib.parse import parse_qs, unquote, urlsplit

import requests

from scalekit.actions.models.upload_progress import UploadProgress
from scalekit.common.exceptions import (
    ScalekitException,
    ScalekitUploadException,
    ScalekitUploadProtocolException,
    ScalekitUploadSessionExpiredException,
    _ScalekitUploadErrorBase,
)
from scalekit.core import (
    DEFAULT_TOOL_CALL_TIMEOUT_S,
    RETRY_BACKOFF_BASE_S,
    RETRY_BACKOFF_MAX_S,
    _assert_valid_timeout,
)

logger = logging.getLogger("scalekit.actions")

# Google requires every chunk except the last to be a multiple of 256 KiB.
CHUNK_GRANULARITY = 256 * 1024
# Upper bound on a server-provided Retry-After, the same as the backoff cap.
RETRY_AFTER_CAP_S = RETRY_BACKOFF_MAX_S

_ALLOWED_METHODS = frozenset({"POST", "PATCH", "PUT"})
_COMPLETE_STATUSES = frozenset({200, 201})
_RESUME_INCOMPLETE = 308
_SESSION_GONE_STATUSES = frozenset({404, 410})
_RETRYABLE_STATUSES = frozenset({408, 429, 500, 502, 503, 504})
_RETRY_AFTER_STATUSES = frozenset({429, 503})
_RANGE_RE = re.compile(r"bytes=0-(\d+)")
_DELTA_SECONDS_RE = re.compile(r"-?\d+")

# A Scalekit-issued 401 is refreshed and resent once. The lock makes the
# refresh single-flight across threads that share one client. The refresh
# itself is CoreClient's private token fetch, the same one ActionClient.request
# uses.
_REFRESH_LOCK = threading.Lock()
_CORE_REFRESH_METHOD = "_CoreClient__authenticate_client"


def _system_now() -> datetime:
    return datetime.now(timezone.utc)


# Indirections so tests can control time and jitter.
_sleep: Callable[[float], None] = time.sleep
_random: Callable[[], float] = random.random
_now: Callable[[], datetime] = _system_now

UploadData = Union[bytes, bytearray, memoryview, IO[bytes], "os.PathLike[str]"]
ProgressCallback = Callable[[UploadProgress], None]
_Reader = Callable[[int], bytes]


class _Core(Protocol):
    """The parts of ``CoreClient`` this module uses."""

    env_url: str
    access_token: str | None

    def get_headers(self, headers: dict[str, str] | None = None) -> dict[str, str]: ...


def _drop_prepared_request(exc: requests.RequestException) -> None:
    """Detach the sent request (and its Authorization header) from a requests error.

    The error is kept as ``__cause__`` of the SDK exception, and error trackers
    serialise the cause chain, so it must not carry the Scalekit access token.
    """
    try:
        exc.request = None
        response = exc.response
        if response is not None:
            response.request = None  # type: ignore[assignment]
    except AttributeError:
        pass


class _TransportError(Exception):
    """No HTTP response: a timeout, a connection failure or another requests error."""

    def __init__(self, original: requests.RequestException, *, retryable: bool) -> None:
        super().__init__(type(original).__name__)
        _drop_prepared_request(original)
        self.original = original
        self.retryable = retryable
        if isinstance(original, requests.exceptions.Timeout):
            self.description = "timed out"
        elif retryable:
            self.description = "failed to connect or was interrupted"
        else:
            self.description = f"failed ({type(original).__name__})"


# --------------------------------------------------------------------------
# Validation (runs before any network call)
# --------------------------------------------------------------------------


def _require_text(name: str, value: object) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str; got {type(value).__name__}.")
    if not value:
        raise ValueError(f"{name} is required.")
    return value


def _require_int(name: str, value: object, *, minimum: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int; got {type(value).__name__}.")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}; got {value}.")
    return value


def _normalize_path(path: object) -> str:
    text = _require_text("path", path)
    if "?" in text or "#" in text:
        raise ValueError(
            "path must not contain '?' or '#'. Pass query parameters in query_params, "
            f"for example query_params={{'supportsAllDrives': True}}; got {text!r}."
        )
    if not text.startswith("/"):
        text = "/" + text
    if any(segment in (".", "..") for segment in unquote(text).split("/")):
        raise ValueError(f"path must not contain '.' or '..' segments; got {text!r}.")
    return text


def _normalize_method(method: object) -> str:
    text = _require_text("method", method).upper()
    if text not in _ALLOWED_METHODS:
        raise ValueError(f"method must be 'POST', 'PATCH' or 'PUT'; got {method!r}.")
    return text


def _require_header_value(name: str, value: object) -> str:
    """A non-empty str that can be sent as an HTTP header value."""
    text = _require_text(name, value)
    if "\r" in text or "\n" in text:
        raise ValueError(f"{name} must not contain line breaks.")
    return text


def _normalize_content_type(content_type: object) -> str:
    return _require_header_value("content_type", content_type)


def _normalize_chunk_size(chunk_size: object) -> int:
    value = _require_int("chunk_size", chunk_size, minimum=1)
    if value % CHUNK_GRANULARITY:
        raise ValueError(
            f"chunk_size must be a positive multiple of {CHUNK_GRANULARITY} bytes (256 KiB); "
            f"got {value}."
        )
    return value


def _encode_query_params(query_params: object) -> list[tuple[str, str]]:
    if query_params is None:
        return []
    if not isinstance(query_params, Mapping):
        raise TypeError(f"query_params must be a mapping; got {type(query_params).__name__}.")
    encoded: list[tuple[str, str]] = []
    for key, value in query_params.items():
        name = _require_text("query_params key", key)
        if name == "uploadType":
            raise ValueError(
                "query_params must not set 'uploadType': the SDK always sends uploadType=resumable."
            )
        if isinstance(value, bool):
            text = "true" if value else "false"
        elif isinstance(value, (str, int)):
            text = str(value)
        else:
            raise TypeError(
                f"query_params[{name!r}] must be a str, int or bool; got {type(value).__name__}."
            )
        encoded.append((name, text))
    return encoded


def _encode_metadata(metadata: object) -> bytes | None:
    if metadata is None:
        return None
    if not isinstance(metadata, Mapping):
        raise TypeError(
            f"metadata must be a mapping (a JSON object); got {type(metadata).__name__}."
        )
    try:
        text = json.dumps(dict(metadata), allow_nan=False)
    except ValueError as exc:
        raise ValueError(f"metadata cannot be encoded as JSON: {exc}") from exc
    return text.encode("utf-8")


def _check_data_type(data: object) -> None:
    if isinstance(data, str):
        raise TypeError(
            "data is a str. Pass bytes (for example text.encode('utf-8')), a binary file "
            "object, or a path as pathlib.Path."
        )
    if isinstance(data, (bytes, bytearray, memoryview, os.PathLike)):
        return
    if isinstance(data, io.TextIOBase):
        raise TypeError("data is a text stream. Open the file in binary mode ('rb').")
    if not callable(getattr(data, "read", None)):
        raise TypeError(
            "data must be bytes, bytearray, memoryview, a binary file object or an "
            f"os.PathLike path; got {type(data).__name__}."
        )


# --------------------------------------------------------------------------
# Reading the content
# --------------------------------------------------------------------------


def _check_declared_total(total_bytes: int | None, size: int) -> None:
    if total_bytes is not None and total_bytes != size:
        raise ValueError(f"total_bytes is {total_bytes}, but data has {size} bytes.")


def _memory_reader(view: memoryview) -> _Reader:
    position = 0

    def read(size: int) -> bytes:
        nonlocal position
        chunk = view[position : position + size].tobytes()
        position += len(chunk)
        return chunk

    return read


def _stream_reader(stream: IO[bytes]) -> _Reader:
    def read(size: int) -> bytes:
        chunk: object = stream.read(size)
        if isinstance(chunk, bytes):
            return chunk
        if isinstance(chunk, (bytearray, memoryview)):
            return bytes(chunk)
        if isinstance(chunk, str):
            raise TypeError("data returned str. Open the file in binary mode ('rb').")
        if chunk is None:
            raise TypeError("data returned None. Non-blocking streams are not supported.")
        raise TypeError(f"data.read() returned {type(chunk).__name__}, expected bytes.")

    return read


def _remaining_size(stream: IO[bytes]) -> int | None:
    """Bytes left from the current position of a seekable stream, else None."""
    seekable = getattr(stream, "seekable", None)
    try:
        if not callable(seekable) or not seekable():
            return None
        position = stream.tell()
        end = stream.seek(0, os.SEEK_END)
        stream.seek(position)
    except OSError:
        return None
    return max(end - position, 0)


@contextmanager
def _open_data(data: UploadData, total_bytes: int | None) -> Iterator[tuple[_Reader, int | None]]:
    """Yield a reader for ``data`` and its total size when known."""
    if isinstance(data, (bytes, bytearray, memoryview)):
        view = memoryview(data).cast("B")
        _check_declared_total(total_bytes, view.nbytes)
        yield _memory_reader(view), view.nbytes
        return
    if isinstance(data, os.PathLike):
        with open(data, "rb") as handle:
            info = os.fstat(handle.fileno())
            size = info.st_size if stat.S_ISREG(info.st_mode) else None
            if size is not None:
                _check_declared_total(total_bytes, size)
            yield _stream_reader(handle), size if size is not None else total_bytes
        return
    size = _remaining_size(data)
    if size is not None:
        _check_declared_total(total_bytes, size)
    yield _stream_reader(data), size if size is not None else total_bytes


class _Source:
    """Reads the content in order, with a one-byte lookahead to detect its end."""

    def __init__(self, reader: _Reader) -> None:
        self._read = reader
        self._lookahead = b""
        self._exhausted = False

    def read(self, size: int) -> bytes:
        """Read up to ``size`` bytes; fewer only at the end of the content."""
        parts: list[bytes] = []
        needed = size
        if self._lookahead and needed > 0:
            # Never hand out more than asked for, even when a stream returned
            # more than it was asked for earlier: chunks must not exceed chunk_size.
            taken, self._lookahead = self._lookahead[:needed], self._lookahead[needed:]
            parts.append(taken)
            needed -= len(taken)
        while needed > 0 and not self._exhausted:
            chunk = self._read(needed)
            if not chunk:
                self._exhausted = True
                break
            if len(chunk) > needed:
                self._lookahead = chunk[needed:]
                chunk = chunk[:needed]
            parts.append(chunk)
            needed -= len(chunk)
        return b"".join(parts)

    def at_end(self) -> bool:
        """Whether no byte is left, reading at most one byte ahead to find out."""
        if self._lookahead:
            return False
        if self._exhausted:
            return True
        self._lookahead = self._read(1)
        if not self._lookahead:
            self._exhausted = True
            return True
        return False


# --------------------------------------------------------------------------
# Response parsing
# --------------------------------------------------------------------------


def _parse_upload_id(location: str | None) -> str | None:
    if not location:
        return None
    values = parse_qs(urlsplit(location).query).get("upload_id")
    if not values or not values[0]:
        return None
    return values[0]


def _parse_retry_after(value: str | None) -> float | None:
    """Seconds to wait from a Retry-After header; None when absent or unparseable."""
    if value is None:
        return None
    text = value.strip()
    if _DELTA_SECONDS_RE.fullmatch(text):
        return max(float(int(text)), 0.0)
    try:
        when = parsedate_to_datetime(text)
    except (TypeError, ValueError, IndexError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max((when - _now()).total_seconds(), 0.0)


def _retry_delay(attempt: int, response: requests.Response | None) -> float:
    """Delay before retry number ``attempt + 1`` (``attempt`` starts at 0)."""
    if response is not None and response.status_code in _RETRY_AFTER_STATUSES:
        retry_after = _parse_retry_after(response.headers.get("Retry-After"))
        if retry_after is not None:
            return min(retry_after, RETRY_AFTER_CAP_S)
    ceiling: float = min(RETRY_BACKOFF_BASE_S * (2**attempt), RETRY_BACKOFF_MAX_S)
    return _random() * ceiling


def _is_scalekit_unauthorized(response: requests.Response) -> bool:
    """A 401 issued by Scalekit itself, as opposed to one from the provider."""
    content_type = response.headers.get("Content-Type", "")
    if content_type.split(";", 1)[0].strip().lower() != "application/json":
        return False
    try:
        payload = json.loads(response.content)
    except ValueError:
        return False
    return (
        isinstance(payload, dict)
        and set(payload) == {"detail", "code"}
        and payload["code"] == "UNAUTHORIZED"
    )


def _response_text(response: requests.Response) -> str:
    return response.content.decode("utf-8", errors="replace")


# --------------------------------------------------------------------------
# The upload
# --------------------------------------------------------------------------


class _ResumableUpload:
    def __init__(
        self,
        core: _Core,
        *,
        connection_name: str,
        identifier: str,
        path: str,
        method: str,
        reader: _Reader,
        total: int | None,
        content_type: str,
        metadata_body: bytes | None,
        query: list[tuple[str, str]],
        chunk_size: int,
        max_retries: int,
        timeout: float,
        on_progress: ProgressCallback | None,
    ) -> None:
        self._core = core
        self._url = core.env_url.rstrip("/") + "/proxy" + path
        # The same proxy headers as ActionClient.request.
        self._proxy_headers = {
            "connection_name": connection_name,
            "Connection_name": connection_name,
            "identifier": identifier,
        }
        self._method = method
        self._source = _Source(reader)
        self._total = total
        self._content_type = content_type
        self._metadata_body = metadata_body
        self._query = query
        self._chunk_size = chunk_size
        self._max_retries = max_retries
        self._timeout = timeout
        self._on_progress = on_progress
        self._upload_id: str | None = None
        # The chunk not yet committed. _start is always the committed offset.
        self._buffer = b""
        self._start = 0
        self._final = False

    def run(self) -> dict[str, Any]:
        # Read the first chunk before starting the session, so content that
        # fits in one chunk gets X-Upload-Content-Length.
        self._fill()
        upload_id = self._start_session()
        return self._send_chunks(upload_id)

    # -- transport ---------------------------------------------------------

    def _request_once(
        self,
        method: str,
        params: list[tuple[str, str]],
        headers: dict[str, str],
        body: bytes | None,
    ) -> requests.Response:
        try:
            return requests.request(
                method=method,
                url=self._url,
                params=params,
                data=body,
                headers=self._core.get_headers({**self._proxy_headers, **headers}),
                timeout=self._timeout,
                allow_redirects=False,
            )
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ChunkedEncodingError,
        ) as exc:
            raise _TransportError(exc, retryable=True) from exc
        except requests.exceptions.RequestException as exc:
            raise _TransportError(exc, retryable=False) from exc

    def _send(
        self,
        method: str,
        params: list[tuple[str, str]],
        headers: dict[str, str],
        body: bytes | None,
        phase: str,
    ) -> requests.Response:
        """Send once; resend once after a token refresh for a Scalekit-issued 401."""
        token_used = self._core.access_token
        response = self._request_once(method, params, headers, body)
        if response.status_code != 401 or not _is_scalekit_unauthorized(response):
            return response
        try:
            refreshed = self._refresh_token(token_used)
        except (ScalekitException, ValueError, KeyError) as exc:
            raise self._http_error(
                ScalekitUploadException,
                response,
                f"The Scalekit access token could not be refreshed after HTTP 401 on the {phase}.",
            ) from exc
        if not refreshed:
            return response
        return self._request_once(method, params, headers, body)

    def _refresh_token(self, token_used: str | None) -> bool:
        """Refresh the token unless another thread already did; True when it changed."""
        with _REFRESH_LOCK:
            if self._core.access_token == token_used:
                refresh: Callable[[], None] = getattr(self._core, _CORE_REFRESH_METHOD)
                refresh()
            return self._core.access_token != token_used

    # -- errors ------------------------------------------------------------

    def _where(self) -> str:
        details = f"bytes_committed={self._start}"
        if self._upload_id is not None:
            details = f"upload_id={self._upload_id}, {details}"
        return details

    def _http_error(
        self,
        cls: type[_ScalekitUploadErrorBase],
        response: requests.Response,
        message: str,
    ) -> _ScalekitUploadErrorBase:
        return cls(
            f"{message} ({self._where()})",
            status_code=response.status_code,
            headers=dict(response.headers),
            body=_response_text(response),
            upload_id=self._upload_id,
            bytes_committed=self._start,
        )

    def _transport_error(self, exc: _TransportError, phase: str) -> ScalekitUploadException:
        return ScalekitUploadException(
            f"The {phase} {exc.description} ({self._where()})",
            upload_id=self._upload_id,
            bytes_committed=self._start,
        )

    # -- session start -----------------------------------------------------

    def _start_session(self) -> str:
        headers = {"X-Upload-Content-Type": self._content_type}
        if self._total is not None:
            headers["X-Upload-Content-Length"] = str(self._total)
        if self._metadata_body is not None:
            headers["Content-Type"] = "application/json; charset=UTF-8"
        params = [("uploadType", "resumable"), *self._query]
        phase = "session-start request"
        # Never retried: a second start request would open a second session.
        try:
            response = self._send(self._method, params, headers, self._metadata_body, phase)
        except _TransportError as exc:
            raise self._transport_error(exc, phase) from exc.original
        status = response.status_code
        if 200 <= status < 300:
            upload_id = _parse_upload_id(response.headers.get("Location"))
            if upload_id is None:
                raise self._http_error(
                    ScalekitUploadProtocolException,
                    response,
                    f"The session-start response (HTTP {status}) has no upload_id in its "
                    "Location header. Check that the path is a resumable upload endpoint.",
                )
            self._upload_id = upload_id
            return upload_id
        if 300 <= status < 400:
            raise self._http_error(
                ScalekitUploadProtocolException,
                response,
                f"The session-start request returned an unexpected redirect (HTTP {status}).",
            )
        raise self._http_error(
            ScalekitUploadException,
            response,
            f"The session-start request failed with HTTP {status}.",
        )

    # -- chunks ------------------------------------------------------------

    def _fill(self) -> None:
        """Top the buffer up to one chunk, and find out whether it ends the content."""
        if self._final:
            return
        position = self._start + len(self._buffer)
        wanted = self._chunk_size - len(self._buffer)
        if self._total is not None:
            wanted = min(wanted, self._total - position)
        data = self._source.read(wanted) if wanted > 0 else b""
        self._buffer += data
        position += len(data)
        if self._total is not None:
            if len(data) < wanted:
                raise ValueError(
                    f"data ended after {position} bytes, but total_bytes is {self._total}."
                )
            if position == self._total:
                if not self._source.at_end():
                    raise ValueError(f"data is longer than total_bytes ({self._total}).")
                self._final = True
        elif len(data) < wanted or self._source.at_end():
            self._final = True
            self._total = position

    def _report(self, committed: int, total: int | None) -> None:
        if self._on_progress is not None:
            self._on_progress(UploadProgress(bytes_committed=committed, total_bytes=total))

    def _back_off(
        self,
        failures: int,
        error: _ScalekitUploadErrorBase,
        cause: BaseException | None,
        response: requests.Response | None,
        reason: str,
    ) -> int:
        """Count one failure; raise ``error`` once retries are used up, else sleep."""
        failures += 1
        if failures > self._max_retries:
            raise error from cause
        delay = _retry_delay(failures - 1, response)
        logger.info(
            "Resumable upload: %s at offset %d; retry %d of %d in %.2fs",
            reason,
            self._start,
            failures,
            self._max_retries,
            delay,
        )
        _sleep(delay)
        return failures

    def _committed_from(self, response: requests.Response) -> int:
        header = response.headers.get("Range")
        if header is None:
            committed = 0
        else:
            match = _RANGE_RE.fullmatch(header.strip())
            if match is None:
                raise self._http_error(
                    ScalekitUploadProtocolException,
                    response,
                    f"The server sent a malformed Range header: {header!r}.",
                )
            committed = int(match.group(1)) + 1
        sent_end = self._start + len(self._buffer)
        if committed < self._start or committed > sent_end:
            raise self._http_error(
                ScalekitUploadProtocolException,
                response,
                f"The server reported {committed} bytes committed, outside the expected "
                f"range {self._start}-{sent_end}.",
            )
        return committed

    def _complete(self, response: requests.Response) -> dict[str, Any]:
        if not self._final or self._total is None:
            raise self._http_error(
                ScalekitUploadProtocolException,
                response,
                f"The server reported the upload complete (HTTP {response.status_code}) "
                "before all data was sent.",
            )
        raw = response.content
        result: object = {}
        if raw.strip():
            try:
                result = json.loads(raw)
            except ValueError as exc:
                raise self._http_error(
                    ScalekitUploadProtocolException,
                    response,
                    "The final upload response is not JSON.",
                ) from exc
        if not isinstance(result, dict):
            raise self._http_error(
                ScalekitUploadProtocolException,
                response,
                "The final upload response is not a JSON object.",
            )
        self._start = self._total
        self._buffer = b""
        self._report(self._total, self._total)
        return result

    def _send_chunks(self, upload_id: str) -> dict[str, Any]:
        params = [("uploadType", "resumable"), ("upload_id", upload_id)]
        failures = 0
        query = False
        while True:
            total_text = str(self._total) if self._total is not None else "*"
            headers: dict[str, str]
            if query or not self._buffer:
                # A status query, or the closing request once every byte is committed
                # (and the only request of a zero-length upload).
                phase = "status query" if query else "final upload request"
                body = b""
                headers = {"Content-Range": f"bytes */{total_text}"}
            else:
                phase = "chunk upload"
                body = self._buffer
                last = self._start + len(body) - 1
                headers = {
                    "Content-Range": f"bytes {self._start}-{last}/{total_text}",
                    "Content-Type": self._content_type,
                }
            try:
                response = self._send("PUT", params, headers, body, phase)
            except _TransportError as exc:
                if not exc.retryable:
                    raise self._transport_error(exc, phase) from exc.original
                failures = self._back_off(
                    failures,
                    self._transport_error(exc, phase),
                    exc.original,
                    None,
                    f"{phase} {exc.description}",
                )
                query = True
                continue

            status = response.status_code
            if status in _COMPLETE_STATUSES:
                return self._complete(response)
            if status == _RESUME_INCOMPLETE:
                committed = self._committed_from(response)
                if committed > self._start:
                    self._buffer = self._buffer[committed - self._start :]
                    self._start = committed
                    failures = 0
                    query = False
                    self._report(committed, self._total)
                    self._fill()
                    continue
                if query:
                    # The status query says where to resume; resend from there.
                    query = False
                    continue
                failures = self._back_off(
                    failures,
                    self._http_error(
                        ScalekitUploadProtocolException,
                        response,
                        "The server kept accepting chunks without storing any data.",
                    ),
                    None,
                    None,
                    "no data committed",
                )
                continue
            if status in _SESSION_GONE_STATUSES:
                raise self._http_error(
                    ScalekitUploadSessionExpiredException,
                    response,
                    f"The upload session expired or no longer exists (HTTP {status} on the "
                    f"{phase}). Start a new upload.",
                )
            if status in _RETRYABLE_STATUSES:
                failures = self._back_off(
                    failures,
                    self._http_error(
                        ScalekitUploadException,
                        response,
                        f"The {phase} failed with HTTP {status} after {self._max_retries} retries.",
                    ),
                    None,
                    response,
                    f"HTTP {status} on the {phase}",
                )
                query = True
                continue
            if 300 <= status < 400:
                raise self._http_error(
                    ScalekitUploadProtocolException,
                    response,
                    f"The {phase} returned an unexpected redirect (HTTP {status}).",
                )
            raise self._http_error(
                ScalekitUploadException,
                response,
                f"The {phase} failed with HTTP {status}.",
            )


def upload_resumable(
    core: _Core,
    *,
    connection_name: str,
    identifier: str,
    path: str,
    data: UploadData,
    total_bytes: int | None,
    content_type: str,
    metadata: Mapping[str, object] | None,
    method: str,
    query_params: Mapping[str, str | int | bool] | None,
    chunk_size: int,
    max_retries: int,
    timeout: float | None,
    on_progress: ProgressCallback | None,
) -> dict[str, Any]:
    """Validate the arguments, then run the upload. See ``ActionClient.upload_resumable``."""
    _require_header_value("connection_name", connection_name)
    _require_header_value("identifier", identifier)
    normalized_path = _normalize_path(path)
    normalized_method = _normalize_method(method)
    normalized_content_type = _normalize_content_type(content_type)
    normalized_chunk_size = _normalize_chunk_size(chunk_size)
    _require_int("max_retries", max_retries, minimum=0)
    if total_bytes is not None:
        _require_int("total_bytes", total_bytes, minimum=0)
    if timeout is None:
        timeout = getattr(core, "tool_call_timeout_s", DEFAULT_TOOL_CALL_TIMEOUT_S)
    _assert_valid_timeout("timeout", timeout)
    query = _encode_query_params(query_params)
    metadata_body = _encode_metadata(metadata)
    if on_progress is not None and not callable(on_progress):
        raise TypeError("on_progress must be callable.")
    _check_data_type(data)

    with _open_data(data, total_bytes) as (reader, total):
        upload = _ResumableUpload(
            core,
            connection_name=connection_name,
            identifier=identifier,
            path=normalized_path,
            method=normalized_method,
            reader=reader,
            total=total,
            content_type=normalized_content_type,
            metadata_body=metadata_body,
            query=query,
            chunk_size=normalized_chunk_size,
            max_retries=max_retries,
            timeout=float(timeout),
            on_progress=on_progress,
        )
        return upload.run()

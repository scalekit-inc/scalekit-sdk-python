"""
Tests for UNAVAILABLE retry-with-backoff and the removal of the blind
"retry every other gRPC code" catch-all in CoreClient.grpc_exec.

Background: before this fix, any grpc.RpcError that wasn't TOOL_ERROR,
UNAUTHENTICATED, or RESOURCE_EXHAUSTED was retried immediately with zero
backoff, regardless of status code (UNAVAILABLE, ABORTED, DEADLINE_EXCEEDED,
INTERNAL, ...). That's dangerous for codes like ABORTED/DEADLINE_EXCEEDED,
which can mean the request already reached and was processed by the server —
blindly retrying risks double-executing a non-idempotent call. This mirrors
the Node SDK's policy: only UNAVAILABLE (always pre-send in this transport
config) gets a backoff retry; UNAUTHENTICATED gets an immediate re-auth
retry; everything else surfaces immediately.

These tests never touch the network or real time.sleep — grpc.RpcError is
faked directly and time.sleep is patched out.
"""
import unittest
from unittest.mock import patch

import grpc
from grpc import StatusCode

from scalekit.core import RETRY_BACKOFF_BASE_S, RETRY_BACKOFF_MAX_S


def _make_rpc_error(status_code: StatusCode):
    class _FakeRpcError(grpc.RpcError):
        def code(self):
            return status_code

        def trailing_metadata(self):
            return None

        def details(self):
            return "error"

    return _FakeRpcError()


def _make_core_client():
    from scalekit.core import CoreClient, DEFAULT_CALL_TIMEOUT_S, DEFAULT_TOOL_CALL_TIMEOUT_S
    client = CoreClient.__new__(CoreClient)
    client.access_token = "test-token"
    client.host = "example.com"
    client.env_url = "https://example.com"
    client.client_id = "cid"
    client.client_secret = "csec"
    client.keys = {}
    client.grpc_secure_channel = None
    client.call_timeout_s = DEFAULT_CALL_TIMEOUT_S
    client.tool_call_timeout_s = DEFAULT_TOOL_CALL_TIMEOUT_S
    return client


class TestUnavailableBackoffRetry(unittest.TestCase):
    def setUp(self):
        self.client = _make_core_client()

    def _always_raise(self, status_code):
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise _make_rpc_error(status_code)

        return func, call_count

    @patch("scalekit.core.time.sleep")
    def test_unavailable_retries_with_backoff_then_succeeds(self, mock_sleep):
        """UNAVAILABLE must be retried, and each retry must sleep first."""
        success_response = object()
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            if call_count[0] < 3:
                raise _make_rpc_error(StatusCode.UNAVAILABLE)
            return success_response

        result = self.client.grpc_exec(func, data=None, retry=2)

        self.assertIs(result, success_response)
        self.assertEqual(call_count[0], 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("scalekit.core.time.sleep")
    def test_unavailable_backoff_is_bounded_and_jittered(self, mock_sleep):
        """Each backoff sleep must fall within [0.5x, 1.0x] of the exponential base, capped."""
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(StatusCode.UNAVAILABLE)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=3)

        self.assertEqual(call_count[0], 4)  # initial + 3 retries
        self.assertEqual(mock_sleep.call_count, 3)
        for attempt, (args, _kwargs) in enumerate(mock_sleep.call_args_list):
            delay = args[0]
            base = min(RETRY_BACKOFF_BASE_S * 2 ** attempt, RETRY_BACKOFF_MAX_S)
            self.assertGreaterEqual(delay, base * 0.5)
            self.assertLessEqual(delay, base * 1.0)

    @patch("scalekit.core.time.sleep")
    def test_unavailable_exhausts_retries_then_raises(self, mock_sleep):
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(StatusCode.UNAVAILABLE)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 3)  # initial + 2 retries

    @patch("scalekit.core.time.sleep")
    def test_aborted_surfaces_immediately_no_retry(self, mock_sleep):
        """ABORTED can mean the request already reached the server — must not
        be retried blindly (double-execution risk for non-idempotent calls)."""
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(StatusCode.ABORTED)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 1)
        mock_sleep.assert_not_called()

    @patch("scalekit.core.time.sleep")
    def test_deadline_exceeded_surfaces_immediately_no_retry(self, mock_sleep):
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(StatusCode.DEADLINE_EXCEEDED)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 1)
        mock_sleep.assert_not_called()

    @patch("scalekit.core.time.sleep")
    def test_internal_surfaces_immediately_no_retry(self, mock_sleep):
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(StatusCode.INTERNAL)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 1)
        mock_sleep.assert_not_called()


class TestExceptionNoneStatusGuard(unittest.TestCase):
    """rpc_status.from_call(error) returns None for any transport-level failure
    with no trailing google.rpc.Status (e.g. a raw connection reset/timeout
    that never reached a real server response) — constructing the exception
    meant to describe that failure must not itself crash."""

    @patch("scalekit.common.exceptions.rpc_status.from_call", return_value=None)
    def test_none_status_falls_back_to_str_error_without_crashing(self, _mock_from_call):
        from scalekit.common.exceptions import ScalekitServerException
        rpc_err = _make_rpc_error(StatusCode.UNAVAILABLE)

        exc = ScalekitServerException(rpc_err)

        self.assertEqual(exc._err_details, [])
        self.assertIsInstance(exc._message, str)


if __name__ == "__main__":
    unittest.main()

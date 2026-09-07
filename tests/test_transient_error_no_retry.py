"""
Tests for CoreClient.grpc_exec's retry policy: UNAUTHENTICATED is the only
gRPC code that auto-retries. Everything else — UNAVAILABLE, ABORTED,
DEADLINE_EXCEEDED, INTERNAL, CANCELLED, ... — surfaces immediately.

Background: before this fix, any grpc.RpcError that wasn't TOOL_ERROR,
UNAUTHENTICATED, or RESOURCE_EXHAUSTED was retried immediately with zero
backoff, regardless of status code. An earlier iteration of this fix added a
backoff retry specifically for UNAVAILABLE (mirroring the Node SDK), but that
was dropped: UNAVAILABLE isn't reliably pre-send in this SDK's keepalive
config (keepalive_time_ms/tool_call_timeout_s both default to 60s, so a
long-running call can cross a keepalive ping boundary mid-flight and surface
UNAVAILABLE even though the server already processed the request) — and with
no per-RPC idempotency classification to tell a safe call from an unsafe one
(e.g. execute_tool sending an email), the only call that's unconditionally
safe to auto-retry is UNAUTHENTICATED, which is rejected before it ever
touches business logic. A caller who wants resilience against a transient
blip on a read/idempotent call is expected to retry at their own layer.

These tests never touch the network — grpc.RpcError is faked directly.
"""
import unittest
from unittest.mock import MagicMock, patch

import grpc
from grpc import StatusCode


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


class TestNoRetryOnTransientErrors(unittest.TestCase):
    def setUp(self):
        self.client = _make_core_client()

    def _always_raise(self, status_code):
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise _make_rpc_error(status_code)

        return func, call_count

    def _assert_surfaces_immediately(self, status_code):
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(status_code)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 1)

    def test_unavailable_surfaces_immediately_no_retry(self):
        """UNAVAILABLE can mean the request already reached and was processed
        by the server (e.g. a keepalive ping timeout mid-call) — not
        retried, for any call."""
        self._assert_surfaces_immediately(StatusCode.UNAVAILABLE)

    def test_aborted_surfaces_immediately_no_retry(self):
        self._assert_surfaces_immediately(StatusCode.ABORTED)

    def test_deadline_exceeded_surfaces_immediately_no_retry(self):
        self._assert_surfaces_immediately(StatusCode.DEADLINE_EXCEEDED)

    def test_internal_surfaces_immediately_no_retry(self):
        self._assert_surfaces_immediately(StatusCode.INTERNAL)

    def test_cancelled_surfaces_immediately_no_retry(self):
        self._assert_surfaces_immediately(StatusCode.CANCELLED)

    def test_unauthenticated_still_triggers_reauth_and_retry(self):
        """UNAUTHENTICATED is the one exception: rejected before touching
        business logic, so there's nothing to double-execute."""
        success_response = object()
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            if call_count[0] == 1:
                raise _make_rpc_error(StatusCode.UNAUTHENTICATED)
            return success_response

        with patch.object(self.client, "_CoreClient__authenticate_client"):
            result = self.client.grpc_exec(func, data=None, retry=2)

        self.assertIs(result, success_response)
        self.assertEqual(call_count[0], 2)

    def test_unauthenticated_exhausts_retries_then_raises(self):
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(StatusCode.UNAUTHENTICATED)

        with patch.object(self.client, "_CoreClient__authenticate_client"):
            with self.assertRaises(ScalekitServerException):
                self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 3)  # initial + 2 retries

    def test_resource_exhausted_surfaces_immediately_no_retry(self):
        self._assert_surfaces_immediately(StatusCode.RESOURCE_EXHAUSTED)


class TestExecuteToolNoLongerNeedsSpecialCasing(unittest.TestCase):
    """execute_tool used to opt out of UNAVAILABLE retry explicitly. Now that
    nothing retries UNAVAILABLE, it needs no special casing — it behaves the
    same as every other call, including reads like list_tools."""

    def setUp(self):
        from scalekit.tools import ToolsClient
        self.core_client = _make_core_client()
        self.core_client.grpc_secure_channel = MagicMock()
        self.tools = ToolsClient(self.core_client)

    def test_execute_tool_does_not_pass_retry_kwargs(self):
        with patch.object(self.core_client, "grpc_exec", return_value="ok") as mock_exec:
            self.tools.execute_tool(tool_name="gmail_send_email", identifier="user@example.com")

        _, kwargs = mock_exec.call_args
        self.assertNotIn("retry_on_unavailable", kwargs)
        self.assertNotIn("retry", kwargs)


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

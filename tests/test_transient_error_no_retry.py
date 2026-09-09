"""
Tests for CoreClient.grpc_exec's retry policy.

UNAUTHENTICATED retries immediately (no backoff — a 401 isn't a signal the
backend is under load). UNAVAILABLE retries with jittered exponential
backoff by default (retry_on_unavailable=True). This is a NARROWING of the
released SDK's behavior, not a preservation of it: the released SDK retries
every status code not already special-cased (INVALID_ARGUMENT, NOT_FOUND,
ALREADY_EXISTS, PERMISSION_DENIED, all of it), immediately, no backoff —
narrowing to UNAVAILABLE-only is the largest user-visible change here.

Both SDKs now retry only a code spelled UNAVAILABLE/Unavailable, and the
backoff formula matches Node's exactly — but that's name-parity, not
behavior-parity, for the failure mode this ticket exists to fix: grpc-python
classifies a dead/reset connection as UNAVAILABLE, so this retry fires for
it; connect-node's own mapping surfaces that same reset as Code.Aborted, and
its retry check runs on that raw code before Aborted is re-keyed to
Unavailable for exception classification — so Node never actually retries
this scenario. See the UNAVAILABLE branch in grpc_exec for the verified
detail. A call site can opt out of the UNAVAILABLE retry via
retry_on_unavailable=False, e.g. ToolsClient.execute_tool, where a retry
risks double-executing a non-idempotent call (sending an email twice);
UNAUTHENTICATED's own retry is unaffected by this flag.

ABORTED, INTERNAL, CANCELLED, and DEADLINE_EXCEEDED never retry, regardless
of retry_on_unavailable (see TestNeverRetriedTransientCodes and
TestDeadlineExceededNeverRetries) — grpc_exec bounds each attempt, not the
total call across retries, so retrying an already-expired DEADLINE_EXCEEDED
multiplies worst-case latency instead of bounding it; ABORTED/INTERNAL/
CANCELLED are excluded on the same "might have already executed" reasoning
that scopes the retried set to UNAVAILABLE specifically.

These tests mock time.sleep to keep them fast/deterministic — the backoff
delay itself is exercised separately in TestTransientRetryBackoff.

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


class TestTransientRetryDefaultOn(unittest.TestCase):
    """Default (retry_on_unavailable=True): UNAVAILABLE retries until
    exhausted, with backoff (mocked here for speed — see
    TestTransientRetryBackoff for the actual delay behavior). Narrower than
    the released SDK's blanket retry-everything, not a preservation of it."""

    def setUp(self):
        self.client = _make_core_client()
        sleep_patcher = patch("scalekit.core.time.sleep")
        self.mock_sleep = sleep_patcher.start()
        self.addCleanup(sleep_patcher.stop)

    def _always_raise(self, status_code):
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise _make_rpc_error(status_code)

        return func, call_count

    def _assert_retries_until_exhausted(self, status_code, retry=2):
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(status_code)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=retry)

        self.assertEqual(call_count[0], retry + 1)  # initial + retries

    def test_unavailable_retries_until_exhausted(self):
        self._assert_retries_until_exhausted(StatusCode.UNAVAILABLE)

    def test_unauthenticated_retry_has_no_backoff_delay(self):
        """UNAUTHENTICATED's own retry is immediate — a 401 isn't a signal
        the backend is under load, unlike the transient-code path."""
        from scalekit.common.exceptions import ScalekitServerException
        func, _ = self._always_raise(StatusCode.UNAUTHENTICATED)
        with patch.object(self.client, "_CoreClient__authenticate_client"):
            with self.assertRaises(ScalekitServerException):
                self.client.grpc_exec(func, data=None, retry=2)

        self.mock_sleep.assert_not_called()

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
        """RESOURCE_EXHAUSTED (Scalekit rate-limits) never retries, unaffected
        by retry_on_unavailable — retrying would triple the damage."""
        from scalekit.common.exceptions import ScalekitServerException
        func, call_count = self._always_raise(StatusCode.RESOURCE_EXHAUSTED)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 1)

    def test_reauth_success_then_different_failure_surfaces_that_failure(self):
        """A successful token refresh must not mask what the retried call
        itself failed with. Regression test: the retry used to be wrapped in
        the same try/except as the refresh call, so a retry that failed for
        an unrelated reason (e.g. DEADLINE_EXCEEDED) was reported as the
        original UNAUTHENTICATED/401 instead — actively misleading, since the
        credentials were never the problem. DEADLINE_EXCEEDED never retries
        (see TestDeadlineExceededNeverRetries), so this also covers that the
        surfaced failure isn't itself silently retried away."""
        from scalekit.common.exceptions import ScalekitServerException
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            if call_count[0] == 1:
                raise _make_rpc_error(StatusCode.UNAUTHENTICATED)
            raise _make_rpc_error(StatusCode.DEADLINE_EXCEEDED)

        with patch.object(self.client, "_CoreClient__authenticate_client"):
            with self.assertRaises(ScalekitServerException) as ctx:
                self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 2)
        self.assertEqual(ctx.exception.grpc_status, StatusCode.DEADLINE_EXCEEDED)


class TestTransientRetryBackoff(unittest.TestCase):
    """The retry_on_unavailable path backs off (jittered exponential, matching
    the Node SDK's formula) rather than retrying instantly — on a backend
    returning UNAVAILABLE because it's overloaded, every client retrying at
    once just triples the load. random.random() is mocked to remove the
    jitter's randomness so the base backoff value is checkable exactly."""

    def setUp(self):
        self.client = _make_core_client()

    def test_backoff_doubles_each_attempt_up_to_the_cap(self):
        from scalekit.core import RETRY_BACKOFF_BASE_S, RETRY_BACKOFF_MAX_S

        def func(data, metadata, timeout=None):
            raise _make_rpc_error(StatusCode.UNAVAILABLE)

        with patch("scalekit.core.random.random", return_value=0.0), \
                patch("scalekit.core.time.sleep") as mock_sleep:
            from scalekit.common.exceptions import ScalekitServerException
            with self.assertRaises(ScalekitServerException):
                self.client.grpc_exec(func, data=None, retry=3)

        # random.random()=0.0 -> jitter factor is always the floor, 0.5x.
        expected = [
            min(RETRY_BACKOFF_BASE_S * (2 ** i), RETRY_BACKOFF_MAX_S) * 0.5
            for i in range(3)
        ]
        self.assertEqual([call.args[0] for call in mock_sleep.call_args_list], expected)

    def test_backoff_capped_at_max(self):
        """A high attempt count must not blow past RETRY_BACKOFF_MAX_S."""
        from scalekit.core import RETRY_BACKOFF_MAX_S

        def func(data, metadata, timeout=None):
            raise _make_rpc_error(StatusCode.UNAVAILABLE)

        with patch("scalekit.core.random.random", return_value=1.0), \
                patch("scalekit.core.time.sleep") as mock_sleep:
            from scalekit.common.exceptions import ScalekitServerException
            with self.assertRaises(ScalekitServerException):
                self.client.grpc_exec(func, data=None, retry=1, _attempt=20)

        # random.random()=1.0 -> jitter factor is always the ceiling, 1.0x,
        # so this asserts the cap directly with no jitter ambiguity.
        mock_sleep.assert_called_once_with(RETRY_BACKOFF_MAX_S)

    def test_backoff_not_applied_when_opted_out(self):
        def func(data, metadata, timeout=None):
            raise _make_rpc_error(StatusCode.UNAVAILABLE)

        with patch("scalekit.core.time.sleep") as mock_sleep:
            from scalekit.common.exceptions import ScalekitServerException
            with self.assertRaises(ScalekitServerException):
                self.client.grpc_exec(func, data=None, retry=2, retry_on_unavailable=False)

        mock_sleep.assert_not_called()


class TestTransientRetryOptOut(unittest.TestCase):
    """retry_on_unavailable=False (see ToolsClient.execute_tool): UNAVAILABLE
    surfaces immediately instead of retrying, but UNAUTHENTICATED still
    retries."""

    def setUp(self):
        self.client = _make_core_client()

    def test_unavailable_surfaces_immediately_when_opted_out(self):
        """UNAVAILABLE can mean the request already reached and was processed
        by the server (e.g. a keepalive ping timeout mid-call) — a call site
        that can't tolerate double-execution opts out via
        retry_on_unavailable=False."""
        from scalekit.common.exceptions import ScalekitServerException
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise _make_rpc_error(StatusCode.UNAVAILABLE)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2, retry_on_unavailable=False)

        self.assertEqual(call_count[0], 1)

    def test_unauthenticated_still_retries_when_opted_out(self):
        """retry_on_unavailable=False must not affect UNAUTHENTICATED's own
        retry — a 401 is rejected before touching business logic, so there's
        nothing to double-execute regardless of this flag."""
        success_response = object()
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            if call_count[0] == 1:
                raise _make_rpc_error(StatusCode.UNAUTHENTICATED)
            return success_response

        with patch.object(self.client, "_CoreClient__authenticate_client"):
            result = self.client.grpc_exec(func, data=None, retry=2, retry_on_unavailable=False)

        self.assertIs(result, success_response)
        self.assertEqual(call_count[0], 2)


class TestNeverRetriedTransientCodes(unittest.TestCase):
    """ABORTED/INTERNAL/CANCELLED never retry, regardless of
    retry_on_unavailable — the retried set is scoped to UNAVAILABLE
    specifically, matching the Node SDK's retry scope exactly (Node also
    retries only Code.Unavailable). Same "might have already executed"
    reasoning as UNAVAILABLE, just not extended to these codes."""

    def setUp(self):
        self.client = _make_core_client()

    def _assert_surfaces_immediately(self, status_code, **kwargs):
        from scalekit.common.exceptions import ScalekitServerException
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise _make_rpc_error(status_code)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2, **kwargs)

        self.assertEqual(call_count[0], 1)

    def test_aborted_never_retries(self):
        self._assert_surfaces_immediately(StatusCode.ABORTED, retry_on_unavailable=True)
        self._assert_surfaces_immediately(StatusCode.ABORTED, retry_on_unavailable=False)

    def test_internal_never_retries(self):
        self._assert_surfaces_immediately(StatusCode.INTERNAL, retry_on_unavailable=True)
        self._assert_surfaces_immediately(StatusCode.INTERNAL, retry_on_unavailable=False)

    def test_cancelled_never_retries(self):
        self._assert_surfaces_immediately(StatusCode.CANCELLED, retry_on_unavailable=True)
        self._assert_surfaces_immediately(StatusCode.CANCELLED, retry_on_unavailable=False)


class TestDeadlineExceededNeverRetries(unittest.TestCase):
    """DEADLINE_EXCEEDED never retries, regardless of retry_on_unavailable:
    grpc_exec passes the same `timeout` into every retry recursion, so it
    bounds each attempt, not the total call. Retrying an already-expired
    deadline with a fresh full-length window multiplies worst-case
    wall-clock time by (retry + 1) instead of bounding it — defeating the
    point of having a deadline. See the DEADLINE_EXCEEDED branch in
    grpc_exec for the full rationale."""

    def setUp(self):
        self.client = _make_core_client()

    def _assert_surfaces_immediately(self, **kwargs):
        from scalekit.common.exceptions import ScalekitServerException
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise _make_rpc_error(StatusCode.DEADLINE_EXCEEDED)

        with self.assertRaises(ScalekitServerException):
            self.client.grpc_exec(func, data=None, retry=2, **kwargs)

        self.assertEqual(call_count[0], 1)

    def test_deadline_exceeded_surfaces_immediately_with_retry_on_unavailable_true(self):
        self._assert_surfaces_immediately(retry_on_unavailable=True)

    def test_deadline_exceeded_surfaces_immediately_with_retry_on_unavailable_false(self):
        self._assert_surfaces_immediately(retry_on_unavailable=False)


class TestExecuteToolOptsOutOfTransientRetryKwarg(unittest.TestCase):
    """execute_tool opts out of the transient-code retry (retry_on_unavailable=
    False) since a retry there risks double-executing a non-idempotent call
    (e.g. sending an email twice). Reads like list_tools/list_scoped_tools
    keep the default (retry_on_unavailable=True)."""

    def setUp(self):
        from scalekit.tools import ToolsClient
        self.core_client = _make_core_client()
        self.core_client.grpc_secure_channel = MagicMock()
        self.tools = ToolsClient(self.core_client)

    def test_execute_tool_passes_retry_on_unavailable_false(self):
        with patch.object(self.core_client, "grpc_exec", return_value="ok") as mock_exec:
            self.tools.execute_tool(tool_name="gmail_send_email", identifier="user@example.com")

        _, kwargs = mock_exec.call_args
        self.assertIs(kwargs["retry_on_unavailable"], False)
        self.assertEqual(kwargs["timeout"], self.core_client.tool_call_timeout_s)

    def test_list_tools_uses_tool_call_timeout(self):
        with patch.object(self.core_client, "grpc_exec", return_value="ok") as mock_exec:
            self.tools.list_tools()

        _, kwargs = mock_exec.call_args
        self.assertEqual(kwargs["timeout"], self.core_client.tool_call_timeout_s)

    def test_list_scoped_tools_uses_tool_call_timeout(self):
        with patch.object(self.core_client, "grpc_exec", return_value="ok") as mock_exec:
            self.tools.list_scoped_tools(identifier="user@example.com")

        _, kwargs = mock_exec.call_args
        self.assertEqual(kwargs["timeout"], self.core_client.tool_call_timeout_s)

    def test_search_tools_uses_tool_call_timeout(self):
        with patch.object(self.core_client, "grpc_exec", return_value="ok") as mock_exec:
            self.tools.search_tools(query="send an email")

        _, kwargs = mock_exec.call_args
        self.assertEqual(kwargs["timeout"], self.core_client.tool_call_timeout_s)


class TestExceptionNoneStatusGuard(unittest.TestCase):
    """rpc_status.from_call(error) returns None for any transport-level failure
    with no trailing google.rpc.Status (e.g. a raw connection reset/timeout
    that never reached a real server response) — constructing the exception
    meant to describe that failure must not itself crash."""

    @patch("scalekit.common.exceptions.rpc_status.from_call", return_value=None)
    def test_none_status_falls_back_to_error_details_without_crashing(self, _mock_from_call):
        from scalekit.common.exceptions import ScalekitServerException
        rpc_err = _make_rpc_error(StatusCode.UNAVAILABLE)  # .details() -> "error"

        exc = ScalekitServerException(rpc_err)

        self.assertEqual(exc._err_details, [])
        # The real error text must actually be captured, not just "some string" —
        # and it must survive into str(exc), which is what a caller actually
        # sees in logs/tracebacks, not just the internal _message attribute.
        self.assertEqual(exc._message, "error")
        self.assertIn("error", str(exc))

    @patch("scalekit.common.exceptions.rpc_status.from_call", return_value=None)
    def test_cancelled_str_does_not_crash(self, _mock_from_call):
        """GRPC_TO_HTTP[CANCELLED] must be renderable via .name/.value like every
        other entry — regression test for the 499-as-a-bare-int crash."""
        from scalekit.common.exceptions import ScalekitServerException
        rpc_err = _make_rpc_error(StatusCode.CANCELLED)

        exc = ScalekitServerException(rpc_err)

        rendered = str(exc)
        self.assertIn("CLIENT_CLOSED_REQUEST", rendered)
        self.assertIn("499", rendered)

    @patch("scalekit.common.exceptions.rpc_status.from_call", side_effect=ValueError("inconsistent status"))
    def test_malformed_status_value_error_falls_back_without_crashing(self, _mock_from_call):
        """rpc_status.from_call raises ValueError (not just returning None) when
        grpc-status-details-bin is present but internally inconsistent with the
        call's own code/message — constructing the exception meant to describe
        that failure must not itself crash."""
        from scalekit.common.exceptions import ScalekitServerException
        rpc_err = _make_rpc_error(StatusCode.UNAVAILABLE)  # .details() -> "error"

        exc = ScalekitServerException(rpc_err)

        self.assertEqual(exc._err_details, [])
        self.assertEqual(exc._message, "error")
        self.assertIn("error", str(exc))

    def test_unmapped_grpc_status_falls_back_to_internal_server_error(self):
        """Every current StatusCode is mapped in GRPC_TO_HTTP, so this is latent
        today — but .get() must still carry a default, or a future/unmapped code
        gives http_status=None and __str__ crashes on None.name, the same shape
        as the CANCELLED-as-bare-int bug already fixed."""
        import scalekit.common.exceptions as exceptions_module
        from http import HTTPStatus

        rpc_err = _make_rpc_error(StatusCode.UNAVAILABLE)
        with patch.object(exceptions_module, "GRPC_TO_HTTP", {}):
            exc = exceptions_module.ScalekitServerException(rpc_err)

        self.assertEqual(exc.http_status, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn("INTERNAL_SERVER_ERROR", str(exc))


if __name__ == "__main__":
    unittest.main()

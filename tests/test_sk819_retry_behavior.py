"""
SK-819: Provider error handling tests.

Phase 1: Tests for CURRENT behavior (must pass before any changes).
Phase 2: Tests for NEW behavior (must fail before implementation, then pass after).
"""
import unittest
from unittest.mock import MagicMock, patch, call
import grpc
from grpc import StatusCode

from google.rpc import status_pb2
from google.protobuf import any_pb2

from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo, ToolErrorInfo
from scalekit.common.exceptions import (
    ScalekitServerException,
    ScalekitTooManyRequestsException,
    ScalekitUnauthorizedException,
    ScalekitForbiddenException,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_rpc_error(status_code: StatusCode, error_code: str = None,
                    tool_error_code: str = None, tool_error_message: str = None,
                    execution_id: str = None, message: str = "error"):
    """Build a mock grpc.RpcError with optional TOOL_ERROR details."""
    details = []
    if error_code is not None:
        tool_error_info = None
        if tool_error_code or tool_error_message or execution_id:
            tool_error_info = ToolErrorInfo(
                execution_id=execution_id or "",
                tool_error_message=tool_error_message or "",
                tool_error_code=tool_error_code or "",
            )
        kwargs = {"error_code": error_code}
        if tool_error_info:
            kwargs["tool_error_info"] = tool_error_info
        info = ErrorInfo(**kwargs)
        detail = any_pb2.Any()
        detail.Pack(info)
        details.append(detail)

    status = status_pb2.Status(
        code=status_code.value[0],
        message=message,
        details=details,
    )
    trailing = (("grpc-status-details-bin", status.SerializeToString()),)

    class _FakeRpcError(grpc.RpcError):
        def code(self):
            return status_code

        def trailing_metadata(self):
            return trailing

        def details(self):
            return message

    return _FakeRpcError()


def _make_core_client():
    """Return a CoreClient instance with __init__ bypassed (no real network calls)."""
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


# ---------------------------------------------------------------------------
# Phase 1: Current behavior tests (must ALL pass before any code changes)
# ---------------------------------------------------------------------------

class TestPhase1CurrentBehavior(unittest.TestCase):
    """
    Document and verify behavior. Originally written as pre-fix baseline;
    P1-1 still holds unchanged. P1-2, P1-3, P1-4 document WHAT WAS WRONG
    (bugs now fixed) — they are rewritten to assert the correct post-fix behavior
    so that the suite remains green and serves as regression tests.
    """

    def setUp(self):
        self.client = _make_core_client()

    def _mock_func(self, side_effects):
        """Helper that creates a callable raising side_effects in sequence."""
        calls = iter(side_effects)

        def func(data, metadata, timeout=None):
            effect = next(calls)
            if isinstance(effect, Exception):
                raise effect
            return effect

        return func

    # ------------------------------------------------------------------
    # P1-1: Scalekit UNAUTHENTICATED (no TOOL_ERROR) → M2M refresh + retry
    #       (behavior unchanged by the fix)
    # ------------------------------------------------------------------
    def test_p1_scalekit_unauthenticated_triggers_m2m_refresh_and_retry(self):
        """Scalekit 401 (no TOOL_ERROR) must call __authenticate_client and retry."""
        unauth_error = _make_rpc_error(StatusCode.UNAUTHENTICATED)  # no error_code
        success_response = object()

        func = self._mock_func([unauth_error, success_response])

        with patch.object(self.client, "_CoreClient__authenticate_client") as mock_auth:
            result = self.client.grpc_exec(func, data=None, retry=2)

        mock_auth.assert_called_once()
        self.assertIs(result, success_response)

    # ------------------------------------------------------------------
    # P1-2: Provider 429 (RESOURCE_EXHAUSTED + TOOL_ERROR)
    #       PRE-FIX BUG: was retried 3x then raised ScalekitTooManyRequestsException
    #       POST-FIX: raises ScalekitToolRateLimitException immediately (no retry)
    # ------------------------------------------------------------------
    def test_p1_provider_429_now_raises_tool_rate_limit_immediately(self):
        """
        Post-fix: RESOURCE_EXHAUSTED + TOOL_ERROR raises ScalekitToolRateLimitException
        immediately with no retries.
        """
        from scalekit.common.exceptions import ScalekitToolRateLimitException
        tool_429 = _make_rpc_error(
            StatusCode.RESOURCE_EXHAUSTED,
            error_code="TOOL_ERROR",
            tool_error_code="RATE_LIMIT_EXCEEDED",
            tool_error_message="Provider rate limited",
            execution_id="exec-001",
        )
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise tool_429

        with self.assertRaises(ScalekitToolRateLimitException):
            self.client.grpc_exec(func, data=None, retry=2)

        # No retry — exactly 1 call
        self.assertEqual(call_count[0], 1)

    # ------------------------------------------------------------------
    # P1-3: Provider 401 (UNAUTHENTICATED + TOOL_ERROR)
    #       PRE-FIX BUG: triggered M2M refresh
    #       POST-FIX: raises ScalekitToolUnauthorizedException immediately, no M2M
    # ------------------------------------------------------------------
    def test_p1_provider_401_now_raises_tool_unauthorized_immediately(self):
        """
        Post-fix: UNAUTHENTICATED + TOOL_ERROR raises ScalekitToolUnauthorizedException
        immediately, without triggering M2M token refresh.
        """
        from scalekit.common.exceptions import ScalekitToolUnauthorizedException
        tool_401 = _make_rpc_error(
            StatusCode.UNAUTHENTICATED,
            error_code="TOOL_ERROR",
            tool_error_code="UNAUTHORIZED",
            tool_error_message="Provider unauthorized",
            execution_id="exec-002",
        )
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise tool_401

        with patch.object(self.client, "_CoreClient__authenticate_client") as mock_auth:
            with self.assertRaises(ScalekitToolUnauthorizedException):
                self.client.grpc_exec(func, data=None, retry=1)

        mock_auth.assert_not_called()
        self.assertEqual(call_count[0], 1)

    # ------------------------------------------------------------------
    # P1-4: Scalekit 429 (RESOURCE_EXHAUSTED, no TOOL_ERROR)
    #       PRE-FIX BUG: was retried (tripling rate-limit damage)
    #       POST-FIX: raises ScalekitTooManyRequestsException immediately
    # ------------------------------------------------------------------
    def test_p1_scalekit_429_now_surfaces_immediately(self):
        """
        Post-fix: plain RESOURCE_EXHAUSTED (no TOOL_ERROR) is surfaced immediately
        as ScalekitTooManyRequestsException without any retries.
        """
        scalekit_429 = _make_rpc_error(StatusCode.RESOURCE_EXHAUSTED)  # no error_code
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise scalekit_429

        with self.assertRaises(ScalekitTooManyRequestsException):
            self.client.grpc_exec(func, data=None, retry=2)

        # No retry — exactly 1 call
        self.assertEqual(call_count[0], 1)


# ---------------------------------------------------------------------------
# Phase 2: New behavior tests (must FAIL before implementation)
# ---------------------------------------------------------------------------

class TestPhase2NewBehavior(unittest.TestCase):
    """Tests for desired (post-fix) behavior. These should FAIL before the fix."""

    def setUp(self):
        self.client = _make_core_client()

    def _always_raise(self, exc):
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise exc

        return func, call_count

    # ------------------------------------------------------------------
    # Exception hierarchy tests
    # ------------------------------------------------------------------
    def test_p2_tool_rate_limit_exception_exists(self):
        """ScalekitToolRateLimitException must exist in exceptions module."""
        from scalekit.common.exceptions import ScalekitToolRateLimitException  # noqa

    def test_p2_tool_unauthorized_exception_exists(self):
        """ScalekitToolUnauthorizedException must exist in exceptions module."""
        from scalekit.common.exceptions import ScalekitToolUnauthorizedException  # noqa

    def test_p2_tool_forbidden_exception_exists(self):
        """ScalekitToolForbiddenException must exist in exceptions module."""
        from scalekit.common.exceptions import ScalekitToolForbiddenException  # noqa

    def test_p2_tool_exception_exists(self):
        """ScalekitToolException must exist in exceptions module."""
        from scalekit.common.exceptions import ScalekitToolException  # noqa

    def test_p2_tool_rate_limit_is_instance_of_too_many_requests(self):
        """ScalekitToolRateLimitException is instance of ScalekitTooManyRequestsException (backward compat)."""
        from scalekit.common.exceptions import ScalekitToolRateLimitException, ScalekitToolException
        assert issubclass(ScalekitToolRateLimitException, ScalekitTooManyRequestsException)
        assert issubclass(ScalekitToolRateLimitException, ScalekitToolException)

    def test_p2_tool_unauthorized_is_instance_of_unauthorized(self):
        """ScalekitToolUnauthorizedException is instance of ScalekitUnauthorizedException (backward compat)."""
        from scalekit.common.exceptions import ScalekitToolUnauthorizedException, ScalekitToolException
        assert issubclass(ScalekitToolUnauthorizedException, ScalekitUnauthorizedException)
        assert issubclass(ScalekitToolUnauthorizedException, ScalekitToolException)

    def test_p2_tool_forbidden_is_instance_of_forbidden(self):
        """ScalekitToolForbiddenException is instance of ScalekitForbiddenException (backward compat)."""
        from scalekit.common.exceptions import ScalekitToolForbiddenException, ScalekitToolException
        assert issubclass(ScalekitToolForbiddenException, ScalekitForbiddenException)
        assert issubclass(ScalekitToolForbiddenException, ScalekitToolException)

    def test_p2_tool_exception_has_tool_error_code_property(self):
        """ScalekitToolException exposes tool_error_code property."""
        from scalekit.common.exceptions import ScalekitToolException
        rpc_err = _make_rpc_error(
            StatusCode.RESOURCE_EXHAUSTED,
            error_code="TOOL_ERROR",
            tool_error_code="RATE_LIMIT_EXCEEDED",
            tool_error_message="Provider rate limited",
            execution_id="exec-123",
        )
        exc = ScalekitToolException(rpc_err)
        self.assertEqual(exc.tool_error_code, "RATE_LIMIT_EXCEEDED")

    def test_p2_tool_exception_has_tool_error_message_property(self):
        """ScalekitToolException exposes tool_error_message property."""
        from scalekit.common.exceptions import ScalekitToolException
        rpc_err = _make_rpc_error(
            StatusCode.RESOURCE_EXHAUSTED,
            error_code="TOOL_ERROR",
            tool_error_code="RATE_LIMIT_EXCEEDED",
            tool_error_message="Provider rate limited",
            execution_id="exec-123",
        )
        exc = ScalekitToolException(rpc_err)
        self.assertEqual(exc.tool_error_message, "Provider rate limited")

    def test_p2_tool_exception_has_execution_id_property(self):
        """ScalekitToolException exposes execution_id property."""
        from scalekit.common.exceptions import ScalekitToolException
        rpc_err = _make_rpc_error(
            StatusCode.RESOURCE_EXHAUSTED,
            error_code="TOOL_ERROR",
            tool_error_code="RATE_LIMIT_EXCEEDED",
            tool_error_message="Provider rate limited",
            execution_id="exec-123",
        )
        exc = ScalekitToolException(rpc_err)
        self.assertEqual(exc.execution_id, "exec-123")

    # ------------------------------------------------------------------
    # Retry behavior: provider errors must raise immediately (no retry)
    # ------------------------------------------------------------------
    def test_p2_provider_429_raises_tool_rate_limit_immediately_no_retry(self):
        """Provider 429 (RESOURCE_EXHAUSTED + TOOL_ERROR) must raise ScalekitToolRateLimitException immediately, no retry."""
        from scalekit.common.exceptions import ScalekitToolRateLimitException
        rpc_err = _make_rpc_error(
            StatusCode.RESOURCE_EXHAUSTED,
            error_code="TOOL_ERROR",
            tool_error_code="RATE_LIMIT_EXCEEDED",
            tool_error_message="Provider rate limited",
            execution_id="exec-001",
        )
        func, call_count = self._always_raise(rpc_err)

        with self.assertRaises(ScalekitToolRateLimitException):
            self.client.grpc_exec(func, data=None, retry=2)

        # Must NOT be retried — exactly 1 call
        self.assertEqual(call_count[0], 1)

    def test_p2_provider_401_raises_tool_unauthorized_immediately_no_m2m_refresh(self):
        """Provider 401 (UNAUTHENTICATED + TOOL_ERROR) must raise ScalekitToolUnauthorizedException immediately, no M2M refresh."""
        from scalekit.common.exceptions import ScalekitToolUnauthorizedException
        rpc_err = _make_rpc_error(
            StatusCode.UNAUTHENTICATED,
            error_code="TOOL_ERROR",
            tool_error_code="UNAUTHORIZED",
            tool_error_message="Provider unauthorized",
            execution_id="exec-002",
        )
        func, call_count = self._always_raise(rpc_err)

        with patch.object(self.client, "_CoreClient__authenticate_client") as mock_auth:
            with self.assertRaises(ScalekitToolUnauthorizedException):
                self.client.grpc_exec(func, data=None, retry=2)

        mock_auth.assert_not_called()
        self.assertEqual(call_count[0], 1)

    def test_p2_provider_403_raises_tool_forbidden_immediately(self):
        """Provider 403 (PERMISSION_DENIED + TOOL_ERROR) must raise ScalekitToolForbiddenException immediately."""
        from scalekit.common.exceptions import ScalekitToolForbiddenException
        rpc_err = _make_rpc_error(
            StatusCode.PERMISSION_DENIED,
            error_code="TOOL_ERROR",
            tool_error_code="FORBIDDEN",
            tool_error_message="Provider forbidden",
            execution_id="exec-003",
        )
        func, call_count = self._always_raise(rpc_err)

        with self.assertRaises(ScalekitToolForbiddenException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 1)

    def test_p2_other_provider_error_raises_tool_exception_immediately(self):
        """Any other TOOL_ERROR (e.g. INTERNAL) raises ScalekitToolException immediately."""
        from scalekit.common.exceptions import ScalekitToolException
        rpc_err = _make_rpc_error(
            StatusCode.INTERNAL,
            error_code="TOOL_ERROR",
            tool_error_code="PROVIDER_ERROR",
            tool_error_message="Provider internal error",
            execution_id="exec-004",
        )
        func, call_count = self._always_raise(rpc_err)

        with self.assertRaises(ScalekitToolException):
            self.client.grpc_exec(func, data=None, retry=2)

        self.assertEqual(call_count[0], 1)

    def test_p2_tool_rate_limit_exception_carries_metadata(self):
        """ScalekitToolRateLimitException carries tool_error_code, tool_error_message, execution_id."""
        from scalekit.common.exceptions import ScalekitToolRateLimitException
        rpc_err = _make_rpc_error(
            StatusCode.RESOURCE_EXHAUSTED,
            error_code="TOOL_ERROR",
            tool_error_code="RATE_LIMIT_EXCEEDED",
            tool_error_message="HubSpot rate limit hit",
            execution_id="exec-hubspot-001",
        )
        func, _ = self._always_raise(rpc_err)

        with self.assertRaises(ScalekitToolRateLimitException) as ctx:
            self.client.grpc_exec(func, data=None, retry=2)

        exc = ctx.exception
        self.assertEqual(exc.tool_error_code, "RATE_LIMIT_EXCEEDED")
        self.assertEqual(exc.tool_error_message, "HubSpot rate limit hit")
        self.assertEqual(exc.execution_id, "exec-hubspot-001")

    # ------------------------------------------------------------------
    # Non-tool errors: Scalekit UNAUTHENTICATED must still refresh + retry
    # ------------------------------------------------------------------
    def test_p2_scalekit_unauthenticated_no_tool_error_still_refreshes(self):
        """Scalekit 401 without TOOL_ERROR must still trigger M2M refresh (unchanged behavior)."""
        unauth_error = _make_rpc_error(StatusCode.UNAUTHENTICATED)  # no error_code
        success_response = object()
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            if call_count[0] == 1:
                raise unauth_error
            return success_response

        with patch.object(self.client, "_CoreClient__authenticate_client") as mock_auth:
            result = self.client.grpc_exec(func, data=None, retry=2)

        mock_auth.assert_called_once()
        self.assertIs(result, success_response)

    # ------------------------------------------------------------------
    # Scalekit 429 (no TOOL_ERROR) must surface immediately, no retry
    # ------------------------------------------------------------------
    def test_p2_scalekit_429_no_tool_error_surfaces_immediately(self):
        """Scalekit RESOURCE_EXHAUSTED without TOOL_ERROR must raise immediately (no retry)."""
        scalekit_429 = _make_rpc_error(StatusCode.RESOURCE_EXHAUSTED)  # no error_code
        call_count = [0]

        def func(data, metadata, timeout=None):
            call_count[0] += 1
            raise scalekit_429

        with self.assertRaises(ScalekitTooManyRequestsException):
            self.client.grpc_exec(func, data=None, retry=2)

        # Must surface immediately — exactly 1 call
        self.assertEqual(call_count[0], 1)


if __name__ == "__main__":
    unittest.main()

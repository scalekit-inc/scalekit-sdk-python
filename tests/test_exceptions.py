"""
Regression tests for ScalekitServerException construction.

Root cause: ScalekitServerException.__init__ called
`rpc_status.from_call(error).message` with no None-guard. rpc_status.from_call
returns None whenever the gRPC error has no google.rpc.Status in trailing
metadata — true for any transport-level failure that never reached a real
server response (deadline exceeded, connection reset, refused, silently
dropped, ...), as opposed to an application-level error the backend actually
returned. Every one of those transport-level failures crashed while
constructing the exception meant to describe it, masking the real error
(UNAVAILABLE, DEADLINE_EXCEEDED, etc.) behind a confusing AttributeError —
found via toxiproxy fault-injection testing where every non-baseline case
across 5 API profiles surfaced this crash instead of a real status.

These tests mock grpc.RpcError directly (via trailing_metadata()) — no real
network calls, no scalekit.core dependency.
"""
import unittest

import grpc
from grpc import StatusCode

from scalekit.common.exceptions import ScalekitServerException, ScalekitServiceUnavailableException


class _FakeRpcError(grpc.RpcError):
    """A grpc.RpcError with a configurable trailing_metadata (empty = no Status, matching a real transport-level failure)."""

    def __init__(self, status_code, message, trailing=()):
        self._status_code = status_code
        self._message = message
        self._trailing = trailing

    def code(self):
        return self._status_code

    def trailing_metadata(self):
        return self._trailing

    def details(self):
        return self._message


class TestNoTrailingStatus(unittest.TestCase):
    """The transport-level-failure case: rpc_status.from_call(error) returns None."""

    def test_unavailable_with_no_status_does_not_crash(self):
        error = _FakeRpcError(StatusCode.UNAVAILABLE, "unavailable")
        exc = ScalekitServerException(error)  # must not raise AttributeError
        self.assertEqual(exc.grpc_status, StatusCode.UNAVAILABLE)
        self.assertEqual(exc.err_details, [])
        self.assertIsNone(exc.error_code)

    def test_deadline_exceeded_with_no_status_does_not_crash(self):
        error = _FakeRpcError(StatusCode.DEADLINE_EXCEEDED, "deadline exceeded")
        exc = ScalekitServerException(error)
        self.assertEqual(exc.grpc_status, StatusCode.DEADLINE_EXCEEDED)

    def test_message_falls_back_to_str_of_the_rpc_error(self):
        error = _FakeRpcError(StatusCode.UNAVAILABLE, "unavailable")
        exc = ScalekitServerException(error)
        self.assertIsNotNone(exc.message)
        self.assertEqual(exc.message, str(error))

    def test_promote_still_selects_the_right_subclass(self):
        """The None-guard must not change dispatch — promote() still returns
        the same exception type it always did for a status-less UNAVAILABLE."""
        error = _FakeRpcError(StatusCode.UNAVAILABLE, "unavailable")
        exc = ScalekitServerException.promote(error)
        self.assertIsInstance(exc, ScalekitServiceUnavailableException)

    def test_str_does_not_crash_either(self):
        error = _FakeRpcError(StatusCode.UNAVAILABLE, "unavailable")
        exc = ScalekitServerException(error)
        self.assertIn("UNAVAILABLE", str(exc))


class TestWithTrailingStatus(unittest.TestCase):
    """Regression guard: a real application-level error (has a Status) must
    keep working exactly as before — the None-guard must not touch this path."""

    def test_real_status_still_extracts_message_and_details(self):
        from google.rpc import status_pb2
        status = status_pb2.Status(code=StatusCode.NOT_FOUND.value[0], message="organization not found", details=[])
        trailing = (("grpc-status-details-bin", status.SerializeToString()),)
        error = _FakeRpcError(StatusCode.NOT_FOUND, "organization not found", trailing=trailing)

        exc = ScalekitServerException(error)
        self.assertEqual(exc.grpc_status, StatusCode.NOT_FOUND)
        self.assertEqual(exc.message, "organization not found")
        self.assertEqual(exc.err_details, [])


if __name__ == "__main__":
    unittest.main()

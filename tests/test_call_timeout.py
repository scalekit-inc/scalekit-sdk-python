"""
Tests for the configurable per-call gRPC timeout in CoreClient.

grpc_exec never passed a `timeout` to the stub call, so a call could block
forever on a connection that looks fine to the client but is silently dead
(the same class of bug DEFAULT_HTTP_TIMEOUT exists to prevent for the
token/JWKS requests calls). call_timeout_s/tool_call_timeout_s close that
gap, following the same configurable-with-validation pattern as
keepalive_time_ms/keepalive_timeout_ms.

These tests never touch the network: __authenticate_client and
grpc.secure_channel are mocked, so only the timeout wiring/validation is
exercised.
"""
import unittest
from unittest.mock import patch

from scalekit.core import (
    CoreClient,
    DEFAULT_CALL_TIMEOUT_S,
    DEFAULT_TOOL_CALL_TIMEOUT_S,
)


def _build_client(**kwargs):
    """Construct a CoreClient with auth and channel creation stubbed."""
    with patch.object(CoreClient, "_CoreClient__authenticate_client"), \
            patch("scalekit.core.grpc.secure_channel"), \
            patch("scalekit.core.grpc.ssl_channel_credentials"), \
            patch("scalekit.core.grpc.access_token_call_credentials"), \
            patch("scalekit.core.grpc.composite_channel_credentials"):
        return CoreClient(
            env_url="https://example.com",
            client_id="cid",
            client_secret="csec",
            **kwargs,
        )


class TestCallTimeoutConfiguration(unittest.TestCase):
    def test_defaults_applied(self):
        """Default construction must set both timeouts to their documented defaults."""
        client = _build_client()
        self.assertEqual(client.call_timeout_s, DEFAULT_CALL_TIMEOUT_S)
        self.assertEqual(client.tool_call_timeout_s, DEFAULT_TOOL_CALL_TIMEOUT_S)
        self.assertEqual(DEFAULT_CALL_TIMEOUT_S, 60)
        self.assertEqual(DEFAULT_TOOL_CALL_TIMEOUT_S, 60)

    def test_custom_values_applied(self):
        """Constructor kwargs must override the defaults."""
        client = _build_client(call_timeout_s=15, tool_call_timeout_s=90)
        self.assertEqual(client.call_timeout_s, 15)
        self.assertEqual(client.tool_call_timeout_s, 90)

    def test_zero_call_timeout_rejected(self):
        """Unlike keepalive_time_ms, 0 is not a valid 'disabled' escape hatch here —
        grpc-python treats timeout<=0 as an already-expired deadline, and there is
        no legitimate reason to reintroduce the unbounded-block bug."""
        with self.assertRaises(ValueError):
            _build_client(call_timeout_s=0)

    def test_negative_call_timeout_rejected(self):
        with self.assertRaises(ValueError):
            _build_client(call_timeout_s=-5)

    def test_zero_tool_call_timeout_rejected(self):
        with self.assertRaises(ValueError):
            _build_client(tool_call_timeout_s=0)

    def test_non_numeric_call_timeout_rejected(self):
        with self.assertRaises(ValueError):
            _build_client(call_timeout_s="30")


class TestGrpcExecPassesTimeout(unittest.TestCase):
    """grpc_exec must forward a real deadline to the stub call, defaulting to
    call_timeout_s and honoring a per-call override."""

    def setUp(self):
        self.client = _build_client()

    def test_default_timeout_forwarded_to_stub_call(self):
        seen = {}

        def func(data, metadata, timeout=None):
            seen["timeout"] = timeout
            return "ok"

        result = self.client.grpc_exec(func, data=None)
        self.assertEqual(result, "ok")
        self.assertEqual(seen["timeout"], DEFAULT_CALL_TIMEOUT_S)

    def test_explicit_timeout_override_forwarded(self):
        seen = {}

        def func(data, metadata, timeout=None):
            seen["timeout"] = timeout
            return "ok"

        self.client.grpc_exec(func, data=None, timeout=5)
        self.assertEqual(seen["timeout"], 5)

    def test_timeout_preserved_across_retries(self):
        """A retried call must keep using the same timeout as the original attempt,
        not silently fall back to call_timeout_s."""
        import grpc

        attempts = []

        class _Unavailable(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.UNAVAILABLE

            def trailing_metadata(self):
                return ()

            def details(self):
                return "unavailable"

        def func(data, metadata, timeout=None):
            attempts.append(timeout)
            if len(attempts) < 2:
                raise _Unavailable()
            return "ok"

        result = self.client.grpc_exec(func, data=None, retry=2, timeout=45)
        self.assertEqual(result, "ok")
        self.assertEqual(attempts, [45, 45])


if __name__ == "__main__":
    unittest.main()

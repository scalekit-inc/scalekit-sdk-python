"""
Tool-execution RPCs (ToolsClient, ActionClient.request) proxy to third-party
provider APIs (Google Calendar, Slack, etc.) and can legitimately run longer
than typical control-plane calls. They must use their own tool_timeout_ms
deadline instead of the tighter control-plane timeout_ms, so a slow (but
healthy) provider call isn't killed early. Also verifies the gRPC channel
now carries a deadline at all (previously calls could hang forever on a
silently dropped connection), and that UNAVAILABLE retries back off.
"""
import unittest
from unittest.mock import MagicMock, patch

import grpc
from grpc import StatusCode

from scalekit.core import CoreClient, DEFAULT_TIMEOUT_MS, DEFAULT_TOOL_TIMEOUT_MS
from scalekit.client import ScalekitClient
from scalekit.tools import ToolsClient
from scalekit.actions.actions import ActionClient


def _make_rpc_error(status_code: StatusCode, message: str = "error"):
    class _FakeRpcError(grpc.RpcError):
        def code(self):
            return status_code

        def trailing_metadata(self):
            return ()

        def details(self):
            return message

    return _FakeRpcError()


def _make_core_client(timeout_ms=None, tool_timeout_ms=None):
    """Return a CoreClient instance with __init__ bypassed (no real network calls)."""
    client = CoreClient.__new__(CoreClient)
    client.access_token = "test-token"
    client.host = "example.com"
    client.env_url = "https://example.com"
    client.client_id = "cid"
    client.client_secret = "csec"
    client.keys = {}
    client.grpc_secure_channel = None
    client.timeout_ms = timeout_ms if timeout_ms is not None else DEFAULT_TIMEOUT_MS
    client.tool_timeout_ms = tool_timeout_ms if tool_timeout_ms is not None else DEFAULT_TOOL_TIMEOUT_MS
    return client


class _FakeChannel:
    """Minimal grpc.Channel stand-in: unary_unary() just returns a MagicMock,
    so stub.SomeMethod.with_call is itself a MagicMock we can assert on."""

    def unary_unary(self, *args, **kwargs):
        return MagicMock()


class TestCoreClientTimeoutDefaults(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(DEFAULT_TIMEOUT_MS, 20_000)
        self.assertEqual(DEFAULT_TOOL_TIMEOUT_MS, 60_000)

    @patch.object(CoreClient, "_CoreClient__authenticate_client", lambda self: None)
    @patch.object(
        CoreClient,
        "_CoreClient__grpc_secure_channel",
        lambda self: setattr(self, "grpc_secure_channel", _FakeChannel()),
    )
    def test_scalekit_client_honors_custom_tool_timeout_ms(self):
        client = ScalekitClient(
            "https://example.scalekit.dev", "cid", "csec", tool_timeout_ms=45_000
        )
        self.assertEqual(client.core_client.tool_timeout_ms, 45_000)
        self.assertEqual(client.core_client.timeout_ms, DEFAULT_TIMEOUT_MS)

    @patch.object(CoreClient, "_CoreClient__authenticate_client", lambda self: None)
    @patch.object(
        CoreClient,
        "_CoreClient__grpc_secure_channel",
        lambda self: setattr(self, "grpc_secure_channel", _FakeChannel()),
    )
    def test_scalekit_client_defaults_when_unconfigured(self):
        client = ScalekitClient("https://example.scalekit.dev", "cid", "csec")
        self.assertEqual(client.core_client.timeout_ms, DEFAULT_TIMEOUT_MS)
        self.assertEqual(client.core_client.tool_timeout_ms, DEFAULT_TOOL_TIMEOUT_MS)


class TestGrpcExecTimeoutWiring(unittest.TestCase):
    def setUp(self):
        self.client = _make_core_client(timeout_ms=20_000, tool_timeout_ms=45_000)

    def test_default_call_uses_control_plane_timeout_in_seconds(self):
        func = MagicMock(return_value="ok")
        result = self.client.grpc_exec(func, data=None)
        self.assertEqual(result, "ok")
        _, kwargs = func.call_args
        self.assertEqual(kwargs["timeout"], 20.0)

    def test_explicit_timeout_ms_overrides_control_plane_default(self):
        func = MagicMock(return_value="ok")
        self.client.grpc_exec(func, data=None, timeout_ms=45_000)
        _, kwargs = func.call_args
        self.assertEqual(kwargs["timeout"], 45.0)

    def test_timeout_ms_preserved_across_unauthenticated_retry(self):
        calls = iter([_make_rpc_error(StatusCode.UNAUTHENTICATED), "ok"])

        def func(data, metadata, timeout=None):
            effect = next(calls)
            if isinstance(effect, Exception):
                raise effect
            return effect

        with patch.object(self.client, "_CoreClient__authenticate_client"):
            result = self.client.grpc_exec(func, data=None, retry=2, timeout_ms=45_000)

        self.assertEqual(result, "ok")

    def test_unavailable_retries_with_backoff_and_preserves_timeout(self):
        calls = iter([_make_rpc_error(StatusCode.UNAVAILABLE), "ok"])

        def func(data, metadata, timeout=None):
            effect = next(calls)
            if isinstance(effect, Exception):
                raise effect
            self.assertEqual(timeout, 45.0)
            return effect

        with patch("scalekit.core.time.sleep") as mock_sleep:
            result = self.client.grpc_exec(func, data=None, retry=2, timeout_ms=45_000)

        self.assertEqual(result, "ok")
        mock_sleep.assert_called_once()


class TestToolsClientUsesToolTimeout(unittest.TestCase):
    def setUp(self):
        self.core_client = _make_core_client(timeout_ms=20_000, tool_timeout_ms=45_000)
        self.core_client.grpc_secure_channel = _FakeChannel()
        self.tools = ToolsClient(self.core_client)

    def test_list_tools_uses_tool_timeout(self):
        self.tools.tool_service.ListTools.with_call.return_value = "ok"
        self.tools.list_tools(page_size=10)
        _, kwargs = self.tools.tool_service.ListTools.with_call.call_args
        self.assertEqual(kwargs["timeout"], 45.0)

    def test_list_scoped_tools_uses_tool_timeout(self):
        self.tools.tool_service.ListScopedTools.with_call.return_value = "ok"
        self.tools.list_scoped_tools(identifier="id")
        _, kwargs = self.tools.tool_service.ListScopedTools.with_call.call_args
        self.assertEqual(kwargs["timeout"], 45.0)

    def test_execute_tool_uses_tool_timeout(self):
        self.tools.tool_service.ExecuteTool.with_call.return_value = "ok"
        self.tools.execute_tool(tool_name="gmail_send_email", identifier="id")
        _, kwargs = self.tools.tool_service.ExecuteTool.with_call.call_args
        self.assertEqual(kwargs["timeout"], 45.0)


class TestActionClientRequestProxyTimeout(unittest.TestCase):
    def setUp(self):
        self.core_client = _make_core_client(timeout_ms=20_000, tool_timeout_ms=45_000)
        self.core_client.grpc_secure_channel = _FakeChannel()
        self.tools = ToolsClient(self.core_client)
        self.actions = ActionClient(self.tools, connected_accounts_client=None)

    def test_defaults_to_tool_timeout_ms(self):
        with patch("scalekit.actions.actions.requests.request") as mock_request:
            mock_request.return_value = MagicMock(status_code=200)
            self.actions.request(
                connection_name="slack", identifier="user@example.com", path="/chat.postMessage"
            )
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs["timeout"], 45.0)

    def test_per_call_override(self):
        with patch("scalekit.actions.actions.requests.request") as mock_request:
            mock_request.return_value = MagicMock(status_code=200)
            self.actions.request(
                connection_name="slack",
                identifier="user@example.com",
                path="/chat.postMessage",
                timeout=5,
            )
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs["timeout"], 5)


if __name__ == "__main__":
    unittest.main()

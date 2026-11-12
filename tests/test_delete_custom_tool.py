"""Offline tests for ActionClient.delete_custom_tool.

Only the gRPC channel is faked. The generated stub, the client's real retry and error mapping, and the
clients all run, so what is checked is what would be put on the wire.
"""
import unittest
from collections import namedtuple
from unittest.mock import MagicMock, patch

import grpc
from google.protobuf import empty_pb2
from google.rpc import status_pb2
from grpc import StatusCode

from scalekit.actions.actions import ActionClient
from scalekit.core import DEFAULT_CALL_TIMEOUT_S, CoreClient
from scalekit.tools import ToolsClient
from scalekit.v1.tools import tools_pb2 as pb

METHOD = "/scalekit.v1.tools.ToolService/DeleteCustomTool"
TOOL_CALL_TIMEOUT_S = 123.0  # unlike every default, so a call that uses another deadline shows

Sent = namedtuple("Sent", "path body timeout metadata")


def _rpc_error(code: StatusCode, message: str) -> grpc.RpcError:
    """An RpcError carrying a google.rpc.Status, the way the server answers."""
    status = status_pb2.Status(code=code.value[0], message=message)
    trailing = (("grpc-status-details-bin", status.SerializeToString()),)

    class _Error(grpc.RpcError):
        def code(self):
            return code

        def details(self):
            return message

        def trailing_metadata(self):
            return trailing

    return _Error()


class _Call:
    def code(self):
        return StatusCode.OK


class _FakeChannel:
    """A channel that records what the generated stub sends and answers from a script of replies and errors."""

    def __init__(self):
        self.script = []
        self.sent = []

    def unary_unary(self, path, request_serializer=None, response_deserializer=None, **_):
        channel = self

        class _Method:
            def with_call(self, request, timeout=None, metadata=None, **_):
                channel.sent.append(Sent(path, request_serializer(request), timeout, dict(metadata or ())))
                item = channel.script.pop(0)
                if isinstance(item, Exception):
                    raise item
                # what the caller gets is what the stub's own deserializer makes of the bytes on the wire
                return response_deserializer(item.SerializeToString()), _Call()

        return _Method()


def _core_client(channel: _FakeChannel) -> CoreClient:
    """A CoreClient with the real retry and error mapping and no network."""
    core = CoreClient.__new__(CoreClient)
    core.access_token = "test-token"
    core.host = "example.com"
    core.env_url = "https://example.com"
    core.client_id = "cid"
    core.client_secret = "csec"
    core.keys = {}
    core.grpc_secure_channel = channel
    core.call_timeout_s = DEFAULT_CALL_TIMEOUT_S
    core.tool_call_timeout_s = TOOL_CALL_TIMEOUT_S
    return core


class DeleteCustomToolTestCase(unittest.TestCase):
    def setUp(self):
        self.channel = _FakeChannel()
        self.actions = ActionClient(ToolsClient(_core_client(self.channel)), MagicMock())
        sleep = patch("scalekit.core.time.sleep")  # the backoff between two attempts
        self.sleep = sleep.start()
        self.addCleanup(sleep.stop)

    def _reply(self, *items):
        self.channel.script.extend(items)

    def _request(self, index: int = -1) -> pb.DeleteCustomToolRequest:
        return pb.DeleteCustomToolRequest.FromString(self.channel.sent[index].body)


class RequestTest(DeleteCustomToolTestCase):
    def test_a_name_is_sent_exactly_as_given(self):
        """The server folds the name's case itself (ASCII letters only), so the client does not: a different
        name could delete a tool the caller did not name."""
        names = (
            "A-Acme_Get_User",  # not folded here
            " a-acme_get_user ",  # not trimmed
            "a-acme_get_userK",  # the Kelvin sign: str.lower() would turn it into an ASCII "k"
            "a-acme_İ",  # a dotted capital I: str.lower() would make two characters of it
        )
        for name in names:
            with self.subTest(name=name):
                self._reply(empty_pb2.Empty())
                self.assertIsNone(self.actions.delete_custom_tool(name))
                self.assertEqual(self._request().tool_identifier, name)

    def test_an_id_is_sent_exactly_as_given(self):
        """The server reads a value that starts with tol_ (in any case) as a tool's id; the client sends it unchanged too."""
        for tool_id in ("tol_1234", "TOL_1234", " tol_1234", "tol_01234"):
            with self.subTest(tool_id=tool_id):
                self._reply(empty_pb2.Empty())
                self.actions.delete_custom_tool(tool_id)
                self.assertEqual(self._request().tool_identifier, tool_id)
        self.assertEqual(self.channel.sent[0].body, b"\x0a\x08tol_1234")
        self.assertEqual({s.path for s in self.channel.sent}, {METHOD})

    def test_a_name_that_is_not_a_non_empty_string_is_refused_before_anything_is_sent(self):
        """No tool has a name like these, so the server would answer 400 or 404: there is no point in asking."""
        for name in ("", " ", "\t\n", " ", None, 7, b"a-acme_get_user"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as refused:
                    self.actions.delete_custom_tool(name)
                self.assertIn("tool_identifier", str(refused.exception))
        self.assertEqual(self.channel.sent, [], "nothing is sent when the name is refused")

    def test_the_tool_call_deadline_is_used(self):
        self._reply(empty_pb2.Empty())
        self.actions.delete_custom_tool("a-acme_get_user")
        self.assertEqual(self.channel.sent[0].timeout, TOOL_CALL_TIMEOUT_S)
        self.assertNotEqual(TOOL_CALL_TIMEOUT_S, DEFAULT_CALL_TIMEOUT_S)


class RetryTest(DeleteCustomToolTestCase):
    """A delete can be repeated, so it keeps the default retry on UNAVAILABLE."""

    def test_a_dropped_connection_is_retried_and_the_delete_goes_through(self):
        self._reply(_rpc_error(StatusCode.UNAVAILABLE, "connection reset"), empty_pb2.Empty())
        self.assertIsNone(self.actions.delete_custom_tool("a-acme_get_user"))
        self.assertEqual([s.path for s in self.channel.sent], [METHOD, METHOD])
        self.assertEqual(self.channel.sent[0].body, self.channel.sent[1].body, "the repeat is the same request")
        self.sleep.assert_called_once()


if __name__ == "__main__":
    unittest.main()

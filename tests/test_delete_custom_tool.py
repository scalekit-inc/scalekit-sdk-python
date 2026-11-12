"""Offline tests for deleting under a custom connector: ToolsClient.delete_custom_tool, and the 409 that
delete_custom_provider answers while a run of the connector is in progress.

Only the gRPC channel is faked. The generated stub, the client's real retry and error mapping, and the
clients all run, so what is checked is what would be put on the wire.
"""
import unittest
from collections import namedtuple
from unittest.mock import MagicMock, patch

import grpc
from google.protobuf import any_pb2, descriptor_pb2, empty_pb2
from google.rpc import status_pb2
from grpc import StatusCode

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import DeleteCustomProviderRequest
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitConflictException,
    ScalekitInternalServerException,
    ScalekitNotFoundException,
    ScalekitServiceUnavailableException,
)
from scalekit.core import DEFAULT_CALL_TIMEOUT_S, CoreClient
from scalekit.providers import ProvidersClient
from scalekit.tools import ToolsClient
from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo
from scalekit.v1.providers import providers_pb2 as providers_pb
from scalekit.v1.tools import tools_pb2 as pb

METHOD = "/scalekit.v1.tools.ToolService/DeleteCustomTool"
PROVIDER_METHOD = "/scalekit.v1.providers.ProviderService/DeleteCustomProvider"
TOOL_CALL_TIMEOUT_S = 123.0  # unlike every default, so a call that uses another deadline shows

Sent = namedtuple("Sent", "path body timeout metadata")


def _rpc_error(code: StatusCode, message: str, error_code: str = None) -> grpc.RpcError:
    """An RpcError carrying a google.rpc.Status, the way the server answers."""
    details = []
    if error_code:
        detail = any_pb2.Any()
        detail.Pack(ErrorInfo(error_code=error_code))
        details.append(detail)
    status = status_pb2.Status(code=code.value[0], message=message, details=details)
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
        self.tools = ToolsClient(_core_client(self.channel))
        sleep = patch("scalekit.core.time.sleep")  # the backoff between two attempts
        self.sleep = sleep.start()
        self.addCleanup(sleep.stop)

    def _reply(self, *items):
        self.channel.script.extend(items)

    def _request(self, index: int = -1) -> pb.DeleteCustomToolRequest:
        return pb.DeleteCustomToolRequest.FromString(self.channel.sent[index].body)


class GeneratedCodeTest(DeleteCustomToolTestCase):
    """The committed stubs must say what the backend's tools.proto says."""

    def test_the_request_has_the_two_fields_of_the_proto(self):
        fields = [(f.name, f.number, f.type) for f in pb.DeleteCustomToolRequest.DESCRIPTOR.fields]
        string = descriptor_pb2.FieldDescriptorProto.TYPE_STRING
        self.assertEqual(fields, [("tool_name", 1, string), ("provider_identifier", 2, string)])

    def test_the_service_declares_the_rpc_with_an_empty_answer(self):
        method = pb.DESCRIPTOR.services_by_name["ToolService"].methods_by_name["DeleteCustomTool"]
        self.assertEqual(method.input_type.full_name, "scalekit.v1.tools.DeleteCustomToolRequest")
        self.assertEqual(method.output_type.full_name, "google.protobuf.Empty")

    def test_a_delete_goes_to_its_own_method_with_both_fields_on_the_wire(self):
        self._reply(empty_pb2.Empty())
        self.tools.delete_custom_tool("a-acme_get_user", provider_identifier="ACME:1234")
        sent = self.channel.sent
        self.assertEqual([s.path for s in sent], [METHOD])
        # field 1 and field 2, both length-delimited
        self.assertEqual(sent[0].body, b"\x0a\x0fa-acme_get_user" + b"\x12\x09ACME:1234")

    def test_without_a_connector_only_the_name_is_on_the_wire(self):
        self._reply(empty_pb2.Empty())
        self.tools.delete_custom_tool("a-acme_get_user")
        self.assertEqual(self.channel.sent[0].body, b"\x0a\x0fa-acme_get_user")

    def test_the_answer_is_the_empty_message_with_the_call_next_to_it(self):
        self._reply(empty_pb2.Empty())
        response, call = self.tools.delete_custom_tool("a-acme_get_user")
        self.assertIsInstance(response, empty_pb2.Empty)
        self.assertEqual(call.code().name, "OK")


class RequestTest(DeleteCustomToolTestCase):
    def test_the_name_and_the_connector_are_sent_exactly_as_given(self):
        """The server folds the name's case itself (ASCII letters only) and matches the connector exactly, so the
        client changes neither: a different name could delete a tool the caller did not name."""
        names = (
            "A-Acme_Get_User",  # not folded here
            " a-acme_get_user ",  # not trimmed
            "a-acme_get_userK",  # the Kelvin sign: str.lower() would turn it into an ASCII "k"
            "a-acme_İ",  # a dotted capital I: str.lower() would make two characters of it
        )
        for name in names:
            for connector in (None, "ACME:1234", "acme:1234", " ACME:1234 "):  # not folded, not trimmed
                with self.subTest(name=name, connector=connector):
                    self._reply(empty_pb2.Empty())
                    self.tools.delete_custom_tool(name, provider_identifier=connector)
                    request = self._request()
                    self.assertEqual(request.tool_name, name)
                    self.assertEqual(request.provider_identifier, connector or "")

    def test_the_connector_is_optional(self):
        for connector in (None, ""):
            with self.subTest(connector=connector):
                self._reply(empty_pb2.Empty())
                self.tools.delete_custom_tool("a-acme_get_user", provider_identifier=connector)
                self.assertEqual(self.channel.sent[-1].body, b"\x0a\x0fa-acme_get_user", "field 2 is left out")

    def test_a_name_that_is_not_a_non_empty_string_is_refused_before_anything_is_sent(self):
        """No tool has a name like these, so the server would answer 400 or 404: there is no point in asking."""
        for name in ("", " ", "\t\n", " ", None, 7, b"a-acme_get_user"):
            for connector in (None, "ACME:1234"):
                with self.subTest(name=name, connector=connector):
                    with self.assertRaises(ValueError) as refused:
                        self.tools.delete_custom_tool(name, provider_identifier=connector)
                    self.assertIn("tool_name", str(refused.exception))
        self.assertEqual(self.channel.sent, [], "nothing is sent when the name is refused")

    def test_the_tool_call_deadline_is_used(self):
        self._reply(empty_pb2.Empty())
        self.tools.delete_custom_tool("a-acme_get_user")
        self.assertEqual(self.channel.sent[0].timeout, TOOL_CALL_TIMEOUT_S)
        self.assertNotEqual(TOOL_CALL_TIMEOUT_S, DEFAULT_CALL_TIMEOUT_S)

    def test_the_call_is_authenticated_like_every_other(self):
        self._reply(empty_pb2.Empty())
        self.tools.delete_custom_tool("a-acme_get_user")
        self.assertEqual(self.channel.sent[0].metadata["authorization"], "Bearer test-token")

    def test_it_is_reachable_through_the_actions_client(self):
        actions = ActionClient(self.tools, MagicMock())
        self.assertIs(actions.tools, self.tools)
        self._reply(empty_pb2.Empty())
        response, _ = actions.tools.delete_custom_tool("a-acme_get_user", provider_identifier="ACME:1234")
        self.assertIsInstance(response, empty_pb2.Empty)
        self.assertEqual([s.path for s in self.channel.sent], [METHOD])
        self.assertEqual(
            (self._request().tool_name, self._request().provider_identifier), ("a-acme_get_user", "ACME:1234")
        )


class RetryTest(DeleteCustomToolTestCase):
    """Deleting by name can be repeated, so it keeps the default retry on UNAVAILABLE (execute_tool and
    trigger_tool_collection opt out, because a repeat of either does the work twice)."""

    def test_a_dropped_connection_is_retried_and_the_delete_goes_through(self):
        self._reply(_rpc_error(StatusCode.UNAVAILABLE, "connection reset"), empty_pb2.Empty())
        response, _ = self.tools.delete_custom_tool("a-acme_get_user", provider_identifier="ACME:1234")
        self.assertIsInstance(response, empty_pb2.Empty)
        self.assertEqual([s.path for s in self.channel.sent], [METHOD, METHOD])
        self.assertEqual(self.channel.sent[0].body, self.channel.sent[1].body, "the repeat is the same request")
        self.sleep.assert_called_once()

    def test_a_repeat_after_a_lost_answer_is_a_404_that_can_be_read_as_gone(self):
        self._reply(
            _rpc_error(StatusCode.UNAVAILABLE, "connection reset"),
            _rpc_error(StatusCode.NOT_FOUND, "custom tool not found", "NOT_FOUND"),
        )
        with self.assertRaises(ScalekitNotFoundException) as gone:
            self.tools.delete_custom_tool("a-acme_get_user")
        self.assertEqual(gone.exception.message, "custom tool not found")
        self.assertEqual(len(self.channel.sent), 2)

    def test_a_service_that_stays_unavailable_is_given_up_after_the_default_retries(self):
        self._reply(*[_rpc_error(StatusCode.UNAVAILABLE, "connection refused")] * 3)
        with self.assertRaises(ScalekitServiceUnavailableException):
            self.tools.delete_custom_tool("a-acme_get_user")
        self.assertEqual(len(self.channel.sent), 3, "one attempt and two retries")

    def test_an_answer_of_the_server_is_never_repeated(self):
        """Every case the server answers leaves the first answer standing, in particular both 409s: nothing was
        deleted, and asking again at once only meets the same answer. The texts are the ones the backend sends
        (service/tools.go, DeleteCustomTool)."""
        answers = (
            (StatusCode.NOT_FOUND, "custom tool not found", "NOT_FOUND", ScalekitNotFoundException),
            (StatusCode.INVALID_ARGUMENT, "OpenAPI-sourced connectors are not enabled for this environment",
             "FEATURE_NOT_ENABLED", ScalekitBadRequestException),
            (StatusCode.ALREADY_EXISTS,
             "a sync of this connector is in progress; nothing was deleted, retry once it has finished",
             "RESOURCE_ALREADY_EXISTS", ScalekitConflictException),
            (StatusCode.ALREADY_EXISTS,
             "tools of more than one connector of this environment have this name (ACME:1234, ACME:1235); "
             "nothing was deleted, set provider_identifier to the full identifier of the OpenAPI-sourced "
             "connector whose tool should be deleted (a connector that no longer exists, or is not "
             "OpenAPI-sourced, answers 404)",
             "TOOL_NAME_AMBIGUOUS", ScalekitConflictException),
            # a database failure: the server does not say whether the tool is still there
            (StatusCode.INTERNAL, "failed to delete custom tool", "INTERNAL_ERROR",
             ScalekitInternalServerException),
        )
        for code, message, error_code, exception in answers:
            with self.subTest(error_code=error_code):
                before = len(self.channel.sent)
                self._reply(_rpc_error(code, message, error_code))
                with self.assertRaises(exception) as raised:
                    self.tools.delete_custom_tool("a-acme_get_user")
                self.assertEqual(len(self.channel.sent), before + 1, "sent once")
                self.assertEqual(raised.exception.error_code, error_code)
                self.assertEqual(raised.exception.message, message)
        self.sleep.assert_not_called()


class DeleteCustomProviderTest(DeleteCustomToolTestCase):
    """The server refuses to delete a connector while one of its runs is queued or processing."""

    def setUp(self):
        super().setUp()
        providers = ProvidersClient(self.tools.core_client)
        self.actions = ActionClient(self.tools, MagicMock(), providers_client=providers)

    def test_a_run_in_progress_is_a_409_that_names_the_run_and_the_delete_goes_through_afterwards(self):
        message = (
            "cannot delete custom provider while an ingestion run is already in progress for this connector "
            "(run tcr_123 is PROCESSING): nothing was deleted, wait for it to finish (see GetToolCollectionRun), "
            "then retry"
        )
        self._reply(
            _rpc_error(StatusCode.ALREADY_EXISTS, message, "RESOURCE_ALREADY_EXISTS"),
            providers_pb.DeleteProviderResponse(),
        )
        request = DeleteCustomProviderRequest(identifier="ACME:1234")
        with self.assertRaises(ScalekitConflictException) as busy:
            self.actions.providers.delete_custom_provider(request)
        self.assertEqual((busy.exception.error_code, busy.exception.message), ("RESOURCE_ALREADY_EXISTS", message))
        self.assertEqual(len(self.channel.sent), 1, "the answer of the server is not repeated")
        # after polling get_tool_collection_run: the same call, once the run has finished
        self.actions.providers.delete_custom_provider(request)
        self.assertEqual([s.path for s in self.channel.sent], [PROVIDER_METHOD, PROVIDER_METHOD])
        repeated = providers_pb.DeleteProviderRequest.FromString(self.channel.sent[1].body)
        self.assertEqual(repeated.identifier, "ACME:1234")


if __name__ == "__main__":
    unittest.main()

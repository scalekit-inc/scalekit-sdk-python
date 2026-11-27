"""Offline tests for the tool collection run methods of ``client.actions``.

``ActionClient.invoke_tool_collection`` and ``ActionClient.get_tool_collection_run`` check their arguments
themselves and make the gRPC call through the tools client, like ``delete_custom_tool``. Nothing about them lives in
the providers layer, so the clients built here have no ``ProvidersClient``.

Only the gRPC channel is faked. The generated stub, the core client and its real error mapping all run, so what is
checked is what would be put on the wire. What a run looks like once decoded is tested in test_tool_collection_runs.py.
"""
import inspect
import typing
import unittest
from collections import namedtuple
from datetime import datetime, timezone
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import grpc
from google.protobuf import any_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from google.rpc import status_pb2
from grpc import StatusCode

import scalekit.actions.types as exported
from scalekit import ScalekitClient
from scalekit.actions.actions import ActionClient
from scalekit.actions.types import SkippedTool, ToolCollectionRun, ToolCollectionRunStatus
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitConflictException,
    ScalekitNotFoundException,
)
from scalekit.core import CoreClient
from scalekit.tools import ToolsClient
from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo
from scalekit.v1.providers import providers_pb2 as pb
from scalekit.v1.tools.tools_pb2 import DeleteCustomToolRequest

INVOKE = "/scalekit.v1.providers.ProviderService/TriggerToolCollection"
GET_RUN = "/scalekit.v1.providers.ProviderService/GetToolCollectionRun"
CONNECTOR = "ACMEAPI:70219645518265104"
RUN_ID = "tcr_153432495495315592"
QUEUED_AT = datetime(2026, 11, 11, 9, 0, 0, tzinfo=timezone.utc)

# Field 1 is provider_identifier and field 2 is run_id, both strings: a tag byte, the length, the UTF-8 text.
IDENTIFIER_FIELD = b"\x0a\x19" + CONNECTOR.encode()  # 25 characters
RUN_ID_FIELD = b"\x12\x16" + RUN_ID.encode()  # 22 characters
LATEST_FIELD = b"\x12\x06latest"

Sent = namedtuple("Sent", "path request body metadata")


def _timestamp(value: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(value)
    return ts


def _run(**kw) -> pb.ToolCollectionRun:
    kw.setdefault("run_id", RUN_ID)
    kw.setdefault("provider_identifier", CONNECTOR)
    kw.setdefault("status", "QUEUED")
    kw.setdefault("created_at", _timestamp(QUEUED_AT))
    return pb.ToolCollectionRun(**kw)


def _request_type(rpc: str):
    """The message that the generated ProviderService declares as the request of ``rpc``."""
    return pb.DESCRIPTOR.services_by_name["ProviderService"].methods_by_name[rpc].input_type


def _rpc_error(code: StatusCode, message: str, error_code: str = "") -> grpc.RpcError:
    """An RpcError carrying a google.rpc.Status (and an ErrorInfo with ``error_code``), the way the server answers."""
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
        self.stubbed = []  # the path of every method a stub asked this channel for

    def unary_unary(self, path, request_serializer=None, response_deserializer=None, **_):
        channel = self
        channel.stubbed.append(path)

        class _Method:
            def with_call(self, request, **options):
                channel.sent.append(
                    Sent(
                        path,
                        request,
                        request_serializer(request),
                        dict(options.get("metadata") or ()),
                    )
                )
                item = channel.script.pop(0)
                if isinstance(item, Exception):
                    raise item
                # what the caller gets is what the stub's own deserializer makes of the bytes on the wire
                return response_deserializer(item.SerializeToString()), _Call()

        return _Method()


def _core_client(channel: _FakeChannel) -> CoreClient:
    """A CoreClient with the real error mapping and no network."""
    core = CoreClient.__new__(CoreClient)
    core.access_token = "test-token"
    core.host = "example.com"
    core.env_url = "https://example.com"
    core.client_id = "cid"
    core.client_secret = "csec"
    core.keys = {}
    core.grpc_secure_channel = channel
    core.call_timeout_s = 20  # grpc_exec reads it
    return core


class ToolCollectionRunsTestCase(unittest.TestCase):
    def setUp(self):
        self.channel = _FakeChannel()
        self.core = _core_client(self.channel)
        # No ProvidersClient: the two methods do not need one.
        self.actions = ActionClient(ToolsClient(self.core), MagicMock())

    def _reply(self, *items):
        self.channel.script.extend(items)

    def assertMapped(self, code, message, error_code, expected, http_status, call):
        """The server's answer reaches the caller as the SDK's exception for it, carrying the server's own text."""
        self.channel.sent.clear()
        self._reply(_rpc_error(code, message, error_code))
        with self.assertRaises(expected) as raised:
            call()
        exception = raised.exception
        self.assertIs(type(exception), expected)  # not wrapped, not translated
        self.assertEqual(exception.message, message)
        self.assertEqual(exception.error_code, error_code)
        self.assertEqual(exception.http_status, http_status)
        self.assertEqual(exception.grpc_status, code)
        self.assertEqual(len(self.channel.sent), 1, "the call is made once")

    def assertPlainCall(self, calls):
        """Like every other call: grpc_exec gets the stub method and the request, nothing else."""
        self.assertEqual(len(calls), 2)
        for call in calls:
            self.assertEqual(len(call.args), 2)
            self.assertEqual(call.kwargs, {})


class InvokeToolCollectionTest(ToolCollectionRunsTestCase):
    def test_sends_the_proto_request_and_returns_the_queued_run_typed(self):
        self._reply(_run())
        run = self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        (sent,) = self.channel.sent
        self.assertEqual(sent.path, INVOKE)
        self.assertEqual(sent.body, IDENTIFIER_FIELD)
        self.assertIs(sent.request.DESCRIPTOR, _request_type("TriggerToolCollection"))
        self.assertEqual(sent.request.provider_identifier, CONNECTOR)
        self.assertIsInstance(run, ToolCollectionRun)
        self.assertEqual((run.run_id, run.provider_identifier), (RUN_ID, CONNECTOR))
        self.assertIs(run.status, ToolCollectionRunStatus.QUEUED)
        self.assertFalse(run.is_terminal)
        self.assertEqual(run.created_at, QUEUED_AT)

    def test_the_identifier_may_be_passed_by_position(self):
        self._reply(_run())
        self.actions.invoke_tool_collection(CONNECTOR)
        self.assertEqual(self.channel.sent[0].body, IDENTIFIER_FIELD)

    def test_the_whitespace_around_the_identifier_is_removed(self):
        for padded in (f"  {CONNECTOR}", f"{CONNECTOR}\n", f"\t{CONNECTOR} \r\n", f"\u00a0{CONNECTOR}\u00a0"):
            with self.subTest(identifier=padded):
                self._reply(_run())
                self.actions.invoke_tool_collection(provider_identifier=padded)
                self.assertEqual(self.channel.sent[-1].body, IDENTIFIER_FIELD)

    def test_a_refused_identifier_sends_nothing(self):
        for value in ("", " ", "\t\n", "\u00a0", None, 7, b"ACMEAPI:70219645518265104", "x" * 256, f"{'x' * 256}\n"):
            with self.subTest(identifier=value):
                with self.assertRaises(ValueError) as refused:
                    self.actions.invoke_tool_collection(provider_identifier=value)
                self.assertIn("provider_identifier", str(refused.exception))
        self.assertEqual(self.channel.sent, [], "nothing is sent when the identifier is refused")

    def test_255_characters_are_accepted_whatever_surrounds_them(self):
        longest = "x" * 255
        self._reply(_run(), _run())
        self.actions.invoke_tool_collection(provider_identifier=longest)
        self.actions.invoke_tool_collection(provider_identifier=f" {longest}\n")
        self.assertEqual([s.request.provider_identifier for s in self.channel.sent], [longest] * 2)

    def test_the_call_is_made_with_the_defaults_of_every_other_call(self):
        self._reply(_run(), _run())
        with patch.object(self.core, "grpc_exec", wraps=self.core.grpc_exec) as grpc_exec:
            self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
            self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        self.assertPlainCall(grpc_exec.call_args_list)

    def test_server_errors_reach_the_caller_as_the_sdk_maps_them(self):
        cases = [
            (
                StatusCode.NOT_FOUND,
                "provider not found",
                "RESOURCE_NOT_FOUND",
                ScalekitNotFoundException,
                HTTPStatus.NOT_FOUND,
            ),
            (
                StatusCode.INVALID_ARGUMENT,
                "this connector is not sourced from an OpenAPI spec",
                "INVALID_ARGUMENT",
                ScalekitBadRequestException,
                HTTPStatus.BAD_REQUEST,
            ),
            (
                StatusCode.INVALID_ARGUMENT,
                "feature not enabled",
                "FEATURE_NOT_ENABLED",
                ScalekitBadRequestException,
                HTTPStatus.BAD_REQUEST,
            ),
            (
                StatusCode.ALREADY_EXISTS,
                "an ingestion run is already in progress for this connector",
                "RESOURCE_ALREADY_EXISTS",
                ScalekitConflictException,
                HTTPStatus.CONFLICT,
            ),
        ]
        for code, message, error_code, expected, http_status in cases:
            with self.subTest(error_code=error_code, message=message):
                self.assertMapped(
                    code,
                    message,
                    error_code,
                    expected,
                    http_status,
                    lambda: self.actions.invoke_tool_collection(provider_identifier=CONNECTOR),
                )


class GetToolCollectionRunTest(ToolCollectionRunsTestCase):
    def test_sends_the_proto_request_for_the_latest_run_by_default_and_returns_the_run_typed(self):
        self._reply(_run(status="PROCESSING"))
        run = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        (sent,) = self.channel.sent
        self.assertEqual(sent.path, GET_RUN)
        self.assertEqual(sent.body, IDENTIFIER_FIELD + LATEST_FIELD)
        self.assertIs(sent.request.DESCRIPTOR, _request_type("GetToolCollectionRun"))
        self.assertEqual((sent.request.provider_identifier, sent.request.run_id), (CONNECTOR, "latest"))
        self.assertIsInstance(run, ToolCollectionRun)
        self.assertIs(run.status, ToolCollectionRunStatus.PROCESSING)
        self.assertFalse(run.is_terminal)

    def test_latest_can_be_passed_and_means_the_default(self):
        self._reply(_run(), _run())
        self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id="latest")
        self.assertEqual(self.channel.sent[0].body, self.channel.sent[1].body)

    def test_a_run_can_be_read_by_id_by_keyword_or_by_position(self):
        self._reply(_run(), _run())
        self.actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id=RUN_ID)
        self.actions.get_tool_collection_run(CONNECTOR, RUN_ID)
        self.assertEqual([s.body for s in self.channel.sent], [IDENTIFIER_FIELD + RUN_ID_FIELD] * 2)

    def test_an_empty_or_blank_run_id_is_sent_as_latest(self):
        for blank in ("", " ", "\t\n", "\u00a0"):
            with self.subTest(run_id=blank):
                self._reply(_run())
                self.actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id=blank)
                self.assertEqual(self.channel.sent[-1].body, IDENTIFIER_FIELD + LATEST_FIELD)

    def test_the_whitespace_around_the_identifier_and_the_run_id_is_removed(self):
        self._reply(_run())
        self.actions.get_tool_collection_run(provider_identifier=f"\t{CONNECTOR} ", run_id=f" {RUN_ID}\n")
        self.assertEqual(self.channel.sent[0].body, IDENTIFIER_FIELD + RUN_ID_FIELD)

    def test_a_refused_argument_sends_nothing(self):
        refused = [  # the argument that is refused, and the name the message gives it
            ({"provider_identifier": ""}, "provider_identifier"),
            ({"provider_identifier": "  "}, "provider_identifier"),
            ({"provider_identifier": None}, "provider_identifier"),
            ({"provider_identifier": 7}, "provider_identifier"),
            ({"provider_identifier": "x" * 256}, "provider_identifier"),
            ({"provider_identifier": CONNECTOR, "run_id": None}, "run_id"),
            ({"provider_identifier": CONNECTOR, "run_id": 7}, "run_id"),
            ({"provider_identifier": CONNECTOR, "run_id": b"latest"}, "run_id"),
            ({"provider_identifier": CONNECTOR, "run_id": "x" * 256}, "run_id"),
            ({"provider_identifier": CONNECTOR, "run_id": f"{'x' * 256}\n"}, "run_id"),
        ]
        for arguments, name in refused:
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError) as error:
                    self.actions.get_tool_collection_run(**arguments)
                self.assertIn(name, str(error.exception))
        self.assertEqual(self.channel.sent, [], "nothing is sent when an argument is refused")

    def test_255_characters_are_accepted_whatever_surrounds_them(self):
        longest = "x" * 255
        self._reply(_run(), _run())
        self.actions.get_tool_collection_run(provider_identifier=longest, run_id=f" {longest}\n")
        self.actions.get_tool_collection_run(provider_identifier=f"\n{longest} ", run_id=longest)
        self.assertEqual(
            [(s.request.provider_identifier, s.request.run_id) for s in self.channel.sent], [(longest, longest)] * 2
        )

    def test_the_call_is_made_with_the_defaults_of_every_other_call(self):
        self._reply(_run(), _run())
        with patch.object(self.core, "grpc_exec", wraps=self.core.grpc_exec) as grpc_exec:
            self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
            self.actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id=RUN_ID)
        self.assertPlainCall(grpc_exec.call_args_list)

    def test_server_errors_reach_the_caller_as_the_sdk_maps_them(self):
        cases = [
            (
                StatusCode.NOT_FOUND,
                "tool collection run not found",
                "RESOURCE_NOT_FOUND",
                ScalekitNotFoundException,
                HTTPStatus.NOT_FOUND,
            ),
            (
                StatusCode.INVALID_ARGUMENT,
                "invalid run_id",
                "INVALID_ARGUMENT",
                ScalekitBadRequestException,
                HTTPStatus.BAD_REQUEST,
            ),
        ]
        for code, message, error_code, expected, http_status in cases:
            with self.subTest(error_code=error_code, message=message):
                self.assertMapped(
                    code,
                    message,
                    error_code,
                    expected,
                    http_status,
                    lambda: self.actions.get_tool_collection_run(provider_identifier=CONNECTOR),
                )


class WithoutProvidersClientTest(ToolCollectionRunsTestCase):
    """The two methods need the tools client only: the providers layer is not involved."""

    def test_they_work_on_a_client_built_without_a_providers_client(self):
        with self.assertRaises(ValueError):
            self.actions.providers  # the providers layer is not there ...
        self._reply(_run(), _run())  # ... and the run methods do not need it
        self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertEqual([s.path for s in self.channel.sent], [INVOKE, GET_RUN])

    def test_a_providers_client_that_is_there_is_not_used(self):
        providers = MagicMock()
        actions = ActionClient(ToolsClient(self.core), MagicMock(), providers_client=providers)
        self._reply(_run(), _run())
        actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertEqual([s.path for s in self.channel.sent], [INVOKE, GET_RUN])
        self.assertEqual(providers.mock_calls, [])

    def test_the_provider_service_stub_is_built_on_first_use_and_kept(self):
        def provider_paths():
            return [path for path in self.channel.stubbed if "ProviderService" in path]

        self.assertEqual(provider_paths(), [], "nothing is built before a call needs it")
        self._reply(_run(), _run(), _run())
        self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        built = provider_paths()
        self.assertIn(INVOKE, built)
        self.assertIn(GET_RUN, built)
        self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        self.assertEqual(provider_paths(), built, "the stub is built once")


class ScalekitClientTest(unittest.TestCase):
    def test_the_methods_work_on_scalekit_client_actions_and_on_scalekit_client_connect(self):
        channel = _FakeChannel()
        with patch("scalekit.client.CoreClient", return_value=_core_client(channel)):
            client = ScalekitClient("https://example.test", "cid", "secret")
        for name in ("actions", "connect"):  # connect is the older name of the same kind of client
            actions = getattr(client, name)
            with self.subTest(client=name):
                self.assertIsInstance(actions, ActionClient)
                channel.sent.clear()
                channel.script.extend([_run(), _run(status="COMPLETED")])
                queued = actions.invoke_tool_collection(provider_identifier=CONNECTOR)
                read = actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id=RUN_ID)
                self.assertEqual([s.path for s in channel.sent], [INVOKE, GET_RUN])
                self.assertEqual(
                    [s.body for s in channel.sent], [IDENTIFIER_FIELD, IDENTIFIER_FIELD + RUN_ID_FIELD]
                )
                self.assertIs(queued.status, ToolCollectionRunStatus.QUEUED)
                self.assertTrue(read.is_terminal)

    def test_delete_custom_tool_is_reachable_the_same_way(self):
        with patch("scalekit.client.CoreClient") as core_cls:
            core = core_cls.return_value = MagicMock()
            client = ScalekitClient("https://example.test", "cid", "secret")
        for actions in (client.actions, client.connect):
            core.grpc_exec.reset_mock()
            self.assertIsNone(actions.delete_custom_tool(tool_identifier=" a-acmeapi_deletepet "))
            (_, request), kwargs = core.grpc_exec.call_args.args, core.grpc_exec.call_args.kwargs
            self.assertEqual(request, DeleteCustomToolRequest(tool_identifier="a-acmeapi_deletepet"))
            self.assertEqual(kwargs, {})


class SignatureTest(unittest.TestCase):
    def test_the_calls_a_customer_writes(self):
        invoke = inspect.signature(ActionClient.invoke_tool_collection).parameters
        self.assertEqual(list(invoke), ["self", "provider_identifier", "kwargs"])
        self.assertIs(invoke["provider_identifier"].default, inspect.Parameter.empty)
        get = inspect.signature(ActionClient.get_tool_collection_run).parameters
        self.assertEqual(list(get), ["self", "provider_identifier", "run_id", "kwargs"])
        self.assertIs(get["provider_identifier"].default, inspect.Parameter.empty)
        self.assertEqual(get["run_id"].default, "latest")
        for parameter in (invoke["provider_identifier"], get["provider_identifier"], get["run_id"]):
            self.assertIs(parameter.kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for parameter in (invoke["kwargs"], get["kwargs"]):
            self.assertIs(parameter.kind, inspect.Parameter.VAR_KEYWORD)

    def test_the_methods_are_typed_and_the_run_types_are_exported(self):
        invoke = typing.get_type_hints(ActionClient.invoke_tool_collection)
        get = typing.get_type_hints(ActionClient.get_tool_collection_run)
        self.assertEqual((invoke["provider_identifier"], invoke["return"]), (str, ToolCollectionRun))
        self.assertEqual((get["provider_identifier"], get["run_id"], get["return"]), (str, str, ToolCollectionRun))
        for name, kind in (
            ("ToolCollectionRun", ToolCollectionRun),
            ("ToolCollectionRunStatus", ToolCollectionRunStatus),
            ("SkippedTool", SkippedTool),
        ):
            self.assertIn(name, exported.__all__)
            self.assertIs(getattr(exported, name), kind)


RUN_METHODS = ("invoke_tool_collection", "get_tool_collection_run")


def _text(method) -> str:
    """A docstring on one line, so that the wrapping of the lines does not matter."""
    return " ".join(method.__doc__.split())


class DocstringsTest(unittest.TestCase):
    def test_the_docstrings_show_the_call_a_customer_writes_with_the_connector_identifier(self):
        for name in RUN_METHODS:
            doc = _text(getattr(ActionClient, name))
            with self.subTest(name):
                self.assertIn(f"scalekit_client.actions.{name}(", doc)
                self.assertIn("ACMEAPI:70219645518265104", doc)
                self.assertIn("``NAME:environment-id``, from ``provider.identifier``), not ``provider.id``", doc)


if __name__ == "__main__":
    unittest.main()

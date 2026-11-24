"""Offline tests for the tool collection run methods on ``client.actions``.

``ActionClient.invoke_tool_collection`` and ``ActionClient.get_tool_collection_run`` are the same operations as
``actions.providers.invoke_tool_collection`` and ``actions.providers.get_tool_collection_run``, which keep working.

Only the gRPC channel is faked. The generated stub, the clients, and the client's real error mapping all run, so what
is checked is what would be put on the wire.
"""
import inspect
import typing
import unittest
from collections import namedtuple
from datetime import datetime, timezone
from unittest.mock import MagicMock, PropertyMock, patch

import grpc
from google.protobuf import any_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from google.rpc import status_pb2
from grpc import StatusCode
from pydantic import ValidationError

from scalekit.actions.actions import ActionClient, ActionProviders
from scalekit.actions.types import (
    GetToolCollectionRunRequest,
    InvokeToolCollectionRequest,
    ToolCollectionRun,
    ToolCollectionRunStatus,
)
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitConflictException,
    ScalekitNotFoundException,
)
from scalekit.core import DEFAULT_CALL_TIMEOUT_S, CoreClient
from scalekit.providers import ProvidersClient
from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo
from scalekit.v1.providers import providers_pb2 as pb
from scalekit.v1.tools.tools_pb2 import DeleteCustomToolRequest

INVOKE = "/scalekit.v1.providers.ProviderService/TriggerToolCollection"
GET_RUN = "/scalekit.v1.providers.ProviderService/GetToolCollectionRun"
CONNECTOR = "PETSTORE:12"
QUEUED_AT = datetime(2026, 11, 11, 9, 0, 0, tzinfo=timezone.utc)
FINISHED_AT = datetime(2026, 11, 11, 9, 0, 20, tzinfo=timezone.utc)
TOOL_CALL_TIMEOUT_S = 123.0  # unlike every default, so a call that uses another deadline shows

Sent = namedtuple("Sent", "path body timeout metadata")


def _timestamp(value: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(value)
    return ts


def _run(**kw) -> pb.ToolCollectionRun:
    kw.setdefault("run_id", "tcr_123")
    kw.setdefault("provider_identifier", CONNECTOR)
    kw.setdefault("status", "QUEUED")
    kw.setdefault("created_at", _timestamp(QUEUED_AT))
    return pb.ToolCollectionRun(**kw)


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
    """A CoreClient with the real error mapping and no network."""
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


class ToolCollectionRunsTestCase(unittest.TestCase):
    def setUp(self):
        self.channel = _FakeChannel()
        self.low = ProvidersClient(_core_client(self.channel))
        self.actions = ActionClient(MagicMock(), MagicMock(), providers_client=self.low)

    def _reply(self, *items):
        self.channel.script.extend(items)

    def _invoke_request(self, index: int = -1) -> pb.TriggerToolCollectionRequest:
        return pb.TriggerToolCollectionRequest.FromString(self.channel.sent[index].body)

    def _get_request(self, index: int = -1) -> pb.GetToolCollectionRunRequest:
        return pb.GetToolCollectionRunRequest.FromString(self.channel.sent[index].body)

    def assertSameError(self, code: StatusCode, message: str, error_code: str, expected: type, call, providers_call):
        """``call`` and the ``actions.providers`` form raise the same exception, as the server sent it."""
        self._reply(_rpc_error(code, message, error_code), _rpc_error(code, message, error_code))
        with self.assertRaises(expected) as direct:
            call()
        with self.assertRaises(expected) as through_providers:
            providers_call()
        for exception in (direct.exception, through_providers.exception):
            self.assertIs(type(exception), expected)  # not wrapped, not translated
            self.assertEqual(exception.message, message)
            self.assertEqual(exception.error_code, error_code)
        self.assertEqual(direct.exception.http_status, through_providers.exception.http_status)
        self.assertEqual(direct.exception.grpc_status, through_providers.exception.grpc_status)


class InvokeToolCollectionTest(ToolCollectionRunsTestCase):
    def test_queues_a_run_and_returns_it_typed(self):
        self._reply(_run())
        run = self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        self.assertEqual([s.path for s in self.channel.sent], [INVOKE])
        self.assertEqual(self._invoke_request(), pb.TriggerToolCollectionRequest(provider_identifier=CONNECTOR))
        self.assertIsInstance(run, ToolCollectionRun)
        self.assertEqual((run.run_id, run.provider_identifier), ("tcr_123", CONNECTOR))
        self.assertIs(run.status, ToolCollectionRunStatus.QUEUED)
        self.assertFalse(run.is_terminal)
        self.assertEqual(run.created_at, QUEUED_AT)

    def test_the_identifier_may_be_passed_by_position(self):
        self._reply(_run())
        self.actions.invoke_tool_collection(CONNECTOR)
        self.assertEqual(self._invoke_request().provider_identifier, CONNECTOR)

    def test_the_whitespace_around_the_identifier_is_removed(self):
        for padded in (f"  {CONNECTOR}", f"{CONNECTOR}\n", f"\t{CONNECTOR} \r\n"):
            with self.subTest(identifier=padded):
                self._reply(_run())
                self.actions.invoke_tool_collection(provider_identifier=padded)
                self.assertEqual(self._invoke_request().provider_identifier, CONNECTOR)

    def test_a_blank_or_invalid_identifier_is_refused_before_anything_is_sent(self):
        for value in ("", " ", "\t\n", None, 7, "x" * 256):
            with self.subTest(identifier=value):
                with self.assertRaises(ValidationError) as refused:
                    self.actions.invoke_tool_collection(provider_identifier=value)
                self.assertIsInstance(refused.exception, ValueError)
                self.assertIn("provider_identifier", str(refused.exception))
        self.assertEqual(self.channel.sent, [], "nothing is sent when the identifier is refused")

    def test_the_client_default_deadline_applies(self):
        """No deadline of its own: the call uses the default, not the tool-call deadline, which differs here."""
        self._reply(_run())
        self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        self.assertEqual(self.channel.sent[0].timeout, DEFAULT_CALL_TIMEOUT_S)
        self.assertNotEqual(TOOL_CALL_TIMEOUT_S, DEFAULT_CALL_TIMEOUT_S)

    def test_server_errors_reach_the_caller_unchanged(self):
        request = InvokeToolCollectionRequest(provider_identifier=CONNECTOR)
        cases = [
            (StatusCode.NOT_FOUND, "provider not found", "RESOURCE_NOT_FOUND", ScalekitNotFoundException),
            (
                StatusCode.INVALID_ARGUMENT,
                "this connector is not sourced from an OpenAPI spec",
                "INVALID_ARGUMENT",
                ScalekitBadRequestException,
            ),
            (StatusCode.INVALID_ARGUMENT, "feature not enabled", "FEATURE_NOT_ENABLED", ScalekitBadRequestException),
            (
                StatusCode.ALREADY_EXISTS,
                "an ingestion run is already in progress for this connector",
                "RESOURCE_ALREADY_EXISTS",
                ScalekitConflictException,
            ),
        ]
        for code, message, error_code, expected in cases:
            with self.subTest(error_code=error_code):
                self.assertSameError(
                    code,
                    message,
                    error_code,
                    expected,
                    lambda: self.actions.invoke_tool_collection(provider_identifier=CONNECTOR),
                    lambda: self.actions.providers.invoke_tool_collection(request),
                )


class GetToolCollectionRunTest(ToolCollectionRunsTestCase):
    def test_reads_the_latest_run_by_default(self):
        self._reply(_run(status="PROCESSING"))
        run = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertEqual([s.path for s in self.channel.sent], [GET_RUN])
        self.assertEqual(
            self._get_request(), pb.GetToolCollectionRunRequest(provider_identifier=CONNECTOR, run_id="latest")
        )
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
        self.actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id="tcr_999")
        self.actions.get_tool_collection_run(CONNECTOR, "tcr_999")
        self.assertEqual(
            [(self._get_request(i).provider_identifier, self._get_request(i).run_id) for i in (0, 1)],
            [(CONNECTOR, "tcr_999")] * 2,
        )

    def test_an_empty_or_blank_run_id_is_sent_as_latest(self):
        for blank in ("", " ", "\t\n"):
            with self.subTest(run_id=blank):
                self._reply(_run())
                self.actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id=blank)
                self.assertEqual(self._get_request().run_id, "latest")

    def test_the_whitespace_around_the_identifier_and_the_run_id_is_removed(self):
        self._reply(_run())
        self.actions.get_tool_collection_run(provider_identifier=f"\t{CONNECTOR} ", run_id=" tcr_999\n")
        request = self._get_request()
        self.assertEqual((request.provider_identifier, request.run_id), (CONNECTOR, "tcr_999"))

    def test_a_blank_or_invalid_identifier_or_run_id_is_refused_before_anything_is_sent(self):
        refused = [
            {"provider_identifier": ""},
            {"provider_identifier": "  "},
            {"provider_identifier": None},
            {"provider_identifier": 7},
            {"provider_identifier": "x" * 256},
            {"provider_identifier": CONNECTOR, "run_id": None},
            {"provider_identifier": CONNECTOR, "run_id": 7},
            {"provider_identifier": CONNECTOR, "run_id": "x" * 256},
        ]
        for arguments in refused:
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValidationError) as error:
                    self.actions.get_tool_collection_run(**arguments)
                self.assertIsInstance(error.exception, ValueError)
        self.assertEqual(self.channel.sent, [], "nothing is sent when an argument is refused")

    def test_the_client_default_deadline_applies(self):
        self._reply(_run())
        self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertEqual(self.channel.sent[0].timeout, DEFAULT_CALL_TIMEOUT_S)
        self.assertNotEqual(TOOL_CALL_TIMEOUT_S, DEFAULT_CALL_TIMEOUT_S)

    def test_a_finished_run_is_decoded_with_its_counters_and_skipped_operations(self):
        self._reply(
            _run(
                status="COMPLETED",
                total_endpoints=12,
                tools_created=9,
                tools_updated=1,
                tools_deleted=2,
                skipped_tools_json='[{"operation_id": "uploadFile", "method": "POST", "path": "/files", "reason": "r"}]',
                finished_at=_timestamp(FINISHED_AT),
            )
        )
        run = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertTrue(run.is_terminal)
        self.assertEqual((run.total_endpoints, run.tools_created, run.tools_updated, run.tools_deleted), (12, 9, 1, 2))
        self.assertEqual(run.finished_at, FINISHED_AT)
        self.assertEqual([t.operation_id for t in run.skipped_tools], ["uploadFile"])

    def test_server_errors_reach_the_caller_unchanged(self):
        request = GetToolCollectionRunRequest(provider_identifier=CONNECTOR)
        cases = [
            (StatusCode.NOT_FOUND, "tool collection run not found", "RESOURCE_NOT_FOUND", ScalekitNotFoundException),
            (StatusCode.INVALID_ARGUMENT, "invalid run_id", "INVALID_ARGUMENT", ScalekitBadRequestException),
        ]
        for code, message, error_code, expected in cases:
            with self.subTest(error_code=error_code, message=message):
                self.assertSameError(
                    code,
                    message,
                    error_code,
                    expected,
                    lambda: self.actions.get_tool_collection_run(provider_identifier=CONNECTOR),
                    lambda: self.actions.providers.get_tool_collection_run(request),
                )


class ProvidersFormTest(ToolCollectionRunsTestCase):
    """The methods of ``actions`` delegate to ``actions.providers``, which keeps its own methods."""

    def test_the_methods_delegate_to_actions_providers_with_the_typed_request(self):
        providers = MagicMock(spec=ActionProviders)
        with patch.object(ActionClient, "providers", new_callable=PropertyMock, return_value=providers):
            invoked = self.actions.invoke_tool_collection(provider_identifier=f" {CONNECTOR} ")
            latest = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
            by_id = self.actions.get_tool_collection_run(CONNECTOR, run_id="tcr_9")
        providers.invoke_tool_collection.assert_called_once_with(
            InvokeToolCollectionRequest(provider_identifier=CONNECTOR)
        )
        self.assertEqual(
            providers.get_tool_collection_run.call_args_list[0].args,
            (GetToolCollectionRunRequest(provider_identifier=CONNECTOR, run_id="latest"),),
        )
        self.assertEqual(
            providers.get_tool_collection_run.call_args_list[1].args,
            (GetToolCollectionRunRequest(provider_identifier=CONNECTOR, run_id="tcr_9"),),
        )
        # what the providers form returns is what the caller gets: nothing is added or converted
        self.assertIs(invoked, providers.invoke_tool_collection.return_value)
        self.assertIs(latest, providers.get_tool_collection_run.return_value)
        self.assertIs(by_id, providers.get_tool_collection_run.return_value)

    def test_the_providers_form_still_sends_the_same_calls(self):
        self._reply(_run(), _run(), _run(), _run())
        direct_invoke = self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        providers_invoke = self.actions.providers.invoke_tool_collection(
            InvokeToolCollectionRequest(provider_identifier=CONNECTOR)
        )
        direct_get = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR, run_id="tcr_9")
        providers_get = self.actions.providers.get_tool_collection_run(
            GetToolCollectionRunRequest(provider_identifier=CONNECTOR, run_id="tcr_9")
        )
        sent = self.channel.sent
        self.assertEqual([s.path for s in sent], [INVOKE, INVOKE, GET_RUN, GET_RUN])
        self.assertEqual(sent[0].body, sent[1].body)
        self.assertEqual(sent[2].body, sent[3].body)
        self.assertEqual(direct_invoke, providers_invoke)
        self.assertEqual(direct_get, providers_get)

    def test_the_providers_form_keeps_its_signature(self):
        self.assertEqual(list(inspect.signature(ActionProviders.invoke_tool_collection).parameters), ["self", "request"])
        self.assertEqual(
            list(inspect.signature(ActionProviders.get_tool_collection_run).parameters), ["self", "request"]
        )

    def test_a_client_built_without_a_providers_client_sends_nothing(self):
        actions = ActionClient(MagicMock(), MagicMock())
        with self.assertRaises(ValueError):
            actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        with self.assertRaises(ValueError):
            actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertEqual(self.channel.sent, [])


class SignatureTest(unittest.TestCase):
    def test_the_calls_a_customer_writes(self):
        invoke = inspect.signature(ActionClient.invoke_tool_collection).parameters
        self.assertEqual(list(invoke)[:2], ["self", "provider_identifier"])
        self.assertIs(invoke["provider_identifier"].default, inspect.Parameter.empty)
        get = inspect.signature(ActionClient.get_tool_collection_run).parameters
        self.assertEqual(list(get)[:3], ["self", "provider_identifier", "run_id"])
        self.assertIs(get["provider_identifier"].default, inspect.Parameter.empty)
        self.assertEqual(get["run_id"].default, "latest")
        for parameter in (invoke["provider_identifier"], get["provider_identifier"], get["run_id"]):
            self.assertIs(parameter.kind, inspect.Parameter.POSITIONAL_OR_KEYWORD)

    def test_the_methods_are_typed_and_the_types_are_exported(self):
        import scalekit.actions.types as exported

        invoke = typing.get_type_hints(ActionClient.invoke_tool_collection)
        get = typing.get_type_hints(ActionClient.get_tool_collection_run)
        self.assertEqual((invoke["provider_identifier"], invoke["return"]), (str, ToolCollectionRun))
        self.assertEqual((get["provider_identifier"], get["run_id"], get["return"]), (str, str, ToolCollectionRun))
        for name in (
            "ToolCollectionRun",
            "ToolCollectionRunStatus",
            "SkippedTool",
            "InvokeToolCollectionRequest",
            "GetToolCollectionRunRequest",
        ):
            self.assertIn(name, exported.__all__)
            self.assertTrue(hasattr(exported, name))


class ScalekitClientTest(unittest.TestCase):
    def test_the_methods_are_reachable_as_scalekit_client_actions_methods(self):
        from scalekit import ScalekitClient

        with patch("scalekit.client.CoreClient") as core_cls:
            core = core_cls.return_value = MagicMock()
            client = ScalekitClient("https://example.test", "cid", "secret")
        sent = []

        def grpc_exec(rpc, request, **kwargs):
            sent.append((request, kwargs))
            return (_run(provider_identifier=request.provider_identifier), None)

        core.grpc_exec.side_effect = grpc_exec
        for actions in (client.actions, client.connect):  # connect is the older name of the same client
            sent.clear()
            queued = actions.invoke_tool_collection(provider_identifier="ACMEAPI:70219645518265104")
            read = actions.get_tool_collection_run(provider_identifier="ACMEAPI:70219645518265104", run_id="latest")
            self.assertEqual((queued.provider_identifier, read.provider_identifier), ("ACMEAPI:70219645518265104",) * 2)
            self.assertEqual(
                [request for request, _ in sent],
                [
                    pb.TriggerToolCollectionRequest(provider_identifier="ACMEAPI:70219645518265104"),
                    pb.GetToolCollectionRunRequest(provider_identifier="ACMEAPI:70219645518265104", run_id="latest"),
                ],
            )
            for _, kwargs in sent:
                self.assertIsNone(kwargs.get("timeout"))  # no deadline of its own

    def test_delete_custom_tool_is_reachable_the_same_way(self):
        from scalekit import ScalekitClient

        with patch("scalekit.client.CoreClient") as core_cls:
            core = core_cls.return_value = MagicMock()
            client = ScalekitClient("https://example.test", "cid", "secret")
        for actions in (client.actions, client.connect):
            core.grpc_exec.reset_mock()
            self.assertIsNone(actions.delete_custom_tool(tool_identifier=" a-acmeapi_deletepet "))
            (_, request), kwargs = core.grpc_exec.call_args.args, core.grpc_exec.call_args.kwargs
            self.assertEqual(request, DeleteCustomToolRequest(tool_identifier="a-acmeapi_deletepet"))
            self.assertNotIn("timeout", kwargs)  # no deadline of its own


class DocstringsTest(unittest.TestCase):
    """The docstrings name the call a customer writes first, and the ``actions.providers`` form after it."""

    def test_the_actions_form_is_named_first(self):
        forms = {
            "invoke_tool_collection": "scalekit_client.actions.invoke_tool_collection(provider_identifier",
            "get_tool_collection_run": "scalekit_client.actions.get_tool_collection_run(provider_identifier",
            "delete_custom_tool": "scalekit_client.actions.delete_custom_tool(tool_identifier",
        }
        for name, form in forms.items():
            doc = getattr(ActionClient, name).__doc__
            with self.subTest(name):
                self.assertIn(form, doc)
                self.assertEqual(doc.index(form), doc.index("scalekit_client.actions."), "the first call form is the actions one")

    def test_the_providers_form_is_named_after_it(self):
        for name in ("invoke_tool_collection", "get_tool_collection_run"):
            doc = getattr(ActionClient, name).__doc__
            with self.subTest(name):
                providers_form = f"scalekit_client.actions.providers.{name}(request)"
                self.assertIn(providers_form, doc)
                self.assertLess(doc.index(f"scalekit_client.actions.{name}("), doc.index(providers_form))
            # and the providers form points back at the actions one
            self.assertIn(f"scalekit_client.actions.{name}(provider_identifier=", getattr(ActionProviders, name).__doc__)

    def test_no_docstring_of_these_calls_names_a_deadline_of_their_own(self):
        documented = [
            ActionClient.invoke_tool_collection, ActionClient.get_tool_collection_run, ActionClient.delete_custom_tool,
            ActionProviders.create_custom_provider, ActionProviders.update_custom_provider,
            ActionProviders.invoke_tool_collection, ActionProviders.get_tool_collection_run,
            ProvidersClient.create_custom_provider, ProvidersClient.update_custom_provider,
            ProvidersClient.invoke_tool_collection, ProvidersClient.get_tool_collection_run,
        ]
        for method in documented:
            with self.subTest(method.__qualname__):
                for text in ("tool_call_timeout", "tool-call timeout", "longer deadline"):
                    self.assertNotIn(text, method.__doc__)


if __name__ == "__main__":
    unittest.main()

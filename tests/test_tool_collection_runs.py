"""Offline tests for tool collection runs of OpenAPI-sourced connectors: the gRPC layer is stubbed."""
import json
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import ValidationError

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import (
    GetToolCollectionRunRequest,
    SkippedTool,
    ToolCollectionRun,
    ToolCollectionRunStatus,
    TriggerToolCollectionRequest,
)
from scalekit.common.exceptions import (
    ScalekitBadRequestException,
    ScalekitConflictException,
    ScalekitNotFoundException,
)
from scalekit.providers import ProvidersClient
from scalekit.v1.providers import providers_pb2 as pb

CONNECTOR = "PETSTORE:12"
QUEUED_AT = datetime(2026, 11, 11, 9, 0, 0, tzinfo=timezone.utc)
STARTED_AT = datetime(2026, 11, 11, 9, 0, 5, tzinfo=timezone.utc)
FINISHED_AT = datetime(2026, 11, 11, 9, 0, 20, tzinfo=timezone.utc)


def _timestamp(value: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(value)
    return ts


def _server_error(cls, message, code):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


def _run(**kw) -> pb.ToolCollectionRun:
    kw.setdefault("run_id", "tcr_123")
    kw.setdefault("provider_identifier", CONNECTOR)
    kw.setdefault("status", "QUEUED")
    kw.setdefault("created_at", _timestamp(QUEUED_AT))
    return pb.ToolCollectionRun(**kw)


class RunsTestCase(unittest.TestCase):
    def setUp(self):
        self.core = MagicMock()
        self.calls = []
        self.low = ProvidersClient(self.core)
        self.client = ActionClient(MagicMock(), MagicMock(), providers_client=self.low)

    def _reply(self, *responses):
        queue = list(responses)

        def grpc_exec(rpc, request, **kwargs):
            self.calls.append((rpc, request, kwargs))
            item = queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return (item, None)

        self.core.grpc_exec.side_effect = grpc_exec


class TriggerToolCollectionTest(RunsTestCase):
    def test_returns_the_queued_run(self):
        self._reply(_run())
        run = self.client.providers.trigger_tool_collection(
            TriggerToolCollectionRequest(provider_identifier=CONNECTOR)
        )
        self.assertEqual(self.calls[0][1].provider_identifier, CONNECTOR)
        self.assertEqual(run.run_id, "tcr_123")
        self.assertEqual(run.provider_identifier, CONNECTOR)
        self.assertEqual(run.status, ToolCollectionRunStatus.QUEUED)
        self.assertFalse(run.is_terminal)
        self.assertEqual(run.created_at, QUEUED_AT)
        self.assertIsNone(run.started_at)
        self.assertIsNone(run.finished_at)

    def test_is_not_retried_and_uses_the_longer_deadline(self):
        self._reply(_run())
        self.low.trigger_tool_collection(CONNECTOR)
        kwargs = self.calls[0][2]
        self.assertFalse(kwargs["retry_on_unavailable"])
        self.assertIs(kwargs["timeout"], self.core.tool_call_timeout_s)

    def test_server_rejections_reach_the_caller_unchanged(self):
        self._reply(
            _server_error(ScalekitNotFoundException, "provider not found", "NOT_FOUND"),
            _server_error(
                ScalekitBadRequestException, "this connector is not sourced from an OpenAPI spec", "INVALID_ARGUMENT"
            ),
            _server_error(
                ScalekitConflictException,
                "an ingestion run is already in progress for this connector",
                "RESOURCE_ALREADY_EXISTS",
            ),
        )
        request = TriggerToolCollectionRequest(provider_identifier=CONNECTOR)
        with self.assertRaises(ScalekitNotFoundException):
            self.client.providers.trigger_tool_collection(request)
        with self.assertRaises(ScalekitBadRequestException) as not_openapi:
            self.client.providers.trigger_tool_collection(request)
        self.assertIn("not sourced from an OpenAPI spec", not_openapi.exception.message)
        with self.assertRaises(ScalekitConflictException) as running:
            self.client.providers.trigger_tool_collection(request)
        self.assertEqual(running.exception.error_code, "RESOURCE_ALREADY_EXISTS")

    def test_identifier_is_required_and_bounded(self):
        with self.assertRaises(ValidationError):
            TriggerToolCollectionRequest(provider_identifier="")
        with self.assertRaises(ValidationError):
            TriggerToolCollectionRequest(provider_identifier="x" * 256)
        TriggerToolCollectionRequest(provider_identifier="x" * 255)


class GetToolCollectionRunTest(RunsTestCase):
    def test_latest_is_the_default(self):
        self._reply(_run(status="PROCESSING", started_at=_timestamp(STARTED_AT)))
        run = self.client.providers.get_tool_collection_run(GetToolCollectionRunRequest(provider_identifier=CONNECTOR))
        request = self.calls[0][1]
        self.assertEqual((request.provider_identifier, request.run_id), (CONNECTOR, "latest"))
        self.assertEqual(run.status, ToolCollectionRunStatus.PROCESSING)
        self.assertFalse(run.is_terminal)
        self.assertEqual(run.started_at, STARTED_AT)

    def test_a_run_can_be_read_by_id(self):
        self._reply(_run())
        self.client.providers.get_tool_collection_run(
            GetToolCollectionRunRequest(provider_identifier=CONNECTOR, run_id="tcr_999")
        )
        self.assertEqual(self.calls[0][1].run_id, "tcr_999")

    def test_an_empty_run_id_is_sent_empty_and_means_latest_to_the_server(self):
        self._reply(_run())
        self.low.get_tool_collection_run(CONNECTOR, "")
        self.assertEqual(self.calls[0][1].run_id, "")

    def test_a_read_is_retried_like_any_other_read(self):
        self._reply(_run())
        self.low.get_tool_collection_run(CONNECTOR)
        self.assertNotIn("retry_on_unavailable", self.calls[0][2])

    def test_a_completed_run_reports_counters_and_skipped_operations(self):
        skipped = [
            {
                "operation_id": "uploadFile",
                "method": "POST",
                "path": "/files",
                "reason": "request body has no application/json, application/x-www-form-urlencoded, "
                "or plain-string representation",
            },
            {"method": "HEAD", "path": "/pets", "reason": "HTTP method has no meaningful agent-callable action"},
        ]
        self._reply(
            _run(
                status="COMPLETED",
                total_endpoints=12,
                tools_created=9,
                tools_updated=1,
                tools_deleted=2,
                skipped_tools_json=json.dumps(skipped),
                started_at=_timestamp(STARTED_AT),
                finished_at=_timestamp(FINISHED_AT),
            )
        )
        run = self.client.providers.get_tool_collection_run(GetToolCollectionRunRequest(provider_identifier=CONNECTOR))
        self.assertEqual(run.status, "COMPLETED")
        self.assertTrue(run.is_terminal)
        self.assertEqual((run.total_endpoints, run.tools_created, run.tools_updated, run.tools_deleted), (12, 9, 1, 2))
        self.assertEqual(run.finished_at, FINISHED_AT)
        self.assertEqual(run.error_message, "")
        self.assertEqual([t.operation_id for t in run.skipped_tools], ["uploadFile", ""])
        self.assertEqual(run.skipped_tools[0].method, "POST")
        self.assertEqual(run.skipped_tools[0].path, "/files")
        self.assertIn("no application/json", run.skipped_tools[0].reason)
        self.assertEqual(json.loads(run.skipped_tools_json), skipped)  # the raw text stays available

    def test_a_failed_run_carries_its_error_and_still_lists_what_was_skipped(self):
        self._reply(
            _run(
                status="FAILED",
                error_message="spec resolved to zero convertible endpoints (1 skipped)",
                skipped_tools_json=json.dumps([{"operation_id": "x", "method": "POST", "path": "/x", "reason": "r"}]),
                finished_at=_timestamp(FINISHED_AT),
            )
        )
        run = self.client.providers.get_tool_collection_run(GetToolCollectionRunRequest(provider_identifier=CONNECTOR))
        self.assertEqual(run.status, ToolCollectionRunStatus.FAILED)
        self.assertTrue(run.is_terminal)
        self.assertIn("zero convertible endpoints", run.error_message)
        self.assertEqual(len(run.skipped_tools), 1)

    def test_server_rejections_reach_the_caller_unchanged(self):
        self._reply(
            _server_error(ScalekitNotFoundException, "tool collection run not found", "NOT_FOUND"),
            _server_error(ScalekitBadRequestException, "invalid run_id", "INVALID_ARGUMENT"),
        )
        request = GetToolCollectionRunRequest(provider_identifier=CONNECTOR)
        with self.assertRaises(ScalekitNotFoundException) as none_yet:
            self.client.providers.get_tool_collection_run(request)
        self.assertIn("not found", none_yet.exception.message)
        with self.assertRaises(ScalekitBadRequestException) as malformed:
            self.client.providers.get_tool_collection_run(request)
        self.assertEqual(malformed.exception.message, "invalid run_id")

    def test_request_bounds(self):
        with self.assertRaises(ValidationError):
            GetToolCollectionRunRequest(provider_identifier="")
        with self.assertRaises(ValidationError):
            GetToolCollectionRunRequest(provider_identifier=CONNECTOR, run_id="x" * 256)
        self.assertEqual(GetToolCollectionRunRequest(provider_identifier=CONNECTOR).run_id, "latest")


class ToolCollectionRunModelTest(unittest.TestCase):
    def test_skipped_tools_json_is_decoded_permissively(self):
        cases = {
            "unset": ("", []),
            "blank": ("  ", []),
            "null": ("null", []),
            "empty array": ("[]", []),
            "not json": ("{oops", []),
            "not an array": ('{"operation_id": "x"}', []),
            "non-object entries are ignored": ('[1, "two", null]', []),
        }
        for name, (raw, expected) in cases.items():
            with self.subTest(name):
                run = ToolCollectionRun.from_proto(_run(status="COMPLETED", skipped_tools_json=raw))
                self.assertEqual(run.skipped_tools, expected)
                self.assertEqual(run.skipped_tools_json, raw)

    def test_an_entry_with_only_a_reason_decodes(self):
        """The server reports a failed clean-up of removed tools with a reason and nothing else."""
        raw = json.dumps([{"method": "", "path": "", "reason": "stale-tool deletion failed"}])
        (entry,) = ToolCollectionRun.from_proto(_run(status="COMPLETED", skipped_tools_json=raw)).skipped_tools
        self.assertEqual((entry.operation_id, entry.method, entry.path), ("", "", ""))
        self.assertEqual(entry.reason, "stale-tool deletion failed")

    def test_unknown_keys_and_null_values_in_an_entry_are_tolerated(self):
        entry = SkippedTool.from_dict({"operation_id": None, "method": "GET", "path": "/p", "reason": "r", "code": 7})
        self.assertEqual(entry.operation_id, "")
        self.assertEqual(entry.model_extra, {"code": 7})

    def test_an_unknown_status_is_kept_as_a_string(self):
        run = ToolCollectionRun.from_proto(_run(status="CANCELLED"))
        self.assertEqual(run.status, "CANCELLED")
        self.assertNotIsInstance(run.status, ToolCollectionRunStatus)
        self.assertFalse(run.is_terminal)

    def test_only_completed_and_failed_are_terminal(self):
        terminal = {
            status: ToolCollectionRun.from_proto(_run(status=status)).is_terminal
            for status in ("QUEUED", "PROCESSING", "COMPLETED", "FAILED")
        }
        self.assertEqual(terminal, {"QUEUED": False, "PROCESSING": False, "COMPLETED": True, "FAILED": True})

    def test_unset_instants_are_none_and_set_ones_are_aware_utc(self):
        run = ToolCollectionRun.from_proto(_run(started_at=_timestamp(STARTED_AT)))
        self.assertEqual(run.created_at.tzinfo, timezone.utc)
        self.assertEqual(run.started_at, STARTED_AT)
        self.assertIsNone(run.finished_at)

    def test_the_model_is_frozen(self):
        run = ToolCollectionRun.from_proto(_run())
        with self.assertRaises(ValidationError):
            run.status = "COMPLETED"


if __name__ == "__main__":
    unittest.main()

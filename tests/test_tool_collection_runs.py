"""Offline tests for what the tool collection run methods of ``client.actions`` return, and for the run model.

The gRPC layer is stubbed. What the methods send, and how the server's errors reach the caller, is tested in
test_actions_tool_collection_runs.py.
"""
import json
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import ValidationError

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import SkippedTool, ToolCollectionRun, ToolCollectionRunStatus
from scalekit.tools import ToolsClient
from scalekit.v1.providers import providers_pb2 as pb

CONNECTOR = "ACMEAPI:70219645518265104"
RUN_ID = "tcr_153432495495315592"
QUEUED_AT = datetime(2026, 11, 11, 9, 0, 0, tzinfo=timezone.utc)
STARTED_AT = datetime(2026, 11, 11, 9, 0, 5, tzinfo=timezone.utc)
FINISHED_AT = datetime(2026, 11, 11, 9, 0, 20, tzinfo=timezone.utc)


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


class RunsTestCase(unittest.TestCase):
    def setUp(self):
        self.core = MagicMock()
        # No ProvidersClient: the two methods call through the tools client's core client, like delete_custom_tool.
        self.actions = ActionClient(ToolsClient(self.core), MagicMock())

    def _reply(self, response: pb.ToolCollectionRun):
        self.core.grpc_exec.return_value = (response, None)


class InvokeToolCollectionTest(RunsTestCase):
    def test_returns_the_queued_run(self):
        self._reply(_run())
        run = self.actions.invoke_tool_collection(provider_identifier=CONNECTOR)
        self.assertIsInstance(run, ToolCollectionRun)
        self.assertEqual(run.run_id, RUN_ID)
        self.assertEqual(run.provider_identifier, CONNECTOR)
        self.assertEqual(run.status, ToolCollectionRunStatus.QUEUED)
        self.assertFalse(run.is_terminal)
        self.assertEqual(run.created_at, QUEUED_AT)
        self.assertIsNone(run.started_at)
        self.assertIsNone(run.finished_at)
        self.assertEqual((run.total_endpoints, run.tools_created, run.tools_updated, run.tools_deleted), (0, 0, 0, 0))
        self.assertEqual(run.skipped_tools, ())


class GetToolCollectionRunTest(RunsTestCase):
    def test_a_run_in_progress_is_not_terminal(self):
        self._reply(_run(status="PROCESSING", started_at=_timestamp(STARTED_AT)))
        run = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertEqual(run.status, ToolCollectionRunStatus.PROCESSING)
        self.assertFalse(run.is_terminal)
        self.assertEqual(run.started_at, STARTED_AT)
        self.assertIsNone(run.finished_at)

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
        run = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
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
        run = self.actions.get_tool_collection_run(provider_identifier=CONNECTOR)
        self.assertEqual(run.status, ToolCollectionRunStatus.FAILED)
        self.assertTrue(run.is_terminal)
        self.assertIn("zero convertible endpoints", run.error_message)
        self.assertEqual(len(run.skipped_tools), 1)


class BothMethodsTest(RunsTestCase):
    def test_both_return_what_the_model_makes_of_the_response(self):
        response = _run(
            status="COMPLETED",
            total_endpoints=3,
            tools_created=2,
            tools_updated=1,
            skipped_tools_json=json.dumps([{"method": "POST", "path": "/files", "reason": "r"}]),
            started_at=_timestamp(STARTED_AT),
            finished_at=_timestamp(FINISHED_AT),
        )
        self._reply(response)
        expected = ToolCollectionRun.from_proto(response)
        self.assertEqual(self.actions.invoke_tool_collection(provider_identifier=CONNECTOR), expected)
        self.assertEqual(self.actions.get_tool_collection_run(provider_identifier=CONNECTOR), expected)


class ToolCollectionRunModelTest(unittest.TestCase):
    def test_a_deeply_nested_skipped_tools_json_gives_no_skipped_tools(self):
        """json.loads raises RecursionError (not ValueError) on absurd nesting; the run must still decode and keep the text."""
        raw = "[" * 100000 + "]" * 100000
        run = ToolCollectionRun.from_proto(_run(status="COMPLETED", skipped_tools_json=raw))
        self.assertEqual(run.skipped_tools, ())
        self.assertEqual(run.skipped_tools_json, raw)

    def test_skipped_tools_json_is_decoded_permissively(self):
        cases = {
            "unset": ("", ()),
            "blank": ("  ", ()),
            "null": ("null", ()),
            "empty array": ("[]", ()),
            "not json": ("{oops", ()),
            "not an array": ('{"operation_id": "x"}', ()),
            "non-object entries are ignored": ('[1, "two", null]', ()),
        }
        for name, (raw, expected) in cases.items():
            with self.subTest(name):
                run = ToolCollectionRun.from_proto(_run(status="COMPLETED", skipped_tools_json=raw))
                self.assertEqual(run.skipped_tools, expected)
                self.assertEqual(run.skipped_tools_json, raw)

    def test_the_skipped_tools_of_a_frozen_run_cannot_be_changed_in_place(self):
        raw = json.dumps([{"method": "GET", "path": "/p", "reason": "r"}])
        run = ToolCollectionRun.from_proto(_run(status="COMPLETED", skipped_tools_json=raw))
        self.assertIsInstance(run.skipped_tools, tuple)
        self.assertEqual(len(run.skipped_tools), 1)
        with self.assertRaises(AttributeError):
            run.skipped_tools.append(SkippedTool(reason="x"))
        with self.assertRaises(ValidationError):
            run.skipped_tools = ()
        self.assertEqual(ToolCollectionRun().skipped_tools, ())

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

    def test_a_known_status_is_a_member_however_the_run_was_built(self):
        """A JSON or dict round trip and a plain string give the member too; a newer status stays a str."""
        run = ToolCollectionRun.from_proto(_run(status="FAILED", error_message="spec resolved to zero endpoints"))
        self.assertIs(run.status, ToolCollectionRunStatus.FAILED)
        rebuilt = {
            "model_validate_json": ToolCollectionRun.model_validate_json(run.model_dump_json()),
            "model_validate of a JSON-mode dump": ToolCollectionRun.model_validate(run.model_dump(mode="json")),
            "constructor with a plain string": ToolCollectionRun(status="FAILED"),
        }
        for name, again in rebuilt.items():
            with self.subTest(name):
                self.assertIs(again.status, ToolCollectionRunStatus.FAILED)
                self.assertEqual(again.status.value, "FAILED")
                self.assertTrue(again.is_terminal)
        self.assertEqual(rebuilt["model_validate_json"], run)

        newer = ToolCollectionRun.from_proto(_run(status="CANCELLED"))
        again = ToolCollectionRun.model_validate_json(newer.model_dump_json())
        self.assertEqual(again.status, "CANCELLED")
        self.assertNotIsInstance(again.status, ToolCollectionRunStatus)
        self.assertFalse(again.is_terminal)

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

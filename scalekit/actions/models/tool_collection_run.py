"""Typed model of one OpenAPI tool collection run.

An OpenAPI-sourced custom connector gets its tools from a tool collection run: the
server fetches the connector's spec, converts every operation it can into a tool,
and records what it did. A run is queued when the connector is created, when its base
URL or spec URL changes, and when you call ``trigger_tool_collection``. It works in the
background, so read its progress with ``get_tool_collection_run``.

Conventions follow the other typed models: the model is frozen (fields cannot be
reassigned), keeps fields this SDK version does not know in ``model.model_extra``, gives
instants as timezone-aware UTC ``datetime`` (``None`` when the server sent none), and
holds an enum member for a known status and the plain ``str`` for a newer one.
"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from scalekit._convert import timestamp_from_proto

__all__ = ["SkippedTool", "ToolCollectionRun", "ToolCollectionRunStatus"]


class ToolCollectionRunStatus(str, Enum):
    """Where a tool collection run is. A run moves QUEUED, PROCESSING, then COMPLETED or FAILED."""

    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


_TERMINAL = (ToolCollectionRunStatus.COMPLETED, ToolCollectionRunStatus.FAILED)


class SkippedTool(BaseModel):
    """One spec operation a run could not turn into a tool, and why.

    The ``reason`` is human-readable text, not a stable code: show it, but do not match on
    it. An entry the server adds for a failed clean-up of removed tools carries only a
    ``reason``, so every other field is then empty.
    """

    model_config = ConfigDict(frozen=True, extra="allow")

    operation_id: str = Field("", description="The operation's operationId in the spec. Empty when the spec gives none.")
    method: str = Field("", description="HTTP method of the operation, for example 'POST'.")
    path: str = Field("", description="Path of the operation in the spec, for example '/pets/{petId}'.")
    reason: str = Field("", description="Why the operation was skipped.")

    @classmethod
    def from_dict(cls, d: dict) -> "SkippedTool":
        """Build from one entry of the server's skipped-tools JSON; keys this SDK does not know are kept."""
        known = {key: str(d.get(key) or "") for key in ("operation_id", "method", "path", "reason")}
        extras = {key: value for key, value in d.items() if key not in known}
        return cls(**known, **extras)


def _parse_skipped_tools(raw: str) -> List[SkippedTool]:
    """Read the server's skipped-tools JSON, which is empty or ``null`` when nothing was skipped.

    The server calls this field provisional, so decoding is permissive: text that is not a
    JSON array gives an empty list, and entries that are not objects are ignored. The
    original text stays available as ``ToolCollectionRun.skipped_tools_json``.
    """
    if not raw or not raw.strip():
        return []
    try:
        data = json.loads(raw)
    except ValueError:
        return []
    if not isinstance(data, list):
        return []
    return [SkippedTool.from_dict(item) for item in data if isinstance(item, dict)]


class ToolCollectionRun(BaseModel):
    """One run of the tool collection pipeline of an OpenAPI-sourced connector.

    Returned by ``trigger_tool_collection`` (a new run, ``QUEUED``) and
    ``get_tool_collection_run``. ``is_terminal`` tells you when to stop polling.
    """

    model_config = ConfigDict(frozen=True, extra="allow")

    run_id: str = Field("", description="This run's own ID.")
    provider_identifier: str = Field("", description="Identifier of the connector the run belongs to.")
    status: Union[ToolCollectionRunStatus, str] = Field(
        "",
        description=(
            "QUEUED, PROCESSING, COMPLETED or FAILED, as a ToolCollectionRunStatus member. "
            "A status this SDK version does not know is the plain string."
        ),
    )
    total_endpoints: int = Field(
        0,
        description=(
            "Number of operations found in the spec, before the ones that cannot become "
            "tools are filtered out. 0 until the run completes."
        ),
    )
    tools_created: int = Field(
        0, description="Number of tools this run created: operations the connector had no tool for yet."
    )
    tools_updated: int = Field(
        0, description="Number of existing tools this run refreshed, for example after a base URL change."
    )
    tools_deleted: int = Field(
        0,
        description=(
            "Number of tools deleted because their operation is no longer in the spec. Adding "
            "the operation back creates a new tool. A run that finds the spec, base URL and auth "
            "patterns unchanged since the last completed run reports 0 created, updated and "
            "deleted, and repeats that run's total_endpoints and skipped_tools. The server does "
            "not take that shortcut for a spec that references external files."
        ),
    )
    skipped_tools_json: str = Field(
        "",
        description=(
            "The server's own JSON text for skipped_tools. Empty until the run reaches a "
            "terminal status, and it can be the JSON text null when nothing was skipped (both "
            "read as no skipped tools)."
        ),
    )
    skipped_tools: List[SkippedTool] = Field(
        default_factory=list,
        description=(
            "The operations this run could not convert into tools, with the reason for each, "
            "parsed from skipped_tools_json. Empty until the run reaches a terminal status. A "
            "run that skipped some operations still completes; one that could not convert any "
            "operation fails and lists the skipped ones here."
        ),
    )
    error_message: str = Field("", description="Why the run failed. Empty unless the status is FAILED.")
    created_at: Optional[datetime] = Field(None, description="When the run was queued.")
    started_at: Optional[datetime] = Field(None, description="When ingestion began. None while the run is QUEUED.")
    finished_at: Optional[datetime] = Field(
        None, description="When the run reached COMPLETED or FAILED. None before that."
    )

    @property
    def is_terminal(self) -> bool:
        """True once the run is COMPLETED or FAILED and will not change again."""
        return self.status in _TERMINAL

    @classmethod
    def from_proto(cls, proto) -> "ToolCollectionRun":
        """Decode a proto ToolCollectionRun message."""
        status: Union[ToolCollectionRunStatus, str]
        try:
            status = ToolCollectionRunStatus(proto.status)
        except ValueError:
            status = proto.status
        return cls(
            run_id=proto.run_id,
            provider_identifier=proto.provider_identifier,
            status=status,
            total_endpoints=proto.total_endpoints,
            tools_created=proto.tools_created,
            tools_updated=proto.tools_updated,
            tools_deleted=proto.tools_deleted,
            skipped_tools_json=proto.skipped_tools_json,
            skipped_tools=_parse_skipped_tools(proto.skipped_tools_json),
            error_message=proto.error_message,
            created_at=timestamp_from_proto(proto, "created_at"),
            started_at=timestamp_from_proto(proto, "started_at"),
            finished_at=timestamp_from_proto(proto, "finished_at"),
        )

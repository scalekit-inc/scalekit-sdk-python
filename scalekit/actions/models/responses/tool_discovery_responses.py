"""Response models for the actions tool-discovery methods.

``list_scoped_tools``, ``list_available_tools`` and ``search_tools`` on ``client.actions``
return these instead of the raw protobuf responses, matching ``list_tools``.
"""
from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.responses.list_tools_response import Tool
from scalekit.v1.tools.tools_pb2 import ToolReadinessState

_READINESS_PREFIX = "TOOL_READINESS_STATE_"


def _readiness_name(value: int) -> str:
    """``TOOL_READINESS_STATE_READY`` -> ``READY``; an unknown number comes back as its string."""
    try:
        name = ToolReadinessState.Name(value)
    except ValueError:
        return str(value)
    return name[len(_READINESS_PREFIX):] if name.startswith(_READINESS_PREFIX) else name


class ScopedTool(BaseModel):
    """A tool together with the connected account it is scoped to"""

    tool: Optional[Tool] = Field(None, description="The tool")
    identifier: Optional[str] = Field(None, description="Connected-account identifier the tool is scoped to")
    connected_account_id: Optional[str] = Field(None, description="Connected account the tool runs against")

    @classmethod
    def from_proto(cls, proto_scoped) -> "ScopedTool":
        return cls(
            tool=Tool.from_proto(proto_scoped.tool) if proto_scoped.HasField("tool") else None,
            identifier=proto_scoped.identifier or None,
            connected_account_id=proto_scoped.connected_account_id or None,
        )

    def to_dict(self) -> dict:
        return {
            "tool": self.tool.to_dict() if self.tool else None,
            "identifier": self.identifier,
            "connected_account_id": self.connected_account_id,
        }


class ListScopedToolsResponse(BaseModel):
    """Response of ``client.actions.list_scoped_tools``"""

    tools: List[ScopedTool] = Field(default_factory=list, description="Tools in this page")
    total_count: Optional[int] = Field(None, description="Total number of matching tools")
    next_page_token: Optional[str] = Field(None, description="Token for the next page; None on the last page")
    previous_page_token: Optional[str] = Field(None, description="Token for the previous page")

    @classmethod
    def from_proto(cls, proto_response) -> "ListScopedToolsResponse":
        return cls(
            tools=[ScopedTool.from_proto(t) for t in proto_response.tools],
            total_count=proto_response.total_size,
            next_page_token=proto_response.next_page_token or None,
            previous_page_token=proto_response.prev_page_token or None,
        )

    def to_dict(self) -> dict:
        return {
            "tools": [t.to_dict() for t in self.tools],
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token,
        }


class ListAvailableToolsResponse(BaseModel):
    """Response of ``client.actions.list_available_tools``"""

    tools: List[Tool] = Field(default_factory=list, description="Tools in this page")
    total_count: Optional[int] = Field(None, description="Total number of available tools")
    next_page_token: Optional[str] = Field(None, description="Token for the next page; None on the last page")
    previous_page_token: Optional[str] = Field(None, description="Token for the previous page")

    @classmethod
    def from_proto(cls, proto_response) -> "ListAvailableToolsResponse":
        return cls(
            tools=[Tool.from_proto(t) for t in proto_response.tools],
            total_count=proto_response.total_size,
            next_page_token=proto_response.next_page_token or None,
            previous_page_token=proto_response.prev_page_token or None,
        )

    def to_dict(self) -> dict:
        return {
            "tools": [t.to_dict() for t in self.tools],
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token,
        }


class ConnectionReadiness(BaseModel):
    """Whether one of the identifier's connections can run a searched tool"""

    connection_name: Optional[str] = Field(None, description="The connection's name")
    connected_account_id: Optional[str] = Field(None, description="Connected account on that connection")
    readiness_state: Optional[str] = Field(
        None, description="READY, NEEDS_CONNECTION or NEEDS_REAUTH (UNSPECIFIED if the server sent none)"
    )

    @classmethod
    def from_proto(cls, proto_readiness) -> "ConnectionReadiness":
        return cls(
            connection_name=proto_readiness.connection_name or None,
            connected_account_id=proto_readiness.connected_account_id or None,
            readiness_state=_readiness_name(proto_readiness.readiness_state),
        )

    def to_dict(self) -> dict:
        return {
            "connection_name": self.connection_name,
            "connected_account_id": self.connected_account_id,
            "readiness_state": self.readiness_state,
        }


class SearchedTool(BaseModel):
    """One ranked result of ``client.actions.search_tools``"""

    name: Optional[str] = Field(None, description="Tool name, as passed to execute_tool")
    provider: Optional[str] = Field(None, description="Provider that exposes the tool")
    description: Optional[str] = Field(None, description="What the tool does")
    score: Optional[float] = Field(
        None, description="Relevance score, higher is better; comparable only within one response"
    )
    connections: List[ConnectionReadiness] = Field(
        default_factory=list,
        description="The identifier's connections for this provider; empty when no identifier was given "
                    "or the identifier has no connection for the provider",
    )

    @classmethod
    def from_proto(cls, proto_tool) -> "SearchedTool":
        return cls(
            name=proto_tool.name or None,
            provider=proto_tool.provider or None,
            description=proto_tool.description or None,
            score=proto_tool.score,
            connections=[ConnectionReadiness.from_proto(c) for c in proto_tool.connections],
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "provider": self.provider,
            "description": self.description,
            "score": self.score,
            "connections": [c.to_dict() for c in self.connections],
        }


class SearchToolsResponse(BaseModel):
    """Response of ``client.actions.search_tools``"""

    tools: List[SearchedTool] = Field(default_factory=list, description="Results, most relevant first")

    @classmethod
    def from_proto(cls, proto_response) -> "SearchToolsResponse":
        return cls(tools=[SearchedTool.from_proto(t) for t in proto_response.tools])

    def to_dict(self) -> dict:
        return {"tools": [t.to_dict() for t in self.tools]}

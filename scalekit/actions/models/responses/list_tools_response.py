from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from google.protobuf.json_format import MessageToDict


class Tool(BaseModel):
    """Tool item in list response with one-to-one mapping to proto Tool"""

    id: Optional[str] = Field(
        None,
        description="Unique identifier for the tool"
    )
    provider: Optional[str] = Field(
        None,
        description="Provider that exposes this tool (e.g., 'github', 'slack')"
    )
    definition: Optional[dict] = Field(
        None,
        description="Tool definition (schema/parameters) as a dictionary"
    )
    metadata: Optional[dict] = Field(
        None,
        description="Additional metadata for the tool"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags associated with the tool"
    )
    is_default: Optional[bool] = Field(
        None,
        description="Whether this is a default tool for its provider"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the tool was last updated"
    )

    @classmethod
    def from_proto(cls, proto_tool) -> 'Tool':
        """
        Create Tool from protobuf Tool

        :param proto_tool: The protobuf Tool object
        :type proto_tool: Tool (from tools_pb2)

        :returns:
            Tool instance
        """
        definition = None
        if proto_tool.HasField("definition"):
            definition = MessageToDict(proto_tool.definition)

        metadata = None
        if proto_tool.HasField("metadata"):
            metadata = MessageToDict(proto_tool.metadata)

        updated_at = None
        if proto_tool.HasField("updated_at"):
            updated_at = proto_tool.updated_at.ToDatetime()

        return cls(
            id=proto_tool.id if proto_tool.id else None,
            provider=proto_tool.provider if proto_tool.provider else None,
            definition=definition,
            metadata=metadata,
            tags=list(proto_tool.tags),
            is_default=proto_tool.is_default.value if proto_tool.HasField("is_default") else None,
            updated_at=updated_at
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation

        :returns:
            Dictionary representation of the tool
        """
        return {
            "id": self.id,
            "provider": self.provider,
            "definition": self.definition,
            "metadata": self.metadata,
            "tags": self.tags,
            "is_default": self.is_default,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ListToolsResponse(BaseModel):
    """List tools response with one-to-one mapping to proto ListToolsResponse"""

    tools: List[Tool] = Field(
        default_factory=list,
        description="List of tools"
    )
    tool_names: List[str] = Field(
        default_factory=list,
        description="Names of the tools in this page"
    )
    total_count: Optional[int] = Field(
        None,
        description="Total number of tools matching the request",
        alias="total_size"
    )
    next_page_token: Optional[str] = Field(
        None,
        description="Token for the next page of results"
    )
    previous_page_token: Optional[str] = Field(
        None,
        description="Token for the previous page of results",
        alias="prev_page_token"
    )

    @classmethod
    def from_proto(cls, proto_response) -> 'ListToolsResponse':
        """
        Create ListToolsResponse from protobuf ListToolsResponse

        :param proto_response: The protobuf ListToolsResponse object
        :type proto_response: ListToolsResponse (from tools_pb2)

        :returns:
            ListToolsResponse instance
        """
        tools = [Tool.from_proto(proto_tool) for proto_tool in proto_response.tools]

        return cls(
            tools=tools,
            tool_names=list(proto_response.tool_names),
            total_count=proto_response.total_size if proto_response.total_size else None,
            next_page_token=proto_response.next_page_token if proto_response.next_page_token else None,
            previous_page_token=proto_response.prev_page_token if proto_response.prev_page_token else None
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation

        :returns:
            Dictionary representation of the response
        """
        return {
            "tools": [tool.to_dict() for tool in self.tools],
            "tool_names": self.tool_names,
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

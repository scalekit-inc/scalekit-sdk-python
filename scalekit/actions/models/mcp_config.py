from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.v1.mcp.mcp_pb2 import (
    McpConfig as ProtoMcpConfig,
    McpConfigConnectionToolMapping as ProtoConfigMapping,
)


class McpConfigConnectionToolMapping(BaseModel):
    """Represents connection to tool mapping details for an MCP config."""

    connection_id: Optional[str] = Field(
        None,
        description="Unique identifier of the connected account mapping",
    )
    connection_name: Optional[str] = Field(
        None,
        description="Name of the connection associated with the mapping",
    )
    provider: Optional[str] = Field(
        None,
        description="Provider name for the connection",
    )
    tools: List[str] = Field(
        default_factory=list,
        description="List of tool names linked to this connection",
    )
    connected_account_id: Optional[str] = Field(
        None,
        description="Identifier for the backing connected account",
    )
    connected_account_status: Optional[str] = Field(
        None,
        description="Status of the connected account relationship",
    )

    def to_proto(self) -> ProtoConfigMapping:
        """Convert the model into a protobuf mapping.

        Only writable fields (connection_name, tools) are propagated to avoid sending
        read-only data such as connection identifiers or statuses back to the API.
        """

        mapping = ProtoConfigMapping()
        if self.connection_name is not None:
            mapping.connection_name = self.connection_name
        if self.tools:
            mapping.tools.extend(self.tools)
        return mapping

    @classmethod
    def from_proto(cls, proto_mapping: ProtoConfigMapping) -> "McpConfigConnectionToolMapping":
        """Instantiate the model from a protobuf mapping."""

        return cls(
            connection_id=proto_mapping.connection_id or None,
            connection_name=proto_mapping.connection_name or None,
            provider=proto_mapping.provider or None,
            tools=list(proto_mapping.tools),
            connected_account_id=proto_mapping.connected_account_id or None,
            connected_account_status=proto_mapping.connected_account_status or None,
        )


class McpConfig(BaseModel):
    """MCP configuration model with helpers for protobuf conversion."""

    id: Optional[str] = Field(None, description="Unique identifier for the MCP config")
    name: str = Field(..., description="Human readable name for the MCP config")
    description: Optional[str] = Field(None, description="Description of the MCP config")
    connection_tool_mappings: List[McpConfigConnectionToolMapping] = Field(
        default_factory=list,
        description="Mappings that connect tools to underlying connections",
    )

    def to_proto(self) -> ProtoMcpConfig:
        """Convert the model into a protobuf MCP config."""

        proto = self.to_proto_static(
            name=self.name,
            description=self.description,
            connection_tool_mappings=self.connection_tool_mappings,
        )
        if self.id is not None:
            proto.id = self.id
        return proto

    @staticmethod
    def to_proto_static(
        name: str,
        description: Optional[str] = None,
        connection_tool_mappings: Optional[List[McpConfigConnectionToolMapping]] = None,
    ) -> ProtoMcpConfig:
        """Build a protobuf MCP config from raw parameters."""

        proto = ProtoMcpConfig()
        proto.name = name
        if description is not None:
            proto.description = description
        if connection_tool_mappings:
            proto.connection_tool_mappings.extend(
                mapping.to_proto() for mapping in connection_tool_mappings
            )
        return proto

    @classmethod
    def from_proto(cls, proto_config: ProtoMcpConfig) -> "McpConfig":
        """Instantiate the model from a protobuf MCP config."""

        return cls(
            id=proto_config.id or None,
            name=proto_config.name,
            description=proto_config.description or None,
            connection_tool_mappings=[
                McpConfigConnectionToolMapping.from_proto(mapping)
                for mapping in proto_config.connection_tool_mappings
            ],
        )

    def to_dict(self) -> dict:
        """Convert the MCP config into a serialisable dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "connection_tool_mappings": [
                mapping.model_dump() for mapping in self.connection_tool_mappings
            ],
        }

    class Config:
        """Pydantic configuration options."""

        validate_assignment = True

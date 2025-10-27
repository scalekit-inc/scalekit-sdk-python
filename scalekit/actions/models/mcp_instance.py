from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_config import McpConfig
from scalekit.v1.mcp.mcp_pb2 import (
    McpInstance as ProtoMcpInstance,
    McpInstanceConnectionAuthState as ProtoConnectionAuthState,
)


class McpInstance(BaseModel):
    """Representation of an MCP instance returned by the API."""

    id: Optional[str] = Field(None, description="Unique identifier for the MCP instance")
    name: Optional[str] = Field(None, description="Display name for the instance")
    user_identifier: Optional[str] = Field(None, description="User identifier associated with the instance")
    config: Optional[McpConfig] = Field(None, description="Backed MCP configuration")
    last_used_at: Optional[datetime] = Field(None, description="Timestamp of when the instance was last used")
    updated_at: Optional[datetime] = Field(None, description="Timestamp of the last update")
    url: Optional[str] = Field(None, description="Endpoint URL for the instance")

    @classmethod
    def from_proto(cls, proto_instance: ProtoMcpInstance) -> "McpInstance":
        """Instantiate from the protobuf MCP instance."""

        last_used_at = proto_instance.last_used_at.ToDatetime() if proto_instance.last_used_at else None
        updated_at = proto_instance.updated_at.ToDatetime() if proto_instance.updated_at else None

        config = None
        if proto_instance.HasField("config"):
            config = McpConfig.from_proto(proto_instance.config)

        return cls(
            id=proto_instance.id or None,
            name=proto_instance.name or None,
            user_identifier=proto_instance.user_identifier or None,
            config=config,
            last_used_at=last_used_at,
            updated_at=updated_at,
            url=proto_instance.url or None,
        )

    def to_dict(self) -> dict:
        """Serialise the instance to a plain dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "user_identifier": self.user_identifier,
            "config": self.config.model_dump() if self.config else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "url": self.url,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        json_encoders = {
            datetime: lambda value: value.isoformat() if value else None,
        }


class McpInstanceConnectionAuthState(BaseModel):
    """Authentication status for a connection referenced by an MCP instance."""

    connection_id: Optional[str] = Field(None, description="Connection identifier")
    connection_name: Optional[str] = Field(None, description="Connection name")
    provider: Optional[str] = Field(None, description="Connection provider")
    connected_account_id: Optional[str] = Field(None, description="Connected account identifier")
    connected_account_status: Optional[str] = Field(None, description="Status of the connected account")
    authentication_link: Optional[str] = Field(None, description="Link to restore authentication if required")

    @classmethod
    def from_proto(cls, proto_state: ProtoConnectionAuthState) -> "McpInstanceConnectionAuthState":
        """Instantiate the auth state from protobuf data."""

        return cls(
            connection_id=proto_state.connection_id or None,
            connection_name=proto_state.connection_name or None,
            provider=proto_state.provider or None,
            connected_account_id=proto_state.connected_account_id or None,
            connected_account_status=proto_state.connected_account_status or None,
            authentication_link=proto_state.authentication_link or None,
        )

    def to_dict(self) -> dict:
        """Serialise the auth state to a dictionary."""

        return {
            "connection_id": self.connection_id,
            "connection_name": self.connection_name,
            "provider": self.provider,
            "connected_account_id": self.connected_account_id,
            "connected_account_status": self.connected_account_status,
            "authentication_link": self.authentication_link,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True

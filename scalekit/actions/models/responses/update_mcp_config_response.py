from typing import Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_config import McpConfig


class UpdateMcpConfigResponse(BaseModel):
    """Response wrapper for MCP config updates."""

    config: Optional[McpConfig] = Field(
        None,
        description="The updated MCP configuration",
    )

    @classmethod
    def from_proto(cls, proto_response) -> "UpdateMcpConfigResponse":
        """Convert protobuf UpdateMcpConfigResponse into the action model."""

        config = None
        if getattr(proto_response, "config", None):
            config = McpConfig.from_proto(proto_response.config)
        return cls(config=config)

    def to_dict(self) -> dict:
        """Serialise the response to a dictionary."""

        return {
            "config": self.config.model_dump() if self.config else None,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True

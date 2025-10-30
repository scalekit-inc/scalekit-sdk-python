from typing import Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_instance import McpInstance


class EnsureMcpInstanceResponse(BaseModel):
    """Response model for ensure/create MCP instance operations."""

    instance: Optional[McpInstance] = Field(
        None,
        description="The ensured MCP instance",
    )

    @classmethod
    def from_proto(cls, proto_response) -> "EnsureMcpInstanceResponse":
        instance = None
        if getattr(proto_response, "instance", None):
            instance = McpInstance.from_proto(proto_response.instance)
        return cls(instance=instance)

    def to_dict(self) -> dict:
        return {
            "instance": self.instance.model_dump() if self.instance else None,
        }

    class Config:
        validate_assignment = True

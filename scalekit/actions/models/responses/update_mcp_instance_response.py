from typing import Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_instance import McpInstance


class UpdateMcpInstanceResponse(BaseModel):
    """Response model for updating MCP instances."""

    instance: Optional[McpInstance] = Field(
        None,
        description="The updated MCP instance",
    )

    @classmethod
    def from_proto(cls, proto_response) -> "UpdateMcpInstanceResponse":
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

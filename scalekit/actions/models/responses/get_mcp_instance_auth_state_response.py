from typing import List

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_instance import McpInstanceConnectionAuthState


class GetMcpInstanceAuthStateResponse(BaseModel):
    """Authentication state details for connections within an MCP instance."""

    connections: List[McpInstanceConnectionAuthState] = Field(
        default_factory=list,
        description="Authentication state per connection",
    )

    @classmethod
    def from_proto(cls, proto_response) -> "GetMcpInstanceAuthStateResponse":
        connections = [
            McpInstanceConnectionAuthState.from_proto(proto_state)
            for proto_state in getattr(proto_response, "connections", [])
        ]
        return cls(connections=connections)

    def to_dict(self) -> dict:
        return {
            "connections": [connection.model_dump() for connection in self.connections],
        }

    class Config:
        validate_assignment = True

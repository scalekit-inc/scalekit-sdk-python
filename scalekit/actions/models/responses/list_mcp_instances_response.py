from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_instance import McpInstance


class ListMcpInstancesResponse(BaseModel):
    """Response model for listing MCP instances."""

    instances: List[McpInstance] = Field(
        default_factory=list,
        description="Collection of MCP instances",
    )
    total_count: Optional[int] = Field(
        None,
        description="Total number of instances",
        alias="total_size",
    )
    next_page_token: Optional[str] = Field(
        None,
        description="Token for fetching the next page",
    )
    previous_page_token: Optional[str] = Field(
        None,
        description="Token for fetching the previous page",
        alias="prev_page_token",
    )

    @classmethod
    def from_proto(cls, proto_response) -> "ListMcpInstancesResponse":
        instances = [
            McpInstance.from_proto(proto_instance)
            for proto_instance in getattr(proto_response, "instances", [])
        ]
        return cls(
            instances=instances,
            total_count=proto_response.total_size if getattr(proto_response, "total_size", 0) else None,
            next_page_token=proto_response.next_page_token or None,
            previous_page_token=proto_response.prev_page_token or None,
        )

    def to_dict(self) -> dict:
        return {
            "instances": [instance.model_dump() for instance in self.instances],
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token,
        }

    class Config:
        validate_assignment = True
        populate_by_name = True

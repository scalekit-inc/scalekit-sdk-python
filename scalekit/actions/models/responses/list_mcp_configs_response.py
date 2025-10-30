from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_config import McpConfig


class ListMcpConfigsResponse(BaseModel):
    """List MCP configs response with helpers for proto conversion."""

    configs: List[McpConfig] = Field(
        default_factory=list,
        description="Collection of MCP configurations",
    )
    total_count: Optional[int] = Field(
        None,
        description="Total number of configs available",
        alias="total_size",
    )
    next_page_token: Optional[str] = Field(
        None,
        description="Token for retrieving the next page",
    )
    previous_page_token: Optional[str] = Field(
        None,
        description="Token for retrieving the previous page",
        alias="prev_page_token",
    )

    @classmethod
    def from_proto(cls, proto_response) -> "ListMcpConfigsResponse":
        """Convert protobuf ListMcpConfigsResponse into the action model."""

        configs = [
            McpConfig.from_proto(proto_config)
            for proto_config in getattr(proto_response, "configs", [])
        ]
        return cls(
            configs=configs,
            total_count=proto_response.total_size if getattr(proto_response, "total_size", 0) else None,
            next_page_token=proto_response.next_page_token or None,
            previous_page_token=proto_response.prev_page_token or None,
        )

    def to_dict(self) -> dict:
        """Serialise the response to a dictionary."""

        return {
            "configs": [config.model_dump() for config in self.configs],
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True

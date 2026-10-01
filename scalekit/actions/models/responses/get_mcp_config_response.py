"""Response model for the ``get_config`` MCP methods."""

from typing import Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_config import McpConfig
from scalekit.v1.mcp.mcp_pb2 import GetMcpConfigResponse as GetMcpConfigResponseProto


class GetMcpConfigResponse(BaseModel):
    """A single MCP configuration, fetched by ID.

    Returned by ``client.actions.mcp.get_config`` and
    ``client.actions.get_config``. Carries the same ``McpConfig`` model as
    ``ListMcpConfigsResponse.configs``.

    Attributes:
        config: The configuration. ``None`` only when the server returned a
            response with no config set; a missing ID raises
            ``ScalekitNotFoundException`` instead.

    Example:
        result = client.actions.mcp.get_config("cfg_123")
        print(result.config.name, result.config.mcp_server_url)

    """

    config: Optional[McpConfig] = Field(
        None,
        description="The MCP configuration",
    )

    @classmethod
    def from_proto(cls, proto_response: GetMcpConfigResponseProto) -> "GetMcpConfigResponse":
        """Build the model from the ``GetMcpConfigResponse`` proto message.

        Args:
            proto_response: The proto message returned by
                ``McpClient.get_config``.

        Returns:
            The mapped response. Presence of ``config`` is read with ``HasField``
            rather than truthiness, because an unset singular message field still
            reads as a truthy default instance in protobuf for Python.

        Example:
            response, _ = client.mcp.get_config("cfg_123")
            result = GetMcpConfigResponse.from_proto(response)

        """
        config = (
            McpConfig.from_proto(proto_response.config)
            if proto_response.HasField("config")
            else None
        )
        return cls(config=config)

    def to_dict(self) -> dict:
        """Serialise the response to a dictionary.

        Returns:
            A dictionary with a single ``config`` key, converted by
            ``McpConfig.to_dict`` or left as ``None``.

        """
        return {
            "config": self.config.to_dict() if self.config else None,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True

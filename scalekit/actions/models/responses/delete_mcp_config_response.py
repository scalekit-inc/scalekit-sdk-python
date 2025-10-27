from pydantic import BaseModel


class DeleteMcpConfigResponse(BaseModel):
    """Response wrapper for MCP config deletion."""

    @classmethod
    def from_proto(cls, proto_response) -> "DeleteMcpConfigResponse":
        """Convert protobuf DeleteMcpConfigResponse into the action model."""

        # The proto response does not contain any fields.
        return cls()

    def to_dict(self) -> dict:
        """Serialise the response to a dictionary."""

        return {}

    class Config:
        """Pydantic configuration."""

        validate_assignment = True

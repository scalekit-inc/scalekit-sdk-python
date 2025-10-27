from pydantic import BaseModel


class DeleteMcpInstanceResponse(BaseModel):
    """Response model for deleting an MCP instance."""

    @classmethod
    def from_proto(cls, proto_response) -> "DeleteMcpInstanceResponse":
        return cls()

    def to_dict(self) -> dict:
        return {}

    class Config:
        validate_assignment = True

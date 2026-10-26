from pydantic import BaseModel, Field


class DeleteCustomProviderRequest(BaseModel):
    """Request model for deleting a custom provider.

    Deletion is permanent. The provider and all associated configuration are
    removed, including its discovered custom MCP tools. The server refuses to
    delete a provider that still has connections ("cannot delete custom provider
    with existing connections"): remove its connected accounts first, then all of
    its connections (a connection that still has connected accounts cannot be
    deleted either).
    """

    identifier: str = Field(
        ...,
        min_length=1,
        description=(
            "Required. Identifier of the custom provider to delete. Obtained from "
            "Provider.identifier in a create or list response."
        ),
    )

    class Config:
        validate_assignment = True

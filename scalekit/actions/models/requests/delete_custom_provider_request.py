from pydantic import BaseModel, Field


class DeleteCustomProviderRequest(BaseModel):
    """Request model for deleting a custom provider.

    Deletion is permanent. The provider and all associated configuration are
    removed. Existing connected accounts for this provider are not automatically
    deleted — handle those separately before deleting the provider if needed.
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

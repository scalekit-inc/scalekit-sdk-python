from pydantic import BaseModel, Field


class DeleteCustomProviderRequest(BaseModel):
    """Request model for deleting a custom provider.

    Deletion is permanent. The provider and all associated configuration are
    removed, including its discovered custom MCP tools. The server refuses to
    delete a provider that still has connections ("cannot delete custom provider
    with existing connections"): remove its connected accounts first, then all of
    its connections with ``scalekit_client.actions.delete_connection`` (a connection
    that still has connected accounts cannot be deleted either).
    """

    identifier: str = Field(
        ...,
        min_length=1,
        description=(
            "Required. Identifier of the connector to delete: the NAME:environment-id string, such as "
            "ACMEAPI:70219645518265104, from Provider.identifier in a create or list response. "
            "It is not Provider.id (prvd_...), which answers 404."
        ),
    )

    class Config:
        validate_assignment = True

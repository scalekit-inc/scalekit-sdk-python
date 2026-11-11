from pydantic import BaseModel, Field


class TriggerToolCollectionRequest(BaseModel):
    """Request model for queueing a new tool collection run on an OpenAPI-sourced connector."""

    provider_identifier: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description=(
            "Required. Identifier of the OpenAPI-sourced connector to regenerate tools for. "
            "Obtained from Provider.identifier in a create or list response."
        ),
    )

    class Config:
        validate_assignment = True

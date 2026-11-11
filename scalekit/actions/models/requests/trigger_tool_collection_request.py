from pydantic import BaseModel, Field, field_validator


class TriggerToolCollectionRequest(BaseModel):
    """Request model for queueing a new tool collection run on an OpenAPI-sourced connector."""

    provider_identifier: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description=(
            "Required. Identifier of the OpenAPI-sourced connector to regenerate tools for. "
            "Obtained from Provider.identifier in a create or list response. Surrounding "
            "whitespace is removed."
        ),
    )

    @field_validator("provider_identifier", mode="before")
    @classmethod
    def _strip_provider_identifier(cls, value):
        return value.strip() if isinstance(value, str) else value

    class Config:
        validate_assignment = True

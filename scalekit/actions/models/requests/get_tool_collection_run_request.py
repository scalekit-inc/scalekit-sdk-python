from pydantic import BaseModel, Field, field_validator


class GetToolCollectionRunRequest(BaseModel):
    """Request model for reading one tool collection run of an OpenAPI-sourced connector."""

    provider_identifier: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description=(
            "Required. Identifier of the connector the run belongs to: the NAME:environment-id string, such "
            "as ACMEAPI:70219645518265104, from Provider.identifier in a create or list response. "
            "It is not Provider.id (prvd_...), which answers 404. Surrounding whitespace is removed."
        ),
    )
    run_id: str = Field(
        "latest",
        max_length=255,
        description=(
            "The run to read: a ToolCollectionRun.run_id, or 'latest' (the default, also meant "
            "when this is empty or blank) for the connector's most recent run. Surrounding "
            "whitespace is removed."
        ),
    )

    @field_validator("provider_identifier", mode="before")
    @classmethod
    def _strip_provider_identifier(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("run_id", mode="before")
    @classmethod
    def _blank_run_id_means_latest(cls, value):
        return (value.strip() or "latest") if isinstance(value, str) else value

    class Config:
        validate_assignment = True

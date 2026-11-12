from pydantic import BaseModel, Field


class GetToolCollectionRunRequest(BaseModel):
    """Request model for reading one tool collection run of an OpenAPI-sourced connector."""

    provider_identifier: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description=(
            "Required. Identifier of the connector the run belongs to. Obtained from "
            "Provider.identifier in a create or list response."
        ),
    )
    run_id: str = Field(
        "latest",
        max_length=255,
        description=(
            "The run to read: a ToolCollectionRun.run_id, or 'latest' (the default, also sent "
            "when this is empty) for the connector's most recent run."
        ),
    )

    class Config:
        validate_assignment = True

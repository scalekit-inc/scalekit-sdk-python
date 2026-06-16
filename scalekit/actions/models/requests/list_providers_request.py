from typing import Optional

from pydantic import BaseModel, Field, validator


class ListProvidersRequest(BaseModel):
    """Request model for listing providers with optional filtering and pagination."""

    provider_type: Optional[int] = Field(
        None,
        description=(
            "Optional. Filter results by provider type. Pass a ProviderType enum "
            "value from scalekit.v1.providers.providers_pb2: "
            "ProviderType.CUSTOM (1) = custom providers only, "
            "ProviderType.DEFAULT (0) = built-in providers only, "
            "ProviderType.ALL (2) = all providers. "
            "Pass None (default) to return all providers."
        ),
    )
    page_size: Optional[int] = Field(
        None,
        description=(
            "Optional. Maximum number of providers to return in a single response. "
            "Pass None (default) to use the server's default page size."
        ),
    )
    page_token: Optional[str] = Field(
        None,
        description=(
            "Optional. Pagination cursor returned as next_page_token in a previous "
            "list response. Pass None (default) to fetch the first page."
        ),
    )
    identifier: Optional[str] = Field(
        None,
        min_length=1,
        description=(
            "Optional. Filter to a specific provider by its identifier. "
            "Pass None (default) to return all providers matching the other filters."
        ),
    )

    @validator("provider_type")
    def validate_provider_type(cls, v):
        if v is not None and v not in (0, 1, 2):
            raise ValueError("provider_type must be 0 (DEFAULT), 1 (CUSTOM), or 2 (ALL)")
        return v

    @validator("page_size")
    def validate_page_size(cls, v):
        if v is not None and v < 1:
            raise ValueError("page_size must be at least 1")
        return v

    class Config:
        validate_assignment = True

from typing import List, Optional

from pydantic import BaseModel, Field, validator

from scalekit.actions.models.custom_provider import AuthPattern


class UpdateCustomProviderRequest(BaseModel):
    """Request model for updating an existing custom provider.

    display_name and proxy_url are required by the server on every update.
    Optional fields left as None are ignored — the server keeps their existing values.
    """

    identifier: str = Field(
        ...,
        min_length=1,
        description=(
            "Required. Identifier of the provider to update. Obtained from "
            "Provider.identifier in a create or list response."
        ),
    )
    display_name: str = Field(
        ...,
        description=(
            "Required. Display name for the provider. Accepted characters: "
            "a-z, A-Z, 0-9, and spaces. Good practice: suffix with 'MCP' for MCP "
            "server providers."
        ),
    )
    description: Optional[str] = Field(
        None,
        description=(
            "Optional. New description for the provider. Pass None (default) to "
            "leave the existing value unchanged."
        ),
    )
    proxy_url: str = Field(
        ...,
        description=(
            "Required. Proxy URL for the provider. Must be a valid HTTPS URL "
            "starting with 'https://'."
        ),
    )
    auth_patterns: Optional[List[AuthPattern]] = Field(
        None,
        description=(
            "Optional. Replacement list of AuthPattern objects. When provided, "
            "this list fully replaces the existing auth_patterns on the server — "
            "it is not merged. Note: currently only a single AuthPattern is supported "
            "— pass a list with exactly one element. The list type is intentional for "
            "future multi-pattern support. Pass None (default) to leave auth_patterns unchanged."
        ),
    )

    @validator("proxy_url")
    def validate_proxy_url_https(cls, v):
        if not v.startswith("https://"):
            raise ValueError("proxy_url must be a valid HTTPS URL starting with 'https://'")
        return v

    @validator("auth_patterns")
    def validate_single_auth_pattern(cls, v):
        if v is not None and len(v) != 1:
            raise ValueError("auth_patterns must contain exactly one AuthPattern when provided")
        return v

    class Config:
        validate_assignment = True

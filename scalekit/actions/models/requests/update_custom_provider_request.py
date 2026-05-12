from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.custom_provider import AuthPattern


class UpdateCustomProviderRequest(BaseModel):
    """Request model for updating an existing custom provider.

    Only fields explicitly set to a non-None value are applied. Fields left as
    None are ignored — the server keeps their existing values. To clear a field,
    pass an empty string or empty list as appropriate.
    """

    identifier: str = Field(
        ...,
        description=(
            "Required. Identifier of the provider to update. Obtained from "
            "Provider.identifier in a create or list response."
        ),
    )
    display_name: Optional[str] = Field(
        None,
        description=(
            "Optional. New display name for the provider. Accepted characters: "
            "a-z, A-Z, 0-9, and spaces. Good practice: suffix with 'MCP' for MCP "
            "server providers. Pass None (default) to leave the existing value unchanged."
        ),
    )
    description: Optional[str] = Field(
        None,
        description=(
            "Optional. New description for the provider. Pass None (default) to "
            "leave the existing value unchanged."
        ),
    )
    proxy_url: Optional[str] = Field(
        None,
        description=(
            "Optional. New proxy URL. Must be a valid HTTPS URL if provided. "
            "Pass None (default) to leave the existing value unchanged."
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

    class Config:
        validate_assignment = True

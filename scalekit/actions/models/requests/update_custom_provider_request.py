from typing import Dict, List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, validator

from scalekit.actions.models.custom_provider import AuthPattern, check_request_is_mcp


class UpdateCustomProviderRequest(BaseModel):
    """Request model for updating an existing custom provider.

    The server applies this as a PUT (PUT /api/v1/custom-providers/{identifier}):
    it replaces the provider's settings and is not a partial update. Send
    display_name, proxy_url and auth_patterns every time. A field left as None does
    not always mean "unchanged"; see each field.
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
            "Required. Name shown in the UI. Letters, digits and spaces only (max 200 "
            "characters); symbols such as '_' or '-' are rejected. Changing the name "
            "does not change the identifier. Good practice: suffix with 'MCP' for MCP "
            "server providers."
        ),
    )
    description: Optional[str] = Field(
        None,
        description=(
            "Optional. New description for the provider. Pass None (default) to "
            "leave the existing value unchanged. An empty string does not clear it: "
            "the server ignores empty values."
        ),
    )
    proxy_url: str = Field(
        ...,
        description=(
            "Required. URL of the external service this provider connects to, and the "
            "address Scalekit sends proxied requests to. For an MCP connector this is "
            "the MCP server's URL; for an API connector it is the API's base URL. "
            "Must be a valid HTTPS URL starting with 'https://'. Send the current "
            "value to keep it unchanged."
        ),
    )
    auth_patterns: Optional[List[AuthPattern]] = Field(
        None,
        description=(
            "Marked required by the API on every update, although the SDK accepts "
            "None. Fully replaces the existing auth_patterns; it is not merged. "
            "Note: currently only a single AuthPattern is supported — pass a list "
            "with exactly one element. The list type is intentional for future "
            "multi-pattern support. The auth type and is_mcp cannot be changed, and "
            "an API_KEY provider cannot switch between single-key and "
            "multiple-headers mode. Editing the header fields of a multiple-headers "
            "provider requires its connected accounts to re-authorize."
        ),
    )
    is_mcp: Optional[bool] = Field(
        None,
        description=(
            "Optional. Must match the connector's existing kind: the server rejects "
            "changing a connector between MCP and API. Pass True when updating an MCP "
            "connector so the replacement pattern stays an MCP connector. Only valid "
            "together with auth_patterns. Use this instead of is_mcp on AuthPattern, "
            "which is deprecated. A value that conflicts with is_mcp on the pattern "
            "raises a validation error."
        ),
    )
    icon_src: Optional[str] = Field(
        None,
        description=(
            "Optional. New URL of the provider's icon image. Pass None (default) to "
            "leave the existing value unchanged. An empty string does not clear it."
        ),
    )
    metadata: Optional[Dict[str, str]] = Field(
        None,
        description=(
            "Optional. Replaces the provider's entire metadata map; it is not merged. "
            "Pass None (default) and the server clears all existing metadata. To keep "
            "the current metadata, read the provider first and pass its metadata here. "
            "Keys must be 3-25 characters, values 1-256 characters, with a maximum of "
            "20 pairs."
        ),
    )

    @validator("proxy_url")
    def validate_proxy_url_https(cls, v):
        parsed = urlparse(v)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("proxy_url must be a valid HTTPS URL (e.g. 'https://server.example.com/mcp')")
        return v

    @validator("auth_patterns")
    def validate_single_auth_pattern(cls, v):
        if v is not None and len(v) != 1:
            raise ValueError("auth_patterns must contain exactly one AuthPattern when provided")
        return v

    @validator("is_mcp")
    def validate_is_mcp_matches_patterns(cls, v, values):
        patterns = values.get("auth_patterns")
        if patterns is None:
            raise ValueError(
                "is_mcp can only be sent together with auth_patterns, because "
                "auth_patterns replace the existing ones. Pass both, or leave is_mcp "
                "unset to keep the current auth patterns."
            )
        check_request_is_mcp(v, patterns)
        return v

    class Config:
        validate_assignment = True

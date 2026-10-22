from typing import Dict, List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, validator

from scalekit.actions.models.custom_provider import AuthPattern, check_request_is_mcp


class CreateCustomProviderRequest(BaseModel):
    """Request model for creating a new custom provider.

    A custom provider represents an external service (e.g. an MCP server or a
    REST API) that end users can connect to. Exactly one AuthPattern is required:
    the server rejects a create with no auth pattern ("auth patterns cannot be
    empty"), so users know how to authenticate with the provider.
    """

    display_name: str = Field(
        ...,
        description=(
            "Required. Name shown in the UI. Letters, digits and spaces only (max 200 "
            "characters); symbols such as '_' or '-' are rejected. The provider "
            "identifier is derived from it ('Acme MCP' becomes 'ACMEMCP:<environment "
            "id>'). The names of the built-in login providers (Github, Google, Gitlab, "
            "Microsoft, LinkedIn, Salesforce, Facebook) are rejected; other built-in "
            "names such as Gmail are accepted. "
            "Good practice: suffix with 'MCP' for MCP server providers. "
            "Example: 'GitHub Copilot MCP', 'Apify MCP Server'."
        ),
    )
    proxy_url: str = Field(
        ...,
        description=(
            "Required. URL of the external service this provider connects to, and the "
            "address Scalekit sends proxied requests to. For an MCP connector this is "
            "the MCP server's URL (example: 'https://server.example.com/mcp'). For an "
            "API connector it is the API's base URL (example: "
            "'https://api.example.com'). Must be a valid HTTPS URL."
        ),
    )
    proxy_enabled: bool = Field(
        True,
        description=(
            "Optional. Whether to enable request proxying through Scalekit for this "
            "provider. True = proxy enabled (default); False = proxy disabled."
        ),
    )
    description: str = Field(
        "",
        description=(
            "Optional. Short description of the provider shown in dashboards and "
            "API responses. Defaults to empty string."
        ),
    )
    auth_patterns: List[AuthPattern] = Field(
        default_factory=list,
        description=(
            "Required in practice. List of AuthPattern objects defining how users can "
            "authenticate with this provider. Each pattern represents one authentication "
            "method (OAUTH, BEARER, API_KEY, or NO_AUTH). Leaving it out fails with a "
            "validation error on provider.auth_patterns, and an empty list fails with "
            "'auth patterns cannot be empty'. The SDK checks neither before sending, so "
            "the error comes back from the server. "
            "Note: currently only a single AuthPattern is supported — pass a list "
            "with exactly one element. The list type is intentional for future "
            "multi-pattern support. The field defaults to an empty list only for "
            "backward compatibility."
        ),
    )
    is_mcp: Optional[bool] = Field(
        None,
        description=(
            "Optional. True creates an MCP (Model Context Protocol) server connector. "
            "None or False creates an API connector. Use this instead of is_mcp on "
            "AuthPattern, which is deprecated. Setting it to a value that conflicts "
            "with is_mcp on the pattern raises a validation error."
        ),
    )
    icon_src: str = Field(
        "",
        description=(
            "Optional. URL of the provider's icon image shown in the UI. "
            "Defaults to empty string (no icon)."
        ),
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Optional. Arbitrary string key-value pairs attached to the provider. "
            "Keys must be 3-25 characters, values 1-256 characters, with a maximum "
            "of 20 pairs. Defaults to empty dict (no metadata)."
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
        if len(v) > 1:
            raise ValueError("auth_patterns must contain at most one AuthPattern")
        return v

    @validator("is_mcp")
    def validate_is_mcp_matches_patterns(cls, v, values):
        check_request_is_mcp(v, values.get("auth_patterns") or [])
        return v

    class Config:
        validate_assignment = True

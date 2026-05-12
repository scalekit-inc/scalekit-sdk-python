from typing import List
from urllib.parse import urlparse

from pydantic import BaseModel, Field, validator

from scalekit.actions.models.custom_provider import AuthPattern


class CreateCustomProviderRequest(BaseModel):
    """Request model for creating a new custom provider.

    A custom provider represents an external service (e.g. an MCP server or a
    REST API) that end users can connect to. At least one AuthPattern should be
    included so users know how to authenticate with the provider.
    """

    display_name: str = Field(
        ...,
        description=(
            "Required. Human-readable name for the provider shown in the UI and "
            "API responses. Accepted characters: a-z, A-Z, 0-9, and spaces. "
            "Good practice: suffix with 'MCP' for MCP server providers. "
            "Example: 'GitHub Copilot MCP', 'Apify MCP Server'."
        ),
    )
    proxy_url: str = Field(
        ...,
        description=(
            "Required. Base URL of the provider's server. All proxied requests are "
            "routed through this URL. Must be a valid HTTPS URL. "
            "Example: 'https://server.example.com/mcp'."
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
            "Optional. List of AuthPattern objects defining how users can authenticate "
            "with this provider. Each pattern represents one authentication method "
            "(OAUTH, BEARER, or API_KEY). At least one pattern is recommended. "
            "Note: currently only a single AuthPattern is supported — pass a list "
            "with exactly one element. The list type is intentional for future "
            "multi-pattern support. Defaults to empty list."
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

    class Config:
        validate_assignment = True

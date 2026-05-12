from typing import List

from pydantic import BaseModel, Field

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

    class Config:
        validate_assignment = True

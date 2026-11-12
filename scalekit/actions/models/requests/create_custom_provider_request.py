from typing import Dict, List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, model_validator, validator

from scalekit.actions.models.custom_provider import AuthPattern


class CreateCustomProviderRequest(BaseModel):
    """Request model for creating a new custom provider.

    A custom provider represents an external service (e.g. an MCP server or a
    REST API) that end users can connect to. Its tools come from an MCP server
    (set proxy_url) or from an OpenAPI spec (set openapi_spec_url): set exactly
    one of the two. The server requires at least one AuthPattern, so users know
    how to authenticate with the provider.
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
    proxy_url: Optional[str] = Field(
        None,
        description=(
            "The MCP server URL of an MCP-sourced connector, which proxied requests "
            "are routed through. Must be a valid HTTPS URL (at most 2048 characters). "
            "Required unless openapi_spec_url is set, and not accepted together with "
            "it: an OpenAPI-sourced connector's base URL is filled in from the spec "
            "itself once its tools are generated, and you can override it later with "
            "UpdateCustomProviderRequest.proxy_url. "
            "Example: 'https://server.example.com/mcp'."
        ),
    )
    openapi_spec_url: Optional[str] = Field(
        None,
        description=(
            "URL of an OpenAPI spec (JSON or YAML; a Swagger 2.0 document is "
            "converted) to source the connector's tools from. Must be a valid HTTPS "
            "URL (at most 2048 characters). Required unless proxy_url is set, and "
            "not accepted together with it. The server fetches and validates the spec "
            "before it stores anything (default limit 5 MB, 50 MB together with the "
            "files it references), then generates the tools in an asynchronous tool "
            "collection run that it queues for you: follow it with "
            "ActionProviders.get_tool_collection_run. Example: "
            "'https://api.example.com/openapi.json'."
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
            "List of AuthPattern objects defining how users can authenticate "
            "with this provider. Each pattern represents one authentication method "
            "(OAUTH, BEARER, API_KEY, BASIC, or NO_AUTH). The server requires at least "
            "one pattern and rejects a request without one. "
            "Note: currently only a single AuthPattern is supported — pass a list "
            "with exactly one element. The list type is intentional for future "
            "multi-pattern support. Defaults to empty list."
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
        if v is None:
            return v
        parsed = urlparse(v)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("proxy_url must be a valid HTTPS URL (e.g. 'https://server.example.com/mcp')")
        return v

    @validator("openapi_spec_url")
    def validate_openapi_spec_url_https(cls, v):
        if v is None:
            return v
        parsed = urlparse(v)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(
                "openapi_spec_url must be a valid HTTPS URL (e.g. 'https://api.example.com/openapi.json')"
            )
        return v

    @model_validator(mode="after")
    def validate_single_source(self):
        # The server enforces the same rule (400 INVALID_ARGUMENT); failing here saves the round trip.
        if self.proxy_url and self.openapi_spec_url:
            raise ValueError(
                "proxy_url cannot be set together with openapi_spec_url: an OpenAPI-sourced "
                "connector's base URL comes from the spec itself"
            )
        if not self.proxy_url and not self.openapi_spec_url:
            raise ValueError("either proxy_url or openapi_spec_url must be set")
        return self

    @validator("auth_patterns")
    def validate_single_auth_pattern(cls, v):
        if len(v) > 1:
            raise ValueError("auth_patterns must contain at most one AuthPattern")
        return v

    class Config:
        validate_assignment = True

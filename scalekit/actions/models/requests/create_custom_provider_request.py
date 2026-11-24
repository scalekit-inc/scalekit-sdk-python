from typing import Dict, List, Optional

from pydantic import BaseModel, Field, model_validator, validator

from scalekit.actions.models.custom_provider import AuthPattern
from scalekit.actions.models.requests._https_url import check_https_url


class CreateCustomProviderRequest(BaseModel):
    """Request model for creating a new custom provider.

    A custom provider represents an external service (e.g. an MCP server or a
    REST API) that end users can connect to. Its tools come from an MCP server
    (set proxy_url) or from an OpenAPI spec (set openapi_spec_url): set exactly
    one of the two. Exactly one AuthPattern is required: the server rejects a
    create without one (400 INVALID_ARGUMENT, a validation error on
    provider.auth_patterns), and this SDK accepts at most one, so users know how
    to authenticate with the provider.
    """

    display_name: str = Field(
        ...,
        description=(
            "Required. Name shown in the UI. ASCII letters (a-z, A-Z), digits and "
            "spaces only, 1-200 characters, with at least one letter or digit; "
            "anything else, such as accented letters or symbols like '_' or '-', is "
            "rejected. The provider "
            "identifier is derived from it ('Acme MCP' becomes 'ACMEMCP:<environment "
            "id>'). The names of the built-in login providers (Github, Google, Gitlab, "
            "Microsoft, LinkedIn, Salesforce, Facebook) are rejected; other built-in "
            "names such as Gmail are accepted. "
            "Good practice: suffix with 'MCP' for MCP server providers. "
            "Example: 'GitHub Copilot MCP', 'Apify MCP Server'."
        ),
    )
    proxy_url: Optional[str] = Field(
        None,
        description=(
            "URL of the external service this provider connects to, and the address "
            "Scalekit sends proxied requests to. For an MCP connector this is the MCP "
            "server's URL (example: 'https://server.example.com/mcp'); for an API "
            "connector it is the API's base URL (example: 'https://api.example.com'). "
            "Must be a valid HTTPS URL that starts with a lower-case 'https://' (at "
            "most 2048 characters). Required unless "
            "openapi_spec_url is set, and not accepted together with it: an "
            "OpenAPI-sourced connector's base URL is filled in from the spec's server "
            "URL by the first tool collection run, only when that URL starts with "
            "https://, and you can override it later with "
            "UpdateCustomProviderRequest.proxy_url."
        ),
    )
    openapi_spec_url: Optional[str] = Field(
        None,
        description=(
            "URL of an OpenAPI spec (JSON or YAML; a Swagger 2.0 document is "
            "converted) to source the connector's tools from. Must be a valid HTTPS "
            "URL that starts with a lower-case 'https://' (at most 2048 characters). "
            "Required unless proxy_url is set, and "
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
            "Ignored. A custom connector is always created with proxy_enabled=True, "
            "whatever is set here. The field is kept so that existing code that sets "
            "it keeps working."
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
            "method (OAUTH, BEARER, API_KEY, BASIC, or NO_AUTH). Leaving it out and "
            "passing an empty list fail the same way: 400 INVALID_ARGUMENT, a "
            "validation error on provider.auth_patterns (the SDK sends no "
            "auth_patterns for an empty list). The SDK checks neither before "
            "sending, so the error comes back from the server. "
            "Note: currently only a single AuthPattern is supported — pass a list "
            "with exactly one element. The list type is intentional for future "
            "multi-pattern support. The field defaults to an empty list only for "
            "backward compatibility."
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
        return check_https_url("proxy_url", v, "https://server.example.com/mcp")

    @validator("openapi_spec_url")
    def validate_openapi_spec_url_https(cls, v):
        if v is None:
            return v
        return check_https_url("openapi_spec_url", v, "https://api.example.com/openapi.json")

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

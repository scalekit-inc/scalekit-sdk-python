from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator

from scalekit.actions.models.custom_provider import AuthPattern
from scalekit.actions.models.requests._https_url import check_https_url


class UpdateCustomProviderRequest(BaseModel):
    """Request model for updating an existing custom provider.

    The server applies this as a PUT (PUT /api/v1/custom-providers/{identifier}): it
    replaces the provider's settings and is not a partial update. It requires
    display_name and auth_patterns on every update, and proxy_url as well for an
    MCP-sourced connector. Fields left as None are not sent: description and icon_src then keep their stored values, but metadata is
    cleared (see that field). The update always sends proxy_enabled=True, which
    create_custom_provider always sets, and has no field for it: a proxy_enabled passed
    to this model is ignored. The server applies the flag on every update, so an update
    switches proxying on for a connector that has it off, and refuses an OpenAPI-sourced
    connector in that state (see ProvidersClient.update_custom_provider).

    An OpenAPI-sourced connector (one created with openapi_spec_url) can only
    change display_name, description, icon_src, metadata and proxy_url, which is
    its base URL, and openapi_spec_url where the workspace has that capability
    enabled. Changing anything else is rejected with 400 INVALID_ARGUMENT. A
    field counts as changed only when its content differs from the stored value,
    so to update such a connector, read it with list_providers and send its
    auth_patterns back exactly as returned. A decoded AuthPattern
    you leave unchanged is sent exactly as the server returned it, so passing
    Provider.auth_patterns through as it is meets that.
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
            "Required. Name shown in the UI. ASCII letters (a-z, A-Z), digits and "
            "spaces only, 1-200 characters, with at least one letter or digit; "
            "anything else, such as accented letters or symbols like '_' or '-', is "
            "rejected. Changing the name does not change the identifier. Good "
            "practice: suffix with 'MCP' for MCP server providers."
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
    proxy_url: Optional[str] = Field(
        None,
        description=(
            "URL of the external service this provider connects to, and the address "
            "Scalekit sends proxied requests to. For an MCP-sourced connector, its MCP "
            "server URL (required: the server answers 400 'proxy_url is required for an "
            "MCP-sourced connector' without it). For an API connector, the API's base "
            "URL. For an OpenAPI-sourced connector, its base URL, which you may omit to "
            "keep the stored one. Changing it (ignoring a trailing slash) saves it and "
            "queues a tool collection run that regenerates every tool; if a run is "
            "already in progress the value is still saved but the call fails with 409 "
            "RESOURCE_ALREADY_EXISTS, so call trigger_tool_collection once that run "
            "completes. Must be a valid HTTPS URL starting with a lower-case "
            "'https://' (at most 2048 characters). An empty "
            "string is accepted and treated like None: it is what Provider.proxy_url "
            "holds for an OpenAPI-sourced connector until its first tool collection run "
            "fills in the base URL (or when the spec's server URL is not https), and the "
            "server keeps the stored base URL when it receives one. An MCP-sourced "
            "connector still needs a URL."
        ),
    )
    openapi_spec_url: Optional[str] = Field(
        None,
        description=(
            "URL of the OpenAPI spec of an OpenAPI-sourced connector. Leave it None "
            "unless you mean to change the spec source: the URL is fixed when the "
            "connector is created, and changing it to a different value fails with 400 "
            "FEATURE_NOT_ENABLED ('updating the OpenAPI spec URL of an existing "
            "connector is not enabled for this workspace') unless that capability is on "
            "for your workspace. Where it is on, the new URL is validated and every tool "
            "is regenerated. Sending the stored value again does nothing. A connector "
            "that was not created from a spec cannot gain one (400 INVALID_ARGUMENT). "
            "Must be a valid HTTPS URL starting with a lower-case 'https://' (at most "
            "2048 characters); an empty string is treated like None."
        ),
    )
    auth_patterns: Optional[List[AuthPattern]] = Field(
        None,
        description=(
            "The AuthPattern objects of the provider. The server requires them on "
            "every update: a request that leaves them out is rejected with 400 "
            "INVALID_ARGUMENT (a validation error on provider.auth_patterns). When "
            "they differ from the stored ones, they replace the existing list rather "
            "than merging. The server accepts an empty list and then keeps the stored "
            "patterns, but this model refuses one. To keep the current patterns, send "
            "the ones list_providers returned. Note: currently only a single "
            "AuthPattern is supported — pass a list with exactly one element. The "
            "list type is intentional for future multi-pattern support. The auth type "
            "and the connector kind (MCP or API) cannot be changed, and an API_KEY "
            "provider cannot switch between single-key and multiple-headers mode. "
            "Editing the header fields of a multiple-headers provider requires its "
            "connected accounts to re-authorize."
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
            "Optional. Replacement metadata key-value pairs. When provided, the server "
            "replaces the provider's entire metadata map with this value — it is not "
            "merged. Keys must be 3-25 characters, values 1-256 characters, with a "
            "maximum of 20 pairs. Leaving it None clears all existing metadata, so to "
            "keep it send the stored map (Provider.metadata)."
        ),
    )

    @validator("proxy_url")
    def validate_proxy_url_https(cls, v):
        # "" is what Provider.proxy_url holds for an OpenAPI-sourced connector whose first
        # run has not filled in a base URL yet; on the wire it is the same as not sending one.
        if v is None or v == "":
            return v
        return check_https_url("proxy_url", v, "https://server.example.com/mcp")

    @validator("openapi_spec_url")
    def validate_openapi_spec_url_https(cls, v):
        if v is None or v == "":  # same as None on the wire: the stored spec URL is kept
            return v
        return check_https_url("openapi_spec_url", v, "https://api.example.com/openapi.json")

    @validator("auth_patterns")
    def validate_single_auth_pattern(cls, v):
        if v is not None and len(v) != 1:
            raise ValueError("auth_patterns must contain exactly one AuthPattern when provided")
        return v

    class Config:
        validate_assignment = True

from typing import List, Optional

from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel, Field


class AuthField(BaseModel):
    """A single credential input field displayed to the user during connection setup.

    AuthField is only used with BEARER and API_KEY auth patterns — do not attach
    fields to OAUTH patterns (the OAuth flow collects credentials itself).

    Use one AuthField per credential the user must supply. For a BEARER connector, add one AuthField(field_name='token', ...). For an
    API_KEY connector, add one AuthField(field_name='api_key',
    ...). Always set input_type='password' for tokens and keys so the UI masks the
    value.
    """

    field_name: str = Field(
        ...,
        description=(
            "Required. Machine-readable identifier for this field. Used as the key "
            "when the credential value is stored and retrieved. "
            "For BEARER patterns use 'token' or 'bearer_token'. "
            "For API_KEY patterns use 'api_key'."
        ),
    )
    label: str = Field(
        "",
        description=(
            "Optional. Human-readable label displayed above the input in the UI. "
            "Example: 'API Key', 'Bearer Token'. Defaults to empty string."
        ),
    )
    input_type: str = Field(
        "text",
        description=(
            "Optional. Controls how the input is rendered in the UI. "
            "Accepted values: 'text' (visible input, default) or "
            "'password' (masked input — use for secrets, tokens, and keys)."
        ),
    )
    hint: str = Field(
        "",
        description=(
            "Optional. Placeholder or helper text shown below the input field. "
            "Example: 'Find your token at Settings → API'. Defaults to empty string."
        ),
    )
    required: bool = Field(
        False,
        description=(
            "Optional. Whether the user must fill this field before the connection "
            "can be saved. True = field is mandatory; False = field is optional. "
            "Defaults to False."
        ),
    )

    def to_dict(self) -> dict:
        """Serialize this field to a wire-format dict for inclusion in auth_patterns.

        :returns: Dict representation of the field. 'hint' and 'required' are omitted
                  when they hold their default values to keep the wire payload minimal.
        :rtype: dict
        """
        d: dict = {
            "field_name": self.field_name,
            "label": self.label,
            "input_type": self.input_type,
        }
        if self.hint:
            d["hint"] = self.hint
        if self.required:
            d["required"] = True
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AuthField":
        """Deserialize an AuthField from a response dict.

        :param d: Dict containing field data as returned by the server.
        :type d: dict
        :returns: AuthField instance populated from the dict values.
        :rtype: AuthField
        """
        return cls(
            field_name=d.get("field_name", ""),
            label=d.get("label", ""),
            input_type=d.get("input_type", "text"),
            hint=d.get("hint", ""),
            required=d.get("required", False),
        )


class OAuthConfig(BaseModel):
    """OAuth configuration attached to an OAUTH auth pattern.

    Pass OAuthConfig() (all defaults) for MCP connectors that use Dynamic Client
    Registration — the MCP server manages the OAuth flow itself and no static
    endpoints are needed. Set pkce_enabled=False only if your OAuth server does
    not support PKCE.

    This class is only used with AuthPattern(type="OAUTH"). Do not attach it to
    BEARER or API_KEY patterns.
    """

    pkce_enabled: bool = Field(
        True,
        description=(
            "Optional. Whether to enable PKCE (Proof Key for Code Exchange, RFC 7636) "
            "for the OAuth authorization flow. True = PKCE on (default, recommended); "
            "False = PKCE disabled. Only set to False if the OAuth server does not "
            "support PKCE."
        ),
    )

    def to_dict(self) -> dict:
        """Serialize to a wire-format dict.

        :returns: Dict with a single key 'pkce_enabled'. Always emitted explicitly
                  so the server receives an unambiguous value.
        :rtype: dict
        """
        return {"pkce_enabled": self.pkce_enabled}

    @classmethod
    def from_dict(cls, d: dict) -> "OAuthConfig":
        """Deserialize an OAuthConfig from a response dict.

        :param d: Dict containing oauth_config data as returned by the server.
        :type d: dict
        :returns: OAuthConfig instance. pkce_enabled defaults to True if the key
                  is absent from the dict.
        :rtype: OAuthConfig
        """
        return cls(pkce_enabled=d.get("pkce_enabled", True))


class AuthPattern(BaseModel):
    """One authentication option available on a custom connector.

    A custom provider can have multiple auth patterns (e.g. both OAUTH and API_KEY),
    giving users a choice of how to authenticate. For MCP connectors set is_mcp=True
    on every pattern.

    Type guide:
      - "OAUTH"   — Browser-based OAuth 2.0 / 2.1 flow. Attach an OAuthConfig.
      - "BEARER"  — Static bearer token supplied by the user. Add AuthFields for
                    the token input.
      - "API_KEY" — Static API key supplied by the user. Add AuthFields for the
                    key input.
    """

    type: str = Field(
        ...,
        description=(
            "Required. Authentication mechanism for this pattern. "
            "Accepted values: 'OAUTH' (browser OAuth flow), "
            "'BEARER' (static bearer token), 'API_KEY' (static API key)."
        ),
    )
    display_name: str = Field(
        ...,
        description=(
            "Required. Human-readable label for this auth option shown in the UI. "
            "Accepted characters: a-z, A-Z, 0-9, and spaces. "
            "Example: 'GitHub OAuth', 'API Token', 'Service Account Key'."
        ),
    )
    description: str = Field(
        "",
        description=(
            "Optional. Short explanation of this auth method shown to the user. "
            "Example: 'Authenticate with your GitHub account using OAuth 2.1'. "
            "Defaults to empty string."
        ),
    )
    fields: List[AuthField] = Field(
        default_factory=list,
        description=(
            "Optional. List of AuthField objects defining the credential inputs "
            "the user must supply. Only applicable to BEARER and API_KEY types — "
            "must be empty (or omitted) for OAUTH, which collects credentials "
            "through the browser OAuth flow and does not use static input fields. "
            "Defaults to empty list."
        ),
    )
    is_mcp: bool = Field(
        False,
        description=(
            "Optional. Set to True for MCP (Model Context Protocol) server connectors. "
            "When True the server sets is_custom_mcp=True on the provider. "
            "Defaults to False."
        ),
    )
    oauth_config: Optional["OAuthConfig"] = Field(
        None,
        description=(
            "Optional. OAuth configuration. Required when type='OAUTH'; omit for "
            "'BEARER' and 'API_KEY' (must be None). "
            "Pass OAuthConfig() for MCP connectors using Dynamic Client Registration. "
            "Pass OAuthConfig(pkce_enabled=False) to disable PKCE. "
            "Defaults to None."
        ),
    )

    def to_dict(self) -> dict:
        """Serialize to a wire-format dict for inclusion in the auth_patterns ListValue.

        :returns: Dict representation of this auth pattern. 'description' is omitted
                  when empty, 'is_mcp' when False, and 'oauth_config' when None, to
                  keep the wire payload minimal.
        :rtype: dict
        """
        d: dict = {
            "type": self.type,
            "display_name": self.display_name,
            "fields": [f.to_dict() for f in self.fields],
        }
        if self.description:
            d["description"] = self.description
        if self.is_mcp:
            d["is_mcp"] = True
        if self.oauth_config is not None:
            d["oauth_config"] = self.oauth_config.to_dict()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AuthPattern":
        """Deserialize an AuthPattern from a response dict.

        :param d: Dict containing auth pattern data as returned by the server.
                  The 'oauth_config' key must be present for OAuth patterns;
                  its absence is interpreted as oauth_config=None (non-OAuth).
        :type d: dict
        :returns: AuthPattern instance populated from the dict values.
        :rtype: AuthPattern
        """
        oauth_cfg: Optional[OAuthConfig] = None
        if "oauth_config" in d:
            oauth_cfg = OAuthConfig.from_dict(d["oauth_config"])
        return cls(
            type=d.get("type", ""),
            display_name=d.get("display_name", ""),
            description=d.get("description", ""),
            fields=[AuthField.from_dict(f) for f in d.get("fields", [])],
            is_mcp=d.get("is_mcp", False),
            oauth_config=oauth_cfg,
        )

    class Config:
        validate_assignment = True


class Provider(BaseModel):
    """A custom provider as returned by the Scalekit API.

    Produced exclusively by ProvidersClient response decoding via from_proto().
    All fields are populated from the server response — do not construct this
    directly. The auth_patterns list is fully decoded so callers never need to
    handle protobuf types.
    """

    identifier: str = Field(
        "",
        description="Unique identifier assigned by the server. Read-only.",
    )
    display_name: str = Field(
        "",
        description=(
            "Human-readable name of the provider. "
            "Accepted characters: a-z, A-Z, 0-9, and spaces."
        ),
    )
    description: str = Field(
        "",
        description="Short description of the provider.",
    )
    proxy_url: str = Field(
        "",
        description="The proxy URL through which requests to this provider are routed.",
    )
    proxy_enabled: bool = Field(
        False,
        description="Whether request proxying is enabled for this provider.",
    )
    is_custom: bool = Field(
        False,
        description="True for all providers created via create_custom_provider.",
    )
    is_custom_mcp: bool = Field(
        False,
        description=(
            "True when at least one auth_pattern was created with is_mcp=True. "
            "Set by the server — not a field you write."
        ),
    )
    auth_patterns: List[AuthPattern] = Field(
        default_factory=list,
        description=(
            "Decoded list of authentication options for this provider. "
            "Currently contains at most one element — only a single auth pattern "
            "is supported today. The list type is intentional for future multi-pattern support."
        ),
    )

    @classmethod
    def from_proto(cls, proto) -> "Provider":
        """Decode a proto Provider message into a typed Provider.

        Calls MessageToDict on the auth_patterns ListValue field to produce a
        plain Python list, then deserializes each element into an AuthPattern.

        :param proto: A proto Provider message instance from providers_pb2.
        :returns: Provider instance with all fields populated and auth_patterns decoded.
        :rtype: Provider
        """
        auth_patterns_raw = MessageToDict(proto.auth_patterns)
        return cls(
            identifier=proto.identifier,
            display_name=proto.display_name,
            description=proto.description,
            proxy_url=proto.proxy_url,
            proxy_enabled=proto.proxy_enabled,
            is_custom=proto.is_custom,
            is_custom_mcp=proto.is_custom_mcp,
            auth_patterns=[AuthPattern.from_dict(p) for p in auth_patterns_raw],
        )

    class Config:
        validate_assignment = True

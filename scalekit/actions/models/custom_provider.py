import copy
import json
from typing import Any, Callable, ClassVar, Dict, List, Optional

from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, ValidationInfo, model_validator


class _ServedForm(BaseModel):
    """Base for the auth-pattern models: remembers the dict an instance was decoded from.

    The server compares the auth_patterns of an OpenAPI-sourced connector with the stored
    ones by content after parsing both into its own Go structs, where a JSON ``null``, an
    absent key, ``""`` and ``[]`` are not all the same value (``"hint": ""`` is not
    ``"hint": null``, ``"fields": []`` is not ``"fields": null``). The typed fields here
    normalise those, so encoding them from the fields alone would turn an unchanged
    pattern into a changed one. from_dict therefore keeps the decoded dict, and the SDK
    sends that dict, as it was received, while no field of the instance (nested ones
    included) has changed since decoding. Once one has, the instance is built from its
    fields as for one you construct yourself, and each nested model that is still
    unchanged is sent as it was decoded.

    That is the wire form, ``_to_wire_dict``, and only the SDK's own requests use it.
    The public ``to_dict`` does not: it always returns the normalised view built from the
    fields, whether the instance was decoded, constructed or edited.

    The remembered dict is not part of equality: two instances with the same field values
    compare equal even if they were decoded from differently shaped dicts.

    A change is recognised by value and by type (``1``, ``1.0`` and ``True`` differ). Assigning
    the value the SDK already decoded (``hint = ""`` where the server sent ``null``, say) is not
    a change, so the value the server sent is the one that goes back.
    """

    _served: Optional[dict] = PrivateAttr(default=None)
    _served_fingerprint: Optional[str] = PrivateAttr(default=None)

    def _fingerprint(self) -> str:
        """The instance's values, nested models included, as text.

        Text rather than the dumped dict, because Python compares 1, 1.0 and True as equal
        and an edit from one of them to another is still an edit: in a free-form key the
        server tells a JSON number from a JSON boolean. Key order is not part of it.
        """
        values = self.model_dump(warnings=False)
        try:
            return json.dumps(values, sort_keys=True, default=repr)
        except (TypeError, ValueError):  # keys that cannot be ordered, a cycle
            return repr(values)

    def _remember_served(self, d: dict) -> None:
        self._served = copy.deepcopy(d)
        self._served_fingerprint = self._fingerprint()

    def _served_if_unchanged(self) -> Optional[dict]:
        """The decoded dict (a copy), or None if there is none or a field changed since."""
        if self._served is None or self._fingerprint() != self._served_fingerprint:
            return None
        return copy.deepcopy(self._served)

    def _build_dict(self, encode: Callable[["_ServedForm"], dict]) -> dict:
        """The normalised dict, built from the fields, with ``encode`` applied to each nested model."""
        raise NotImplementedError

    def _to_wire_dict(self) -> dict:
        """The dict the SDK sends to the server for this instance.

        The decoded dict as received while nothing has changed since from_dict. Otherwise
        the normalised dict, in which each nested model is again sent as decoded while it
        is unchanged.
        """
        served = self._served_if_unchanged()
        if served is not None:
            return served
        return self._build_dict(lambda child: child._to_wire_dict())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseModel):
            return NotImplemented
        return (
            type(self) is type(other)
            and self.__dict__ == other.__dict__
            and self.__pydantic_extra__ == other.__pydantic_extra__
        )

    __hash__ = None  # type: ignore[assignment]  # mutable, like every non-frozen model


class AuthFieldOption(_ServedForm):
    """One selectable choice on an AuthField whose input_type is 'select'.

    Served alongside every select field. Without these the caller has a
    dropdown with no values to render.
    """

    value: str = Field(
        "",
        description=(
            "The value submitted when this choice is selected. This is what gets "
            "stored as the field's credential value. Example: 'offline'."
        ),
    )
    display_name: str = Field(
        "",
        description=(
            "Human-readable label for this choice as shown in the dropdown. "
            "Example: 'Offline'."
        ),
    )
    description: str = Field(
        "",
        description=(
            "Optional. Longer explanation of what this choice means, shown as "
            "helper text. Example: 'Offline with refresh token support'."
        ),
    )
    default: bool = Field(
        False,
        description=(
            "Whether this choice is pre-selected when the field is first "
            "rendered. At most one option in a field is the default."
        ),
    )

    def to_dict(self) -> dict:
        """Serialize this option to a wire-format dict.

        :returns: Dict with 'value', 'display_name', 'description', and 'default'.
                  Keys the SDK does not declare are re-emitted unchanged.
        :rtype: dict
        """
        return self._build_dict(lambda child: child.to_dict())

    def _build_dict(self, encode: Callable[[_ServedForm], dict]) -> dict:
        d: dict = {
            "value": self.value,
            "display_name": self.display_name,
            "description": self.description,
            "default": self.default,
        }
        d.update(self.model_extra or {})
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AuthFieldOption":
        """Deserialize an AuthFieldOption from a response dict.

        Keys this SDK does not declare are kept on the instance rather than
        dropped, so they survive a decode/encode round-trip.

        :param d: Dict containing option data as returned by the server.
        :type d: dict
        :returns: AuthFieldOption instance populated from the dict values.
        :rtype: AuthFieldOption
        """
        known = {
            "value": d.get("value") or "",
            "display_name": d.get("display_name") or "",
            "description": d.get("description") or "",
            "default": d.get("default") or False,
        }
        extras = {k: v for k, v in d.items() if k not in known}
        option = cls(**known, **extras)
        option._remember_served(d)
        return option

    class Config:
        extra = "allow"


class CredentialPlacement(_ServedForm):
    """Where a static credential is sent when it does not go in an HTTP header.

    Set it on the ``placement`` of an AuthField. Without a placement a credential is
    sent in a header, as before.

    * ``"query"``: the value is set as the query parameter ``name`` of every request,
      replacing a value the caller sent for it.
    * ``"body"``: the value is set as the top-level JSON body field ``name``. A request
      that has no body gets ``{name: value}``. A tool that sends a form-encoded body
      cannot use it.
    * ``"path"``: the value fills the ``{{name}}`` placeholder in the path of the
      connector's ``proxy_url``, path-escaped, for example
      ``https://api.telegram.org/bot{{bot_token}}``. The placeholder must sit in the
      path, not in the host or the query string.

    A placed credential is never also sent in a header, and the server does not follow
    redirects on a request that carries one. It applies to the ``api_key`` field of an
    API_KEY pattern, the ``token`` field of a BEARER pattern, and the ``username`` and
    ``password`` fields of a BASIC pattern (a BASIC pattern places both or neither). The
    field must have ``input_type="password"`` (a BASIC ``username`` may be ``"text"``). It
    cannot be combined with ``header_name``, ``is_path_param`` or
    ``auth_field_mutations``, and is not supported on ``account_fields``, OAUTH or
    NO_AUTH patterns, or on MCP connectors. The server checks all of this when it
    creates or updates a connector and rejects a violation with 400 INVALID_ARGUMENT
    ('invalid credential placement: ...'). An update that removes the placeholder
    from ``proxy_url`` is rejected too.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    PATH: ClassVar[str] = "path"
    QUERY: ClassVar[str] = "query"
    BODY: ClassVar[str] = "body"

    in_: str = Field(
        ...,
        alias="in",
        description=(
            "Where the value is sent: 'path', 'query' or 'body' (the constants "
            "CredentialPlacement.PATH, QUERY and BODY). The server ignores case and "
            "surrounding spaces, and rejects any other value. Sent on the wire as 'in'."
        ),
    )
    name: str = Field(
        ...,
        description=(
            "The query parameter or JSON body field that carries the value, or the name of "
            "the {{name}} placeholder for 'path'. Required, at most 64 characters. For "
            "'query' and 'body' it may contain only letters, digits, '_', '.' and '-'. For "
            "'path' it may contain only letters, digits and '_', and it cannot be 'domain', "
            "'version' or the name of one of the pattern's is_path_param fields. Two fields "
            "cannot place into the same location under the same name."
        ),
    )

    def to_dict(self) -> dict:
        """Serialize to a wire-format dict.

        :returns: Dict with 'in' and 'name', plus any other keys the placement was
                  decoded with, re-emitted unchanged.
        :rtype: dict
        """
        return self._build_dict(lambda child: child.to_dict())

    def _build_dict(self, encode: Callable[[_ServedForm], dict]) -> dict:
        d: dict = {"in": self.in_, "name": self.name}
        d.update(self.model_extra or {})
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "CredentialPlacement":
        """Deserialize a placement from a response dict. Keys this SDK does not declare are kept."""
        extras = {k: v for k, v in d.items() if k not in ("in", "name")}
        placement = cls(in_=d.get("in") or "", name=d.get("name") or "", **extras)
        placement._remember_served(d)
        return placement


class AuthField(_ServedForm):
    """A single input field displayed to the user during connection setup.

    Use one AuthField per value the user must supply. For a BEARER connector, add
    one AuthField(field_name='token', ...). For an API_KEY connector, add one
    AuthField(field_name='api_key', ...). For a BASIC connector, add
    AuthField(field_name='username', ...) and AuthField(field_name='password', ...).
    Always set input_type='password' for tokens, keys and passwords so the UI masks
    the value.

    Fields are not limited to BEARER and API_KEY patterns. OAUTH patterns carry
    them too, for options collected before the browser flow starts rather than
    credentials — a select field choosing how the flow behaves, for example.

    The server models this as a free-form JSON object, so it may carry keys this
    SDK does not declare. Those are preserved on the instance and re-emitted by
    to_dict() rather than dropped. A field decoded from a response is sent back to
    the server exactly as it was received while you leave it unchanged (to_dict()
    itself always returns the normalised view).
    """

    field_name: str = Field(
        ...,
        description=(
            "Required. Machine-readable identifier for this field. Used as the key "
            "when the credential value is stored and retrieved. "
            "For BEARER patterns use 'token' or 'bearer_token'. "
            "For API_KEY patterns use 'api_key'. "
            "For BASIC patterns use 'username' and 'password'."
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
            "Known values: 'text' (visible input, default), 'password' (masked "
            "input — use for secrets, tokens, and keys), 'select' (dropdown), and "
            "'textarea' (multi-line input). Not restricted to a fixed set: the "
            "value vocabulary is owned by the Scalekit provider catalogue and may "
            "grow, so the SDK accepts any string and passes an unknown type through "
            "unchanged rather than failing to parse the response."
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
    options: List["AuthFieldOption"] = Field(
        default_factory=list,
        description=(
            "Optional. The selectable choices for this field, populated when "
            "input_type='select'. Empty for every other input type. A select "
            "field without options cannot be rendered, so the catalogue always "
            "ships them together."
        ),
    )
    is_path_param: bool = Field(
        False,
        description=(
            "Optional. True when the collected value is substituted into the "
            "provider's request path rather than sent as a credential — used by "
            "connectors whose base URL embeds a tenant or region. Defaults to False."
        ),
    )
    header_name: str = Field(
        "",
        description=(
            "Optional. On an API_KEY pattern, marks this field's value for "
            "injection as this exact HTTP header (case preserved). Setting it on "
            "any field puts the pattern in multiple-headers mode. Empty means "
            "single-key mode, which uses the pattern's auth_header_key_override. "
            "In multiple-headers mode every field that is not an is_path_param field "
            "needs a header_name, a pattern has at most 10 headers, and a header name "
            "may contain only letters, '.', '-' and '_' (no digits or spaces), must be "
            "unique ignoring case, and cannot be connection, keep-alive, "
            "proxy-authenticate, proxy-authorization, te, trailer, transfer-encoding, "
            "upgrade, host or content-length. The server replaces each field_name with "
            "a slug of its header name (lowercased, with runs of '-', '.' and spaces "
            "turned into '_', so 'X-Api-Key' becomes 'x_api_key'). A violation is "
            "rejected with 400 and error_code INVALID_HEADER_CONFIG, and so is switching "
            "a connector between single-key and multiple-headers mode after it is "
            "created. Where multiple-headers connectors are not enabled for the "
            "environment, create and update fail with 400 FEATURE_NOT_ENABLED. "
            "Renaming or removing a header later breaks the connected accounts created "
            "before the change until they authorize again. Cannot be combined with "
            "placement. Defaults to empty string."
        ),
    )
    placement: Optional[CredentialPlacement] = Field(
        None,
        description=(
            "Optional. Sends this field's value in the URL path, the query string or the "
            "JSON body of the request instead of an HTTP header. See CredentialPlacement "
            "for the rules. Defaults to None, which keeps sending it in a header."
        ),
    )

    def to_dict(self) -> dict:
        """Serialize this field to a wire-format dict for inclusion in auth_patterns.

        :returns: Dict representation of the field. 'hint', 'required', 'options',
                  'is_path_param', 'header_name' and 'placement' are omitted when they
                  hold their default values to keep the wire payload minimal. Keys the
                  SDK does not declare are re-emitted unchanged.
        :rtype: dict
        """
        return self._build_dict(lambda child: child.to_dict())

    def _build_dict(self, encode: Callable[[_ServedForm], dict]) -> dict:
        d: dict = {
            "field_name": self.field_name,
            "label": self.label,
            "input_type": self.input_type,
        }
        if self.hint:
            d["hint"] = self.hint
        if self.required:
            d["required"] = True
        if self.options:
            d["options"] = [encode(o) for o in self.options]
        if self.is_path_param:
            d["is_path_param"] = True
        if self.header_name:
            d["header_name"] = self.header_name
        if self.placement is not None:
            d["placement"] = encode(self.placement)
        d.update(self.model_extra or {})
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AuthField":
        """Deserialize an AuthField from a response dict.

        Keys this SDK does not declare are kept on the instance rather than
        dropped, so a field the catalogue grows later survives a decode/encode
        round-trip.

        :param d: Dict containing field data as returned by the server.
        :type d: dict
        :returns: AuthField instance populated from the dict values.
        :rtype: AuthField
        """
        known = {
            "field_name": d.get("field_name") or "",
            "label": d.get("label") or "",
            "input_type": d.get("input_type") or "text",
            "hint": d.get("hint") or "",
            "required": d.get("required") or False,
            "options": [AuthFieldOption.from_dict(o) for o in d.get("options") or []],
            "is_path_param": d.get("is_path_param") or False,
            "header_name": d.get("header_name") or "",
            "placement": (
                CredentialPlacement.from_dict(d["placement"])
                if isinstance(d.get("placement"), dict)
                else None
            ),
        }
        extras = {k: v for k, v in d.items() if k not in known}
        field = cls(**known, **extras)
        field._remember_served(d)
        return field

    class Config:
        extra = "allow"


class OAuthConfig(_ServedForm):
    """OAuth configuration attached to an OAUTH auth pattern.

    Pass OAuthConfig() (all defaults) for MCP connectors that use Dynamic Client
    Registration — the MCP server manages the OAuth flow itself and no static
    endpoints are needed. Set pkce_enabled=False only if your OAuth server does
    not support PKCE.

    Attach it to AuthPattern(type="OAUTH"). The managed catalogue also attaches
    one to its other OAuth-family types ('OAUTH_M2M', 'GOOGLE_DWD',
    'TRELLO_OAUTH1'). Do not attach it to BEARER or API_KEY patterns.

    pkce_enabled is the only key you set when authoring a connector, but a
    catalogue provider's oauth_config carries much more — 'authorize_uri',
    'token_uri', 'user_info_uri', 'available_scopes',
    'allow_use_scalekit_credentials' and others. Those are preserved on the
    instance (readable as ordinary attributes) and re-emitted by to_dict()
    rather than dropped, so reading a provider and writing it back does not
    erase its OAuth endpoints and scopes.
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

        :returns: Dict with 'pkce_enabled', always emitted explicitly so the
                  server receives an unambiguous value, plus any other keys the
                  config was decoded with, re-emitted unchanged.
        :rtype: dict
        """
        return self._build_dict(lambda child: child.to_dict())

    def _build_dict(self, encode: Callable[[_ServedForm], dict]) -> dict:
        d: dict = {"pkce_enabled": self.pkce_enabled}
        d.update(self.model_extra or {})
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "OAuthConfig":
        """Deserialize an OAuthConfig from a response dict.

        Keys this SDK does not declare are kept on the instance rather than
        dropped, so a catalogue provider's endpoints and scopes survive a
        decode/encode round-trip.

        :param d: Dict containing oauth_config data as returned by the server.
        :type d: dict
        :returns: OAuthConfig instance. pkce_enabled is False if the key is absent
                  from the dict, because the server leaves it out when it is false.
        :rtype: OAuthConfig
        """
        extras = {k: v for k, v in d.items() if k != "pkce_enabled"}
        config = cls(pkce_enabled=d.get("pkce_enabled", False), **extras)
        config._remember_served(d)
        return config

    class Config:
        extra = "allow"


class AuthPattern(_ServedForm):
    """One authentication option available on a custom connector.

    A custom provider can have multiple auth patterns (e.g. both OAUTH and API_KEY),
    giving users a choice of how to authenticate. For MCP connectors set is_mcp=True
    on every pattern.

    Type guide for the types you create custom connectors with:
      - "OAUTH"   — Browser-based OAuth 2.0 / 2.1 flow. Attach an OAuthConfig.
      - "BEARER"  — Static bearer token supplied by the user. Add AuthFields for
                    the token input.
      - "API_KEY" — Static API key supplied by the user. Add AuthFields for the
                    key input. Give several fields a header_name to send them as
                    several headers.
      - "BASIC"   — Username and password supplied by the user. Add AuthFields
                    named 'username' and 'password'. The server accepts it on every
                    custom connector.
      - "NO_AUTH" — Connector requires no credentials (e.g. public docs MCP
                    servers). Attach no fields and no OAuthConfig.

    A static credential (BEARER, API_KEY, BASIC) is sent in an HTTP header unless its
    AuthField sets a placement, which sends it in the URL path, the query string or
    the JSON body instead.

    Reading providers back can surface further types the managed catalogue uses
    (e.g. 'OAUTH_M2M', 'GOOGLE_DWD', 'TRELLO_OAUTH1', 'TRUSTED_IDP'), so type is not
    restricted to the ones above — see the field description.

    The server models this as a free-form JSON object, so it may carry keys this
    SDK does not declare. Those are preserved on the instance and re-emitted by
    to_dict() rather than dropped.

    A pattern decoded from a response (Provider.auth_patterns) is sent to the server
    exactly as the server returned it while you leave it and its fields unchanged, so
    it can be sent back to update_custom_provider as returned. That matters for an
    OpenAPI-sourced connector, whose patterns the server compares with the stored ones
    by content and must not change. to_dict() is not that: it always returns the
    normalised view built from the values. The form the server returned survives copy,
    deepcopy and pickle, but not model_dump() or JSON, nor to_dict() followed by
    from_dict() or a constructor, which rebuild the pattern in the normalised form, so
    for an OpenAPI-sourced connector always pass the patterns that list_providers (or the
    create and update responses) returned through untouched.
    """

    type: str = Field(
        ...,
        description=(
            "Required. Authentication mechanism for this pattern. "
            "Use one of 'OAUTH' (browser OAuth flow), 'BEARER' (static bearer "
            "token), 'API_KEY' (static API key), 'BASIC' (username and password) "
            "or 'NO_AUTH' (connector requires no credentials) when creating a "
            "custom connector. Not restricted to those five: the managed catalogue "
            "also serves 'OAUTH_M2M', 'GOOGLE_DWD', 'TRELLO_OAUTH1', 'TRUSTED_IDP' "
            "and others, and the set is owned by the server, so the SDK accepts any "
            "string and passes an unknown type through unchanged rather than "
            "failing to parse. The type of an existing connector cannot be changed."
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
            "Optional. List of AuthField objects defining the inputs the user must "
            "supply. For BEARER and API_KEY these are the credential itself. OAUTH "
            "patterns also use them, for options gathered before the browser flow "
            "starts rather than for credentials, which the flow collects itself. "
            "Leave empty for NO_AUTH, which collects nothing. Defaults to empty list."
        ),
    )
    account_fields: List[AuthField] = Field(
        default_factory=list,
        description=(
            "Optional. Inputs collected per connected account rather than once per "
            "connection, for connectors that need an account-scoped value (a "
            "workspace or subdomain, say) alongside the shared credential. Same "
            "shape as 'fields'. Defaults to empty list."
        ),
    )
    is_mcp: bool = Field(
        False,
        description=(
            "Optional. Set to True for MCP (Model Context Protocol) server connectors. "
            "When True the server sets is_custom_mcp=True on the provider. "
            "The server forces it to False on an OpenAPI-sourced connector. "
            "Defaults to False."
        ),
    )
    is_open_api: bool = Field(
        False,
        description=(
            "Read-only. True on the pattern of an OpenAPI-sourced connector (one created "
            "with openapi_spec_url). The server derives it from the connector and ignores "
            "a value you send on create, so leave it False when you author a pattern. Keep "
            "it as returned when you send a pattern back to update_custom_provider: the "
            "server compares patterns by content, so a pattern rebuilt without it counts "
            "as a change. Defaults to False."
        ),
    )
    oauth_config: Optional["OAuthConfig"] = Field(
        None,
        description=(
            "Optional. OAuth configuration. Required when type='OAUTH'; omit for "
            "'BEARER' and 'API_KEY'. "
            "Pass OAuthConfig() for MCP connectors using Dynamic Client Registration. "
            "Pass OAuthConfig(pkce_enabled=False) to disable PKCE. "
            "The managed catalogue also attaches one to its other OAuth-family "
            "types ('OAUTH_M2M', 'GOOGLE_DWD', 'TRELLO_OAUTH1'). "
            "Defaults to None."
        ),
    )
    auth_header_key_override: str = Field(
        "",
        description=(
            "Optional. Overrides the HTTP header name Scalekit uses when injecting "
            "the static credential into proxied requests. Applies to BEARER and "
            "API_KEY patterns. Example: 'x-api-key' to send the credential in the "
            "'x-api-key' header instead of the default 'Authorization' header. "
            "Defaults to empty string (use the default header)."
        ),
    )
    allowed_proxy_domains: List[str] = Field(
        default_factory=list,
        description=(
            "Optional. Domains this connector's proxied requests may be routed to. "
            "Empty means no domain restriction beyond the provider's proxy_url. "
            "Defaults to empty list."
        ),
    )

    # Set on instances produced by from_dict. validate_assignment=True re-runs
    # the validator below on every attribute write, and that re-run carries no
    # validation context, so without this flag editing a decoded provider would
    # raise for a shape the server legitimately served.
    _decoded: bool = PrivateAttr(default=False)

    @model_validator(mode="after")
    def validate_auth_invariants(self, info: ValidationInfo):
        """Guard the shapes create_custom_provider accepts.

        These are SDK-side authoring guardrails, not server rules — the API
        validates almost nothing about an auth pattern. So they are skipped for
        anything decoded from a response (from_dict passes decoding=True): the
        managed catalogue legitimately serves shapes a caller should not
        hand-author, and refusing one would break list_providers() for the whole
        page.
        """
        if (info.context or {}).get("decoding"):
            self._decoded = True
            return self
        if self._decoded:
            return self
        if self.type == "OAUTH" and self.oauth_config is None:
            raise ValueError("oauth_config is required when type='OAUTH'")
        if self.type == "NO_AUTH" and self.fields:
            raise ValueError("fields must be empty when type='NO_AUTH'")
        return self

    def to_dict(self) -> dict:
        """Serialize to a wire-format dict for inclusion in the auth_patterns ListValue.

        The normalised view, built from the values of the pattern, whether it was decoded,
        constructed or edited. It is not what update_custom_provider sends for a pattern
        decoded from a response: the SDK sends that exactly as the server returned it while
        it is unchanged (see the class docstring).

        :returns: Dict representation of this auth pattern. 'description' is omitted
                  when empty, 'is_mcp' and 'is_open_api' when False, 'oauth_config' when None, and
                  'auth_header_key_override', 'account_fields' and
                  'allowed_proxy_domains' when empty, to keep the wire payload
                  minimal. Keys the SDK does not declare are re-emitted unchanged.
        :rtype: dict
        """
        return self._build_dict(lambda child: child.to_dict())

    def _build_dict(self, encode: Callable[[_ServedForm], dict]) -> dict:
        d: dict = {
            "type": self.type,
            "display_name": self.display_name,
            "fields": [encode(f) for f in self.fields],
        }
        if self.description:
            d["description"] = self.description
        if self.is_mcp:
            d["is_mcp"] = True
        if self.is_open_api:
            d["is_open_api"] = True
        if self.oauth_config is not None:
            d["oauth_config"] = encode(self.oauth_config)
        if self.auth_header_key_override:
            d["auth_header_key_override"] = self.auth_header_key_override
        if self.account_fields:
            d["account_fields"] = [encode(f) for f in self.account_fields]
        if self.allowed_proxy_domains:
            d["allowed_proxy_domains"] = list(self.allowed_proxy_domains)
        d.update(self.model_extra or {})
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AuthPattern":
        """Deserialize an AuthPattern from a response dict.

        Decoding is deliberately permissive: the authoring guardrails in
        validate_auth_invariants are skipped, unknown 'type' values are accepted,
        and keys this SDK does not declare are kept on the instance. A managed
        provider whose shape the SDK has not seen still decodes, instead of
        failing the whole list_providers() page.

        :param d: Dict containing auth pattern data as returned by the server.
                  The 'oauth_config' key must be present for OAuth patterns;
                  its absence is interpreted as oauth_config=None.
        :type d: dict
        :returns: AuthPattern instance populated from the dict values.
        :rtype: AuthPattern
        """
        # A JSON null is treated as absent, not as an empty config: the server
        # models oauth_config as a nullable pointer, so the key can arrive with
        # no value.
        oauth_cfg: Optional[OAuthConfig] = None
        if d.get("oauth_config") is not None:
            oauth_cfg = OAuthConfig.from_dict(d["oauth_config"])
        known = {
            "type": d.get("type", ""),
            "display_name": d.get("display_name", ""),
            "description": d.get("description", ""),
            "fields": [AuthField.from_dict(f) for f in d.get("fields") or []],
            "account_fields": [
                AuthField.from_dict(f) for f in d.get("account_fields") or []
            ],
            "is_mcp": d.get("is_mcp", False),
            "is_open_api": d.get("is_open_api", False),
            "oauth_config": oauth_cfg,
            "auth_header_key_override": d.get("auth_header_key_override", ""),
            "allowed_proxy_domains": list(d.get("allowed_proxy_domains") or []),
        }
        extras = {k: v for k, v in d.items() if k not in known}
        pattern = cls.model_validate({**known, **extras}, context={"decoding": True})
        pattern._remember_served(d)
        return pattern

    class Config:
        validate_assignment = True
        extra = "allow"


class Provider(BaseModel):
    """A custom provider as returned by the Scalekit API.

    Produced exclusively by ProvidersClient response decoding via from_proto().
    All fields are populated from the server response — do not construct this
    directly. The auth_patterns list is fully decoded so callers never need to
    handle protobuf types.
    """

    id: str = Field(
        "",
        description="Unique provider ID assigned by the server (for example 'prvd_...'). Read-only.",
    )
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
        description=(
            "For an MCP-sourced connector, the MCP server URL that requests to this "
            "provider are routed through. For an OpenAPI-sourced connector "
            "(openapi_spec_url is set), its base URL, which replaces the spec's own "
            "server URL for every tool call: it is filled in from the spec's server URL "
            "once the first tool collection run completes (only when that URL starts "
            "with https://) and can be changed with update_custom_provider."
        ),
    )
    proxy_enabled: bool = Field(
        False,
        description="Whether request proxying is enabled for this provider.",
    )
    openapi_spec_url: str = Field(
        "",
        description=(
            "URL of the OpenAPI spec (JSON or YAML) this connector was sourced from. "
            "Set only for an OpenAPI-sourced custom connector; empty otherwise. You choose "
            "it when you create the connector; changing it later with "
            "update_custom_provider is not enabled for every workspace."
        ),
    )
    icon_src: str = Field(
        "",
        description="URL of the provider's icon image. Empty string when not set.",
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Arbitrary string key-value pairs attached to the provider. "
            "Empty dict when none are set."
        ),
    )
    categories: List[str] = Field(
        default_factory=list,
        description="Categories the provider is listed under (for example ['AI', 'Search']). Empty list when none are set.",
    )
    display_priority: int = Field(
        0,
        description="Sort priority used when listing providers. Read-only.",
    )
    coming_soon: bool = Field(
        False,
        description="True for providers that are announced but not yet available. Read-only.",
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
            id=proto.id,
            identifier=proto.identifier,
            display_name=proto.display_name,
            description=proto.description,
            proxy_url=proto.proxy_url,
            proxy_enabled=proto.proxy_enabled,
            openapi_spec_url=proto.openapi_spec_url,
            icon_src=proto.icon_src,
            metadata=dict(proto.metadata),
            categories=list(proto.categories),
            display_priority=proto.display_priority,
            coming_soon=proto.coming_soon,
            is_custom=proto.is_custom,
            is_custom_mcp=proto.is_custom_mcp,
            auth_patterns=[AuthPattern.from_dict(p) for p in auth_patterns_raw],
        )

    class Config:
        validate_assignment = True

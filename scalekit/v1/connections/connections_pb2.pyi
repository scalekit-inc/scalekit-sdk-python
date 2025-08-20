from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.domains import domains_pb2 as _domains_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CodeChallengeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CODE_CHALLENGE_TYPE_UNSPECIFIED: _ClassVar[CodeChallengeType]
    NUMERIC: _ClassVar[CodeChallengeType]
    ALPHANUMERIC: _ClassVar[CodeChallengeType]

class ConfigurationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONFIGURATION_TYPE_UNSPECIFIED: _ClassVar[ConfigurationType]
    DISCOVERY: _ClassVar[ConfigurationType]
    MANUAL: _ClassVar[ConfigurationType]

class NameIdFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NAME_ID_FORMAT_NIL: _ClassVar[NameIdFormat]
    UNSPECIFIED: _ClassVar[NameIdFormat]
    EMAIL: _ClassVar[NameIdFormat]
    TRANSIENT: _ClassVar[NameIdFormat]
    PERSISTENT: _ClassVar[NameIdFormat]

class PasswordlessType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PasswordlessType_UNSPECIFIED: _ClassVar[PasswordlessType]
    LINK: _ClassVar[PasswordlessType]
    OTP: _ClassVar[PasswordlessType]
    LINK_OTP: _ClassVar[PasswordlessType]

class TestResultStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PENDING: _ClassVar[TestResultStatus]
    SUCCESS: _ClassVar[TestResultStatus]
    FAILURE: _ClassVar[TestResultStatus]

class SAMLSigningOptions(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SAML_SIGNING_OPTIONS_UNSPECIFIED: _ClassVar[SAMLSigningOptions]
    NO_SIGNING: _ClassVar[SAMLSigningOptions]
    SAML_ONLY_RESPONSE_SIGNING: _ClassVar[SAMLSigningOptions]
    SAML_ONLY_ASSERTION_SIGNING: _ClassVar[SAMLSigningOptions]
    SAML_RESPONSE_ASSERTION_SIGNING: _ClassVar[SAMLSigningOptions]
    SAML_RESPONSE_OR_ASSERTION_SIGNING: _ClassVar[SAMLSigningOptions]

class RequestBinding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REQUEST_BINDING_UNSPECIFIED: _ClassVar[RequestBinding]
    HTTP_POST: _ClassVar[RequestBinding]
    HTTP_REDIRECT: _ClassVar[RequestBinding]

class TokenAuthType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOKEN_AUTH_TYPE_UNSPECIFIED: _ClassVar[TokenAuthType]
    URL_PARAMS: _ClassVar[TokenAuthType]
    BASIC_AUTH: _ClassVar[TokenAuthType]

class OIDCScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OIDC_SCOPE_UNSPECIFIED: _ClassVar[OIDCScope]
    openid: _ClassVar[OIDCScope]
    profile: _ClassVar[OIDCScope]
    email: _ClassVar[OIDCScope]
    address: _ClassVar[OIDCScope]
    phone: _ClassVar[OIDCScope]

class ConnectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID: _ClassVar[ConnectionType]
    OIDC: _ClassVar[ConnectionType]
    SAML: _ClassVar[ConnectionType]
    PASSWORD: _ClassVar[ConnectionType]
    OAUTH: _ClassVar[ConnectionType]
    PASSWORDLESS: _ClassVar[ConnectionType]
    BASIC: _ClassVar[ConnectionType]
    BEARER: _ClassVar[ConnectionType]
    API_KEY: _ClassVar[ConnectionType]

class ConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTION_STATUS_UNSPECIFIED: _ClassVar[ConnectionStatus]
    DRAFT: _ClassVar[ConnectionStatus]
    IN_PROGRESS: _ClassVar[ConnectionStatus]
    COMPLETED: _ClassVar[ConnectionStatus]

class ConnectionProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTION_PROVIDER_UNSPECIFIED: _ClassVar[ConnectionProvider]
    OKTA: _ClassVar[ConnectionProvider]
    GOOGLE: _ClassVar[ConnectionProvider]
    MICROSOFT_AD: _ClassVar[ConnectionProvider]
    AUTH0: _ClassVar[ConnectionProvider]
    ONELOGIN: _ClassVar[ConnectionProvider]
    PING_IDENTITY: _ClassVar[ConnectionProvider]
    JUMPCLOUD: _ClassVar[ConnectionProvider]
    CUSTOM: _ClassVar[ConnectionProvider]
    GITHUB: _ClassVar[ConnectionProvider]
    GITLAB: _ClassVar[ConnectionProvider]
    LINKEDIN: _ClassVar[ConnectionProvider]
    SALESFORCE: _ClassVar[ConnectionProvider]
    MICROSOFT: _ClassVar[ConnectionProvider]
    IDP_SIMULATOR: _ClassVar[ConnectionProvider]
    SCALEKIT: _ClassVar[ConnectionProvider]
    ADFS: _ClassVar[ConnectionProvider]
CODE_CHALLENGE_TYPE_UNSPECIFIED: CodeChallengeType
NUMERIC: CodeChallengeType
ALPHANUMERIC: CodeChallengeType
CONFIGURATION_TYPE_UNSPECIFIED: ConfigurationType
DISCOVERY: ConfigurationType
MANUAL: ConfigurationType
NAME_ID_FORMAT_NIL: NameIdFormat
UNSPECIFIED: NameIdFormat
EMAIL: NameIdFormat
TRANSIENT: NameIdFormat
PERSISTENT: NameIdFormat
PasswordlessType_UNSPECIFIED: PasswordlessType
LINK: PasswordlessType
OTP: PasswordlessType
LINK_OTP: PasswordlessType
PENDING: TestResultStatus
SUCCESS: TestResultStatus
FAILURE: TestResultStatus
SAML_SIGNING_OPTIONS_UNSPECIFIED: SAMLSigningOptions
NO_SIGNING: SAMLSigningOptions
SAML_ONLY_RESPONSE_SIGNING: SAMLSigningOptions
SAML_ONLY_ASSERTION_SIGNING: SAMLSigningOptions
SAML_RESPONSE_ASSERTION_SIGNING: SAMLSigningOptions
SAML_RESPONSE_OR_ASSERTION_SIGNING: SAMLSigningOptions
REQUEST_BINDING_UNSPECIFIED: RequestBinding
HTTP_POST: RequestBinding
HTTP_REDIRECT: RequestBinding
TOKEN_AUTH_TYPE_UNSPECIFIED: TokenAuthType
URL_PARAMS: TokenAuthType
BASIC_AUTH: TokenAuthType
OIDC_SCOPE_UNSPECIFIED: OIDCScope
openid: OIDCScope
profile: OIDCScope
email: OIDCScope
address: OIDCScope
phone: OIDCScope
INVALID: ConnectionType
OIDC: ConnectionType
SAML: ConnectionType
PASSWORD: ConnectionType
OAUTH: ConnectionType
PASSWORDLESS: ConnectionType
BASIC: ConnectionType
BEARER: ConnectionType
API_KEY: ConnectionType
CONNECTION_STATUS_UNSPECIFIED: ConnectionStatus
DRAFT: ConnectionStatus
IN_PROGRESS: ConnectionStatus
COMPLETED: ConnectionStatus
CONNECTION_PROVIDER_UNSPECIFIED: ConnectionProvider
OKTA: ConnectionProvider
GOOGLE: ConnectionProvider
MICROSOFT_AD: ConnectionProvider
AUTH0: ConnectionProvider
ONELOGIN: ConnectionProvider
PING_IDENTITY: ConnectionProvider
JUMPCLOUD: ConnectionProvider
CUSTOM: ConnectionProvider
GITHUB: ConnectionProvider
GITLAB: ConnectionProvider
LINKEDIN: ConnectionProvider
SALESFORCE: ConnectionProvider
MICROSOFT: ConnectionProvider
IDP_SIMULATOR: ConnectionProvider
SCALEKIT: ConnectionProvider
ADFS: ConnectionProvider

class AssignDomainsToConnectionRequest(_message.Message):
    __slots__ = ("organization_id", "connection_id", "domain_ids")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_IDS_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    connection_id: str
    domain_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, organization_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., domain_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AssignDomainsToConnectionResponse(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: Connection
    def __init__(self, connection: _Optional[_Union[Connection, _Mapping]] = ...) -> None: ...

class GetProvidersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetProvidersResponse(_message.Message):
    __slots__ = ("providers",)
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[Provider]
    def __init__(self, providers: _Optional[_Iterable[_Union[Provider, _Mapping]]] = ...) -> None: ...

class Provider(_message.Message):
    __slots__ = ("key_id", "display_name", "description")
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    key_id: str
    display_name: str
    description: str
    def __init__(self, key_id: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateEnvironmentConnectionRequest(_message.Message):
    __slots__ = ("connection", "flags")
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    connection: CreateConnection
    flags: Flags
    def __init__(self, connection: _Optional[_Union[CreateConnection, _Mapping]] = ..., flags: _Optional[_Union[Flags, _Mapping]] = ...) -> None: ...

class CreateConnectionRequest(_message.Message):
    __slots__ = ("organization_id", "connection")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    connection: CreateConnection
    def __init__(self, organization_id: _Optional[str] = ..., connection: _Optional[_Union[CreateConnection, _Mapping]] = ...) -> None: ...

class CreateConnection(_message.Message):
    __slots__ = ("provider", "type", "provider_key", "key_id")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_KEY_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    provider: ConnectionProvider
    type: ConnectionType
    provider_key: str
    key_id: str
    def __init__(self, provider: _Optional[_Union[ConnectionProvider, str]] = ..., type: _Optional[_Union[ConnectionType, str]] = ..., provider_key: _Optional[str] = ..., key_id: _Optional[str] = ...) -> None: ...

class Connection(_message.Message):
    __slots__ = ("id", "provider", "type", "status", "enabled", "debug_enabled", "organization_id", "ui_button_title", "configuration_type", "test_connection_uri", "attribute_mapping", "create_time", "update_time", "oidc_config", "saml_config", "oauth_config", "passwordless_config", "static_config", "key_id", "provider_key", "domains")
    class AttributeMappingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DEBUG_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    UI_BUTTON_TITLE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEST_CONNECTION_URI_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    OIDC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SAML_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OAUTH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PASSWORDLESS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_KEY_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    id: str
    provider: ConnectionProvider
    type: ConnectionType
    status: ConnectionStatus
    enabled: bool
    debug_enabled: bool
    organization_id: str
    ui_button_title: str
    configuration_type: ConfigurationType
    test_connection_uri: str
    attribute_mapping: _containers.ScalarMap[str, str]
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    oidc_config: OIDCConnectionConfig
    saml_config: SAMLConnectionConfigResponse
    oauth_config: OAuthConnectionConfig
    passwordless_config: PasswordLessConfig
    static_config: StaticAuthConfig
    key_id: str
    provider_key: str
    domains: _containers.RepeatedCompositeFieldContainer[_domains_pb2.Domain]
    def __init__(self, id: _Optional[str] = ..., provider: _Optional[_Union[ConnectionProvider, str]] = ..., type: _Optional[_Union[ConnectionType, str]] = ..., status: _Optional[_Union[ConnectionStatus, str]] = ..., enabled: bool = ..., debug_enabled: bool = ..., organization_id: _Optional[str] = ..., ui_button_title: _Optional[str] = ..., configuration_type: _Optional[_Union[ConfigurationType, str]] = ..., test_connection_uri: _Optional[str] = ..., attribute_mapping: _Optional[_Mapping[str, str]] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., oidc_config: _Optional[_Union[OIDCConnectionConfig, _Mapping]] = ..., saml_config: _Optional[_Union[SAMLConnectionConfigResponse, _Mapping]] = ..., oauth_config: _Optional[_Union[OAuthConnectionConfig, _Mapping]] = ..., passwordless_config: _Optional[_Union[PasswordLessConfig, _Mapping]] = ..., static_config: _Optional[_Union[StaticAuthConfig, _Mapping]] = ..., key_id: _Optional[str] = ..., provider_key: _Optional[str] = ..., domains: _Optional[_Iterable[_Union[_domains_pb2.Domain, _Mapping]]] = ...) -> None: ...

class CreateConnectionResponse(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: Connection
    def __init__(self, connection: _Optional[_Union[Connection, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentConnectionRequest(_message.Message):
    __slots__ = ("connection_id", "connection")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connection: UpdateConnection
    def __init__(self, connection_id: _Optional[str] = ..., connection: _Optional[_Union[UpdateConnection, _Mapping]] = ...) -> None: ...

class UpdateConnectionRequest(_message.Message):
    __slots__ = ("organization_id", "id", "connection")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    connection: UpdateConnection
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., connection: _Optional[_Union[UpdateConnection, _Mapping]] = ...) -> None: ...

class UpdateConnection(_message.Message):
    __slots__ = ("provider", "type", "debug_enabled", "ui_button_title", "configuration_type", "attribute_mapping", "oidc_config", "saml_config", "oauth_config", "passwordless_config", "static_config", "key_id", "provider_key")
    class AttributeMappingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DEBUG_ENABLED_FIELD_NUMBER: _ClassVar[int]
    UI_BUTTON_TITLE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    OIDC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SAML_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OAUTH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PASSWORDLESS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_KEY_FIELD_NUMBER: _ClassVar[int]
    provider: ConnectionProvider
    type: ConnectionType
    debug_enabled: _wrappers_pb2.BoolValue
    ui_button_title: _wrappers_pb2.StringValue
    configuration_type: ConfigurationType
    attribute_mapping: _containers.ScalarMap[str, str]
    oidc_config: OIDCConnectionConfig
    saml_config: SAMLConnectionConfigRequest
    oauth_config: OAuthConnectionConfig
    passwordless_config: PasswordLessConfig
    static_config: StaticAuthConfig
    key_id: str
    provider_key: str
    def __init__(self, provider: _Optional[_Union[ConnectionProvider, str]] = ..., type: _Optional[_Union[ConnectionType, str]] = ..., debug_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., ui_button_title: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., configuration_type: _Optional[_Union[ConfigurationType, str]] = ..., attribute_mapping: _Optional[_Mapping[str, str]] = ..., oidc_config: _Optional[_Union[OIDCConnectionConfig, _Mapping]] = ..., saml_config: _Optional[_Union[SAMLConnectionConfigRequest, _Mapping]] = ..., oauth_config: _Optional[_Union[OAuthConnectionConfig, _Mapping]] = ..., passwordless_config: _Optional[_Union[PasswordLessConfig, _Mapping]] = ..., static_config: _Optional[_Union[StaticAuthConfig, _Mapping]] = ..., key_id: _Optional[str] = ..., provider_key: _Optional[str] = ...) -> None: ...

class UpdateConnectionResponse(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: Connection
    def __init__(self, connection: _Optional[_Union[Connection, _Mapping]] = ...) -> None: ...

class DeleteEnvironmentConnectionRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class DeleteConnectionRequest(_message.Message):
    __slots__ = ("organization_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetEnvironmentConnectionRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class GetConnectionRequest(_message.Message):
    __slots__ = ("organization_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetConnectionResponse(_message.Message):
    __slots__ = ("connection",)
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: Connection
    def __init__(self, connection: _Optional[_Union[Connection, _Mapping]] = ...) -> None: ...

class ListConnectionsRequest(_message.Message):
    __slots__ = ("organization_id", "domain", "include")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    domain: str
    include: str
    def __init__(self, organization_id: _Optional[str] = ..., domain: _Optional[str] = ..., include: _Optional[str] = ...) -> None: ...

class ListConnectionsResponse(_message.Message):
    __slots__ = ("connections",)
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[ListConnection]
    def __init__(self, connections: _Optional[_Iterable[_Union[ListConnection, _Mapping]]] = ...) -> None: ...

class ListConnection(_message.Message):
    __slots__ = ("id", "provider", "type", "status", "enabled", "organization_id", "ui_button_title", "domains", "organization_name", "provider_key", "key_id", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    UI_BUTTON_TITLE_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_KEY_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    provider: ConnectionProvider
    type: ConnectionType
    status: ConnectionStatus
    enabled: bool
    organization_id: str
    ui_button_title: str
    domains: _containers.RepeatedScalarFieldContainer[str]
    organization_name: str
    provider_key: str
    key_id: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., provider: _Optional[_Union[ConnectionProvider, str]] = ..., type: _Optional[_Union[ConnectionType, str]] = ..., status: _Optional[_Union[ConnectionStatus, str]] = ..., enabled: bool = ..., organization_id: _Optional[str] = ..., ui_button_title: _Optional[str] = ..., domains: _Optional[_Iterable[str]] = ..., organization_name: _Optional[str] = ..., provider_key: _Optional[str] = ..., key_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListOrganizationConnectionsRequest(_message.Message):
    __slots__ = ("page_size", "page_token")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListOrganizationConnectionsResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "prev_page_token", "connections")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    prev_page_token: str
    connections: _containers.RepeatedCompositeFieldContainer[ListConnection]
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ..., connections: _Optional[_Iterable[_Union[ListConnection, _Mapping]]] = ...) -> None: ...

class SearchOrganizationConnectionsRequest(_message.Message):
    __slots__ = ("query", "provider", "status", "connection_type", "enabled", "page_size", "page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: str
    provider: str
    status: ConnectionStatus
    connection_type: ConnectionType
    enabled: bool
    page_size: int
    page_token: str
    def __init__(self, query: _Optional[str] = ..., provider: _Optional[str] = ..., status: _Optional[_Union[ConnectionStatus, str]] = ..., connection_type: _Optional[_Union[ConnectionType, str]] = ..., enabled: bool = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class SearchOrganizationConnectionsResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "prev_page_token", "connections")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    prev_page_token: str
    connections: _containers.RepeatedCompositeFieldContainer[ListConnection]
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ..., connections: _Optional[_Iterable[_Union[ListConnection, _Mapping]]] = ...) -> None: ...

class ToggleEnvironmentConnectionRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class ToggleConnectionRequest(_message.Message):
    __slots__ = ("organization_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class ToggleConnectionResponse(_message.Message):
    __slots__ = ("enabled", "error_message")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    error_message: str
    def __init__(self, enabled: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class OIDCConnectionConfig(_message.Message):
    __slots__ = ("issuer", "discovery_endpoint", "authorize_uri", "token_uri", "user_info_uri", "jwks_uri", "client_id", "client_secret", "scopes", "token_auth_type", "redirect_uri", "pkce_enabled", "idp_logout_required", "post_logout_redirect_uri", "backchannel_logout_redirect_uri")
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    DISCOVERY_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZE_URI_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URI_FIELD_NUMBER: _ClassVar[int]
    USER_INFO_URI_FIELD_NUMBER: _ClassVar[int]
    JWKS_URI_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_AUTH_TYPE_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    PKCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IDP_LOGOUT_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    POST_LOGOUT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    BACKCHANNEL_LOGOUT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    issuer: _wrappers_pb2.StringValue
    discovery_endpoint: _wrappers_pb2.StringValue
    authorize_uri: _wrappers_pb2.StringValue
    token_uri: _wrappers_pb2.StringValue
    user_info_uri: _wrappers_pb2.StringValue
    jwks_uri: _wrappers_pb2.StringValue
    client_id: _wrappers_pb2.StringValue
    client_secret: _wrappers_pb2.StringValue
    scopes: _containers.RepeatedScalarFieldContainer[OIDCScope]
    token_auth_type: TokenAuthType
    redirect_uri: str
    pkce_enabled: _wrappers_pb2.BoolValue
    idp_logout_required: _wrappers_pb2.BoolValue
    post_logout_redirect_uri: _wrappers_pb2.StringValue
    backchannel_logout_redirect_uri: _wrappers_pb2.StringValue
    def __init__(self, issuer: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., discovery_endpoint: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., authorize_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., token_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., user_info_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., jwks_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., client_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., client_secret: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., scopes: _Optional[_Iterable[_Union[OIDCScope, str]]] = ..., token_auth_type: _Optional[_Union[TokenAuthType, str]] = ..., redirect_uri: _Optional[str] = ..., pkce_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., idp_logout_required: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., post_logout_redirect_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., backchannel_logout_redirect_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class OAuthConnectionConfig(_message.Message):
    __slots__ = ("authorize_uri", "token_uri", "user_info_uri", "client_id", "client_secret", "scopes", "redirect_uri", "pkce_enabled", "prompt", "use_platform_creds", "access_type")
    AUTHORIZE_URI_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URI_FIELD_NUMBER: _ClassVar[int]
    USER_INFO_URI_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    PKCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    USE_PLATFORM_CREDS_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    authorize_uri: _wrappers_pb2.StringValue
    token_uri: _wrappers_pb2.StringValue
    user_info_uri: _wrappers_pb2.StringValue
    client_id: _wrappers_pb2.StringValue
    client_secret: _wrappers_pb2.StringValue
    scopes: _containers.RepeatedScalarFieldContainer[str]
    redirect_uri: str
    pkce_enabled: _wrappers_pb2.BoolValue
    prompt: _wrappers_pb2.StringValue
    use_platform_creds: _wrappers_pb2.BoolValue
    access_type: _wrappers_pb2.StringValue
    def __init__(self, authorize_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., token_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., user_info_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., client_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., client_secret: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., scopes: _Optional[_Iterable[str]] = ..., redirect_uri: _Optional[str] = ..., pkce_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., prompt: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., use_platform_creds: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., access_type: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class PasswordLessConfig(_message.Message):
    __slots__ = ("type", "frequency", "validity", "enforce_same_browser_origin", "code_challenge_length", "code_challenge_type", "regenerate_passwordless_credentials_on_resend")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_SAME_BROWSER_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    CODE_CHALLENGE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    CODE_CHALLENGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REGENERATE_PASSWORDLESS_CREDENTIALS_ON_RESEND_FIELD_NUMBER: _ClassVar[int]
    type: PasswordlessType
    frequency: _wrappers_pb2.UInt32Value
    validity: _wrappers_pb2.UInt32Value
    enforce_same_browser_origin: _wrappers_pb2.BoolValue
    code_challenge_length: _wrappers_pb2.UInt32Value
    code_challenge_type: CodeChallengeType
    regenerate_passwordless_credentials_on_resend: _wrappers_pb2.BoolValue
    def __init__(self, type: _Optional[_Union[PasswordlessType, str]] = ..., frequency: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., validity: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., enforce_same_browser_origin: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., code_challenge_length: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., code_challenge_type: _Optional[_Union[CodeChallengeType, str]] = ..., regenerate_passwordless_credentials_on_resend: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class StaticAuthConfig(_message.Message):
    __slots__ = ("static_config",)
    STATIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    static_config: _struct_pb2.Struct
    def __init__(self, static_config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SAMLConnectionConfigRequest(_message.Message):
    __slots__ = ("idp_metadata_url", "idp_entity_id", "idp_sso_url", "idp_certificate", "idp_slo_url", "ui_button_title", "idp_name_id_format", "idp_sso_request_binding", "idp_slo_request_binding", "saml_signing_option", "force_authn", "default_redirect_uri", "assertion_encrypted", "want_request_signed", "certificate_id", "idp_slo_required")
    IDP_METADATA_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    IDP_SSO_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    IDP_SLO_URL_FIELD_NUMBER: _ClassVar[int]
    UI_BUTTON_TITLE_FIELD_NUMBER: _ClassVar[int]
    IDP_NAME_ID_FORMAT_FIELD_NUMBER: _ClassVar[int]
    IDP_SSO_REQUEST_BINDING_FIELD_NUMBER: _ClassVar[int]
    IDP_SLO_REQUEST_BINDING_FIELD_NUMBER: _ClassVar[int]
    SAML_SIGNING_OPTION_FIELD_NUMBER: _ClassVar[int]
    FORCE_AUTHN_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    ASSERTION_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    WANT_REQUEST_SIGNED_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_ID_FIELD_NUMBER: _ClassVar[int]
    IDP_SLO_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    idp_metadata_url: _wrappers_pb2.StringValue
    idp_entity_id: _wrappers_pb2.StringValue
    idp_sso_url: _wrappers_pb2.StringValue
    idp_certificate: _wrappers_pb2.StringValue
    idp_slo_url: _wrappers_pb2.StringValue
    ui_button_title: _wrappers_pb2.StringValue
    idp_name_id_format: NameIdFormat
    idp_sso_request_binding: RequestBinding
    idp_slo_request_binding: RequestBinding
    saml_signing_option: SAMLSigningOptions
    force_authn: _wrappers_pb2.BoolValue
    default_redirect_uri: _wrappers_pb2.StringValue
    assertion_encrypted: _wrappers_pb2.BoolValue
    want_request_signed: _wrappers_pb2.BoolValue
    certificate_id: _wrappers_pb2.StringValue
    idp_slo_required: _wrappers_pb2.BoolValue
    def __init__(self, idp_metadata_url: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_entity_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_sso_url: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_certificate: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_slo_url: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., ui_button_title: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_name_id_format: _Optional[_Union[NameIdFormat, str]] = ..., idp_sso_request_binding: _Optional[_Union[RequestBinding, str]] = ..., idp_slo_request_binding: _Optional[_Union[RequestBinding, str]] = ..., saml_signing_option: _Optional[_Union[SAMLSigningOptions, str]] = ..., force_authn: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., default_redirect_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., assertion_encrypted: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., want_request_signed: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., certificate_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_slo_required: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class SAMLConnectionConfigResponse(_message.Message):
    __slots__ = ("sp_entity_id", "sp_assertion_url", "sp_metadata_url", "idp_metadata_url", "idp_entity_id", "idp_sso_url", "idp_certificates", "idp_slo_url", "ui_button_title", "idp_name_id_format", "idp_sso_request_binding", "idp_slo_request_binding", "saml_signing_option", "allow_idp_initiated_login", "force_authn", "default_redirect_uri", "assertion_encrypted", "want_request_signed", "certificate_id", "idp_slo_required", "sp_slo_url")
    SP_ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    SP_ASSERTION_URL_FIELD_NUMBER: _ClassVar[int]
    SP_METADATA_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_METADATA_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    IDP_SSO_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    IDP_SLO_URL_FIELD_NUMBER: _ClassVar[int]
    UI_BUTTON_TITLE_FIELD_NUMBER: _ClassVar[int]
    IDP_NAME_ID_FORMAT_FIELD_NUMBER: _ClassVar[int]
    IDP_SSO_REQUEST_BINDING_FIELD_NUMBER: _ClassVar[int]
    IDP_SLO_REQUEST_BINDING_FIELD_NUMBER: _ClassVar[int]
    SAML_SIGNING_OPTION_FIELD_NUMBER: _ClassVar[int]
    ALLOW_IDP_INITIATED_LOGIN_FIELD_NUMBER: _ClassVar[int]
    FORCE_AUTHN_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    ASSERTION_ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    WANT_REQUEST_SIGNED_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_ID_FIELD_NUMBER: _ClassVar[int]
    IDP_SLO_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    SP_SLO_URL_FIELD_NUMBER: _ClassVar[int]
    sp_entity_id: str
    sp_assertion_url: str
    sp_metadata_url: str
    idp_metadata_url: _wrappers_pb2.StringValue
    idp_entity_id: _wrappers_pb2.StringValue
    idp_sso_url: _wrappers_pb2.StringValue
    idp_certificates: _containers.RepeatedCompositeFieldContainer[IDPCertificate]
    idp_slo_url: _wrappers_pb2.StringValue
    ui_button_title: _wrappers_pb2.StringValue
    idp_name_id_format: NameIdFormat
    idp_sso_request_binding: RequestBinding
    idp_slo_request_binding: RequestBinding
    saml_signing_option: SAMLSigningOptions
    allow_idp_initiated_login: _wrappers_pb2.BoolValue
    force_authn: _wrappers_pb2.BoolValue
    default_redirect_uri: _wrappers_pb2.StringValue
    assertion_encrypted: _wrappers_pb2.BoolValue
    want_request_signed: _wrappers_pb2.BoolValue
    certificate_id: _wrappers_pb2.StringValue
    idp_slo_required: _wrappers_pb2.BoolValue
    sp_slo_url: _wrappers_pb2.StringValue
    def __init__(self, sp_entity_id: _Optional[str] = ..., sp_assertion_url: _Optional[str] = ..., sp_metadata_url: _Optional[str] = ..., idp_metadata_url: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_entity_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_sso_url: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_certificates: _Optional[_Iterable[_Union[IDPCertificate, _Mapping]]] = ..., idp_slo_url: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., ui_button_title: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_name_id_format: _Optional[_Union[NameIdFormat, str]] = ..., idp_sso_request_binding: _Optional[_Union[RequestBinding, str]] = ..., idp_slo_request_binding: _Optional[_Union[RequestBinding, str]] = ..., saml_signing_option: _Optional[_Union[SAMLSigningOptions, str]] = ..., allow_idp_initiated_login: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., force_authn: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., default_redirect_uri: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., assertion_encrypted: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., want_request_signed: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., certificate_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., idp_slo_required: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., sp_slo_url: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class IDPCertificate(_message.Message):
    __slots__ = ("certificate", "create_time", "expiry_time", "id", "issuer")
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_TIME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    certificate: str
    create_time: _timestamp_pb2.Timestamp
    expiry_time: _timestamp_pb2.Timestamp
    id: str
    issuer: str
    def __init__(self, certificate: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expiry_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., issuer: _Optional[str] = ...) -> None: ...

class GetOIDCMetadataRequest(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: OIDCMetadataRequest
    def __init__(self, metadata: _Optional[_Union[OIDCMetadataRequest, _Mapping]] = ...) -> None: ...

class OIDCMetadataRequest(_message.Message):
    __slots__ = ("issuer",)
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    issuer: str
    def __init__(self, issuer: _Optional[str] = ...) -> None: ...

class GetOIDCMetadataResponse(_message.Message):
    __slots__ = ("issuer", "authorization_endpoint", "token_endpoint", "userinfo_endpoint", "jwks_uri")
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    USERINFO_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    JWKS_URI_FIELD_NUMBER: _ClassVar[int]
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str
    def __init__(self, issuer: _Optional[str] = ..., authorization_endpoint: _Optional[str] = ..., token_endpoint: _Optional[str] = ..., userinfo_endpoint: _Optional[str] = ..., jwks_uri: _Optional[str] = ...) -> None: ...

class GetSAMLMetadataRequest(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: SAMLMetadataRequest
    def __init__(self, metadata: _Optional[_Union[SAMLMetadataRequest, _Mapping]] = ...) -> None: ...

class SAMLMetadataRequest(_message.Message):
    __slots__ = ("metadata_url",)
    METADATA_URL_FIELD_NUMBER: _ClassVar[int]
    metadata_url: str
    def __init__(self, metadata_url: _Optional[str] = ...) -> None: ...

class GetSAMLMetadataResponse(_message.Message):
    __slots__ = ("idp_entity_id", "idp_sso_url", "idp_slo_url", "idp_certificates", "idp_name_id_format", "request_binding", "want_assertions_signed")
    IDP_ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    IDP_SSO_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_SLO_URL_FIELD_NUMBER: _ClassVar[int]
    IDP_CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    IDP_NAME_ID_FORMAT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BINDING_FIELD_NUMBER: _ClassVar[int]
    WANT_ASSERTIONS_SIGNED_FIELD_NUMBER: _ClassVar[int]
    idp_entity_id: str
    idp_sso_url: str
    idp_slo_url: str
    idp_certificates: _containers.RepeatedScalarFieldContainer[str]
    idp_name_id_format: str
    request_binding: str
    want_assertions_signed: bool
    def __init__(self, idp_entity_id: _Optional[str] = ..., idp_sso_url: _Optional[str] = ..., idp_slo_url: _Optional[str] = ..., idp_certificates: _Optional[_Iterable[str]] = ..., idp_name_id_format: _Optional[str] = ..., request_binding: _Optional[str] = ..., want_assertions_signed: bool = ...) -> None: ...

class GetSAMLCertificateDetailsRequest(_message.Message):
    __slots__ = ("certificate",)
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    certificate: SAMLCertificateRequest
    def __init__(self, certificate: _Optional[_Union[SAMLCertificateRequest, _Mapping]] = ...) -> None: ...

class SAMLCertificateRequest(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class GetSAMLCertificateDetailsResponse(_message.Message):
    __slots__ = ("text", "not_after", "not_before", "subject", "issuer")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    NOT_AFTER_FIELD_NUMBER: _ClassVar[int]
    NOT_BEFORE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    ISSUER_FIELD_NUMBER: _ClassVar[int]
    text: str
    not_after: int
    not_before: int
    subject: str
    issuer: str
    def __init__(self, text: _Optional[str] = ..., not_after: _Optional[int] = ..., not_before: _Optional[int] = ..., subject: _Optional[str] = ..., issuer: _Optional[str] = ...) -> None: ...

class GetConnectionTestResultRequest(_message.Message):
    __slots__ = ("connection_id", "test_request_id")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TEST_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    test_request_id: str
    def __init__(self, connection_id: _Optional[str] = ..., test_request_id: _Optional[str] = ...) -> None: ...

class GetConnectionTestResultResponse(_message.Message):
    __slots__ = ("status", "user_info", "error", "error_description", "error_details")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_INFO_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_DETAILS_FIELD_NUMBER: _ClassVar[int]
    status: TestResultStatus
    user_info: str
    error: str
    error_description: str
    error_details: str
    def __init__(self, status: _Optional[_Union[TestResultStatus, str]] = ..., user_info: _Optional[str] = ..., error: _Optional[str] = ..., error_description: _Optional[str] = ..., error_details: _Optional[str] = ...) -> None: ...

class PasswordConnectionConfig(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Flags(_message.Message):
    __slots__ = ("is_login", "is_app")
    IS_LOGIN_FIELD_NUMBER: _ClassVar[int]
    IS_APP_FIELD_NUMBER: _ClassVar[int]
    is_login: bool
    is_app: bool
    def __init__(self, is_login: bool = ..., is_app: bool = ...) -> None: ...

class ListAppConnectionsRequest(_message.Message):
    __slots__ = ("page_size", "page_token", "provider")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    provider: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., provider: _Optional[str] = ...) -> None: ...

class ListAppConnectionsResponse(_message.Message):
    __slots__ = ("connections", "next_page_token", "prev_page_token", "total_size")
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[ListConnection]
    next_page_token: str
    prev_page_token: str
    total_size: int
    def __init__(self, connections: _Optional[_Iterable[_Union[ListConnection, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

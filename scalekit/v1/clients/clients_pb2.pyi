from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplicationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    APPLICATION_TYPE_UNSPECIFIED: _ClassVar[ApplicationType]
    WEB: _ClassVar[ApplicationType]
    MOBILE: _ClassVar[ApplicationType]
    DESKTOP: _ClassVar[ApplicationType]
    SERVER: _ClassVar[ApplicationType]
    MCP_SERVER: _ClassVar[ApplicationType]

class ClientSecretStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE: _ClassVar[ClientSecretStatus]
    INACTIVE: _ClassVar[ClientSecretStatus]
APPLICATION_TYPE_UNSPECIFIED: ApplicationType
WEB: ApplicationType
MOBILE: ApplicationType
DESKTOP: ApplicationType
SERVER: ApplicationType
MCP_SERVER: ApplicationType
ACTIVE: ClientSecretStatus
INACTIVE: ClientSecretStatus

class CreateApplicationRequest(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: CreateApplication
    def __init__(self, application: _Optional[_Union[CreateApplication, _Mapping]] = ...) -> None: ...

class CreateApplication(_message.Message):
    __slots__ = ("application_type", "third_party", "name", "description", "resource_id", "access_token_expiry", "refresh_token_expiry", "allow_dynamic_client_registration", "logo_uri")
    APPLICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    THIRD_PARTY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ALLOW_DYNAMIC_CLIENT_REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    LOGO_URI_FIELD_NUMBER: _ClassVar[int]
    application_type: ApplicationType
    third_party: bool
    name: str
    description: str
    resource_id: str
    access_token_expiry: int
    refresh_token_expiry: int
    allow_dynamic_client_registration: bool
    logo_uri: str
    def __init__(self, application_type: _Optional[_Union[ApplicationType, str]] = ..., third_party: bool = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., resource_id: _Optional[str] = ..., access_token_expiry: _Optional[int] = ..., refresh_token_expiry: _Optional[int] = ..., allow_dynamic_client_registration: bool = ..., logo_uri: _Optional[str] = ...) -> None: ...

class ApplicationClient(_message.Message):
    __slots__ = ("name", "description", "scopes", "audience", "custom_claims", "expiry", "redirect_uri")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    audience: _containers.RepeatedScalarFieldContainer[str]
    custom_claims: _containers.RepeatedCompositeFieldContainer[CustomClaim]
    expiry: int
    redirect_uri: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ..., audience: _Optional[_Iterable[str]] = ..., custom_claims: _Optional[_Iterable[_Union[CustomClaim, _Mapping]]] = ..., expiry: _Optional[int] = ..., redirect_uri: _Optional[str] = ...) -> None: ...

class CreateApplicationResponse(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: Application
    def __init__(self, application: _Optional[_Union[Application, _Mapping]] = ...) -> None: ...

class GetApplicationRequest(_message.Message):
    __slots__ = ("application_id",)
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    application_id: str
    def __init__(self, application_id: _Optional[str] = ...) -> None: ...

class GetApplicationResponse(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: Application
    def __init__(self, application: _Optional[_Union[Application, _Mapping]] = ...) -> None: ...

class Application(_message.Message):
    __slots__ = ("id", "name", "resource_id", "description", "application_type", "third_party", "allow_dynamic_client_registration", "logo_uri", "access_token_expiry", "refresh_token_expiry", "create_time", "update_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    THIRD_PARTY_FIELD_NUMBER: _ClassVar[int]
    ALLOW_DYNAMIC_CLIENT_REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    LOGO_URI_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    resource_id: str
    description: str
    application_type: ApplicationType
    third_party: bool
    allow_dynamic_client_registration: bool
    logo_uri: str
    access_token_expiry: int
    refresh_token_expiry: int
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., resource_id: _Optional[str] = ..., description: _Optional[str] = ..., application_type: _Optional[_Union[ApplicationType, str]] = ..., third_party: bool = ..., allow_dynamic_client_registration: bool = ..., logo_uri: _Optional[str] = ..., access_token_expiry: _Optional[int] = ..., refresh_token_expiry: _Optional[int] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RegisterClientRequest(_message.Message):
    __slots__ = ("app_id", "client")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    client: RegisterClient
    def __init__(self, app_id: _Optional[str] = ..., client: _Optional[_Union[RegisterClient, _Mapping]] = ...) -> None: ...

class RegisterClient(_message.Message):
    __slots__ = ("client_name", "description", "redirect_uris", "scope", "client_uri", "logo_uri", "tos_uri", "policy_uri")
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_URI_FIELD_NUMBER: _ClassVar[int]
    LOGO_URI_FIELD_NUMBER: _ClassVar[int]
    TOS_URI_FIELD_NUMBER: _ClassVar[int]
    POLICY_URI_FIELD_NUMBER: _ClassVar[int]
    client_name: str
    description: str
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    scope: _containers.RepeatedScalarFieldContainer[str]
    client_uri: str
    logo_uri: str
    tos_uri: str
    policy_uri: str
    def __init__(self, client_name: _Optional[str] = ..., description: _Optional[str] = ..., redirect_uris: _Optional[_Iterable[str]] = ..., scope: _Optional[_Iterable[str]] = ..., client_uri: _Optional[str] = ..., logo_uri: _Optional[str] = ..., tos_uri: _Optional[str] = ..., policy_uri: _Optional[str] = ...) -> None: ...

class RegisterClientResponse(_message.Message):
    __slots__ = ("client_id", "secrets", "name", "description", "create_time", "update_time", "scopes", "audience", "custom_claims", "expiry", "application_id", "redirect_uris")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    secrets: _containers.RepeatedCompositeFieldContainer[ClientSecret]
    name: str
    description: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    scopes: _containers.RepeatedScalarFieldContainer[str]
    audience: _containers.RepeatedScalarFieldContainer[str]
    custom_claims: _containers.RepeatedCompositeFieldContainer[CustomClaim]
    expiry: int
    application_id: str
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, client_id: _Optional[str] = ..., secrets: _Optional[_Iterable[_Union[ClientSecret, _Mapping]]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., scopes: _Optional[_Iterable[str]] = ..., audience: _Optional[_Iterable[str]] = ..., custom_claims: _Optional[_Iterable[_Union[CustomClaim, _Mapping]]] = ..., expiry: _Optional[int] = ..., application_id: _Optional[str] = ..., redirect_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class ListApplicationsRequest(_message.Message):
    __slots__ = ("application_type", "page_token", "page_size")
    APPLICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    application_type: ApplicationType
    page_token: str
    page_size: int
    def __init__(self, application_type: _Optional[_Union[ApplicationType, str]] = ..., page_token: _Optional[str] = ..., page_size: _Optional[int] = ...) -> None: ...

class ListApplicationsResponse(_message.Message):
    __slots__ = ("total_size", "next_page_token", "applications")
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    total_size: int
    next_page_token: str
    applications: _containers.RepeatedCompositeFieldContainer[Application]
    def __init__(self, total_size: _Optional[int] = ..., next_page_token: _Optional[str] = ..., applications: _Optional[_Iterable[_Union[Application, _Mapping]]] = ...) -> None: ...

class UpdateApplicationRequest(_message.Message):
    __slots__ = ("application_id", "application")
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application_id: str
    application: UpdateApplication
    def __init__(self, application_id: _Optional[str] = ..., application: _Optional[_Union[UpdateApplication, _Mapping]] = ...) -> None: ...

class UpdateApplication(_message.Message):
    __slots__ = ("name", "description", "resource_id", "access_token_expiry", "refresh_token_expiry", "allow_dynamic_client_registration", "logo_uri")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ALLOW_DYNAMIC_CLIENT_REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    LOGO_URI_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    resource_id: str
    access_token_expiry: int
    refresh_token_expiry: int
    allow_dynamic_client_registration: bool
    logo_uri: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., resource_id: _Optional[str] = ..., access_token_expiry: _Optional[int] = ..., refresh_token_expiry: _Optional[int] = ..., allow_dynamic_client_registration: bool = ..., logo_uri: _Optional[str] = ...) -> None: ...

class UpdateApplicationResponse(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: Application
    def __init__(self, application: _Optional[_Union[Application, _Mapping]] = ...) -> None: ...

class CreateApplicationClientRequest(_message.Message):
    __slots__ = ("application_id", "client")
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    application_id: str
    client: ApplicationClient
    def __init__(self, application_id: _Optional[str] = ..., client: _Optional[_Union[ApplicationClient, _Mapping]] = ...) -> None: ...

class CreateApplicationClientResponse(_message.Message):
    __slots__ = ("client", "plain_secret")
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    client: M2MClient
    plain_secret: str
    def __init__(self, client: _Optional[_Union[M2MClient, _Mapping]] = ..., plain_secret: _Optional[str] = ...) -> None: ...

class GetApplicationClientRequest(_message.Message):
    __slots__ = ("application_id", "client_id")
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    application_id: str
    client_id: str
    def __init__(self, application_id: _Optional[str] = ..., client_id: _Optional[str] = ...) -> None: ...

class GetApplicationClientResponse(_message.Message):
    __slots__ = ("application", "client")
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    application: Application
    client: M2MClient
    def __init__(self, application: _Optional[_Union[Application, _Mapping]] = ..., client: _Optional[_Union[M2MClient, _Mapping]] = ...) -> None: ...

class CreateOrganizationClientRequest(_message.Message):
    __slots__ = ("organization_id", "client")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    client: OrganizationClient
    def __init__(self, organization_id: _Optional[str] = ..., client: _Optional[_Union[OrganizationClient, _Mapping]] = ...) -> None: ...

class OrganizationClient(_message.Message):
    __slots__ = ("name", "description", "scopes", "audience", "custom_claims", "expiry")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    audience: _containers.RepeatedScalarFieldContainer[str]
    custom_claims: _containers.RepeatedCompositeFieldContainer[CustomClaim]
    expiry: int
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ..., audience: _Optional[_Iterable[str]] = ..., custom_claims: _Optional[_Iterable[_Union[CustomClaim, _Mapping]]] = ..., expiry: _Optional[int] = ...) -> None: ...

class CreateOrganizationClientResponse(_message.Message):
    __slots__ = ("client", "plain_secret")
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    client: M2MClient
    plain_secret: str
    def __init__(self, client: _Optional[_Union[M2MClient, _Mapping]] = ..., plain_secret: _Optional[str] = ...) -> None: ...

class UpdateOrganizationClientRequest(_message.Message):
    __slots__ = ("organization_id", "client_id", "client")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    client_id: str
    client: OrganizationClient
    def __init__(self, organization_id: _Optional[str] = ..., client_id: _Optional[str] = ..., client: _Optional[_Union[OrganizationClient, _Mapping]] = ...) -> None: ...

class UpdateOrganizationClientResponse(_message.Message):
    __slots__ = ("client",)
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    client: M2MClient
    def __init__(self, client: _Optional[_Union[M2MClient, _Mapping]] = ...) -> None: ...

class M2MClient(_message.Message):
    __slots__ = ("client_id", "secrets", "name", "description", "organization_id", "create_time", "update_time", "scopes", "audience", "custom_claims", "expiry", "application_id", "redirect_uris")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    secrets: _containers.RepeatedCompositeFieldContainer[ClientSecret]
    name: str
    description: str
    organization_id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    scopes: _containers.RepeatedScalarFieldContainer[str]
    audience: _containers.RepeatedScalarFieldContainer[str]
    custom_claims: _containers.RepeatedCompositeFieldContainer[CustomClaim]
    expiry: int
    application_id: str
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, client_id: _Optional[str] = ..., secrets: _Optional[_Iterable[_Union[ClientSecret, _Mapping]]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., organization_id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., scopes: _Optional[_Iterable[str]] = ..., audience: _Optional[_Iterable[str]] = ..., custom_claims: _Optional[_Iterable[_Union[CustomClaim, _Mapping]]] = ..., expiry: _Optional[int] = ..., application_id: _Optional[str] = ..., redirect_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class GetOrganizationClientRequest(_message.Message):
    __slots__ = ("organization_id", "client_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    client_id: str
    def __init__(self, organization_id: _Optional[str] = ..., client_id: _Optional[str] = ...) -> None: ...

class CreateOrganizationClientSecretRequest(_message.Message):
    __slots__ = ("organization_id", "client_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    client_id: str
    def __init__(self, organization_id: _Optional[str] = ..., client_id: _Optional[str] = ...) -> None: ...

class CreateOrganizationClientSecretResponse(_message.Message):
    __slots__ = ("plain_secret", "secret")
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    plain_secret: str
    secret: ClientSecret
    def __init__(self, plain_secret: _Optional[str] = ..., secret: _Optional[_Union[ClientSecret, _Mapping]] = ...) -> None: ...

class DeleteOrganizationClientSecretRequest(_message.Message):
    __slots__ = ("organization_id", "client_id", "secret_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    client_id: str
    secret_id: str
    def __init__(self, organization_id: _Optional[str] = ..., client_id: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class GetOrganizationClientResponse(_message.Message):
    __slots__ = ("client",)
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    client: M2MClient
    def __init__(self, client: _Optional[_Union[M2MClient, _Mapping]] = ...) -> None: ...

class CustomClaim(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class DeleteOrganizationClientRequest(_message.Message):
    __slots__ = ("organization_id", "client_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    client_id: str
    def __init__(self, organization_id: _Optional[str] = ..., client_id: _Optional[str] = ...) -> None: ...

class GetClientRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class GetClientResponse(_message.Message):
    __slots__ = ("client",)
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    client: Client
    def __init__(self, client: _Optional[_Union[Client, _Mapping]] = ...) -> None: ...

class ListClientsRequest(_message.Message):
    __slots__ = ("include_plain_secret",)
    INCLUDE_PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    include_plain_secret: bool
    def __init__(self, include_plain_secret: bool = ...) -> None: ...

class ListClientsResponse(_message.Message):
    __slots__ = ("total_size", "clients")
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    total_size: int
    clients: _containers.RepeatedCompositeFieldContainer[Client]
    def __init__(self, total_size: _Optional[int] = ..., clients: _Optional[_Iterable[_Union[Client, _Mapping]]] = ...) -> None: ...

class UpdateClientRequest(_message.Message):
    __slots__ = ("client_id", "client", "mask")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client: UpdateClient
    mask: _field_mask_pb2.FieldMask
    def __init__(self, client_id: _Optional[str] = ..., client: _Optional[_Union[UpdateClient, _Mapping]] = ..., mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateClient(_message.Message):
    __slots__ = ("redirect_uris", "default_redirect_uri", "back_channel_logout_uris", "post_logout_redirect_uris", "initiate_login_uri", "post_login_uris")
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    BACK_CHANNEL_LOGOUT_URIS_FIELD_NUMBER: _ClassVar[int]
    POST_LOGOUT_REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    INITIATE_LOGIN_URI_FIELD_NUMBER: _ClassVar[int]
    POST_LOGIN_URIS_FIELD_NUMBER: _ClassVar[int]
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    default_redirect_uri: str
    back_channel_logout_uris: _containers.RepeatedScalarFieldContainer[str]
    post_logout_redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    initiate_login_uri: str
    post_login_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, redirect_uris: _Optional[_Iterable[str]] = ..., default_redirect_uri: _Optional[str] = ..., back_channel_logout_uris: _Optional[_Iterable[str]] = ..., post_logout_redirect_uris: _Optional[_Iterable[str]] = ..., initiate_login_uri: _Optional[str] = ..., post_login_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateClientResponse(_message.Message):
    __slots__ = ("client",)
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    client: Client
    def __init__(self, client: _Optional[_Union[Client, _Mapping]] = ...) -> None: ...

class CreateClientSecretRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class CreateClientSecretResponse(_message.Message):
    __slots__ = ("plain_secret", "secret")
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    plain_secret: str
    secret: ClientSecret
    def __init__(self, plain_secret: _Optional[str] = ..., secret: _Optional[_Union[ClientSecret, _Mapping]] = ...) -> None: ...

class UpdateClientSecretRequest(_message.Message):
    __slots__ = ("client_id", "secret_id", "secret", "mask")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    secret_id: str
    secret: UpdateClientSecret
    mask: _field_mask_pb2.FieldMask
    def __init__(self, client_id: _Optional[str] = ..., secret_id: _Optional[str] = ..., secret: _Optional[_Union[UpdateClientSecret, _Mapping]] = ..., mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateClientSecret(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ClientSecretStatus
    def __init__(self, status: _Optional[_Union[ClientSecretStatus, str]] = ...) -> None: ...

class UpdateClientSecretResponse(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: ClientSecret
    def __init__(self, secret: _Optional[_Union[ClientSecret, _Mapping]] = ...) -> None: ...

class DeleteClientSecretRequest(_message.Message):
    __slots__ = ("client_id", "secret_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    secret_id: str
    def __init__(self, client_id: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class Client(_message.Message):
    __slots__ = ("id", "keyId", "create_time", "update_time", "redirect_uris", "default_redirect_uri", "secrets", "post_logout_redirect_uris", "back_channel_logout_uris", "initiate_login_uri", "post_login_uris")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEYID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    POST_LOGOUT_REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    BACK_CHANNEL_LOGOUT_URIS_FIELD_NUMBER: _ClassVar[int]
    INITIATE_LOGIN_URI_FIELD_NUMBER: _ClassVar[int]
    POST_LOGIN_URIS_FIELD_NUMBER: _ClassVar[int]
    id: str
    keyId: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    default_redirect_uri: str
    secrets: _containers.RepeatedCompositeFieldContainer[ClientSecret]
    post_logout_redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    back_channel_logout_uris: _containers.RepeatedScalarFieldContainer[str]
    initiate_login_uri: str
    post_login_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., keyId: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., redirect_uris: _Optional[_Iterable[str]] = ..., default_redirect_uri: _Optional[str] = ..., secrets: _Optional[_Iterable[_Union[ClientSecret, _Mapping]]] = ..., post_logout_redirect_uris: _Optional[_Iterable[str]] = ..., back_channel_logout_uris: _Optional[_Iterable[str]] = ..., initiate_login_uri: _Optional[str] = ..., post_login_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class ClientSecret(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "secret_suffix", "created_by", "status", "expire_time", "last_used_time", "plain_secret")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    SECRET_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_TIME_FIELD_NUMBER: _ClassVar[int]
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    secret_suffix: str
    created_by: str
    status: ClientSecretStatus
    expire_time: _timestamp_pb2.Timestamp
    last_used_time: _timestamp_pb2.Timestamp
    plain_secret: str
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., secret_suffix: _Optional[str] = ..., created_by: _Optional[str] = ..., status: _Optional[_Union[ClientSecretStatus, str]] = ..., expire_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_used_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., plain_secret: _Optional[str] = ...) -> None: ...

class Scope(_message.Message):
    __slots__ = ("name", "description", "enabled")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    enabled: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class CreateScope(_message.Message):
    __slots__ = ("name", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateScopeRequest(_message.Message):
    __slots__ = ("env_id", "scope")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    scope: CreateScope
    def __init__(self, env_id: _Optional[str] = ..., scope: _Optional[_Union[CreateScope, _Mapping]] = ...) -> None: ...

class CreateScopeResponse(_message.Message):
    __slots__ = ("scope",)
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    scope: Scope
    def __init__(self, scope: _Optional[_Union[Scope, _Mapping]] = ...) -> None: ...

class ListScopesRequest(_message.Message):
    __slots__ = ("env_id",)
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    def __init__(self, env_id: _Optional[str] = ...) -> None: ...

class ListScopesResponse(_message.Message):
    __slots__ = ("scopes",)
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    scopes: _containers.RepeatedCompositeFieldContainer[Scope]
    def __init__(self, scopes: _Optional[_Iterable[_Union[Scope, _Mapping]]] = ...) -> None: ...

class GetConsentDetailsResponse(_message.Message):
    __slots__ = ("application", "user", "client", "scopes")
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    application: Application
    user: User
    client: ConsentClient
    scopes: _containers.RepeatedCompositeFieldContainer[ConsentScope]
    def __init__(self, application: _Optional[_Union[Application, _Mapping]] = ..., user: _Optional[_Union[User, _Mapping]] = ..., client: _Optional[_Union[ConsentClient, _Mapping]] = ..., scopes: _Optional[_Iterable[_Union[ConsentScope, _Mapping]]] = ...) -> None: ...

class ConsentClient(_message.Message):
    __slots__ = ("name", "privacy_uri", "tos_uri")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_URI_FIELD_NUMBER: _ClassVar[int]
    TOS_URI_FIELD_NUMBER: _ClassVar[int]
    name: str
    privacy_uri: str
    tos_uri: str
    def __init__(self, name: _Optional[str] = ..., privacy_uri: _Optional[str] = ..., tos_uri: _Optional[str] = ...) -> None: ...

class ConsentScope(_message.Message):
    __slots__ = ("name", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

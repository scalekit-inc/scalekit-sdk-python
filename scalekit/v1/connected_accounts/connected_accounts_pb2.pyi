from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectorStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTION_STATUS_UNSPECIFIED: _ClassVar[ConnectorStatus]
    ACTIVE: _ClassVar[ConnectorStatus]
    EXPIRED: _ClassVar[ConnectorStatus]
    PENDING_AUTH: _ClassVar[ConnectorStatus]

class ConnectorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTION_TYPE_UNSPECIFIED: _ClassVar[ConnectorType]
    OAUTH: _ClassVar[ConnectorType]
    API_KEY: _ClassVar[ConnectorType]
    BASIC_AUTH: _ClassVar[ConnectorType]
    BEARER_TOKEN: _ClassVar[ConnectorType]
    CUSTOM: _ClassVar[ConnectorType]
    BASIC: _ClassVar[ConnectorType]
CONNECTION_STATUS_UNSPECIFIED: ConnectorStatus
ACTIVE: ConnectorStatus
EXPIRED: ConnectorStatus
PENDING_AUTH: ConnectorStatus
CONNECTION_TYPE_UNSPECIFIED: ConnectorType
OAUTH: ConnectorType
API_KEY: ConnectorType
BASIC_AUTH: ConnectorType
BEARER_TOKEN: ConnectorType
CUSTOM: ConnectorType
BASIC: ConnectorType

class ListConnectedAccountsRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "connector", "identifier", "provider", "page_size", "page_token", "query")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    connector: str
    identifier: str
    provider: str
    page_size: int
    page_token: str
    query: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., connector: _Optional[str] = ..., identifier: _Optional[str] = ..., provider: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., query: _Optional[str] = ...) -> None: ...

class ListConnectedAccountsResponse(_message.Message):
    __slots__ = ("connected_accounts", "total_size", "next_page_token", "prev_page_token")
    CONNECTED_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    connected_accounts: _containers.RepeatedCompositeFieldContainer[ConnectedAccountForList]
    total_size: int
    next_page_token: str
    prev_page_token: str
    def __init__(self, connected_accounts: _Optional[_Iterable[_Union[ConnectedAccountForList, _Mapping]]] = ..., total_size: _Optional[int] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class SearchConnectedAccountsRequest(_message.Message):
    __slots__ = ("query", "page_size", "page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_size: int
    page_token: str
    def __init__(self, query: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class SearchConnectedAccountsResponse(_message.Message):
    __slots__ = ("connected_accounts", "total_size", "next_page_token", "prev_page_token")
    CONNECTED_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    connected_accounts: _containers.RepeatedCompositeFieldContainer[ConnectedAccountForList]
    total_size: int
    next_page_token: str
    prev_page_token: str
    def __init__(self, connected_accounts: _Optional[_Iterable[_Union[ConnectedAccountForList, _Mapping]]] = ..., total_size: _Optional[int] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class CreateConnectedAccountRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "connector", "identifier", "connected_account")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    connector: str
    identifier: str
    connected_account: CreateConnectedAccount
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., connector: _Optional[str] = ..., identifier: _Optional[str] = ..., connected_account: _Optional[_Union[CreateConnectedAccount, _Mapping]] = ...) -> None: ...

class CreateConnectedAccountResponse(_message.Message):
    __slots__ = ("connected_account",)
    CONNECTED_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    connected_account: ConnectedAccount
    def __init__(self, connected_account: _Optional[_Union[ConnectedAccount, _Mapping]] = ...) -> None: ...

class UpdateConnectedAccountRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "connector", "identifier", "id", "connected_account")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    connector: str
    identifier: str
    id: str
    connected_account: UpdateConnectedAccount
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., connector: _Optional[str] = ..., identifier: _Optional[str] = ..., id: _Optional[str] = ..., connected_account: _Optional[_Union[UpdateConnectedAccount, _Mapping]] = ...) -> None: ...

class UpdateConnectedAccountResponse(_message.Message):
    __slots__ = ("connected_account",)
    CONNECTED_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    connected_account: ConnectedAccount
    def __init__(self, connected_account: _Optional[_Union[ConnectedAccount, _Mapping]] = ...) -> None: ...

class DeleteConnectedAccountRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "connector", "identifier", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    connector: str
    identifier: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., connector: _Optional[str] = ..., identifier: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class DeleteConnectedAccountResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMagicLinkForConnectedAccountRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "connector", "identifier", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    connector: str
    identifier: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., connector: _Optional[str] = ..., identifier: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetMagicLinkForConnectedAccountRedirectRequest(_message.Message):
    __slots__ = ("redirect_to",)
    REDIRECT_TO_FIELD_NUMBER: _ClassVar[int]
    redirect_to: str
    def __init__(self, redirect_to: _Optional[str] = ...) -> None: ...

class GetMagicLinkForConnectedAccountResponse(_message.Message):
    __slots__ = ("link", "expiry")
    LINK_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    link: str
    expiry: _timestamp_pb2.Timestamp
    def __init__(self, link: _Optional[str] = ..., expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetMagicLinkForConnectedAccountRedirectResponse(_message.Message):
    __slots__ = ("redirect_to", "expiry")
    REDIRECT_TO_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    redirect_to: str
    expiry: _timestamp_pb2.Timestamp
    def __init__(self, redirect_to: _Optional[str] = ..., expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetConnectedAccountByIdentifierRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "connector", "identifier", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    connector: str
    identifier: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., connector: _Optional[str] = ..., identifier: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetConnectedAccountByIdentifierResponse(_message.Message):
    __slots__ = ("connected_account",)
    CONNECTED_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    connected_account: ConnectedAccount
    def __init__(self, connected_account: _Optional[_Union[ConnectedAccount, _Mapping]] = ...) -> None: ...

class ConnectedAccount(_message.Message):
    __slots__ = ("identifier", "provider", "status", "authorization_type", "authorization_details", "token_expires_at", "updated_at", "connector", "last_used_at", "id", "connection_id")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    provider: str
    status: ConnectorStatus
    authorization_type: ConnectorType
    authorization_details: AuthorizationDetails
    token_expires_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    connector: str
    last_used_at: _timestamp_pb2.Timestamp
    id: str
    connection_id: str
    def __init__(self, identifier: _Optional[str] = ..., provider: _Optional[str] = ..., status: _Optional[_Union[ConnectorStatus, str]] = ..., authorization_type: _Optional[_Union[ConnectorType, str]] = ..., authorization_details: _Optional[_Union[AuthorizationDetails, _Mapping]] = ..., token_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., connector: _Optional[str] = ..., last_used_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., connection_id: _Optional[str] = ...) -> None: ...

class CreateConnectedAccount(_message.Message):
    __slots__ = ("authorization_details",)
    AUTHORIZATION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    authorization_details: AuthorizationDetails
    def __init__(self, authorization_details: _Optional[_Union[AuthorizationDetails, _Mapping]] = ...) -> None: ...

class UpdateConnectedAccount(_message.Message):
    __slots__ = ("authorization_details",)
    AUTHORIZATION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    authorization_details: AuthorizationDetails
    def __init__(self, authorization_details: _Optional[_Union[AuthorizationDetails, _Mapping]] = ...) -> None: ...

class ConnectedAccountForList(_message.Message):
    __slots__ = ("identifier", "provider", "status", "authorization_type", "token_expires_at", "updated_at", "connector", "last_used_at", "id", "connection_id")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    provider: str
    status: ConnectorStatus
    authorization_type: ConnectorType
    token_expires_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    connector: str
    last_used_at: _timestamp_pb2.Timestamp
    id: str
    connection_id: str
    def __init__(self, identifier: _Optional[str] = ..., provider: _Optional[str] = ..., status: _Optional[_Union[ConnectorStatus, str]] = ..., authorization_type: _Optional[_Union[ConnectorType, str]] = ..., token_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., connector: _Optional[str] = ..., last_used_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., connection_id: _Optional[str] = ...) -> None: ...

class AuthorizationDetails(_message.Message):
    __slots__ = ("oauth_token", "static_auth")
    OAUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    STATIC_AUTH_FIELD_NUMBER: _ClassVar[int]
    oauth_token: OauthToken
    static_auth: StaticAuth
    def __init__(self, oauth_token: _Optional[_Union[OauthToken, _Mapping]] = ..., static_auth: _Optional[_Union[StaticAuth, _Mapping]] = ...) -> None: ...

class OauthToken(_message.Message):
    __slots__ = ("access_token", "refresh_token", "scopes")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    refresh_token: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ...) -> None: ...

class StaticAuth(_message.Message):
    __slots__ = ("details",)
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: _struct_pb2.Struct
    def __init__(self, details: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

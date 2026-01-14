from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: CreateToken
    def __init__(self, token: _Optional[_Union[CreateToken, _Mapping]] = ...) -> None: ...

class CreateToken(_message.Message):
    __slots__ = ("organization_id", "user_id", "custom_claims", "expiry", "description")
    class CustomClaimsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    custom_claims: _containers.ScalarMap[str, str]
    expiry: _timestamp_pb2.Timestamp
    description: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., custom_claims: _Optional[_Mapping[str, str]] = ..., expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class CreateTokenResponse(_message.Message):
    __slots__ = ("token", "token_id", "token_info")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_INFO_FIELD_NUMBER: _ClassVar[int]
    token: str
    token_id: str
    token_info: Token
    def __init__(self, token: _Optional[str] = ..., token_id: _Optional[str] = ..., token_info: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

class ValidateTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ValidateTokenResponse(_message.Message):
    __slots__ = ("token_info",)
    TOKEN_INFO_FIELD_NUMBER: _ClassVar[int]
    token_info: Token
    def __init__(self, token_info: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

class InvalidateTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ListTokensRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "page_size", "page_token")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    page_size: int
    page_token: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListTokensResponse(_message.Message):
    __slots__ = ("tokens", "total_count", "next_page_token", "prev_page_token")
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    total_count: int
    next_page_token: str
    prev_page_token: str
    def __init__(self, tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., total_count: _Optional[int] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class UpdateTokenRequest(_message.Message):
    __slots__ = ("token", "custom_claims", "description")
    class CustomClaimsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    token: str
    custom_claims: _containers.ScalarMap[str, str]
    description: str
    def __init__(self, token: _Optional[str] = ..., custom_claims: _Optional[_Mapping[str, str]] = ..., description: _Optional[str] = ...) -> None: ...

class UpdateTokenResponse(_message.Message):
    __slots__ = ("token_info",)
    TOKEN_INFO_FIELD_NUMBER: _ClassVar[int]
    token_info: Token
    def __init__(self, token_info: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ("token_id", "organization_id", "organization_external_id", "user_id", "user_external_id", "custom_claims", "expiry", "created_at", "description", "token_suffix", "email", "roles")
    class CustomClaimsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CLAIMS_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TOKEN_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    token_id: str
    organization_id: str
    organization_external_id: str
    user_id: str
    user_external_id: str
    custom_claims: _containers.ScalarMap[str, str]
    expiry: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    description: str
    token_suffix: str
    email: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, token_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., organization_external_id: _Optional[str] = ..., user_id: _Optional[str] = ..., user_external_id: _Optional[str] = ..., custom_claims: _Optional[_Mapping[str, str]] = ..., expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., token_suffix: _Optional[str] = ..., email: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ("user_id", "email", "name", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email: str
    name: str
    attributes: _containers.ScalarMap[str, str]
    def __init__(self, user_id: _Optional[str] = ..., email: _Optional[str] = ..., name: _Optional[str] = ..., attributes: _Optional[_Mapping[str, str]] = ...) -> None: ...

class FetchTokenRequest(_message.Message):
    __slots__ = ("token_id",)
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    token_id: str
    def __init__(self, token_id: _Optional[str] = ...) -> None: ...

class FetchTokenResponse(_message.Message):
    __slots__ = ("token", "retrieved_at", "token_info")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    RETRIEVED_AT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_INFO_FIELD_NUMBER: _ClassVar[int]
    token: str
    retrieved_at: _timestamp_pb2.Timestamp
    token_info: Token
    def __init__(self, token: _Optional[str] = ..., retrieved_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., token_info: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

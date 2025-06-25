from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TemplateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[TemplateType]
    SIGNIN: _ClassVar[TemplateType]
    SIGNUP: _ClassVar[TemplateType]

class PasswordlessType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PASSWORDLESS_TYPE_UNSPECIFIED: _ClassVar[PasswordlessType]
    OTP: _ClassVar[PasswordlessType]
    LINK: _ClassVar[PasswordlessType]
    LINK_OTP: _ClassVar[PasswordlessType]
UNSPECIFIED: TemplateType
SIGNIN: TemplateType
SIGNUP: TemplateType
PASSWORDLESS_TYPE_UNSPECIFIED: PasswordlessType
OTP: PasswordlessType
LINK: PasswordlessType
LINK_OTP: PasswordlessType

class SendPasswordlessRequest(_message.Message):
    __slots__ = ("email", "template", "magiclink_auth_uri", "state", "expires_in", "template_variables")
    class TemplateVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    MAGICLINK_AUTH_URI_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    email: str
    template: TemplateType
    magiclink_auth_uri: str
    state: str
    expires_in: int
    template_variables: _containers.ScalarMap[str, str]
    def __init__(self, email: _Optional[str] = ..., template: _Optional[_Union[TemplateType, str]] = ..., magiclink_auth_uri: _Optional[str] = ..., state: _Optional[str] = ..., expires_in: _Optional[int] = ..., template_variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SendPasswordlessResponse(_message.Message):
    __slots__ = ("auth_request_id", "expires_at", "expires_in", "passwordless_type")
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    PASSWORDLESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    auth_request_id: str
    expires_at: int
    expires_in: int
    passwordless_type: PasswordlessType
    def __init__(self, auth_request_id: _Optional[str] = ..., expires_at: _Optional[int] = ..., expires_in: _Optional[int] = ..., passwordless_type: _Optional[_Union[PasswordlessType, str]] = ...) -> None: ...

class VerifyPasswordLessRequest(_message.Message):
    __slots__ = ("code", "link_token", "auth_request_id")
    CODE_FIELD_NUMBER: _ClassVar[int]
    LINK_TOKEN_FIELD_NUMBER: _ClassVar[int]
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    code: str
    link_token: str
    auth_request_id: str
    def __init__(self, code: _Optional[str] = ..., link_token: _Optional[str] = ..., auth_request_id: _Optional[str] = ...) -> None: ...

class ResendPasswordlessRequest(_message.Message):
    __slots__ = ("auth_request_id",)
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    auth_request_id: str
    def __init__(self, auth_request_id: _Optional[str] = ...) -> None: ...

class VerifyPasswordLessResponse(_message.Message):
    __slots__ = ("email", "state", "template", "passwordless_type")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    PASSWORDLESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    email: str
    state: str
    template: TemplateType
    passwordless_type: PasswordlessType
    def __init__(self, email: _Optional[str] = ..., state: _Optional[str] = ..., template: _Optional[_Union[TemplateType, str]] = ..., passwordless_type: _Optional[_Union[PasswordlessType, str]] = ...) -> None: ...

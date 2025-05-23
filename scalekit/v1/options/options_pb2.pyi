from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthenticationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BLOCKED: _ClassVar[AuthenticationType]
    NONE: _ClassVar[AuthenticationType]
    WORKSPACE: _ClassVar[AuthenticationType]
    CUSTOMER_PORTAL: _ClassVar[AuthenticationType]
    SESSION: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CUSTOMER_PORTAL: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CUSTOMER_PORTAL_CLIENT: _ClassVar[AuthenticationType]
    USER: _ClassVar[AuthenticationType]
    CLIENT: _ClassVar[AuthenticationType]
    SESSION_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CLIENT: _ClassVar[AuthenticationType]
    CUSTOMER_PORTAL_SESSION_CLIENT: _ClassVar[AuthenticationType]
BLOCKED: AuthenticationType
NONE: AuthenticationType
WORKSPACE: AuthenticationType
CUSTOMER_PORTAL: AuthenticationType
SESSION: AuthenticationType
WORKSPACE_SESSION: AuthenticationType
WORKSPACE_SESSION_CUSTOMER_PORTAL: AuthenticationType
WORKSPACE_SESSION_CUSTOMER_PORTAL_CLIENT: AuthenticationType
USER: AuthenticationType
CLIENT: AuthenticationType
SESSION_CLIENT: AuthenticationType
WORKSPACE_SESSION_CLIENT: AuthenticationType
CUSTOMER_PORTAL_SESSION_CLIENT: AuthenticationType
AUTH_OPTION_FIELD_NUMBER: _ClassVar[int]
auth_option: _descriptor.FieldDescriptor

class AuthOption(_message.Message):
    __slots__ = ("authentication_type", "permission")
    AUTHENTICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    authentication_type: AuthenticationType
    permission: str
    def __init__(self, authentication_type: _Optional[_Union[AuthenticationType, str]] = ..., permission: _Optional[str] = ...) -> None: ...

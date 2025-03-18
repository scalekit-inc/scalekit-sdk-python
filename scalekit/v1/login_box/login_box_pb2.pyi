from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.connections import connections_pb2 as _connections_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLoginMethodRequest(_message.Message):
    __slots__ = ("auth_request_id",)
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    auth_request_id: str
    def __init__(self, auth_request_id: _Optional[str] = ...) -> None: ...

class GetLoginMethodResponse(_message.Message):
    __slots__ = ("connections",)
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[LoginConnections]
    def __init__(self, connections: _Optional[_Iterable[_Union[LoginConnections, _Mapping]]] = ...) -> None: ...

class LoginConnections(_message.Message):
    __slots__ = ("connection_id", "connection_type", "connection_provider")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connection_type: _connections_pb2.ConnectionType
    connection_provider: _connections_pb2.ConnectionProvider
    def __init__(self, connection_id: _Optional[str] = ..., connection_type: _Optional[_Union[_connections_pb2.ConnectionType, str]] = ..., connection_provider: _Optional[_Union[_connections_pb2.ConnectionProvider, str]] = ...) -> None: ...

class SetLoginMethodRequest(_message.Message):
    __slots__ = ("auth_request_id", "data")
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    auth_request_id: str
    data: LoginMethodUserRequest
    def __init__(self, auth_request_id: _Optional[str] = ..., data: _Optional[_Union[LoginMethodUserRequest, _Mapping]] = ...) -> None: ...

class LoginMethodUserRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class SetLoginMethodResponse(_message.Message):
    __slots__ = ("id", "type", "magic_link_enabled", "magic_otp_enabled")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MAGIC_LINK_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MAGIC_OTP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: _connections_pb2.ConnectionType
    magic_link_enabled: bool
    magic_otp_enabled: bool
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[_connections_pb2.ConnectionType, str]] = ..., magic_link_enabled: bool = ..., magic_otp_enabled: bool = ...) -> None: ...

class GetBoxCustomizationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBoxCustomizationResponse(_message.Message):
    __slots__ = ("customization_settings",)
    CUSTOMIZATION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    customization_settings: _struct_pb2.Struct
    def __init__(self, customization_settings: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class VerifyPasswordLessRequest(_message.Message):
    __slots__ = ("auth_request_id", "code")
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    auth_request_id: str
    code: str
    def __init__(self, auth_request_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class VerifyPasswordLessResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

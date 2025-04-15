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

class ListAuthMethodsResponse(_message.Message):
    __slots__ = ("auth_methods",)
    AUTH_METHODS_FIELD_NUMBER: _ClassVar[int]
    auth_methods: _containers.RepeatedCompositeFieldContainer[AuthMethod]
    def __init__(self, auth_methods: _Optional[_Iterable[_Union[AuthMethod, _Mapping]]] = ...) -> None: ...

class AuthMethod(_message.Message):
    __slots__ = ("connection_id", "connection_type", "provider", "auth_initiation_uri", "passwordless_type", "code_challenge_length")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    AUTH_INITIATION_URI_FIELD_NUMBER: _ClassVar[int]
    PASSWORDLESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CODE_CHALLENGE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connection_type: _connections_pb2.ConnectionType
    provider: _connections_pb2.ConnectionProvider
    auth_initiation_uri: str
    passwordless_type: _connections_pb2.PasswordlessType
    code_challenge_length: int
    def __init__(self, connection_id: _Optional[str] = ..., connection_type: _Optional[_Union[_connections_pb2.ConnectionType, str]] = ..., provider: _Optional[_Union[_connections_pb2.ConnectionProvider, str]] = ..., auth_initiation_uri: _Optional[str] = ..., passwordless_type: _Optional[_Union[_connections_pb2.PasswordlessType, str]] = ..., code_challenge_length: _Optional[int] = ...) -> None: ...

class DiscoveryAuthMethodRequest(_message.Message):
    __slots__ = ("discovery_request",)
    DISCOVERY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    discovery_request: DiscoveryRequest
    def __init__(self, discovery_request: _Optional[_Union[DiscoveryRequest, _Mapping]] = ...) -> None: ...

class DiscoveryRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class DiscoveryAuthMethodResponse(_message.Message):
    __slots__ = ("auth_method",)
    AUTH_METHOD_FIELD_NUMBER: _ClassVar[int]
    auth_method: AuthMethod
    def __init__(self, auth_method: _Optional[_Union[AuthMethod, _Mapping]] = ...) -> None: ...

class GetAuthCustomizationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuthCustomizationsResponse(_message.Message):
    __slots__ = ("customizations",)
    CUSTOMIZATIONS_FIELD_NUMBER: _ClassVar[int]
    customizations: _struct_pb2.Struct
    def __init__(self, customizations: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class VerifyPasswordLessRequest(_message.Message):
    __slots__ = ("otp_req",)
    OTP_REQ_FIELD_NUMBER: _ClassVar[int]
    otp_req: OTPRequest
    def __init__(self, otp_req: _Optional[_Union[OTPRequest, _Mapping]] = ...) -> None: ...

class OTPRequest(_message.Message):
    __slots__ = ("code_challenge",)
    CODE_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    code_challenge: str
    def __init__(self, code_challenge: _Optional[str] = ...) -> None: ...

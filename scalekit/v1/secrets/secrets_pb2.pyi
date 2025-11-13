from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SecretType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SECRET_TYPE_UNSPECIFIED: _ClassVar[SecretType]
    INTERCEPTOR_HMAC: _ClassVar[SecretType]
    DIRECTORY_TOKEN: _ClassVar[SecretType]

class TenantType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TENANT_TYPE_UNSPECIFIED: _ClassVar[TenantType]
    INTERCEPTOR: _ClassVar[TenantType]
    DIRECTORY: _ClassVar[TenantType]
SECRET_TYPE_UNSPECIFIED: SecretType
INTERCEPTOR_HMAC: SecretType
DIRECTORY_TOKEN: SecretType
TENANT_TYPE_UNSPECIFIED: TenantType
INTERCEPTOR: TenantType
DIRECTORY: TenantType

class CreateSecretRequest(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: CreateSecret
    def __init__(self, secret: _Optional[_Union[CreateSecret, _Mapping]] = ...) -> None: ...

class CreateSecret(_message.Message):
    __slots__ = ("secret_type", "tenant_type")
    SECRET_TYPE_FIELD_NUMBER: _ClassVar[int]
    TENANT_TYPE_FIELD_NUMBER: _ClassVar[int]
    secret_type: SecretType
    tenant_type: TenantType
    def __init__(self, secret_type: _Optional[_Union[SecretType, str]] = ..., tenant_type: _Optional[_Union[TenantType, str]] = ...) -> None: ...

class CreateSecretResponse(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: Secret
    def __init__(self, secret: _Optional[_Union[Secret, _Mapping]] = ...) -> None: ...

class RotateSecretRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RotateSecretResponse(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: Secret
    def __init__(self, secret: _Optional[_Union[Secret, _Mapping]] = ...) -> None: ...

class GetSecretRequest(_message.Message):
    __slots__ = ("id", "include_plaintext_secret")
    ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PLAINTEXT_SECRET_FIELD_NUMBER: _ClassVar[int]
    id: str
    include_plaintext_secret: bool
    def __init__(self, id: _Optional[str] = ..., include_plaintext_secret: bool = ...) -> None: ...

class GetSecretResponse(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: Secret
    def __init__(self, secret: _Optional[_Union[Secret, _Mapping]] = ...) -> None: ...

class ListSecretsRequest(_message.Message):
    __slots__ = ("secret_type",)
    SECRET_TYPE_FIELD_NUMBER: _ClassVar[int]
    secret_type: SecretType
    def __init__(self, secret_type: _Optional[_Union[SecretType, str]] = ...) -> None: ...

class DeleteSecretRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ListSecretsResponse(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: _containers.RepeatedCompositeFieldContainer[Secret]
    def __init__(self, secret: _Optional[_Iterable[_Union[Secret, _Mapping]]] = ...) -> None: ...

class Secret(_message.Message):
    __slots__ = ("id", "tenant_type", "secret_type", "secret_suffix", "plaintext_secret", "created_at", "last_used_at", "expires_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TENANT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SECRET_TYPE_FIELD_NUMBER: _ClassVar[int]
    SECRET_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    PLAINTEXT_SECRET_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    tenant_type: TenantType
    secret_type: SecretType
    secret_suffix: str
    plaintext_secret: str
    created_at: _timestamp_pb2.Timestamp
    last_used_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., tenant_type: _Optional[_Union[TenantType, str]] = ..., secret_type: _Optional[_Union[SecretType, str]] = ..., secret_suffix: _Optional[str] = ..., plaintext_secret: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_used_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

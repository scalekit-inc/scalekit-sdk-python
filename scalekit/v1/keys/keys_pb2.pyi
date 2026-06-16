from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DEKKeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEK_KEY_TYPE_UNSPECIFIED: _ClassVar[DEKKeyType]
    ENVIRONMENT_KEY: _ClassVar[DEKKeyType]
    BYOK: _ClassVar[DEKKeyType]
    SCALEKIT_MANAGED_KEY: _ClassVar[DEKKeyType]
DEK_KEY_TYPE_UNSPECIFIED: DEKKeyType
ENVIRONMENT_KEY: DEKKeyType
BYOK: DEKKeyType
SCALEKIT_MANAGED_KEY: DEKKeyType

class CreateDEKRequest(_message.Message):
    __slots__ = ("key_type", "provider", "key_ref")
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    KEY_REF_FIELD_NUMBER: _ClassVar[int]
    key_type: DEKKeyType
    provider: str
    key_ref: str
    def __init__(self, key_type: _Optional[_Union[DEKKeyType, str]] = ..., provider: _Optional[str] = ..., key_ref: _Optional[str] = ...) -> None: ...

class CreateDEKResponse(_message.Message):
    __slots__ = ("dek",)
    DEK_FIELD_NUMBER: _ClassVar[int]
    dek: EnvironmentKey
    def __init__(self, dek: _Optional[_Union[EnvironmentKey, _Mapping]] = ...) -> None: ...

class RotateDEKRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RotateDEKResponse(_message.Message):
    __slots__ = ("dek",)
    DEK_FIELD_NUMBER: _ClassVar[int]
    dek: EnvironmentKey
    def __init__(self, dek: _Optional[_Union[EnvironmentKey, _Mapping]] = ...) -> None: ...

class ListDEKsRequest(_message.Message):
    __slots__ = ("status", "page_size", "page_token")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    status: str
    page_size: int
    page_token: str
    def __init__(self, status: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListDEKsResponse(_message.Message):
    __slots__ = ("deks", "next_page_token", "total_size")
    DEKS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    deks: _containers.RepeatedCompositeFieldContainer[EnvironmentKey]
    next_page_token: str
    total_size: int
    def __init__(self, deks: _Optional[_Iterable[_Union[EnvironmentKey, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class DeleteDEKRequest(_message.Message):
    __slots__ = ("dek_version",)
    DEK_VERSION_FIELD_NUMBER: _ClassVar[int]
    dek_version: int
    def __init__(self, dek_version: _Optional[int] = ...) -> None: ...

class RotateMasterKeyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RotateMasterKeyResponse(_message.Message):
    __slots__ = ("new_master_key",)
    NEW_MASTER_KEY_FIELD_NUMBER: _ClassVar[int]
    new_master_key: MasterKey
    def __init__(self, new_master_key: _Optional[_Union[MasterKey, _Mapping]] = ...) -> None: ...

class EnvironmentKey(_message.Message):
    __slots__ = ("id", "environment_id", "dek_version", "master_version", "algorithm", "status", "created_at", "rotated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEK_VERSION_FIELD_NUMBER: _ClassVar[int]
    MASTER_VERSION_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ROTATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    dek_version: int
    master_version: int
    algorithm: str
    status: str
    created_at: _timestamp_pb2.Timestamp
    rotated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., dek_version: _Optional[int] = ..., master_version: _Optional[int] = ..., algorithm: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rotated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MasterKey(_message.Message):
    __slots__ = ("id", "provider", "key_ref", "version", "status", "created_at", "rotated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    KEY_REF_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ROTATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    provider: str
    key_ref: str
    version: int
    status: str
    created_at: _timestamp_pb2.Timestamp
    rotated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., provider: _Optional[str] = ..., key_ref: _Optional[str] = ..., version: _Optional[int] = ..., status: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rotated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateMasterKeyRequest(_message.Message):
    __slots__ = ("provider", "key_ref", "version")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    KEY_REF_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    provider: str
    key_ref: str
    version: int
    def __init__(self, provider: _Optional[str] = ..., key_ref: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class CreateMasterKeyResponse(_message.Message):
    __slots__ = ("master_key",)
    MASTER_KEY_FIELD_NUMBER: _ClassVar[int]
    master_key: MasterKey
    def __init__(self, master_key: _Optional[_Union[MasterKey, _Mapping]] = ...) -> None: ...

class SetActiveDEKRequest(_message.Message):
    __slots__ = ("dek_version",)
    DEK_VERSION_FIELD_NUMBER: _ClassVar[int]
    dek_version: int
    def __init__(self, dek_version: _Optional[int] = ...) -> None: ...

class SetActiveDEKResponse(_message.Message):
    __slots__ = ("dek",)
    DEK_FIELD_NUMBER: _ClassVar[int]
    dek: EnvironmentKey
    def __init__(self, dek: _Optional[_Union[EnvironmentKey, _Mapping]] = ...) -> None: ...

class SetActiveMasterKeyRequest(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    def __init__(self, version: _Optional[int] = ...) -> None: ...

class SetActiveMasterKeyResponse(_message.Message):
    __slots__ = ("master_key",)
    MASTER_KEY_FIELD_NUMBER: _ClassVar[int]
    master_key: MasterKey
    def __init__(self, master_key: _Optional[_Union[MasterKey, _Mapping]] = ...) -> None: ...

class DestroyDEKRequest(_message.Message):
    __slots__ = ("dek_version",)
    DEK_VERSION_FIELD_NUMBER: _ClassVar[int]
    dek_version: int
    def __init__(self, dek_version: _Optional[int] = ...) -> None: ...

class DestroyMasterKeyRequest(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    def __init__(self, version: _Optional[int] = ...) -> None: ...

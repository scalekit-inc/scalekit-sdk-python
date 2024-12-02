from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MigrationServiceResponse(_message.Message):
    __slots__ = ("success_environments", "failed_environments")
    SUCCESS_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    FAILED_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    success_environments: int
    failed_environments: int
    def __init__(self, success_environments: _Optional[int] = ..., failed_environments: _Optional[int] = ...) -> None: ...

class MigrationSAMLRequest(_message.Message):
    __slots__ = ("environment_ids", "batch_size")
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    environment_ids: _containers.RepeatedScalarFieldContainer[int]
    batch_size: int
    def __init__(self, environment_ids: _Optional[_Iterable[int]] = ..., batch_size: _Optional[int] = ...) -> None: ...

class MigrationSAMLResponse(_message.Message):
    __slots__ = ("success_environments", "failed_environments")
    SUCCESS_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    FAILED_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    success_environments: int
    failed_environments: int
    def __init__(self, success_environments: _Optional[int] = ..., failed_environments: _Optional[int] = ...) -> None: ...

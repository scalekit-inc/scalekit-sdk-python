from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class RegionCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REGION_CODE_UNSPECIFIED: _ClassVar[RegionCode]
    US: _ClassVar[RegionCode]
    EU: _ClassVar[RegionCode]

class EnvironmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENVIRONMENT_TYPE_UNSPECIFIED: _ClassVar[EnvironmentType]
    PRD: _ClassVar[EnvironmentType]
    DEV: _ClassVar[EnvironmentType]
REGION_CODE_UNSPECIFIED: RegionCode
US: RegionCode
EU: RegionCode
ENVIRONMENT_TYPE_UNSPECIFIED: EnvironmentType
PRD: EnvironmentType
DEV: EnvironmentType

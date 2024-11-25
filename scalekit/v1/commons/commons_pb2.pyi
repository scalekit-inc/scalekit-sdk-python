from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class UserStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_STATUS_UNSPECIFIED: _ClassVar[UserStatus]
    ACTIVE: _ClassVar[UserStatus]
    INACTIVE: _ClassVar[UserStatus]
REGION_CODE_UNSPECIFIED: RegionCode
US: RegionCode
EU: RegionCode
ENVIRONMENT_TYPE_UNSPECIFIED: EnvironmentType
PRD: EnvironmentType
DEV: EnvironmentType
USER_STATUS_UNSPECIFIED: UserStatus
ACTIVE: UserStatus
INACTIVE: UserStatus

class OrganizationMembership(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: UserStatus
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[UserStatus, str]] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ("id", "first_name", "last_name", "name", "locale", "email_verified", "metadata", "custom_attributes")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class CustomAttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    id: str
    first_name: str
    last_name: str
    name: str
    locale: str
    email_verified: bool
    metadata: _containers.ScalarMap[str, str]
    custom_attributes: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., name: _Optional[str] = ..., locale: _Optional[str] = ..., email_verified: bool = ..., metadata: _Optional[_Mapping[str, str]] = ..., custom_attributes: _Optional[_Mapping[str, str]] = ...) -> None: ...

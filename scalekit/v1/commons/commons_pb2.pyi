from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class MembershipStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Membership_Status_UNSPECIFIED: _ClassVar[MembershipStatus]
    ACTIVE: _ClassVar[MembershipStatus]
    INACTIVE: _ClassVar[MembershipStatus]
    PENDING_INVITE: _ClassVar[MembershipStatus]
    INVITE_EXPIRED: _ClassVar[MembershipStatus]

class IdentityProviderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IDENTITY_PROVIDER_UNSPECIFIED: _ClassVar[IdentityProviderType]
    OKTA: _ClassVar[IdentityProviderType]
    GOOGLE: _ClassVar[IdentityProviderType]
    MICROSOFT_AD: _ClassVar[IdentityProviderType]
    AUTH0: _ClassVar[IdentityProviderType]
    ONELOGIN: _ClassVar[IdentityProviderType]
    PING_IDENTITY: _ClassVar[IdentityProviderType]
    JUMPCLOUD: _ClassVar[IdentityProviderType]
    CUSTOM: _ClassVar[IdentityProviderType]
    GITHUB: _ClassVar[IdentityProviderType]
    GITLAB: _ClassVar[IdentityProviderType]
    LINKEDIN: _ClassVar[IdentityProviderType]
    SALESFORCE: _ClassVar[IdentityProviderType]
    MICROSOFT: _ClassVar[IdentityProviderType]
    IDP_SIMULATOR: _ClassVar[IdentityProviderType]
    SCALEKIT: _ClassVar[IdentityProviderType]
    ADFS: _ClassVar[IdentityProviderType]
REGION_CODE_UNSPECIFIED: RegionCode
US: RegionCode
EU: RegionCode
ENVIRONMENT_TYPE_UNSPECIFIED: EnvironmentType
PRD: EnvironmentType
DEV: EnvironmentType
Membership_Status_UNSPECIFIED: MembershipStatus
ACTIVE: MembershipStatus
INACTIVE: MembershipStatus
PENDING_INVITE: MembershipStatus
INVITE_EXPIRED: MembershipStatus
IDENTITY_PROVIDER_UNSPECIFIED: IdentityProviderType
OKTA: IdentityProviderType
GOOGLE: IdentityProviderType
MICROSOFT_AD: IdentityProviderType
AUTH0: IdentityProviderType
ONELOGIN: IdentityProviderType
PING_IDENTITY: IdentityProviderType
JUMPCLOUD: IdentityProviderType
CUSTOM: IdentityProviderType
GITHUB: IdentityProviderType
GITLAB: IdentityProviderType
LINKEDIN: IdentityProviderType
SALESFORCE: IdentityProviderType
MICROSOFT: IdentityProviderType
IDP_SIMULATOR: IdentityProviderType
SCALEKIT: IdentityProviderType
ADFS: IdentityProviderType

class OrganizationMembership(_message.Message):
    __slots__ = ("organization_id", "join_time", "membership_status", "roles", "name", "metadata", "display_name", "invited_by", "created_at", "accepted_at", "expires_at")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    JOIN_TIME_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_STATUS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    INVITED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    join_time: _timestamp_pb2.Timestamp
    membership_status: MembershipStatus
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    name: str
    metadata: _containers.ScalarMap[str, str]
    display_name: str
    invited_by: str
    created_at: _timestamp_pb2.Timestamp
    accepted_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, organization_id: _Optional[str] = ..., join_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., membership_status: _Optional[_Union[MembershipStatus, str]] = ..., roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ..., name: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., display_name: _Optional[str] = ..., invited_by: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., accepted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Role(_message.Message):
    __slots__ = ("id", "name", "display_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    display_name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ("id", "first_name", "last_name", "name", "locale", "email_verified", "phone_number", "metadata", "custom_attributes")
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
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    id: str
    first_name: str
    last_name: str
    name: str
    locale: str
    email_verified: bool
    phone_number: str
    metadata: _containers.ScalarMap[str, str]
    custom_attributes: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., name: _Optional[str] = ..., locale: _Optional[str] = ..., email_verified: bool = ..., phone_number: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., custom_attributes: _Optional[_Mapping[str, str]] = ...) -> None: ...

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

class DirectoryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTORY_TYPE_UNSPECIFIED: _ClassVar[DirectoryType]
    SCIM: _ClassVar[DirectoryType]
    LDAP: _ClassVar[DirectoryType]
    POLL: _ClassVar[DirectoryType]

class DirectoryProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTORY_PROVIDER_UNSPECIFIED: _ClassVar[DirectoryProvider]
    OKTA: _ClassVar[DirectoryProvider]
    GOOGLE: _ClassVar[DirectoryProvider]
    MICROSOFT_AD: _ClassVar[DirectoryProvider]
    AUTH0: _ClassVar[DirectoryProvider]
    ONELOGIN: _ClassVar[DirectoryProvider]
    JUMPCLOUD: _ClassVar[DirectoryProvider]
    PING_IDENTITY: _ClassVar[DirectoryProvider]

class DirectoryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTORY_STATUS_UNSPECIFIED: _ClassVar[DirectoryStatus]
    DRAFT: _ClassVar[DirectoryStatus]
    IN_PROGRESS: _ClassVar[DirectoryStatus]
    COMPLETED: _ClassVar[DirectoryStatus]

class SecretStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE: _ClassVar[SecretStatus]
    INACTIVE: _ClassVar[SecretStatus]
DIRECTORY_TYPE_UNSPECIFIED: DirectoryType
SCIM: DirectoryType
LDAP: DirectoryType
POLL: DirectoryType
DIRECTORY_PROVIDER_UNSPECIFIED: DirectoryProvider
OKTA: DirectoryProvider
GOOGLE: DirectoryProvider
MICROSOFT_AD: DirectoryProvider
AUTH0: DirectoryProvider
ONELOGIN: DirectoryProvider
JUMPCLOUD: DirectoryProvider
PING_IDENTITY: DirectoryProvider
DIRECTORY_STATUS_UNSPECIFIED: DirectoryStatus
DRAFT: DirectoryStatus
IN_PROGRESS: DirectoryStatus
COMPLETED: DirectoryStatus
ACTIVE: SecretStatus
INACTIVE: SecretStatus

class GetDirectoryRequest(_message.Message):
    __slots__ = ("id", "organization_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    organization_id: str
    def __init__(self, id: _Optional[str] = ..., organization_id: _Optional[str] = ...) -> None: ...

class GetDirectoryResponse(_message.Message):
    __slots__ = ("directory",)
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    directory: Directory
    def __init__(self, directory: _Optional[_Union[Directory, _Mapping]] = ...) -> None: ...

class CreateDirectoryRequest(_message.Message):
    __slots__ = ("organization_id", "directory")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    directory: CreateDirectory
    def __init__(self, organization_id: _Optional[str] = ..., directory: _Optional[_Union[CreateDirectory, _Mapping]] = ...) -> None: ...

class CreateDirectory(_message.Message):
    __slots__ = ("directory_type", "directory_provider")
    DIRECTORY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    directory_type: DirectoryType
    directory_provider: DirectoryProvider
    def __init__(self, directory_type: _Optional[_Union[DirectoryType, str]] = ..., directory_provider: _Optional[_Union[DirectoryProvider, str]] = ...) -> None: ...

class CreateDirectoryResponse(_message.Message):
    __slots__ = ("directory",)
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    directory: Directory
    def __init__(self, directory: _Optional[_Union[Directory, _Mapping]] = ...) -> None: ...

class UpdateDirectoryRequest(_message.Message):
    __slots__ = ("id", "organization_id", "directory")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    id: str
    organization_id: str
    directory: UpdateDirectory
    def __init__(self, id: _Optional[str] = ..., organization_id: _Optional[str] = ..., directory: _Optional[_Union[UpdateDirectory, _Mapping]] = ...) -> None: ...

class UpdateDirectory(_message.Message):
    __slots__ = ("name", "directory_type", "enabled", "directory_provider", "status", "mappings", "groups")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    directory_type: DirectoryType
    enabled: bool
    directory_provider: DirectoryProvider
    status: DirectoryStatus
    mappings: _containers.RepeatedCompositeFieldContainer[DirectoryMapping]
    groups: _containers.RepeatedCompositeFieldContainer[ExternalGroup]
    def __init__(self, name: _Optional[str] = ..., directory_type: _Optional[_Union[DirectoryType, str]] = ..., enabled: bool = ..., directory_provider: _Optional[_Union[DirectoryProvider, str]] = ..., status: _Optional[_Union[DirectoryStatus, str]] = ..., mappings: _Optional[_Iterable[_Union[DirectoryMapping, _Mapping]]] = ..., groups: _Optional[_Iterable[_Union[ExternalGroup, _Mapping]]] = ...) -> None: ...

class UpdateDirectoryResponse(_message.Message):
    __slots__ = ("directory",)
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    directory: Directory
    def __init__(self, directory: _Optional[_Union[Directory, _Mapping]] = ...) -> None: ...

class AssignGroupsForDirectoryRequest(_message.Message):
    __slots__ = ("id", "organization_id", "external_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    organization_id: str
    external_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., organization_id: _Optional[str] = ..., external_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListDirectoriesRequest(_message.Message):
    __slots__ = ("organization_id",)
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    def __init__(self, organization_id: _Optional[str] = ...) -> None: ...

class ListDirectoriesResponse(_message.Message):
    __slots__ = ("directories",)
    DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    directories: _containers.RepeatedCompositeFieldContainer[Directory]
    def __init__(self, directories: _Optional[_Iterable[_Union[Directory, _Mapping]]] = ...) -> None: ...

class ListDirectoryUsersRequest(_message.Message):
    __slots__ = ("organization_id", "directory_id", "page_size", "page_token", "include_detail", "directory_group_id", "updated_after")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DETAIL_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AFTER_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    directory_id: str
    page_size: int
    page_token: str
    include_detail: bool
    directory_group_id: str
    updated_after: _timestamp_pb2.Timestamp
    def __init__(self, organization_id: _Optional[str] = ..., directory_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., include_detail: bool = ..., directory_group_id: _Optional[str] = ..., updated_after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListDirectoryUsersResponse(_message.Message):
    __slots__ = ("users", "total_size", "next_page_token", "prev_page_token")
    USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[DirectoryUser]
    total_size: int
    next_page_token: str
    prev_page_token: str
    def __init__(self, users: _Optional[_Iterable[_Union[DirectoryUser, _Mapping]]] = ..., total_size: _Optional[int] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class ListDirectoryGroupsRequest(_message.Message):
    __slots__ = ("organization_id", "directory_id", "page_size", "page_token", "updated_after", "include_detail", "include_external_groups")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AFTER_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DETAIL_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EXTERNAL_GROUPS_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    directory_id: str
    page_size: int
    page_token: str
    updated_after: _timestamp_pb2.Timestamp
    include_detail: bool
    include_external_groups: bool
    def __init__(self, organization_id: _Optional[str] = ..., directory_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., updated_after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., include_detail: bool = ..., include_external_groups: bool = ...) -> None: ...

class ListDirectoryGroupsResponse(_message.Message):
    __slots__ = ("groups", "total_size", "next_page_token", "prev_page_token")
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[DirectoryGroup]
    total_size: int
    next_page_token: str
    prev_page_token: str
    def __init__(self, groups: _Optional[_Iterable[_Union[DirectoryGroup, _Mapping]]] = ..., total_size: _Optional[int] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class ListDirectoryGroupsSummaryRequest(_message.Message):
    __slots__ = ("organization_id", "directory_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    directory_id: str
    def __init__(self, organization_id: _Optional[str] = ..., directory_id: _Optional[str] = ...) -> None: ...

class Directory(_message.Message):
    __slots__ = ("id", "name", "directory_type", "organization_id", "enabled", "directory_provider", "last_synced_at", "directory_endpoint", "total_users", "total_groups", "secrets", "stats", "role_assignments", "attribute_mappings", "status", "email", "groups_tracked")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    LAST_SYNCED_AT_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GROUPS_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    ROLE_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    GROUPS_TRACKED_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    directory_type: DirectoryType
    organization_id: str
    enabled: bool
    directory_provider: DirectoryProvider
    last_synced_at: _timestamp_pb2.Timestamp
    directory_endpoint: str
    total_users: int
    total_groups: int
    secrets: _containers.RepeatedCompositeFieldContainer[Secret]
    stats: Stats
    role_assignments: RoleAssignments
    attribute_mappings: AttributeMappings
    status: str
    email: str
    groups_tracked: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., directory_type: _Optional[_Union[DirectoryType, str]] = ..., organization_id: _Optional[str] = ..., enabled: bool = ..., directory_provider: _Optional[_Union[DirectoryProvider, str]] = ..., last_synced_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., directory_endpoint: _Optional[str] = ..., total_users: _Optional[int] = ..., total_groups: _Optional[int] = ..., secrets: _Optional[_Iterable[_Union[Secret, _Mapping]]] = ..., stats: _Optional[_Union[Stats, _Mapping]] = ..., role_assignments: _Optional[_Union[RoleAssignments, _Mapping]] = ..., attribute_mappings: _Optional[_Union[AttributeMappings, _Mapping]] = ..., status: _Optional[str] = ..., email: _Optional[str] = ..., groups_tracked: _Optional[str] = ...) -> None: ...

class ToggleDirectoryRequest(_message.Message):
    __slots__ = ("organization_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class ToggleDirectoryResponse(_message.Message):
    __slots__ = ("enabled", "error_message")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    error_message: str
    def __init__(self, enabled: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class DirectoryMapping(_message.Message):
    __slots__ = ("key", "map_to", "display_name")
    KEY_FIELD_NUMBER: _ClassVar[int]
    MAP_TO_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    key: str
    map_to: str
    display_name: str
    def __init__(self, key: _Optional[str] = ..., map_to: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class DirectoryUser(_message.Message):
    __slots__ = ("id", "email", "preferred_username", "given_name", "family_name", "updated_at", "emails", "groups", "user_detail")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_USERNAME_FIELD_NUMBER: _ClassVar[int]
    GIVEN_NAME_FIELD_NUMBER: _ClassVar[int]
    FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    EMAILS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    USER_DETAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    preferred_username: str
    given_name: str
    family_name: str
    updated_at: _timestamp_pb2.Timestamp
    emails: _containers.RepeatedScalarFieldContainer[str]
    groups: _containers.RepeatedCompositeFieldContainer[DirectoryGroup]
    user_detail: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., preferred_username: _Optional[str] = ..., given_name: _Optional[str] = ..., family_name: _Optional[str] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., emails: _Optional[_Iterable[str]] = ..., groups: _Optional[_Iterable[_Union[DirectoryGroup, _Mapping]]] = ..., user_detail: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ExternalGroup(_message.Message):
    __slots__ = ("external_id", "display_name", "email")
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    display_name: str
    email: str
    def __init__(self, external_id: _Optional[str] = ..., display_name: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class DirectoryGroup(_message.Message):
    __slots__ = ("id", "display_name", "total_users", "updated_at", "group_detail")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_USERS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    GROUP_DETAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    total_users: int
    updated_at: _timestamp_pb2.Timestamp
    group_detail: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., display_name: _Optional[str] = ..., total_users: _Optional[int] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., group_detail: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CreateDirectorySecretRequest(_message.Message):
    __slots__ = ("organization_id", "directory_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    directory_id: str
    def __init__(self, organization_id: _Optional[str] = ..., directory_id: _Optional[str] = ...) -> None: ...

class CreateDirectorySecretResponse(_message.Message):
    __slots__ = ("plain_secret", "secret")
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    plain_secret: str
    secret: Secret
    def __init__(self, plain_secret: _Optional[str] = ..., secret: _Optional[_Union[Secret, _Mapping]] = ...) -> None: ...

class RegenerateDirectorySecretRequest(_message.Message):
    __slots__ = ("organization_id", "directory_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    directory_id: str
    def __init__(self, organization_id: _Optional[str] = ..., directory_id: _Optional[str] = ...) -> None: ...

class RegenerateDirectorySecretResponse(_message.Message):
    __slots__ = ("plain_secret", "secret")
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    plain_secret: str
    secret: Secret
    def __init__(self, plain_secret: _Optional[str] = ..., secret: _Optional[_Union[Secret, _Mapping]] = ...) -> None: ...

class Secret(_message.Message):
    __slots__ = ("id", "create_time", "secret_suffix", "status", "expire_time", "last_used_time", "directory_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    SECRET_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_TIME_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    secret_suffix: str
    status: SecretStatus
    expire_time: _timestamp_pb2.Timestamp
    last_used_time: _timestamp_pb2.Timestamp
    directory_id: str
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., secret_suffix: _Optional[str] = ..., status: _Optional[_Union[SecretStatus, str]] = ..., expire_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_used_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., directory_id: _Optional[str] = ...) -> None: ...

class Stats(_message.Message):
    __slots__ = ("total_users", "total_groups", "group_updated_at", "user_updated_at")
    TOTAL_USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GROUPS_FIELD_NUMBER: _ClassVar[int]
    GROUP_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    total_users: int
    total_groups: int
    group_updated_at: _timestamp_pb2.Timestamp
    user_updated_at: _timestamp_pb2.Timestamp
    def __init__(self, total_users: _Optional[int] = ..., total_groups: _Optional[int] = ..., group_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AssignRolesRequest(_message.Message):
    __slots__ = ("organization_id", "id", "role_assignments")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    role_assignments: RoleAssignments
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., role_assignments: _Optional[_Union[RoleAssignments, _Mapping]] = ...) -> None: ...

class RoleAssignments(_message.Message):
    __slots__ = ("assignments",)
    ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[RoleAssignment]
    def __init__(self, assignments: _Optional[_Iterable[_Union[RoleAssignment, _Mapping]]] = ...) -> None: ...

class AssignRolesResponse(_message.Message):
    __slots__ = ("role_assignments",)
    ROLE_ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    role_assignments: RoleAssignments
    def __init__(self, role_assignments: _Optional[_Union[RoleAssignments, _Mapping]] = ...) -> None: ...

class RoleAssignment(_message.Message):
    __slots__ = ("group_id", "role_name", "role_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    role_name: str
    role_id: str
    def __init__(self, group_id: _Optional[str] = ..., role_name: _Optional[str] = ..., role_id: _Optional[str] = ...) -> None: ...

class UpdateAttributesRequest(_message.Message):
    __slots__ = ("organization_id", "id", "attribute_mapping")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_MAPPING_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    attribute_mapping: AttributeMappings
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., attribute_mapping: _Optional[_Union[AttributeMappings, _Mapping]] = ...) -> None: ...

class AttributeMappings(_message.Message):
    __slots__ = ("attributes",)
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[AttributeMapping]
    def __init__(self, attributes: _Optional[_Iterable[_Union[AttributeMapping, _Mapping]]] = ...) -> None: ...

class AttributeMapping(_message.Message):
    __slots__ = ("key", "map_to")
    KEY_FIELD_NUMBER: _ClassVar[int]
    MAP_TO_FIELD_NUMBER: _ClassVar[int]
    key: str
    map_to: str
    def __init__(self, key: _Optional[str] = ..., map_to: _Optional[str] = ...) -> None: ...

class UpdateAttributesResponse(_message.Message):
    __slots__ = ("attribute_mappings",)
    ATTRIBUTE_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    attribute_mappings: AttributeMappings
    def __init__(self, attribute_mappings: _Optional[_Union[AttributeMappings, _Mapping]] = ...) -> None: ...

class DeleteDirectoryRequest(_message.Message):
    __slots__ = ("organization_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class TriggerDirectorySyncRequest(_message.Message):
    __slots__ = ("directory_id", "organization_id")
    DIRECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    directory_id: str
    organization_id: str
    def __init__(self, directory_id: _Optional[str] = ..., organization_id: _Optional[str] = ...) -> None: ...

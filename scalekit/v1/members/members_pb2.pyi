from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from scalekit.v1.users import users_pb2 as _users_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MEMBER_ROLE_UNSPECIFIED: _ClassVar[MemberRole]
    ADMIN: _ClassVar[MemberRole]
    USER: _ClassVar[MemberRole]
MEMBER_ROLE_UNSPECIFIED: MemberRole
ADMIN: MemberRole
USER: MemberRole

class Member(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "workspace_id", "role", "first_name", "last_name", "email", "metadata", "organizations", "user_profile", "external_id", "workspace_ids", "active_workspace_external_id", "dashboard_role", "dashboard_role_name")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_IDS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_WORKSPACE_EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ROLE_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    workspace_id: str
    role: MemberRole
    first_name: str
    last_name: str
    email: str
    metadata: _containers.ScalarMap[str, str]
    organizations: _containers.RepeatedCompositeFieldContainer[_commons_pb2.OrganizationMembership]
    user_profile: _commons_pb2.UserProfile
    external_id: str
    workspace_ids: _containers.RepeatedScalarFieldContainer[str]
    active_workspace_external_id: str
    dashboard_role: DashboardRole
    dashboard_role_name: str
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workspace_id: _Optional[str] = ..., role: _Optional[_Union[MemberRole, str]] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., organizations: _Optional[_Iterable[_Union[_commons_pb2.OrganizationMembership, _Mapping]]] = ..., user_profile: _Optional[_Union[_commons_pb2.UserProfile, _Mapping]] = ..., external_id: _Optional[str] = ..., workspace_ids: _Optional[_Iterable[str]] = ..., active_workspace_external_id: _Optional[str] = ..., dashboard_role: _Optional[_Union[DashboardRole, _Mapping]] = ..., dashboard_role_name: _Optional[str] = ...) -> None: ...

class CreateMemberRequest(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: Member
    def __init__(self, member: _Optional[_Union[Member, _Mapping]] = ...) -> None: ...

class InviteMemberRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class CreateMemberResponse(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: Member
    def __init__(self, member: _Optional[_Union[Member, _Mapping]] = ...) -> None: ...

class UpdateMember(_message.Message):
    __slots__ = ("first_name", "last_name", "metadata", "user_profile")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    metadata: _containers.ScalarMap[str, str]
    user_profile: _users_pb2.UpdateUserProfile
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., user_profile: _Optional[_Union[_users_pb2.UpdateUserProfile, _Mapping]] = ...) -> None: ...

class UpdateCurrentMemberRequest(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: UpdateMember
    def __init__(self, member: _Optional[_Union[UpdateMember, _Mapping]] = ...) -> None: ...

class UpdateMemberRequest(_message.Message):
    __slots__ = ("id", "member")
    ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    id: str
    member: UpdateMember
    def __init__(self, id: _Optional[str] = ..., member: _Optional[_Union[UpdateMember, _Mapping]] = ...) -> None: ...

class UpdateMemberResponse(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: Member
    def __init__(self, member: _Optional[_Union[Member, _Mapping]] = ...) -> None: ...

class GetCurrentMemberRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMemberRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetMemberResponse(_message.Message):
    __slots__ = ("member", "dashboard_permissions")
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    member: Member
    dashboard_permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, member: _Optional[_Union[Member, _Mapping]] = ..., dashboard_permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class ListMemberRequest(_message.Message):
    __slots__ = ("page_size", "page_token")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListMemberResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "members")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    members: _containers.RepeatedCompositeFieldContainer[Member]
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., members: _Optional[_Iterable[_Union[Member, _Mapping]]] = ...) -> None: ...

class DeleteMemberRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DashboardRole(_message.Message):
    __slots__ = ("id", "name", "display_name", "permissions", "is_fixed", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    IS_FIXED_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    display_name: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    is_fixed: bool
    description: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ..., is_fixed: bool = ..., description: _Optional[str] = ...) -> None: ...

class AssignDashboardRoleRequest(_message.Message):
    __slots__ = ("member_id", "role")
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    member_id: str
    role: str
    def __init__(self, member_id: _Optional[str] = ..., role: _Optional[str] = ...) -> None: ...

class AssignDashboardRoleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetDashboardEnvironmentRoleRequest(_message.Message):
    __slots__ = ("member_id", "environment_id", "role")
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    member_id: str
    environment_id: str
    role: str
    def __init__(self, member_id: _Optional[str] = ..., environment_id: _Optional[str] = ..., role: _Optional[str] = ...) -> None: ...

class SetDashboardEnvironmentRoleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClearDashboardEnvironmentRoleRequest(_message.Message):
    __slots__ = ("member_id", "environment_id")
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    member_id: str
    environment_id: str
    def __init__(self, member_id: _Optional[str] = ..., environment_id: _Optional[str] = ...) -> None: ...

class ClearDashboardEnvironmentRoleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDashboardRolesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDashboardRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[DashboardRole]
    def __init__(self, roles: _Optional[_Iterable[_Union[DashboardRole, _Mapping]]] = ...) -> None: ...

class DashboardPermission(_message.Message):
    __slots__ = ("key", "group", "tier", "description", "sensitive")
    KEY_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SENSITIVE_FIELD_NUMBER: _ClassVar[int]
    key: str
    group: str
    tier: str
    description: str
    sensitive: bool
    def __init__(self, key: _Optional[str] = ..., group: _Optional[str] = ..., tier: _Optional[str] = ..., description: _Optional[str] = ..., sensitive: bool = ...) -> None: ...

class ListDashboardPermissionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDashboardPermissionsResponse(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[DashboardPermission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[DashboardPermission, _Mapping]]] = ...) -> None: ...

class CreateDashboardRoleRequest(_message.Message):
    __slots__ = ("name", "description", "permissions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateDashboardRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: DashboardRole
    def __init__(self, role: _Optional[_Union[DashboardRole, _Mapping]] = ...) -> None: ...

class UpdateDashboardRoleRequest(_message.Message):
    __slots__ = ("role_id", "name", "description", "permissions")
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    role_id: str
    name: str
    description: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, role_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateDashboardRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: DashboardRole
    def __init__(self, role: _Optional[_Union[DashboardRole, _Mapping]] = ...) -> None: ...

class DeleteDashboardRoleRequest(_message.Message):
    __slots__ = ("role_id",)
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    role_id: str
    def __init__(self, role_id: _Optional[str] = ...) -> None: ...

class DeleteDashboardRoleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListDashboardMemberEnvironmentRolesRequest(_message.Message):
    __slots__ = ("member_id",)
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    member_id: str
    def __init__(self, member_id: _Optional[str] = ...) -> None: ...

class DashboardMemberEnvironmentRole(_message.Message):
    __slots__ = ("environment_id", "environment_name", "effective_role", "is_override")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_ROLE_FIELD_NUMBER: _ClassVar[int]
    IS_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    environment_name: str
    effective_role: DashboardRole
    is_override: bool
    def __init__(self, environment_id: _Optional[str] = ..., environment_name: _Optional[str] = ..., effective_role: _Optional[_Union[DashboardRole, _Mapping]] = ..., is_override: bool = ...) -> None: ...

class ListDashboardMemberEnvironmentRolesResponse(_message.Message):
    __slots__ = ("environments",)
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    environments: _containers.RepeatedCompositeFieldContainer[DashboardMemberEnvironmentRole]
    def __init__(self, environments: _Optional[_Iterable[_Union[DashboardMemberEnvironmentRole, _Mapping]]] = ...) -> None: ...

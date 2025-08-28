from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Role(_message.Message):
    __slots__ = ("id", "name", "display_name", "description", "default_creator", "default_member", "extends", "permissions", "dependent_roles_count", "is_org_role")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    DEPENDENT_ROLES_COUNT_FIELD_NUMBER: _ClassVar[int]
    IS_ORG_ROLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    display_name: str
    description: str
    default_creator: bool
    default_member: bool
    extends: str
    permissions: _containers.RepeatedCompositeFieldContainer[RolePermission]
    dependent_roles_count: int
    is_org_role: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., default_creator: bool = ..., default_member: bool = ..., extends: _Optional[str] = ..., permissions: _Optional[_Iterable[_Union[RolePermission, _Mapping]]] = ..., dependent_roles_count: _Optional[int] = ..., is_org_role: bool = ...) -> None: ...

class CreateRole(_message.Message):
    __slots__ = ("name", "display_name", "description", "extends", "permissions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    description: str
    extends: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., extends: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateOrganizationRole(_message.Message):
    __slots__ = ("name", "display_name", "description", "extends", "permissions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    description: str
    extends: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., extends: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateRoleRequest(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: CreateRole
    def __init__(self, role: _Optional[_Union[CreateRole, _Mapping]] = ...) -> None: ...

class CreateRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class GetRoleRequest(_message.Message):
    __slots__ = ("role_name", "include")
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    include: str
    def __init__(self, role_name: _Optional[str] = ..., include: _Optional[str] = ...) -> None: ...

class GetRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class ListRolesRequest(_message.Message):
    __slots__ = ("include",)
    INCLUDE_FIELD_NUMBER: _ClassVar[int]
    include: str
    def __init__(self, include: _Optional[str] = ...) -> None: ...

class ListRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ...) -> None: ...

class UpdateRole(_message.Message):
    __slots__ = ("display_name", "description", "extends", "permissions")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    extends: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., extends: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateRoleRequest(_message.Message):
    __slots__ = ("role_name", "role")
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    role: UpdateRole
    def __init__(self, role_name: _Optional[str] = ..., role: _Optional[_Union[UpdateRole, _Mapping]] = ...) -> None: ...

class UpdateRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class DeleteRoleRequest(_message.Message):
    __slots__ = ("role_name", "reassign_role_id", "reassign_role_name")
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    REASSIGN_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    REASSIGN_ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    reassign_role_id: str
    reassign_role_name: str
    def __init__(self, role_name: _Optional[str] = ..., reassign_role_id: _Optional[str] = ..., reassign_role_name: _Optional[str] = ...) -> None: ...

class CreateOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "role")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    role: CreateOrganizationRole
    def __init__(self, org_id: _Optional[str] = ..., role: _Optional[_Union[CreateOrganizationRole, _Mapping]] = ...) -> None: ...

class CreateOrganizationRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class GetOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "role_name", "include")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    role_name: str
    include: str
    def __init__(self, org_id: _Optional[str] = ..., role_name: _Optional[str] = ..., include: _Optional[str] = ...) -> None: ...

class GetOrganizationRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class ListOrganizationRolesRequest(_message.Message):
    __slots__ = ("org_id", "include")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    include: str
    def __init__(self, org_id: _Optional[str] = ..., include: _Optional[str] = ...) -> None: ...

class ListOrganizationRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ...) -> None: ...

class UpdateOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "role_name", "role")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    role_name: str
    role: UpdateRole
    def __init__(self, org_id: _Optional[str] = ..., role_name: _Optional[str] = ..., role: _Optional[_Union[UpdateRole, _Mapping]] = ...) -> None: ...

class UpdateOrganizationRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class DeleteOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "role_name", "reassign_role_name")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    REASSIGN_ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    role_name: str
    reassign_role_name: str
    def __init__(self, org_id: _Optional[str] = ..., role_name: _Optional[str] = ..., reassign_role_name: _Optional[str] = ...) -> None: ...

class GetRoleUsersCountRequest(_message.Message):
    __slots__ = ("role_name",)
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    def __init__(self, role_name: _Optional[str] = ...) -> None: ...

class GetRoleUsersCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class GetOrganizationRoleUsersCountRequest(_message.Message):
    __slots__ = ("org_id", "role_name")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    role_name: str
    def __init__(self, org_id: _Optional[str] = ..., role_name: _Optional[str] = ...) -> None: ...

class GetOrganizationRoleUsersCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class UpdateDefaultRolesRequest(_message.Message):
    __slots__ = ("default_creator", "default_member", "default_creator_role", "default_member_role")
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_CREATOR_ROLE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_ROLE_FIELD_NUMBER: _ClassVar[int]
    default_creator: UpdateDefaultRole
    default_member: UpdateDefaultRole
    default_creator_role: str
    default_member_role: str
    def __init__(self, default_creator: _Optional[_Union[UpdateDefaultRole, _Mapping]] = ..., default_member: _Optional[_Union[UpdateDefaultRole, _Mapping]] = ..., default_creator_role: _Optional[str] = ..., default_member_role: _Optional[str] = ...) -> None: ...

class UpdateDefaultOrganizationRolesRequest(_message.Message):
    __slots__ = ("org_id", "default_member_role")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_ROLE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    default_member_role: str
    def __init__(self, org_id: _Optional[str] = ..., default_member_role: _Optional[str] = ...) -> None: ...

class UpdateDefaultRolesResponse(_message.Message):
    __slots__ = ("default_creator", "default_member")
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    default_creator: Role
    default_member: Role
    def __init__(self, default_creator: _Optional[_Union[Role, _Mapping]] = ..., default_member: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class UpdateDefaultOrganizationRolesResponse(_message.Message):
    __slots__ = ("default_member",)
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    default_member: Role
    def __init__(self, default_member: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class UpdateDefaultRole(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Permission(_message.Message):
    __slots__ = ("id", "name", "description", "create_time", "update_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RolePermission(_message.Message):
    __slots__ = ("id", "name", "description", "create_time", "update_time", "role_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    role_name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., role_name: _Optional[str] = ...) -> None: ...

class CreatePermission(_message.Message):
    __slots__ = ("name", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreatePermissionRequest(_message.Message):
    __slots__ = ("permission",)
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    permission: CreatePermission
    def __init__(self, permission: _Optional[_Union[CreatePermission, _Mapping]] = ...) -> None: ...

class CreatePermissionResponse(_message.Message):
    __slots__ = ("permission",)
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    permission: Permission
    def __init__(self, permission: _Optional[_Union[Permission, _Mapping]] = ...) -> None: ...

class GetPermissionRequest(_message.Message):
    __slots__ = ("permission_name",)
    PERMISSION_NAME_FIELD_NUMBER: _ClassVar[int]
    permission_name: str
    def __init__(self, permission_name: _Optional[str] = ...) -> None: ...

class GetPermissionResponse(_message.Message):
    __slots__ = ("permission",)
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    permission: Permission
    def __init__(self, permission: _Optional[_Union[Permission, _Mapping]] = ...) -> None: ...

class UpdatePermissionRequest(_message.Message):
    __slots__ = ("permission_name", "permission")
    PERMISSION_NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    permission_name: str
    permission: CreatePermission
    def __init__(self, permission_name: _Optional[str] = ..., permission: _Optional[_Union[CreatePermission, _Mapping]] = ...) -> None: ...

class UpdatePermissionResponse(_message.Message):
    __slots__ = ("permission",)
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    permission: Permission
    def __init__(self, permission: _Optional[_Union[Permission, _Mapping]] = ...) -> None: ...

class ListPermissionsRequest(_message.Message):
    __slots__ = ("page_token", "page_size")
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    page_token: str
    page_size: int
    def __init__(self, page_token: _Optional[str] = ..., page_size: _Optional[int] = ...) -> None: ...

class ListPermissionsResponse(_message.Message):
    __slots__ = ("permissions", "prev_page_token", "next_page_token", "total_size")
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    prev_page_token: str
    next_page_token: str
    total_size: int
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ..., prev_page_token: _Optional[str] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class DeletePermissionRequest(_message.Message):
    __slots__ = ("permission_name",)
    PERMISSION_NAME_FIELD_NUMBER: _ClassVar[int]
    permission_name: str
    def __init__(self, permission_name: _Optional[str] = ...) -> None: ...

class ListRolePermissionsRequest(_message.Message):
    __slots__ = ("role_name",)
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    def __init__(self, role_name: _Optional[str] = ...) -> None: ...

class ListRolePermissionsResponse(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

class AddPermissionsToRoleRequest(_message.Message):
    __slots__ = ("role_name", "permission_names")
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_NAMES_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    permission_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, role_name: _Optional[str] = ..., permission_names: _Optional[_Iterable[str]] = ...) -> None: ...

class AddPermissionsToRoleResponse(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

class RemovePermissionFromRoleRequest(_message.Message):
    __slots__ = ("role_name", "permission_name")
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    permission_name: str
    def __init__(self, role_name: _Optional[str] = ..., permission_name: _Optional[str] = ...) -> None: ...

class ListEffectiveRolePermissionsRequest(_message.Message):
    __slots__ = ("role_name",)
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    def __init__(self, role_name: _Optional[str] = ...) -> None: ...

class ListEffectiveRolePermissionsResponse(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

class ListDependentRolesRequest(_message.Message):
    __slots__ = ("role_name",)
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    def __init__(self, role_name: _Optional[str] = ...) -> None: ...

class ListDependentRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ...) -> None: ...

class DeleteRoleBaseRequest(_message.Message):
    __slots__ = ("role_name",)
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    def __init__(self, role_name: _Optional[str] = ...) -> None: ...

class DeleteOrganizationRoleBaseRequest(_message.Message):
    __slots__ = ("org_id", "role_name")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    role_name: str
    def __init__(self, org_id: _Optional[str] = ..., role_name: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("id", "name", "display_name", "description", "default", "default_creator", "default_member")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    display_name: str
    description: str
    default: bool
    default_creator: bool
    default_member: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., default: bool = ..., default_creator: bool = ..., default_member: bool = ...) -> None: ...

class CreateRole(_message.Message):
    __slots__ = ("name", "display_name", "description", "default", "default_creator", "default_member")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    description: str
    default: bool
    default_creator: bool
    default_member: bool
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., default: bool = ..., default_creator: bool = ..., default_member: bool = ...) -> None: ...

class CreateRoleRequest(_message.Message):
    __slots__ = ("env_id", "role")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    role: CreateRole
    def __init__(self, env_id: _Optional[str] = ..., role: _Optional[_Union[CreateRole, _Mapping]] = ...) -> None: ...

class CreateRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class GetRoleRequest(_message.Message):
    __slots__ = ("env_id", "id")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    id: str
    def __init__(self, env_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class ListRolesRequest(_message.Message):
    __slots__ = ("env_id",)
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    def __init__(self, env_id: _Optional[str] = ...) -> None: ...

class ListRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ...) -> None: ...

class UpdateRole(_message.Message):
    __slots__ = ("display_name", "description", "default", "default_creator", "default_member")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    default: bool
    default_creator: bool
    default_member: bool
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., default: bool = ..., default_creator: bool = ..., default_member: bool = ...) -> None: ...

class UpdateRoleRequest(_message.Message):
    __slots__ = ("env_id", "id", "role")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    id: str
    role: UpdateRole
    def __init__(self, env_id: _Optional[str] = ..., id: _Optional[str] = ..., role: _Optional[_Union[UpdateRole, _Mapping]] = ...) -> None: ...

class UpdateRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class DeleteRoleRequest(_message.Message):
    __slots__ = ("env_id", "id", "reassign_role_id")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    REASSIGN_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    id: str
    reassign_role_id: str
    def __init__(self, env_id: _Optional[str] = ..., id: _Optional[str] = ..., reassign_role_id: _Optional[str] = ...) -> None: ...

class CreateOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "role")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    role: CreateRole
    def __init__(self, org_id: _Optional[str] = ..., role: _Optional[_Union[CreateRole, _Mapping]] = ...) -> None: ...

class CreateOrganizationRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class GetOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "id")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    id: str
    def __init__(self, org_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetOrganizationRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class ListOrganizationRolesRequest(_message.Message):
    __slots__ = ("org_id",)
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    def __init__(self, org_id: _Optional[str] = ...) -> None: ...

class ListOrganizationRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ...) -> None: ...

class UpdateOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "id", "role")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    id: str
    role: UpdateRole
    def __init__(self, org_id: _Optional[str] = ..., id: _Optional[str] = ..., role: _Optional[_Union[UpdateRole, _Mapping]] = ...) -> None: ...

class UpdateOrganizationRoleResponse(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: Role
    def __init__(self, role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class DeleteOrganizationRoleRequest(_message.Message):
    __slots__ = ("org_id", "id", "reassign_role_id")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    REASSIGN_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    id: str
    reassign_role_id: str
    def __init__(self, org_id: _Optional[str] = ..., id: _Optional[str] = ..., reassign_role_id: _Optional[str] = ...) -> None: ...

class GetRoleUsersCountRequest(_message.Message):
    __slots__ = ("env_id", "id")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    id: str
    def __init__(self, env_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetRoleUsersCountResponse(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class UpdateDefaultRolesRequest(_message.Message):
    __slots__ = ("env_id", "default_creator", "default_member")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    default_creator: UpdateDefaultRole
    default_member: UpdateDefaultRole
    def __init__(self, env_id: _Optional[str] = ..., default_creator: _Optional[_Union[UpdateDefaultRole, _Mapping]] = ..., default_member: _Optional[_Union[UpdateDefaultRole, _Mapping]] = ...) -> None: ...

class UpdateDefaultRolesResponse(_message.Message):
    __slots__ = ("default_creator", "default_member")
    DEFAULT_CREATOR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    default_creator: Role
    default_member: Role
    def __init__(self, default_creator: _Optional[_Union[Role, _Mapping]] = ..., default_member: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class UpdateDefaultRole(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

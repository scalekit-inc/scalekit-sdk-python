from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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
    __slots__ = ("id", "create_time", "update_time", "workspace_id", "role", "first_name", "last_name", "email", "metadata", "organizations", "user_profile", "external_id")
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
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workspace_id: _Optional[str] = ..., role: _Optional[_Union[MemberRole, str]] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., email: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., organizations: _Optional[_Iterable[_Union[_commons_pb2.OrganizationMembership, _Mapping]]] = ..., user_profile: _Optional[_Union[_commons_pb2.UserProfile, _Mapping]] = ..., external_id: _Optional[str] = ...) -> None: ...

class CreateMemberRequest(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: Member
    def __init__(self, member: _Optional[_Union[Member, _Mapping]] = ...) -> None: ...

class CreateMemberResponse(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: Member
    def __init__(self, member: _Optional[_Union[Member, _Mapping]] = ...) -> None: ...

class UpdateMember(_message.Message):
    __slots__ = ("role", "first_name", "last_name", "metadata", "user_profile")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ROLE_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    role: MemberRole
    first_name: str
    last_name: str
    metadata: _containers.ScalarMap[str, str]
    user_profile: _users_pb2.UpdateUserProfile
    def __init__(self, role: _Optional[_Union[MemberRole, str]] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., user_profile: _Optional[_Union[_users_pb2.UpdateUserProfile, _Mapping]] = ...) -> None: ...

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
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: Member
    def __init__(self, member: _Optional[_Union[Member, _Mapping]] = ...) -> None: ...

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

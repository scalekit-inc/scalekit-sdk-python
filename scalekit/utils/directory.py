
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, \
    Union as _Union

from scalekit.v1.directories.directories_pb2 import DirectoryGroup


class DirUser(_message.Message):
    """ """
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
    id: str | None
    email: str | None
    preferred_username: str | None
    given_name: str | None
    family_name: str | None
    updated_at: _timestamp_pb2.Timestamp | None
    emails: _containers.RepeatedScalarFieldContainer[str] | None
    groups: _containers.RepeatedCompositeFieldContainer[DirectoryGroup] | None
    user_detail: str | None

    def __init__(self): ...


class DirGroup(_message.Message):
    """ """
    __slots__ = ("id", "display_name", "total_users", "updated_at", "group_detail")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_USERS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    GROUP_DETAIL_FIELD_NUMBER: _ClassVar[int]
    id: str | None
    display_name: str | None
    total_users: int | None
    updated_at: _timestamp_pb2.Timestamp | None
    group_detail: str | None
    def __init__(self): ...


class ListDirUsersResponse(_message.Message):
    __slots__ = ("users", "total_size", "next_page_token", "prev_page_token")
    USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[DirUser]
    total_size: int
    next_page_token: str
    prev_page_token: str

    def __init__(self, users: _Optional[_Iterable[_Union[DirUser, _Mapping]]] = ...,
                 total_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...,
                 prev_page_token: _Optional[str] = ...) -> None: ...


class ListDirGroupsResponse(_message.Message):
    __slots__ = ("groups", "total_size", "next_page_token", "prev_page_token")
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[DirGroup]
    total_size: int
    next_page_token: str
    prev_page_token: str

    def __init__(self, groups: _Optional[_Iterable[_Union[DirGroup, _Mapping]]] = ...,
                 total_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...,
                 prev_page_token: _Optional[str] = ...) -> None: ...

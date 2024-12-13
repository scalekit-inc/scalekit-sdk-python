from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "environment_id", "create_time", "update_time", "email", "external_id", "identity", "phone_number", "organizations", "user_profile", "metadata", "last_login")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    LAST_LOGIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    email: str
    external_id: str
    identity: str
    phone_number: str
    organizations: _containers.RepeatedCompositeFieldContainer[_commons_pb2.OrganizationMembership]
    user_profile: _commons_pb2.UserProfile
    metadata: _containers.ScalarMap[str, str]
    last_login: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., email: _Optional[str] = ..., external_id: _Optional[str] = ..., identity: _Optional[str] = ..., phone_number: _Optional[str] = ..., organizations: _Optional[_Iterable[_Union[_commons_pb2.OrganizationMembership, _Mapping]]] = ..., user_profile: _Optional[_Union[_commons_pb2.UserProfile, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., last_login: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("organization_id", "user")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user: User
    def __init__(self, organization_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UpdateUser(_message.Message):
    __slots__ = ("external_id", "metadata", "user_profile")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    metadata: _containers.ScalarMap[str, str]
    user_profile: _commons_pb2.UserProfile
    def __init__(self, external_id: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., user_profile: _Optional[_Union[_commons_pb2.UserProfile, _Mapping]] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("organization_id", "id", "external_id", "identity", "user")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    external_id: str
    identity: str
    user: UpdateUser
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., external_id: _Optional[str] = ..., identity: _Optional[str] = ..., user: _Optional[_Union[UpdateUser, _Mapping]] = ...) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("organization_id", "id", "external_id", "identity")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    external_id: str
    identity: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., external_id: _Optional[str] = ..., identity: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class ListUserRequest(_message.Message):
    __slots__ = ("organization_id", "page_size", "page_token")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    page_size: int
    page_token: str
    def __init__(self, organization_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListUserResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "users", "prev_page_token")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    users: _containers.RepeatedCompositeFieldContainer[User]
    prev_page_token: str
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("organization_id", "id", "external_id", "identity")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    external_id: str
    identity: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., external_id: _Optional[str] = ..., identity: _Optional[str] = ...) -> None: ...

class AddUserRequest(_message.Message):
    __slots__ = ("organization_id", "id", "external_id", "identity")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    external_id: str
    identity: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., external_id: _Optional[str] = ..., identity: _Optional[str] = ...) -> None: ...

class AddUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

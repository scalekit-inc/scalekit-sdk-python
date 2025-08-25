from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.errdetails import errdetails_pb2 as _errdetails_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "environment_id", "create_time", "update_time", "email", "external_id", "memberships", "user_profile", "metadata", "last_login")
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
    MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    LAST_LOGIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    email: str
    external_id: str
    memberships: _containers.RepeatedCompositeFieldContainer[_commons_pb2.OrganizationMembership]
    user_profile: _commons_pb2.UserProfile
    metadata: _containers.ScalarMap[str, str]
    last_login: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., email: _Optional[str] = ..., external_id: _Optional[str] = ..., memberships: _Optional[_Iterable[_Union[_commons_pb2.OrganizationMembership, _Mapping]]] = ..., user_profile: _Optional[_Union[_commons_pb2.UserProfile, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., last_login: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateUserAndMembershipRequest(_message.Message):
    __slots__ = ("organization_id", "user", "send_invitation_email")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    SEND_INVITATION_EMAIL_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user: CreateUser
    send_invitation_email: bool
    def __init__(self, organization_id: _Optional[str] = ..., user: _Optional[_Union[CreateUser, _Mapping]] = ..., send_invitation_email: bool = ...) -> None: ...

class CreateUserAndMembershipResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UpdateUser(_message.Message):
    __slots__ = ("external_id", "user_profile", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    user_profile: UpdateUserProfile
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, external_id: _Optional[str] = ..., user_profile: _Optional[_Union[UpdateUserProfile, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("id", "external_id", "user")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    user: UpdateUser
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ..., user: _Optional[_Union[UpdateUser, _Mapping]] = ...) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id", "external_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class ListOrganizationUsersRequest(_message.Message):
    __slots__ = ("organization_id", "page_size", "page_token")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    page_size: int
    page_token: str
    def __init__(self, organization_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListOrganizationUsersResponse(_message.Message):
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

class DeleteMembershipRequest(_message.Message):
    __slots__ = ("organization_id", "id", "external_id", "cascade")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CASCADE_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    external_id: str
    cascade: bool
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., external_id: _Optional[str] = ..., cascade: bool = ...) -> None: ...

class CreateMembershipRequest(_message.Message):
    __slots__ = ("organization_id", "membership", "id", "external_id", "send_invitation_email")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SEND_INVITATION_EMAIL_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    membership: CreateMembership
    id: str
    external_id: str
    send_invitation_email: bool
    def __init__(self, organization_id: _Optional[str] = ..., membership: _Optional[_Union[CreateMembership, _Mapping]] = ..., id: _Optional[str] = ..., external_id: _Optional[str] = ..., send_invitation_email: bool = ...) -> None: ...

class CreateMembershipResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ("page_size", "page_token")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ("users", "next_page_token", "total_size", "prev_page_token")
    USERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    next_page_token: str
    total_size: int
    prev_page_token: str
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class SearchUsersRequest(_message.Message):
    __slots__ = ("query", "page_size", "page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_size: int
    page_token: str
    def __init__(self, query: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class SearchUsersResponse(_message.Message):
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
    __slots__ = ("id", "external_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ...) -> None: ...

class UpdateMembershipRequest(_message.Message):
    __slots__ = ("organization_id", "id", "external_id", "membership")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    external_id: str
    membership: UpdateMembership
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ..., external_id: _Optional[str] = ..., membership: _Optional[_Union[UpdateMembership, _Mapping]] = ...) -> None: ...

class UpdateMembership(_message.Message):
    __slots__ = ("roles", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ROLES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[_commons_pb2.Role]
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, roles: _Optional[_Iterable[_Union[_commons_pb2.Role, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreateMembership(_message.Message):
    __slots__ = ("roles", "metadata", "inviter_email")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ROLES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    INVITER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[_commons_pb2.Role]
    metadata: _containers.ScalarMap[str, str]
    inviter_email: str
    def __init__(self, roles: _Optional[_Iterable[_Union[_commons_pb2.Role, _Mapping]]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., inviter_email: _Optional[str] = ...) -> None: ...

class UpdateMembershipResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class SearchOrganizationUsersRequest(_message.Message):
    __slots__ = ("organization_id", "query", "page_size", "page_token")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    query: str
    page_size: int
    page_token: str
    def __init__(self, organization_id: _Optional[str] = ..., query: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class SearchOrganizationUsersResponse(_message.Message):
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

class CreateUser(_message.Message):
    __slots__ = ("email", "external_id", "membership", "user_profile", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    email: str
    external_id: str
    membership: CreateMembership
    user_profile: CreateUserProfile
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, email: _Optional[str] = ..., external_id: _Optional[str] = ..., membership: _Optional[_Union[CreateMembership, _Mapping]] = ..., user_profile: _Optional[_Union[CreateUserProfile, _Mapping]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CreateUserProfile(_message.Message):
    __slots__ = ("first_name", "last_name", "name", "locale", "phone_number", "metadata", "custom_attributes")
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
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    name: str
    locale: str
    phone_number: str
    metadata: _containers.ScalarMap[str, str]
    custom_attributes: _containers.ScalarMap[str, str]
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., name: _Optional[str] = ..., locale: _Optional[str] = ..., phone_number: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., custom_attributes: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateUserProfile(_message.Message):
    __slots__ = ("first_name", "last_name", "name", "locale", "phone_number", "metadata", "custom_attributes")
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
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    name: str
    locale: str
    phone_number: str
    metadata: _containers.ScalarMap[str, str]
    custom_attributes: _containers.ScalarMap[str, str]
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., name: _Optional[str] = ..., locale: _Optional[str] = ..., phone_number: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., custom_attributes: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Invite(_message.Message):
    __slots__ = ("organization_id", "user_id", "invited_by", "status", "created_at", "expires_at", "resent_at", "resent_count")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    INVITED_BY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    RESENT_AT_FIELD_NUMBER: _ClassVar[int]
    RESENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    invited_by: str
    status: str
    created_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    resent_at: _timestamp_pb2.Timestamp
    resent_count: int
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., invited_by: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., resent_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., resent_count: _Optional[int] = ...) -> None: ...

class ResendInviteRequest(_message.Message):
    __slots__ = ("organization_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class ResendInviteResponse(_message.Message):
    __slots__ = ("invite",)
    INVITE_FIELD_NUMBER: _ClassVar[int]
    invite: Invite
    def __init__(self, invite: _Optional[_Union[Invite, _Mapping]] = ...) -> None: ...

class ListUserRolesRequest(_message.Message):
    __slots__ = ("organization_id", "user_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class ListUserRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[_commons_pb2.Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[_commons_pb2.Role, _Mapping]]] = ...) -> None: ...

class AssignUserRolesRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "roles")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    roles: _containers.RepeatedCompositeFieldContainer[AssignRoleRequest]
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., roles: _Optional[_Iterable[_Union[AssignRoleRequest, _Mapping]]] = ...) -> None: ...

class AssignRoleRequest(_message.Message):
    __slots__ = ("id", "role_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    role_name: str
    def __init__(self, id: _Optional[str] = ..., role_name: _Optional[str] = ...) -> None: ...

class AssignUserRolesResponse(_message.Message):
    __slots__ = ("roles",)
    ROLES_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[_commons_pb2.Role]
    def __init__(self, roles: _Optional[_Iterable[_Union[_commons_pb2.Role, _Mapping]]] = ...) -> None: ...

class RemoveUserRoleRequest(_message.Message):
    __slots__ = ("organization_id", "user_id", "role_name")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    role_name: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., role_name: _Optional[str] = ...) -> None: ...

class ListUserPermissionsRequest(_message.Message):
    __slots__ = ("organization_id", "user_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    user_id: str
    def __init__(self, organization_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class Permission(_message.Message):
    __slots__ = ("id", "name", "display_name", "description", "tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    display_name: str
    description: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class ListUserPermissionsResponse(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

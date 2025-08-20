from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class Feature(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEATURE_UNSPECIFIED: _ClassVar[Feature]
    UNSPECIFIED: _ClassVar[Feature]
    dir_sync: _ClassVar[Feature]
    sso: _ClassVar[Feature]
FEATURE_UNSPECIFIED: Feature
UNSPECIFIED: Feature
dir_sync: Feature
sso: Feature

class CreateOrganizationRequest(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: CreateOrganization
    def __init__(self, organization: _Optional[_Union[CreateOrganization, _Mapping]] = ...) -> None: ...

class CreateOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class CreateOrganization(_message.Message):
    __slots__ = ("display_name", "region_code", "external_id", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_CODE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    region_code: _commons_pb2.RegionCode
    external_id: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, display_name: _Optional[str] = ..., region_code: _Optional[_Union[_commons_pb2.RegionCode, str]] = ..., external_id: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Organization(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "display_name", "region_code", "external_id", "metadata", "settings")
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
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_CODE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    display_name: str
    region_code: _commons_pb2.RegionCode
    external_id: str
    metadata: _containers.ScalarMap[str, str]
    settings: OrganizationSettings
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., display_name: _Optional[str] = ..., region_code: _Optional[_Union[_commons_pb2.RegionCode, str]] = ..., external_id: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ..., settings: _Optional[_Union[OrganizationSettings, _Mapping]] = ...) -> None: ...

class UpdateOrganizationRequest(_message.Message):
    __slots__ = ("id", "external_id", "organization", "update_mask")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    organization: UpdateOrganization
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ..., organization: _Optional[_Union[UpdateOrganization, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateOrganization(_message.Message):
    __slots__ = ("display_name", "external_id", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    external_id: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, display_name: _Optional[str] = ..., external_id: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class GetOrganizationRequest(_message.Message):
    __slots__ = ("id", "external_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ...) -> None: ...

class GetOrganizationResponse(_message.Message):
    __slots__ = ("organization",)
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    organization: Organization
    def __init__(self, organization: _Optional[_Union[Organization, _Mapping]] = ...) -> None: ...

class ListOrganizationsRequest(_message.Message):
    __slots__ = ("page_size", "page_token", "external_id")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    external_id: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., external_id: _Optional[str] = ...) -> None: ...

class ListOrganizationsResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "organizations", "prev_page_token")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    organizations: _containers.RepeatedCompositeFieldContainer[Organization]
    prev_page_token: str
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., organizations: _Optional[_Iterable[_Union[Organization, _Mapping]]] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class SearchOrganizationsRequest(_message.Message):
    __slots__ = ("query", "page_size", "page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_size: int
    page_token: str
    def __init__(self, query: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class SearchOrganizationsResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "organizations", "prev_page_token")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    organizations: _containers.RepeatedCompositeFieldContainer[Organization]
    prev_page_token: str
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., organizations: _Optional[_Iterable[_Union[Organization, _Mapping]]] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class DeleteOrganizationRequest(_message.Message):
    __slots__ = ("id", "external_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ...) -> None: ...

class GeneratePortalLinkRequest(_message.Message):
    __slots__ = ("id", "sso", "directory_sync", "features")
    ID_FIELD_NUMBER: _ClassVar[int]
    SSO_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_SYNC_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    id: str
    sso: bool
    directory_sync: bool
    features: _containers.RepeatedScalarFieldContainer[Feature]
    def __init__(self, id: _Optional[str] = ..., sso: bool = ..., directory_sync: bool = ..., features: _Optional[_Iterable[_Union[Feature, str]]] = ...) -> None: ...

class GetPortalLinkRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePortalLinkRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePortalLinkByIdRequest(_message.Message):
    __slots__ = ("id", "link_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    LINK_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    link_id: str
    def __init__(self, id: _Optional[str] = ..., link_id: _Optional[str] = ...) -> None: ...

class Link(_message.Message):
    __slots__ = ("id", "location", "expire_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    location: str
    expire_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., location: _Optional[str] = ..., expire_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GeneratePortalLinkResponse(_message.Message):
    __slots__ = ("link",)
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: Link
    def __init__(self, link: _Optional[_Union[Link, _Mapping]] = ...) -> None: ...

class GetPortalLinksResponse(_message.Message):
    __slots__ = ("links",)
    LINKS_FIELD_NUMBER: _ClassVar[int]
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

class UpdateOrganizationSettingsRequest(_message.Message):
    __slots__ = ("id", "settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    settings: OrganizationSettings
    def __init__(self, id: _Optional[str] = ..., settings: _Optional[_Union[OrganizationSettings, _Mapping]] = ...) -> None: ...

class UpdateOrganizationSessionSettingsRequest(_message.Message):
    __slots__ = ("id", "environment_id", "session_settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    session_settings: OrganizationSessionSettings
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., session_settings: _Optional[_Union[OrganizationSessionSettings, _Mapping]] = ...) -> None: ...

class UpdateOrganizationSessionSettingsResponse(_message.Message):
    __slots__ = ("environment_id", "organization_id", "session_settings")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    organization_id: str
    session_settings: OrganizationSessionSettings
    def __init__(self, environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., session_settings: _Optional[_Union[OrganizationSessionSettings, _Mapping]] = ...) -> None: ...

class OrganizationUserManagementSettings(_message.Message):
    __slots__ = ("jit_provisioning_with_sso_enabled", "sync_user_profile_on_signin", "deprecated_placeholder")
    JIT_PROVISIONING_WITH_SSO_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SYNC_USER_PROFILE_ON_SIGNIN_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_PLACEHOLDER_FIELD_NUMBER: _ClassVar[int]
    jit_provisioning_with_sso_enabled: _wrappers_pb2.BoolValue
    sync_user_profile_on_signin: _wrappers_pb2.BoolValue
    deprecated_placeholder: _struct_pb2.NullValue
    def __init__(self, jit_provisioning_with_sso_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., sync_user_profile_on_signin: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., deprecated_placeholder: _Optional[_Union[_struct_pb2.NullValue, str]] = ...) -> None: ...

class OrganizationSessionSettings(_message.Message):
    __slots__ = ("absolute_session_timeout", "session_management_enabled", "idle_session_timeout", "idle_session_enabled")
    ABSOLUTE_SESSION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SESSION_MANAGEMENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IDLE_SESSION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    IDLE_SESSION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    absolute_session_timeout: _wrappers_pb2.Int32Value
    session_management_enabled: _wrappers_pb2.BoolValue
    idle_session_timeout: _wrappers_pb2.Int32Value
    idle_session_enabled: _wrappers_pb2.BoolValue
    def __init__(self, absolute_session_timeout: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., session_management_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., idle_session_timeout: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., idle_session_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class GetOrganizationSessionSettingsRequest(_message.Message):
    __slots__ = ("id", "environment_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ...) -> None: ...

class CreateOrganizationSessionSettingsRequest(_message.Message):
    __slots__ = ("id", "environment_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ...) -> None: ...

class CreateOrganizationSessionSettingsResponse(_message.Message):
    __slots__ = ("environment_id", "organization_id", "session_settings")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    organization_id: str
    session_settings: OrganizationSessionSettings
    def __init__(self, environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., session_settings: _Optional[_Union[OrganizationSessionSettings, _Mapping]] = ...) -> None: ...

class GetOrganizationSessionSettingsResponse(_message.Message):
    __slots__ = ("environment_id", "organization_id", "session_settings")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    organization_id: str
    session_settings: OrganizationSessionSettings
    def __init__(self, environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., session_settings: _Optional[_Union[OrganizationSessionSettings, _Mapping]] = ...) -> None: ...

class DeleteOrganizationSessionSettingsRequest(_message.Message):
    __slots__ = ("id", "environment_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ...) -> None: ...

class OrganizationSettings(_message.Message):
    __slots__ = ("features",)
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[OrganizationSettingsFeature]
    def __init__(self, features: _Optional[_Iterable[_Union[OrganizationSettingsFeature, _Mapping]]] = ...) -> None: ...

class OrganizationSettingsFeature(_message.Message):
    __slots__ = ("name", "enabled")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    name: str
    enabled: bool
    def __init__(self, name: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class UpdateUserManagementSettingsRequest(_message.Message):
    __slots__ = ("organization_id", "settings")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    settings: OrganizationUserManagementSettings
    def __init__(self, organization_id: _Optional[str] = ..., settings: _Optional[_Union[OrganizationUserManagementSettings, _Mapping]] = ...) -> None: ...

class UpdateUserManagementSettingsResponse(_message.Message):
    __slots__ = ("settings",)
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    settings: OrganizationUserManagementSettings
    def __init__(self, settings: _Optional[_Union[OrganizationUserManagementSettings, _Mapping]] = ...) -> None: ...

class GetOrganizationUserManagementSettingsRequest(_message.Message):
    __slots__ = ("organization_id",)
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    def __init__(self, organization_id: _Optional[str] = ...) -> None: ...

class GetOrganizationUserManagementSettingsResponse(_message.Message):
    __slots__ = ("settings",)
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    settings: OrganizationUserManagementSettings
    def __init__(self, settings: _Optional[_Union[OrganizationUserManagementSettings, _Mapping]] = ...) -> None: ...

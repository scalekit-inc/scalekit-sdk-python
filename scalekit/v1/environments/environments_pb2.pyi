from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CustomDomainStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[CustomDomainStatus]
    PENDING: _ClassVar[CustomDomainStatus]
    ACTIVE: _ClassVar[CustomDomainStatus]
    FAILED: _ClassVar[CustomDomainStatus]
    INITIAL: _ClassVar[CustomDomainStatus]

class AssetCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_CATEGORY_UNSPECIFIED: _ClassVar[AssetCategory]
    PORTAL_CUSTOMIZATION_IMAGE: _ClassVar[AssetCategory]

class OrgUserRelationshipType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OrgUserRelationshipType_UNSPECIFIED: _ClassVar[OrgUserRelationshipType]
    SINGLE_ORGANIZATION: _ClassVar[OrgUserRelationshipType]
    MULTIPLE_ORGANIZATIONS: _ClassVar[OrgUserRelationshipType]

class CookiePersistenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CookiePersistenceType_UNSPECIFIED: _ClassVar[CookiePersistenceType]
    PERSISTENT: _ClassVar[CookiePersistenceType]
    SESSION: _ClassVar[CookiePersistenceType]

class CookieSameSiteSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CookieSameSiteSetting_UNSPECIFIED: _ClassVar[CookieSameSiteSetting]
    LAX_MODE: _ClassVar[CookieSameSiteSetting]
    NONE_MODE: _ClassVar[CookieSameSiteSetting]
UNSPECIFIED: CustomDomainStatus
PENDING: CustomDomainStatus
ACTIVE: CustomDomainStatus
FAILED: CustomDomainStatus
INITIAL: CustomDomainStatus
ASSET_CATEGORY_UNSPECIFIED: AssetCategory
PORTAL_CUSTOMIZATION_IMAGE: AssetCategory
OrgUserRelationshipType_UNSPECIFIED: OrgUserRelationshipType
SINGLE_ORGANIZATION: OrgUserRelationshipType
MULTIPLE_ORGANIZATIONS: OrgUserRelationshipType
CookiePersistenceType_UNSPECIFIED: CookiePersistenceType
PERSISTENT: CookiePersistenceType
SESSION: CookiePersistenceType
CookieSameSiteSetting_UNSPECIFIED: CookieSameSiteSetting
LAX_MODE: CookieSameSiteSetting
NONE_MODE: CookieSameSiteSetting

class CreateCustomDomainRequest(_message.Message):
    __slots__ = ("id", "custom_domain")
    ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    custom_domain: str
    def __init__(self, id: _Optional[str] = ..., custom_domain: _Optional[str] = ...) -> None: ...

class CreateCustomDomainResponse(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    def __init__(self, environment: _Optional[_Union[Environment, _Mapping]] = ...) -> None: ...

class GetDNSRecordsRequest(_message.Message):
    __slots__ = ("id", "custom_domain")
    ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    custom_domain: str
    def __init__(self, id: _Optional[str] = ..., custom_domain: _Optional[str] = ...) -> None: ...

class GetDNSRecordsResponse(_message.Message):
    __slots__ = ("dns_records",)
    DNS_RECORDS_FIELD_NUMBER: _ClassVar[int]
    dns_records: _containers.RepeatedCompositeFieldContainer[DNSRecords]
    def __init__(self, dns_records: _Optional[_Iterable[_Union[DNSRecords, _Mapping]]] = ...) -> None: ...

class DNSRecords(_message.Message):
    __slots__ = ("host_name", "type", "value")
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    host_name: str
    type: str
    value: str
    def __init__(self, host_name: _Optional[str] = ..., type: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class Environment(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "display_name", "domain", "region_code", "type", "custom_domain", "custom_domain_status")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    REGION_CODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DOMAIN_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    display_name: str
    domain: str
    region_code: _commons_pb2.RegionCode
    type: _commons_pb2.EnvironmentType
    custom_domain: str
    custom_domain_status: CustomDomainStatus
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., display_name: _Optional[str] = ..., domain: _Optional[str] = ..., region_code: _Optional[_Union[_commons_pb2.RegionCode, str]] = ..., type: _Optional[_Union[_commons_pb2.EnvironmentType, str]] = ..., custom_domain: _Optional[str] = ..., custom_domain_status: _Optional[_Union[CustomDomainStatus, str]] = ...) -> None: ...

class CreateEnvironment(_message.Message):
    __slots__ = ("display_name", "region_code", "type")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_CODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    region_code: _commons_pb2.RegionCode
    type: _commons_pb2.EnvironmentType
    def __init__(self, display_name: _Optional[str] = ..., region_code: _Optional[_Union[_commons_pb2.RegionCode, str]] = ..., type: _Optional[_Union[_commons_pb2.EnvironmentType, str]] = ...) -> None: ...

class UpdateEnvironment(_message.Message):
    __slots__ = ("display_name",)
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    def __init__(self, display_name: _Optional[str] = ...) -> None: ...

class UpdateEnvironmentDomain(_message.Message):
    __slots__ = ("domain",)
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: str
    def __init__(self, domain: _Optional[str] = ...) -> None: ...

class CreateEnvironmentRequest(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: CreateEnvironment
    def __init__(self, environment: _Optional[_Union[CreateEnvironment, _Mapping]] = ...) -> None: ...

class CreateEnvironmentResponse(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    def __init__(self, environment: _Optional[_Union[Environment, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentRequest(_message.Message):
    __slots__ = ("id", "environment")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment: UpdateEnvironment
    def __init__(self, id: _Optional[str] = ..., environment: _Optional[_Union[UpdateEnvironment, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentDomainRequest(_message.Message):
    __slots__ = ("id", "environment")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment: UpdateEnvironmentDomain
    def __init__(self, id: _Optional[str] = ..., environment: _Optional[_Union[UpdateEnvironmentDomain, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentResponse(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    def __init__(self, environment: _Optional[_Union[Environment, _Mapping]] = ...) -> None: ...

class GetEnvironmentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetEnvironmentResponse(_message.Message):
    __slots__ = ("environment",)
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    environment: Environment
    def __init__(self, environment: _Optional[_Union[Environment, _Mapping]] = ...) -> None: ...

class ListEnvironmentsRequest(_message.Message):
    __slots__ = ("page_size", "page_token")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListEnvironmentsResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "environments")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    environments: _containers.RepeatedCompositeFieldContainer[Environment]
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., environments: _Optional[_Iterable[_Union[Environment, _Mapping]]] = ...) -> None: ...

class DeleteEnvironmentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GenerateSamlCertificateRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GenerateSamlCertificateResponse(_message.Message):
    __slots__ = ("id", "certificate", "expiry")
    ID_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    id: str
    certificate: str
    expiry: int
    def __init__(self, id: _Optional[str] = ..., certificate: _Optional[str] = ..., expiry: _Optional[int] = ...) -> None: ...

class UpdatePortalCustomizationResponse(_message.Message):
    __slots__ = ("environmentId", "customization_settings")
    ENVIRONMENTID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMIZATION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    environmentId: str
    customization_settings: _struct_pb2.Struct
    def __init__(self, environmentId: _Optional[str] = ..., customization_settings: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class UpdatePortalCustomizationRequest(_message.Message):
    __slots__ = ("id", "customization_settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMIZATION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    customization_settings: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., customization_settings: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetPortalCustomizationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetPortalCustomizationResponse(_message.Message):
    __slots__ = ("environmentId", "customization_settings")
    ENVIRONMENTID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMIZATION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    environmentId: str
    customization_settings: _struct_pb2.Struct
    def __init__(self, environmentId: _Optional[str] = ..., customization_settings: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CreateAssetUploadUrlResponse(_message.Message):
    __slots__ = ("upload_url", "fetch_url")
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    FETCH_URL_FIELD_NUMBER: _ClassVar[int]
    upload_url: str
    fetch_url: str
    def __init__(self, upload_url: _Optional[str] = ..., fetch_url: _Optional[str] = ...) -> None: ...

class CreateAssetUploadUrlRequest(_message.Message):
    __slots__ = ("id", "asset_settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    ASSET_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    asset_settings: AssetSettings
    def __init__(self, id: _Optional[str] = ..., asset_settings: _Optional[_Union[AssetSettings, _Mapping]] = ...) -> None: ...

class AssetSettings(_message.Message):
    __slots__ = ("category", "extension")
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    category: AssetCategory
    extension: str
    def __init__(self, category: _Optional[_Union[AssetCategory, str]] = ..., extension: _Optional[str] = ...) -> None: ...

class UpdateFeaturesRequest(_message.Message):
    __slots__ = ("id", "features")
    ID_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    id: str
    features: _containers.RepeatedCompositeFieldContainer[EnvironmentFeature]
    def __init__(self, id: _Optional[str] = ..., features: _Optional[_Iterable[_Union[EnvironmentFeature, _Mapping]]] = ...) -> None: ...

class EnableFSAFeatureRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetFeaturesRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetFeaturesResponse(_message.Message):
    __slots__ = ("features",)
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[EnvironmentFeature]
    def __init__(self, features: _Optional[_Iterable[_Union[EnvironmentFeature, _Mapping]]] = ...) -> None: ...

class EnableFeatureRequest(_message.Message):
    __slots__ = ("id", "feature_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    feature_id: str
    def __init__(self, id: _Optional[str] = ..., feature_id: _Optional[str] = ...) -> None: ...

class DisableFeatureRequest(_message.Message):
    __slots__ = ("id", "feature_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    feature_id: str
    def __init__(self, id: _Optional[str] = ..., feature_id: _Optional[str] = ...) -> None: ...

class EnvironmentFeature(_message.Message):
    __slots__ = ("name", "enabled")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    name: str
    enabled: bool
    def __init__(self, name: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class GetEnvironmentSessionSettingsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetEnvironmentUserManagementRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetEnvironmentSessionSettingsResponse(_message.Message):
    __slots__ = ("session_settings",)
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    session_settings: SessionSettings
    def __init__(self, session_settings: _Optional[_Union[SessionSettings, _Mapping]] = ...) -> None: ...

class GetEnvironmentUserManagementResponse(_message.Message):
    __slots__ = ("user_management",)
    USER_MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    user_management: UserManagement
    def __init__(self, user_management: _Optional[_Union[UserManagement, _Mapping]] = ...) -> None: ...

class CreateEnvironmentSessionSettingsRequest(_message.Message):
    __slots__ = ("id", "session_settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    session_settings: SessionSettings
    def __init__(self, id: _Optional[str] = ..., session_settings: _Optional[_Union[SessionSettings, _Mapping]] = ...) -> None: ...

class CreateEnvironmentUserManagementRequest(_message.Message):
    __slots__ = ("id", "user_management")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_management: UserManagement
    def __init__(self, id: _Optional[str] = ..., user_management: _Optional[_Union[UserManagement, _Mapping]] = ...) -> None: ...

class CreateEnvironmentSessionSettingsResponse(_message.Message):
    __slots__ = ("environment_id", "session_settings")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    session_settings: SessionSettings
    def __init__(self, environment_id: _Optional[str] = ..., session_settings: _Optional[_Union[SessionSettings, _Mapping]] = ...) -> None: ...

class CreateEnvironmentUserManagementResponse(_message.Message):
    __slots__ = ("environment_id", "user_management")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    user_management: UserManagement
    def __init__(self, environment_id: _Optional[str] = ..., user_management: _Optional[_Union[UserManagement, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentSessionSettingsRequest(_message.Message):
    __slots__ = ("id", "session_settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    session_settings: SessionSettings
    def __init__(self, id: _Optional[str] = ..., session_settings: _Optional[_Union[SessionSettings, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentUserManagementRequest(_message.Message):
    __slots__ = ("id", "user_management")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_management: UserManagement
    def __init__(self, id: _Optional[str] = ..., user_management: _Optional[_Union[UserManagement, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentSessionSettingsResponse(_message.Message):
    __slots__ = ("environment_id", "session_settings")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    session_settings: SessionSettings
    def __init__(self, environment_id: _Optional[str] = ..., session_settings: _Optional[_Union[SessionSettings, _Mapping]] = ...) -> None: ...

class UpdateEnvironmentUserManagementResponse(_message.Message):
    __slots__ = ("environment_id", "user_management")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    user_management: UserManagement
    def __init__(self, environment_id: _Optional[str] = ..., user_management: _Optional[_Union[UserManagement, _Mapping]] = ...) -> None: ...

class SessionSettings(_message.Message):
    __slots__ = ("access_token_expiry", "client_access_token_expiry", "absolute_session_timeout", "session_management_enabled", "idle_session_timeout", "idle_session_enabled", "cookie_persistence_type", "cookie_same_site_setting", "cookie_custom_domain")
    ACCESS_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ACCESS_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_SESSION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SESSION_MANAGEMENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IDLE_SESSION_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    IDLE_SESSION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COOKIE_PERSISTENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    COOKIE_SAME_SITE_SETTING_FIELD_NUMBER: _ClassVar[int]
    COOKIE_CUSTOM_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    access_token_expiry: _wrappers_pb2.Int32Value
    client_access_token_expiry: _wrappers_pb2.Int32Value
    absolute_session_timeout: _wrappers_pb2.Int32Value
    session_management_enabled: _wrappers_pb2.BoolValue
    idle_session_timeout: _wrappers_pb2.Int32Value
    idle_session_enabled: _wrappers_pb2.BoolValue
    cookie_persistence_type: CookiePersistenceType
    cookie_same_site_setting: CookieSameSiteSetting
    cookie_custom_domain: _wrappers_pb2.StringValue
    def __init__(self, access_token_expiry: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., client_access_token_expiry: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., absolute_session_timeout: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., session_management_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., idle_session_timeout: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., idle_session_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., cookie_persistence_type: _Optional[_Union[CookiePersistenceType, str]] = ..., cookie_same_site_setting: _Optional[_Union[CookieSameSiteSetting, str]] = ..., cookie_custom_domain: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class UserManagement(_message.Message):
    __slots__ = ("allow_duplicate_user_identities", "allow_multiple_memberships", "allow_organization_signup", "org_user_relationship", "enable_max_users_limit", "max_users_limit", "invitation_expiry", "organization_meta_name")
    ALLOW_DUPLICATE_USER_IDENTITIES_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MULTIPLE_MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_ORGANIZATION_SIGNUP_FIELD_NUMBER: _ClassVar[int]
    ORG_USER_RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    ENABLE_MAX_USERS_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAX_USERS_LIMIT_FIELD_NUMBER: _ClassVar[int]
    INVITATION_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_META_NAME_FIELD_NUMBER: _ClassVar[int]
    allow_duplicate_user_identities: _wrappers_pb2.BoolValue
    allow_multiple_memberships: _wrappers_pb2.BoolValue
    allow_organization_signup: _wrappers_pb2.BoolValue
    org_user_relationship: OrgUserRelationshipType
    enable_max_users_limit: _wrappers_pb2.BoolValue
    max_users_limit: _wrappers_pb2.Int32Value
    invitation_expiry: _wrappers_pb2.UInt32Value
    organization_meta_name: _wrappers_pb2.StringValue
    def __init__(self, allow_duplicate_user_identities: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., allow_multiple_memberships: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., allow_organization_signup: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., org_user_relationship: _Optional[_Union[OrgUserRelationshipType, str]] = ..., enable_max_users_limit: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., max_users_limit: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., invitation_expiry: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., organization_meta_name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class GetContextRequest(_message.Message):
    __slots__ = ("environment_id",)
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    def __init__(self, environment_id: _Optional[str] = ...) -> None: ...

class GetContextResponse(_message.Message):
    __slots__ = ("context",)
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    context: _struct_pb2.Struct
    def __init__(self, context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class UpdateContextRequest(_message.Message):
    __slots__ = ("environment_id", "context")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    context: _struct_pb2.Struct
    def __init__(self, environment_id: _Optional[str] = ..., context: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetCurrentSessionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCurrentSessionResponse(_message.Message):
    __slots__ = ("session_expiry", "access_token_expiry", "organization_id", "subject", "email")
    SESSION_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    session_expiry: _timestamp_pb2.Timestamp
    access_token_expiry: _timestamp_pb2.Timestamp
    organization_id: str
    subject: str
    email: str
    def __init__(self, session_expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., access_token_expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., organization_id: _Optional[str] = ..., subject: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class ResourceMetadata(_message.Message):
    __slots__ = ("type", "identifiers")
    class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        organization: _ClassVar[ResourceMetadata.ResourceType]
        connection: _ClassVar[ResourceMetadata.ResourceType]
        auth_request: _ClassVar[ResourceMetadata.ResourceType]
    organization: ResourceMetadata.ResourceType
    connection: ResourceMetadata.ResourceType
    auth_request: ResourceMetadata.ResourceType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    type: ResourceMetadata.ResourceType
    identifiers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[_Union[ResourceMetadata.ResourceType, str]] = ..., identifiers: _Optional[_Iterable[str]] = ...) -> None: ...

class ScalekitResourceRequest(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[ResourceMetadata]
    def __init__(self, resources: _Optional[_Iterable[_Union[ResourceMetadata, _Mapping]]] = ...) -> None: ...

class ScalekitResourceResponse(_message.Message):
    __slots__ = ("resources",)
    class ResourcesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Struct
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.MessageMap[str, _struct_pb2.Struct]
    def __init__(self, resources: _Optional[_Mapping[str, _struct_pb2.Struct]] = ...) -> None: ...

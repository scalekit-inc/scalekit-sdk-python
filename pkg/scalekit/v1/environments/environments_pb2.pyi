from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class AssetCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ASSET_CATEGORY_UNSPECIFIED: _ClassVar[AssetCategory]
    PORTAL_CUSTOMIZATION_IMAGE: _ClassVar[AssetCategory]
UNSPECIFIED: CustomDomainStatus
PENDING: CustomDomainStatus
ACTIVE: CustomDomainStatus
FAILED: CustomDomainStatus
ASSET_CATEGORY_UNSPECIFIED: AssetCategory
PORTAL_CUSTOMIZATION_IMAGE: AssetCategory

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

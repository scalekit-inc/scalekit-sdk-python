from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VerificationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VERIFICATION_STATUS_UNSPECIFIED: _ClassVar[VerificationStatus]
    PENDING: _ClassVar[VerificationStatus]
    VERIFIED: _ClassVar[VerificationStatus]
    FAILED: _ClassVar[VerificationStatus]
    AUTO_VERIFIED: _ClassVar[VerificationStatus]

class DomainType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOMAIN_TYPE_UNSPECIFIED: _ClassVar[DomainType]
    ALLOWED_EMAIL_DOMAIN: _ClassVar[DomainType]
    ORGANIZATION_DOMAIN: _ClassVar[DomainType]
VERIFICATION_STATUS_UNSPECIFIED: VerificationStatus
PENDING: VerificationStatus
VERIFIED: VerificationStatus
FAILED: VerificationStatus
AUTO_VERIFIED: VerificationStatus
DOMAIN_TYPE_UNSPECIFIED: DomainType
ALLOWED_EMAIL_DOMAIN: DomainType
ORGANIZATION_DOMAIN: DomainType

class CreateDomainRequest(_message.Message):
    __slots__ = ("organization_id", "external_id", "connection_id", "domain")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    external_id: str
    connection_id: str
    domain: CreateDomain
    def __init__(self, organization_id: _Optional[str] = ..., external_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., domain: _Optional[_Union[CreateDomain, _Mapping]] = ...) -> None: ...

class CreateDomainResponse(_message.Message):
    __slots__ = ("domain",)
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: Domain
    def __init__(self, domain: _Optional[_Union[Domain, _Mapping]] = ...) -> None: ...

class CreateDomain(_message.Message):
    __slots__ = ("domain", "domain_type")
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    domain: str
    domain_type: DomainType
    def __init__(self, domain: _Optional[str] = ..., domain_type: _Optional[_Union[DomainType, str]] = ...) -> None: ...

class UpdateDomainRequest(_message.Message):
    __slots__ = ("organization_id", "external_id", "connection_id", "id", "domain")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    external_id: str
    connection_id: str
    id: str
    domain: UpdateDomain
    def __init__(self, organization_id: _Optional[str] = ..., external_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., id: _Optional[str] = ..., domain: _Optional[_Union[UpdateDomain, _Mapping]] = ...) -> None: ...

class UpdateDomain(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateDomainResponse(_message.Message):
    __slots__ = ("domain",)
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: Domain
    def __init__(self, domain: _Optional[_Union[Domain, _Mapping]] = ...) -> None: ...

class GetDomainRequest(_message.Message):
    __slots__ = ("organization_id", "external_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    external_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., external_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetDomainResponse(_message.Message):
    __slots__ = ("domain",)
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: Domain
    def __init__(self, domain: _Optional[_Union[Domain, _Mapping]] = ...) -> None: ...

class DeleteDomainRequest(_message.Message):
    __slots__ = ("id", "organization_id", "external_id", "connection_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    organization_id: str
    external_id: str
    connection_id: str
    def __init__(self, id: _Optional[str] = ..., organization_id: _Optional[str] = ..., external_id: _Optional[str] = ..., connection_id: _Optional[str] = ...) -> None: ...

class ListDomainRequest(_message.Message):
    __slots__ = ("organization_id", "external_id", "connection_id", "include", "page_size", "page_number", "domain_type")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    external_id: str
    connection_id: str
    include: str
    page_size: _wrappers_pb2.Int32Value
    page_number: _wrappers_pb2.Int32Value
    domain_type: DomainType
    def __init__(self, organization_id: _Optional[str] = ..., external_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., include: _Optional[str] = ..., page_size: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., page_number: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., domain_type: _Optional[_Union[DomainType, str]] = ...) -> None: ...

class VerifyDomainRequest(_message.Message):
    __slots__ = ("organization_id", "external_id", "id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    external_id: str
    id: str
    def __init__(self, organization_id: _Optional[str] = ..., external_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class ListDomainResponse(_message.Message):
    __slots__ = ("page_size", "page_number", "domains")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_number: int
    domains: _containers.RepeatedCompositeFieldContainer[Domain]
    def __init__(self, page_size: _Optional[int] = ..., page_number: _Optional[int] = ..., domains: _Optional[_Iterable[_Union[Domain, _Mapping]]] = ...) -> None: ...

class ListAuthorizedDomainRequest(_message.Message):
    __slots__ = ("origin",)
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    origin: str
    def __init__(self, origin: _Optional[str] = ...) -> None: ...

class ListAuthorizedDomainResponse(_message.Message):
    __slots__ = ("domains",)
    DOMAINS_FIELD_NUMBER: _ClassVar[int]
    domains: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, domains: _Optional[_Iterable[str]] = ...) -> None: ...

class Domain(_message.Message):
    __slots__ = ("id", "domain", "environment_id", "organization_id", "connection_id", "txt_record_key", "txt_record_secret", "verification_status", "create_time", "update_time", "created_by", "domain_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TXT_RECORD_KEY_FIELD_NUMBER: _ClassVar[int]
    TXT_RECORD_SECRET_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    domain: str
    environment_id: str
    organization_id: str
    connection_id: str
    txt_record_key: str
    txt_record_secret: str
    verification_status: VerificationStatus
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    created_by: str
    domain_type: DomainType
    def __init__(self, id: _Optional[str] = ..., domain: _Optional[str] = ..., environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., txt_record_key: _Optional[str] = ..., txt_record_secret: _Optional[str] = ..., verification_status: _Optional[_Union[VerificationStatus, str]] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[str] = ..., domain_type: _Optional[_Union[DomainType, str]] = ...) -> None: ...

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventActor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTOR_UNSPECIFIED: _ClassVar[EventActor]
    HUMAN: _ClassVar[EventActor]
    MACHINE: _ClassVar[EventActor]
    API: _ClassVar[EventActor]

class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOURCE_UNSPECIFIED: _ClassVar[Source]
    SCALEKIT: _ClassVar[Source]
    DIR_SYNC: _ClassVar[Source]

class EventTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVENT_TARGET_UNSPECIFIED: _ClassVar[EventTarget]
    WORKSPACE: _ClassVar[EventTarget]
    ENVIRONMENT: _ClassVar[EventTarget]
    ORGANIZATION: _ClassVar[EventTarget]
    USER: _ClassVar[EventTarget]
    SESSION: _ClassVar[EventTarget]
    TEMPLATE: _ClassVar[EventTarget]
    EMAIL_SERVER: _ClassVar[EventTarget]
    EMAIL: _ClassVar[EventTarget]

class EventCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVENT_SOURCE_UNSPECIFIED: _ClassVar[EventCategory]
    CORE: _ClassVar[EventCategory]
    SSO: _ClassVar[EventCategory]
    DIRSYNC: _ClassVar[EventCategory]

class ObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OBJECT_TYPE_UNSPECIFIED: _ClassVar[ObjectType]
    Workspace: _ClassVar[ObjectType]
    Environment: _ClassVar[ObjectType]
    Organization: _ClassVar[ObjectType]
    Connection: _ClassVar[ObjectType]
    User: _ClassVar[ObjectType]
    Role: _ClassVar[ObjectType]
    CustomAttributes: _ClassVar[ObjectType]
    Directory: _ClassVar[ObjectType]
    DirectoryUser: _ClassVar[ObjectType]
    DirectoryGroup: _ClassVar[ObjectType]
    Session: _ClassVar[ObjectType]
    Template: _ClassVar[ObjectType]
    Job: _ClassVar[ObjectType]
    Domain: _ClassVar[ObjectType]
    EmailServer: _ClassVar[ObjectType]
    Email: _ClassVar[ObjectType]
    AuthRequest: _ClassVar[ObjectType]
    SAMLRequest: _ClassVar[ObjectType]
    SAMLResponse: _ClassVar[ObjectType]
    TokenClaims: _ClassVar[ObjectType]
    OIDCReqParams: _ClassVar[ObjectType]
    OIDCRespClaims: _ClassVar[ObjectType]
    SSOError: _ClassVar[ObjectType]
    GenericError: _ClassVar[ObjectType]
    RefreshTokens: _ClassVar[ObjectType]
    EndSessionRequest: _ClassVar[ObjectType]
    LogoutTokenClaims: _ClassVar[ObjectType]
    OAuthResponse: _ClassVar[ObjectType]
    JSON: _ClassVar[ObjectType]
    SKErrors: _ClassVar[ObjectType]
    OrgMembership: _ClassVar[ObjectType]
    UserProfile: _ClassVar[ObjectType]
    IDPInitiatedPayload: _ClassVar[ObjectType]
    DeviceDetails: _ClassVar[ObjectType]
ACTOR_UNSPECIFIED: EventActor
HUMAN: EventActor
MACHINE: EventActor
API: EventActor
SOURCE_UNSPECIFIED: Source
SCALEKIT: Source
DIR_SYNC: Source
EVENT_TARGET_UNSPECIFIED: EventTarget
WORKSPACE: EventTarget
ENVIRONMENT: EventTarget
ORGANIZATION: EventTarget
USER: EventTarget
SESSION: EventTarget
TEMPLATE: EventTarget
EMAIL_SERVER: EventTarget
EMAIL: EventTarget
EVENT_SOURCE_UNSPECIFIED: EventCategory
CORE: EventCategory
SSO: EventCategory
DIRSYNC: EventCategory
OBJECT_TYPE_UNSPECIFIED: ObjectType
Workspace: ObjectType
Environment: ObjectType
Organization: ObjectType
Connection: ObjectType
User: ObjectType
Role: ObjectType
CustomAttributes: ObjectType
Directory: ObjectType
DirectoryUser: ObjectType
DirectoryGroup: ObjectType
Session: ObjectType
Template: ObjectType
Job: ObjectType
Domain: ObjectType
EmailServer: ObjectType
Email: ObjectType
AuthRequest: ObjectType
SAMLRequest: ObjectType
SAMLResponse: ObjectType
TokenClaims: ObjectType
OIDCReqParams: ObjectType
OIDCRespClaims: ObjectType
SSOError: ObjectType
GenericError: ObjectType
RefreshTokens: ObjectType
EndSessionRequest: ObjectType
LogoutTokenClaims: ObjectType
OAuthResponse: ObjectType
JSON: ObjectType
SKErrors: ObjectType
OrgMembership: ObjectType
UserProfile: ObjectType
IDPInitiatedPayload: ObjectType
DeviceDetails: ObjectType

class SendCustomEventRequest(_message.Message):
    __slots__ = ("event_type", "event")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event_type: str
    event: _struct_pb2.Struct
    def __init__(self, event_type: _Optional[str] = ..., event: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SendCustomEventResponse(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    def __init__(self, event_id: _Optional[str] = ...) -> None: ...

class IEventPaginationTokens(_message.Message):
    __slots__ = ("NextPage", "PreviousPage", "Total")
    NEXTPAGE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUSPAGE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    NextPage: str
    PreviousPage: str
    Total: int
    def __init__(self, NextPage: _Optional[str] = ..., PreviousPage: _Optional[str] = ..., Total: _Optional[int] = ...) -> None: ...

class ListEventsRequest(_message.Message):
    __slots__ = ("filter", "page_size", "page_token")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    filter: EventFilter
    page_size: int
    page_token: str
    def __init__(self, filter: _Optional[_Union[EventFilter, _Mapping]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListEventsResponse(_message.Message):
    __slots__ = ("events", "next_page_token", "prev_page_token", "total_size")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[ScalekitEvent]
    next_page_token: str
    prev_page_token: str
    total_size: int
    def __init__(self, events: _Optional[_Iterable[_Union[ScalekitEvent, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class IEvent(_message.Message):
    __slots__ = ("spec_version", "id", "type", "occurred_at", "actor", "tenant_id", "target", "source", "data", "old_data", "context", "metadata")
    class ContextEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SPEC_VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTOR_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    OLD_DATA_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    spec_version: str
    id: str
    type: str
    occurred_at: _timestamp_pb2.Timestamp
    actor: Actor
    tenant_id: str
    target: Target
    source: str
    data: _struct_pb2.Struct
    old_data: _struct_pb2.Struct
    context: _containers.ScalarMap[str, str]
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, spec_version: _Optional[str] = ..., id: _Optional[str] = ..., type: _Optional[str] = ..., occurred_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., actor: _Optional[_Union[Actor, _Mapping]] = ..., tenant_id: _Optional[str] = ..., target: _Optional[_Union[Target, _Mapping]] = ..., source: _Optional[str] = ..., data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., old_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., context: _Optional[_Mapping[str, str]] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("spec_version", "id", "type", "occurred_at", "actor", "tenant_id", "target", "source", "data", "old_data", "context", "metadata", "object")
    class ContextEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SPEC_VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTOR_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    OLD_DATA_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    spec_version: str
    id: str
    type: str
    occurred_at: _timestamp_pb2.Timestamp
    actor: Actor
    tenant_id: str
    target: Target
    source: str
    data: _struct_pb2.Struct
    old_data: _struct_pb2.Struct
    context: _containers.ScalarMap[str, str]
    metadata: _containers.ScalarMap[str, str]
    object: ObjectType
    def __init__(self, spec_version: _Optional[str] = ..., id: _Optional[str] = ..., type: _Optional[str] = ..., occurred_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., actor: _Optional[_Union[Actor, _Mapping]] = ..., tenant_id: _Optional[str] = ..., target: _Optional[_Union[Target, _Mapping]] = ..., source: _Optional[str] = ..., data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., old_data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., context: _Optional[_Mapping[str, str]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., object: _Optional[_Union[ObjectType, str]] = ...) -> None: ...

class Actor(_message.Message):
    __slots__ = ("id", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: EventActor
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[EventActor, str]] = ...) -> None: ...

class Target(_message.Message):
    __slots__ = ("id", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: EventTarget
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[EventTarget, str]] = ...) -> None: ...

class IEventFilter(_message.Message):
    __slots__ = ("event_types", "start_time", "end_time", "tenant_id", "target", "source", "metadata", "internal_events")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_EVENTS_FIELD_NUMBER: _ClassVar[int]
    event_types: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    tenant_id: str
    target: Target
    source: Source
    metadata: _containers.ScalarMap[str, str]
    internal_events: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, event_types: _Optional[_Iterable[str]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., tenant_id: _Optional[str] = ..., target: _Optional[_Union[Target, _Mapping]] = ..., source: _Optional[_Union[Source, str]] = ..., metadata: _Optional[_Mapping[str, str]] = ..., internal_events: _Optional[_Iterable[str]] = ...) -> None: ...

class EventFilter(_message.Message):
    __slots__ = ("event_types", "start_time", "end_time", "organization_id", "source", "auth_request_id")
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    event_types: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    organization_id: str
    source: Source
    auth_request_id: str
    def __init__(self, event_types: _Optional[_Iterable[str]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., organization_id: _Optional[str] = ..., source: _Optional[_Union[Source, str]] = ..., auth_request_id: _Optional[str] = ...) -> None: ...

class ScalekitEvent(_message.Message):
    __slots__ = ("spec_version", "id", "type", "occurred_at", "environment_id", "organization_id", "object", "data", "display_name")
    SPEC_VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    spec_version: str
    id: str
    type: str
    occurred_at: _timestamp_pb2.Timestamp
    environment_id: str
    organization_id: str
    object: ObjectType
    data: _struct_pb2.Struct
    display_name: str
    def __init__(self, spec_version: _Optional[str] = ..., id: _Optional[str] = ..., type: _Optional[str] = ..., occurred_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., object: _Optional[_Union[ObjectType, str]] = ..., data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., display_name: _Optional[str] = ...) -> None: ...

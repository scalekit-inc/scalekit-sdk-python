from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OBJECT_TYPE_UNSPECIFIED: _ClassVar[ObjectType]
    ORGANIZATION: _ClassVar[ObjectType]
    USER: _ClassVar[ObjectType]
    DIRECTORY_USER: _ClassVar[ObjectType]
    CONNECTION: _ClassVar[ObjectType]
    DIRECTORY: _ClassVar[ObjectType]

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVENT_TYPE_UNSPECIFIED: _ClassVar[EventType]
    ORGANIZATION_CREATED: _ClassVar[EventType]
    ORGANIZATION_UPDATED: _ClassVar[EventType]
    ORGANIZATION_DELETED: _ClassVar[EventType]
    USER_SIGNUP: _ClassVar[EventType]
    USER_LOGIN: _ClassVar[EventType]
    USER_LOGOUT: _ClassVar[EventType]
    USER_ORGANIZATION_INVITATION: _ClassVar[EventType]
    USER_ORGANIZATION_MEMBERSHIP_CREATED: _ClassVar[EventType]
    USER_ORGANIZATION_MEMBERSHIP_UPDATED: _ClassVar[EventType]
    USER_ORGANIZATION_MEMBERSHIP_DELETED: _ClassVar[EventType]
OBJECT_TYPE_UNSPECIFIED: ObjectType
ORGANIZATION: ObjectType
USER: ObjectType
DIRECTORY_USER: ObjectType
CONNECTION: ObjectType
DIRECTORY: ObjectType
EVENT_TYPE_UNSPECIFIED: EventType
ORGANIZATION_CREATED: EventType
ORGANIZATION_UPDATED: EventType
ORGANIZATION_DELETED: EventType
USER_SIGNUP: EventType
USER_LOGIN: EventType
USER_LOGOUT: EventType
USER_ORGANIZATION_INVITATION: EventType
USER_ORGANIZATION_MEMBERSHIP_CREATED: EventType
USER_ORGANIZATION_MEMBERSHIP_UPDATED: EventType
USER_ORGANIZATION_MEMBERSHIP_DELETED: EventType

class SendTestEventRequest(_message.Message):
    __slots__ = ("event_type",)
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    event_type: str
    def __init__(self, event_type: _Optional[str] = ...) -> None: ...

class SendTestEventResponse(_message.Message):
    __slots__ = ("event_type", "event_payload")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    event_type: str
    event_payload: _struct_pb2.Struct
    def __init__(self, event_type: _Optional[str] = ..., event_payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetPortalURLRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetPortalURLResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class WebhookWrapperRequest(_message.Message):
    __slots__ = ("request_body",)
    REQUEST_BODY_FIELD_NUMBER: _ClassVar[int]
    request_body: _struct_pb2.Struct
    def __init__(self, request_body: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class WebhookWrapperResponse(_message.Message):
    __slots__ = ("response_body",)
    RESPONSE_BODY_FIELD_NUMBER: _ClassVar[int]
    response_body: _struct_pb2.Struct
    def __init__(self, response_body: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class WebhookEvent(_message.Message):
    __slots__ = ("spec_version", "id", "object", "occurred_at", "environment_id", "organization_id", "type", "organization", "user")
    SPEC_VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    spec_version: str
    id: str
    object: ObjectType
    occurred_at: _timestamp_pb2.Timestamp
    environment_id: str
    organization_id: str
    type: EventType
    organization: OrganizationEventData
    user: UserEventData
    def __init__(self, spec_version: _Optional[str] = ..., id: _Optional[str] = ..., object: _Optional[_Union[ObjectType, str]] = ..., occurred_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., type: _Optional[_Union[EventType, str]] = ..., organization: _Optional[_Union[OrganizationEventData, _Mapping]] = ..., user: _Optional[_Union[UserEventData, _Mapping]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class OrganizationEventData(_message.Message):
    __slots__ = ("id", "external_id", "metadata", "settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    metadata: _struct_pb2.Struct
    settings: OrganizationSettings
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., settings: _Optional[_Union[OrganizationSettings, _Mapping]] = ...) -> None: ...

class OrganizationSettings(_message.Message):
    __slots__ = ("features",)
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeatureFlag]
    def __init__(self, features: _Optional[_Iterable[_Union[FeatureFlag, _Mapping]]] = ...) -> None: ...

class FeatureFlag(_message.Message):
    __slots__ = ("enabled", "name")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    name: str
    def __init__(self, enabled: bool = ..., name: _Optional[str] = ...) -> None: ...

class UserEventData(_message.Message):
    __slots__ = ("id", "email", "external_id", "profile", "created_at", "updated_at", "organization")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    external_id: str
    profile: UserProfile
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    organization: OrganizationReference
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., external_id: _Optional[str] = ..., profile: _Optional[_Union[UserProfile, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., organization: _Optional[_Union[OrganizationReference, _Mapping]] = ...) -> None: ...

class UserProfile(_message.Message):
    __slots__ = ("given_name", "family_name", "picture", "email_verified")
    GIVEN_NAME_FIELD_NUMBER: _ClassVar[int]
    FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    PICTURE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    given_name: str
    family_name: str
    picture: str
    email_verified: bool
    def __init__(self, given_name: _Optional[str] = ..., family_name: _Optional[str] = ..., picture: _Optional[str] = ..., email_verified: bool = ...) -> None: ...

class OrganizationReference(_message.Message):
    __slots__ = ("id", "external_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    external_id: str
    def __init__(self, id: _Optional[str] = ..., external_id: _Optional[str] = ...) -> None: ...

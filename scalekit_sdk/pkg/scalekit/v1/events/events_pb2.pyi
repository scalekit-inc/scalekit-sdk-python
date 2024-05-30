from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVENT_TYPE_UNSPECIFIED: _ClassVar[EventType]
    ORGANIZATION_CREATE: _ClassVar[EventType]
EVENT_TYPE_UNSPECIFIED: EventType
ORGANIZATION_CREATE: EventType

class Event(_message.Message):
    __slots__ = ("id", "type", "create_time", "actor", "trace_context", "source", "request_id", "payload", "previous_payload")
    class Actor(_message.Message):
        __slots__ = ("environment_id", "organization_id", "user_id", "user_type", "ip_addr", "user_agent")
        class UserType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            USER_TYPE_UNSPECIFIED: _ClassVar[Event.Actor.UserType]
            USER_TYPE_HUMAN: _ClassVar[Event.Actor.UserType]
            USER_TYPE_MACHINE: _ClassVar[Event.Actor.UserType]
        USER_TYPE_UNSPECIFIED: Event.Actor.UserType
        USER_TYPE_HUMAN: Event.Actor.UserType
        USER_TYPE_MACHINE: Event.Actor.UserType
        ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
        ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        USER_TYPE_FIELD_NUMBER: _ClassVar[int]
        IP_ADDR_FIELD_NUMBER: _ClassVar[int]
        USER_AGENT_FIELD_NUMBER: _ClassVar[int]
        environment_id: str
        organization_id: str
        user_id: str
        user_type: Event.Actor.UserType
        ip_addr: str
        user_agent: str
        def __init__(self, environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., user_id: _Optional[str] = ..., user_type: _Optional[_Union[Event.Actor.UserType, str]] = ..., ip_addr: _Optional[str] = ..., user_agent: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    ACTOR_FIELD_NUMBER: _ClassVar[int]
    TRACE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: EventType
    create_time: _timestamp_pb2.Timestamp
    actor: Event.Actor
    trace_context: str
    source: str
    request_id: str
    payload: _any_pb2.Any
    previous_payload: _any_pb2.Any
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[EventType, str]] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., actor: _Optional[_Union[Event.Actor, _Mapping]] = ..., trace_context: _Optional[str] = ..., source: _Optional[str] = ..., request_id: _Optional[str] = ..., payload: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., previous_payload: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

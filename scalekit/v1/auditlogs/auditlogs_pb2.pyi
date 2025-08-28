from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListAuthLogRequest(_message.Message):
    __slots__ = ("page_size", "page_token", "email", "status", "start_time", "end_time")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    email: str
    status: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., email: _Optional[str] = ..., status: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListAuthLogResponse(_message.Message):
    __slots__ = ("next_page_token", "prev_page_token", "total_size", "authRequests")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    AUTHREQUESTS_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    prev_page_token: str
    total_size: int
    authRequests: _containers.RepeatedCompositeFieldContainer[AuthLogRequest]
    def __init__(self, next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., authRequests: _Optional[_Iterable[_Union[AuthLogRequest, _Mapping]]] = ...) -> None: ...

class AuthLogRequest(_message.Message):
    __slots__ = ("organization_id", "environment_id", "connection_id", "auth_request_id", "email", "connection_type", "connection_provider", "status", "timestamp", "connection_details", "workflow")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    AUTH_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    environment_id: str
    connection_id: str
    auth_request_id: str
    email: str
    connection_type: str
    connection_provider: str
    status: str
    timestamp: _timestamp_pb2.Timestamp
    connection_details: _containers.RepeatedCompositeFieldContainer[ConnectionDetails]
    workflow: str
    def __init__(self, organization_id: _Optional[str] = ..., environment_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., auth_request_id: _Optional[str] = ..., email: _Optional[str] = ..., connection_type: _Optional[str] = ..., connection_provider: _Optional[str] = ..., status: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., connection_details: _Optional[_Iterable[_Union[ConnectionDetails, _Mapping]]] = ..., workflow: _Optional[str] = ...) -> None: ...

class ConnectionDetails(_message.Message):
    __slots__ = ("connection_id", "organization_id", "connection_type", "connection_provider")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    organization_id: str
    connection_type: str
    connection_provider: str
    def __init__(self, connection_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., connection_type: _Optional[str] = ..., connection_provider: _Optional[str] = ...) -> None: ...

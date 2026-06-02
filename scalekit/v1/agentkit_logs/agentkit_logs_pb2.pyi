from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListToolCallLogsRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "status", "provider", "connection_id", "connected_account_id", "identifier", "agent_run_id", "page_size", "page_token", "connection_name")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    AGENT_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    status: _containers.RepeatedScalarFieldContainer[str]
    provider: _containers.RepeatedScalarFieldContainer[str]
    connection_id: str
    connected_account_id: str
    identifier: str
    agent_run_id: str
    page_size: int
    page_token: str
    connection_name: str
    def __init__(self, start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Iterable[str]] = ..., provider: _Optional[_Iterable[str]] = ..., connection_id: _Optional[str] = ..., connected_account_id: _Optional[str] = ..., identifier: _Optional[str] = ..., agent_run_id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., connection_name: _Optional[str] = ...) -> None: ...

class ListToolCallLogsResponse(_message.Message):
    __slots__ = ("tool_call_logs", "next_page_token", "total_size", "prev_page_token")
    TOOL_CALL_LOGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    tool_call_logs: _containers.RepeatedCompositeFieldContainer[ToolCallLog]
    next_page_token: str
    total_size: int
    prev_page_token: str
    def __init__(self, tool_call_logs: _Optional[_Iterable[_Union[ToolCallLog, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class GetToolCallLogRequest(_message.Message):
    __slots__ = ("execution_id",)
    EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    execution_id: str
    def __init__(self, execution_id: _Optional[str] = ...) -> None: ...

class ToolCallLog(_message.Message):
    __slots__ = ("id", "environment_id", "execution_id", "agent_run_id", "tool_name", "provider", "connected_account_id", "connection_id", "connection_name", "identifier", "user_id", "organization_id", "source", "status", "error_tier", "error_code", "error_message", "duration_ms", "started_at", "workspace_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_TIER_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    execution_id: str
    agent_run_id: str
    tool_name: str
    provider: str
    connected_account_id: str
    connection_id: str
    connection_name: str
    identifier: str
    user_id: str
    organization_id: str
    source: str
    status: str
    error_tier: str
    error_code: str
    error_message: str
    duration_ms: int
    started_at: _timestamp_pb2.Timestamp
    workspace_id: str
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., execution_id: _Optional[str] = ..., agent_run_id: _Optional[str] = ..., tool_name: _Optional[str] = ..., provider: _Optional[str] = ..., connected_account_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., connection_name: _Optional[str] = ..., identifier: _Optional[str] = ..., user_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., source: _Optional[str] = ..., status: _Optional[str] = ..., error_tier: _Optional[str] = ..., error_code: _Optional[str] = ..., error_message: _Optional[str] = ..., duration_ms: _Optional[int] = ..., started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workspace_id: _Optional[str] = ...) -> None: ...

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

class GetOverviewStatsRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "provider", "status", "error_code", "connection_name")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    provider: _containers.RepeatedScalarFieldContainer[str]
    status: _containers.RepeatedScalarFieldContainer[str]
    error_code: _containers.RepeatedScalarFieldContainer[str]
    connection_name: str
    def __init__(self, start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., provider: _Optional[_Iterable[str]] = ..., status: _Optional[_Iterable[str]] = ..., error_code: _Optional[_Iterable[str]] = ..., connection_name: _Optional[str] = ...) -> None: ...

class OverviewStats(_message.Message):
    __slots__ = ("total", "success", "errors", "provider_errors", "platform_errors", "top_error_codes", "connector_breakdown", "time_series")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ERRORS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ERRORS_FIELD_NUMBER: _ClassVar[int]
    TOP_ERROR_CODES_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
    TIME_SERIES_FIELD_NUMBER: _ClassVar[int]
    total: int
    success: int
    errors: int
    provider_errors: int
    platform_errors: int
    top_error_codes: _containers.RepeatedCompositeFieldContainer[ErrorCodeCount]
    connector_breakdown: _containers.RepeatedCompositeFieldContainer[ConnectorStat]
    time_series: _containers.RepeatedCompositeFieldContainer[TimeSeriesBucket]
    def __init__(self, total: _Optional[int] = ..., success: _Optional[int] = ..., errors: _Optional[int] = ..., provider_errors: _Optional[int] = ..., platform_errors: _Optional[int] = ..., top_error_codes: _Optional[_Iterable[_Union[ErrorCodeCount, _Mapping]]] = ..., connector_breakdown: _Optional[_Iterable[_Union[ConnectorStat, _Mapping]]] = ..., time_series: _Optional[_Iterable[_Union[TimeSeriesBucket, _Mapping]]] = ...) -> None: ...

class ErrorCodeCount(_message.Message):
    __slots__ = ("error_code", "count")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    error_code: str
    count: int
    def __init__(self, error_code: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class ConnectorStat(_message.Message):
    __slots__ = ("provider", "total", "success", "errors", "provider_errors", "platform_errors")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ERRORS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ERRORS_FIELD_NUMBER: _ClassVar[int]
    provider: str
    total: int
    success: int
    errors: int
    provider_errors: int
    platform_errors: int
    def __init__(self, provider: _Optional[str] = ..., total: _Optional[int] = ..., success: _Optional[int] = ..., errors: _Optional[int] = ..., provider_errors: _Optional[int] = ..., platform_errors: _Optional[int] = ...) -> None: ...

class TimeSeriesBucket(_message.Message):
    __slots__ = ("bucket", "total", "success", "errors", "bucket_duration_seconds", "provider_errors", "platform_errors")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ERRORS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ERRORS_FIELD_NUMBER: _ClassVar[int]
    bucket: _timestamp_pb2.Timestamp
    total: int
    success: int
    errors: int
    bucket_duration_seconds: int
    provider_errors: int
    platform_errors: int
    def __init__(self, bucket: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., total: _Optional[int] = ..., success: _Optional[int] = ..., errors: _Optional[int] = ..., bucket_duration_seconds: _Optional[int] = ..., provider_errors: _Optional[int] = ..., platform_errors: _Optional[int] = ...) -> None: ...

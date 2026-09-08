from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogStreamProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOG_STREAM_PROVIDER_UNSPECIFIED: _ClassVar[LogStreamProvider]
    DATADOG: _ClassVar[LogStreamProvider]
    CROWDSTRIKE: _ClassVar[LogStreamProvider]
    GOOGLE_SECOPS: _ClassVar[LogStreamProvider]

class LogStreamStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOG_STREAM_STATUS_UNSPECIFIED: _ClassVar[LogStreamStatus]
    PENDING: _ClassVar[LogStreamStatus]
    ACTIVE: _ClassVar[LogStreamStatus]
    ERROR: _ClassVar[LogStreamStatus]
    DISABLED: _ClassVar[LogStreamStatus]

class LogStreamDeliveryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOG_STREAM_DELIVERY_STATUS_UNSPECIFIED: _ClassVar[LogStreamDeliveryStatus]
    LOG_STREAM_DELIVERY_STATUS_SUCCESS: _ClassVar[LogStreamDeliveryStatus]
    LOG_STREAM_DELIVERY_STATUS_PENDING: _ClassVar[LogStreamDeliveryStatus]
    LOG_STREAM_DELIVERY_STATUS_FAILED: _ClassVar[LogStreamDeliveryStatus]
    LOG_STREAM_DELIVERY_STATUS_SENDING: _ClassVar[LogStreamDeliveryStatus]
    LOG_STREAM_DELIVERY_STATUS_CANCELED: _ClassVar[LogStreamDeliveryStatus]
LOG_STREAM_PROVIDER_UNSPECIFIED: LogStreamProvider
DATADOG: LogStreamProvider
CROWDSTRIKE: LogStreamProvider
GOOGLE_SECOPS: LogStreamProvider
LOG_STREAM_STATUS_UNSPECIFIED: LogStreamStatus
PENDING: LogStreamStatus
ACTIVE: LogStreamStatus
ERROR: LogStreamStatus
DISABLED: LogStreamStatus
LOG_STREAM_DELIVERY_STATUS_UNSPECIFIED: LogStreamDeliveryStatus
LOG_STREAM_DELIVERY_STATUS_SUCCESS: LogStreamDeliveryStatus
LOG_STREAM_DELIVERY_STATUS_PENDING: LogStreamDeliveryStatus
LOG_STREAM_DELIVERY_STATUS_FAILED: LogStreamDeliveryStatus
LOG_STREAM_DELIVERY_STATUS_SENDING: LogStreamDeliveryStatus
LOG_STREAM_DELIVERY_STATUS_CANCELED: LogStreamDeliveryStatus

class DatadogConfig(_message.Message):
    __slots__ = ("site",)
    SITE_FIELD_NUMBER: _ClassVar[int]
    site: str
    def __init__(self, site: _Optional[str] = ...) -> None: ...

class CrowdstrikeConfig(_message.Message):
    __slots__ = ("ingest_url",)
    INGEST_URL_FIELD_NUMBER: _ClassVar[int]
    ingest_url: str
    def __init__(self, ingest_url: _Optional[str] = ...) -> None: ...

class GoogleSecopsConfig(_message.Message):
    __slots__ = ("gcp_project_id", "location", "instance_id", "log_type")
    GCP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    LOG_TYPE_FIELD_NUMBER: _ClassVar[int]
    gcp_project_id: str
    location: str
    instance_id: str
    log_type: str
    def __init__(self, gcp_project_id: _Optional[str] = ..., location: _Optional[str] = ..., instance_id: _Optional[str] = ..., log_type: _Optional[str] = ...) -> None: ...

class LogStreamConfig(_message.Message):
    __slots__ = ("datadog", "crowdstrike", "google_secops")
    DATADOG_FIELD_NUMBER: _ClassVar[int]
    CROWDSTRIKE_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_SECOPS_FIELD_NUMBER: _ClassVar[int]
    datadog: DatadogConfig
    crowdstrike: CrowdstrikeConfig
    google_secops: GoogleSecopsConfig
    def __init__(self, datadog: _Optional[_Union[DatadogConfig, _Mapping]] = ..., crowdstrike: _Optional[_Union[CrowdstrikeConfig, _Mapping]] = ..., google_secops: _Optional[_Union[GoogleSecopsConfig, _Mapping]] = ...) -> None: ...

class DatadogCredentials(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    def __init__(self, api_key: _Optional[str] = ...) -> None: ...

class CrowdstrikeCredentials(_message.Message):
    __slots__ = ("ingest_token",)
    INGEST_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ingest_token: str
    def __init__(self, ingest_token: _Optional[str] = ...) -> None: ...

class LogStreamCredentials(_message.Message):
    __slots__ = ("datadog", "crowdstrike")
    DATADOG_FIELD_NUMBER: _ClassVar[int]
    CROWDSTRIKE_FIELD_NUMBER: _ClassVar[int]
    datadog: DatadogCredentials
    crowdstrike: CrowdstrikeCredentials
    def __init__(self, datadog: _Optional[_Union[DatadogCredentials, _Mapping]] = ..., crowdstrike: _Optional[_Union[CrowdstrikeCredentials, _Mapping]] = ...) -> None: ...

class LogStream(_message.Message):
    __slots__ = ("id", "provider", "display_name", "enabled", "config", "event_types", "credential_hint", "status", "last_delivered_at", "update_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_HINT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_DELIVERED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    provider: LogStreamProvider
    display_name: str
    enabled: bool
    config: LogStreamConfig
    event_types: _containers.RepeatedScalarFieldContainer[str]
    credential_hint: str
    status: LogStreamStatus
    last_delivered_at: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., provider: _Optional[_Union[LogStreamProvider, str]] = ..., display_name: _Optional[str] = ..., enabled: bool = ..., config: _Optional[_Union[LogStreamConfig, _Mapping]] = ..., event_types: _Optional[_Iterable[str]] = ..., credential_hint: _Optional[str] = ..., status: _Optional[_Union[LogStreamStatus, str]] = ..., last_delivered_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LogStreamWrite(_message.Message):
    __slots__ = ("provider", "display_name", "enabled", "config", "credentials", "event_types")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    provider: LogStreamProvider
    display_name: str
    enabled: bool
    config: LogStreamConfig
    credentials: LogStreamCredentials
    event_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, provider: _Optional[_Union[LogStreamProvider, str]] = ..., display_name: _Optional[str] = ..., enabled: bool = ..., config: _Optional[_Union[LogStreamConfig, _Mapping]] = ..., credentials: _Optional[_Union[LogStreamCredentials, _Mapping]] = ..., event_types: _Optional[_Iterable[str]] = ...) -> None: ...

class ListLogStreamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListLogStreamsResponse(_message.Message):
    __slots__ = ("log_streams", "proxy_service_account_email")
    LOG_STREAMS_FIELD_NUMBER: _ClassVar[int]
    PROXY_SERVICE_ACCOUNT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    log_streams: _containers.RepeatedCompositeFieldContainer[LogStream]
    proxy_service_account_email: str
    def __init__(self, log_streams: _Optional[_Iterable[_Union[LogStream, _Mapping]]] = ..., proxy_service_account_email: _Optional[str] = ...) -> None: ...

class GetLogStreamRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetLogStreamResponse(_message.Message):
    __slots__ = ("log_stream",)
    LOG_STREAM_FIELD_NUMBER: _ClassVar[int]
    log_stream: LogStream
    def __init__(self, log_stream: _Optional[_Union[LogStream, _Mapping]] = ...) -> None: ...

class CreateLogStreamRequest(_message.Message):
    __slots__ = ("log_stream",)
    LOG_STREAM_FIELD_NUMBER: _ClassVar[int]
    log_stream: LogStreamWrite
    def __init__(self, log_stream: _Optional[_Union[LogStreamWrite, _Mapping]] = ...) -> None: ...

class CreateLogStreamResponse(_message.Message):
    __slots__ = ("log_stream",)
    LOG_STREAM_FIELD_NUMBER: _ClassVar[int]
    log_stream: LogStream
    def __init__(self, log_stream: _Optional[_Union[LogStream, _Mapping]] = ...) -> None: ...

class UpdateLogStreamRequest(_message.Message):
    __slots__ = ("id", "log_stream")
    ID_FIELD_NUMBER: _ClassVar[int]
    LOG_STREAM_FIELD_NUMBER: _ClassVar[int]
    id: str
    log_stream: LogStreamWrite
    def __init__(self, id: _Optional[str] = ..., log_stream: _Optional[_Union[LogStreamWrite, _Mapping]] = ...) -> None: ...

class UpdateLogStreamResponse(_message.Message):
    __slots__ = ("log_stream",)
    LOG_STREAM_FIELD_NUMBER: _ClassVar[int]
    log_stream: LogStream
    def __init__(self, log_stream: _Optional[_Union[LogStream, _Mapping]] = ...) -> None: ...

class DeleteLogStreamRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TestLogStreamConnectionRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TestLogStreamConnectionResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class LogStreamDelivery(_message.Message):
    __slots__ = ("id", "event_type", "event_id", "status", "created_at", "next_attempt_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    NEXT_ATTEMPT_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    event_type: str
    event_id: str
    status: LogStreamDeliveryStatus
    created_at: _timestamp_pb2.Timestamp
    next_attempt_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., event_type: _Optional[str] = ..., event_id: _Optional[str] = ..., status: _Optional[_Union[LogStreamDeliveryStatus, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., next_attempt_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LogStreamDeliveryAttempt(_message.Message):
    __slots__ = ("id", "status", "response_status_code", "response", "attempted_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: LogStreamDeliveryStatus
    response_status_code: int
    response: str
    attempted_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[LogStreamDeliveryStatus, str]] = ..., response_status_code: _Optional[int] = ..., response: _Optional[str] = ..., attempted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListLogStreamDeliveriesRequest(_message.Message):
    __slots__ = ("id", "page_size", "page_token", "event_types", "status", "after", "before")
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AFTER_FIELD_NUMBER: _ClassVar[int]
    BEFORE_FIELD_NUMBER: _ClassVar[int]
    id: str
    page_size: int
    page_token: str
    event_types: _containers.RepeatedScalarFieldContainer[str]
    status: LogStreamDeliveryStatus
    after: _timestamp_pb2.Timestamp
    before: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., event_types: _Optional[_Iterable[str]] = ..., status: _Optional[_Union[LogStreamDeliveryStatus, str]] = ..., after: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., before: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListLogStreamDeliveriesResponse(_message.Message):
    __slots__ = ("deliveries", "next_page_token")
    DELIVERIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    deliveries: _containers.RepeatedCompositeFieldContainer[LogStreamDelivery]
    next_page_token: str
    def __init__(self, deliveries: _Optional[_Iterable[_Union[LogStreamDelivery, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class ListLogStreamDeliveryAttemptsRequest(_message.Message):
    __slots__ = ("id", "delivery_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    delivery_id: str
    def __init__(self, id: _Optional[str] = ..., delivery_id: _Optional[str] = ...) -> None: ...

class ListLogStreamDeliveryAttemptsResponse(_message.Message):
    __slots__ = ("attempts",)
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    attempts: _containers.RepeatedCompositeFieldContainer[LogStreamDeliveryAttempt]
    def __init__(self, attempts: _Optional[_Iterable[_Union[LogStreamDeliveryAttempt, _Mapping]]] = ...) -> None: ...

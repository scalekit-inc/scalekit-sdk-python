from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SessionDetailsRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class UserSessionDetailsRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class RevokeSessionRequest(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class RevokeSessionResponse(_message.Message):
    __slots__ = ("revoked_session",)
    REVOKED_SESSION_FIELD_NUMBER: _ClassVar[int]
    revoked_session: SessionDetails
    def __init__(self, revoked_session: _Optional[_Union[SessionDetails, _Mapping]] = ...) -> None: ...

class UserSessionDetails(_message.Message):
    __slots__ = ("sessions",)
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    sessions: _containers.RepeatedCompositeFieldContainer[SessionDetails]
    def __init__(self, sessions: _Optional[_Iterable[_Union[SessionDetails, _Mapping]]] = ...) -> None: ...

class SessionDetails(_message.Message):
    __slots__ = ("session_id", "user_id", "authenticated_organizations", "organization_id", "created_at", "updated_at", "idle_expires_at", "absolute_expires_at", "expired_at", "logout_at", "status", "initial_user_agent", "initial_os", "initial_os_version", "initial_browser", "initial_browser_version", "initial_device_type", "initial_timezone", "initial_ip", "initial_location", "latest_user_agent", "latest_os", "latest_os_version", "latest_browser", "latest_browser_version", "latest_device_type", "latest_timezone", "latest_ip", "latest_location")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATED_ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IDLE_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_AT_FIELD_NUMBER: _ClassVar[int]
    LOGOUT_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    INITIAL_OS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    INITIAL_BROWSER_FIELD_NUMBER: _ClassVar[int]
    INITIAL_BROWSER_VERSION_FIELD_NUMBER: _ClassVar[int]
    INITIAL_DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_IP_FIELD_NUMBER: _ClassVar[int]
    INITIAL_LOCATION_FIELD_NUMBER: _ClassVar[int]
    LATEST_USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    LATEST_OS_FIELD_NUMBER: _ClassVar[int]
    LATEST_OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    LATEST_BROWSER_FIELD_NUMBER: _ClassVar[int]
    LATEST_BROWSER_VERSION_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LATEST_TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    LATEST_IP_FIELD_NUMBER: _ClassVar[int]
    LATEST_LOCATION_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    user_id: str
    authenticated_organizations: _containers.RepeatedScalarFieldContainer[str]
    organization_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    idle_expires_at: _timestamp_pb2.Timestamp
    absolute_expires_at: _timestamp_pb2.Timestamp
    expired_at: _timestamp_pb2.Timestamp
    logout_at: _timestamp_pb2.Timestamp
    status: str
    initial_user_agent: str
    initial_os: str
    initial_os_version: str
    initial_browser: str
    initial_browser_version: str
    initial_device_type: str
    initial_timezone: str
    initial_ip: str
    initial_location: Location
    latest_user_agent: str
    latest_os: str
    latest_os_version: str
    latest_browser: str
    latest_browser_version: str
    latest_device_type: str
    latest_timezone: str
    latest_ip: str
    latest_location: Location
    def __init__(self, session_id: _Optional[str] = ..., user_id: _Optional[str] = ..., authenticated_organizations: _Optional[_Iterable[str]] = ..., organization_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., idle_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., absolute_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expired_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., logout_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[str] = ..., initial_user_agent: _Optional[str] = ..., initial_os: _Optional[str] = ..., initial_os_version: _Optional[str] = ..., initial_browser: _Optional[str] = ..., initial_browser_version: _Optional[str] = ..., initial_device_type: _Optional[str] = ..., initial_timezone: _Optional[str] = ..., initial_ip: _Optional[str] = ..., initial_location: _Optional[_Union[Location, _Mapping]] = ..., latest_user_agent: _Optional[str] = ..., latest_os: _Optional[str] = ..., latest_os_version: _Optional[str] = ..., latest_browser: _Optional[str] = ..., latest_browser_version: _Optional[str] = ..., latest_device_type: _Optional[str] = ..., latest_timezone: _Optional[str] = ..., latest_ip: _Optional[str] = ..., latest_location: _Optional[_Union[Location, _Mapping]] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("region", "region_subdivision", "city", "latitude", "longitude")
    REGION_FIELD_NUMBER: _ClassVar[int]
    REGION_SUBDIVISION_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    region: str
    region_subdivision: str
    city: str
    latitude: str
    longitude: str
    def __init__(self, region: _Optional[str] = ..., region_subdivision: _Optional[str] = ..., city: _Optional[str] = ..., latitude: _Optional[str] = ..., longitude: _Optional[str] = ...) -> None: ...

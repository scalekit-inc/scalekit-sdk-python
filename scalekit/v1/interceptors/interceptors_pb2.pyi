from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.errdetails import errdetails_pb2 as _errdetails_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TriggerPoint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_POINT_UNSPECIFIED: _ClassVar[TriggerPoint]
    POST_USER_AUTHENTICATION: _ClassVar[TriggerPoint]
    PRE_SIGNUP: _ClassVar[TriggerPoint]
    PRE_SESSION_CREATION: _ClassVar[TriggerPoint]
    PRE_USER_INVITATION: _ClassVar[TriggerPoint]
    PRE_M2M_TOKEN_CREATION: _ClassVar[TriggerPoint]

class InterceptorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTERCEPTOR_TYPE_UNSPECIFIED: _ClassVar[InterceptorType]
    AUTH: _ClassVar[InterceptorType]

class FailurePolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FAILURE_POLICY_UNSPECIFIED: _ClassVar[FailurePolicy]
    FAIL_OPEN: _ClassVar[FailurePolicy]
    FAIL_CLOSED: _ClassVar[FailurePolicy]

class InterceptorDecision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTERCEPTOR_DECISION_UNSPECIFIED: _ClassVar[InterceptorDecision]
    ALLOW: _ClassVar[InterceptorDecision]
    DENY: _ClassVar[InterceptorDecision]

class AuthConfigType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUTH_CONFIG_TYPE_UNSPECIFIED: _ClassVar[AuthConfigType]
    API_KEY: _ClassVar[AuthConfigType]
    OAUTH2: _ClassVar[AuthConfigType]
TRIGGER_POINT_UNSPECIFIED: TriggerPoint
POST_USER_AUTHENTICATION: TriggerPoint
PRE_SIGNUP: TriggerPoint
PRE_SESSION_CREATION: TriggerPoint
PRE_USER_INVITATION: TriggerPoint
PRE_M2M_TOKEN_CREATION: TriggerPoint
INTERCEPTOR_TYPE_UNSPECIFIED: InterceptorType
AUTH: InterceptorType
FAILURE_POLICY_UNSPECIFIED: FailurePolicy
FAIL_OPEN: FailurePolicy
FAIL_CLOSED: FailurePolicy
INTERCEPTOR_DECISION_UNSPECIFIED: InterceptorDecision
ALLOW: InterceptorDecision
DENY: InterceptorDecision
AUTH_CONFIG_TYPE_UNSPECIFIED: AuthConfigType
API_KEY: AuthConfigType
OAUTH2: AuthConfigType

class CreateInterceptor(_message.Message):
    __slots__ = ("display_name", "description", "trigger_point", "interceptor_type", "api_url", "config", "timeout_ms", "failure_policy", "request_template", "response_template")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_POINT_FIELD_NUMBER: _ClassVar[int]
    INTERCEPTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    API_URL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_POLICY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    trigger_point: TriggerPoint
    interceptor_type: InterceptorType
    api_url: str
    config: Config
    timeout_ms: int
    failure_policy: FailurePolicy
    request_template: str
    response_template: str
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., trigger_point: _Optional[_Union[TriggerPoint, str]] = ..., interceptor_type: _Optional[_Union[InterceptorType, str]] = ..., api_url: _Optional[str] = ..., config: _Optional[_Union[Config, _Mapping]] = ..., timeout_ms: _Optional[int] = ..., failure_policy: _Optional[_Union[FailurePolicy, str]] = ..., request_template: _Optional[str] = ..., response_template: _Optional[str] = ...) -> None: ...

class Interceptor(_message.Message):
    __slots__ = ("id", "display_name", "description", "trigger_point", "interceptor_type", "api_url", "config", "timeout_ms", "failure_policy", "request_template", "response_template", "secret_id", "secret_suffix", "enabled", "created_at", "updated_at", "last_executed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_POINT_FIELD_NUMBER: _ClassVar[int]
    INTERCEPTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    API_URL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_POLICY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    description: str
    trigger_point: TriggerPoint
    interceptor_type: InterceptorType
    api_url: str
    config: Config
    timeout_ms: int
    failure_policy: FailurePolicy
    request_template: str
    response_template: str
    secret_id: str
    secret_suffix: str
    enabled: bool
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    last_executed_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., trigger_point: _Optional[_Union[TriggerPoint, str]] = ..., interceptor_type: _Optional[_Union[InterceptorType, str]] = ..., api_url: _Optional[str] = ..., config: _Optional[_Union[Config, _Mapping]] = ..., timeout_ms: _Optional[int] = ..., failure_policy: _Optional[_Union[FailurePolicy, str]] = ..., request_template: _Optional[str] = ..., response_template: _Optional[str] = ..., secret_id: _Optional[str] = ..., secret_suffix: _Optional[str] = ..., enabled: bool = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_executed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Config(_message.Message):
    __slots__ = ("auth_config",)
    AUTH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    auth_config: AuthenticationConfig
    def __init__(self, auth_config: _Optional[_Union[AuthenticationConfig, _Mapping]] = ...) -> None: ...

class AuthenticationConfig(_message.Message):
    __slots__ = ("api_key", "oauth2", "auth_config_type")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    OAUTH2_FIELD_NUMBER: _ClassVar[int]
    AUTH_CONFIG_TYPE_FIELD_NUMBER: _ClassVar[int]
    api_key: ApiKeyAuth
    oauth2: Oauth2Auth
    auth_config_type: AuthConfigType
    def __init__(self, api_key: _Optional[_Union[ApiKeyAuth, _Mapping]] = ..., oauth2: _Optional[_Union[Oauth2Auth, _Mapping]] = ..., auth_config_type: _Optional[_Union[AuthConfigType, str]] = ...) -> None: ...

class ApiKeyAuth(_message.Message):
    __slots__ = ("api_key", "header_name")
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    HEADER_NAME_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    header_name: str
    def __init__(self, api_key: _Optional[str] = ..., header_name: _Optional[str] = ...) -> None: ...

class Oauth2Auth(_message.Message):
    __slots__ = ("token_url", "client_id", "client_secret", "scope")
    TOKEN_URL_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    token_url: str
    client_id: str
    client_secret: str
    scope: str
    def __init__(self, token_url: _Optional[str] = ..., client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., scope: _Optional[str] = ...) -> None: ...

class CreateInterceptorRequest(_message.Message):
    __slots__ = ("interceptor",)
    INTERCEPTOR_FIELD_NUMBER: _ClassVar[int]
    interceptor: CreateInterceptor
    def __init__(self, interceptor: _Optional[_Union[CreateInterceptor, _Mapping]] = ...) -> None: ...

class CreateInterceptorResponse(_message.Message):
    __slots__ = ("interceptor",)
    INTERCEPTOR_FIELD_NUMBER: _ClassVar[int]
    interceptor: Interceptor
    def __init__(self, interceptor: _Optional[_Union[Interceptor, _Mapping]] = ...) -> None: ...

class GetInterceptorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetInterceptorResponse(_message.Message):
    __slots__ = ("interceptor",)
    INTERCEPTOR_FIELD_NUMBER: _ClassVar[int]
    interceptor: Interceptor
    def __init__(self, interceptor: _Optional[_Union[Interceptor, _Mapping]] = ...) -> None: ...

class EnableInterceptorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DisableInterceptorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ListInterceptorsRequest(_message.Message):
    __slots__ = ("trigger_point", "enabled", "page_size", "page_token")
    TRIGGER_POINT_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    trigger_point: TriggerPoint
    enabled: bool
    page_size: int
    page_token: str
    def __init__(self, trigger_point: _Optional[_Union[TriggerPoint, str]] = ..., enabled: bool = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListInterceptorsResponse(_message.Message):
    __slots__ = ("interceptors", "next_page_token", "total_size", "prev_page_token")
    INTERCEPTORS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    interceptors: _containers.RepeatedCompositeFieldContainer[Interceptor]
    next_page_token: str
    total_size: int
    prev_page_token: str
    def __init__(self, interceptors: _Optional[_Iterable[_Union[Interceptor, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class UpdateInterceptorRequest(_message.Message):
    __slots__ = ("id", "interceptor")
    ID_FIELD_NUMBER: _ClassVar[int]
    INTERCEPTOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    interceptor: UpdateInterceptor
    def __init__(self, id: _Optional[str] = ..., interceptor: _Optional[_Union[UpdateInterceptor, _Mapping]] = ...) -> None: ...

class UpdateInterceptor(_message.Message):
    __slots__ = ("display_name", "description", "trigger_point", "api_url", "config", "timeout_ms", "failure_policy", "request_template", "response_template")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_POINT_FIELD_NUMBER: _ClassVar[int]
    API_URL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_POLICY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    trigger_point: TriggerPoint
    api_url: str
    config: Config
    timeout_ms: int
    failure_policy: FailurePolicy
    request_template: str
    response_template: str
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., trigger_point: _Optional[_Union[TriggerPoint, str]] = ..., api_url: _Optional[str] = ..., config: _Optional[_Union[Config, _Mapping]] = ..., timeout_ms: _Optional[int] = ..., failure_policy: _Optional[_Union[FailurePolicy, str]] = ..., request_template: _Optional[str] = ..., response_template: _Optional[str] = ...) -> None: ...

class UpdateInterceptorResponse(_message.Message):
    __slots__ = ("interceptor",)
    INTERCEPTOR_FIELD_NUMBER: _ClassVar[int]
    interceptor: Interceptor
    def __init__(self, interceptor: _Optional[_Union[Interceptor, _Mapping]] = ...) -> None: ...

class DeleteInterceptorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class InterceptorError(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class TestInterceptorRequest(_message.Message):
    __slots__ = ("id", "data")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    data: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class TestInterceptorResponse(_message.Message):
    __slots__ = ("interceptor_response", "validation_error", "error")
    INTERCEPTOR_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    interceptor_response: _struct_pb2.Struct
    validation_error: _errdetails_pb2.ValidationErrorInfo
    error: ErrorMessage
    def __init__(self, interceptor_response: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., validation_error: _Optional[_Union[_errdetails_pb2.ValidationErrorInfo, _Mapping]] = ..., error: _Optional[_Union[ErrorMessage, _Mapping]] = ...) -> None: ...

class ErrorMessage(_message.Message):
    __slots__ = ("code", "message", "details")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    details: _struct_pb2.Struct
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ..., details: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class InterceptorResponse(_message.Message):
    __slots__ = ("decision", "error")
    DECISION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    decision: InterceptorDecision
    error: InterceptorError
    def __init__(self, decision: _Optional[_Union[InterceptorDecision, str]] = ..., error: _Optional[_Union[InterceptorError, _Mapping]] = ...) -> None: ...

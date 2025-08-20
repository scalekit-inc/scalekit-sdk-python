from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorInfo(_message.Message):
    __slots__ = ("error_code", "debug_info", "help_info", "localized_message_info", "resource_info", "request_info", "validation_error_info", "tool_error_info")
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    DEBUG_INFO_FIELD_NUMBER: _ClassVar[int]
    HELP_INFO_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_MESSAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_INFO_FIELD_NUMBER: _ClassVar[int]
    REQUEST_INFO_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    TOOL_ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    error_code: str
    debug_info: DebugInfo
    help_info: HelpInfo
    localized_message_info: LocalizedMessageInfo
    resource_info: ResourceInfo
    request_info: RequestInfo
    validation_error_info: ValidationErrorInfo
    tool_error_info: ToolErrorInfo
    def __init__(self, error_code: _Optional[str] = ..., debug_info: _Optional[_Union[DebugInfo, _Mapping]] = ..., help_info: _Optional[_Union[HelpInfo, _Mapping]] = ..., localized_message_info: _Optional[_Union[LocalizedMessageInfo, _Mapping]] = ..., resource_info: _Optional[_Union[ResourceInfo, _Mapping]] = ..., request_info: _Optional[_Union[RequestInfo, _Mapping]] = ..., validation_error_info: _Optional[_Union[ValidationErrorInfo, _Mapping]] = ..., tool_error_info: _Optional[_Union[ToolErrorInfo, _Mapping]] = ...) -> None: ...

class DebugInfo(_message.Message):
    __slots__ = ("stack_entries", "detail")
    STACK_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    stack_entries: _containers.RepeatedScalarFieldContainer[str]
    detail: str
    def __init__(self, stack_entries: _Optional[_Iterable[str]] = ..., detail: _Optional[str] = ...) -> None: ...

class ValidationErrorInfo(_message.Message):
    __slots__ = ("field_violations",)
    class FieldViolation(_message.Message):
        __slots__ = ("field", "description", "constraint")
        FIELD_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        CONSTRAINT_FIELD_NUMBER: _ClassVar[int]
        field: str
        description: str
        constraint: str
        def __init__(self, field: _Optional[str] = ..., description: _Optional[str] = ..., constraint: _Optional[str] = ...) -> None: ...
    FIELD_VIOLATIONS_FIELD_NUMBER: _ClassVar[int]
    field_violations: _containers.RepeatedCompositeFieldContainer[ValidationErrorInfo.FieldViolation]
    def __init__(self, field_violations: _Optional[_Iterable[_Union[ValidationErrorInfo.FieldViolation, _Mapping]]] = ...) -> None: ...

class RequestInfo(_message.Message):
    __slots__ = ("request_id", "serving_data")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SERVING_DATA_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    serving_data: str
    def __init__(self, request_id: _Optional[str] = ..., serving_data: _Optional[str] = ...) -> None: ...

class ResourceInfo(_message.Message):
    __slots__ = ("resource_type", "resource_name", "owner", "description")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    resource_type: str
    resource_name: str
    owner: str
    description: str
    def __init__(self, resource_type: _Optional[str] = ..., resource_name: _Optional[str] = ..., owner: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class HelpInfo(_message.Message):
    __slots__ = ("links",)
    class Link(_message.Message):
        __slots__ = ("description", "url")
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        description: str
        url: str
        def __init__(self, description: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...
    LINKS_FIELD_NUMBER: _ClassVar[int]
    links: _containers.RepeatedCompositeFieldContainer[HelpInfo.Link]
    def __init__(self, links: _Optional[_Iterable[_Union[HelpInfo.Link, _Mapping]]] = ...) -> None: ...

class LocalizedMessageInfo(_message.Message):
    __slots__ = ("locale", "message")
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    locale: str
    message: str
    def __init__(self, locale: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ToolErrorInfo(_message.Message):
    __slots__ = ("execution_id", "tool_error_message", "tool_error_code")
    EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TOOL_ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    execution_id: str
    tool_error_message: str
    tool_error_code: str
    def __init__(self, execution_id: _Optional[str] = ..., tool_error_message: _Optional[str] = ..., tool_error_code: _Optional[str] = ...) -> None: ...

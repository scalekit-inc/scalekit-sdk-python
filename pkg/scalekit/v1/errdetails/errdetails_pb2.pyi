from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorInfo(_message.Message):
    __slots__ = ("code_id", "error_code")
    CODE_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    code_id: str
    error_code: str
    def __init__(self, code_id: _Optional[str] = ..., error_code: _Optional[str] = ...) -> None: ...

class DebugInfo(_message.Message):
    __slots__ = ("stack_entries", "detail")
    STACK_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    stack_entries: _containers.RepeatedScalarFieldContainer[str]
    detail: str
    def __init__(self, stack_entries: _Optional[_Iterable[str]] = ..., detail: _Optional[str] = ...) -> None: ...

class BadRequest(_message.Message):
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
    field_violations: _containers.RepeatedCompositeFieldContainer[BadRequest.FieldViolation]
    def __init__(self, field_violations: _Optional[_Iterable[_Union[BadRequest.FieldViolation, _Mapping]]] = ...) -> None: ...

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

class Help(_message.Message):
    __slots__ = ("links",)
    class Link(_message.Message):
        __slots__ = ("description", "url")
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        description: str
        url: str
        def __init__(self, description: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...
    LINKS_FIELD_NUMBER: _ClassVar[int]
    links: _containers.RepeatedCompositeFieldContainer[Help.Link]
    def __init__(self, links: _Optional[_Iterable[_Union[Help.Link, _Mapping]]] = ...) -> None: ...

class LocalizedMessage(_message.Message):
    __slots__ = ("locale", "message")
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    locale: str
    message: str
    def __init__(self, locale: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class SsoErrorInfo(_message.Message):
    __slots__ = ("code", "description", "redirect_params", "redirect_url")
    class RedirectParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URL_FIELD_NUMBER: _ClassVar[int]
    code: str
    description: str
    redirect_params: _containers.ScalarMap[str, str]
    redirect_url: str
    def __init__(self, code: _Optional[str] = ..., description: _Optional[str] = ..., redirect_params: _Optional[_Mapping[str, str]] = ..., redirect_url: _Optional[str] = ...) -> None: ...

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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

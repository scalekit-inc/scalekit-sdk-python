from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateMcpRequest(_message.Message):
    __slots__ = ("mcp",)
    MCP_FIELD_NUMBER: _ClassVar[int]
    mcp: Mcp
    def __init__(self, mcp: _Optional[_Union[Mcp, _Mapping]] = ...) -> None: ...

class CreateMcpResponse(_message.Message):
    __slots__ = ("mcp",)
    MCP_FIELD_NUMBER: _ClassVar[int]
    mcp: Mcp
    def __init__(self, mcp: _Optional[_Union[Mcp, _Mapping]] = ...) -> None: ...

class Mcp(_message.Message):
    __slots__ = ("id", "tool_mappings", "connected_account_identifier", "url")
    ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    tool_mappings: _containers.RepeatedCompositeFieldContainer[ToolMapping]
    connected_account_identifier: str
    url: str
    def __init__(self, id: _Optional[str] = ..., tool_mappings: _Optional[_Iterable[_Union[ToolMapping, _Mapping]]] = ..., connected_account_identifier: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class ToolMapping(_message.Message):
    __slots__ = ("tool_names", "connection_name", "status")
    TOOL_NAMES_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    tool_names: _containers.RepeatedScalarFieldContainer[str]
    connection_name: str
    status: str
    def __init__(self, tool_names: _Optional[_Iterable[str]] = ..., connection_name: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class GetMcpRequest(_message.Message):
    __slots__ = ("mcp_id",)
    MCP_ID_FIELD_NUMBER: _ClassVar[int]
    mcp_id: str
    def __init__(self, mcp_id: _Optional[str] = ...) -> None: ...

class GetMcpResponse(_message.Message):
    __slots__ = ("mcp",)
    MCP_FIELD_NUMBER: _ClassVar[int]
    mcp: Mcp
    def __init__(self, mcp: _Optional[_Union[Mcp, _Mapping]] = ...) -> None: ...

class ListMcpRequest(_message.Message):
    __slots__ = ("filter",)
    class Filter(_message.Message):
        __slots__ = ("connected_account_identifier", "link_token")
        CONNECTED_ACCOUNT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        LINK_TOKEN_FIELD_NUMBER: _ClassVar[int]
        connected_account_identifier: str
        link_token: str
        def __init__(self, connected_account_identifier: _Optional[str] = ..., link_token: _Optional[str] = ...) -> None: ...
    FILTER_FIELD_NUMBER: _ClassVar[int]
    filter: ListMcpRequest.Filter
    def __init__(self, filter: _Optional[_Union[ListMcpRequest.Filter, _Mapping]] = ...) -> None: ...

class ListMcpResponse(_message.Message):
    __slots__ = ("mcps",)
    MCPS_FIELD_NUMBER: _ClassVar[int]
    mcps: _containers.RepeatedCompositeFieldContainer[Mcp]
    def __init__(self, mcps: _Optional[_Iterable[_Union[Mcp, _Mapping]]] = ...) -> None: ...

class DeleteMcpRequest(_message.Message):
    __slots__ = ("mcp_id",)
    MCP_ID_FIELD_NUMBER: _ClassVar[int]
    mcp_id: str
    def __init__(self, mcp_id: _Optional[str] = ...) -> None: ...

class DeleteMcpResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

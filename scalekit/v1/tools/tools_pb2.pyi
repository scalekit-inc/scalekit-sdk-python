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

class CreateToolRequest(_message.Message):
    __slots__ = ("tool",)
    TOOL_FIELD_NUMBER: _ClassVar[int]
    tool: Tool
    def __init__(self, tool: _Optional[_Union[Tool, _Mapping]] = ...) -> None: ...

class CreateToolResponse(_message.Message):
    __slots__ = ("tool",)
    TOOL_FIELD_NUMBER: _ClassVar[int]
    tool: Tool
    def __init__(self, tool: _Optional[_Union[Tool, _Mapping]] = ...) -> None: ...

class Tool(_message.Message):
    __slots__ = ("id", "provider", "definition", "metadata", "tags", "is_default", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    provider: str
    definition: _struct_pb2.Struct
    metadata: _struct_pb2.Struct
    tags: _containers.RepeatedScalarFieldContainer[str]
    is_default: _wrappers_pb2.BoolValue
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., provider: _Optional[str] = ..., definition: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., tags: _Optional[_Iterable[str]] = ..., is_default: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ScopedTool(_message.Message):
    __slots__ = ("tool", "identifier", "connected_account_id")
    TOOL_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    tool: Tool
    identifier: str
    connected_account_id: str
    def __init__(self, tool: _Optional[_Union[Tool, _Mapping]] = ..., identifier: _Optional[str] = ..., connected_account_id: _Optional[str] = ...) -> None: ...

class ListToolsRequest(_message.Message):
    __slots__ = ("filter", "page_size", "page_token")
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    filter: Filter
    page_size: int
    page_token: str
    def __init__(self, filter: _Optional[_Union[Filter, _Mapping]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("summary", "provider", "identifier", "tool_name")
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    summary: _wrappers_pb2.BoolValue
    provider: str
    identifier: str
    tool_name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, summary: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., provider: _Optional[str] = ..., identifier: _Optional[str] = ..., tool_name: _Optional[_Iterable[str]] = ...) -> None: ...

class ListToolsResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "prev_page_token", "tool_names", "tools")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAMES_FIELD_NUMBER: _ClassVar[int]
    TOOLS_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    prev_page_token: str
    tool_names: _containers.RepeatedScalarFieldContainer[str]
    tools: _containers.RepeatedCompositeFieldContainer[Tool]
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ..., tool_names: _Optional[_Iterable[str]] = ..., tools: _Optional[_Iterable[_Union[Tool, _Mapping]]] = ...) -> None: ...

class ExecuteToolRequest(_message.Message):
    __slots__ = ("tool_name", "identifier", "params", "connected_account_id", "connector", "organization_id", "user_id")
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    tool_name: str
    identifier: str
    params: _struct_pb2.Struct
    connected_account_id: str
    connector: str
    organization_id: str
    user_id: str
    def __init__(self, tool_name: _Optional[str] = ..., identifier: _Optional[str] = ..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., connected_account_id: _Optional[str] = ..., connector: _Optional[str] = ..., organization_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class ExecuteToolResponse(_message.Message):
    __slots__ = ("data", "execution_id")
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    data: _struct_pb2.Struct
    execution_id: str
    def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., execution_id: _Optional[str] = ...) -> None: ...

class SetToolDefaultRequest(_message.Message):
    __slots__ = ("name", "schema_version", "tool_version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    TOOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    schema_version: str
    tool_version: str
    def __init__(self, name: _Optional[str] = ..., schema_version: _Optional[str] = ..., tool_version: _Optional[str] = ...) -> None: ...

class SetToolDefaultResponse(_message.Message):
    __slots__ = ("tool",)
    TOOL_FIELD_NUMBER: _ClassVar[int]
    tool: Tool
    def __init__(self, tool: _Optional[_Union[Tool, _Mapping]] = ...) -> None: ...

class UpdateToolRequest(_message.Message):
    __slots__ = ("tool",)
    TOOL_FIELD_NUMBER: _ClassVar[int]
    tool: Tool
    def __init__(self, tool: _Optional[_Union[Tool, _Mapping]] = ...) -> None: ...

class UpdateToolResponse(_message.Message):
    __slots__ = ("tool",)
    TOOL_FIELD_NUMBER: _ClassVar[int]
    tool: Tool
    def __init__(self, tool: _Optional[_Union[Tool, _Mapping]] = ...) -> None: ...

class DeleteToolRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ListScopedToolsRequest(_message.Message):
    __slots__ = ("identifier", "filter", "page_size", "page_token")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    filter: ScopedToolFilter
    page_size: int
    page_token: str
    def __init__(self, identifier: _Optional[str] = ..., filter: _Optional[_Union[ScopedToolFilter, _Mapping]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListScopedToolsResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "prev_page_token", "tools")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOOLS_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    prev_page_token: str
    tools: _containers.RepeatedCompositeFieldContainer[ScopedTool]
    def __init__(self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ..., tools: _Optional[_Iterable[_Union[ScopedTool, _Mapping]]] = ...) -> None: ...

class ScopedToolFilter(_message.Message):
    __slots__ = ("providers", "tool_names", "connection_names")
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAMES_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_NAMES_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedScalarFieldContainer[str]
    tool_names: _containers.RepeatedScalarFieldContainer[str]
    connection_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, providers: _Optional[_Iterable[str]] = ..., tool_names: _Optional[_Iterable[str]] = ..., connection_names: _Optional[_Iterable[str]] = ...) -> None: ...

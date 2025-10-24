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

class CreateMcpConfigRequest(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: McpConfig
    def __init__(self, config: _Optional[_Union[McpConfig, _Mapping]] = ...) -> None: ...

class CreateMcpConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: McpConfig
    def __init__(self, config: _Optional[_Union[McpConfig, _Mapping]] = ...) -> None: ...

class UpdateMcpConfigRequest(_message.Message):
    __slots__ = ("config_id", "description", "connection_tool_mappings")
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TOOL_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    config_id: str
    description: str
    connection_tool_mappings: _containers.RepeatedCompositeFieldContainer[McpConfigConnectionToolMapping]
    def __init__(self, config_id: _Optional[str] = ..., description: _Optional[str] = ..., connection_tool_mappings: _Optional[_Iterable[_Union[McpConfigConnectionToolMapping, _Mapping]]] = ...) -> None: ...

class UpdateMcpConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: McpConfig
    def __init__(self, config: _Optional[_Union[McpConfig, _Mapping]] = ...) -> None: ...

class DeleteMcpConfigRequest(_message.Message):
    __slots__ = ("config_id",)
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    config_id: str
    def __init__(self, config_id: _Optional[str] = ...) -> None: ...

class DeleteMcpConfigResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMcpConfigRequest(_message.Message):
    __slots__ = ("config_id",)
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    config_id: str
    def __init__(self, config_id: _Optional[str] = ...) -> None: ...

class GetMcpConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: McpConfig
    def __init__(self, config: _Optional[_Union[McpConfig, _Mapping]] = ...) -> None: ...

class ListMcpConfigsRequest(_message.Message):
    __slots__ = ("filter", "search", "page_size", "page_token")
    class Filter(_message.Message):
        __slots__ = ("id", "name", "provider")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        provider: str
        def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., provider: _Optional[str] = ...) -> None: ...
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    filter: ListMcpConfigsRequest.Filter
    search: str
    page_size: int
    page_token: str
    def __init__(self, filter: _Optional[_Union[ListMcpConfigsRequest.Filter, _Mapping]] = ..., search: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListMcpConfigsResponse(_message.Message):
    __slots__ = ("configs", "next_page_token", "prev_page_token", "total_size")
    CONFIGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    configs: _containers.RepeatedCompositeFieldContainer[McpConfig]
    next_page_token: str
    prev_page_token: str
    total_size: int
    def __init__(self, configs: _Optional[_Iterable[_Union[McpConfig, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class EnsureMcpInstanceRequest(_message.Message):
    __slots__ = ("name", "config_name", "user_identifier")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    name: str
    config_name: str
    user_identifier: str
    def __init__(self, name: _Optional[str] = ..., config_name: _Optional[str] = ..., user_identifier: _Optional[str] = ...) -> None: ...

class EnsureMcpInstanceResponse(_message.Message):
    __slots__ = ("instance",)
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    instance: McpInstance
    def __init__(self, instance: _Optional[_Union[McpInstance, _Mapping]] = ...) -> None: ...

class ListMcpInstancesRequest(_message.Message):
    __slots__ = ("filter", "search", "page_size", "page_token")
    class Filter(_message.Message):
        __slots__ = ("id", "name", "config_name", "user_identifier")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        CONFIG_NAME_FIELD_NUMBER: _ClassVar[int]
        USER_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        config_name: str
        user_identifier: str
        def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., config_name: _Optional[str] = ..., user_identifier: _Optional[str] = ...) -> None: ...
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    filter: ListMcpInstancesRequest.Filter
    search: str
    page_size: int
    page_token: str
    def __init__(self, filter: _Optional[_Union[ListMcpInstancesRequest.Filter, _Mapping]] = ..., search: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListMcpInstancesResponse(_message.Message):
    __slots__ = ("instances", "next_page_token", "prev_page_token", "total_size")
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    instances: _containers.RepeatedCompositeFieldContainer[McpInstance]
    next_page_token: str
    prev_page_token: str
    total_size: int
    def __init__(self, instances: _Optional[_Iterable[_Union[McpInstance, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class DeleteMcpInstanceRequest(_message.Message):
    __slots__ = ("instance_id",)
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    def __init__(self, instance_id: _Optional[str] = ...) -> None: ...

class DeleteMcpInstanceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateMcpInstanceRequest(_message.Message):
    __slots__ = ("instance_id", "name", "config_name")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_NAME_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    name: str
    config_name: str
    def __init__(self, instance_id: _Optional[str] = ..., name: _Optional[str] = ..., config_name: _Optional[str] = ...) -> None: ...

class UpdateMcpInstanceResponse(_message.Message):
    __slots__ = ("instance",)
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    instance: McpInstance
    def __init__(self, instance: _Optional[_Union[McpInstance, _Mapping]] = ...) -> None: ...

class GetMcpInstanceRequest(_message.Message):
    __slots__ = ("instance_id",)
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    def __init__(self, instance_id: _Optional[str] = ...) -> None: ...

class GetMcpInstanceResponse(_message.Message):
    __slots__ = ("instance",)
    INSTANCE_FIELD_NUMBER: _ClassVar[int]
    instance: McpInstance
    def __init__(self, instance: _Optional[_Union[McpInstance, _Mapping]] = ...) -> None: ...

class GetMcpInstanceAuthStateRequest(_message.Message):
    __slots__ = ("instance_id", "include_auth_links")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_AUTH_LINKS_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    include_auth_links: bool
    def __init__(self, instance_id: _Optional[str] = ..., include_auth_links: bool = ...) -> None: ...

class McpInstanceConnectionAuthState(_message.Message):
    __slots__ = ("connection_id", "connection_name", "provider", "connected_account_id", "connected_account_status", "authentication_link")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_STATUS_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_LINK_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connection_name: str
    provider: str
    connected_account_id: str
    connected_account_status: str
    authentication_link: str
    def __init__(self, connection_id: _Optional[str] = ..., connection_name: _Optional[str] = ..., provider: _Optional[str] = ..., connected_account_id: _Optional[str] = ..., connected_account_status: _Optional[str] = ..., authentication_link: _Optional[str] = ...) -> None: ...

class GetMcpInstanceAuthStateResponse(_message.Message):
    __slots__ = ("connections",)
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[McpInstanceConnectionAuthState]
    def __init__(self, connections: _Optional[_Iterable[_Union[McpInstanceConnectionAuthState, _Mapping]]] = ...) -> None: ...

class McpInstance(_message.Message):
    __slots__ = ("id", "name", "user_identifier", "config", "last_used_at", "updated_at", "url")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    user_identifier: str
    config: McpConfig
    last_used_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    url: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., user_identifier: _Optional[str] = ..., config: _Optional[_Union[McpConfig, _Mapping]] = ..., last_used_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., url: _Optional[str] = ...) -> None: ...

class McpConfig(_message.Message):
    __slots__ = ("id", "name", "description", "connection_tool_mappings")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TOOL_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    connection_tool_mappings: _containers.RepeatedCompositeFieldContainer[McpConfigConnectionToolMapping]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., connection_tool_mappings: _Optional[_Iterable[_Union[McpConfigConnectionToolMapping, _Mapping]]] = ...) -> None: ...

class McpConfigConnectionToolMapping(_message.Message):
    __slots__ = ("connection_id", "connection_name", "provider", "tools", "connected_account_id", "connected_account_status")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TOOLS_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_STATUS_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connection_name: str
    provider: str
    tools: _containers.RepeatedScalarFieldContainer[str]
    connected_account_id: str
    connected_account_status: str
    def __init__(self, connection_id: _Optional[str] = ..., connection_name: _Optional[str] = ..., provider: _Optional[str] = ..., tools: _Optional[_Iterable[str]] = ..., connected_account_id: _Optional[str] = ..., connected_account_status: _Optional[str] = ...) -> None: ...

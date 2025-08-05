from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Provider(_message.Message):
    __slots__ = ("id", "identifier", "display_name", "description", "categories", "auth_patterns", "icon_src", "display_priority")
    ID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    AUTH_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    ICON_SRC_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    identifier: str
    display_name: str
    description: str
    categories: _containers.RepeatedScalarFieldContainer[str]
    auth_patterns: _struct_pb2.ListValue
    icon_src: str
    display_priority: int
    def __init__(self, id: _Optional[str] = ..., identifier: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., categories: _Optional[_Iterable[str]] = ..., auth_patterns: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ..., icon_src: _Optional[str] = ..., display_priority: _Optional[int] = ...) -> None: ...

class CreateProvider(_message.Message):
    __slots__ = ("identifier", "display_name", "description", "categories", "auth_patterns", "icon_src", "display_priority")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    AUTH_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    ICON_SRC_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    display_name: str
    description: str
    categories: _containers.RepeatedScalarFieldContainer[str]
    auth_patterns: _struct_pb2.ListValue
    icon_src: str
    display_priority: int
    def __init__(self, identifier: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., categories: _Optional[_Iterable[str]] = ..., auth_patterns: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ..., icon_src: _Optional[str] = ..., display_priority: _Optional[int] = ...) -> None: ...

class CreateProviderRequest(_message.Message):
    __slots__ = ("provider",)
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    provider: CreateProvider
    def __init__(self, provider: _Optional[_Union[CreateProvider, _Mapping]] = ...) -> None: ...

class CreateProviderResponse(_message.Message):
    __slots__ = ("provider",)
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    provider: Provider
    def __init__(self, provider: _Optional[_Union[Provider, _Mapping]] = ...) -> None: ...

class UpdateProvider(_message.Message):
    __slots__ = ("display_name", "description", "categories", "auth_patterns", "icon_src", "display_priority")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    AUTH_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    ICON_SRC_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    categories: _containers.RepeatedScalarFieldContainer[str]
    auth_patterns: _struct_pb2.ListValue
    icon_src: str
    display_priority: int
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., categories: _Optional[_Iterable[str]] = ..., auth_patterns: _Optional[_Union[_struct_pb2.ListValue, _Mapping]] = ..., icon_src: _Optional[str] = ..., display_priority: _Optional[int] = ...) -> None: ...

class UpdateProviderRequest(_message.Message):
    __slots__ = ("identifier", "provider")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    provider: UpdateProvider
    def __init__(self, identifier: _Optional[str] = ..., provider: _Optional[_Union[UpdateProvider, _Mapping]] = ...) -> None: ...

class UpdateProviderResponse(_message.Message):
    __slots__ = ("provider",)
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    provider: Provider
    def __init__(self, provider: _Optional[_Union[Provider, _Mapping]] = ...) -> None: ...

class ListProvidersRequest(_message.Message):
    __slots__ = ("identifier", "page_size", "page_token")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    page_size: int
    page_token: str
    def __init__(self, identifier: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListProvidersResponse(_message.Message):
    __slots__ = ("providers", "next_page_token", "total_size", "prev_page_token")
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[Provider]
    next_page_token: str
    total_size: int
    prev_page_token: str
    def __init__(self, providers: _Optional[_Iterable[_Union[Provider, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., prev_page_token: _Optional[str] = ...) -> None: ...

class DeleteProviderRequest(_message.Message):
    __slots__ = ("identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    def __init__(self, identifier: _Optional[str] = ...) -> None: ...

class DeleteProviderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

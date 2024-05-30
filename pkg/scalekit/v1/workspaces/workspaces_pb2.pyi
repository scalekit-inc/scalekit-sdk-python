from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class YesNo(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    YES: _ClassVar[YesNo]
    NO: _ClassVar[YesNo]
YES: YesNo
NO: YesNo

class Workspace(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "display_name", "region_code")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_CODE_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    display_name: str
    region_code: _commons_pb2.RegionCode
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., display_name: _Optional[str] = ..., region_code: _Optional[_Union[_commons_pb2.RegionCode, str]] = ...) -> None: ...

class CreateWorkspace(_message.Message):
    __slots__ = ("email", "company", "send_welcome_email")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    SEND_WELCOME_EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    company: str
    send_welcome_email: YesNo
    def __init__(self, email: _Optional[str] = ..., company: _Optional[str] = ..., send_welcome_email: _Optional[_Union[YesNo, str]] = ...) -> None: ...

class UpdateWorkspace(_message.Message):
    __slots__ = ("display_name",)
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    def __init__(self, display_name: _Optional[str] = ...) -> None: ...

class CreateWorkspaceRequest(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: CreateWorkspace
    def __init__(self, workspace: _Optional[_Union[CreateWorkspace, _Mapping]] = ...) -> None: ...

class CreateWorkspaceResponse(_message.Message):
    __slots__ = ("workspace", "link")
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    workspace: Workspace
    link: str
    def __init__(self, workspace: _Optional[_Union[Workspace, _Mapping]] = ..., link: _Optional[str] = ...) -> None: ...

class UpdateWorkspaceRequest(_message.Message):
    __slots__ = ("id", "workspace")
    ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    id: str
    workspace: UpdateWorkspace
    def __init__(self, id: _Optional[str] = ..., workspace: _Optional[_Union[UpdateWorkspace, _Mapping]] = ...) -> None: ...

class UpdateCurrentWorkspaceRequest(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: UpdateWorkspace
    def __init__(self, workspace: _Optional[_Union[UpdateWorkspace, _Mapping]] = ...) -> None: ...

class UpdateWorkspaceResponse(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: Workspace
    def __init__(self, workspace: _Optional[_Union[Workspace, _Mapping]] = ...) -> None: ...

class GetWorkspaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCurrentWorkspaceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetWorkspaceResponse(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: Workspace
    def __init__(self, workspace: _Optional[_Union[Workspace, _Mapping]] = ...) -> None: ...

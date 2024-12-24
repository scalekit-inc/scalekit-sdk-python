from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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
    __slots__ = ("email", "company")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    email: str
    company: str
    def __init__(self, email: _Optional[str] = ..., company: _Optional[str] = ...) -> None: ...

class UpdateWorkspace(_message.Message):
    __slots__ = ("display_name",)
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    def __init__(self, display_name: _Optional[str] = ...) -> None: ...

class OnboardWorkspace(_message.Message):
    __slots__ = ("workspace_display_name", "user_given_name", "user_family_name")
    WORKSPACE_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_GIVEN_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    workspace_display_name: str
    user_given_name: str
    user_family_name: str
    def __init__(self, workspace_display_name: _Optional[str] = ..., user_given_name: _Optional[str] = ..., user_family_name: _Optional[str] = ...) -> None: ...

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

class OnboardWorkspaceRequest(_message.Message):
    __slots__ = ("workspace",)
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: OnboardWorkspace
    def __init__(self, workspace: _Optional[_Union[OnboardWorkspace, _Mapping]] = ...) -> None: ...

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

class GetBillingPortalRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetBillingPortalResponse(_message.Message):
    __slots__ = ("url", "id")
    URL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    url: str
    id: str
    def __init__(self, url: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetWorkspacePricingTableRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetWorkspacePricingTableResponse(_message.Message):
    __slots__ = ("id", "pricing_table_id", "publishable_token", "customer_session_client_secret", "expiry")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRICING_TABLE_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLISHABLE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_SESSION_CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    id: str
    pricing_table_id: str
    publishable_token: str
    customer_session_client_secret: str
    expiry: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., pricing_table_id: _Optional[str] = ..., publishable_token: _Optional[str] = ..., customer_session_client_secret: _Optional[str] = ..., expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetWorkspaceSubscriptionsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetWorkspaceSubscriptionsResponse(_message.Message):
    __slots__ = ("id", "subscriptions")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    subscriptions: _containers.RepeatedCompositeFieldContainer[Subscription]
    def __init__(self, id: _Optional[str] = ..., subscriptions: _Optional[_Iterable[_Union[Subscription, _Mapping]]] = ...) -> None: ...

class Subscription(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

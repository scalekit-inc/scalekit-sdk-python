from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RevokeInviteRequest(_message.Message):
    __slots__ = ("id", "membership_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    membership_id: str
    def __init__(self, id: _Optional[str] = ..., membership_id: _Optional[str] = ...) -> None: ...

class RevokeInviteResponse(_message.Message):
    __slots__ = ("invite",)
    INVITE_FIELD_NUMBER: _ClassVar[int]
    invite: Invite
    def __init__(self, invite: _Optional[_Union[Invite, _Mapping]] = ...) -> None: ...

class Invite(_message.Message):
    __slots__ = ("id", "organization_id", "environment_id", "user_id", "invited_by", "invitee_name", "status", "expiry", "accepted_at", "resent_at", "link_id", "resent_times")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    INVITED_BY_FIELD_NUMBER: _ClassVar[int]
    INVITEE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    RESENT_AT_FIELD_NUMBER: _ClassVar[int]
    LINK_ID_FIELD_NUMBER: _ClassVar[int]
    RESENT_TIMES_FIELD_NUMBER: _ClassVar[int]
    id: str
    organization_id: str
    environment_id: str
    user_id: str
    invited_by: str
    invitee_name: str
    status: str
    expiry: _timestamp_pb2.Timestamp
    accepted_at: _timestamp_pb2.Timestamp
    resent_at: _timestamp_pb2.Timestamp
    link_id: str
    resent_times: int
    def __init__(self, id: _Optional[str] = ..., organization_id: _Optional[str] = ..., environment_id: _Optional[str] = ..., user_id: _Optional[str] = ..., invited_by: _Optional[str] = ..., invitee_name: _Optional[str] = ..., status: _Optional[str] = ..., expiry: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., accepted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., resent_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., link_id: _Optional[str] = ..., resent_times: _Optional[int] = ...) -> None: ...

class ResendInviteRequest(_message.Message):
    __slots__ = ("id", "membership_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    membership_id: str
    def __init__(self, id: _Optional[str] = ..., membership_id: _Optional[str] = ...) -> None: ...

class ResendInviteResponse(_message.Message):
    __slots__ = ("invite",)
    INVITE_FIELD_NUMBER: _ClassVar[int]
    invite: Invite
    def __init__(self, invite: _Optional[_Union[Invite, _Mapping]] = ...) -> None: ...

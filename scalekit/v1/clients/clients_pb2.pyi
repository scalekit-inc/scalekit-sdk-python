from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientSecretStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE: _ClassVar[ClientSecretStatus]
    INACTIVE: _ClassVar[ClientSecretStatus]
ACTIVE: ClientSecretStatus
INACTIVE: ClientSecretStatus

class GetClientRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class GetClientResponse(_message.Message):
    __slots__ = ("client",)
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    client: Client
    def __init__(self, client: _Optional[_Union[Client, _Mapping]] = ...) -> None: ...

class ListClientsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListClientsResponse(_message.Message):
    __slots__ = ("total_size", "clients")
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    total_size: int
    clients: _containers.RepeatedCompositeFieldContainer[Client]
    def __init__(self, total_size: _Optional[int] = ..., clients: _Optional[_Iterable[_Union[Client, _Mapping]]] = ...) -> None: ...

class UpdateClientRequest(_message.Message):
    __slots__ = ("client_id", "client", "mask")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client: UpdateClient
    mask: _field_mask_pb2.FieldMask
    def __init__(self, client_id: _Optional[str] = ..., client: _Optional[_Union[UpdateClient, _Mapping]] = ..., mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateClient(_message.Message):
    __slots__ = ("redirect_uris", "default_redirect_uri", "back_channel_logout_uri", "post_logout_redirect_uris")
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    BACK_CHANNEL_LOGOUT_URI_FIELD_NUMBER: _ClassVar[int]
    POST_LOGOUT_REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    default_redirect_uri: str
    back_channel_logout_uri: str
    post_logout_redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, redirect_uris: _Optional[_Iterable[str]] = ..., default_redirect_uri: _Optional[str] = ..., back_channel_logout_uri: _Optional[str] = ..., post_logout_redirect_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateClientResponse(_message.Message):
    __slots__ = ("client",)
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    client: Client
    def __init__(self, client: _Optional[_Union[Client, _Mapping]] = ...) -> None: ...

class CreateClientSecretRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class CreateClientSecretResponse(_message.Message):
    __slots__ = ("plain_secret", "secret")
    PLAIN_SECRET_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    plain_secret: str
    secret: ClientSecret
    def __init__(self, plain_secret: _Optional[str] = ..., secret: _Optional[_Union[ClientSecret, _Mapping]] = ...) -> None: ...

class UpdateClientSecretRequest(_message.Message):
    __slots__ = ("client_id", "secret_id", "secret", "mask")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    secret_id: str
    secret: UpdateClientSecret
    mask: _field_mask_pb2.FieldMask
    def __init__(self, client_id: _Optional[str] = ..., secret_id: _Optional[str] = ..., secret: _Optional[_Union[UpdateClientSecret, _Mapping]] = ..., mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateClientSecret(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ClientSecretStatus
    def __init__(self, status: _Optional[_Union[ClientSecretStatus, str]] = ...) -> None: ...

class UpdateClientSecretResponse(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: ClientSecret
    def __init__(self, secret: _Optional[_Union[ClientSecret, _Mapping]] = ...) -> None: ...

class DeleteClientSecretRequest(_message.Message):
    __slots__ = ("client_id", "secret_id")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    secret_id: str
    def __init__(self, client_id: _Optional[str] = ..., secret_id: _Optional[str] = ...) -> None: ...

class Client(_message.Message):
    __slots__ = ("id", "keyId", "create_time", "update_time", "redirect_uris", "default_redirect_uri", "secrets", "post_logout_redirect_uris", "back_channel_logout_uri")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEYID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REDIRECT_URI_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    POST_LOGOUT_REDIRECT_URIS_FIELD_NUMBER: _ClassVar[int]
    BACK_CHANNEL_LOGOUT_URI_FIELD_NUMBER: _ClassVar[int]
    id: str
    keyId: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    default_redirect_uri: str
    secrets: _containers.RepeatedCompositeFieldContainer[ClientSecret]
    post_logout_redirect_uris: _containers.RepeatedScalarFieldContainer[str]
    back_channel_logout_uri: str
    def __init__(self, id: _Optional[str] = ..., keyId: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., redirect_uris: _Optional[_Iterable[str]] = ..., default_redirect_uri: _Optional[str] = ..., secrets: _Optional[_Iterable[_Union[ClientSecret, _Mapping]]] = ..., post_logout_redirect_uris: _Optional[_Iterable[str]] = ..., back_channel_logout_uri: _Optional[str] = ...) -> None: ...

class ClientSecret(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "secret_suffix", "created_by", "status", "expire_time", "last_used_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    SECRET_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    secret_suffix: str
    created_by: str
    status: ClientSecretStatus
    expire_time: _timestamp_pb2.Timestamp
    last_used_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., secret_suffix: _Optional[str] = ..., created_by: _Optional[str] = ..., status: _Optional[_Union[ClientSecretStatus, str]] = ..., expire_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_used_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

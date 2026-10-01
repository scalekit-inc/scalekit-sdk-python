from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TriggerMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_MODE_UNSPECIFIED: _ClassVar[TriggerMode]
    WEBHOOK: _ClassVar[TriggerMode]
    POLL: _ClassVar[TriggerMode]

class TriggerSubscriptionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_SUBSCRIPTION_STATUS_UNSPECIFIED: _ClassVar[TriggerSubscriptionStatus]
    ACTIVE: _ClassVar[TriggerSubscriptionStatus]
    THROTTLED: _ClassVar[TriggerSubscriptionStatus]
    PAUSED: _ClassVar[TriggerSubscriptionStatus]
    PAUSED_CREDENTIAL: _ClassVar[TriggerSubscriptionStatus]
TRIGGER_MODE_UNSPECIFIED: TriggerMode
WEBHOOK: TriggerMode
POLL: TriggerMode
TRIGGER_SUBSCRIPTION_STATUS_UNSPECIFIED: TriggerSubscriptionStatus
ACTIVE: TriggerSubscriptionStatus
THROTTLED: TriggerSubscriptionStatus
PAUSED: TriggerSubscriptionStatus
PAUSED_CREDENTIAL: TriggerSubscriptionStatus

class RequiredScope(_message.Message):
    __slots__ = ("scope", "grant")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    GRANT_FIELD_NUMBER: _ClassVar[int]
    scope: str
    grant: str
    def __init__(self, scope: _Optional[str] = ..., grant: _Optional[str] = ...) -> None: ...

class ConfigField(_message.Message):
    __slots__ = ("key", "display_name", "help_text", "placeholder", "required")
    KEY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    HELP_TEXT_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDER_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    key: str
    display_name: str
    help_text: str
    placeholder: str
    required: bool
    def __init__(self, key: _Optional[str] = ..., display_name: _Optional[str] = ..., help_text: _Optional[str] = ..., placeholder: _Optional[str] = ..., required: bool = ...) -> None: ...

class AvailableTrigger(_message.Message):
    __slots__ = ("name", "display_name", "description", "provider", "mode", "setup", "required_scopes", "min_interval_seconds", "default_interval_seconds", "config_fields", "available", "reason", "remedy", "delivery_scope")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    SETUP_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_SCOPES_FIELD_NUMBER: _ClassVar[int]
    MIN_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELDS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REMEDY_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_SCOPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    description: str
    provider: str
    mode: TriggerMode
    setup: str
    required_scopes: _containers.RepeatedCompositeFieldContainer[RequiredScope]
    min_interval_seconds: int
    default_interval_seconds: int
    config_fields: _containers.RepeatedCompositeFieldContainer[ConfigField]
    available: bool
    reason: str
    remedy: str
    delivery_scope: str
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., provider: _Optional[str] = ..., mode: _Optional[_Union[TriggerMode, str]] = ..., setup: _Optional[str] = ..., required_scopes: _Optional[_Iterable[_Union[RequiredScope, _Mapping]]] = ..., min_interval_seconds: _Optional[int] = ..., default_interval_seconds: _Optional[int] = ..., config_fields: _Optional[_Iterable[_Union[ConfigField, _Mapping]]] = ..., available: bool = ..., reason: _Optional[str] = ..., remedy: _Optional[str] = ..., delivery_scope: _Optional[str] = ...) -> None: ...

class EligibleAccount(_message.Message):
    __slots__ = ("id", "identifier", "eligible", "reason", "remedy")
    ID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ELIGIBLE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REMEDY_FIELD_NUMBER: _ClassVar[int]
    id: str
    identifier: str
    eligible: bool
    reason: str
    remedy: str
    def __init__(self, id: _Optional[str] = ..., identifier: _Optional[str] = ..., eligible: bool = ..., reason: _Optional[str] = ..., remedy: _Optional[str] = ...) -> None: ...

class TriggerSubscription(_message.Message):
    __slots__ = ("id", "connected_account_id", "connection_id", "provider", "trigger_name", "status", "requested_interval_seconds", "effective_interval_seconds", "config", "delivery_scope")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_SCOPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    connected_account_id: str
    connection_id: str
    provider: str
    trigger_name: str
    status: TriggerSubscriptionStatus
    requested_interval_seconds: int
    effective_interval_seconds: int
    config: _containers.ScalarMap[str, str]
    delivery_scope: str
    def __init__(self, id: _Optional[str] = ..., connected_account_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., provider: _Optional[str] = ..., trigger_name: _Optional[str] = ..., status: _Optional[_Union[TriggerSubscriptionStatus, str]] = ..., requested_interval_seconds: _Optional[int] = ..., effective_interval_seconds: _Optional[int] = ..., config: _Optional[_Mapping[str, str]] = ..., delivery_scope: _Optional[str] = ...) -> None: ...

class ListAvailableTriggersRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class ListAvailableTriggersResponse(_message.Message):
    __slots__ = ("triggers",)
    TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    triggers: _containers.RepeatedCompositeFieldContainer[AvailableTrigger]
    def __init__(self, triggers: _Optional[_Iterable[_Union[AvailableTrigger, _Mapping]]] = ...) -> None: ...

class ListEligibleAccountsRequest(_message.Message):
    __slots__ = ("connection_id", "trigger_name")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    trigger_name: str
    def __init__(self, connection_id: _Optional[str] = ..., trigger_name: _Optional[str] = ...) -> None: ...

class ListEligibleAccountsResponse(_message.Message):
    __slots__ = ("accounts", "hidden_count")
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[EligibleAccount]
    hidden_count: int
    def __init__(self, accounts: _Optional[_Iterable[_Union[EligibleAccount, _Mapping]]] = ..., hidden_count: _Optional[int] = ...) -> None: ...

class ListTriggerSubscriptionsRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class ListTriggerSubscriptionsResponse(_message.Message):
    __slots__ = ("subscriptions",)
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    subscriptions: _containers.RepeatedCompositeFieldContainer[TriggerSubscription]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[TriggerSubscription, _Mapping]]] = ...) -> None: ...

class CreateTriggerSubscriptionRequest(_message.Message):
    __slots__ = ("connection_id", "connected_account_id", "trigger_name", "interval_seconds", "config")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connected_account_id: str
    trigger_name: str
    interval_seconds: int
    config: _containers.ScalarMap[str, str]
    def __init__(self, connection_id: _Optional[str] = ..., connected_account_id: _Optional[str] = ..., trigger_name: _Optional[str] = ..., interval_seconds: _Optional[int] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DeleteTriggerSubscriptionRequest(_message.Message):
    __slots__ = ("connection_id", "subscription_id")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    subscription_id: str
    def __init__(self, connection_id: _Optional[str] = ..., subscription_id: _Optional[str] = ...) -> None: ...

class TriggerIngressEndpoint(_message.Message):
    __slots__ = ("id", "connection_id", "url", "signing_secret_configured", "masked_signing_secret", "rotation_in_progress", "previous_signing_secret_expires_at", "signing_secret_rotation_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_CONFIGURED_FIELD_NUMBER: _ClassVar[int]
    MASKED_SIGNING_SECRET_FIELD_NUMBER: _ClassVar[int]
    ROTATION_IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_SIGNING_SECRET_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_ROTATION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    connection_id: str
    url: str
    signing_secret_configured: bool
    masked_signing_secret: str
    rotation_in_progress: bool
    previous_signing_secret_expires_at: _timestamp_pb2.Timestamp
    signing_secret_rotation_id: int
    def __init__(self, id: _Optional[str] = ..., connection_id: _Optional[str] = ..., url: _Optional[str] = ..., signing_secret_configured: bool = ..., masked_signing_secret: _Optional[str] = ..., rotation_in_progress: bool = ..., previous_signing_secret_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., signing_secret_rotation_id: _Optional[int] = ...) -> None: ...

class GetTriggerIngressEndpointRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class SetTriggerSigningSecretRequest(_message.Message):
    __slots__ = ("connection_id", "signing_secret")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    signing_secret: str
    def __init__(self, connection_id: _Optional[str] = ..., signing_secret: _Optional[str] = ...) -> None: ...

class ConfirmTriggerSigningSecretRotationRequest(_message.Message):
    __slots__ = ("connection_id", "signing_secret_rotation_id")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNING_SECRET_ROTATION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    signing_secret_rotation_id: int
    def __init__(self, connection_id: _Optional[str] = ..., signing_secret_rotation_id: _Optional[int] = ...) -> None: ...

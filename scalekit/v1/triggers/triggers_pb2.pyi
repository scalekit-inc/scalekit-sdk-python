from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class TriggerDeliveryScope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_DELIVERY_SCOPE_UNSPECIFIED: _ClassVar[TriggerDeliveryScope]
    ACCOUNT: _ClassVar[TriggerDeliveryScope]
    CONNECTION: _ClassVar[TriggerDeliveryScope]

class TriggerPlatformCredentials(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_PLATFORM_CREDENTIALS_UNSPECIFIED: _ClassVar[TriggerPlatformCredentials]
    SUPPORTED: _ClassVar[TriggerPlatformCredentials]
    UNSUPPORTED: _ClassVar[TriggerPlatformCredentials]

class TriggerRefusalCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_REFUSAL_CODE_UNSPECIFIED: _ClassVar[TriggerRefusalCode]
    SHARED_APP: _ClassVar[TriggerRefusalCode]
    POLL_CONNECTION_SCOPE: _ClassVar[TriggerRefusalCode]

class AccountHealthState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACCOUNT_HEALTH_STATE_UNSPECIFIED: _ClassVar[AccountHealthState]
    READY: _ClassVar[AccountHealthState]
    AWAITING_CONFIRMATION: _ClassVar[AccountHealthState]
    WRONG_APP: _ClassVar[AccountHealthState]
    DISCONNECTED: _ClassVar[AccountHealthState]
    NEEDS_REAUTHENTICATION: _ClassVar[AccountHealthState]

class AccountHealthAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACCOUNT_HEALTH_ACTION_UNSPECIFIED: _ClassVar[AccountHealthAction]
    RECONNECT: _ClassVar[AccountHealthAction]
    COMPLETE_SETUP: _ClassVar[AccountHealthAction]

class TriggerSubscriptionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_SUBSCRIPTION_STATUS_UNSPECIFIED: _ClassVar[TriggerSubscriptionStatus]
    ACTIVE: _ClassVar[TriggerSubscriptionStatus]
    THROTTLED: _ClassVar[TriggerSubscriptionStatus]
    PAUSED: _ClassVar[TriggerSubscriptionStatus]
    PAUSED_CREDENTIAL: _ClassVar[TriggerSubscriptionStatus]

class TriggerPollErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_POLL_ERROR_CODE_UNSPECIFIED: _ClassVar[TriggerPollErrorCode]
    RATE_LIMITED: _ClassVar[TriggerPollErrorCode]
    CREDENTIAL_REVOKED: _ClassVar[TriggerPollErrorCode]
    INVALID_CONFIGURATION: _ClassVar[TriggerPollErrorCode]
    PROVIDER_ERROR: _ClassVar[TriggerPollErrorCode]
    DELIVERY_FAILED: _ClassVar[TriggerPollErrorCode]
    TIMED_OUT: _ClassVar[TriggerPollErrorCode]
    POLL_FAILED: _ClassVar[TriggerPollErrorCode]

class BatchSubscribeOutcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATCH_SUBSCRIBE_OUTCOME_UNSPECIFIED: _ClassVar[BatchSubscribeOutcome]
    CREATED: _ClassVar[BatchSubscribeOutcome]
    ALREADY_SUBSCRIBED: _ClassVar[BatchSubscribeOutcome]
    REFUSED: _ClassVar[BatchSubscribeOutcome]
    NOT_FOUND: _ClassVar[BatchSubscribeOutcome]
    FAILED: _ClassVar[BatchSubscribeOutcome]

class TriggerDeliveryAttemptStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRIGGER_DELIVERY_ATTEMPT_STATUS_UNSPECIFIED: _ClassVar[TriggerDeliveryAttemptStatus]
    SUCCESS: _ClassVar[TriggerDeliveryAttemptStatus]
    PENDING: _ClassVar[TriggerDeliveryAttemptStatus]
    FAIL: _ClassVar[TriggerDeliveryAttemptStatus]
    SENDING: _ClassVar[TriggerDeliveryAttemptStatus]
    CANCELED: _ClassVar[TriggerDeliveryAttemptStatus]
TRIGGER_MODE_UNSPECIFIED: TriggerMode
WEBHOOK: TriggerMode
POLL: TriggerMode
TRIGGER_DELIVERY_SCOPE_UNSPECIFIED: TriggerDeliveryScope
ACCOUNT: TriggerDeliveryScope
CONNECTION: TriggerDeliveryScope
TRIGGER_PLATFORM_CREDENTIALS_UNSPECIFIED: TriggerPlatformCredentials
SUPPORTED: TriggerPlatformCredentials
UNSUPPORTED: TriggerPlatformCredentials
TRIGGER_REFUSAL_CODE_UNSPECIFIED: TriggerRefusalCode
SHARED_APP: TriggerRefusalCode
POLL_CONNECTION_SCOPE: TriggerRefusalCode
ACCOUNT_HEALTH_STATE_UNSPECIFIED: AccountHealthState
READY: AccountHealthState
AWAITING_CONFIRMATION: AccountHealthState
WRONG_APP: AccountHealthState
DISCONNECTED: AccountHealthState
NEEDS_REAUTHENTICATION: AccountHealthState
ACCOUNT_HEALTH_ACTION_UNSPECIFIED: AccountHealthAction
RECONNECT: AccountHealthAction
COMPLETE_SETUP: AccountHealthAction
TRIGGER_SUBSCRIPTION_STATUS_UNSPECIFIED: TriggerSubscriptionStatus
ACTIVE: TriggerSubscriptionStatus
THROTTLED: TriggerSubscriptionStatus
PAUSED: TriggerSubscriptionStatus
PAUSED_CREDENTIAL: TriggerSubscriptionStatus
TRIGGER_POLL_ERROR_CODE_UNSPECIFIED: TriggerPollErrorCode
RATE_LIMITED: TriggerPollErrorCode
CREDENTIAL_REVOKED: TriggerPollErrorCode
INVALID_CONFIGURATION: TriggerPollErrorCode
PROVIDER_ERROR: TriggerPollErrorCode
DELIVERY_FAILED: TriggerPollErrorCode
TIMED_OUT: TriggerPollErrorCode
POLL_FAILED: TriggerPollErrorCode
BATCH_SUBSCRIBE_OUTCOME_UNSPECIFIED: BatchSubscribeOutcome
CREATED: BatchSubscribeOutcome
ALREADY_SUBSCRIBED: BatchSubscribeOutcome
REFUSED: BatchSubscribeOutcome
NOT_FOUND: BatchSubscribeOutcome
FAILED: BatchSubscribeOutcome
TRIGGER_DELIVERY_ATTEMPT_STATUS_UNSPECIFIED: TriggerDeliveryAttemptStatus
SUCCESS: TriggerDeliveryAttemptStatus
PENDING: TriggerDeliveryAttemptStatus
FAIL: TriggerDeliveryAttemptStatus
SENDING: TriggerDeliveryAttemptStatus
CANCELED: TriggerDeliveryAttemptStatus

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
    __slots__ = ("name", "display_name", "description", "provider", "mode", "required_scopes", "min_interval_seconds", "default_interval_seconds", "config_fields", "available", "reason", "remedy", "delivery_scope", "platform_credentials", "refusal_code", "requires_signing_secret", "register_hint", "secret_hint")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_SCOPES_FIELD_NUMBER: _ClassVar[int]
    MIN_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELDS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REMEDY_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_SCOPE_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    REFUSAL_CODE_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_SIGNING_SECRET_FIELD_NUMBER: _ClassVar[int]
    REGISTER_HINT_FIELD_NUMBER: _ClassVar[int]
    SECRET_HINT_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    description: str
    provider: str
    mode: TriggerMode
    required_scopes: _containers.RepeatedCompositeFieldContainer[RequiredScope]
    min_interval_seconds: int
    default_interval_seconds: int
    config_fields: _containers.RepeatedCompositeFieldContainer[ConfigField]
    available: bool
    reason: str
    remedy: str
    delivery_scope: TriggerDeliveryScope
    platform_credentials: TriggerPlatformCredentials
    refusal_code: TriggerRefusalCode
    requires_signing_secret: bool
    register_hint: str
    secret_hint: str
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., provider: _Optional[str] = ..., mode: _Optional[_Union[TriggerMode, str]] = ..., required_scopes: _Optional[_Iterable[_Union[RequiredScope, _Mapping]]] = ..., min_interval_seconds: _Optional[int] = ..., default_interval_seconds: _Optional[int] = ..., config_fields: _Optional[_Iterable[_Union[ConfigField, _Mapping]]] = ..., available: bool = ..., reason: _Optional[str] = ..., remedy: _Optional[str] = ..., delivery_scope: _Optional[_Union[TriggerDeliveryScope, str]] = ..., platform_credentials: _Optional[_Union[TriggerPlatformCredentials, str]] = ..., refusal_code: _Optional[_Union[TriggerRefusalCode, str]] = ..., requires_signing_secret: bool = ..., register_hint: _Optional[str] = ..., secret_hint: _Optional[str] = ...) -> None: ...

class EligibleAccount(_message.Message):
    __slots__ = ("id", "identifier", "eligible", "reason", "remedy", "health")
    ID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    ELIGIBLE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REMEDY_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    id: str
    identifier: str
    eligible: bool
    reason: str
    remedy: str
    health: AccountHealth
    def __init__(self, id: _Optional[str] = ..., identifier: _Optional[str] = ..., eligible: bool = ..., reason: _Optional[str] = ..., remedy: _Optional[str] = ..., health: _Optional[_Union[AccountHealth, _Mapping]] = ...) -> None: ...

class AccountHealth(_message.Message):
    __slots__ = ("state", "reason", "remedy", "action", "blocks_tool_calls")
    STATE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REMEDY_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    state: AccountHealthState
    reason: str
    remedy: str
    action: AccountHealthAction
    blocks_tool_calls: bool
    def __init__(self, state: _Optional[_Union[AccountHealthState, str]] = ..., reason: _Optional[str] = ..., remedy: _Optional[str] = ..., action: _Optional[_Union[AccountHealthAction, str]] = ..., blocks_tool_calls: bool = ...) -> None: ...

class TriggerSubscription(_message.Message):
    __slots__ = ("id", "connected_account_id", "connection_id", "provider", "trigger_name", "status", "requested_interval_seconds", "effective_interval_seconds", "config", "delivery_scope", "connected_account_identifier", "created_at", "poll_state", "account_health")
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
    CONNECTED_ACCOUNT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    POLL_STATE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_HEALTH_FIELD_NUMBER: _ClassVar[int]
    id: str
    connected_account_id: str
    connection_id: str
    provider: str
    trigger_name: str
    status: TriggerSubscriptionStatus
    requested_interval_seconds: int
    effective_interval_seconds: int
    config: _containers.ScalarMap[str, str]
    delivery_scope: TriggerDeliveryScope
    connected_account_identifier: str
    created_at: _timestamp_pb2.Timestamp
    poll_state: TriggerPollState
    account_health: AccountHealthState
    def __init__(self, id: _Optional[str] = ..., connected_account_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., provider: _Optional[str] = ..., trigger_name: _Optional[str] = ..., status: _Optional[_Union[TriggerSubscriptionStatus, str]] = ..., requested_interval_seconds: _Optional[int] = ..., effective_interval_seconds: _Optional[int] = ..., config: _Optional[_Mapping[str, str]] = ..., delivery_scope: _Optional[_Union[TriggerDeliveryScope, str]] = ..., connected_account_identifier: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., poll_state: _Optional[_Union[TriggerPollState, _Mapping]] = ..., account_health: _Optional[_Union[AccountHealthState, str]] = ...) -> None: ...

class TriggerPollState(_message.Message):
    __slots__ = ("last_run_at", "last_error", "consecutive_failures", "backoff_until", "watermark_updated_at", "last_error_code")
    LAST_RUN_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_ERROR_FIELD_NUMBER: _ClassVar[int]
    CONSECUTIVE_FAILURES_FIELD_NUMBER: _ClassVar[int]
    BACKOFF_UNTIL_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    last_run_at: _timestamp_pb2.Timestamp
    last_error: str
    consecutive_failures: int
    backoff_until: _timestamp_pb2.Timestamp
    watermark_updated_at: _timestamp_pb2.Timestamp
    last_error_code: TriggerPollErrorCode
    def __init__(self, last_run_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_error: _Optional[str] = ..., consecutive_failures: _Optional[int] = ..., backoff_until: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., watermark_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_error_code: _Optional[_Union[TriggerPollErrorCode, str]] = ...) -> None: ...

class ListAvailableTriggersRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class ListAvailableTriggersResponse(_message.Message):
    __slots__ = ("triggers", "connection_uses_shared_app")
    TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_USES_SHARED_APP_FIELD_NUMBER: _ClassVar[int]
    triggers: _containers.RepeatedCompositeFieldContainer[AvailableTrigger]
    connection_uses_shared_app: bool
    def __init__(self, triggers: _Optional[_Iterable[_Union[AvailableTrigger, _Mapping]]] = ..., connection_uses_shared_app: bool = ...) -> None: ...

class ListEligibleAccountsRequest(_message.Message):
    __slots__ = ("connection_id", "trigger_name", "query", "page_size", "page_token")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    trigger_name: str
    query: str
    page_size: int
    page_token: str
    def __init__(self, connection_id: _Optional[str] = ..., trigger_name: _Optional[str] = ..., query: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListEligibleAccountsResponse(_message.Message):
    __slots__ = ("accounts", "next_page_token", "prev_page_token", "total_size")
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[EligibleAccount]
    next_page_token: str
    prev_page_token: str
    total_size: int
    def __init__(self, accounts: _Optional[_Iterable[_Union[EligibleAccount, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class ListTriggerSubscriptionsRequest(_message.Message):
    __slots__ = ("connection_id", "trigger_name", "statuses", "page_size", "page_token")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    trigger_name: str
    statuses: _containers.RepeatedScalarFieldContainer[TriggerSubscriptionStatus]
    page_size: int
    page_token: str
    def __init__(self, connection_id: _Optional[str] = ..., trigger_name: _Optional[str] = ..., statuses: _Optional[_Iterable[_Union[TriggerSubscriptionStatus, str]]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListTriggerSubscriptionsResponse(_message.Message):
    __slots__ = ("subscriptions", "next_page_token", "prev_page_token", "total_size", "status_counts")
    class StatusCountsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PREV_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    STATUS_COUNTS_FIELD_NUMBER: _ClassVar[int]
    subscriptions: _containers.RepeatedCompositeFieldContainer[TriggerSubscription]
    next_page_token: str
    prev_page_token: str
    total_size: int
    status_counts: _containers.ScalarMap[str, int]
    def __init__(self, subscriptions: _Optional[_Iterable[_Union[TriggerSubscription, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., prev_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., status_counts: _Optional[_Mapping[str, int]] = ...) -> None: ...

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

class BatchCreateTriggerSubscriptionsRequest(_message.Message):
    __slots__ = ("connection_id", "connected_account_ids", "trigger_name", "interval_seconds", "config")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_NAME_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connected_account_ids: _containers.RepeatedScalarFieldContainer[str]
    trigger_name: str
    interval_seconds: int
    config: _containers.ScalarMap[str, str]
    def __init__(self, connection_id: _Optional[str] = ..., connected_account_ids: _Optional[_Iterable[str]] = ..., trigger_name: _Optional[str] = ..., interval_seconds: _Optional[int] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class BatchCreateTriggerSubscriptionResult(_message.Message):
    __slots__ = ("connected_account_id", "outcome", "subscription", "reason")
    CONNECTED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    connected_account_id: str
    outcome: BatchSubscribeOutcome
    subscription: TriggerSubscription
    reason: str
    def __init__(self, connected_account_id: _Optional[str] = ..., outcome: _Optional[_Union[BatchSubscribeOutcome, str]] = ..., subscription: _Optional[_Union[TriggerSubscription, _Mapping]] = ..., reason: _Optional[str] = ...) -> None: ...

class BatchCreateTriggerSubscriptionsResponse(_message.Message):
    __slots__ = ("results", "created_count")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_COUNT_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[BatchCreateTriggerSubscriptionResult]
    created_count: int
    def __init__(self, results: _Optional[_Iterable[_Union[BatchCreateTriggerSubscriptionResult, _Mapping]]] = ..., created_count: _Optional[int] = ...) -> None: ...

class DeleteTriggerSubscriptionRequest(_message.Message):
    __slots__ = ("connection_id", "subscription_id")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    subscription_id: str
    def __init__(self, connection_id: _Optional[str] = ..., subscription_id: _Optional[str] = ...) -> None: ...

class GetTriggerActivityRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTriggerActivityResponse(_message.Message):
    __slots__ = ("counts", "window_hours", "signature_banner", "degraded", "explains_individual_events", "delivery_details_path")
    class CountsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    WINDOW_HOURS_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_BANNER_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    EXPLAINS_INDIVIDUAL_EVENTS_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_DETAILS_PATH_FIELD_NUMBER: _ClassVar[int]
    counts: _containers.ScalarMap[str, int]
    window_hours: int
    signature_banner: bool
    degraded: bool
    explains_individual_events: bool
    delivery_details_path: str
    def __init__(self, counts: _Optional[_Mapping[str, int]] = ..., window_hours: _Optional[int] = ..., signature_banner: bool = ..., degraded: bool = ..., explains_individual_events: bool = ..., delivery_details_path: _Optional[str] = ...) -> None: ...

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

class CreateTriggerIngressEndpointRequest(_message.Message):
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

class SyncTriggerDefinitionsRequest(_message.Message):
    __slots__ = ("provider", "definitions", "provider_metadata")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_METADATA_FIELD_NUMBER: _ClassVar[int]
    provider: str
    definitions: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    provider_metadata: _struct_pb2.Struct
    def __init__(self, provider: _Optional[str] = ..., definitions: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., provider_metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SyncTriggerDefinitionsResponse(_message.Message):
    __slots__ = ("provider", "submitted", "stored", "skipped_drafts", "identity_declared")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    SUBMITTED_FIELD_NUMBER: _ClassVar[int]
    STORED_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_DRAFTS_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_DECLARED_FIELD_NUMBER: _ClassVar[int]
    provider: str
    submitted: int
    stored: int
    skipped_drafts: _containers.RepeatedScalarFieldContainer[str]
    identity_declared: bool
    def __init__(self, provider: _Optional[str] = ..., submitted: _Optional[int] = ..., stored: _Optional[int] = ..., skipped_drafts: _Optional[_Iterable[str]] = ..., identity_declared: bool = ...) -> None: ...

class ListTriggerDeliveryAttemptsByEndpointRequest(_message.Message):
    __slots__ = ("endpoint_id", "page_size")
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    endpoint_id: str
    page_size: int
    def __init__(self, endpoint_id: _Optional[str] = ..., page_size: _Optional[int] = ...) -> None: ...

class ListTriggerDeliveryAttemptsByEndpointResponse(_message.Message):
    __slots__ = ("attempts",)
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    attempts: _containers.RepeatedCompositeFieldContainer[TriggerDeliveryAttempt]
    def __init__(self, attempts: _Optional[_Iterable[_Union[TriggerDeliveryAttempt, _Mapping]]] = ...) -> None: ...

class TriggerDeliveryAttempt(_message.Message):
    __slots__ = ("id", "endpoint_id", "msg_id", "status", "response_status_code", "response", "timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    endpoint_id: str
    msg_id: str
    status: TriggerDeliveryAttemptStatus
    response_status_code: int
    response: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., endpoint_id: _Optional[str] = ..., msg_id: _Optional[str] = ..., status: _Optional[_Union[TriggerDeliveryAttemptStatus, str]] = ..., response_status_code: _Optional[int] = ..., response: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TriggerWebhookWrapperRequest(_message.Message):
    __slots__ = ("request_body",)
    REQUEST_BODY_FIELD_NUMBER: _ClassVar[int]
    request_body: _struct_pb2.Struct
    def __init__(self, request_body: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

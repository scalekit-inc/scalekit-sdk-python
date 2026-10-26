from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntitlementKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTITLEMENT_KIND_UNSPECIFIED: _ClassVar[EntitlementKind]
    VOLUME: _ClassVar[EntitlementKind]
    FLAT: _ClassVar[EntitlementKind]
    BOOLEAN: _ClassVar[EntitlementKind]
    SCALAR: _ClassVar[EntitlementKind]

class Grant(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GRANT_UNSPECIFIED: _ClassVar[Grant]
    INCLUDED: _ClassVar[Grant]
    PURCHASABLE: _ClassVar[Grant]
    ABSENT: _ClassVar[Grant]

class OnExceed(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ON_EXCEED_UNSPECIFIED: _ClassVar[OnExceed]
    BILL: _ClassVar[OnExceed]
    BLOCK: _ClassVar[OnExceed]
    UPGRADE: _ClassVar[OnExceed]

class BillingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_MODE_UNSPECIFIED: _ClassVar[BillingMode]
    STRIPE: _ClassVar[BillingMode]
    METRONOME: _ClassVar[BillingMode]

class BillingAccountStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_ACCOUNT_STATUS_UNSPECIFIED: _ClassVar[BillingAccountStatus]
    PENDING: _ClassVar[BillingAccountStatus]
    ACTIVE: _ClassVar[BillingAccountStatus]
    SUSPENDED: _ClassVar[BillingAccountStatus]

class CardStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CARD_STATUS_UNSPECIFIED: _ClassVar[CardStatus]
    NONE: _ClassVar[CardStatus]
    CARD_PENDING: _ClassVar[CardStatus]
    VERIFIED: _ClassVar[CardStatus]

class PaymentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_STATUS_UNSPECIFIED: _ClassVar[PaymentStatus]
    CURRENT: _ClassVar[PaymentStatus]
    PAST_DUE: _ClassVar[PaymentStatus]

class ContractStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTRACT_STATUS_UNSPECIFIED: _ClassVar[ContractStatus]
    CONTRACT_ACTIVE: _ClassVar[ContractStatus]
    CONTRACT_ARCHIVED: _ClassVar[ContractStatus]
    CONTRACT_PROVISIONING: _ClassVar[ContractStatus]
ENTITLEMENT_KIND_UNSPECIFIED: EntitlementKind
VOLUME: EntitlementKind
FLAT: EntitlementKind
BOOLEAN: EntitlementKind
SCALAR: EntitlementKind
GRANT_UNSPECIFIED: Grant
INCLUDED: Grant
PURCHASABLE: Grant
ABSENT: Grant
ON_EXCEED_UNSPECIFIED: OnExceed
BILL: OnExceed
BLOCK: OnExceed
UPGRADE: OnExceed
BILLING_MODE_UNSPECIFIED: BillingMode
STRIPE: BillingMode
METRONOME: BillingMode
BILLING_ACCOUNT_STATUS_UNSPECIFIED: BillingAccountStatus
PENDING: BillingAccountStatus
ACTIVE: BillingAccountStatus
SUSPENDED: BillingAccountStatus
CARD_STATUS_UNSPECIFIED: CardStatus
NONE: CardStatus
CARD_PENDING: CardStatus
VERIFIED: CardStatus
PAYMENT_STATUS_UNSPECIFIED: PaymentStatus
CURRENT: PaymentStatus
PAST_DUE: PaymentStatus
CONTRACT_STATUS_UNSPECIFIED: ContractStatus
CONTRACT_ACTIVE: ContractStatus
CONTRACT_ARCHIVED: ContractStatus
CONTRACT_PROVISIONING: ContractStatus

class GetBillingCatalogRequest(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    def __init__(self, version: _Optional[int] = ...) -> None: ...

class GetBillingCatalogResponse(_message.Message):
    __slots__ = ("version", "pinned", "currency", "lines")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    version: int
    pinned: bool
    currency: str
    lines: _containers.RepeatedCompositeFieldContainer[ProductLine]
    def __init__(self, version: _Optional[int] = ..., pinned: bool = ..., currency: _Optional[str] = ..., lines: _Optional[_Iterable[_Union[ProductLine, _Mapping]]] = ...) -> None: ...

class ProductLine(_message.Message):
    __slots__ = ("key", "display_name", "plans")
    KEY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    key: str
    display_name: str
    plans: _containers.RepeatedCompositeFieldContainer[Plan]
    def __init__(self, key: _Optional[str] = ..., display_name: _Optional[str] = ..., plans: _Optional[_Iterable[_Union[Plan, _Mapping]]] = ...) -> None: ...

class Plan(_message.Message):
    __slots__ = ("tier", "base_fee", "negotiated", "entitlements")
    TIER_FIELD_NUMBER: _ClassVar[int]
    BASE_FEE_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATED_FIELD_NUMBER: _ClassVar[int]
    ENTITLEMENTS_FIELD_NUMBER: _ClassVar[int]
    tier: str
    base_fee: Money
    negotiated: bool
    entitlements: _containers.RepeatedCompositeFieldContainer[Entitlement]
    def __init__(self, tier: _Optional[str] = ..., base_fee: _Optional[_Union[Money, _Mapping]] = ..., negotiated: bool = ..., entitlements: _Optional[_Iterable[_Union[Entitlement, _Mapping]]] = ...) -> None: ...

class Entitlement(_message.Message):
    __slots__ = ("key", "display_name", "kind", "allowance", "price", "grant", "value", "highlight", "display_order")
    KEY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    GRANT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_ORDER_FIELD_NUMBER: _ClassVar[int]
    key: str
    display_name: str
    kind: EntitlementKind
    allowance: Allowance
    price: Money
    grant: Grant
    value: str
    highlight: bool
    display_order: int
    def __init__(self, key: _Optional[str] = ..., display_name: _Optional[str] = ..., kind: _Optional[_Union[EntitlementKind, str]] = ..., allowance: _Optional[_Union[Allowance, _Mapping]] = ..., price: _Optional[_Union[Money, _Mapping]] = ..., grant: _Optional[_Union[Grant, str]] = ..., value: _Optional[str] = ..., highlight: bool = ..., display_order: _Optional[int] = ...) -> None: ...

class Allowance(_message.Message):
    __slots__ = ("included", "unlimited", "negotiated", "unit", "on_exceed", "overage")
    INCLUDED_FIELD_NUMBER: _ClassVar[int]
    UNLIMITED_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATED_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    ON_EXCEED_FIELD_NUMBER: _ClassVar[int]
    OVERAGE_FIELD_NUMBER: _ClassVar[int]
    included: int
    unlimited: bool
    negotiated: bool
    unit: str
    on_exceed: OnExceed
    overage: _containers.RepeatedCompositeFieldContainer[Tier]
    def __init__(self, included: _Optional[int] = ..., unlimited: bool = ..., negotiated: bool = ..., unit: _Optional[str] = ..., on_exceed: _Optional[_Union[OnExceed, str]] = ..., overage: _Optional[_Iterable[_Union[Tier, _Mapping]]] = ...) -> None: ...

class Tier(_message.Message):
    __slots__ = ("size", "price")
    SIZE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    size: int
    price: Money
    def __init__(self, size: _Optional[int] = ..., price: _Optional[_Union[Money, _Mapping]] = ...) -> None: ...

class Money(_message.Message):
    __slots__ = ("amount",)
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    amount: str
    def __init__(self, amount: _Optional[str] = ...) -> None: ...

class GetBillingAccountRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingAccountResponse(_message.Message):
    __slots__ = ("status", "card_status", "payment_status", "catalog_version", "production_unlocked", "billing_mode", "stripe_customer_id", "metronome_customer_id", "billing_subscription_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CARD_STATUS_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CATALOG_VERSION_FIELD_NUMBER: _ClassVar[int]
    PRODUCTION_UNLOCKED_FIELD_NUMBER: _ClassVar[int]
    BILLING_MODE_FIELD_NUMBER: _ClassVar[int]
    STRIPE_CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    METRONOME_CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    status: BillingAccountStatus
    card_status: CardStatus
    payment_status: PaymentStatus
    catalog_version: int
    production_unlocked: bool
    billing_mode: BillingMode
    stripe_customer_id: str
    metronome_customer_id: str
    billing_subscription_id: str
    def __init__(self, status: _Optional[_Union[BillingAccountStatus, str]] = ..., card_status: _Optional[_Union[CardStatus, str]] = ..., payment_status: _Optional[_Union[PaymentStatus, str]] = ..., catalog_version: _Optional[int] = ..., production_unlocked: bool = ..., billing_mode: _Optional[_Union[BillingMode, str]] = ..., stripe_customer_id: _Optional[str] = ..., metronome_customer_id: _Optional[str] = ..., billing_subscription_id: _Optional[str] = ...) -> None: ...

class GetBillingConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingConfigResponse(_message.Message):
    __slots__ = ("publishable_key",)
    PUBLISHABLE_KEY_FIELD_NUMBER: _ClassVar[int]
    publishable_key: str
    def __init__(self, publishable_key: _Optional[str] = ...) -> None: ...

class AddPaymentMethodRequest(_message.Message):
    __slots__ = ("force",)
    FORCE_FIELD_NUMBER: _ClassVar[int]
    force: bool
    def __init__(self, force: bool = ...) -> None: ...

class AddPaymentMethodResponse(_message.Message):
    __slots__ = ("checkout_url", "status", "payment_method_on_file", "client_secret")
    CHECKOUT_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_ON_FILE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    checkout_url: str
    status: BillingAccountStatus
    payment_method_on_file: bool
    client_secret: str
    def __init__(self, checkout_url: _Optional[str] = ..., status: _Optional[_Union[BillingAccountStatus, str]] = ..., payment_method_on_file: bool = ..., client_secret: _Optional[str] = ...) -> None: ...

class ListEnvironmentBillingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListEnvironmentBillingResponse(_message.Message):
    __slots__ = ("environments",)
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    environments: _containers.RepeatedCompositeFieldContainer[EnvironmentBilling]
    def __init__(self, environments: _Optional[_Iterable[_Union[EnvironmentBilling, _Mapping]]] = ...) -> None: ...

class EnvironmentBilling(_message.Message):
    __slots__ = ("environment_id", "environment_name", "plans", "catalog_version", "contract_status", "add_ons", "purchasable_add_ons", "full_stack_auth", "period_start", "period_end")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    CATALOG_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_STATUS_FIELD_NUMBER: _ClassVar[int]
    ADD_ONS_FIELD_NUMBER: _ClassVar[int]
    PURCHASABLE_ADD_ONS_FIELD_NUMBER: _ClassVar[int]
    FULL_STACK_AUTH_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    environment_name: str
    plans: _containers.RepeatedCompositeFieldContainer[LinePlan]
    catalog_version: int
    contract_status: ContractStatus
    add_ons: _containers.RepeatedScalarFieldContainer[str]
    purchasable_add_ons: _containers.RepeatedScalarFieldContainer[str]
    full_stack_auth: bool
    period_start: str
    period_end: str
    def __init__(self, environment_id: _Optional[str] = ..., environment_name: _Optional[str] = ..., plans: _Optional[_Iterable[_Union[LinePlan, _Mapping]]] = ..., catalog_version: _Optional[int] = ..., contract_status: _Optional[_Union[ContractStatus, str]] = ..., add_ons: _Optional[_Iterable[str]] = ..., purchasable_add_ons: _Optional[_Iterable[str]] = ..., full_stack_auth: bool = ..., period_start: _Optional[str] = ..., period_end: _Optional[str] = ...) -> None: ...

class LinePlan(_message.Message):
    __slots__ = ("line", "tier")
    LINE_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    line: str
    tier: str
    def __init__(self, line: _Optional[str] = ..., tier: _Optional[str] = ...) -> None: ...

class UpdateBillingPlanRequest(_message.Message):
    __slots__ = ("plans", "add_ons")
    PLANS_FIELD_NUMBER: _ClassVar[int]
    ADD_ONS_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[LinePlan]
    add_ons: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, plans: _Optional[_Iterable[_Union[LinePlan, _Mapping]]] = ..., add_ons: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateBillingPlanResponse(_message.Message):
    __slots__ = ("plans", "add_ons", "exceeded")
    PLANS_FIELD_NUMBER: _ClassVar[int]
    ADD_ONS_FIELD_NUMBER: _ClassVar[int]
    EXCEEDED_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[LinePlan]
    add_ons: _containers.RepeatedScalarFieldContainer[str]
    exceeded: _containers.RepeatedCompositeFieldContainer[ExceededAllowance]
    def __init__(self, plans: _Optional[_Iterable[_Union[LinePlan, _Mapping]]] = ..., add_ons: _Optional[_Iterable[str]] = ..., exceeded: _Optional[_Iterable[_Union[ExceededAllowance, _Mapping]]] = ...) -> None: ...

class ExceededAllowance(_message.Message):
    __slots__ = ("entitlement", "line", "allowance", "current_usage", "on_exceed")
    ENTITLEMENT_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    ALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_USAGE_FIELD_NUMBER: _ClassVar[int]
    ON_EXCEED_FIELD_NUMBER: _ClassVar[int]
    entitlement: str
    line: str
    allowance: int
    current_usage: int
    on_exceed: OnExceed
    def __init__(self, entitlement: _Optional[str] = ..., line: _Optional[str] = ..., allowance: _Optional[int] = ..., current_usage: _Optional[int] = ..., on_exceed: _Optional[_Union[OnExceed, str]] = ...) -> None: ...

class GetBillingUsageRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingUsageResponse(_message.Message):
    __slots__ = ("metrics", "period_start", "period_end")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[MetricUsage]
    period_start: str
    period_end: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[MetricUsage, _Mapping]]] = ..., period_start: _Optional[str] = ..., period_end: _Optional[str] = ...) -> None: ...

class MetricUsage(_message.Message):
    __slots__ = ("entitlement", "line", "allowance", "current_usage", "display_name")
    ENTITLEMENT_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    ALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_USAGE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    entitlement: str
    line: str
    allowance: Allowance
    current_usage: float
    display_name: str
    def __init__(self, entitlement: _Optional[str] = ..., line: _Optional[str] = ..., allowance: _Optional[_Union[Allowance, _Mapping]] = ..., current_usage: _Optional[float] = ..., display_name: _Optional[str] = ...) -> None: ...

class GetBillingConnectionCountsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingConnectionCountsResponse(_message.Message):
    __slots__ = ("sso_connections", "scim_connections")
    SSO_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    SCIM_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    sso_connections: int
    scim_connections: int
    def __init__(self, sso_connections: _Optional[int] = ..., scim_connections: _Optional[int] = ...) -> None: ...

class GetInvoicesDashboardUrlRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetInvoicesDashboardUrlResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class GetSupportWorkspaceBillingRequest(_message.Message):
    __slots__ = ("workspace_id", "include_live")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_LIVE_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    include_live: bool
    def __init__(self, workspace_id: _Optional[str] = ..., include_live: bool = ...) -> None: ...

class GetSupportWorkspaceBillingResponse(_message.Message):
    __slots__ = ("account", "environments")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    account: SupportBillingAccount
    environments: _containers.RepeatedCompositeFieldContainer[SupportEnvironmentBilling]
    def __init__(self, account: _Optional[_Union[SupportBillingAccount, _Mapping]] = ..., environments: _Optional[_Iterable[_Union[SupportEnvironmentBilling, _Mapping]]] = ...) -> None: ...

class SupportBillingAccount(_message.Message):
    __slots__ = ("workspace_id", "billing_mode", "status", "catalog_version", "card_status", "production_card_exempt", "payment_status", "region", "test_workspace", "stripe_customer_id", "metronome_customer_id")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_MODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CATALOG_VERSION_FIELD_NUMBER: _ClassVar[int]
    CARD_STATUS_FIELD_NUMBER: _ClassVar[int]
    PRODUCTION_CARD_EXEMPT_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    TEST_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    STRIPE_CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    METRONOME_CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    billing_mode: BillingMode
    status: BillingAccountStatus
    catalog_version: int
    card_status: CardStatus
    production_card_exempt: bool
    payment_status: PaymentStatus
    region: str
    test_workspace: bool
    stripe_customer_id: str
    metronome_customer_id: str
    def __init__(self, workspace_id: _Optional[str] = ..., billing_mode: _Optional[_Union[BillingMode, str]] = ..., status: _Optional[_Union[BillingAccountStatus, str]] = ..., catalog_version: _Optional[int] = ..., card_status: _Optional[_Union[CardStatus, str]] = ..., production_card_exempt: bool = ..., payment_status: _Optional[_Union[PaymentStatus, str]] = ..., region: _Optional[str] = ..., test_workspace: bool = ..., stripe_customer_id: _Optional[str] = ..., metronome_customer_id: _Optional[str] = ...) -> None: ...

class SupportEnvironmentBilling(_message.Message):
    __slots__ = ("environment_id", "environment_name", "contract_id", "contract_status", "period_start", "period_end", "state", "etag", "live", "drift")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_STATUS_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_FIELD_NUMBER: _ClassVar[int]
    PERIOD_END_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    LIVE_FIELD_NUMBER: _ClassVar[int]
    DRIFT_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    environment_name: str
    contract_id: str
    contract_status: ContractStatus
    period_start: str
    period_end: str
    state: SupportBillingState
    etag: str
    live: SupportBillingState
    drift: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, environment_id: _Optional[str] = ..., environment_name: _Optional[str] = ..., contract_id: _Optional[str] = ..., contract_status: _Optional[_Union[ContractStatus, str]] = ..., period_start: _Optional[str] = ..., period_end: _Optional[str] = ..., state: _Optional[_Union[SupportBillingState, _Mapping]] = ..., etag: _Optional[str] = ..., live: _Optional[_Union[SupportBillingState, _Mapping]] = ..., drift: _Optional[_Iterable[str]] = ...) -> None: ...

class SupportBillingState(_message.Message):
    __slots__ = ("plans", "add_ons", "grants")
    PLANS_FIELD_NUMBER: _ClassVar[int]
    ADD_ONS_FIELD_NUMBER: _ClassVar[int]
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[LinePlan]
    add_ons: _containers.RepeatedScalarFieldContainer[str]
    grants: _containers.RepeatedCompositeFieldContainer[NegotiatedGrant]
    def __init__(self, plans: _Optional[_Iterable[_Union[LinePlan, _Mapping]]] = ..., add_ons: _Optional[_Iterable[str]] = ..., grants: _Optional[_Iterable[_Union[NegotiatedGrant, _Mapping]]] = ...) -> None: ...

class NegotiatedGrant(_message.Message):
    __slots__ = ("entitlement_key", "included", "unlimited", "entitled", "scalar")
    ENTITLEMENT_KEY_FIELD_NUMBER: _ClassVar[int]
    INCLUDED_FIELD_NUMBER: _ClassVar[int]
    UNLIMITED_FIELD_NUMBER: _ClassVar[int]
    ENTITLED_FIELD_NUMBER: _ClassVar[int]
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    entitlement_key: str
    included: int
    unlimited: bool
    entitled: bool
    scalar: str
    def __init__(self, entitlement_key: _Optional[str] = ..., included: _Optional[int] = ..., unlimited: bool = ..., entitled: bool = ..., scalar: _Optional[str] = ...) -> None: ...

class UpdateSupportEnvironmentBillingRequest(_message.Message):
    __slots__ = ("environment_id", "operations", "etag", "effective_at", "reason", "dry_run")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_AT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    operations: _containers.RepeatedCompositeFieldContainer[SupportBillingOperation]
    etag: str
    effective_at: str
    reason: str
    dry_run: bool
    def __init__(self, environment_id: _Optional[str] = ..., operations: _Optional[_Iterable[_Union[SupportBillingOperation, _Mapping]]] = ..., etag: _Optional[str] = ..., effective_at: _Optional[str] = ..., reason: _Optional[str] = ..., dry_run: bool = ...) -> None: ...

class SupportBillingOperation(_message.Message):
    __slots__ = ("set_plan", "add_add_on", "remove_add_on", "set_grant", "remove_grant")
    SET_PLAN_FIELD_NUMBER: _ClassVar[int]
    ADD_ADD_ON_FIELD_NUMBER: _ClassVar[int]
    REMOVE_ADD_ON_FIELD_NUMBER: _ClassVar[int]
    SET_GRANT_FIELD_NUMBER: _ClassVar[int]
    REMOVE_GRANT_FIELD_NUMBER: _ClassVar[int]
    set_plan: LinePlan
    add_add_on: str
    remove_add_on: str
    set_grant: NegotiatedGrant
    remove_grant: str
    def __init__(self, set_plan: _Optional[_Union[LinePlan, _Mapping]] = ..., add_add_on: _Optional[str] = ..., remove_add_on: _Optional[str] = ..., set_grant: _Optional[_Union[NegotiatedGrant, _Mapping]] = ..., remove_grant: _Optional[str] = ...) -> None: ...

class UpdateSupportEnvironmentBillingResponse(_message.Message):
    __slots__ = ("environment_id", "workspace_id", "dry_run", "state", "change", "effective_at", "etag", "warnings")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_AT_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    workspace_id: str
    dry_run: bool
    state: SupportBillingState
    change: SupportContractChange
    effective_at: str
    etag: str
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, environment_id: _Optional[str] = ..., workspace_id: _Optional[str] = ..., dry_run: bool = ..., state: _Optional[_Union[SupportBillingState, _Mapping]] = ..., change: _Optional[_Union[SupportContractChange, _Mapping]] = ..., effective_at: _Optional[str] = ..., etag: _Optional[str] = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class SupportContractChange(_message.Message):
    __slots__ = ("subscriptions_added", "subscriptions_ended", "overrides_added", "overrides_removed", "custom_fields")
    class CustomFieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SUBSCRIPTIONS_ADDED_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_ENDED_FIELD_NUMBER: _ClassVar[int]
    OVERRIDES_ADDED_FIELD_NUMBER: _ClassVar[int]
    OVERRIDES_REMOVED_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELDS_FIELD_NUMBER: _ClassVar[int]
    subscriptions_added: _containers.RepeatedScalarFieldContainer[str]
    subscriptions_ended: _containers.RepeatedScalarFieldContainer[str]
    overrides_added: _containers.RepeatedScalarFieldContainer[str]
    overrides_removed: _containers.RepeatedScalarFieldContainer[str]
    custom_fields: _containers.ScalarMap[str, str]
    def __init__(self, subscriptions_added: _Optional[_Iterable[str]] = ..., subscriptions_ended: _Optional[_Iterable[str]] = ..., overrides_added: _Optional[_Iterable[str]] = ..., overrides_removed: _Optional[_Iterable[str]] = ..., custom_fields: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateSupportWorkspaceBillingAccountRequest(_message.Message):
    __slots__ = ("workspace_id", "set_production_card_exemption", "reason", "dry_run")
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    SET_PRODUCTION_CARD_EXEMPTION_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    set_production_card_exemption: bool
    reason: str
    dry_run: bool
    def __init__(self, workspace_id: _Optional[str] = ..., set_production_card_exemption: bool = ..., reason: _Optional[str] = ..., dry_run: bool = ...) -> None: ...

class UpdateSupportWorkspaceBillingAccountResponse(_message.Message):
    __slots__ = ("account", "dry_run", "warnings")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    account: SupportBillingAccount
    dry_run: bool
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, account: _Optional[_Union[SupportBillingAccount, _Mapping]] = ..., dry_run: bool = ..., warnings: _Optional[_Iterable[str]] = ...) -> None: ...

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
    STRIPE_AND_METRONOME: _ClassVar[BillingMode]
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
STRIPE_AND_METRONOME: BillingMode
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
    __slots__ = ("environment_id", "environment_name", "plans", "catalog_version", "contract_status")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    CATALOG_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_STATUS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    environment_name: str
    plans: _containers.RepeatedCompositeFieldContainer[LinePlan]
    catalog_version: int
    contract_status: ContractStatus
    def __init__(self, environment_id: _Optional[str] = ..., environment_name: _Optional[str] = ..., plans: _Optional[_Iterable[_Union[LinePlan, _Mapping]]] = ..., catalog_version: _Optional[int] = ..., contract_status: _Optional[_Union[ContractStatus, str]] = ...) -> None: ...

class LinePlan(_message.Message):
    __slots__ = ("line", "tier")
    LINE_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    line: str
    tier: str
    def __init__(self, line: _Optional[str] = ..., tier: _Optional[str] = ...) -> None: ...

class UpdateEnvironmentPlanRequest(_message.Message):
    __slots__ = ("environment_id", "plans")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PLANS_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    plans: _containers.RepeatedCompositeFieldContainer[LinePlan]
    def __init__(self, environment_id: _Optional[str] = ..., plans: _Optional[_Iterable[_Union[LinePlan, _Mapping]]] = ...) -> None: ...

class UpdateEnvironmentPlanResponse(_message.Message):
    __slots__ = ("plans", "exceeded")
    PLANS_FIELD_NUMBER: _ClassVar[int]
    EXCEEDED_FIELD_NUMBER: _ClassVar[int]
    plans: _containers.RepeatedCompositeFieldContainer[LinePlan]
    exceeded: _containers.RepeatedCompositeFieldContainer[ExceededAllowance]
    def __init__(self, plans: _Optional[_Iterable[_Union[LinePlan, _Mapping]]] = ..., exceeded: _Optional[_Iterable[_Union[ExceededAllowance, _Mapping]]] = ...) -> None: ...

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

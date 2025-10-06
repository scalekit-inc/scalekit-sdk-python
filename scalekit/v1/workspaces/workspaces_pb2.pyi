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
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BillingSubscriptionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BILLING_SUBSCRIPTION_STATUS_UNSPECIFIED: _ClassVar[BillingSubscriptionStatus]
    BILLING_SUBSCRIPTION_ACTIVE: _ClassVar[BillingSubscriptionStatus]
    BILLING_SUBSCRIPTION_CANCELED: _ClassVar[BillingSubscriptionStatus]
    BILLING_SUBSCRIPTION_PAST_DUE: _ClassVar[BillingSubscriptionStatus]

class InvoiceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVOICE_STATUS_UNSPECIFIED: _ClassVar[InvoiceStatus]
    INVOICE_PAID: _ClassVar[InvoiceStatus]
    INVOICE_DUE: _ClassVar[InvoiceStatus]
    INVOICE_OVERDUE: _ClassVar[InvoiceStatus]
    INVOICE_VOID: _ClassVar[InvoiceStatus]

class PaymentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_TYPE_UNSPECIFIED: _ClassVar[PaymentType]
    CARD: _ClassVar[PaymentType]
    BANK_ACCOUNT: _ClassVar[PaymentType]
    OFFLINE: _ClassVar[PaymentType]

class PaymentMethodStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_METHOD_STATUS_UNSPECIFIED: _ClassVar[PaymentMethodStatus]
    PAYMENT_METHOD_ACTIVE: _ClassVar[PaymentMethodStatus]
    PAYMENT_METHOD_EXPIRED: _ClassVar[PaymentMethodStatus]
    PAYMENT_METHOD_FAILED: _ClassVar[PaymentMethodStatus]
BILLING_SUBSCRIPTION_STATUS_UNSPECIFIED: BillingSubscriptionStatus
BILLING_SUBSCRIPTION_ACTIVE: BillingSubscriptionStatus
BILLING_SUBSCRIPTION_CANCELED: BillingSubscriptionStatus
BILLING_SUBSCRIPTION_PAST_DUE: BillingSubscriptionStatus
INVOICE_STATUS_UNSPECIFIED: InvoiceStatus
INVOICE_PAID: InvoiceStatus
INVOICE_DUE: InvoiceStatus
INVOICE_OVERDUE: InvoiceStatus
INVOICE_VOID: InvoiceStatus
PAYMENT_TYPE_UNSPECIFIED: PaymentType
CARD: PaymentType
BANK_ACCOUNT: PaymentType
OFFLINE: PaymentType
PAYMENT_METHOD_STATUS_UNSPECIFIED: PaymentMethodStatus
PAYMENT_METHOD_ACTIVE: PaymentMethodStatus
PAYMENT_METHOD_EXPIRED: PaymentMethodStatus
PAYMENT_METHOD_FAILED: PaymentMethodStatus

class WorkspaceExtendedInfo(_message.Message):
    __slots__ = ("payment_overdue", "payment_method_present", "free_quota_exceeded")
    PAYMENT_OVERDUE_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_PRESENT_FIELD_NUMBER: _ClassVar[int]
    FREE_QUOTA_EXCEEDED_FIELD_NUMBER: _ClassVar[int]
    payment_overdue: bool
    payment_method_present: bool
    free_quota_exceeded: bool
    def __init__(self, payment_overdue: bool = ..., payment_method_present: bool = ..., free_quota_exceeded: bool = ...) -> None: ...

class Workspace(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "display_name", "region_code", "extended_info", "billing_customer_id", "billing_subscription_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_CODE_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_INFO_FIELD_NUMBER: _ClassVar[int]
    BILLING_CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    BILLING_SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    display_name: str
    region_code: _commons_pb2.RegionCode
    extended_info: WorkspaceExtendedInfo
    billing_customer_id: str
    billing_subscription_id: str
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., display_name: _Optional[str] = ..., region_code: _Optional[_Union[_commons_pb2.RegionCode, str]] = ..., extended_info: _Optional[_Union[WorkspaceExtendedInfo, _Mapping]] = ..., billing_customer_id: _Optional[str] = ..., billing_subscription_id: _Optional[str] = ...) -> None: ...

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

class GetBillingInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBillingInfoResponse(_message.Message):
    __slots__ = ("billing_info",)
    BILLING_INFO_FIELD_NUMBER: _ClassVar[int]
    billing_info: BillingInfo
    def __init__(self, billing_info: _Optional[_Union[BillingInfo, _Mapping]] = ...) -> None: ...

class BillingInfo(_message.Message):
    __slots__ = ("plan_name", "subscriptions", "current_invoice", "payment_method", "billing_contact_info", "addons", "last_invoice")
    PLAN_NAME_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_INVOICE_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    BILLING_CONTACT_INFO_FIELD_NUMBER: _ClassVar[int]
    ADDONS_FIELD_NUMBER: _ClassVar[int]
    LAST_INVOICE_FIELD_NUMBER: _ClassVar[int]
    plan_name: str
    subscriptions: _containers.RepeatedCompositeFieldContainer[BillingSubscription]
    current_invoice: CurrentInvoice
    payment_method: PaymentMethod
    billing_contact_info: BillingContactInfo
    addons: _containers.RepeatedCompositeFieldContainer[Addon]
    last_invoice: LastInvoice
    def __init__(self, plan_name: _Optional[str] = ..., subscriptions: _Optional[_Iterable[_Union[BillingSubscription, _Mapping]]] = ..., current_invoice: _Optional[_Union[CurrentInvoice, _Mapping]] = ..., payment_method: _Optional[_Union[PaymentMethod, _Mapping]] = ..., billing_contact_info: _Optional[_Union[BillingContactInfo, _Mapping]] = ..., addons: _Optional[_Iterable[_Union[Addon, _Mapping]]] = ..., last_invoice: _Optional[_Union[LastInvoice, _Mapping]] = ...) -> None: ...

class BillingSubscription(_message.Message):
    __slots__ = ("id", "status", "start_date", "end_date", "amount", "currency", "items")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: BillingSubscriptionStatus
    start_date: _timestamp_pb2.Timestamp
    end_date: _timestamp_pb2.Timestamp
    amount: float
    currency: str
    items: _containers.RepeatedCompositeFieldContainer[SubscriptionItem]
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[BillingSubscriptionStatus, str]] = ..., start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., amount: _Optional[float] = ..., currency: _Optional[str] = ..., items: _Optional[_Iterable[_Union[SubscriptionItem, _Mapping]]] = ...) -> None: ...

class SubscriptionItem(_message.Message):
    __slots__ = ("id", "price_id", "quantity", "product", "price")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: str
    price_id: str
    quantity: int
    product: SubscriptionProduct
    price: SubscriptionPrice
    def __init__(self, id: _Optional[str] = ..., price_id: _Optional[str] = ..., quantity: _Optional[int] = ..., product: _Optional[_Union[SubscriptionProduct, _Mapping]] = ..., price: _Optional[_Union[SubscriptionPrice, _Mapping]] = ...) -> None: ...

class SubscriptionProduct(_message.Message):
    __slots__ = ("id", "name", "description", "active")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    active: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., active: bool = ...) -> None: ...

class SubscriptionPrice(_message.Message):
    __slots__ = ("id", "amount", "type", "interval", "billing_scheme", "usage_type", "tiers", "total_usage", "aggregation_method")
    ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    BILLING_SCHEME_FIELD_NUMBER: _ClassVar[int]
    USAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_USAGE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    id: str
    amount: int
    type: str
    interval: str
    billing_scheme: str
    usage_type: str
    tiers: _containers.RepeatedCompositeFieldContainer[PriceTier]
    total_usage: int
    aggregation_method: str
    def __init__(self, id: _Optional[str] = ..., amount: _Optional[int] = ..., type: _Optional[str] = ..., interval: _Optional[str] = ..., billing_scheme: _Optional[str] = ..., usage_type: _Optional[str] = ..., tiers: _Optional[_Iterable[_Union[PriceTier, _Mapping]]] = ..., total_usage: _Optional[int] = ..., aggregation_method: _Optional[str] = ...) -> None: ...

class PriceTier(_message.Message):
    __slots__ = ("up_to", "amount")
    UP_TO_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    up_to: int
    amount: int
    def __init__(self, up_to: _Optional[int] = ..., amount: _Optional[int] = ...) -> None: ...

class CurrentInvoice(_message.Message):
    __slots__ = ("id", "amount", "currency", "status", "due_date", "issued_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    ISSUED_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    amount: float
    currency: str
    status: InvoiceStatus
    due_date: _timestamp_pb2.Timestamp
    issued_date: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., amount: _Optional[float] = ..., currency: _Optional[str] = ..., status: _Optional[_Union[InvoiceStatus, str]] = ..., due_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., issued_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LastInvoice(_message.Message):
    __slots__ = ("id", "amount", "currency", "status", "due_date", "issued_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    ISSUED_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    amount: float
    currency: str
    status: InvoiceStatus
    due_date: _timestamp_pb2.Timestamp
    issued_date: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., amount: _Optional[float] = ..., currency: _Optional[str] = ..., status: _Optional[_Union[InvoiceStatus, str]] = ..., due_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., issued_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PaymentMethod(_message.Message):
    __slots__ = ("id", "type", "account_number", "account_type", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: PaymentType
    account_number: str
    account_type: str
    status: PaymentMethodStatus
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[PaymentType, str]] = ..., account_number: _Optional[str] = ..., account_type: _Optional[str] = ..., status: _Optional[_Union[PaymentMethodStatus, str]] = ...) -> None: ...

class BillingContactInfo(_message.Message):
    __slots__ = ("name", "email", "line1", "line2", "city", "state", "postal_code", "country")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    LINE1_FIELD_NUMBER: _ClassVar[int]
    LINE2_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    name: str
    email: str
    line1: str
    line2: str
    city: str
    state: str
    postal_code: str
    country: str
    def __init__(self, name: _Optional[str] = ..., email: _Optional[str] = ..., line1: _Optional[str] = ..., line2: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., postal_code: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class Addon(_message.Message):
    __slots__ = ("id", "name", "description", "features", "enabled", "price", "currency")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    features: _containers.RepeatedScalarFieldContainer[str]
    enabled: bool
    price: float
    currency: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., features: _Optional[_Iterable[str]] = ..., enabled: bool = ..., price: _Optional[float] = ..., currency: _Optional[str] = ...) -> None: ...

class GetProductUsageRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetProductUsageResponse(_message.Message):
    __slots__ = ("products", "total_amount", "currency")
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    products: _containers.RepeatedCompositeFieldContainer[ProductUsage]
    total_amount: float
    currency: str
    def __init__(self, products: _Optional[_Iterable[_Union[ProductUsage, _Mapping]]] = ..., total_amount: _Optional[float] = ..., currency: _Optional[str] = ...) -> None: ...

class ProductUsage(_message.Message):
    __slots__ = ("product_id", "product_name", "description", "tiers", "total_product_amount", "currency")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TIERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRODUCT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    product_name: str
    description: str
    tiers: _containers.RepeatedCompositeFieldContainer[UsageTier]
    total_product_amount: float
    currency: str
    def __init__(self, product_id: _Optional[str] = ..., product_name: _Optional[str] = ..., description: _Optional[str] = ..., tiers: _Optional[_Iterable[_Union[UsageTier, _Mapping]]] = ..., total_product_amount: _Optional[float] = ..., currency: _Optional[str] = ...) -> None: ...

class UsageTier(_message.Message):
    __slots__ = ("tier_name", "current_count", "total_available_count", "price_for_current_tier", "currency", "is_free_tier")
    TIER_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AVAILABLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FOR_CURRENT_TIER_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    IS_FREE_TIER_FIELD_NUMBER: _ClassVar[int]
    tier_name: str
    current_count: int
    total_available_count: int
    price_for_current_tier: float
    currency: str
    is_free_tier: bool
    def __init__(self, tier_name: _Optional[str] = ..., current_count: _Optional[int] = ..., total_available_count: _Optional[int] = ..., price_for_current_tier: _Optional[float] = ..., currency: _Optional[str] = ..., is_free_tier: bool = ...) -> None: ...

class GetProductCatalogRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetProductCatalogResponse(_message.Message):
    __slots__ = ("catalog",)
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    catalog: ProductCatalog
    def __init__(self, catalog: _Optional[_Union[ProductCatalog, _Mapping]] = ...) -> None: ...

class ProductCatalog(_message.Message):
    __slots__ = ("products",)
    PRODUCTS_FIELD_NUMBER: _ClassVar[int]
    products: _containers.RepeatedCompositeFieldContainer[ProductCatalogItem]
    def __init__(self, products: _Optional[_Iterable[_Union[ProductCatalogItem, _Mapping]]] = ...) -> None: ...

class ProductCatalogItem(_message.Message):
    __slots__ = ("product", "prices", "billing_type")
    PRODUCT_FIELD_NUMBER: _ClassVar[int]
    PRICES_FIELD_NUMBER: _ClassVar[int]
    BILLING_TYPE_FIELD_NUMBER: _ClassVar[int]
    product: CatalogProduct
    prices: _containers.RepeatedCompositeFieldContainer[CatalogPrice]
    billing_type: str
    def __init__(self, product: _Optional[_Union[CatalogProduct, _Mapping]] = ..., prices: _Optional[_Iterable[_Union[CatalogPrice, _Mapping]]] = ..., billing_type: _Optional[str] = ...) -> None: ...

class CatalogProduct(_message.Message):
    __slots__ = ("id", "name", "description", "active", "metadata", "default_price_id")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PRICE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    active: bool
    metadata: _containers.ScalarMap[str, str]
    default_price_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., active: bool = ..., metadata: _Optional[_Mapping[str, str]] = ..., default_price_id: _Optional[str] = ...) -> None: ...

class CatalogPrice(_message.Message):
    __slots__ = ("id", "amount", "currency", "type", "interval", "billing_scheme", "usage_type", "tiers")
    ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    BILLING_SCHEME_FIELD_NUMBER: _ClassVar[int]
    USAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    amount: int
    currency: str
    type: str
    interval: str
    billing_scheme: str
    usage_type: str
    tiers: _containers.RepeatedCompositeFieldContainer[PriceTier]
    def __init__(self, id: _Optional[str] = ..., amount: _Optional[int] = ..., currency: _Optional[str] = ..., type: _Optional[str] = ..., interval: _Optional[str] = ..., billing_scheme: _Optional[str] = ..., usage_type: _Optional[str] = ..., tiers: _Optional[_Iterable[_Union[PriceTier, _Mapping]]] = ...) -> None: ...

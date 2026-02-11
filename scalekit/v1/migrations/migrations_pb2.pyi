from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FSADataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FSA_DATA_TYPE_UNSPECIFIED: _ClassVar[FSADataType]
    FSA_DATA_TYPE_CONNECTION: _ClassVar[FSADataType]
    FSA_DATA_TYPE_SESSION: _ClassVar[FSADataType]
    FSA_DATA_TYPE_USER_MANAGEMENT: _ClassVar[FSADataType]
FSA_DATA_TYPE_UNSPECIFIED: FSADataType
FSA_DATA_TYPE_CONNECTION: FSADataType
FSA_DATA_TYPE_SESSION: FSADataType
FSA_DATA_TYPE_USER_MANAGEMENT: FSADataType

class MigrationServiceResponse(_message.Message):
    __slots__ = ("success_environments", "failed_environments")
    SUCCESS_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    FAILED_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    success_environments: int
    failed_environments: int
    def __init__(self, success_environments: _Optional[int] = ..., failed_environments: _Optional[int] = ...) -> None: ...

class MigrationSAMLRequest(_message.Message):
    __slots__ = ("environment_ids", "batch_size")
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    environment_ids: _containers.RepeatedScalarFieldContainer[int]
    batch_size: int
    def __init__(self, environment_ids: _Optional[_Iterable[int]] = ..., batch_size: _Optional[int] = ...) -> None: ...

class MigrateFSARequest(_message.Message):
    __slots__ = ("environment_ids", "data_type", "batch_size")
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    environment_ids: _containers.RepeatedScalarFieldContainer[int]
    data_type: FSADataType
    batch_size: int
    def __init__(self, environment_ids: _Optional[_Iterable[int]] = ..., data_type: _Optional[_Union[FSADataType, str]] = ..., batch_size: _Optional[int] = ...) -> None: ...

class MigrationFSAResponse(_message.Message):
    __slots__ = ("success_environments", "failed_environments")
    SUCCESS_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    FAILED_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    success_environments: int
    failed_environments: int
    def __init__(self, success_environments: _Optional[int] = ..., failed_environments: _Optional[int] = ...) -> None: ...

class MigrateStripeCustomersRequest(_message.Message):
    __slots__ = ("migrate_stripe_customers",)
    MIGRATE_STRIPE_CUSTOMERS_FIELD_NUMBER: _ClassVar[int]
    migrate_stripe_customers: MigrateStripeCustomers
    def __init__(self, migrate_stripe_customers: _Optional[_Union[MigrateStripeCustomers, _Mapping]] = ...) -> None: ...

class MigrateStripeCustomers(_message.Message):
    __slots__ = ("workspace_ids", "plan_name", "batch_size", "include_test_accounts")
    WORKSPACE_IDS_FIELD_NUMBER: _ClassVar[int]
    PLAN_NAME_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TEST_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    workspace_ids: _containers.RepeatedScalarFieldContainer[int]
    plan_name: str
    batch_size: int
    include_test_accounts: bool
    def __init__(self, workspace_ids: _Optional[_Iterable[int]] = ..., plan_name: _Optional[str] = ..., batch_size: _Optional[int] = ..., include_test_accounts: bool = ...) -> None: ...

class MigrateStripeCustomersResponse(_message.Message):
    __slots__ = ("success_count", "failed_count", "failed_workspace_ids", "error_messages")
    SUCCESS_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILED_WORKSPACE_IDS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    success_count: int
    failed_count: int
    failed_workspace_ids: _containers.RepeatedScalarFieldContainer[int]
    error_messages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, success_count: _Optional[int] = ..., failed_count: _Optional[int] = ..., failed_workspace_ids: _Optional[_Iterable[int]] = ..., error_messages: _Optional[_Iterable[str]] = ...) -> None: ...

class MigrationSAMLResponse(_message.Message):
    __slots__ = ("success_environments", "failed_environments")
    SUCCESS_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    FAILED_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    success_environments: int
    failed_environments: int
    def __init__(self, success_environments: _Optional[int] = ..., failed_environments: _Optional[int] = ...) -> None: ...

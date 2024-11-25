from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserAttributeDatatype(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_DATATYPE: _ClassVar[UserAttributeDatatype]
    STRING: _ClassVar[UserAttributeDatatype]
    NUMBER: _ClassVar[UserAttributeDatatype]
    BOOL: _ClassVar[UserAttributeDatatype]
    ARRAY: _ClassVar[UserAttributeDatatype]
    OBJECT: _ClassVar[UserAttributeDatatype]

class UserAttributeCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_CATEGORY: _ClassVar[UserAttributeCategory]
    STANDARD: _ClassVar[UserAttributeCategory]
    CUSTOM: _ClassVar[UserAttributeCategory]
UNSPECIFIED_DATATYPE: UserAttributeDatatype
STRING: UserAttributeDatatype
NUMBER: UserAttributeDatatype
BOOL: UserAttributeDatatype
ARRAY: UserAttributeDatatype
OBJECT: UserAttributeDatatype
UNSPECIFIED_CATEGORY: UserAttributeCategory
STANDARD: UserAttributeCategory
CUSTOM: UserAttributeCategory

class UserAttribute(_message.Message):
    __slots__ = ("key", "enabled", "required", "label", "datatype", "category", "sso_addition_info", "directory_user_additional_info")
    KEY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SSO_ADDITION_INFO_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_USER_ADDITIONAL_INFO_FIELD_NUMBER: _ClassVar[int]
    key: str
    enabled: bool
    required: bool
    label: str
    datatype: UserAttributeDatatype
    category: UserAttributeCategory
    sso_addition_info: SSOUserAdditionInfo
    directory_user_additional_info: DirectoryUserAdditionalInfo
    def __init__(self, key: _Optional[str] = ..., enabled: bool = ..., required: bool = ..., label: _Optional[str] = ..., datatype: _Optional[_Union[UserAttributeDatatype, str]] = ..., category: _Optional[_Union[UserAttributeCategory, str]] = ..., sso_addition_info: _Optional[_Union[SSOUserAdditionInfo, _Mapping]] = ..., directory_user_additional_info: _Optional[_Union[DirectoryUserAdditionalInfo, _Mapping]] = ...) -> None: ...

class SSOUserAdditionInfo(_message.Message):
    __slots__ = ("default_saml_mapping", "default_oidc_mapping")
    DEFAULT_SAML_MAPPING_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_OIDC_MAPPING_FIELD_NUMBER: _ClassVar[int]
    default_saml_mapping: str
    default_oidc_mapping: str
    def __init__(self, default_saml_mapping: _Optional[str] = ..., default_oidc_mapping: _Optional[str] = ...) -> None: ...

class DirectoryUserAdditionalInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateUserAttributeRequest(_message.Message):
    __slots__ = ("user_attribute",)
    USER_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    user_attribute: UserAttribute
    def __init__(self, user_attribute: _Optional[_Union[UserAttribute, _Mapping]] = ...) -> None: ...

class CreateUserAttributeResponse(_message.Message):
    __slots__ = ("user_attribute",)
    USER_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    user_attribute: UserAttribute
    def __init__(self, user_attribute: _Optional[_Union[UserAttribute, _Mapping]] = ...) -> None: ...

class ListUserAttributesResponse(_message.Message):
    __slots__ = ("user_attributes",)
    USER_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    user_attributes: _containers.RepeatedCompositeFieldContainer[UserAttribute]
    def __init__(self, user_attributes: _Optional[_Iterable[_Union[UserAttribute, _Mapping]]] = ...) -> None: ...

class UpdateUserAttributeRequest(_message.Message):
    __slots__ = ("key", "user_attribute")
    KEY_FIELD_NUMBER: _ClassVar[int]
    USER_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    key: str
    user_attribute: UserAttribute
    def __init__(self, key: _Optional[str] = ..., user_attribute: _Optional[_Union[UserAttribute, _Mapping]] = ...) -> None: ...

class UpdateUserAttributeResponse(_message.Message):
    __slots__ = ("user_attribute",)
    USER_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    user_attribute: UserAttribute
    def __init__(self, user_attribute: _Optional[_Union[UserAttribute, _Mapping]] = ...) -> None: ...

class DeleteUserAttributeRequest(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

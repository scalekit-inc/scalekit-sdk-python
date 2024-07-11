from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserProfileAttributeDatatype(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_DATATYPE: _ClassVar[UserProfileAttributeDatatype]
    STRING: _ClassVar[UserProfileAttributeDatatype]
    NUMBER: _ClassVar[UserProfileAttributeDatatype]
    BOOL: _ClassVar[UserProfileAttributeDatatype]
    ARRAY: _ClassVar[UserProfileAttributeDatatype]
    OBJECT: _ClassVar[UserProfileAttributeDatatype]

class UserProfileAttributeCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_CATEGORY: _ClassVar[UserProfileAttributeCategory]
    STANDARD: _ClassVar[UserProfileAttributeCategory]
    CUSTOM: _ClassVar[UserProfileAttributeCategory]
UNSPECIFIED_DATATYPE: UserProfileAttributeDatatype
STRING: UserProfileAttributeDatatype
NUMBER: UserProfileAttributeDatatype
BOOL: UserProfileAttributeDatatype
ARRAY: UserProfileAttributeDatatype
OBJECT: UserProfileAttributeDatatype
UNSPECIFIED_CATEGORY: UserProfileAttributeCategory
STANDARD: UserProfileAttributeCategory
CUSTOM: UserProfileAttributeCategory

class UserProfileAttribute(_message.Message):
    __slots__ = ("key", "enabled", "required", "label", "datatype", "category", "default_saml_mapping", "default_oidc_mapping")
    KEY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_SAML_MAPPING_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_OIDC_MAPPING_FIELD_NUMBER: _ClassVar[int]
    key: str
    enabled: bool
    required: bool
    label: str
    datatype: UserProfileAttributeDatatype
    category: UserProfileAttributeCategory
    default_saml_mapping: str
    default_oidc_mapping: str
    def __init__(self, key: _Optional[str] = ..., enabled: bool = ..., required: bool = ..., label: _Optional[str] = ..., datatype: _Optional[_Union[UserProfileAttributeDatatype, str]] = ..., category: _Optional[_Union[UserProfileAttributeCategory, str]] = ..., default_saml_mapping: _Optional[str] = ..., default_oidc_mapping: _Optional[str] = ...) -> None: ...

class CreateUserProfileAttributeRequest(_message.Message):
    __slots__ = ("user_profile_attribute",)
    USER_PROFILE_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    user_profile_attribute: UserProfileAttribute
    def __init__(self, user_profile_attribute: _Optional[_Union[UserProfileAttribute, _Mapping]] = ...) -> None: ...

class CreateUserProfileAttributeResponse(_message.Message):
    __slots__ = ("user_profile_attribute",)
    USER_PROFILE_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    user_profile_attribute: UserProfileAttribute
    def __init__(self, user_profile_attribute: _Optional[_Union[UserProfileAttribute, _Mapping]] = ...) -> None: ...

class ListUserProfileAttributesResponse(_message.Message):
    __slots__ = ("user_profile_attributes",)
    USER_PROFILE_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    user_profile_attributes: _containers.RepeatedCompositeFieldContainer[UserProfileAttribute]
    def __init__(self, user_profile_attributes: _Optional[_Iterable[_Union[UserProfileAttribute, _Mapping]]] = ...) -> None: ...

class UpdateUserProfileAttributeRequest(_message.Message):
    __slots__ = ("key", "user_profile_attribute")
    KEY_FIELD_NUMBER: _ClassVar[int]
    USER_PROFILE_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    key: str
    user_profile_attribute: UserProfileAttribute
    def __init__(self, key: _Optional[str] = ..., user_profile_attribute: _Optional[_Union[UserProfileAttribute, _Mapping]] = ...) -> None: ...

class UpdateUserProfileAttributeResponse(_message.Message):
    __slots__ = ("user_profile_attribute",)
    USER_PROFILE_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    user_profile_attribute: UserProfileAttribute
    def __init__(self, user_profile_attribute: _Optional[_Union[UserProfileAttribute, _Mapping]] = ...) -> None: ...

class DeleteUserProfileAttributeRequest(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

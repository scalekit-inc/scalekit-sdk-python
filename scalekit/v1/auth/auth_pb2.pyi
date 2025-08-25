from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.api import visibility_pb2 as _visibility_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.connections import connections_pb2 as _connections_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Intent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INTENT_UNSPECIFIED: _ClassVar[Intent]
    sign_in: _ClassVar[Intent]
    sign_up: _ClassVar[Intent]

class AuthState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUTH_STATE_UNSPECIFIED: _ClassVar[AuthState]
    AUTHENTICATION_IN_PROGRESS: _ClassVar[AuthState]
    ORGANIZATION_SWITCHER: _ClassVar[AuthState]
    ORGANIZATION_SELECTED: _ClassVar[AuthState]
    ORGANIZATION_SIGNUP: _ClassVar[AuthState]
    ORGANIZATION_SWITCHER_SIGNUP: _ClassVar[AuthState]
    OTP_VERIFICATION_PENDING: _ClassVar[AuthState]
    MAGIC_LINK_SENT: _ClassVar[AuthState]
    LINK_SENT_OTP_VERIFICATION_PENDING: _ClassVar[AuthState]
    OTP_VERIFIED: _ClassVar[AuthState]
    LINK_VERIFIED: _ClassVar[AuthState]
    SSO_AUTHENTICATED: _ClassVar[AuthState]
    ORG_USER_CREATED: _ClassVar[AuthState]
    AUTHENTICATION_COMPLETED: _ClassVar[AuthState]
    AUTHENTICATION_FAILED: _ClassVar[AuthState]
INTENT_UNSPECIFIED: Intent
sign_in: Intent
sign_up: Intent
AUTH_STATE_UNSPECIFIED: AuthState
AUTHENTICATION_IN_PROGRESS: AuthState
ORGANIZATION_SWITCHER: AuthState
ORGANIZATION_SELECTED: AuthState
ORGANIZATION_SIGNUP: AuthState
ORGANIZATION_SWITCHER_SIGNUP: AuthState
OTP_VERIFICATION_PENDING: AuthState
MAGIC_LINK_SENT: AuthState
LINK_SENT_OTP_VERIFICATION_PENDING: AuthState
OTP_VERIFIED: AuthState
LINK_VERIFIED: AuthState
SSO_AUTHENTICATED: AuthState
ORG_USER_CREATED: AuthState
AUTHENTICATION_COMPLETED: AuthState
AUTHENTICATION_FAILED: AuthState

class ListAuthMethodsRequest(_message.Message):
    __slots__ = ("intent",)
    INTENT_FIELD_NUMBER: _ClassVar[int]
    intent: str
    def __init__(self, intent: _Optional[str] = ...) -> None: ...

class ListAuthMethodsResponse(_message.Message):
    __slots__ = ("auth_methods",)
    AUTH_METHODS_FIELD_NUMBER: _ClassVar[int]
    auth_methods: _containers.RepeatedCompositeFieldContainer[AuthMethod]
    def __init__(self, auth_methods: _Optional[_Iterable[_Union[AuthMethod, _Mapping]]] = ...) -> None: ...

class AuthMethod(_message.Message):
    __slots__ = ("connection_id", "connection_type", "provider", "auth_initiation_uri", "passwordless_type", "code_challenge_length")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    AUTH_INITIATION_URI_FIELD_NUMBER: _ClassVar[int]
    PASSWORDLESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CODE_CHALLENGE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    connection_type: _connections_pb2.ConnectionType
    provider: str
    auth_initiation_uri: str
    passwordless_type: _connections_pb2.PasswordlessType
    code_challenge_length: int
    def __init__(self, connection_id: _Optional[str] = ..., connection_type: _Optional[_Union[_connections_pb2.ConnectionType, str]] = ..., provider: _Optional[str] = ..., auth_initiation_uri: _Optional[str] = ..., passwordless_type: _Optional[_Union[_connections_pb2.PasswordlessType, str]] = ..., code_challenge_length: _Optional[int] = ...) -> None: ...

class DiscoveryAuthMethodRequest(_message.Message):
    __slots__ = ("discovery_request",)
    DISCOVERY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    discovery_request: DiscoveryRequest
    def __init__(self, discovery_request: _Optional[_Union[DiscoveryRequest, _Mapping]] = ...) -> None: ...

class DiscoveryRequest(_message.Message):
    __slots__ = ("email", "intent")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    email: str
    intent: Intent
    def __init__(self, email: _Optional[str] = ..., intent: _Optional[_Union[Intent, str]] = ...) -> None: ...

class DiscoveryAuthMethodResponse(_message.Message):
    __slots__ = ("auth_method",)
    AUTH_METHOD_FIELD_NUMBER: _ClassVar[int]
    auth_method: AuthMethod
    def __init__(self, auth_method: _Optional[_Union[AuthMethod, _Mapping]] = ...) -> None: ...

class GetAuthCustomizationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuthCustomizationsResponse(_message.Message):
    __slots__ = ("customization_settings",)
    CUSTOMIZATION_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    customization_settings: _struct_pb2.Struct
    def __init__(self, customization_settings: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetAuthFeaturesResponse(_message.Message):
    __slots__ = ("features",)
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _struct_pb2.Struct
    def __init__(self, features: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class VerifyPasswordLessRequest(_message.Message):
    __slots__ = ("otp_req",)
    OTP_REQ_FIELD_NUMBER: _ClassVar[int]
    otp_req: OTPRequest
    def __init__(self, otp_req: _Optional[_Union[OTPRequest, _Mapping]] = ...) -> None: ...

class VerifyPasswordLessResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class OTPRequest(_message.Message):
    __slots__ = ("code_challenge",)
    CODE_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    code_challenge: str
    def __init__(self, code_challenge: _Optional[str] = ...) -> None: ...

class ListUserOrganizationsResponse(_message.Message):
    __slots__ = ("organizations", "user", "intent")
    ORGANIZATIONS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    organizations: _containers.RepeatedCompositeFieldContainer[Organization]
    user: UserDetails
    intent: Intent
    def __init__(self, organizations: _Optional[_Iterable[_Union[Organization, _Mapping]]] = ..., user: _Optional[_Union[UserDetails, _Mapping]] = ..., intent: _Optional[_Union[Intent, str]] = ...) -> None: ...

class Organization(_message.Message):
    __slots__ = ("id", "name", "membership_status", "invitation_invited_by", "invitation_accepted_at", "invitation_created_at", "invitation_expires_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERSHIP_STATUS_FIELD_NUMBER: _ClassVar[int]
    INVITATION_INVITED_BY_FIELD_NUMBER: _ClassVar[int]
    INVITATION_ACCEPTED_AT_FIELD_NUMBER: _ClassVar[int]
    INVITATION_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    INVITATION_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    membership_status: str
    invitation_invited_by: str
    invitation_accepted_at: _timestamp_pb2.Timestamp
    invitation_created_at: _timestamp_pb2.Timestamp
    invitation_expires_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., membership_status: _Optional[str] = ..., invitation_invited_by: _Optional[str] = ..., invitation_accepted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., invitation_created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., invitation_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UserDetails(_message.Message):
    __slots__ = ("email", "first_name", "last_name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    first_name: str
    last_name: str
    def __init__(self, email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class SignupOrganizationRequest(_message.Message):
    __slots__ = ("organization_name", "first_name", "last_name", "full_name", "phone_number")
    ORGANIZATION_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    organization_name: str
    first_name: str
    last_name: str
    full_name: str
    phone_number: str
    def __init__(self, organization_name: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., full_name: _Optional[str] = ..., phone_number: _Optional[str] = ...) -> None: ...

class SignupOrganizationResponse(_message.Message):
    __slots__ = ("organization_id", "organization_name")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_NAME_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    organization_name: str
    def __init__(self, organization_id: _Optional[str] = ..., organization_name: _Optional[str] = ...) -> None: ...

class UpdateLoginUserDetailsRequest(_message.Message):
    __slots__ = ("connection_id", "login_request_id", "user")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    LOGIN_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    login_request_id: str
    user: User
    def __init__(self, connection_id: _Optional[str] = ..., login_request_id: _Optional[str] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("sub", "email", "given_name", "family_name", "email_verified", "phone_number", "phone_number_verified", "name", "preferred_username", "picture", "gender", "locale", "groups", "custom_attributes")
    SUB_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    GIVEN_NAME_FIELD_NUMBER: _ClassVar[int]
    FAMILY_NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_USERNAME_FIELD_NUMBER: _ClassVar[int]
    PICTURE_FIELD_NUMBER: _ClassVar[int]
    GENDER_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    sub: str
    email: str
    given_name: str
    family_name: str
    email_verified: bool
    phone_number: str
    phone_number_verified: bool
    name: str
    preferred_username: str
    picture: str
    gender: str
    locale: str
    groups: _containers.RepeatedScalarFieldContainer[str]
    custom_attributes: _struct_pb2.Struct
    def __init__(self, sub: _Optional[str] = ..., email: _Optional[str] = ..., given_name: _Optional[str] = ..., family_name: _Optional[str] = ..., email_verified: bool = ..., phone_number: _Optional[str] = ..., phone_number_verified: bool = ..., name: _Optional[str] = ..., preferred_username: _Optional[str] = ..., picture: _Optional[str] = ..., gender: _Optional[str] = ..., locale: _Optional[str] = ..., groups: _Optional[_Iterable[str]] = ..., custom_attributes: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetAuthStateResponse(_message.Message):
    __slots__ = ("auth_state",)
    AUTH_STATE_FIELD_NUMBER: _ClassVar[int]
    auth_state: AuthState
    def __init__(self, auth_state: _Optional[_Union[AuthState, str]] = ...) -> None: ...

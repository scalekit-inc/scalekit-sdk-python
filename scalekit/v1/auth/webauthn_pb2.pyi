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
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BeginRegistrationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BeginRegistrationResponse(_message.Message):
    __slots__ = ("options",)
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    options: _struct_pb2.Struct
    def __init__(self, options: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class FinishRegistrationRequest(_message.Message):
    __slots__ = ("credential_id", "attestation_object", "client_data_json", "type", "transports", "authenticator_attachment", "client_extension_results")
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_OBJECT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DATA_JSON_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTS_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATOR_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_EXTENSION_RESULTS_FIELD_NUMBER: _ClassVar[int]
    credential_id: bytes
    attestation_object: bytes
    client_data_json: bytes
    type: str
    transports: _containers.RepeatedScalarFieldContainer[str]
    authenticator_attachment: str
    client_extension_results: _struct_pb2.Struct
    def __init__(self, credential_id: _Optional[bytes] = ..., attestation_object: _Optional[bytes] = ..., client_data_json: _Optional[bytes] = ..., type: _Optional[str] = ..., transports: _Optional[_Iterable[str]] = ..., authenticator_attachment: _Optional[str] = ..., client_extension_results: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class FinishRegistrationResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class BeginAuthenticationRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class BeginAuthenticationResponse(_message.Message):
    __slots__ = ("session_id", "options")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    options: _struct_pb2.Struct
    def __init__(self, session_id: _Optional[str] = ..., options: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class FinishAuthenticationRequest(_message.Message):
    __slots__ = ("session_id", "credential_id", "client_extension_results", "type", "response", "authenticator_attachment")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_EXTENSION_RESULTS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATOR_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    credential_id: bytes
    client_extension_results: _struct_pb2.Struct
    type: str
    response: AuthenticatorAssertionResponse
    authenticator_attachment: str
    def __init__(self, session_id: _Optional[str] = ..., credential_id: _Optional[bytes] = ..., client_extension_results: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., type: _Optional[str] = ..., response: _Optional[_Union[AuthenticatorAssertionResponse, _Mapping]] = ..., authenticator_attachment: _Optional[str] = ...) -> None: ...

class AuthenticatorAssertionResponse(_message.Message):
    __slots__ = ("authenticator_data", "client_data_json", "signature", "user_handle")
    AUTHENTICATOR_DATA_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DATA_JSON_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    USER_HANDLE_FIELD_NUMBER: _ClassVar[int]
    authenticator_data: bytes
    client_data_json: bytes
    signature: bytes
    user_handle: bytes
    def __init__(self, authenticator_data: _Optional[bytes] = ..., client_data_json: _Optional[bytes] = ..., signature: _Optional[bytes] = ..., user_handle: _Optional[bytes] = ...) -> None: ...

class FinishAuthenticationResponse(_message.Message):
    __slots__ = ("success", "user_id", "session_token")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    success: bool
    user_id: str
    session_token: str
    def __init__(self, success: bool = ..., user_id: _Optional[str] = ..., session_token: _Optional[str] = ...) -> None: ...

class WebAuthnConfiguration(_message.Message):
    __slots__ = ("rp_id", "rp_origin", "user_verification", "authenticator_attachment", "resident_key", "timeout", "allowed_transports")
    RP_ID_FIELD_NUMBER: _ClassVar[int]
    RP_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    USER_VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATOR_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    RESIDENT_KEY_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_TRANSPORTS_FIELD_NUMBER: _ClassVar[int]
    rp_id: str
    rp_origin: str
    user_verification: str
    authenticator_attachment: str
    resident_key: str
    timeout: int
    allowed_transports: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, rp_id: _Optional[str] = ..., rp_origin: _Optional[str] = ..., user_verification: _Optional[str] = ..., authenticator_attachment: _Optional[str] = ..., resident_key: _Optional[str] = ..., timeout: _Optional[int] = ..., allowed_transports: _Optional[_Iterable[str]] = ...) -> None: ...

class ListCredentialsRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class ListCredentialsResponse(_message.Message):
    __slots__ = ("credentials", "all_accepted_credentials_options")
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    ALL_ACCEPTED_CREDENTIALS_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[WebAuthnCredential]
    all_accepted_credentials_options: AllAcceptedCredentialsOptions
    def __init__(self, credentials: _Optional[_Iterable[_Union[WebAuthnCredential, _Mapping]]] = ..., all_accepted_credentials_options: _Optional[_Union[AllAcceptedCredentialsOptions, _Mapping]] = ...) -> None: ...

class DeleteCredentialRequest(_message.Message):
    __slots__ = ("credential_id",)
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    credential_id: str
    def __init__(self, credential_id: _Optional[str] = ...) -> None: ...

class DeleteCredentialResponse(_message.Message):
    __slots__ = ("success", "unknown_credential_options")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_CREDENTIAL_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    unknown_credential_options: UnknownCredentialOptions
    def __init__(self, success: bool = ..., unknown_credential_options: _Optional[_Union[UnknownCredentialOptions, _Mapping]] = ...) -> None: ...

class UnknownCredentialOptions(_message.Message):
    __slots__ = ("rp_id", "credential_id")
    RP_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    rp_id: str
    credential_id: str
    def __init__(self, rp_id: _Optional[str] = ..., credential_id: _Optional[str] = ...) -> None: ...

class AllAcceptedCredentialsOptions(_message.Message):
    __slots__ = ("rp_id", "user_id", "all_accepted_credential_ids")
    RP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ALL_ACCEPTED_CREDENTIAL_IDS_FIELD_NUMBER: _ClassVar[int]
    rp_id: str
    user_id: str
    all_accepted_credential_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, rp_id: _Optional[str] = ..., user_id: _Optional[str] = ..., all_accepted_credential_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateCredentialRequest(_message.Message):
    __slots__ = ("credential_id", "display_name")
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    credential_id: str
    display_name: str
    def __init__(self, credential_id: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class UpdateCredentialResponse(_message.Message):
    __slots__ = ("credential",)
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    credential: WebAuthnCredential
    def __init__(self, credential: _Optional[_Union[WebAuthnCredential, _Mapping]] = ...) -> None: ...

class WebAuthnCredential(_message.Message):
    __slots__ = ("id", "user_id", "credential_id", "attestation_type", "authenticator", "transports", "authenticator_flags", "created_at", "updated_at", "user_agent", "client_info", "display_name")
    class AuthenticatorFlags(_message.Message):
        __slots__ = ("user_present", "user_verified", "backup_eligible", "backup_state")
        USER_PRESENT_FIELD_NUMBER: _ClassVar[int]
        USER_VERIFIED_FIELD_NUMBER: _ClassVar[int]
        BACKUP_ELIGIBLE_FIELD_NUMBER: _ClassVar[int]
        BACKUP_STATE_FIELD_NUMBER: _ClassVar[int]
        user_present: bool
        user_verified: bool
        backup_eligible: bool
        backup_state: bool
        def __init__(self, user_present: bool = ..., user_verified: bool = ..., backup_eligible: bool = ..., backup_state: bool = ...) -> None: ...
    class Authenticator(_message.Message):
        __slots__ = ("aaguid", "name", "attachment", "icon_dark", "icon_light")
        AAGUID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
        ICON_DARK_FIELD_NUMBER: _ClassVar[int]
        ICON_LIGHT_FIELD_NUMBER: _ClassVar[int]
        aaguid: str
        name: str
        attachment: str
        icon_dark: str
        icon_light: str
        def __init__(self, aaguid: _Optional[str] = ..., name: _Optional[str] = ..., attachment: _Optional[str] = ..., icon_dark: _Optional[str] = ..., icon_light: _Optional[str] = ...) -> None: ...
    class UserAgent(_message.Message):
        __slots__ = ("raw", "url", "browser", "browser_version", "os", "os_version", "device_type", "device_model")
        RAW_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        BROWSER_FIELD_NUMBER: _ClassVar[int]
        BROWSER_VERSION_FIELD_NUMBER: _ClassVar[int]
        OS_FIELD_NUMBER: _ClassVar[int]
        OS_VERSION_FIELD_NUMBER: _ClassVar[int]
        DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
        DEVICE_MODEL_FIELD_NUMBER: _ClassVar[int]
        raw: str
        url: str
        browser: str
        browser_version: str
        os: str
        os_version: str
        device_type: str
        device_model: str
        def __init__(self, raw: _Optional[str] = ..., url: _Optional[str] = ..., browser: _Optional[str] = ..., browser_version: _Optional[str] = ..., os: _Optional[str] = ..., os_version: _Optional[str] = ..., device_type: _Optional[str] = ..., device_model: _Optional[str] = ...) -> None: ...
    class ClientInfo(_message.Message):
        __slots__ = ("ip", "region", "region_subdivision", "city")
        IP_FIELD_NUMBER: _ClassVar[int]
        REGION_FIELD_NUMBER: _ClassVar[int]
        REGION_SUBDIVISION_FIELD_NUMBER: _ClassVar[int]
        CITY_FIELD_NUMBER: _ClassVar[int]
        ip: str
        region: str
        region_subdivision: str
        city: str
        def __init__(self, ip: _Optional[str] = ..., region: _Optional[str] = ..., region_subdivision: _Optional[str] = ..., city: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATOR_FIELD_NUMBER: _ClassVar[int]
    TRANSPORTS_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATOR_FLAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_INFO_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    credential_id: bytes
    attestation_type: str
    authenticator: WebAuthnCredential.Authenticator
    transports: _containers.RepeatedScalarFieldContainer[str]
    authenticator_flags: WebAuthnCredential.AuthenticatorFlags
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    user_agent: WebAuthnCredential.UserAgent
    client_info: WebAuthnCredential.ClientInfo
    display_name: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., credential_id: _Optional[bytes] = ..., attestation_type: _Optional[str] = ..., authenticator: _Optional[_Union[WebAuthnCredential.Authenticator, _Mapping]] = ..., transports: _Optional[_Iterable[str]] = ..., authenticator_flags: _Optional[_Union[WebAuthnCredential.AuthenticatorFlags, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_agent: _Optional[_Union[WebAuthnCredential.UserAgent, _Mapping]] = ..., client_info: _Optional[_Union[WebAuthnCredential.ClientInfo, _Mapping]] = ..., display_name: _Optional[str] = ...) -> None: ...

class GetRelatedOriginsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetRelatedOriginsResponse(_message.Message):
    __slots__ = ("origins",)
    ORIGINS_FIELD_NUMBER: _ClassVar[int]
    origins: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, origins: _Optional[_Iterable[str]] = ...) -> None: ...

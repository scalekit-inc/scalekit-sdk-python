from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TOTPRegistrationRequest(_message.Message):
    __slots__ = ("totp_registration",)
    TOTP_REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    totp_registration: TOTPRegistration
    def __init__(self, totp_registration: _Optional[_Union[TOTPRegistration, _Mapping]] = ...) -> None: ...

class TOTPRegistrationResponse(_message.Message):
    __slots__ = ("totp_registration",)
    TOTP_REGISTRATION_FIELD_NUMBER: _ClassVar[int]
    totp_registration: TOTPRegistration
    def __init__(self, totp_registration: _Optional[_Union[TOTPRegistration, _Mapping]] = ...) -> None: ...

class TOTPRegistration(_message.Message):
    __slots__ = ("id", "create_time", "update_time", "user_id", "account_name", "qr_code_uri")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    QR_CODE_URI_FIELD_NUMBER: _ClassVar[int]
    id: str
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    user_id: str
    account_name: str
    qr_code_uri: str
    def __init__(self, id: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_id: _Optional[str] = ..., account_name: _Optional[str] = ..., qr_code_uri: _Optional[str] = ...) -> None: ...

class EnableRegistrationTOTPRequest(_message.Message):
    __slots__ = ("registration_id", "code")
    REGISTRATION_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    registration_id: str
    code: str
    def __init__(self, registration_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class EnableRegistrationTOTPResponse(_message.Message):
    __slots__ = ("id", "backup_codes")
    ID_FIELD_NUMBER: _ClassVar[int]
    BACKUP_CODES_FIELD_NUMBER: _ClassVar[int]
    id: str
    backup_codes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., backup_codes: _Optional[_Iterable[str]] = ...) -> None: ...

class DisableRegistrationTOTPRequest(_message.Message):
    __slots__ = ("registration_id", "code")
    REGISTRATION_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    registration_id: str
    code: str
    def __init__(self, registration_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class GenerateQRCodeRequest(_message.Message):
    __slots__ = ("environment_id", "identifier", "is_user")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    IS_USER_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    identifier: str
    is_user: bool
    def __init__(self, environment_id: _Optional[str] = ..., identifier: _Optional[str] = ..., is_user: bool = ...) -> None: ...

class GenerateQRCodeResponse(_message.Message):
    __slots__ = ("qr_code",)
    QR_CODE_FIELD_NUMBER: _ClassVar[int]
    qr_code: str
    def __init__(self, qr_code: _Optional[str] = ...) -> None: ...

class VerifyUserCodeRequest(_message.Message):
    __slots__ = ("user_id", "code")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    code: str
    def __init__(self, user_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class VerifyCodeResponse(_message.Message):
    __slots__ = ("valid",)
    VALID_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    def __init__(self, valid: bool = ...) -> None: ...

class VerifyRegistrationCodeRequest(_message.Message):
    __slots__ = ("registration_id", "code")
    REGISTRATION_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    registration_id: str
    code: str
    def __init__(self, registration_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

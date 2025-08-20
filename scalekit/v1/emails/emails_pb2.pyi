from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.commons import commons_pb2 as _commons_pb2
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TemplateUsecase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEMPLATE_USECASE_UNSPECIFIED: _ClassVar[TemplateUsecase]
    LOGIN: _ClassVar[TemplateUsecase]
    OTP_LOGIN: _ClassVar[TemplateUsecase]
    MEMBER_INVITE: _ClassVar[TemplateUsecase]
    USER_INVITE: _ClassVar[TemplateUsecase]
    USER_LOGIN: _ClassVar[TemplateUsecase]
    SIGNUP: _ClassVar[TemplateUsecase]
    USER_LOGIN_OTP: _ClassVar[TemplateUsecase]
    USER_LOGIN_LINK: _ClassVar[TemplateUsecase]
    USER_LOGIN_LINK_OTP: _ClassVar[TemplateUsecase]
    USER_SIGNUP_OTP: _ClassVar[TemplateUsecase]
    USER_SIGNUP_LINK: _ClassVar[TemplateUsecase]
    USER_SIGNUP_LINK_OTP: _ClassVar[TemplateUsecase]

class EmailServerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[EmailServerType]
    INHOUSE: _ClassVar[EmailServerType]
    CUSTOMER: _ClassVar[EmailServerType]

class EmailServerProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMAIL_SERVER_UNSPECIFIED: _ClassVar[EmailServerProvider]
    SENDGRID: _ClassVar[EmailServerProvider]
    POSTMARK: _ClassVar[EmailServerProvider]
    OTHER: _ClassVar[EmailServerProvider]
TEMPLATE_USECASE_UNSPECIFIED: TemplateUsecase
LOGIN: TemplateUsecase
OTP_LOGIN: TemplateUsecase
MEMBER_INVITE: TemplateUsecase
USER_INVITE: TemplateUsecase
USER_LOGIN: TemplateUsecase
SIGNUP: TemplateUsecase
USER_LOGIN_OTP: TemplateUsecase
USER_LOGIN_LINK: TemplateUsecase
USER_LOGIN_LINK_OTP: TemplateUsecase
USER_SIGNUP_OTP: TemplateUsecase
USER_SIGNUP_LINK: TemplateUsecase
USER_SIGNUP_LINK_OTP: TemplateUsecase
UNSPECIFIED: EmailServerType
INHOUSE: EmailServerType
CUSTOMER: EmailServerType
EMAIL_SERVER_UNSPECIFIED: EmailServerProvider
SENDGRID: EmailServerProvider
POSTMARK: EmailServerProvider
OTHER: EmailServerProvider

class GetPlaceholdersRequest(_message.Message):
    __slots__ = ("use_case",)
    USE_CASE_FIELD_NUMBER: _ClassVar[int]
    use_case: TemplateUsecase
    def __init__(self, use_case: _Optional[_Union[TemplateUsecase, str]] = ...) -> None: ...

class GetPlaceholdersResponse(_message.Message):
    __slots__ = ("placeholders",)
    PLACEHOLDERS_FIELD_NUMBER: _ClassVar[int]
    placeholders: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, placeholders: _Optional[_Iterable[str]] = ...) -> None: ...

class GetTemplateUseCasesResponse(_message.Message):
    __slots__ = ("use_cases",)
    USE_CASES_FIELD_NUMBER: _ClassVar[int]
    use_cases: _containers.RepeatedCompositeFieldContainer[TemplateUsecaseWithPlaceholders]
    def __init__(self, use_cases: _Optional[_Iterable[_Union[TemplateUsecaseWithPlaceholders, _Mapping]]] = ...) -> None: ...

class TemplateUsecaseWithPlaceholders(_message.Message):
    __slots__ = ("use_case", "title", "description", "placeholders", "display", "default_template")
    USE_CASE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDERS_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    use_case: TemplateUsecase
    title: str
    description: str
    placeholders: _containers.RepeatedCompositeFieldContainer[Placeholder]
    display: bool
    default_template: Template
    def __init__(self, use_case: _Optional[_Union[TemplateUsecase, str]] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., placeholders: _Optional[_Iterable[_Union[Placeholder, _Mapping]]] = ..., display: bool = ..., default_template: _Optional[_Union[Template, _Mapping]] = ...) -> None: ...

class Placeholder(_message.Message):
    __slots__ = ("name", "title", "description", "display", "category")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    name: str
    title: str
    description: str
    display: bool
    category: str
    def __init__(self, name: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., display: bool = ..., category: _Optional[str] = ...) -> None: ...

class Template(_message.Message):
    __slots__ = ("updated_at", "id", "use_case", "enabled", "subject", "html_content", "plain_content", "placeholders")
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    USE_CASE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    HTML_CONTENT_FIELD_NUMBER: _ClassVar[int]
    PLAIN_CONTENT_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDERS_FIELD_NUMBER: _ClassVar[int]
    updated_at: _timestamp_pb2.Timestamp
    id: str
    use_case: TemplateUsecase
    enabled: bool
    subject: str
    html_content: str
    plain_content: str
    placeholders: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., use_case: _Optional[_Union[TemplateUsecase, str]] = ..., enabled: bool = ..., subject: _Optional[str] = ..., html_content: _Optional[str] = ..., plain_content: _Optional[str] = ..., placeholders: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateEmailTemplate(_message.Message):
    __slots__ = ("updated_at", "id", "use_case", "subject", "html_content", "plain_content")
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    USE_CASE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    HTML_CONTENT_FIELD_NUMBER: _ClassVar[int]
    PLAIN_CONTENT_FIELD_NUMBER: _ClassVar[int]
    updated_at: _timestamp_pb2.Timestamp
    id: str
    use_case: TemplateUsecase
    subject: str
    html_content: str
    plain_content: str
    def __init__(self, updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., use_case: _Optional[_Union[TemplateUsecase, str]] = ..., subject: _Optional[str] = ..., html_content: _Optional[str] = ..., plain_content: _Optional[str] = ...) -> None: ...

class CreateEmailTemplateRequest(_message.Message):
    __slots__ = ("organization_id", "template")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    template: CreateEmailTemplate
    def __init__(self, organization_id: _Optional[str] = ..., template: _Optional[_Union[CreateEmailTemplate, _Mapping]] = ...) -> None: ...

class CreateEmailTemplateResponse(_message.Message):
    __slots__ = ("template",)
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    template: Template
    def __init__(self, template: _Optional[_Union[Template, _Mapping]] = ...) -> None: ...

class EnableEmailTemplateRequest(_message.Message):
    __slots__ = ("organization_id", "template_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    template_id: str
    def __init__(self, organization_id: _Optional[str] = ..., template_id: _Optional[str] = ...) -> None: ...

class EnableEmailTemplateResponse(_message.Message):
    __slots__ = ("active_template_id", "last_active_template_id")
    ACTIVE_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVE_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    active_template_id: _wrappers_pb2.StringValue
    last_active_template_id: _wrappers_pb2.StringValue
    def __init__(self, active_template_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., last_active_template_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class DisableEmailTemplateRequest(_message.Message):
    __slots__ = ("organization_id", "template_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    template_id: str
    def __init__(self, organization_id: _Optional[str] = ..., template_id: _Optional[str] = ...) -> None: ...

class GetEmailTemplateRequest(_message.Message):
    __slots__ = ("organization_id", "template_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    template_id: str
    def __init__(self, organization_id: _Optional[str] = ..., template_id: _Optional[str] = ...) -> None: ...

class GetEmailTemplateResponse(_message.Message):
    __slots__ = ("template",)
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    template: Template
    def __init__(self, template: _Optional[_Union[Template, _Mapping]] = ...) -> None: ...

class ListEmailTemplateRequest(_message.Message):
    __slots__ = ("organization_id",)
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    def __init__(self, organization_id: _Optional[str] = ...) -> None: ...

class ListEmailTemplateResponse(_message.Message):
    __slots__ = ("templates",)
    TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    templates: _containers.RepeatedCompositeFieldContainer[Template]
    def __init__(self, templates: _Optional[_Iterable[_Union[Template, _Mapping]]] = ...) -> None: ...

class UpdateTemplate(_message.Message):
    __slots__ = ("subject", "html_content", "plain_content")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    HTML_CONTENT_FIELD_NUMBER: _ClassVar[int]
    PLAIN_CONTENT_FIELD_NUMBER: _ClassVar[int]
    subject: str
    html_content: str
    plain_content: str
    def __init__(self, subject: _Optional[str] = ..., html_content: _Optional[str] = ..., plain_content: _Optional[str] = ...) -> None: ...

class GetEmailConfigurationResponse(_message.Message):
    __slots__ = ("default_from_name", "default_from_address", "email_server_selected", "server")
    DEFAULT_FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    EMAIL_SERVER_SELECTED_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    default_from_name: str
    default_from_address: str
    email_server_selected: EmailServerType
    server: EmailServer
    def __init__(self, default_from_name: _Optional[str] = ..., default_from_address: _Optional[str] = ..., email_server_selected: _Optional[_Union[EmailServerType, str]] = ..., server: _Optional[_Union[EmailServer, _Mapping]] = ...) -> None: ...

class UpsertEmailConfigurationRequest(_message.Message):
    __slots__ = ("default_from_name", "server")
    DEFAULT_FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    default_from_name: str
    server: UpsertEmailConfigurationServer
    def __init__(self, default_from_name: _Optional[str] = ..., server: _Optional[_Union[UpsertEmailConfigurationServer, _Mapping]] = ...) -> None: ...

class UpsertEmailConfigurationServer(_message.Message):
    __slots__ = ("id", "provider", "enabled", "settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    provider: EmailServerProvider
    enabled: _wrappers_pb2.BoolValue
    settings: UpsertEmailConfigurationSMTPServerSettings
    def __init__(self, id: _Optional[str] = ..., provider: _Optional[_Union[EmailServerProvider, str]] = ..., enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., settings: _Optional[_Union[UpsertEmailConfigurationSMTPServerSettings, _Mapping]] = ...) -> None: ...

class UpsertEmailConfigurationSMTPServerSettings(_message.Message):
    __slots__ = ("host", "port", "username", "password", "from_email", "from_name")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FROM_EMAIL_FIELD_NUMBER: _ClassVar[int]
    FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    username: str
    password: str
    from_email: str
    from_name: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., from_email: _Optional[str] = ..., from_name: _Optional[str] = ...) -> None: ...

class UpsertEmailConfigurationResponse(_message.Message):
    __slots__ = ("default_from_name", "default_from_address", "email_server_selected", "server")
    DEFAULT_FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    EMAIL_SERVER_SELECTED_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    default_from_name: str
    default_from_address: str
    email_server_selected: EmailServerType
    server: EmailServer
    def __init__(self, default_from_name: _Optional[str] = ..., default_from_address: _Optional[str] = ..., email_server_selected: _Optional[_Union[EmailServerType, str]] = ..., server: _Optional[_Union[EmailServer, _Mapping]] = ...) -> None: ...

class PatchEmailTemplateRequest(_message.Message):
    __slots__ = ("organization_id", "template_id", "template", "update_mask")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    template_id: str
    template: UpdateTemplate
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, organization_id: _Optional[str] = ..., template_id: _Optional[str] = ..., template: _Optional[_Union[UpdateTemplate, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class DeleteEmailTemplateRequest(_message.Message):
    __slots__ = ("organization_id", "template_id")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    template_id: str
    def __init__(self, organization_id: _Optional[str] = ..., template_id: _Optional[str] = ...) -> None: ...

class EmailServer(_message.Message):
    __slots__ = ("updated_at", "id", "provider", "enabled", "smtp_settings")
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SMTP_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    updated_at: _timestamp_pb2.Timestamp
    id: str
    provider: EmailServerProvider
    enabled: bool
    smtp_settings: SMTPServerSettings
    def __init__(self, updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., provider: _Optional[_Union[EmailServerProvider, str]] = ..., enabled: bool = ..., smtp_settings: _Optional[_Union[SMTPServerSettings, _Mapping]] = ...) -> None: ...

class SMTPServerSettings(_message.Message):
    __slots__ = ("host", "port", "username", "password", "from_email", "from_name")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FROM_EMAIL_FIELD_NUMBER: _ClassVar[int]
    FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    username: str
    password: str
    from_email: str
    from_name: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., from_email: _Optional[str] = ..., from_name: _Optional[str] = ...) -> None: ...

class PatchSMTPServerSettings(_message.Message):
    __slots__ = ("host", "port", "username", "password", "from_email", "from_name")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FROM_EMAIL_FIELD_NUMBER: _ClassVar[int]
    FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    username: str
    password: str
    from_email: str
    from_name: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., from_email: _Optional[str] = ..., from_name: _Optional[str] = ...) -> None: ...

class CreateEmailServerRequest(_message.Message):
    __slots__ = ("provider", "settings")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    provider: EmailServerProvider
    settings: SMTPServerSettings
    def __init__(self, provider: _Optional[_Union[EmailServerProvider, str]] = ..., settings: _Optional[_Union[SMTPServerSettings, _Mapping]] = ...) -> None: ...

class CreateEmailServerResponse(_message.Message):
    __slots__ = ("server",)
    SERVER_FIELD_NUMBER: _ClassVar[int]
    server: EmailServer
    def __init__(self, server: _Optional[_Union[EmailServer, _Mapping]] = ...) -> None: ...

class GetEmailServerRequest(_message.Message):
    __slots__ = ("server_id",)
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    server_id: str
    def __init__(self, server_id: _Optional[str] = ...) -> None: ...

class GetEmailServerResponse(_message.Message):
    __slots__ = ("server",)
    SERVER_FIELD_NUMBER: _ClassVar[int]
    server: EmailServer
    def __init__(self, server: _Optional[_Union[EmailServer, _Mapping]] = ...) -> None: ...

class EnableEmailServerRequest(_message.Message):
    __slots__ = ("server_id",)
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    server_id: str
    def __init__(self, server_id: _Optional[str] = ...) -> None: ...

class EnableEmailServerResponse(_message.Message):
    __slots__ = ("active_server_id", "last_active_server_id")
    ACTIVE_SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVE_SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    active_server_id: _wrappers_pb2.StringValue
    last_active_server_id: _wrappers_pb2.StringValue
    def __init__(self, active_server_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., last_active_server_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class DisableEmailServerRequest(_message.Message):
    __slots__ = ("server_id",)
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    server_id: str
    def __init__(self, server_id: _Optional[str] = ...) -> None: ...

class ListEmailServerResponse(_message.Message):
    __slots__ = ("servers",)
    SERVERS_FIELD_NUMBER: _ClassVar[int]
    servers: _containers.RepeatedCompositeFieldContainer[EmailServer]
    def __init__(self, servers: _Optional[_Iterable[_Union[EmailServer, _Mapping]]] = ...) -> None: ...

class PatchEmailServerSettingsRequest(_message.Message):
    __slots__ = ("server_id", "settings")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    server_id: str
    settings: PatchSMTPServerSettings
    def __init__(self, server_id: _Optional[str] = ..., settings: _Optional[_Union[PatchSMTPServerSettings, _Mapping]] = ...) -> None: ...

class DeleteEmailServerRequest(_message.Message):
    __slots__ = ("server_id",)
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    server_id: str
    def __init__(self, server_id: _Optional[str] = ...) -> None: ...

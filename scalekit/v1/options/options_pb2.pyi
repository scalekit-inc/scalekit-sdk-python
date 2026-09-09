from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Policy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DENY: _ClassVar[Policy]
    PARTIAL: _ClassVar[Policy]
    ALLOW: _ClassVar[Policy]

class AuthenticationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BLOCKED: _ClassVar[AuthenticationType]
    NONE: _ClassVar[AuthenticationType]
    WORKSPACE: _ClassVar[AuthenticationType]
    CUSTOMER_PORTAL: _ClassVar[AuthenticationType]
    SESSION: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION: _ClassVar[AuthenticationType]
    WORKSPACE_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CUSTOMER_PORTAL: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CUSTOMER_PORTAL_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_CUSTOMER_PORTAL_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_CUSTOMER_PORTAL: _ClassVar[AuthenticationType]
    USER: _ClassVar[AuthenticationType]
    CLIENT: _ClassVar[AuthenticationType]
    SESSION_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CLIENT: _ClassVar[AuthenticationType]
    CUSTOMER_PORTAL_SESSION_CLIENT: _ClassVar[AuthenticationType]
    SESSION_USER: _ClassVar[AuthenticationType]
    ACTIONS_PORTAL: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CUSTOMER_PORTAL_ACTIONS_PORTAL: _ClassVar[AuthenticationType]
    WORKSPACE_SESSION_CUSTOMER_PORTAL_ACTIONS_PORTAL_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_ACTIONS_PORTAL: _ClassVar[AuthenticationType]
    WORKSPACE_ACTIONS_PORTAL_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_ACTIONS_PORTAL_CUSTOMER_PORTAL_CLIENT: _ClassVar[AuthenticationType]
    WORKSPACE_CUSTOMER_PORTAL_ACTIONS_PORTAL: _ClassVar[AuthenticationType]

class Mutation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MUTATION_UNSPECIFIED: _ClassVar[Mutation]
    READ: _ClassVar[Mutation]
    WRITE: _ClassVar[Mutation]
DENY: Policy
PARTIAL: Policy
ALLOW: Policy
BLOCKED: AuthenticationType
NONE: AuthenticationType
WORKSPACE: AuthenticationType
CUSTOMER_PORTAL: AuthenticationType
SESSION: AuthenticationType
WORKSPACE_SESSION: AuthenticationType
WORKSPACE_CLIENT: AuthenticationType
WORKSPACE_SESSION_CUSTOMER_PORTAL: AuthenticationType
WORKSPACE_SESSION_CUSTOMER_PORTAL_CLIENT: AuthenticationType
WORKSPACE_CUSTOMER_PORTAL_CLIENT: AuthenticationType
WORKSPACE_CUSTOMER_PORTAL: AuthenticationType
USER: AuthenticationType
CLIENT: AuthenticationType
SESSION_CLIENT: AuthenticationType
WORKSPACE_SESSION_CLIENT: AuthenticationType
CUSTOMER_PORTAL_SESSION_CLIENT: AuthenticationType
SESSION_USER: AuthenticationType
ACTIONS_PORTAL: AuthenticationType
WORKSPACE_SESSION_CUSTOMER_PORTAL_ACTIONS_PORTAL: AuthenticationType
WORKSPACE_SESSION_CUSTOMER_PORTAL_ACTIONS_PORTAL_CLIENT: AuthenticationType
WORKSPACE_ACTIONS_PORTAL: AuthenticationType
WORKSPACE_ACTIONS_PORTAL_CLIENT: AuthenticationType
WORKSPACE_ACTIONS_PORTAL_CUSTOMER_PORTAL_CLIENT: AuthenticationType
WORKSPACE_CUSTOMER_PORTAL_ACTIONS_PORTAL: AuthenticationType
MUTATION_UNSPECIFIED: Mutation
READ: Mutation
WRITE: Mutation
AUTH_OPTION_FIELD_NUMBER: _ClassVar[int]
auth_option: _descriptor.FieldDescriptor
AGENT_TOOL_FIELD_NUMBER: _ClassVar[int]
agent_tool: _descriptor.FieldDescriptor
AGENT_FIELD_FIELD_NUMBER: _ClassVar[int]
agent_field: _descriptor.FieldDescriptor

class AuthOption(_message.Message):
    __slots__ = ("authentication_type", "permissions", "policy")
    AUTHENTICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    authentication_type: AuthenticationType
    permissions: _containers.RepeatedScalarFieldContainer[str]
    policy: Policy
    def __init__(self, authentication_type: _Optional[_Union[AuthenticationType, str]] = ..., permissions: _Optional[_Iterable[str]] = ..., policy: _Optional[_Union[Policy, str]] = ...) -> None: ...

class AgentToolOption(_message.Message):
    __slots__ = ("name", "description", "mutation", "summary", "scope_fields")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MUTATION_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    mutation: Mutation
    summary: str
    scope_fields: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., mutation: _Optional[_Union[Mutation, str]] = ..., summary: _Optional[str] = ..., scope_fields: _Optional[_Iterable[str]] = ...) -> None: ...

class AgentFieldOption(_message.Message):
    __slots__ = ("expose",)
    EXPOSE_FIELD_NUMBER: _ClassVar[int]
    expose: bool
    def __init__(self, expose: bool = ...) -> None: ...

from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from scalekit.v1.options import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GatewayGroupSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GATEWAY_GROUP_SOURCE_UNSPECIFIED: _ClassVar[GatewayGroupSource]
    GATEWAY_GROUP_SOURCE_BUILTIN: _ClassVar[GatewayGroupSource]
    GATEWAY_GROUP_SOURCE_DIRECTORY: _ClassVar[GatewayGroupSource]
    GATEWAY_GROUP_SOURCE_MANUAL: _ClassVar[GatewayGroupSource]

class GroupConnectionPolicyMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GROUP_CONNECTION_POLICY_MODE_UNSPECIFIED: _ClassVar[GroupConnectionPolicyMode]
    GROUP_CONNECTION_POLICY_MODE_ALL: _ClassVar[GroupConnectionPolicyMode]
    GROUP_CONNECTION_POLICY_MODE_SUBSET_ALLOW: _ClassVar[GroupConnectionPolicyMode]
    GROUP_CONNECTION_POLICY_MODE_SUBSET_DENY: _ClassVar[GroupConnectionPolicyMode]

class ToolPolicyMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOOL_POLICY_MODE_UNSPECIFIED: _ClassVar[ToolPolicyMode]
    TOOL_POLICY_MODE_ALLOW: _ClassVar[ToolPolicyMode]
    TOOL_POLICY_MODE_DENY: _ClassVar[ToolPolicyMode]
GATEWAY_GROUP_SOURCE_UNSPECIFIED: GatewayGroupSource
GATEWAY_GROUP_SOURCE_BUILTIN: GatewayGroupSource
GATEWAY_GROUP_SOURCE_DIRECTORY: GatewayGroupSource
GATEWAY_GROUP_SOURCE_MANUAL: GatewayGroupSource
GROUP_CONNECTION_POLICY_MODE_UNSPECIFIED: GroupConnectionPolicyMode
GROUP_CONNECTION_POLICY_MODE_ALL: GroupConnectionPolicyMode
GROUP_CONNECTION_POLICY_MODE_SUBSET_ALLOW: GroupConnectionPolicyMode
GROUP_CONNECTION_POLICY_MODE_SUBSET_DENY: GroupConnectionPolicyMode
TOOL_POLICY_MODE_UNSPECIFIED: ToolPolicyMode
TOOL_POLICY_MODE_ALLOW: ToolPolicyMode
TOOL_POLICY_MODE_DENY: ToolPolicyMode

class Gateway(_message.Message):
    __slots__ = ("id", "environment_id", "url", "authorization_server_url", "protected_resource_metadata_url", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_SERVER_URL_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_RESOURCE_METADATA_URL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    url: str
    authorization_server_url: str
    protected_resource_metadata_url: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., url: _Optional[str] = ..., authorization_server_url: _Optional[str] = ..., protected_resource_metadata_url: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EnableGatewayRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EnableGatewayResponse(_message.Message):
    __slots__ = ("gateway", "already_enabled")
    GATEWAY_FIELD_NUMBER: _ClassVar[int]
    ALREADY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    gateway: Gateway
    already_enabled: bool
    def __init__(self, gateway: _Optional[_Union[Gateway, _Mapping]] = ..., already_enabled: bool = ...) -> None: ...

class GetGatewayRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetGatewayResponse(_message.Message):
    __slots__ = ("gateway", "organization_id", "enabled")
    GATEWAY_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    gateway: Gateway
    organization_id: str
    enabled: bool
    def __init__(self, gateway: _Optional[_Union[Gateway, _Mapping]] = ..., organization_id: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class SetupGatewayIdentityRequest(_message.Message):
    __slots__ = ("organization_name",)
    ORGANIZATION_NAME_FIELD_NUMBER: _ClassVar[int]
    organization_name: str
    def __init__(self, organization_name: _Optional[str] = ...) -> None: ...

class SetupGatewayIdentityResponse(_message.Message):
    __slots__ = ("organization_id", "already_provisioned")
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ALREADY_PROVISIONED_FIELD_NUMBER: _ClassVar[int]
    organization_id: str
    already_provisioned: bool
    def __init__(self, organization_id: _Optional[str] = ..., already_provisioned: bool = ...) -> None: ...

class DisableGatewayRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DisableGatewayResponse(_message.Message):
    __slots__ = ("already_disabled",)
    ALREADY_DISABLED_FIELD_NUMBER: _ClassVar[int]
    already_disabled: bool
    def __init__(self, already_disabled: bool = ...) -> None: ...

class GatewayGroup(_message.Message):
    __slots__ = ("id", "environment_id", "organization_id", "source", "directory_group_id", "builtin_name", "display_name", "description", "member_count", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    BUILTIN_NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    organization_id: str
    source: GatewayGroupSource
    directory_group_id: str
    builtin_name: str
    display_name: str
    description: str
    member_count: int
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., source: _Optional[_Union[GatewayGroupSource, str]] = ..., directory_group_id: _Optional[str] = ..., builtin_name: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., member_count: _Optional[int] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListGatewayGroupsRequest(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: GatewayGroupSource
    def __init__(self, source: _Optional[_Union[GatewayGroupSource, str]] = ...) -> None: ...

class ListGatewayGroupsResponse(_message.Message):
    __slots__ = ("groups",)
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[GatewayGroup]
    def __init__(self, groups: _Optional[_Iterable[_Union[GatewayGroup, _Mapping]]] = ...) -> None: ...

class CreateManualGatewayGroupRequest(_message.Message):
    __slots__ = ("display_name", "description")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateManualGatewayGroupResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: GatewayGroup
    def __init__(self, group: _Optional[_Union[GatewayGroup, _Mapping]] = ...) -> None: ...

class UpdateManualGatewayGroupRequest(_message.Message):
    __slots__ = ("group_id", "display_name", "description")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    display_name: str
    description: str
    def __init__(self, group_id: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class UpdateManualGatewayGroupResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: GatewayGroup
    def __init__(self, group: _Optional[_Union[GatewayGroup, _Mapping]] = ...) -> None: ...

class DeleteManualGatewayGroupRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    def __init__(self, group_id: _Optional[str] = ...) -> None: ...

class DeleteManualGatewayGroupResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ManualGroupMember(_message.Message):
    __slots__ = ("group_id", "user_id", "user_email", "user_display_name", "added_at")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ADDED_AT_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    user_id: str
    user_email: str
    user_display_name: str
    added_at: _timestamp_pb2.Timestamp
    def __init__(self, group_id: _Optional[str] = ..., user_id: _Optional[str] = ..., user_email: _Optional[str] = ..., user_display_name: _Optional[str] = ..., added_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListManualGatewayGroupMembersRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    def __init__(self, group_id: _Optional[str] = ...) -> None: ...

class ListManualGatewayGroupMembersResponse(_message.Message):
    __slots__ = ("members",)
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[ManualGroupMember]
    def __init__(self, members: _Optional[_Iterable[_Union[ManualGroupMember, _Mapping]]] = ...) -> None: ...

class AddManualGatewayGroupMemberRequest(_message.Message):
    __slots__ = ("group_id", "user_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    user_id: str
    def __init__(self, group_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class AddManualGatewayGroupMemberResponse(_message.Message):
    __slots__ = ("member",)
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    member: ManualGroupMember
    def __init__(self, member: _Optional[_Union[ManualGroupMember, _Mapping]] = ...) -> None: ...

class RemoveManualGatewayGroupMemberRequest(_message.Message):
    __slots__ = ("group_id", "user_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    user_id: str
    def __init__(self, group_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class RemoveManualGatewayGroupMemberResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GroupConnectionGrant(_message.Message):
    __slots__ = ("id", "environment_id", "group_id", "connection_id", "policy_mode", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_MODE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    group_id: str
    connection_id: str
    policy_mode: GroupConnectionPolicyMode
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., environment_id: _Optional[str] = ..., group_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., policy_mode: _Optional[_Union[GroupConnectionPolicyMode, str]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class UpsertGroupConnectionGrantRequest(_message.Message):
    __slots__ = ("group_id", "connection_id", "policy_mode")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_MODE_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    connection_id: str
    policy_mode: GroupConnectionPolicyMode
    def __init__(self, group_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., policy_mode: _Optional[_Union[GroupConnectionPolicyMode, str]] = ...) -> None: ...

class UpsertGroupConnectionGrantResponse(_message.Message):
    __slots__ = ("grant",)
    GRANT_FIELD_NUMBER: _ClassVar[int]
    grant: GroupConnectionGrant
    def __init__(self, grant: _Optional[_Union[GroupConnectionGrant, _Mapping]] = ...) -> None: ...

class DeleteGroupConnectionGrantRequest(_message.Message):
    __slots__ = ("group_id", "connection_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    connection_id: str
    def __init__(self, group_id: _Optional[str] = ..., connection_id: _Optional[str] = ...) -> None: ...

class DeleteGroupConnectionGrantResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListGroupConnectionGrantsRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: str
    def __init__(self, connection_id: _Optional[str] = ...) -> None: ...

class ListGroupConnectionGrantsResponse(_message.Message):
    __slots__ = ("grants",)
    GRANTS_FIELD_NUMBER: _ClassVar[int]
    grants: _containers.RepeatedCompositeFieldContainer[GroupConnectionGrant]
    def __init__(self, grants: _Optional[_Iterable[_Union[GroupConnectionGrant, _Mapping]]] = ...) -> None: ...

class GroupToolPolicy(_message.Message):
    __slots__ = ("id", "group_id", "connection_id", "tool_name", "mode", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    group_id: str
    connection_id: str
    tool_name: str
    mode: ToolPolicyMode
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., group_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., tool_name: _Optional[str] = ..., mode: _Optional[_Union[ToolPolicyMode, str]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GroupToolPolicyInput(_message.Message):
    __slots__ = ("tool_name", "mode")
    TOOL_NAME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    tool_name: str
    mode: ToolPolicyMode
    def __init__(self, tool_name: _Optional[str] = ..., mode: _Optional[_Union[ToolPolicyMode, str]] = ...) -> None: ...

class ReplaceGroupToolPoliciesRequest(_message.Message):
    __slots__ = ("group_id", "connection_id", "policies")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    connection_id: str
    policies: _containers.RepeatedCompositeFieldContainer[GroupToolPolicyInput]
    def __init__(self, group_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., policies: _Optional[_Iterable[_Union[GroupToolPolicyInput, _Mapping]]] = ...) -> None: ...

class ReplaceGroupToolPoliciesResponse(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[GroupToolPolicy]
    def __init__(self, policies: _Optional[_Iterable[_Union[GroupToolPolicy, _Mapping]]] = ...) -> None: ...

class ListGroupToolPoliciesRequest(_message.Message):
    __slots__ = ("group_id", "connection_id")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    connection_id: str
    def __init__(self, group_id: _Optional[str] = ..., connection_id: _Optional[str] = ...) -> None: ...

class ListGroupToolPoliciesResponse(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[GroupToolPolicy]
    def __init__(self, policies: _Optional[_Iterable[_Union[GroupToolPolicy, _Mapping]]] = ...) -> None: ...

class PreviewEffectivePolicyRequest(_message.Message):
    __slots__ = ("user_id", "connection_id", "candidate_tool_names")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_TOOL_NAMES_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    connection_id: str
    candidate_tool_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, user_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., candidate_tool_names: _Optional[_Iterable[str]] = ...) -> None: ...

class PreviewEffectivePolicyResponse(_message.Message):
    __slots__ = ("contributing_group_ids", "permitted_tool_names")
    CONTRIBUTING_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    PERMITTED_TOOL_NAMES_FIELD_NUMBER: _ClassVar[int]
    contributing_group_ids: _containers.RepeatedScalarFieldContainer[str]
    permitted_tool_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, contributing_group_ids: _Optional[_Iterable[str]] = ..., permitted_tool_names: _Optional[_Iterable[str]] = ...) -> None: ...

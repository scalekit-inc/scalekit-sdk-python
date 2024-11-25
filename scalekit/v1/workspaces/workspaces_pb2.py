# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/workspaces/workspaces.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from scalekit.v1.commons import commons_pb2 as scalekit_dot_v1_dot_commons_dot_commons__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'scalekit/v1/workspaces/workspaces.proto\x12\x16scalekit.v1.workspaces\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a!scalekit/v1/commons/commons.proto\x1a!scalekit/v1/options/options.proto\"\x96\x02\n\tWorkspace\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03\x65nvR\x02id\x12;\n\x0b\x63reate_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12-\n\x0c\x64isplay_name\x18\x04 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\xc8\x01R\x0b\x64isplayName\x12@\n\x0bregion_code\x18\x06 \x01(\x0e\x32\x1f.scalekit.v1.commons.RegionCodeR\nregionCode\"\x89\x02\n\x0f\x43reateWorkspace\x12V\n\x05\x65mail\x18\x01 \x01(\tB@\xbaH=\xba\x01:\n\x0bvalid_email\x12\x1b\x65mail must be a valid email\x1a\x0ethis.isEmail()R\x05\x65mail\x12)\n\x07\x63ompany\x18\x02 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\x80\x02H\x00R\x07\x63ompany\x88\x01\x01\x12P\n\x12send_welcome_email\x18\x03 \x01(\x0e\x32\x1d.scalekit.v1.workspaces.YesNoH\x01R\x10sendWelcomeEmail\x88\x01\x01\x42\n\n\x08_companyB\x15\n\x13_send_welcome_email\"@\n\x0fUpdateWorkspace\x12-\n\x0c\x64isplay_name\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\x80\x02R\x0b\x64isplayName\"\xb2\x01\n\x10OnboardWorkspace\x12@\n\x16workspace_display_name\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\x80\x02R\x14workspaceDisplayName\x12\x32\n\x0fuser_given_name\x18\x02 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\x80\x02R\ruserGivenName\x12(\n\x10user_family_name\x18\x03 \x01(\tR\x0euserFamilyName\"g\n\x16\x43reateWorkspaceRequest\x12M\n\tworkspace\x18\x01 \x01(\x0b\x32\'.scalekit.v1.workspaces.CreateWorkspaceB\x06\xbaH\x03\xc8\x01\x01R\tworkspace\"n\n\x17\x43reateWorkspaceResponse\x12?\n\tworkspace\x18\x01 \x01(\x0b\x32!.scalekit.v1.workspaces.WorkspaceR\tworkspace\x12\x12\n\x04link\x18\x02 \x01(\tR\x04link\"\x87\x01\n\x16UpdateWorkspaceRequest\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\x12M\n\tworkspace\x18\x02 \x01(\x0b\x32\'.scalekit.v1.workspaces.UpdateWorkspaceB\x06\xbaH\x03\xc8\x01\x01R\tworkspace\"i\n\x17OnboardWorkspaceRequest\x12N\n\tworkspace\x18\x02 \x01(\x0b\x32(.scalekit.v1.workspaces.OnboardWorkspaceB\x06\xbaH\x03\xc8\x01\x01R\tworkspace\"n\n\x1dUpdateCurrentWorkspaceRequest\x12M\n\tworkspace\x18\x01 \x01(\x0b\x32\'.scalekit.v1.workspaces.UpdateWorkspaceB\x06\xbaH\x03\xc8\x01\x01R\tworkspace\"Z\n\x17UpdateWorkspaceResponse\x12?\n\tworkspace\x18\x01 \x01(\x0b\x32!.scalekit.v1.workspaces.WorkspaceR\tworkspace\"5\n\x13GetWorkspaceRequest\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\"\x1c\n\x1aGetCurrentWorkspaceRequest\"W\n\x14GetWorkspaceResponse\x12?\n\tworkspace\x18\x01 \x01(\x0b\x32!.scalekit.v1.workspaces.WorkspaceR\tworkspace\"9\n\x17GetBillingPortalRequest\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\"<\n\x18GetBillingPortalResponse\x12\x10\n\x03url\x18\x01 \x01(\tR\x03url\x12\x0e\n\x02id\x18\x02 \x01(\tR\x02id\"A\n\x1fGetWorkspacePricingTableRequest\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\"\x82\x02\n GetWorkspacePricingTableResponse\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12(\n\x10pricing_table_id\x18\x02 \x01(\tR\x0epricingTableId\x12+\n\x11publishable_token\x18\x03 \x01(\tR\x10publishableToken\x12\x43\n\x1e\x63ustomer_session_client_secret\x18\x04 \x01(\tR\x1b\x63ustomerSessionClientSecret\x12\x32\n\x06\x65xpiry\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x06\x65xpiry\"B\n GetWorkspaceSubscriptionsRequest\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\"\x8f\x01\n!GetWorkspaceSubscriptionsResponse\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\x12J\n\rsubscriptions\x18\x02 \x03(\x0b\x32$.scalekit.v1.workspaces.SubscriptionR\rsubscriptions\"6\n\x0cSubscription\x12\x0e\n\x02id\x18\x02 \x01(\tR\x02id\x12\x16\n\x06status\x18\x07 \x01(\tR\x06status*\x18\n\x05YesNo\x12\x07\n\x03YES\x10\x00\x12\x06\n\x02NO\x10\x01\x32\xa7\x0c\n\x10WorkspaceService\x12\x9b\x01\n\x0f\x43reateWorkspace\x12..scalekit.v1.workspaces.CreateWorkspaceRequest\x1a/.scalekit.v1.workspaces.CreateWorkspaceResponse\"\'\x82\xb5\x18\x02\x18\x01\x82\xd3\xe4\x93\x02\x1b\"\x0e/api/v1/signup:\tworkspace\x12\x90\x01\n\x0cGetWorkspace\x12+.scalekit.v1.workspaces.GetWorkspaceRequest\x1a,.scalekit.v1.workspaces.GetWorkspaceResponse\"%\x82\xb5\x18\x02\x18@\x82\xd3\xe4\x93\x02\x19\x12\x17/api/v1/workspaces/{id}\x12\x9e\x01\n\x13GetCurrentWorkspace\x12\x32.scalekit.v1.workspaces.GetCurrentWorkspaceRequest\x1a,.scalekit.v1.workspaces.GetWorkspaceResponse\"%\x82\xb5\x18\x02\x18P\x82\xd3\xe4\x93\x02\x19\x12\x17/api/v1/workspaces:this\x12\xa4\x01\n\x0fUpdateWorkspace\x12..scalekit.v1.workspaces.UpdateWorkspaceRequest\x1a/.scalekit.v1.workspaces.UpdateWorkspaceResponse\"0\x82\xb5\x18\x02\x18@\x82\xd3\xe4\x93\x02$2\x17/api/v1/workspaces/{id}:\tworkspace\x12\x90\x01\n\x10OnboardWorkspace\x12/.scalekit.v1.workspaces.OnboardWorkspaceRequest\x1a\x16.google.protobuf.Empty\"3\x82\xb5\x18\x02\x18@\x82\xd3\xe4\x93\x02\'2\x1a/api/v1/workspaces:onboard:\tworkspace\x12\xb2\x01\n\x16UpdateCurrentWorkspace\x12\x35.scalekit.v1.workspaces.UpdateCurrentWorkspaceRequest\x1a/.scalekit.v1.workspaces.UpdateWorkspaceResponse\"0\x82\xb5\x18\x02\x18P\x82\xd3\xe4\x93\x02$2\x17/api/v1/workspaces:this:\tworkspace\x12\xcd\x01\n\x19GetWorkspaceSubscriptions\x12\x38.scalekit.v1.workspaces.GetWorkspaceSubscriptionsRequest\x1a\x39.scalekit.v1.workspaces.GetWorkspaceSubscriptionsResponse\";\x82\xb5\x18\x02\x18P\x82\xd3\xe4\x93\x02/\x12-/api/v1/workspaces/{id}/billing/subscriptions\x12\xca\x01\n\x18GetWorkspacePricingTable\x12\x37.scalekit.v1.workspaces.GetWorkspacePricingTableRequest\x1a\x38.scalekit.v1.workspaces.GetWorkspacePricingTableResponse\";\x82\xb5\x18\x02\x18P\x82\xd3\xe4\x93\x02/\x12-/api/v1/workspaces/{id}/billing/pricing-table\x12\xb4\x01\n\x10GetBillingPortal\x12/.scalekit.v1.workspaces.GetBillingPortalRequest\x1a\x30.scalekit.v1.workspaces.GetBillingPortalResponse\"=\x82\xb5\x18\x02\x18P\x82\xd3\xe4\x93\x02\x31\x12//api/v1/workspaces/{id}/billing/customer-portalB6Z4github.com/scalekit-inc/scalekit/pkg/grpc/workspacesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.workspaces.workspaces_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z4github.com/scalekit-inc/scalekit/pkg/grpc/workspaces'
  _globals['_WORKSPACE'].fields_by_name['id']._loaded_options = None
  _globals['_WORKSPACE'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003env'
  _globals['_WORKSPACE'].fields_by_name['display_name']._loaded_options = None
  _globals['_WORKSPACE'].fields_by_name['display_name']._serialized_options = b'\272H\007r\005\020\001\030\310\001'
  _globals['_CREATEWORKSPACE'].fields_by_name['email']._loaded_options = None
  _globals['_CREATEWORKSPACE'].fields_by_name['email']._serialized_options = b'\272H=\272\001:\n\013valid_email\022\033email must be a valid email\032\016this.isEmail()'
  _globals['_CREATEWORKSPACE'].fields_by_name['company']._loaded_options = None
  _globals['_CREATEWORKSPACE'].fields_by_name['company']._serialized_options = b'\272H\007r\005\020\001\030\200\002'
  _globals['_UPDATEWORKSPACE'].fields_by_name['display_name']._loaded_options = None
  _globals['_UPDATEWORKSPACE'].fields_by_name['display_name']._serialized_options = b'\272H\007r\005\020\001\030\200\002'
  _globals['_ONBOARDWORKSPACE'].fields_by_name['workspace_display_name']._loaded_options = None
  _globals['_ONBOARDWORKSPACE'].fields_by_name['workspace_display_name']._serialized_options = b'\272H\007r\005\020\001\030\200\002'
  _globals['_ONBOARDWORKSPACE'].fields_by_name['user_given_name']._loaded_options = None
  _globals['_ONBOARDWORKSPACE'].fields_by_name['user_given_name']._serialized_options = b'\272H\007r\005\020\001\030\200\002'
  _globals['_CREATEWORKSPACEREQUEST'].fields_by_name['workspace']._loaded_options = None
  _globals['_CREATEWORKSPACEREQUEST'].fields_by_name['workspace']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['workspace']._loaded_options = None
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['workspace']._serialized_options = b'\272H\003\310\001\001'
  _globals['_ONBOARDWORKSPACEREQUEST'].fields_by_name['workspace']._loaded_options = None
  _globals['_ONBOARDWORKSPACEREQUEST'].fields_by_name['workspace']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPDATECURRENTWORKSPACEREQUEST'].fields_by_name['workspace']._loaded_options = None
  _globals['_UPDATECURRENTWORKSPACEREQUEST'].fields_by_name['workspace']._serialized_options = b'\272H\003\310\001\001'
  _globals['_GETWORKSPACEREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_GETWORKSPACEREQUEST'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_GETBILLINGPORTALREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_GETBILLINGPORTALREQUEST'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_GETWORKSPACEPRICINGTABLEREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_GETWORKSPACEPRICINGTABLEREQUEST'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_GETWORKSPACESUBSCRIPTIONSREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_GETWORKSPACESUBSCRIPTIONSREQUEST'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_GETWORKSPACESUBSCRIPTIONSRESPONSE'].fields_by_name['id']._loaded_options = None
  _globals['_GETWORKSPACESUBSCRIPTIONSRESPONSE'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_WORKSPACESERVICE'].methods_by_name['CreateWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['CreateWorkspace']._serialized_options = b'\202\265\030\002\030\001\202\323\344\223\002\033\"\016/api/v1/signup:\tworkspace'
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspace']._serialized_options = b'\202\265\030\002\030@\202\323\344\223\002\031\022\027/api/v1/workspaces/{id}'
  _globals['_WORKSPACESERVICE'].methods_by_name['GetCurrentWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['GetCurrentWorkspace']._serialized_options = b'\202\265\030\002\030P\202\323\344\223\002\031\022\027/api/v1/workspaces:this'
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateWorkspace']._serialized_options = b'\202\265\030\002\030@\202\323\344\223\002$2\027/api/v1/workspaces/{id}:\tworkspace'
  _globals['_WORKSPACESERVICE'].methods_by_name['OnboardWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['OnboardWorkspace']._serialized_options = b'\202\265\030\002\030@\202\323\344\223\002\'2\032/api/v1/workspaces:onboard:\tworkspace'
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateCurrentWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateCurrentWorkspace']._serialized_options = b'\202\265\030\002\030P\202\323\344\223\002$2\027/api/v1/workspaces:this:\tworkspace'
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspaceSubscriptions']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspaceSubscriptions']._serialized_options = b'\202\265\030\002\030P\202\323\344\223\002/\022-/api/v1/workspaces/{id}/billing/subscriptions'
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspacePricingTable']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspacePricingTable']._serialized_options = b'\202\265\030\002\030P\202\323\344\223\002/\022-/api/v1/workspaces/{id}/billing/pricing-table'
  _globals['_WORKSPACESERVICE'].methods_by_name['GetBillingPortal']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['GetBillingPortal']._serialized_options = b'\202\265\030\002\030P\202\323\344\223\0021\022//api/v1/workspaces/{id}/billing/customer-portal'
  _globals['_YESNO']._serialized_start=2705
  _globals['_YESNO']._serialized_end=2729
  _globals['_WORKSPACE']._serialized_start=351
  _globals['_WORKSPACE']._serialized_end=629
  _globals['_CREATEWORKSPACE']._serialized_start=632
  _globals['_CREATEWORKSPACE']._serialized_end=897
  _globals['_UPDATEWORKSPACE']._serialized_start=899
  _globals['_UPDATEWORKSPACE']._serialized_end=963
  _globals['_ONBOARDWORKSPACE']._serialized_start=966
  _globals['_ONBOARDWORKSPACE']._serialized_end=1144
  _globals['_CREATEWORKSPACEREQUEST']._serialized_start=1146
  _globals['_CREATEWORKSPACEREQUEST']._serialized_end=1249
  _globals['_CREATEWORKSPACERESPONSE']._serialized_start=1251
  _globals['_CREATEWORKSPACERESPONSE']._serialized_end=1361
  _globals['_UPDATEWORKSPACEREQUEST']._serialized_start=1364
  _globals['_UPDATEWORKSPACEREQUEST']._serialized_end=1499
  _globals['_ONBOARDWORKSPACEREQUEST']._serialized_start=1501
  _globals['_ONBOARDWORKSPACEREQUEST']._serialized_end=1606
  _globals['_UPDATECURRENTWORKSPACEREQUEST']._serialized_start=1608
  _globals['_UPDATECURRENTWORKSPACEREQUEST']._serialized_end=1718
  _globals['_UPDATEWORKSPACERESPONSE']._serialized_start=1720
  _globals['_UPDATEWORKSPACERESPONSE']._serialized_end=1810
  _globals['_GETWORKSPACEREQUEST']._serialized_start=1812
  _globals['_GETWORKSPACEREQUEST']._serialized_end=1865
  _globals['_GETCURRENTWORKSPACEREQUEST']._serialized_start=1867
  _globals['_GETCURRENTWORKSPACEREQUEST']._serialized_end=1895
  _globals['_GETWORKSPACERESPONSE']._serialized_start=1897
  _globals['_GETWORKSPACERESPONSE']._serialized_end=1984
  _globals['_GETBILLINGPORTALREQUEST']._serialized_start=1986
  _globals['_GETBILLINGPORTALREQUEST']._serialized_end=2043
  _globals['_GETBILLINGPORTALRESPONSE']._serialized_start=2045
  _globals['_GETBILLINGPORTALRESPONSE']._serialized_end=2105
  _globals['_GETWORKSPACEPRICINGTABLEREQUEST']._serialized_start=2107
  _globals['_GETWORKSPACEPRICINGTABLEREQUEST']._serialized_end=2172
  _globals['_GETWORKSPACEPRICINGTABLERESPONSE']._serialized_start=2175
  _globals['_GETWORKSPACEPRICINGTABLERESPONSE']._serialized_end=2433
  _globals['_GETWORKSPACESUBSCRIPTIONSREQUEST']._serialized_start=2435
  _globals['_GETWORKSPACESUBSCRIPTIONSREQUEST']._serialized_end=2501
  _globals['_GETWORKSPACESUBSCRIPTIONSRESPONSE']._serialized_start=2504
  _globals['_GETWORKSPACESUBSCRIPTIONSRESPONSE']._serialized_end=2647
  _globals['_SUBSCRIPTION']._serialized_start=2649
  _globals['_SUBSCRIPTION']._serialized_end=2703
  _globals['_WORKSPACESERVICE']._serialized_start=2732
  _globals['_WORKSPACESERVICE']._serialized_end=4307
# @@protoc_insertion_point(module_scope)

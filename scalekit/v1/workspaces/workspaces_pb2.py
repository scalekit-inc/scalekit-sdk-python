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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'scalekit/v1/workspaces/workspaces.proto\x12\x16scalekit.v1.workspaces\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a!scalekit/v1/commons/commons.proto\x1a!scalekit/v1/options/options.proto\"\x96\x02\n\tWorkspace\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03\x65nvR\x02id\x12;\n\x0b\x63reate_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12-\n\x0c\x64isplay_name\x18\x04 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\xc8\x01R\x0b\x64isplayName\x12@\n\x0bregion_code\x18\x06 \x01(\x0e\x32\x1f.scalekit.v1.commons.RegionCodeR\nregionCode\"\xd3\x01\n\x0f\x43reateWorkspace\x12 \n\x05\x65mail\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\x80\x02R\x05\x65mail\x12)\n\x07\x63ompany\x18\x02 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\x80\x02H\x00R\x07\x63ompany\x88\x01\x01\x12P\n\x12send_welcome_email\x18\x03 \x01(\x0e\x32\x1d.scalekit.v1.workspaces.YesNoH\x01R\x10sendWelcomeEmail\x88\x01\x01\x42\n\n\x08_companyB\x15\n\x13_send_welcome_email\"@\n\x0fUpdateWorkspace\x12-\n\x0c\x64isplay_name\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\x80\x02R\x0b\x64isplayName\"g\n\x16\x43reateWorkspaceRequest\x12M\n\tworkspace\x18\x01 \x01(\x0b\x32\'.scalekit.v1.workspaces.CreateWorkspaceB\x06\xbaH\x03\xc8\x01\x01R\tworkspace\"n\n\x17\x43reateWorkspaceResponse\x12?\n\tworkspace\x18\x01 \x01(\x0b\x32!.scalekit.v1.workspaces.WorkspaceR\tworkspace\x12\x12\n\x04link\x18\x02 \x01(\tR\x04link\"\x87\x01\n\x16UpdateWorkspaceRequest\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\x12M\n\tworkspace\x18\x02 \x01(\x0b\x32\'.scalekit.v1.workspaces.UpdateWorkspaceB\x06\xbaH\x03\xc8\x01\x01R\tworkspace\"n\n\x1dUpdateCurrentWorkspaceRequest\x12M\n\tworkspace\x18\x01 \x01(\x0b\x32\'.scalekit.v1.workspaces.UpdateWorkspaceB\x06\xbaH\x03\xc8\x01\x01R\tworkspace\"Z\n\x17UpdateWorkspaceResponse\x12?\n\tworkspace\x18\x01 \x01(\x0b\x32!.scalekit.v1.workspaces.WorkspaceR\tworkspace\"5\n\x13GetWorkspaceRequest\x12\x1e\n\x02id\x18\x01 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03wksR\x02id\"\x1c\n\x1aGetCurrentWorkspaceRequest\"W\n\x14GetWorkspaceResponse\x12?\n\tworkspace\x18\x01 \x01(\x0b\x32!.scalekit.v1.workspaces.WorkspaceR\tworkspace*\x18\n\x05YesNo\x12\x07\n\x03YES\x10\x00\x12\x06\n\x02NO\x10\x01\x32\xc0\x06\n\x10WorkspaceService\x12\x9b\x01\n\x0f\x43reateWorkspace\x12..scalekit.v1.workspaces.CreateWorkspaceRequest\x1a/.scalekit.v1.workspaces.CreateWorkspaceResponse\"\'\x82\xb5\x18\x02\x18\x01\x82\xd3\xe4\x93\x02\x1b\"\x0e/api/v1/signup:\tworkspace\x12\x90\x01\n\x0cGetWorkspace\x12+.scalekit.v1.workspaces.GetWorkspaceRequest\x1a,.scalekit.v1.workspaces.GetWorkspaceResponse\"%\x82\xb5\x18\x02\x18@\x82\xd3\xe4\x93\x02\x19\x12\x17/api/v1/workspaces/{id}\x12\x9e\x01\n\x13GetCurrentWorkspace\x12\x32.scalekit.v1.workspaces.GetCurrentWorkspaceRequest\x1a,.scalekit.v1.workspaces.GetWorkspaceResponse\"%\x82\xb5\x18\x02\x18P\x82\xd3\xe4\x93\x02\x19\x12\x17/api/v1/workspaces:this\x12\xa4\x01\n\x0fUpdateWorkspace\x12..scalekit.v1.workspaces.UpdateWorkspaceRequest\x1a/.scalekit.v1.workspaces.UpdateWorkspaceResponse\"0\x82\xb5\x18\x02\x18@\x82\xd3\xe4\x93\x02$2\x17/api/v1/workspaces/{id}:\tworkspace\x12\xb2\x01\n\x16UpdateCurrentWorkspace\x12\x35.scalekit.v1.workspaces.UpdateCurrentWorkspaceRequest\x1a/.scalekit.v1.workspaces.UpdateWorkspaceResponse\"0\x82\xb5\x18\x02\x18P\x82\xd3\xe4\x93\x02$2\x17/api/v1/workspaces:this:\tworkspaceB6Z4github.com/scalekit-inc/scalekit/pkg/grpc/workspacesb\x06proto3')

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
  _globals['_CREATEWORKSPACE'].fields_by_name['email']._serialized_options = b'\272H\007r\005\020\001\030\200\002'
  _globals['_CREATEWORKSPACE'].fields_by_name['company']._loaded_options = None
  _globals['_CREATEWORKSPACE'].fields_by_name['company']._serialized_options = b'\272H\007r\005\020\001\030\200\002'
  _globals['_UPDATEWORKSPACE'].fields_by_name['display_name']._loaded_options = None
  _globals['_UPDATEWORKSPACE'].fields_by_name['display_name']._serialized_options = b'\272H\007r\005\020\001\030\200\002'
  _globals['_CREATEWORKSPACEREQUEST'].fields_by_name['workspace']._loaded_options = None
  _globals['_CREATEWORKSPACEREQUEST'].fields_by_name['workspace']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['workspace']._loaded_options = None
  _globals['_UPDATEWORKSPACEREQUEST'].fields_by_name['workspace']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPDATECURRENTWORKSPACEREQUEST'].fields_by_name['workspace']._loaded_options = None
  _globals['_UPDATECURRENTWORKSPACEREQUEST'].fields_by_name['workspace']._serialized_options = b'\272H\003\310\001\001'
  _globals['_GETWORKSPACEREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_GETWORKSPACEREQUEST'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003wks'
  _globals['_WORKSPACESERVICE'].methods_by_name['CreateWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['CreateWorkspace']._serialized_options = b'\202\265\030\002\030\001\202\323\344\223\002\033\"\016/api/v1/signup:\tworkspace'
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['GetWorkspace']._serialized_options = b'\202\265\030\002\030@\202\323\344\223\002\031\022\027/api/v1/workspaces/{id}'
  _globals['_WORKSPACESERVICE'].methods_by_name['GetCurrentWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['GetCurrentWorkspace']._serialized_options = b'\202\265\030\002\030P\202\323\344\223\002\031\022\027/api/v1/workspaces:this'
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateWorkspace']._serialized_options = b'\202\265\030\002\030@\202\323\344\223\002$2\027/api/v1/workspaces/{id}:\tworkspace'
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateCurrentWorkspace']._loaded_options = None
  _globals['_WORKSPACESERVICE'].methods_by_name['UpdateCurrentWorkspace']._serialized_options = b'\202\265\030\002\030P\202\323\344\223\002$2\027/api/v1/workspaces:this:\tworkspace'
  _globals['_YESNO']._serialized_start=1644
  _globals['_YESNO']._serialized_end=1668
  _globals['_WORKSPACE']._serialized_start=351
  _globals['_WORKSPACE']._serialized_end=629
  _globals['_CREATEWORKSPACE']._serialized_start=632
  _globals['_CREATEWORKSPACE']._serialized_end=843
  _globals['_UPDATEWORKSPACE']._serialized_start=845
  _globals['_UPDATEWORKSPACE']._serialized_end=909
  _globals['_CREATEWORKSPACEREQUEST']._serialized_start=911
  _globals['_CREATEWORKSPACEREQUEST']._serialized_end=1014
  _globals['_CREATEWORKSPACERESPONSE']._serialized_start=1016
  _globals['_CREATEWORKSPACERESPONSE']._serialized_end=1126
  _globals['_UPDATEWORKSPACEREQUEST']._serialized_start=1129
  _globals['_UPDATEWORKSPACEREQUEST']._serialized_end=1264
  _globals['_UPDATECURRENTWORKSPACEREQUEST']._serialized_start=1266
  _globals['_UPDATECURRENTWORKSPACEREQUEST']._serialized_end=1376
  _globals['_UPDATEWORKSPACERESPONSE']._serialized_start=1378
  _globals['_UPDATEWORKSPACERESPONSE']._serialized_end=1468
  _globals['_GETWORKSPACEREQUEST']._serialized_start=1470
  _globals['_GETWORKSPACEREQUEST']._serialized_end=1523
  _globals['_GETCURRENTWORKSPACEREQUEST']._serialized_start=1525
  _globals['_GETCURRENTWORKSPACEREQUEST']._serialized_end=1553
  _globals['_GETWORKSPACERESPONSE']._serialized_start=1555
  _globals['_GETWORKSPACERESPONSE']._serialized_end=1642
  _globals['_WORKSPACESERVICE']._serialized_start=1671
  _globals['_WORKSPACESERVICE']._serialized_end=2503
# @@protoc_insertion_point(module_scope)

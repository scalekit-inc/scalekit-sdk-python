# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/options/options.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!scalekit/v1/options/options.proto\x12\x13scalekit.v1.options\x1a google/protobuf/descriptor.proto\"\x86\x01\n\nAuthOption\x12X\n\x13\x61uthentication_type\x18\x03 \x01(\x0e\x32\'.scalekit.v1.options.AuthenticationTypeR\x12\x61uthenticationType\x12\x1e\n\npermission\x18\x01 \x01(\tR\npermission*\xdf\x01\n\x12\x41uthenticationType\x12\x0b\n\x07\x42LOCKED\x10\x00\x12\x08\n\x04NONE\x10\x01\x12\r\n\tWORKSPACE\x10@\x12\x13\n\x0f\x43USTOMER_PORTAL\x10 \x12\x0b\n\x07SESSION\x10\x10\x12\x15\n\x11WORKSPACE_SESSION\x10P\x12\x08\n\x04USER\x10\x08\x12\n\n\x06\x43LIENT\x10\x04\x12\x12\n\x0eSESSION_CLIENT\x10\x14\x12\x1c\n\x18WORKSPACE_SESSION_CLIENT\x10T\x12\"\n\x1e\x43USTOMER_PORTAL_SESSION_CLIENT\x10\x34:b\n\x0b\x61uth_option\x12\x1e.google.protobuf.MethodOptions\x18\xd0\x86\x03 \x01(\x0b\x32\x1f.scalekit.v1.options.AuthOptionR\nauthOptionB6Z4github.com/scalekit-inc/scalekit/pkg/grpc/authoptionb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.options.options_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z4github.com/scalekit-inc/scalekit/pkg/grpc/authoption'
  _globals['_AUTHENTICATIONTYPE']._serialized_start=230
  _globals['_AUTHENTICATIONTYPE']._serialized_end=453
  _globals['_AUTHOPTION']._serialized_start=93
  _globals['_AUTHOPTION']._serialized_end=227
# @@protoc_insertion_point(module_scope)

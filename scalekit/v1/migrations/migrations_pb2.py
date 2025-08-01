# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/migrations/migrations.proto
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
from google.api import visibility_pb2 as google_dot_api_dot_visibility__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
from scalekit.v1.commons import commons_pb2 as scalekit_dot_v1_dot_commons_dot_commons__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'scalekit/v1/migrations/migrations.proto\x12\x16scalekit.v1.migrations\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/api/visibility.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a.protoc-gen-openapiv2/options/annotations.proto\x1a!scalekit/v1/commons/commons.proto\x1a!scalekit/v1/options/options.proto\"~\n\x18MigrationServiceResponse\x12\x31\n\x14success_environments\x18\x01 \x01(\x05R\x13successEnvironments\x12/\n\x13\x66\x61iled_environments\x18\x02 \x01(\x05R\x12\x66\x61iledEnvironments\"f\n\x14MigrationSAMLRequest\x12\'\n\x0f\x65nvironment_ids\x18\x01 \x03(\x03R\x0e\x65nvironmentIds\x12%\n\nbatch_size\x18\x02 \x01(\x05\x42\x06\xbaH\x03\xc8\x01\x01R\tbatchSize\"\xad\x01\n\x11MigrateFSARequest\x12\'\n\x0f\x65nvironment_ids\x18\x01 \x03(\x03R\x0e\x65nvironmentIds\x12H\n\tdata_type\x18\x02 \x01(\x0e\x32#.scalekit.v1.migrations.FSADataTypeB\x06\xbaH\x03\xc8\x01\x01R\x08\x64\x61taType\x12%\n\nbatch_size\x18\x03 \x01(\x05\x42\x06\xbaH\x03\xc8\x01\x01R\tbatchSize\"z\n\x14MigrationFSAResponse\x12\x31\n\x14success_environments\x18\x01 \x01(\x05R\x13successEnvironments\x12/\n\x13\x66\x61iled_environments\x18\x02 \x01(\x05R\x12\x66\x61iledEnvironments\"{\n\x15MigrationSAMLResponse\x12\x31\n\x14success_environments\x18\x01 \x01(\x05R\x13successEnvironments\x12/\n\x13\x66\x61iled_environments\x18\x02 \x01(\x05R\x12\x66\x61iledEnvironments*\x88\x01\n\x0b\x46SADataType\x12\x1d\n\x19\x46SA_DATA_TYPE_UNSPECIFIED\x10\x00\x12\x1c\n\x18\x46SA_DATA_TYPE_CONNECTION\x10\x01\x12\x19\n\x15\x46SA_DATA_TYPE_SESSION\x10\x02\x12!\n\x1d\x46SA_DATA_TYPE_USER_MANAGEMENT\x10\x03\x32\xb1\x01\n\x10MigrationService\x12\x9c\x01\n\x0eMigrateFSAData\x12).scalekit.v1.migrations.MigrateFSARequest\x1a,.scalekit.v1.migrations.MigrationFSAResponse\"1\x82\xb5\x18\x02\x18\x01\xfa\xd2\xe4\x93\x02\t\x12\x07PREVIEW\x82\xd3\xe4\x93\x02\x16\"\x14/migrations/fsa-dataB6Z4github.com/scalekit-inc/scalekit/pkg/grpc/migrationsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.migrations.migrations_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z4github.com/scalekit-inc/scalekit/pkg/grpc/migrations'
  _globals['_MIGRATIONSAMLREQUEST'].fields_by_name['batch_size']._loaded_options = None
  _globals['_MIGRATIONSAMLREQUEST'].fields_by_name['batch_size']._serialized_options = b'\272H\003\310\001\001'
  _globals['_MIGRATEFSAREQUEST'].fields_by_name['data_type']._loaded_options = None
  _globals['_MIGRATEFSAREQUEST'].fields_by_name['data_type']._serialized_options = b'\272H\003\310\001\001'
  _globals['_MIGRATEFSAREQUEST'].fields_by_name['batch_size']._loaded_options = None
  _globals['_MIGRATEFSAREQUEST'].fields_by_name['batch_size']._serialized_options = b'\272H\003\310\001\001'
  _globals['_MIGRATIONSERVICE'].methods_by_name['MigrateFSAData']._loaded_options = None
  _globals['_MIGRATIONSERVICE'].methods_by_name['MigrateFSAData']._serialized_options = b'\202\265\030\002\030\001\372\322\344\223\002\t\022\007PREVIEW\202\323\344\223\002\026\"\024/migrations/fsa-data'
  _globals['_FSADATATYPE']._serialized_start=960
  _globals['_FSADATATYPE']._serialized_end=1096
  _globals['_MIGRATIONSERVICERESPONSE']._serialized_start=302
  _globals['_MIGRATIONSERVICERESPONSE']._serialized_end=428
  _globals['_MIGRATIONSAMLREQUEST']._serialized_start=430
  _globals['_MIGRATIONSAMLREQUEST']._serialized_end=532
  _globals['_MIGRATEFSAREQUEST']._serialized_start=535
  _globals['_MIGRATEFSAREQUEST']._serialized_end=708
  _globals['_MIGRATIONFSARESPONSE']._serialized_start=710
  _globals['_MIGRATIONFSARESPONSE']._serialized_end=832
  _globals['_MIGRATIONSAMLRESPONSE']._serialized_start=834
  _globals['_MIGRATIONSAMLRESPONSE']._serialized_end=957
  _globals['_MIGRATIONSERVICE']._serialized_start=1099
  _globals['_MIGRATIONSERVICE']._serialized_end=1276
# @@protoc_insertion_point(module_scope)

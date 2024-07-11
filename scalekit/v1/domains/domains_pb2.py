# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/domains/domains.proto
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
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!scalekit/v1/domains/domains.proto\x12\x13scalekit.v1.domains\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a!scalekit/v1/options/options.proto\"\xfe\x01\n\x13\x43reateDomainRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12(\n\rconnection_id\x18\x03 \x01(\tH\x01R\x0c\x63onnectionId\x88\x01\x01\x12\x39\n\x06\x64omain\x18\x04 \x01(\x0b\x32!.scalekit.v1.domains.CreateDomainR\x06\x64omainB\x0c\n\nidentitiesB\x10\n\x0e_connection_id\"K\n\x14\x43reateDomainResponse\x12\x33\n\x06\x64omain\x18\x01 \x01(\x0b\x32\x1b.scalekit.v1.domains.DomainR\x06\x64omain\"5\n\x0c\x43reateDomain\x12%\n\x06\x64omain\x18\x01 \x01(\tB\r\xbaH\nr\x05\x10\x04\x18\xff\x01\xc8\x01\x01R\x06\x64omain\"\x8e\x02\n\x13UpdateDomainRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12(\n\rconnection_id\x18\x03 \x01(\tH\x01R\x0c\x63onnectionId\x88\x01\x01\x12\x0e\n\x02id\x18\x04 \x01(\tR\x02id\x12\x39\n\x06\x64omain\x18\x05 \x01(\x0b\x32!.scalekit.v1.domains.UpdateDomainR\x06\x64omainB\x0c\n\nidentitiesB\x10\n\x0e_connection_id\"\x0e\n\x0cUpdateDomain\"K\n\x14UpdateDomainResponse\x12\x33\n\x06\x64omain\x18\x01 \x01(\x0b\x32\x1b.scalekit.v1.domains.DomainR\x06\x64omain\"\x94\x01\n\x10GetDomainRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12\x0e\n\x02id\x18\x03 \x01(\tR\x02idB\x0c\n\nidentities\"H\n\x11GetDomainResponse\x12\x33\n\x06\x64omain\x18\x01 \x01(\x0b\x32\x1b.scalekit.v1.domains.DomainR\x06\x64omain\"\xd3\x01\n\x13\x44\x65leteDomainRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x34\n\x0forganization_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x03 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12(\n\rconnection_id\x18\x04 \x01(\tH\x01R\x0c\x63onnectionId\x88\x01\x01\x42\x0c\n\nidentitiesB\x10\n\x0e_connection_id\"\xe4\x02\n\x11ListDomainRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12(\n\rconnection_id\x18\x03 \x01(\tH\x01R\x0c\x63onnectionId\x88\x01\x01\x12\x1d\n\x07include\x18\x04 \x01(\tH\x02R\x07include\x88\x01\x01\x12\x38\n\tpage_size\x18\x05 \x01(\x0b\x32\x1b.google.protobuf.Int32ValueR\x08pageSize\x12<\n\x0bpage_number\x18\x06 \x01(\x0b\x32\x1b.google.protobuf.Int32ValueR\npageNumberB\x0c\n\nidentitiesB\x10\n\x0e_connection_idB\n\n\x08_include\"\x89\x01\n\x12ListDomainResponse\x12\x1b\n\tpage_size\x18\x01 \x01(\x05R\x08pageSize\x12\x1f\n\x0bpage_number\x18\x02 \x01(\x05R\npageNumber\x12\x35\n\x07\x64omains\x18\x03 \x03(\x0b\x32\x1b.scalekit.v1.domains.DomainR\x07\x64omains\"5\n\x1bListAuthorizedDomainRequest\x12\x16\n\x06origin\x18\x01 \x01(\tR\x06origin\"8\n\x1cListAuthorizedDomainResponse\x12\x18\n\x07\x64omains\x18\x01 \x03(\tR\x07\x64omains\"\xfe\x03\n\x06\x44omain\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x16\n\x06\x64omain\x18\x02 \x01(\tR\x06\x64omain\x12%\n\x0e\x65nvironment_id\x18\x03 \x01(\tR\renvironmentId\x12\'\n\x0forganization_id\x18\x04 \x01(\tR\x0eorganizationId\x12#\n\rconnection_id\x18\x05 \x01(\tR\x0c\x63onnectionId\x12$\n\x0etxt_record_key\x18\x06 \x01(\tR\x0ctxtRecordKey\x12*\n\x11txt_record_secret\x18\x07 \x01(\tR\x0ftxtRecordSecret\x12X\n\x13verification_status\x18\x08 \x01(\x0e\x32\'.scalekit.v1.domains.VerificationStatusR\x12verificationStatus\x12;\n\x0b\x63reate_time\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12\"\n\ncreated_by\x18\x0b \x01(\tH\x00R\tcreatedBy\x88\x01\x01\x42\r\n\x0b_created_by*`\n\x12VerificationStatus\x12#\n\x1fVERIFICATION_STATUS_UNSPECIFIED\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\x0c\n\x08VERIFIED\x10\x02\x12\n\n\x06\x46\x41ILED\x10\x03\x32\xb6\t\n\rDomainService\x12\xd5\x01\n\x0c\x43reateDomain\x12(.scalekit.v1.domains.CreateDomainRequest\x1a).scalekit.v1.domains.CreateDomainResponse\"p\x82\xb5\x18\x02\x18\x14\x82\xd3\xe4\x93\x02\x64\"//api/v1/organizations/{organization_id}/domains:\x06\x64omainZ)\"\x1f/api/v1/organizations/-/domains:\x06\x64omain\x12\xda\x01\n\x0cUpdateDomain\x12(.scalekit.v1.domains.UpdateDomainRequest\x1a).scalekit.v1.domains.UpdateDomainResponse\"u\x82\xb5\x18\x02\x18\x14\x82\xd3\xe4\x93\x02i24/api/v1/organizations/{organization_id}/domains/{id}:\x06\x64omainZ)2\x1f/api/v1/organizations/-/domains:\x06\x64omain\x12\xc6\x01\n\tGetDomain\x12%.scalekit.v1.domains.GetDomainRequest\x1a&.scalekit.v1.domains.GetDomainResponse\"j\x82\xb5\x18\x02\x18\x14\x82\xd3\xe4\x93\x02^\x12\x34/api/v1/organizations/{organization_id}/domains/{id}Z&\x12$/api/v1/organizations/-/domains/{id}\x12\xbc\x01\n\x0c\x44\x65leteDomain\x12(.scalekit.v1.domains.DeleteDomainRequest\x1a\x16.google.protobuf.Empty\"j\x82\xb5\x18\x02\x18\x14\x82\xd3\xe4\x93\x02^*4/api/v1/organizations/{organization_id}/domains/{id}Z&*$/api/v1/organizations/-/domains/{id}\x12\xc0\x01\n\x0bListDomains\x12&.scalekit.v1.domains.ListDomainRequest\x1a\'.scalekit.v1.domains.ListDomainResponse\"`\x82\xb5\x18\x02\x18\x14\x82\xd3\xe4\x93\x02T\x12//api/v1/organizations/{organization_id}/domainsZ!\x12\x1f/api/v1/organizations/-/domains\x12\xa4\x01\n\x15ListAuthorizedDomains\x12\x30.scalekit.v1.domains.ListAuthorizedDomainRequest\x1a\x31.scalekit.v1.domains.ListAuthorizedDomainResponse\"&\x82\xb5\x18\x02\x18\x01\x82\xd3\xe4\x93\x02\x1a\x12\x18/api/v1/domains/{origin}B3Z1github.com/scalekit-inc/scalekit/pkg/grpc/domainsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.domains.domains_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z1github.com/scalekit-inc/scalekit/pkg/grpc/domains'
  _globals['_CREATEDOMAINREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_CREATEDOMAINREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_CREATEDOMAINREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_CREATEDOMAINREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_CREATEDOMAIN'].fields_by_name['domain']._loaded_options = None
  _globals['_CREATEDOMAIN'].fields_by_name['domain']._serialized_options = b'\272H\nr\005\020\004\030\377\001\310\001\001'
  _globals['_UPDATEDOMAINREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_UPDATEDOMAINREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATEDOMAINREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_UPDATEDOMAINREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_GETDOMAINREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_GETDOMAINREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_GETDOMAINREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_GETDOMAINREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DELETEDOMAINREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_DELETEDOMAINREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DELETEDOMAINREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_DELETEDOMAINREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_LISTDOMAINREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_LISTDOMAINREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_LISTDOMAINREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_LISTDOMAINREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DOMAINSERVICE'].methods_by_name['CreateDomain']._loaded_options = None
  _globals['_DOMAINSERVICE'].methods_by_name['CreateDomain']._serialized_options = b'\202\265\030\002\030\024\202\323\344\223\002d\"//api/v1/organizations/{organization_id}/domains:\006domainZ)\"\037/api/v1/organizations/-/domains:\006domain'
  _globals['_DOMAINSERVICE'].methods_by_name['UpdateDomain']._loaded_options = None
  _globals['_DOMAINSERVICE'].methods_by_name['UpdateDomain']._serialized_options = b'\202\265\030\002\030\024\202\323\344\223\002i24/api/v1/organizations/{organization_id}/domains/{id}:\006domainZ)2\037/api/v1/organizations/-/domains:\006domain'
  _globals['_DOMAINSERVICE'].methods_by_name['GetDomain']._loaded_options = None
  _globals['_DOMAINSERVICE'].methods_by_name['GetDomain']._serialized_options = b'\202\265\030\002\030\024\202\323\344\223\002^\0224/api/v1/organizations/{organization_id}/domains/{id}Z&\022$/api/v1/organizations/-/domains/{id}'
  _globals['_DOMAINSERVICE'].methods_by_name['DeleteDomain']._loaded_options = None
  _globals['_DOMAINSERVICE'].methods_by_name['DeleteDomain']._serialized_options = b'\202\265\030\002\030\024\202\323\344\223\002^*4/api/v1/organizations/{organization_id}/domains/{id}Z&*$/api/v1/organizations/-/domains/{id}'
  _globals['_DOMAINSERVICE'].methods_by_name['ListDomains']._loaded_options = None
  _globals['_DOMAINSERVICE'].methods_by_name['ListDomains']._serialized_options = b'\202\265\030\002\030\024\202\323\344\223\002T\022//api/v1/organizations/{organization_id}/domainsZ!\022\037/api/v1/organizations/-/domains'
  _globals['_DOMAINSERVICE'].methods_by_name['ListAuthorizedDomains']._loaded_options = None
  _globals['_DOMAINSERVICE'].methods_by_name['ListAuthorizedDomains']._serialized_options = b'\202\265\030\002\030\001\202\323\344\223\002\032\022\030/api/v1/domains/{origin}'
  _globals['_VERIFICATIONSTATUS']._serialized_start=2598
  _globals['_VERIFICATIONSTATUS']._serialized_end=2694
  _globals['_CREATEDOMAINREQUEST']._serialized_start=280
  _globals['_CREATEDOMAINREQUEST']._serialized_end=534
  _globals['_CREATEDOMAINRESPONSE']._serialized_start=536
  _globals['_CREATEDOMAINRESPONSE']._serialized_end=611
  _globals['_CREATEDOMAIN']._serialized_start=613
  _globals['_CREATEDOMAIN']._serialized_end=666
  _globals['_UPDATEDOMAINREQUEST']._serialized_start=669
  _globals['_UPDATEDOMAINREQUEST']._serialized_end=939
  _globals['_UPDATEDOMAIN']._serialized_start=941
  _globals['_UPDATEDOMAIN']._serialized_end=955
  _globals['_UPDATEDOMAINRESPONSE']._serialized_start=957
  _globals['_UPDATEDOMAINRESPONSE']._serialized_end=1032
  _globals['_GETDOMAINREQUEST']._serialized_start=1035
  _globals['_GETDOMAINREQUEST']._serialized_end=1183
  _globals['_GETDOMAINRESPONSE']._serialized_start=1185
  _globals['_GETDOMAINRESPONSE']._serialized_end=1257
  _globals['_DELETEDOMAINREQUEST']._serialized_start=1260
  _globals['_DELETEDOMAINREQUEST']._serialized_end=1471
  _globals['_LISTDOMAINREQUEST']._serialized_start=1474
  _globals['_LISTDOMAINREQUEST']._serialized_end=1830
  _globals['_LISTDOMAINRESPONSE']._serialized_start=1833
  _globals['_LISTDOMAINRESPONSE']._serialized_end=1970
  _globals['_LISTAUTHORIZEDDOMAINREQUEST']._serialized_start=1972
  _globals['_LISTAUTHORIZEDDOMAINREQUEST']._serialized_end=2025
  _globals['_LISTAUTHORIZEDDOMAINRESPONSE']._serialized_start=2027
  _globals['_LISTAUTHORIZEDDOMAINRESPONSE']._serialized_end=2083
  _globals['_DOMAIN']._serialized_start=2086
  _globals['_DOMAIN']._serialized_end=2596
  _globals['_DOMAINSERVICE']._serialized_start=2697
  _globals['_DOMAINSERVICE']._serialized_end=3903
# @@protoc_insertion_point(module_scope)

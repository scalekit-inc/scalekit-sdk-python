# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/clients/clients.proto
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
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from scalekit.v1.commons import commons_pb2 as scalekit_dot_v1_dot_commons_dot_commons__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!scalekit/v1/clients/clients.proto\x12\x13scalekit.v1.clients\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a!scalekit/v1/commons/commons.proto\x1a!scalekit/v1/options/options.proto\":\n\x10GetClientRequest\x12&\n\tclient_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x08\x63lientId\"H\n\x11GetClientResponse\x12\x33\n\x06\x63lient\x18\x01 \x01(\x0b\x32\x1b.scalekit.v1.clients.ClientR\x06\x63lient\"\x14\n\x12ListClientsRequest\"k\n\x13ListClientsResponse\x12\x1d\n\ntotal_size\x18\x01 \x01(\rR\ttotalSize\x12\x35\n\x07\x63lients\x18\x02 \x03(\x0b\x32\x1b.scalekit.v1.clients.ClientR\x07\x63lients\"\xb0\x01\n\x13UpdateClientRequest\x12&\n\tclient_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x08\x63lientId\x12\x41\n\x06\x63lient\x18\x02 \x01(\x0b\x32!.scalekit.v1.clients.UpdateClientB\x06\xbaH\x03\xc8\x01\x01R\x06\x63lient\x12.\n\x04mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\x04mask\"\xce\x01\n\x0cUpdateClient\x12\x34\n\rredirect_uris\x18\x02 \x03(\tB\x0f\xbaH\x0c\x92\x01\t\x18\x01\"\x05r\x03\x88\x01\x01R\x0credirectUris\x12o\n\x14\x64\x65\x66\x61ult_redirect_uri\x18\x03 \x01(\tB8\xbaH5\xba\x01\x32\n\tvalid_uri\x12\x17uri must be a valid URI\x1a\x0cthis.isUri()H\x00R\x12\x64\x65\x66\x61ultRedirectUri\x88\x01\x01\x42\x17\n\x15_default_redirect_uri\"K\n\x14UpdateClientResponse\x12\x33\n\x06\x63lient\x18\x01 \x01(\x0b\x32\x1b.scalekit.v1.clients.ClientR\x06\x63lient\"C\n\x19\x43reateClientSecretRequest\x12&\n\tclient_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x08\x63lientId\"z\n\x1a\x43reateClientSecretResponse\x12!\n\x0cplain_secret\x18\x01 \x01(\tR\x0bplainSecret\x12\x39\n\x06secret\x18\x02 \x01(\x0b\x32!.scalekit.v1.clients.ClientSecretR\x06secret\"\xe4\x01\n\x19UpdateClientSecretRequest\x12&\n\tclient_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x08\x63lientId\x12&\n\tsecret_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x08secretId\x12G\n\x06secret\x18\x03 \x01(\x0b\x32\'.scalekit.v1.clients.UpdateClientSecretB\x06\xbaH\x03\xc8\x01\x01R\x06secret\x12.\n\x04mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\x04mask\"U\n\x12UpdateClientSecret\x12?\n\x06status\x18\x01 \x01(\x0e\x32\'.scalekit.v1.clients.ClientSecretStatusR\x06status\"W\n\x1aUpdateClientSecretResponse\x12\x39\n\x06secret\x18\x01 \x01(\x0b\x32!.scalekit.v1.clients.ClientSecretR\x06secret\"k\n\x19\x44\x65leteClientSecretRequest\x12&\n\tclient_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x08\x63lientId\x12&\n\tsecret_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x08secretId\"\xbc\x02\n\x06\x43lient\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x14\n\x05keyId\x18\x02 \x01(\tR\x05keyId\x12;\n\x0b\x63reate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12#\n\rredirect_uris\x18\x05 \x03(\tR\x0credirectUris\x12\x30\n\x14\x64\x65\x66\x61ult_redirect_uri\x18\x06 \x01(\tR\x12\x64\x65\x66\x61ultRedirectUri\x12;\n\x07secrets\x18\x07 \x03(\x0b\x32!.scalekit.v1.clients.ClientSecretR\x07secrets\"\xb0\x03\n\x0c\x43lientSecret\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12;\n\x0b\x63reate_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12#\n\rsecret_suffix\x18\x04 \x01(\tR\x0csecretSuffix\x12\"\n\ncreated_by\x18\x05 \x01(\tH\x00R\tcreatedBy\x88\x01\x01\x12?\n\x06status\x18\x06 \x01(\x0e\x32\'.scalekit.v1.clients.ClientSecretStatusR\x06status\x12;\n\x0b\x65xpire_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nexpireTime\x12@\n\x0elast_used_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0clastUsedTimeB\r\n\x0b_created_by*.\n\x12\x43lientSecretStatus\x12\n\n\x06\x41\x43TIVE\x10\x00\x12\x0c\n\x08INACTIVE\x10\x01\x32\x94\x08\n\rClientService\x12~\n\nListClient\x12\'.scalekit.v1.clients.ListClientsRequest\x1a(.scalekit.v1.clients.ListClientsResponse\"\x1d\x82\xb5\x18\x02\x18\x10\x82\xd3\xe4\x93\x02\x11\x12\x0f/api/v1/clients\x12\x7f\n\tGetClient\x12%.scalekit.v1.clients.GetClientRequest\x1a&.scalekit.v1.clients.GetClientResponse\"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/api/v1/clients/{client_id}\x12\xbd\x01\n\x0cUpdateClient\x12(.scalekit.v1.clients.UpdateClientRequest\x1a).scalekit.v1.clients.UpdateClientResponse\"X\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02L\x1a\x1b/api/v1/clients/{client_id}:\x06\x63lientZ%2\x1b/api/v1/clients/{client_id}:\x06\x63lient\x12\xa8\x01\n\x12\x43reateClientSecret\x12..scalekit.v1.clients.CreateClientSecretRequest\x1a/.scalekit.v1.clients.CreateClientSecretResponse\"1\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02%\"#/api/v1/clients/{client_id}/secrets\x12\xf8\x01\n\x12UpdateClientSecret\x12..scalekit.v1.clients.UpdateClientSecretRequest\x1a/.scalekit.v1.clients.UpdateClientSecretResponse\"\x80\x01\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02t\x1a//api/v1/clients/{client_id}/secrets/{secret_id}:\x06secretZ92//api/v1/clients/{client_id}/secrets/{secret_id}:\x06secret\x12\x9b\x01\n\x12\x44\x65leteClientSecret\x12..scalekit.v1.clients.DeleteClientSecretRequest\x1a\x16.google.protobuf.Empty\"=\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x31*//api/v1/clients/{client_id}/secrets/{secret_id}B3Z1github.com/scalekit-inc/scalekit/pkg/grpc/clientsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.clients.clients_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z1github.com/scalekit-inc/scalekit/pkg/grpc/clients'
  _globals['_GETCLIENTREQUEST'].fields_by_name['client_id']._loaded_options = None
  _globals['_GETCLIENTREQUEST'].fields_by_name['client_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECLIENTREQUEST'].fields_by_name['client_id']._loaded_options = None
  _globals['_UPDATECLIENTREQUEST'].fields_by_name['client_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECLIENTREQUEST'].fields_by_name['client']._loaded_options = None
  _globals['_UPDATECLIENTREQUEST'].fields_by_name['client']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPDATECLIENT'].fields_by_name['redirect_uris']._loaded_options = None
  _globals['_UPDATECLIENT'].fields_by_name['redirect_uris']._serialized_options = b'\272H\014\222\001\t\030\001\"\005r\003\210\001\001'
  _globals['_UPDATECLIENT'].fields_by_name['default_redirect_uri']._loaded_options = None
  _globals['_UPDATECLIENT'].fields_by_name['default_redirect_uri']._serialized_options = b'\272H5\272\0012\n\tvalid_uri\022\027uri must be a valid URI\032\014this.isUri()'
  _globals['_CREATECLIENTSECRETREQUEST'].fields_by_name['client_id']._loaded_options = None
  _globals['_CREATECLIENTSECRETREQUEST'].fields_by_name['client_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECLIENTSECRETREQUEST'].fields_by_name['client_id']._loaded_options = None
  _globals['_UPDATECLIENTSECRETREQUEST'].fields_by_name['client_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECLIENTSECRETREQUEST'].fields_by_name['secret_id']._loaded_options = None
  _globals['_UPDATECLIENTSECRETREQUEST'].fields_by_name['secret_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECLIENTSECRETREQUEST'].fields_by_name['secret']._loaded_options = None
  _globals['_UPDATECLIENTSECRETREQUEST'].fields_by_name['secret']._serialized_options = b'\272H\003\310\001\001'
  _globals['_DELETECLIENTSECRETREQUEST'].fields_by_name['client_id']._loaded_options = None
  _globals['_DELETECLIENTSECRETREQUEST'].fields_by_name['client_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DELETECLIENTSECRETREQUEST'].fields_by_name['secret_id']._loaded_options = None
  _globals['_DELETECLIENTSECRETREQUEST'].fields_by_name['secret_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_CLIENTSERVICE'].methods_by_name['ListClient']._loaded_options = None
  _globals['_CLIENTSERVICE'].methods_by_name['ListClient']._serialized_options = b'\202\265\030\002\030\020\202\323\344\223\002\021\022\017/api/v1/clients'
  _globals['_CLIENTSERVICE'].methods_by_name['GetClient']._loaded_options = None
  _globals['_CLIENTSERVICE'].methods_by_name['GetClient']._serialized_options = b'\202\323\344\223\002\035\022\033/api/v1/clients/{client_id}'
  _globals['_CLIENTSERVICE'].methods_by_name['UpdateClient']._loaded_options = None
  _globals['_CLIENTSERVICE'].methods_by_name['UpdateClient']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002L\032\033/api/v1/clients/{client_id}:\006clientZ%2\033/api/v1/clients/{client_id}:\006client'
  _globals['_CLIENTSERVICE'].methods_by_name['CreateClientSecret']._loaded_options = None
  _globals['_CLIENTSERVICE'].methods_by_name['CreateClientSecret']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002%\"#/api/v1/clients/{client_id}/secrets'
  _globals['_CLIENTSERVICE'].methods_by_name['UpdateClientSecret']._loaded_options = None
  _globals['_CLIENTSERVICE'].methods_by_name['UpdateClientSecret']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002t\032//api/v1/clients/{client_id}/secrets/{secret_id}:\006secretZ92//api/v1/clients/{client_id}/secrets/{secret_id}:\006secret'
  _globals['_CLIENTSERVICE'].methods_by_name['DeleteClientSecret']._loaded_options = None
  _globals['_CLIENTSERVICE'].methods_by_name['DeleteClientSecret']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\0021*//api/v1/clients/{client_id}/secrets/{secret_id}'
  _globals['_CLIENTSECRETSTATUS']._serialized_start=2568
  _globals['_CLIENTSECRETSTATUS']._serialized_end=2614
  _globals['_GETCLIENTREQUEST']._serialized_start=375
  _globals['_GETCLIENTREQUEST']._serialized_end=433
  _globals['_GETCLIENTRESPONSE']._serialized_start=435
  _globals['_GETCLIENTRESPONSE']._serialized_end=507
  _globals['_LISTCLIENTSREQUEST']._serialized_start=509
  _globals['_LISTCLIENTSREQUEST']._serialized_end=529
  _globals['_LISTCLIENTSRESPONSE']._serialized_start=531
  _globals['_LISTCLIENTSRESPONSE']._serialized_end=638
  _globals['_UPDATECLIENTREQUEST']._serialized_start=641
  _globals['_UPDATECLIENTREQUEST']._serialized_end=817
  _globals['_UPDATECLIENT']._serialized_start=820
  _globals['_UPDATECLIENT']._serialized_end=1026
  _globals['_UPDATECLIENTRESPONSE']._serialized_start=1028
  _globals['_UPDATECLIENTRESPONSE']._serialized_end=1103
  _globals['_CREATECLIENTSECRETREQUEST']._serialized_start=1105
  _globals['_CREATECLIENTSECRETREQUEST']._serialized_end=1172
  _globals['_CREATECLIENTSECRETRESPONSE']._serialized_start=1174
  _globals['_CREATECLIENTSECRETRESPONSE']._serialized_end=1296
  _globals['_UPDATECLIENTSECRETREQUEST']._serialized_start=1299
  _globals['_UPDATECLIENTSECRETREQUEST']._serialized_end=1527
  _globals['_UPDATECLIENTSECRET']._serialized_start=1529
  _globals['_UPDATECLIENTSECRET']._serialized_end=1614
  _globals['_UPDATECLIENTSECRETRESPONSE']._serialized_start=1616
  _globals['_UPDATECLIENTSECRETRESPONSE']._serialized_end=1703
  _globals['_DELETECLIENTSECRETREQUEST']._serialized_start=1705
  _globals['_DELETECLIENTSECRETREQUEST']._serialized_end=1812
  _globals['_CLIENT']._serialized_start=1815
  _globals['_CLIENT']._serialized_end=2131
  _globals['_CLIENTSECRET']._serialized_start=2134
  _globals['_CLIENTSECRET']._serialized_end=2566
  _globals['_CLIENTSERVICE']._serialized_start=2617
  _globals['_CLIENTSERVICE']._serialized_end=3661
# @@protoc_insertion_point(module_scope)

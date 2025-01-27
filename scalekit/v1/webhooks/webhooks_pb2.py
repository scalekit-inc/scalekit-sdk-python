# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/webhooks/webhooks.proto
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
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#scalekit/v1/webhooks/webhooks.proto\x12\x14scalekit.v1.webhooks\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/api/visibility.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a!scalekit/v1/options/options.proto\"A\n\x14SendTestEventRequest\x12)\n\nevent_type\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\xff\x01R\teventType\"t\n\x15SendTestEventResponse\x12\x1d\n\nevent_type\x18\x01 \x01(\tR\teventType\x12<\n\revent_payload\x18\x02 \x01(\x0b\x32\x17.google.protobuf.StructR\x0c\x65ventPayload\"\x15\n\x13GetPortalURLRequest\"(\n\x14GetPortalURLResponse\x12\x10\n\x03url\x18\x01 \x01(\tR\x03url\"S\n\x15WebhookWrapperRequest\x12:\n\x0crequest_body\x18\x01 \x01(\x0b\x32\x17.google.protobuf.StructR\x0brequestBody\"V\n\x16WebhookWrapperResponse\x12<\n\rresponse_body\x18\x01 \x01(\x0b\x32\x17.google.protobuf.StructR\x0cresponseBody2\xf7\x04\n\x0eWebhookService\x12\x90\x01\n\x0cGetPortalURL\x12).scalekit.v1.webhooks.GetPortalURLRequest\x1a*.scalekit.v1.webhooks.GetPortalURLResponse\")\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x1d\x12\x1b/api/v1/webhooks/portal-url\x12\x9f\x02\n\x0eWebhookWrapper\x12+.scalekit.v1.webhooks.WebhookWrapperRequest\x1a\x17.google.protobuf.Struct\"\xc6\x01\x82\xb5\x18\x02\x18P\xfa\xd2\xe4\x93\x02\t\x12\x07PREVIEW\x82\xd3\xe4\x93\x02\xaa\x01\x12\x16/api/v1/webhooks/wb/**Z&\"\x16/api/v1/webhooks/wb/**:\x0crequest_bodyZ&\x1a\x16/api/v1/webhooks/wb/**:\x0crequest_bodyZ&2\x16/api/v1/webhooks/wb/**:\x0crequest_bodyZ\x18*\x16/api/v1/webhooks/wb/**\x12\xaf\x01\n\rSendTestEvent\x12*.scalekit.v1.webhooks.SendTestEventRequest\x1a+.scalekit.v1.webhooks.SendTestEventResponse\"E\x82\xb5\x18\x02\x18T\xfa\xd2\xe4\x93\x02\t\x12\x07PREVIEW\x82\xd3\xe4\x93\x02*\"(/api/v1/webhooks/test-event/{event_type}B4Z2github.com/scalekit-inc/scalekit/pkg/grpc/webhooksb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.webhooks.webhooks_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z2github.com/scalekit-inc/scalekit/pkg/grpc/webhooks'
  _globals['_SENDTESTEVENTREQUEST'].fields_by_name['event_type']._loaded_options = None
  _globals['_SENDTESTEVENTREQUEST'].fields_by_name['event_type']._serialized_options = b'\272H\007r\005\020\001\030\377\001'
  _globals['_WEBHOOKSERVICE'].methods_by_name['GetPortalURL']._loaded_options = None
  _globals['_WEBHOOKSERVICE'].methods_by_name['GetPortalURL']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\035\022\033/api/v1/webhooks/portal-url'
  _globals['_WEBHOOKSERVICE'].methods_by_name['WebhookWrapper']._loaded_options = None
  _globals['_WEBHOOKSERVICE'].methods_by_name['WebhookWrapper']._serialized_options = b'\202\265\030\002\030P\372\322\344\223\002\t\022\007PREVIEW\202\323\344\223\002\252\001\022\026/api/v1/webhooks/wb/**Z&\"\026/api/v1/webhooks/wb/**:\014request_bodyZ&\032\026/api/v1/webhooks/wb/**:\014request_bodyZ&2\026/api/v1/webhooks/wb/**:\014request_bodyZ\030*\026/api/v1/webhooks/wb/**'
  _globals['_WEBHOOKSERVICE'].methods_by_name['SendTestEvent']._loaded_options = None
  _globals['_WEBHOOKSERVICE'].methods_by_name['SendTestEvent']._serialized_options = b'\202\265\030\002\030T\372\322\344\223\002\t\022\007PREVIEW\202\323\344\223\002*\"(/api/v1/webhooks/test-event/{event_type}'
  _globals['_SENDTESTEVENTREQUEST']._serialized_start=214
  _globals['_SENDTESTEVENTREQUEST']._serialized_end=279
  _globals['_SENDTESTEVENTRESPONSE']._serialized_start=281
  _globals['_SENDTESTEVENTRESPONSE']._serialized_end=397
  _globals['_GETPORTALURLREQUEST']._serialized_start=399
  _globals['_GETPORTALURLREQUEST']._serialized_end=420
  _globals['_GETPORTALURLRESPONSE']._serialized_start=422
  _globals['_GETPORTALURLRESPONSE']._serialized_end=462
  _globals['_WEBHOOKWRAPPERREQUEST']._serialized_start=464
  _globals['_WEBHOOKWRAPPERREQUEST']._serialized_end=547
  _globals['_WEBHOOKWRAPPERRESPONSE']._serialized_start=549
  _globals['_WEBHOOKWRAPPERRESPONSE']._serialized_end=635
  _globals['_WEBHOOKSERVICE']._serialized_start=638
  _globals['_WEBHOOKSERVICE']._serialized_end=1269
# @@protoc_insertion_point(module_scope)

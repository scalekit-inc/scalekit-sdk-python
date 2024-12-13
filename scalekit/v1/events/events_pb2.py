# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/events/events.proto
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
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
from scalekit.v1.commons import commons_pb2 as scalekit_dot_v1_dot_commons_dot_commons__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fscalekit/v1/events/events.proto\x12\x12scalekit.v1.events\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/protobuf/any.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a.protoc-gen-openapiv2/options/annotations.proto\x1a!scalekit/v1/commons/commons.proto\x1a!scalekit/v1/options/options.proto\"n\n\x16IEventPaginationTokens\x12\x1a\n\x08NextPage\x18\x01 \x01(\tR\x08NextPage\x12\"\n\x0cPreviousPage\x18\x02 \x01(\tR\x0cPreviousPage\x12\x14\n\x05Total\x18\x03 \x01(\rR\x05Total\"\x88\x01\n\x11ListEventsRequest\x12\x37\n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x1f.scalekit.v1.events.EventFilterR\x06\x66ilter\x12\x1b\n\tpage_size\x18\x02 \x01(\rR\x08pageSize\x12\x1d\n\npage_token\x18\x03 \x01(\tR\tpageToken\"\xbe\x01\n\x12ListEventsResponse\x12\x39\n\x06\x65vents\x18\x01 \x03(\x0b\x32!.scalekit.v1.events.ScalekitEventR\x06\x65vents\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageToken\x12&\n\x0fprev_page_token\x18\x03 \x01(\tR\rprevPageToken\x12\x1d\n\ntotal_size\x18\x04 \x01(\rR\ttotalSize\"\xc6\x05\n\x06IEvent\x12!\n\x0cspec_version\x18\x01 \x01(\tR\x0bspecVersion\x12\x19\n\x02id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x02id\x12\x12\n\x04type\x18\x03 \x01(\tR\x04type\x12;\n\x0boccurred_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\noccurredAt\x12/\n\x05\x61\x63tor\x18\x05 \x01(\x0b\x32\x19.scalekit.v1.events.ActorR\x05\x61\x63tor\x12\x1b\n\ttenant_id\x18\x06 \x01(\tR\x08tenantId\x12\x32\n\x06target\x18\x07 \x01(\x0b\x32\x1a.scalekit.v1.events.TargetR\x06target\x12\x16\n\x06source\x18\x08 \x01(\tR\x06source\x12+\n\x04\x64\x61ta\x18\t \x01(\x0b\x32\x17.google.protobuf.StructR\x04\x64\x61ta\x12\x32\n\x08old_data\x18\n \x01(\x0b\x32\x17.google.protobuf.StructR\x07oldData\x12Z\n\x07\x63ontext\x18\x0b \x03(\x0b\x32\'.scalekit.v1.events.IEvent.ContextEntryB\x17\xbaH\x14\x9a\x01\x11\"\x06r\x04\x10\x03\x18\x19*\x07r\x05\x10\x01\x18\xd0\x0fR\x07\x63ontext\x12]\n\x08metadata\x18\x0c \x03(\x0b\x32(.scalekit.v1.events.IEvent.MetadataEntryB\x17\xbaH\x14\x9a\x01\x11\"\x06r\x04\x10\x03\x18\x19*\x07r\x05\x10\x01\x18\xd0\x0fR\x08metadata\x1a:\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a;\n\rMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\xfb\x05\n\x05\x45vent\x12!\n\x0cspec_version\x18\x01 \x01(\tR\x0bspecVersion\x12\x19\n\x02id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x02id\x12\x12\n\x04type\x18\x03 \x01(\tR\x04type\x12;\n\x0boccurred_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\noccurredAt\x12/\n\x05\x61\x63tor\x18\x05 \x01(\x0b\x32\x19.scalekit.v1.events.ActorR\x05\x61\x63tor\x12\x1b\n\ttenant_id\x18\x06 \x01(\tR\x08tenantId\x12\x32\n\x06target\x18\x07 \x01(\x0b\x32\x1a.scalekit.v1.events.TargetR\x06target\x12\x16\n\x06source\x18\x08 \x01(\tR\x06source\x12+\n\x04\x64\x61ta\x18\t \x01(\x0b\x32\x17.google.protobuf.StructR\x04\x64\x61ta\x12\x32\n\x08old_data\x18\n \x01(\x0b\x32\x17.google.protobuf.StructR\x07oldData\x12Y\n\x07\x63ontext\x18\x0b \x03(\x0b\x32&.scalekit.v1.events.Event.ContextEntryB\x17\xbaH\x14\x9a\x01\x11\"\x06r\x04\x10\x03\x18\x19*\x07r\x05\x10\x01\x18\xd0\x0fR\x07\x63ontext\x12\\\n\x08metadata\x18\x0c \x03(\x0b\x32\'.scalekit.v1.events.Event.MetadataEntryB\x17\xbaH\x14\x9a\x01\x11\"\x06r\x04\x10\x03\x18\x19*\x07r\x05\x10\x01\x18\xd0\x0fR\x08metadata\x12\x36\n\x06object\x18\r \x01(\x0e\x32\x1e.scalekit.v1.events.ObjectTypeR\x06object\x1a:\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a;\n\rMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"K\n\x05\x41\x63tor\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x32\n\x04type\x18\x02 \x01(\x0e\x32\x1e.scalekit.v1.events.EventActorR\x04type\"M\n\x06Target\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x33\n\x04type\x18\x02 \x01(\x0e\x32\x1f.scalekit.v1.events.EventTargetR\x04type\"\xc8\x03\n\x0cIEventFilter\x12\x1f\n\x0b\x65vent_types\x18\x01 \x03(\tR\neventTypes\x12\x39\n\nstart_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\x12\x35\n\x08\x65nd_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07\x65ndTime\x12\x1b\n\ttenant_id\x18\x04 \x01(\tR\x08tenantId\x12\x32\n\x06target\x18\x05 \x01(\x0b\x32\x1a.scalekit.v1.events.TargetR\x06target\x12\x32\n\x06source\x18\x06 \x01(\x0e\x32\x1a.scalekit.v1.events.SourceR\x06source\x12\x63\n\x08metadata\x18\x07 \x03(\x0b\x32..scalekit.v1.events.IEventFilter.MetadataEntryB\x17\xbaH\x14\x9a\x01\x11\"\x06r\x04\x10\x03\x18\x19*\x07r\x05\x10\x01\x18\xd0\x0fR\x08metadata\x1a;\n\rMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\xfd\x01\n\x0b\x45ventFilter\x12\x1f\n\x0b\x65vent_types\x18\x01 \x03(\tR\neventTypes\x12\x39\n\nstart_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\x12\x35\n\x08\x65nd_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x07\x65ndTime\x12\'\n\x0forganization_id\x18\x04 \x01(\tR\x0eorganizationId\x12\x32\n\x06source\x18\x05 \x01(\x0e\x32\x1a.scalekit.v1.events.SourceR\x06source\"\xf7\x02\n\rScalekitEvent\x12!\n\x0cspec_version\x18\x01 \x01(\tR\x0bspecVersion\x12\x1e\n\x02id\x18\x02 \x01(\tB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03\x65vtR\x02id\x12\x12\n\x04type\x18\x03 \x01(\tR\x04type\x12;\n\x0boccurred_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\noccurredAt\x12%\n\x0e\x65nvironment_id\x18\x06 \x01(\tR\renvironmentId\x12,\n\x0forganization_id\x18\x07 \x01(\tH\x00R\x0eorganizationId\x88\x01\x01\x12\x36\n\x06object\x18\x08 \x01(\x0e\x32\x1e.scalekit.v1.events.ObjectTypeR\x06object\x12+\n\x04\x64\x61ta\x18\t \x01(\x0b\x32\x17.google.protobuf.StructR\x04\x64\x61taB\x12\n\x10_organization_idJ\x04\x08\x05\x10\x06*D\n\nEventActor\x12\x15\n\x11\x41\x43TOR_UNSPECIFIED\x10\x00\x12\t\n\x05HUMAN\x10\x01\x12\x0b\n\x07MACHINE\x10\x02\x12\x07\n\x03\x41PI\x10\x03*<\n\x06Source\x12\x16\n\x12SOURCE_UNSPECIFIED\x10\x00\x12\x0c\n\x08SCALEKIT\x10\x01\x12\x0c\n\x08\x44IR_SYNC\x10\x02*g\n\x0b\x45ventTarget\x12\x1c\n\x18\x45VENT_TARGET_UNSPECIFIED\x10\x00\x12\r\n\tWORKSPACE\x10\x01\x12\x0f\n\x0b\x45NVIRONMENT\x10\x02\x12\x10\n\x0cORGANIZATION\x10\x03\x12\x08\n\x04USER\x10\x04*M\n\rEventCategory\x12\x1c\n\x18\x45VENT_SOURCE_UNSPECIFIED\x10\x00\x12\x08\n\x04\x43ORE\x10\x01\x12\x07\n\x03SSO\x10\x02\x12\x0b\n\x07\x44IRSYNC\x10\x03*\xd8\x01\n\nObjectType\x12\x1b\n\x17OBJECT_TYPE_UNSPECIFIED\x10\x00\x12\r\n\tWorkspace\x10\x01\x12\x0f\n\x0b\x45nvironment\x10\x02\x12\x10\n\x0cOrganization\x10\x03\x12\x0e\n\nConnection\x10\x04\x12\x08\n\x04User\x10\x05\x12\x08\n\x04Role\x10\x06\x12\x14\n\x10\x43ustomAttributes\x10\x07\x12\r\n\tDirectory\x10\x08\x12\x11\n\rDirectoryUser\x10\t\x12\x12\n\x0e\x44irectoryGroup\x10\n\x12\x0b\n\x07Session\x10\x0b\x32\x93\x01\n\rEventsService\x12\x81\x01\n\nListEvents\x12%.scalekit.v1.events.ListEventsRequest\x1a&.scalekit.v1.events.ListEventsResponse\"$\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02\x18\"\x0e/api/v1/events:\x06\x66ilterB2Z0github.com/scalekit-inc/scalekit/pkg/grpc/eventsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.events.events_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/scalekit-inc/scalekit/pkg/grpc/events'
  _globals['_IEVENT_CONTEXTENTRY']._loaded_options = None
  _globals['_IEVENT_CONTEXTENTRY']._serialized_options = b'8\001'
  _globals['_IEVENT_METADATAENTRY']._loaded_options = None
  _globals['_IEVENT_METADATAENTRY']._serialized_options = b'8\001'
  _globals['_IEVENT'].fields_by_name['id']._loaded_options = None
  _globals['_IEVENT'].fields_by_name['id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_IEVENT'].fields_by_name['context']._loaded_options = None
  _globals['_IEVENT'].fields_by_name['context']._serialized_options = b'\272H\024\232\001\021\"\006r\004\020\003\030\031*\007r\005\020\001\030\320\017'
  _globals['_IEVENT'].fields_by_name['metadata']._loaded_options = None
  _globals['_IEVENT'].fields_by_name['metadata']._serialized_options = b'\272H\024\232\001\021\"\006r\004\020\003\030\031*\007r\005\020\001\030\320\017'
  _globals['_EVENT_CONTEXTENTRY']._loaded_options = None
  _globals['_EVENT_CONTEXTENTRY']._serialized_options = b'8\001'
  _globals['_EVENT_METADATAENTRY']._loaded_options = None
  _globals['_EVENT_METADATAENTRY']._serialized_options = b'8\001'
  _globals['_EVENT'].fields_by_name['id']._loaded_options = None
  _globals['_EVENT'].fields_by_name['id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_EVENT'].fields_by_name['context']._loaded_options = None
  _globals['_EVENT'].fields_by_name['context']._serialized_options = b'\272H\024\232\001\021\"\006r\004\020\003\030\031*\007r\005\020\001\030\320\017'
  _globals['_EVENT'].fields_by_name['metadata']._loaded_options = None
  _globals['_EVENT'].fields_by_name['metadata']._serialized_options = b'\272H\024\232\001\021\"\006r\004\020\003\030\031*\007r\005\020\001\030\320\017'
  _globals['_IEVENTFILTER_METADATAENTRY']._loaded_options = None
  _globals['_IEVENTFILTER_METADATAENTRY']._serialized_options = b'8\001'
  _globals['_IEVENTFILTER'].fields_by_name['metadata']._loaded_options = None
  _globals['_IEVENTFILTER'].fields_by_name['metadata']._serialized_options = b'\272H\024\232\001\021\"\006r\004\020\003\030\031*\007r\005\020\001\030\320\017'
  _globals['_SCALEKITEVENT'].fields_by_name['id']._loaded_options = None
  _globals['_SCALEKITEVENT'].fields_by_name['id']._serialized_options = b'\272H\013r\t\020\001\030 :\003evt'
  _globals['_EVENTSSERVICE'].methods_by_name['ListEvents']._loaded_options = None
  _globals['_EVENTSSERVICE'].methods_by_name['ListEvents']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002\030\"\016/api/v1/events:\006filter'
  _globals['_EVENTACTOR']._serialized_start=3559
  _globals['_EVENTACTOR']._serialized_end=3627
  _globals['_SOURCE']._serialized_start=3629
  _globals['_SOURCE']._serialized_end=3689
  _globals['_EVENTTARGET']._serialized_start=3691
  _globals['_EVENTTARGET']._serialized_end=3794
  _globals['_EVENTCATEGORY']._serialized_start=3796
  _globals['_EVENTCATEGORY']._serialized_end=3873
  _globals['_OBJECTTYPE']._serialized_start=3876
  _globals['_OBJECTTYPE']._serialized_end=4092
  _globals['_IEVENTPAGINATIONTOKENS']._serialized_start=387
  _globals['_IEVENTPAGINATIONTOKENS']._serialized_end=497
  _globals['_LISTEVENTSREQUEST']._serialized_start=500
  _globals['_LISTEVENTSREQUEST']._serialized_end=636
  _globals['_LISTEVENTSRESPONSE']._serialized_start=639
  _globals['_LISTEVENTSRESPONSE']._serialized_end=829
  _globals['_IEVENT']._serialized_start=832
  _globals['_IEVENT']._serialized_end=1542
  _globals['_IEVENT_CONTEXTENTRY']._serialized_start=1423
  _globals['_IEVENT_CONTEXTENTRY']._serialized_end=1481
  _globals['_IEVENT_METADATAENTRY']._serialized_start=1483
  _globals['_IEVENT_METADATAENTRY']._serialized_end=1542
  _globals['_EVENT']._serialized_start=1545
  _globals['_EVENT']._serialized_end=2308
  _globals['_EVENT_CONTEXTENTRY']._serialized_start=1423
  _globals['_EVENT_CONTEXTENTRY']._serialized_end=1481
  _globals['_EVENT_METADATAENTRY']._serialized_start=1483
  _globals['_EVENT_METADATAENTRY']._serialized_end=1542
  _globals['_ACTOR']._serialized_start=2310
  _globals['_ACTOR']._serialized_end=2385
  _globals['_TARGET']._serialized_start=2387
  _globals['_TARGET']._serialized_end=2464
  _globals['_IEVENTFILTER']._serialized_start=2467
  _globals['_IEVENTFILTER']._serialized_end=2923
  _globals['_IEVENTFILTER_METADATAENTRY']._serialized_start=1483
  _globals['_IEVENTFILTER_METADATAENTRY']._serialized_end=1542
  _globals['_EVENTFILTER']._serialized_start=2926
  _globals['_EVENTFILTER']._serialized_end=3179
  _globals['_SCALEKITEVENT']._serialized_start=3182
  _globals['_SCALEKITEVENT']._serialized_end=3557
  _globals['_EVENTSSERVICE']._serialized_start=4095
  _globals['_EVENTSSERVICE']._serialized_end=4242
# @@protoc_insertion_point(module_scope)
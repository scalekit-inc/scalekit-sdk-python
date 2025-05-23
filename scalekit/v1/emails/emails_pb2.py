# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/emails/emails.proto
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
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from scalekit.v1.commons import commons_pb2 as scalekit_dot_v1_dot_commons_dot_commons__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fscalekit/v1/emails/emails.proto\x12\x12scalekit.v1.emails\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a!scalekit/v1/commons/commons.proto\x1a!scalekit/v1/options/options.proto\"`\n\x16GetPlaceholdersRequest\x12\x46\n\x08use_case\x18\x01 \x01(\x0e\x32#.scalekit.v1.emails.TemplateUsecaseB\x06\xbaH\x03\xc8\x01\x01R\x07useCase\"B\n\x17GetPlaceholdersResponse\x12\'\n\x0cplaceholders\x18\x01 \x03(\tB\x03\xe0\x41\x03R\x0cplaceholders\"\xea\x02\n\x08Template\x12>\n\nupdated_at\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03R\tupdatedAt\x12\x13\n\x02id\x18\x02 \x01(\tB\x03\xe0\x41\x03R\x02id\x12>\n\x08use_case\x18\x03 \x01(\x0e\x32#.scalekit.v1.emails.TemplateUsecaseR\x07useCase\x12\x18\n\x07\x65nabled\x18\x04 \x01(\x08R\x07\x65nabled\x12$\n\x07subject\x18\x05 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\xff\x01R\x07subject\x12.\n\x0chtml_content\x18\x06 \x01(\tB\x0b\xbaH\x08r\x06\x10\x01(\x80\x80@R\x0bhtmlContent\x12\x30\n\rplain_content\x18\x07 \x01(\tB\x0b\xbaH\x08r\x06\x10\x01(\x80\x80@R\x0cplainContent\x12\'\n\x0cplaceholders\x18\x08 \x03(\tB\x03\xe0\x41\x03R\x0cplaceholders\"\xc8\x02\n\x13\x43reateEmailTemplate\x12>\n\nupdated_at\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03R\tupdatedAt\x12\x13\n\x02id\x18\x02 \x01(\tB\x03\xe0\x41\x03R\x02id\x12K\n\x08use_case\x18\x03 \x01(\x0e\x32#.scalekit.v1.emails.TemplateUsecaseB\x0b\xbaH\x08\x82\x01\x02\x10\x01\xc8\x01\x01R\x07useCase\x12\'\n\x07subject\x18\x04 \x01(\tB\r\xbaH\nr\x05\x10\x01\x18\xff\x01\xc8\x01\x01R\x07subject\x12\x31\n\x0chtml_content\x18\x05 \x01(\tB\x0e\xbaH\x0br\x06\x10\x01(\x80\x80@\xc8\x01\x01R\x0bhtmlContent\x12\x33\n\rplain_content\x18\x06 \x01(\tB\x0e\xbaH\x0br\x06\x10\x01(\x80\x80@\xc8\x01\x01R\x0cplainContent\"\x9d\x01\n\x1a\x43reateEmailTemplateRequest\x12\x32\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x00\x18 R\x0eorganizationId\x12K\n\x08template\x18\x02 \x01(\x0b\x32\'.scalekit.v1.emails.CreateEmailTemplateB\x06\xbaH\x03\xc8\x01\x01R\x08template\"_\n\x1b\x43reateEmailTemplateResponse\x12@\n\x08template\x18\x01 \x01(\x0b\x32\x1c.scalekit.v1.emails.TemplateB\x06\xbaH\x03\xc8\x01\x01R\x08template\"\x84\x01\n\x1a\x45nableEmailTemplateRequest\x12\x32\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x00\x18 R\x0eorganizationId\x12\x32\n\x0btemplate_id\x18\x02 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03tpl\xc8\x01\x01R\ntemplateId\"\xde\x01\n\x1b\x45nableEmailTemplateResponse\x12Z\n\x12\x61\x63tive_template_id\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03tplR\x10\x61\x63tiveTemplateId\x12\x63\n\x17last_active_template_id\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03tplR\x14lastActiveTemplateId\"\x85\x01\n\x1b\x44isableEmailTemplateRequest\x12\x32\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x00\x18 R\x0eorganizationId\x12\x32\n\x0btemplate_id\x18\x02 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03tpl\xc8\x01\x01R\ntemplateId\"\x81\x01\n\x17GetEmailTemplateRequest\x12\x32\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x00\x18 R\x0eorganizationId\x12\x32\n\x0btemplate_id\x18\x02 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03tpl\xc8\x01\x01R\ntemplateId\"T\n\x18GetEmailTemplateResponse\x12\x38\n\x08template\x18\x01 \x01(\x0b\x32\x1c.scalekit.v1.emails.TemplateR\x08template\"N\n\x18ListEmailTemplateRequest\x12\x32\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x00\x18 R\x0eorganizationId\"W\n\x19ListEmailTemplateResponse\x12:\n\ttemplates\x18\x01 \x03(\x0b\x32\x1c.scalekit.v1.emails.TemplateR\ttemplates\"\x90\x03\n\x0eUpdateTemplate\x12)\n\x07subject\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\xff\x01H\x00R\x07subject\x88\x01\x01\x12\x33\n\x0chtml_content\x18\x02 \x01(\tB\x0b\xbaH\x08r\x06\x10\x01(\x80\x80@H\x01R\x0bhtmlContent\x88\x01\x01\x12\x35\n\rplain_content\x18\x03 \x01(\tB\x0b\xbaH\x08r\x06\x10\x01(\x80\x80@H\x02R\x0cplainContent\x88\x01\x01:\xb7\x01\xbaH\xb3\x01\x1a\xb0\x01\n\x1b\x61t_least_one_field_required\x12IAt least one of \'subject\', \'html_content\', or \'plain_content\' must be set\x1a\x46has(this.subject) || has(this.html_content) || has(this.plain_content)B\n\n\x08_subjectB\x0f\n\r_html_contentB\x10\n\x0e_plain_content\"\x88\x02\n\x19PatchEmailTemplateRequest\x12\x32\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x00\x18 R\x0eorganizationId\x12\x32\n\x0btemplate_id\x18\x02 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03tpl\xc8\x01\x01R\ntemplateId\x12\x46\n\x08template\x18\x04 \x01(\x0b\x32\".scalekit.v1.emails.UpdateTemplateB\x06\xbaH\x03\xc8\x01\x01R\x08template\x12;\n\x0bupdate_mask\x18\x63 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\nupdateMask\"\x84\x01\n\x1a\x44\x65leteEmailTemplateRequest\x12\x32\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x00\x18 R\x0eorganizationId\x12\x32\n\x0btemplate_id\x18\x02 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03tpl\xc8\x01\x01R\ntemplateId\"\xac\x02\n\x0b\x45mailServer\x12>\n\nupdated_at\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03R\tupdatedAt\x12\x13\n\x02id\x18\x02 \x01(\tB\x03\xe0\x41\x03R\x02id\x12K\n\x08provider\x18\x03 \x01(\x0e\x32\'.scalekit.v1.emails.EmailServerProviderB\x06\xbaH\x03\xc8\x01\x01R\x08provider\x12\x18\n\x07\x65nabled\x18\x04 \x01(\x08R\x07\x65nabled\x12U\n\rsmtp_settings\x18\x05 \x01(\x0b\x32&.scalekit.v1.emails.SMTPServerSettingsB\x06\xbaH\x03\xc8\x01\x01H\x00R\x0csmtpSettingsB\n\n\x08settings\"\x86\x02\n\x12SMTPServerSettings\x12!\n\x04host\x18\x01 \x01(\tB\r\xbaH\nr\x05\x10\x01\x18\xff\x01\xc8\x01\x01R\x04host\x12\x1a\n\x04port\x18\x02 \x01(\x03\x42\x06\xbaH\x03\xc8\x01\x01R\x04port\x12)\n\x08username\x18\x03 \x01(\tB\r\xbaH\nr\x05\x10\x01\x18\xff\x01\xc8\x01\x01R\x08username\x12,\n\x08password\x18\x04 \x01(\tB\x10\xe0\x41\x04\xbaH\nr\x05\x10\x01\x18\xff\x01\xc8\x01\x01R\x08password\x12,\n\nfrom_email\x18\x05 \x01(\tB\r\xbaH\nr\x05\x10\x01\x18\xff\x01\xc8\x01\x01R\tfromEmail\x12*\n\tfrom_name\x18\x06 \x01(\tB\r\xbaH\nr\x05\x10\x01\x18\xff\x01\xc8\x01\x01R\x08\x66romName\"\xab\x01\n\x18\x43reateEmailServerRequest\x12K\n\x08provider\x18\x01 \x01(\x0e\x32\'.scalekit.v1.emails.EmailServerProviderB\x06\xbaH\x03\xc8\x01\x01R\x08provider\x12\x42\n\x08settings\x18\x02 \x01(\x0b\x32&.scalekit.v1.emails.SMTPServerSettingsR\x08settings\"\\\n\x19\x43reateEmailServerResponse\x12?\n\x06server\x18\x01 \x01(\x0b\x32\x1f.scalekit.v1.emails.EmailServerB\x06\xbaH\x03\xc8\x01\x01R\x06server\"G\n\x15GetEmailServerRequest\x12.\n\tserver_id\x18\x01 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03\x65sr\xc8\x01\x01R\x08serverId\"Q\n\x16GetEmailServerResponse\x12\x37\n\x06server\x18\x01 \x01(\x0b\x32\x1f.scalekit.v1.emails.EmailServerR\x06server\"J\n\x18\x45nableEmailServerRequest\x12.\n\tserver_id\x18\x01 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03\x65sr\xc8\x01\x01R\x08serverId\"\xd4\x01\n\x19\x45nableEmailServerResponse\x12V\n\x10\x61\x63tive_server_id\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03\x65srR\x0e\x61\x63tiveServerId\x12_\n\x15last_active_server_id\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x0e\xbaH\x0br\t\x10\x01\x18 :\x03\x65srR\x12lastActiveServerId\"K\n\x19\x44isableEmailServerRequest\x12.\n\tserver_id\x18\x01 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03\x65sr\xc8\x01\x01R\x08serverId\"T\n\x17ListEmailServerResponse\x12\x39\n\x07servers\x18\x01 \x03(\x0b\x32\x1f.scalekit.v1.emails.EmailServerR\x07servers\"\x9d\x01\n\x1fPatchEmailServerSettingsRequest\x12.\n\tserver_id\x18\x01 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03\x65sr\xc8\x01\x01R\x08serverId\x12J\n\x08settings\x18\x02 \x01(\x0b\x32&.scalekit.v1.emails.SMTPServerSettingsB\x06\xbaH\x03\xc8\x01\x01R\x08settings\"J\n\x18\x44\x65leteEmailServerRequest\x12.\n\tserver_id\x18\x01 \x01(\tB\x11\xbaH\x0er\t\x10\x01\x18 :\x03\x65sr\xc8\x01\x01R\x08serverId*\xcf\x01\n\x0fTemplateUsecase\x12 \n\x1cTEMPLATE_USECASE_UNSPECIFIED\x10\x00\x12\t\n\x05LOGIN\x10\x01\x12\r\n\tOTP_LOGIN\x10\x02\x12\x11\n\rMEMBER_INVITE\x10\x03\x12\x0f\n\x0bUSER_INVITE\x10\x04\x12\x0e\n\nUSER_LOGIN\x10\x05\x12\n\n\x06SIGNUP\x10\x06\x12\x12\n\x0eUSER_LOGIN_OTP\x10\x07\x12\x13\n\x0fUSER_LOGIN_LINK\x10\x08\x12\x17\n\x13USER_LOGIN_LINK_OTP\x10\t*Z\n\x13\x45mailServerProvider\x12\x1c\n\x18\x45MAIL_SERVER_UNSPECIFIED\x10\x00\x12\x0c\n\x08SENDGRID\x10\x01\x12\x0c\n\x08POSTMARK\x10\x02\x12\t\n\x05OTHER\x10\x03\x32\xfc\x17\n\x0c\x45mailService\x12\xa6\x01\n\x17GetTemplatePlaceholders\x12*.scalekit.v1.emails.GetPlaceholdersRequest\x1a+.scalekit.v1.emails.GetPlaceholdersResponse\"2\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02&\x12$/api/v1/email/templates/placeholders\x12\xfd\x01\n\x13\x43reateEmailTemplate\x12..scalekit.v1.emails.CreateEmailTemplateRequest\x1a/.scalekit.v1.emails.CreateEmailTemplateResponse\"\x84\x01\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02x\"7/api/v1/organizations/{organization_id}/email/templates:\x08templateZ3\"\'/api/v1/organizations/-/email/templates:\x08template\x12\x96\x02\n\x13UpdateEmailTemplate\x12-.scalekit.v1.emails.PatchEmailTemplateRequest\x1a,.scalekit.v1.emails.GetEmailTemplateResponse\"\xa1\x01\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x94\x01\x32\x45/api/v1/organizations/{organization_id}/email/templates/{template_id}:\x08templateZA25/api/v1/organizations/-/email/templates/{template_id}:\x08template\x12\x94\x02\n\x13\x45nableEmailTemplate\x12..scalekit.v1.emails.EnableEmailTemplateRequest\x1a/.scalekit.v1.emails.EnableEmailTemplateResponse\"\x9b\x01\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x8e\x01\x32L/api/v1/organizations/{organization_id}/email/templates/{template_id}:enableZ>2</api/v1/organizations/-/email/templates/{template_id}:enable\x12\xff\x01\n\x14\x44isableEmailTemplate\x12/.scalekit.v1.emails.DisableEmailTemplateRequest\x1a\x16.google.protobuf.Empty\"\x9d\x01\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x90\x01\x32M/api/v1/organizations/{organization_id}/email/templates/{template_id}:disableZ?2=/api/v1/organizations/-/email/templates/{template_id}:disable\x12\xfd\x01\n\x10GetEmailTemplate\x12+.scalekit.v1.emails.GetEmailTemplateRequest\x1a,.scalekit.v1.emails.GetEmailTemplateResponse\"\x8d\x01\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x80\x01\x12\x45/api/v1/organizations/{organization_id}/email/templates/{template_id}Z7\x12\x35/api/v1/organizations/-/email/templates/{template_id}\x12\xe3\x01\n\x12ListEmailTemplates\x12,.scalekit.v1.emails.ListEmailTemplateRequest\x1a-.scalekit.v1.emails.ListEmailTemplateResponse\"p\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x64\x12\x37/api/v1/organizations/{organization_id}/email/templatesZ)\x12\'/api/v1/organizations/-/email/templates\x12\xed\x01\n\x13\x44\x65leteEmailTemplate\x12..scalekit.v1.emails.DeleteEmailTemplateRequest\x1a\x16.google.protobuf.Empty\"\x8d\x01\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x80\x01*E/api/v1/organizations/{organization_id}/email/templates/{template_id}Z7*5/api/v1/organizations/-/email/templates/{template_id}\x12\x98\x01\n\x11\x43reateEmailServer\x12,.scalekit.v1.emails.CreateEmailServerRequest\x1a-.scalekit.v1.emails.CreateEmailServerResponse\"&\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x1a\"\x15/api/v1/email/servers:\x01*\x12\xb7\x01\n\x19UpdateEmailServerSettings\x12\x33.scalekit.v1.emails.PatchEmailServerSettingsRequest\x1a*.scalekit.v1.emails.GetEmailServerResponse\"9\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02-\x1a!/api/v1/email/servers/{server_id}:\x08settings\x12\xa8\x01\n\x11\x45nableEmailServer\x12,.scalekit.v1.emails.EnableEmailServerRequest\x1a-.scalekit.v1.emails.EnableEmailServerResponse\"6\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02*2(/api/v1/email/servers/{server_id}:enable\x12\x94\x01\n\x12\x44isableEmailServer\x12-.scalekit.v1.emails.DisableEmailServerRequest\x1a\x16.google.protobuf.Empty\"7\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02+2)/api/v1/email/servers/{server_id}:disable\x12\x98\x01\n\x0eGetEmailServer\x12).scalekit.v1.emails.GetEmailServerRequest\x1a*.scalekit.v1.emails.GetEmailServerResponse\"/\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02#\x12!/api/v1/email/servers/{server_id}\x12|\n\x10ListEmailServers\x12\x16.google.protobuf.Empty\x1a+.scalekit.v1.emails.ListEmailServerResponse\"#\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02\x17\x12\x15/api/v1/email/servers\x12\x8a\x01\n\x11\x44\x65leteEmailServer\x12,.scalekit.v1.emails.DeleteEmailServerRequest\x1a\x16.google.protobuf.Empty\"/\x82\xb5\x18\x02\x18T\x82\xd3\xe4\x93\x02#*!/api/v1/email/servers/{server_id}B2Z0github.com/scalekit-inc/scalekit/pkg/grpc/emailsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.emails.emails_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/scalekit-inc/scalekit/pkg/grpc/emails'
  _globals['_GETPLACEHOLDERSREQUEST'].fields_by_name['use_case']._loaded_options = None
  _globals['_GETPLACEHOLDERSREQUEST'].fields_by_name['use_case']._serialized_options = b'\272H\003\310\001\001'
  _globals['_GETPLACEHOLDERSRESPONSE'].fields_by_name['placeholders']._loaded_options = None
  _globals['_GETPLACEHOLDERSRESPONSE'].fields_by_name['placeholders']._serialized_options = b'\340A\003'
  _globals['_TEMPLATE'].fields_by_name['updated_at']._loaded_options = None
  _globals['_TEMPLATE'].fields_by_name['updated_at']._serialized_options = b'\340A\003'
  _globals['_TEMPLATE'].fields_by_name['id']._loaded_options = None
  _globals['_TEMPLATE'].fields_by_name['id']._serialized_options = b'\340A\003'
  _globals['_TEMPLATE'].fields_by_name['subject']._loaded_options = None
  _globals['_TEMPLATE'].fields_by_name['subject']._serialized_options = b'\272H\007r\005\020\001\030\377\001'
  _globals['_TEMPLATE'].fields_by_name['html_content']._loaded_options = None
  _globals['_TEMPLATE'].fields_by_name['html_content']._serialized_options = b'\272H\010r\006\020\001(\200\200@'
  _globals['_TEMPLATE'].fields_by_name['plain_content']._loaded_options = None
  _globals['_TEMPLATE'].fields_by_name['plain_content']._serialized_options = b'\272H\010r\006\020\001(\200\200@'
  _globals['_TEMPLATE'].fields_by_name['placeholders']._loaded_options = None
  _globals['_TEMPLATE'].fields_by_name['placeholders']._serialized_options = b'\340A\003'
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['updated_at']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['updated_at']._serialized_options = b'\340A\003'
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['id']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['id']._serialized_options = b'\340A\003'
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['use_case']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['use_case']._serialized_options = b'\272H\010\202\001\002\020\001\310\001\001'
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['subject']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['subject']._serialized_options = b'\272H\nr\005\020\001\030\377\001\310\001\001'
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['html_content']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['html_content']._serialized_options = b'\272H\013r\006\020\001(\200\200@\310\001\001'
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['plain_content']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATE'].fields_by_name['plain_content']._serialized_options = b'\272H\013r\006\020\001(\200\200@\310\001\001'
  _globals['_CREATEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\000\030 '
  _globals['_CREATEEMAILTEMPLATEREQUEST'].fields_by_name['template']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATEREQUEST'].fields_by_name['template']._serialized_options = b'\272H\003\310\001\001'
  _globals['_CREATEEMAILTEMPLATERESPONSE'].fields_by_name['template']._loaded_options = None
  _globals['_CREATEEMAILTEMPLATERESPONSE'].fields_by_name['template']._serialized_options = b'\272H\003\310\001\001'
  _globals['_ENABLEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_ENABLEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\000\030 '
  _globals['_ENABLEEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._loaded_options = None
  _globals['_ENABLEEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003tpl\310\001\001'
  _globals['_ENABLEEMAILTEMPLATERESPONSE'].fields_by_name['active_template_id']._loaded_options = None
  _globals['_ENABLEEMAILTEMPLATERESPONSE'].fields_by_name['active_template_id']._serialized_options = b'\272H\013r\t\020\001\030 :\003tpl'
  _globals['_ENABLEEMAILTEMPLATERESPONSE'].fields_by_name['last_active_template_id']._loaded_options = None
  _globals['_ENABLEEMAILTEMPLATERESPONSE'].fields_by_name['last_active_template_id']._serialized_options = b'\272H\013r\t\020\001\030 :\003tpl'
  _globals['_DISABLEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_DISABLEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\000\030 '
  _globals['_DISABLEEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._loaded_options = None
  _globals['_DISABLEEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003tpl\310\001\001'
  _globals['_GETEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_GETEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\000\030 '
  _globals['_GETEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._loaded_options = None
  _globals['_GETEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003tpl\310\001\001'
  _globals['_LISTEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_LISTEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\000\030 '
  _globals['_UPDATETEMPLATE'].fields_by_name['subject']._loaded_options = None
  _globals['_UPDATETEMPLATE'].fields_by_name['subject']._serialized_options = b'\272H\007r\005\020\001\030\377\001'
  _globals['_UPDATETEMPLATE'].fields_by_name['html_content']._loaded_options = None
  _globals['_UPDATETEMPLATE'].fields_by_name['html_content']._serialized_options = b'\272H\010r\006\020\001(\200\200@'
  _globals['_UPDATETEMPLATE'].fields_by_name['plain_content']._loaded_options = None
  _globals['_UPDATETEMPLATE'].fields_by_name['plain_content']._serialized_options = b'\272H\010r\006\020\001(\200\200@'
  _globals['_UPDATETEMPLATE']._loaded_options = None
  _globals['_UPDATETEMPLATE']._serialized_options = b'\272H\263\001\032\260\001\n\033at_least_one_field_required\022IAt least one of \'subject\', \'html_content\', or \'plain_content\' must be set\032Fhas(this.subject) || has(this.html_content) || has(this.plain_content)'
  _globals['_PATCHEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_PATCHEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\000\030 '
  _globals['_PATCHEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._loaded_options = None
  _globals['_PATCHEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003tpl\310\001\001'
  _globals['_PATCHEMAILTEMPLATEREQUEST'].fields_by_name['template']._loaded_options = None
  _globals['_PATCHEMAILTEMPLATEREQUEST'].fields_by_name['template']._serialized_options = b'\272H\003\310\001\001'
  _globals['_DELETEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_DELETEEMAILTEMPLATEREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\000\030 '
  _globals['_DELETEEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._loaded_options = None
  _globals['_DELETEEMAILTEMPLATEREQUEST'].fields_by_name['template_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003tpl\310\001\001'
  _globals['_EMAILSERVER'].fields_by_name['updated_at']._loaded_options = None
  _globals['_EMAILSERVER'].fields_by_name['updated_at']._serialized_options = b'\340A\003'
  _globals['_EMAILSERVER'].fields_by_name['id']._loaded_options = None
  _globals['_EMAILSERVER'].fields_by_name['id']._serialized_options = b'\340A\003'
  _globals['_EMAILSERVER'].fields_by_name['provider']._loaded_options = None
  _globals['_EMAILSERVER'].fields_by_name['provider']._serialized_options = b'\272H\003\310\001\001'
  _globals['_EMAILSERVER'].fields_by_name['smtp_settings']._loaded_options = None
  _globals['_EMAILSERVER'].fields_by_name['smtp_settings']._serialized_options = b'\272H\003\310\001\001'
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['host']._loaded_options = None
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['host']._serialized_options = b'\272H\nr\005\020\001\030\377\001\310\001\001'
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['port']._loaded_options = None
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['port']._serialized_options = b'\272H\003\310\001\001'
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['username']._loaded_options = None
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['username']._serialized_options = b'\272H\nr\005\020\001\030\377\001\310\001\001'
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['password']._loaded_options = None
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['password']._serialized_options = b'\340A\004\272H\nr\005\020\001\030\377\001\310\001\001'
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['from_email']._loaded_options = None
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['from_email']._serialized_options = b'\272H\nr\005\020\001\030\377\001\310\001\001'
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['from_name']._loaded_options = None
  _globals['_SMTPSERVERSETTINGS'].fields_by_name['from_name']._serialized_options = b'\272H\nr\005\020\001\030\377\001\310\001\001'
  _globals['_CREATEEMAILSERVERREQUEST'].fields_by_name['provider']._loaded_options = None
  _globals['_CREATEEMAILSERVERREQUEST'].fields_by_name['provider']._serialized_options = b'\272H\003\310\001\001'
  _globals['_CREATEEMAILSERVERRESPONSE'].fields_by_name['server']._loaded_options = None
  _globals['_CREATEEMAILSERVERRESPONSE'].fields_by_name['server']._serialized_options = b'\272H\003\310\001\001'
  _globals['_GETEMAILSERVERREQUEST'].fields_by_name['server_id']._loaded_options = None
  _globals['_GETEMAILSERVERREQUEST'].fields_by_name['server_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003esr\310\001\001'
  _globals['_ENABLEEMAILSERVERREQUEST'].fields_by_name['server_id']._loaded_options = None
  _globals['_ENABLEEMAILSERVERREQUEST'].fields_by_name['server_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003esr\310\001\001'
  _globals['_ENABLEEMAILSERVERRESPONSE'].fields_by_name['active_server_id']._loaded_options = None
  _globals['_ENABLEEMAILSERVERRESPONSE'].fields_by_name['active_server_id']._serialized_options = b'\272H\013r\t\020\001\030 :\003esr'
  _globals['_ENABLEEMAILSERVERRESPONSE'].fields_by_name['last_active_server_id']._loaded_options = None
  _globals['_ENABLEEMAILSERVERRESPONSE'].fields_by_name['last_active_server_id']._serialized_options = b'\272H\013r\t\020\001\030 :\003esr'
  _globals['_DISABLEEMAILSERVERREQUEST'].fields_by_name['server_id']._loaded_options = None
  _globals['_DISABLEEMAILSERVERREQUEST'].fields_by_name['server_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003esr\310\001\001'
  _globals['_PATCHEMAILSERVERSETTINGSREQUEST'].fields_by_name['server_id']._loaded_options = None
  _globals['_PATCHEMAILSERVERSETTINGSREQUEST'].fields_by_name['server_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003esr\310\001\001'
  _globals['_PATCHEMAILSERVERSETTINGSREQUEST'].fields_by_name['settings']._loaded_options = None
  _globals['_PATCHEMAILSERVERSETTINGSREQUEST'].fields_by_name['settings']._serialized_options = b'\272H\003\310\001\001'
  _globals['_DELETEEMAILSERVERREQUEST'].fields_by_name['server_id']._loaded_options = None
  _globals['_DELETEEMAILSERVERREQUEST'].fields_by_name['server_id']._serialized_options = b'\272H\016r\t\020\001\030 :\003esr\310\001\001'
  _globals['_EMAILSERVICE'].methods_by_name['GetTemplatePlaceholders']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['GetTemplatePlaceholders']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002&\022$/api/v1/email/templates/placeholders'
  _globals['_EMAILSERVICE'].methods_by_name['CreateEmailTemplate']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['CreateEmailTemplate']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002x\"7/api/v1/organizations/{organization_id}/email/templates:\010templateZ3\"\'/api/v1/organizations/-/email/templates:\010template'
  _globals['_EMAILSERVICE'].methods_by_name['UpdateEmailTemplate']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['UpdateEmailTemplate']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\224\0012E/api/v1/organizations/{organization_id}/email/templates/{template_id}:\010templateZA25/api/v1/organizations/-/email/templates/{template_id}:\010template'
  _globals['_EMAILSERVICE'].methods_by_name['EnableEmailTemplate']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['EnableEmailTemplate']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\216\0012L/api/v1/organizations/{organization_id}/email/templates/{template_id}:enableZ>2</api/v1/organizations/-/email/templates/{template_id}:enable'
  _globals['_EMAILSERVICE'].methods_by_name['DisableEmailTemplate']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['DisableEmailTemplate']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\220\0012M/api/v1/organizations/{organization_id}/email/templates/{template_id}:disableZ?2=/api/v1/organizations/-/email/templates/{template_id}:disable'
  _globals['_EMAILSERVICE'].methods_by_name['GetEmailTemplate']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['GetEmailTemplate']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\200\001\022E/api/v1/organizations/{organization_id}/email/templates/{template_id}Z7\0225/api/v1/organizations/-/email/templates/{template_id}'
  _globals['_EMAILSERVICE'].methods_by_name['ListEmailTemplates']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['ListEmailTemplates']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002d\0227/api/v1/organizations/{organization_id}/email/templatesZ)\022\'/api/v1/organizations/-/email/templates'
  _globals['_EMAILSERVICE'].methods_by_name['DeleteEmailTemplate']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['DeleteEmailTemplate']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\200\001*E/api/v1/organizations/{organization_id}/email/templates/{template_id}Z7*5/api/v1/organizations/-/email/templates/{template_id}'
  _globals['_EMAILSERVICE'].methods_by_name['CreateEmailServer']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['CreateEmailServer']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\032\"\025/api/v1/email/servers:\001*'
  _globals['_EMAILSERVICE'].methods_by_name['UpdateEmailServerSettings']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['UpdateEmailServerSettings']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002-\032!/api/v1/email/servers/{server_id}:\010settings'
  _globals['_EMAILSERVICE'].methods_by_name['EnableEmailServer']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['EnableEmailServer']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002*2(/api/v1/email/servers/{server_id}:enable'
  _globals['_EMAILSERVICE'].methods_by_name['DisableEmailServer']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['DisableEmailServer']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002+2)/api/v1/email/servers/{server_id}:disable'
  _globals['_EMAILSERVICE'].methods_by_name['GetEmailServer']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['GetEmailServer']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002#\022!/api/v1/email/servers/{server_id}'
  _globals['_EMAILSERVICE'].methods_by_name['ListEmailServers']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['ListEmailServers']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002\027\022\025/api/v1/email/servers'
  _globals['_EMAILSERVICE'].methods_by_name['DeleteEmailServer']._loaded_options = None
  _globals['_EMAILSERVICE'].methods_by_name['DeleteEmailServer']._serialized_options = b'\202\265\030\002\030T\202\323\344\223\002#*!/api/v1/email/servers/{server_id}'
  _globals['_TEMPLATEUSECASE']._serialized_start=4835
  _globals['_TEMPLATEUSECASE']._serialized_end=5042
  _globals['_EMAILSERVERPROVIDER']._serialized_start=5044
  _globals['_EMAILSERVERPROVIDER']._serialized_end=5134
  _globals['_GETPLACEHOLDERSREQUEST']._serialized_start=345
  _globals['_GETPLACEHOLDERSREQUEST']._serialized_end=441
  _globals['_GETPLACEHOLDERSRESPONSE']._serialized_start=443
  _globals['_GETPLACEHOLDERSRESPONSE']._serialized_end=509
  _globals['_TEMPLATE']._serialized_start=512
  _globals['_TEMPLATE']._serialized_end=874
  _globals['_CREATEEMAILTEMPLATE']._serialized_start=877
  _globals['_CREATEEMAILTEMPLATE']._serialized_end=1205
  _globals['_CREATEEMAILTEMPLATEREQUEST']._serialized_start=1208
  _globals['_CREATEEMAILTEMPLATEREQUEST']._serialized_end=1365
  _globals['_CREATEEMAILTEMPLATERESPONSE']._serialized_start=1367
  _globals['_CREATEEMAILTEMPLATERESPONSE']._serialized_end=1462
  _globals['_ENABLEEMAILTEMPLATEREQUEST']._serialized_start=1465
  _globals['_ENABLEEMAILTEMPLATEREQUEST']._serialized_end=1597
  _globals['_ENABLEEMAILTEMPLATERESPONSE']._serialized_start=1600
  _globals['_ENABLEEMAILTEMPLATERESPONSE']._serialized_end=1822
  _globals['_DISABLEEMAILTEMPLATEREQUEST']._serialized_start=1825
  _globals['_DISABLEEMAILTEMPLATEREQUEST']._serialized_end=1958
  _globals['_GETEMAILTEMPLATEREQUEST']._serialized_start=1961
  _globals['_GETEMAILTEMPLATEREQUEST']._serialized_end=2090
  _globals['_GETEMAILTEMPLATERESPONSE']._serialized_start=2092
  _globals['_GETEMAILTEMPLATERESPONSE']._serialized_end=2176
  _globals['_LISTEMAILTEMPLATEREQUEST']._serialized_start=2178
  _globals['_LISTEMAILTEMPLATEREQUEST']._serialized_end=2256
  _globals['_LISTEMAILTEMPLATERESPONSE']._serialized_start=2258
  _globals['_LISTEMAILTEMPLATERESPONSE']._serialized_end=2345
  _globals['_UPDATETEMPLATE']._serialized_start=2348
  _globals['_UPDATETEMPLATE']._serialized_end=2748
  _globals['_PATCHEMAILTEMPLATEREQUEST']._serialized_start=2751
  _globals['_PATCHEMAILTEMPLATEREQUEST']._serialized_end=3015
  _globals['_DELETEEMAILTEMPLATEREQUEST']._serialized_start=3018
  _globals['_DELETEEMAILTEMPLATEREQUEST']._serialized_end=3150
  _globals['_EMAILSERVER']._serialized_start=3153
  _globals['_EMAILSERVER']._serialized_end=3453
  _globals['_SMTPSERVERSETTINGS']._serialized_start=3456
  _globals['_SMTPSERVERSETTINGS']._serialized_end=3718
  _globals['_CREATEEMAILSERVERREQUEST']._serialized_start=3721
  _globals['_CREATEEMAILSERVERREQUEST']._serialized_end=3892
  _globals['_CREATEEMAILSERVERRESPONSE']._serialized_start=3894
  _globals['_CREATEEMAILSERVERRESPONSE']._serialized_end=3986
  _globals['_GETEMAILSERVERREQUEST']._serialized_start=3988
  _globals['_GETEMAILSERVERREQUEST']._serialized_end=4059
  _globals['_GETEMAILSERVERRESPONSE']._serialized_start=4061
  _globals['_GETEMAILSERVERRESPONSE']._serialized_end=4142
  _globals['_ENABLEEMAILSERVERREQUEST']._serialized_start=4144
  _globals['_ENABLEEMAILSERVERREQUEST']._serialized_end=4218
  _globals['_ENABLEEMAILSERVERRESPONSE']._serialized_start=4221
  _globals['_ENABLEEMAILSERVERRESPONSE']._serialized_end=4433
  _globals['_DISABLEEMAILSERVERREQUEST']._serialized_start=4435
  _globals['_DISABLEEMAILSERVERREQUEST']._serialized_end=4510
  _globals['_LISTEMAILSERVERRESPONSE']._serialized_start=4512
  _globals['_LISTEMAILSERVERRESPONSE']._serialized_end=4596
  _globals['_PATCHEMAILSERVERSETTINGSREQUEST']._serialized_start=4599
  _globals['_PATCHEMAILSERVERSETTINGSREQUEST']._serialized_end=4756
  _globals['_DELETEEMAILSERVERREQUEST']._serialized_start=4758
  _globals['_DELETEEMAILSERVERREQUEST']._serialized_end=4832
  _globals['_EMAILSERVICE']._serialized_start=5137
  _globals['_EMAILSERVICE']._serialized_end=8205
# @@protoc_insertion_point(module_scope)

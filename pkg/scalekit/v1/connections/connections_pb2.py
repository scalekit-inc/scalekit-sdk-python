# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scalekit/v1/connections/connections.proto
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
from scalekit.v1.commons import commons_pb2 as scalekit_dot_v1_dot_commons_dot_commons__pb2
from scalekit.v1.options import options_pb2 as scalekit_dot_v1_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)scalekit/v1/connections/connections.proto\x12\x17scalekit.v1.connections\x1a\x1b\x62uf/validate/validate.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a!scalekit/v1/commons/commons.proto\x1a!scalekit/v1/options/options.proto\"\xde\x01\n\x17\x43reateConnectionRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12Q\n\nconnection\x18\x03 \x01(\x0b\x32).scalekit.v1.connections.CreateConnectionB\x06\xbaH\x03\xc8\x01\x01R\nconnectionB\x0c\n\nidentities\"\xac\x01\n\x10\x43reateConnection\x12Q\n\x08provider\x18\x01 \x01(\x0e\x32+.scalekit.v1.connections.ConnectionProviderB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x08provider\x12\x45\n\x04type\x18\x02 \x01(\x0e\x32\'.scalekit.v1.connections.ConnectionTypeB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x04type\"\xd2\x07\n\nConnection\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12G\n\x08provider\x18\x02 \x01(\x0e\x32+.scalekit.v1.connections.ConnectionProviderR\x08provider\x12;\n\x04type\x18\x03 \x01(\x0e\x32\'.scalekit.v1.connections.ConnectionTypeR\x04type\x12\x41\n\x06status\x18\x04 \x01(\x0e\x32).scalekit.v1.connections.ConnectionStatusR\x06status\x12\x18\n\x07\x65nabled\x18\x05 \x01(\x08R\x07\x65nabled\x12#\n\rdebug_enabled\x18\x06 \x01(\x08R\x0c\x64\x65\x62ugEnabled\x12\'\n\x0forganization_id\x18\x07 \x01(\tR\x0eorganizationId\x12&\n\x0fui_button_title\x18\x08 \x01(\tR\ruiButtonTitle\x12\x30\n\x14login_initiation_uri\x18\t \x01(\tR\x12loginInitiationUri\x12\x1d\n\nlogout_uri\x18\n \x01(\tR\tlogoutUri\x12Y\n\x12\x63onfiguration_type\x18\x0b \x01(\x0e\x32*.scalekit.v1.connections.ConfigurationTypeR\x11\x63onfigurationType\x12.\n\x13test_connection_uri\x18\x0c \x01(\tR\x11testConnectionUri\x12P\n\x0boidc_config\x18\r \x01(\x0b\x32-.scalekit.v1.connections.OIDCConnectionConfigH\x00R\noidcConfig\x12X\n\x0bsaml_config\x18\x0e \x01(\x0b\x32\x35.scalekit.v1.connections.SAMLConnectionConfigResponseH\x00R\nsamlConfig\x12\x81\x01\n\x11\x61ttribute_mapping\x18\x0f \x03(\x0b\x32\x39.scalekit.v1.connections.Connection.AttributeMappingEntryB\x19\xbaH\x16\x9a\x01\x13\x10\n\"\x06r\x04\x10\x01\x18\x19*\x07r\x05\x10\x01\x18\x80\x02R\x10\x61ttributeMapping\x1a\x43\n\x15\x41ttributeMappingEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\n\n\x08settings\"_\n\x18\x43reateConnectionResponse\x12\x43\n\nconnection\x18\x01 \x01(\x0b\x32#.scalekit.v1.connections.ConnectionR\nconnection\"\xf9\x01\n\x17UpdateConnectionRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12\x19\n\x02id\x18\x03 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x02id\x12Q\n\nconnection\x18\x04 \x01(\x0b\x32).scalekit.v1.connections.UpdateConnectionB\x06\xbaH\x03\xc8\x01\x01R\nconnectionB\x0c\n\nidentities\"\xdb\x06\n\x10UpdateConnection\x12Q\n\x08provider\x18\x01 \x01(\x0e\x32+.scalekit.v1.connections.ConnectionProviderB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x08provider\x12\x45\n\x04type\x18\x02 \x01(\x0e\x32\'.scalekit.v1.connections.ConnectionTypeB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x04type\x12?\n\rdebug_enabled\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x0c\x64\x65\x62ugEnabled\x12\x44\n\x0fui_button_title\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\ruiButtonTitle\x12;\n\nlogout_uri\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\tlogoutUri\x12\x63\n\x12\x63onfiguration_type\x18\x06 \x01(\x0e\x32*.scalekit.v1.connections.ConfigurationTypeB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x11\x63onfigurationType\x12P\n\x0boidc_config\x18\x07 \x01(\x0b\x32-.scalekit.v1.connections.OIDCConnectionConfigH\x00R\noidcConfig\x12W\n\x0bsaml_config\x18\x08 \x01(\x0b\x32\x34.scalekit.v1.connections.SAMLConnectionConfigRequestH\x00R\nsamlConfig\x12\x87\x01\n\x11\x61ttribute_mapping\x18\t \x03(\x0b\x32?.scalekit.v1.connections.UpdateConnection.AttributeMappingEntryB\x19\xbaH\x16\x9a\x01\x13\x10\n\"\x06r\x04\x10\x01\x18\x19*\x07r\x05\x10\x01\x18\x80\x02R\x10\x61ttributeMapping\x1a\x43\n\x15\x41ttributeMappingEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\n\n\x08settings\"_\n\x18UpdateConnectionResponse\x12\x43\n\nconnection\x18\x01 \x01(\x0b\x32#.scalekit.v1.connections.ConnectionR\nconnection\"\xa6\x01\n\x17\x44\x65leteConnectionRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12\x19\n\x02id\x18\x03 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x02idB\x0c\n\nidentities\"\xa3\x01\n\x14GetConnectionRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12\x19\n\x02id\x18\x03 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x02idB\x0c\n\nidentities\"\\\n\x15GetConnectionResponse\x12\x43\n\nconnection\x18\x01 \x01(\x0b\x32#.scalekit.v1.connections.ConnectionR\nconnection\"\xb5\x01\n\x16ListConnectionsRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12\x1d\n\x07include\x18\x03 \x01(\tH\x01R\x07include\x88\x01\x01\x42\x0c\n\nidentitiesB\n\n\x08_include\"d\n\x17ListConnectionsResponse\x12I\n\x0b\x63onnections\x18\x01 \x03(\x0b\x32\'.scalekit.v1.connections.ListConnectionR\x0b\x63onnections\"\xd4\x02\n\x0eListConnection\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12G\n\x08provider\x18\x02 \x01(\x0e\x32+.scalekit.v1.connections.ConnectionProviderR\x08provider\x12;\n\x04type\x18\x03 \x01(\x0e\x32\'.scalekit.v1.connections.ConnectionTypeR\x04type\x12\x41\n\x06status\x18\x04 \x01(\x0e\x32).scalekit.v1.connections.ConnectionStatusR\x06status\x12\x18\n\x07\x65nabled\x18\x05 \x01(\x08R\x07\x65nabled\x12\'\n\x0forganization_id\x18\x06 \x01(\tR\x0eorganizationId\x12&\n\x0fui_button_title\x18\x07 \x01(\tR\ruiButtonTitle\"\xa6\x01\n\x17\x45nableConnectionRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12\x19\n\x02id\x18\x03 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x02idB\x0c\n\nidentities\"\xa7\x01\n\x18\x44isableConnectionRequest\x12\x34\n\x0forganization_id\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\x0eorganizationId\x12,\n\x0b\x65xternal_id\x18\x02 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 H\x00R\nexternalId\x12\x19\n\x02id\x18\x03 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x02idB\x0c\n\nidentities\"p\n\x18ToggleConnectionResponse\x12\x18\n\x07\x65nabled\x18\x01 \x01(\x08R\x07\x65nabled\x12(\n\rerror_message\x18\x02 \x01(\tH\x00R\x0c\x65rrorMessage\x88\x01\x01\x42\x10\n\x0e_error_message\"\xfe\x05\n\x14OIDCConnectionConfig\x12\x34\n\x06issuer\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x06issuer\x12K\n\x12\x64iscovery_endpoint\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x11\x64iscoveryEndpoint\x12\x41\n\rauthorize_uri\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0c\x61uthorizeUri\x12\x39\n\ttoken_uri\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x08tokenUri\x12@\n\ruser_info_uri\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0buserInfoUri\x12\x37\n\x08jwks_uri\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x07jwksUri\x12\x39\n\tclient_id\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x08\x63lientId\x12\x41\n\rclient_secret\x18\t \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0c\x63lientSecret\x12:\n\x06scopes\x18\n \x03(\x0e\x32\".scalekit.v1.connections.OIDCScopeR\x06scopes\x12N\n\x0ftoken_auth_type\x18\x0b \x01(\x0e\x32&.scalekit.v1.connections.TokenAuthTypeR\rtokenAuthType\x12!\n\x0credirect_uri\x18\x0c \x01(\tR\x0bredirectUri\x12=\n\x0cpkce_enabled\x18\r \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x0bpkceEnabled\"\x90\t\n\x1bSAMLConnectionConfigRequest\x12\x46\n\x10idp_metadata_url\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0eidpMetadataUrl\x12@\n\ridp_entity_id\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0bidpEntityId\x12<\n\x0bidp_sso_url\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\tidpSsoUrl\x12\x45\n\x0fidp_certificate\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0eidpCertificate\x12<\n\x0bidp_slo_url\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\tidpSloUrl\x12\x44\n\x0fui_button_title\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\ruiButtonTitle\x12R\n\x12idp_name_id_format\x18\x07 \x01(\x0e\x32%.scalekit.v1.connections.NameIdFormatR\x0fidpNameIdFormat\x12W\n\x13sso_request_binding\x18\x08 \x01(\x0e\x32\'.scalekit.v1.connections.RequestBindingR\x11ssoRequestBinding\x12W\n\x13slo_request_binding\x18\t \x01(\x0e\x32\'.scalekit.v1.connections.RequestBindingR\x11sloRequestBinding\x12[\n\x13saml_signing_option\x18\n \x01(\x0e\x32+.scalekit.v1.connections.SAMLSigningOptionsR\x11samlSigningOption\x12U\n\x19\x61llow_idp_initiated_login\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x16\x61llowIdpInitiatedLogin\x12;\n\x0b\x66orce_authn\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\nforceAuthn\x12N\n\x14\x64\x65\x66\x61ult_redirect_uri\x18\r \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x12\x64\x65\x66\x61ultRedirectUri\x12K\n\x13\x61ssertion_encrypted\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x12\x61ssertionEncrypted\x12J\n\x13want_request_signed\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x11wantRequestSigned\"\xa0\n\n\x1cSAMLConnectionConfigResponse\x12 \n\x0csp_entity_id\x18\x01 \x01(\tR\nspEntityId\x12(\n\x10sp_assertion_url\x18\x02 \x01(\tR\x0espAssertionUrl\x12&\n\x0fsp_metadata_url\x18\x03 \x01(\tR\rspMetadataUrl\x12\x46\n\x10idp_metadata_url\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0eidpMetadataUrl\x12@\n\ridp_entity_id\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x0bidpEntityId\x12<\n\x0bidp_sso_url\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\tidpSsoUrl\x12R\n\x10idp_certificates\x18\x07 \x03(\x0b\x32\'.scalekit.v1.connections.IDPCertificateR\x0fidpCertificates\x12<\n\x0bidp_slo_url\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\tidpSloUrl\x12\x44\n\x0fui_button_title\x18\t \x01(\x0b\x32\x1c.google.protobuf.StringValueR\ruiButtonTitle\x12R\n\x12idp_name_id_format\x18\n \x01(\x0e\x32%.scalekit.v1.connections.NameIdFormatR\x0fidpNameIdFormat\x12^\n\x17idp_sso_request_binding\x18\x0b \x01(\x0e\x32\'.scalekit.v1.connections.RequestBindingR\x14idpSsoRequestBinding\x12^\n\x17idp_slo_request_binding\x18\x0c \x01(\x0e\x32\'.scalekit.v1.connections.RequestBindingR\x14idpSloRequestBinding\x12[\n\x13saml_signing_option\x18\r \x01(\x0e\x32+.scalekit.v1.connections.SAMLSigningOptionsR\x11samlSigningOption\x12U\n\x19\x61llow_idp_initiated_login\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x16\x61llowIdpInitiatedLogin\x12;\n\x0b\x66orce_authn\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\nforceAuthn\x12N\n\x14\x64\x65\x66\x61ult_redirect_uri\x18\x10 \x01(\x0b\x32\x1c.google.protobuf.StringValueR\x12\x64\x65\x66\x61ultRedirectUri\x12K\n\x13\x61ssertion_encrypted\x18\x11 \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x12\x61ssertionEncrypted\x12J\n\x13want_request_signed\x18\x12 \x01(\x0b\x32\x1a.google.protobuf.BoolValueR\x11wantRequestSigned\"\xd4\x01\n\x0eIDPCertificate\x12 \n\x0b\x63\x65rtificate\x18\x01 \x01(\tR\x0b\x63\x65rtificate\x12;\n\x0b\x63reate_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0b\x65xpiry_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nexpiryTime\x12\x0e\n\x02id\x18\x04 \x01(\tR\x02id\x12\x16\n\x06issuer\x18\x05 \x01(\tR\x06issuer\"A\n\x1cGetConnectionByDomainRequest\x12!\n\x06\x64omain\x18\x01 \x01(\tB\t\xbaH\x06r\x04\x10\x01\x18 R\x06\x64omain\"\xec\x01\n\x1dGetConnectionByDomainResponse\x12#\n\rconnection_id\x18\x01 \x01(\tR\x0c\x63onnectionId\x12\x41\n\x06status\x18\x02 \x01(\x0e\x32).scalekit.v1.connections.ConnectionStatusR\x06status\x12;\n\x04type\x18\x03 \x01(\x0e\x32\'.scalekit.v1.connections.ConnectionTypeR\x04type\x12&\n\x0fui_button_title\x18\x04 \x01(\tR\ruiButtonTitle\"b\n\x16GetOIDCMetadataRequest\x12H\n\x08metadata\x18\x01 \x01(\x0b\x32,.scalekit.v1.connections.OIDCMetadataRequestR\x08metadata\"9\n\x13OIDCMetadataRequest\x12\"\n\x06issuer\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\xc8\x01R\x06issuer\"\xd7\x01\n\x17GetOIDCMetadataResponse\x12\x16\n\x06issuer\x18\x01 \x01(\tR\x06issuer\x12\x35\n\x16\x61uthorization_endpoint\x18\x02 \x01(\tR\x15\x61uthorizationEndpoint\x12%\n\x0etoken_endpoint\x18\x03 \x01(\tR\rtokenEndpoint\x12+\n\x11userinfo_endpoint\x18\x04 \x01(\tR\x10userinfoEndpoint\x12\x19\n\x08jwks_uri\x18\x05 \x01(\tR\x07jwksUri\"b\n\x16GetSAMLMetadataRequest\x12H\n\x08metadata\x18\x01 \x01(\x0b\x32,.scalekit.v1.connections.SAMLMetadataRequestR\x08metadata\"D\n\x13SAMLMetadataRequest\x12-\n\x0cmetadata_url\x18\x01 \x01(\tB\n\xbaH\x07r\x05\x10\x01\x18\xc8\x01R\x0bmetadataUrl\"\xb4\x02\n\x17GetSAMLMetadataResponse\x12\"\n\ridp_entity_id\x18\x01 \x01(\tR\x0bidpEntityId\x12\x1e\n\x0bidp_sso_url\x18\x02 \x01(\tR\tidpSsoUrl\x12\x1e\n\x0bidp_slo_url\x18\x03 \x01(\tR\tidpSloUrl\x12)\n\x10idp_certificates\x18\x04 \x03(\tR\x0fidpCertificates\x12+\n\x12idp_name_id_format\x18\x05 \x01(\tR\x0fidpNameIdFormat\x12\'\n\x0frequest_binding\x18\x06 \x01(\tR\x0erequestBinding\x12\x34\n\x16want_assertions_signed\x18\x07 \x01(\x08R\x14wantAssertionsSigned\"u\n GetSAMLCertificateDetailsRequest\x12Q\n\x0b\x63\x65rtificate\x18\x01 \x01(\x0b\x32/.scalekit.v1.connections.SAMLCertificateRequestR\x0b\x63\x65rtificate\"5\n\x16SAMLCertificateRequest\x12\x1b\n\x04text\x18\x01 \x01(\tB\x07\xbaH\x04r\x02\x10\x01R\x04text\"\xa5\x01\n!GetSAMLCertificateDetailsResponse\x12\x12\n\x04text\x18\x01 \x01(\tR\x04text\x12\x1b\n\tnot_after\x18\x02 \x01(\x03R\x08notAfter\x12\x1d\n\nnot_before\x18\x03 \x01(\x03R\tnotBefore\x12\x18\n\x07subject\x18\x04 \x01(\tR\x07subject\x12\x16\n\x06issuer\x18\x05 \x01(\tR\x06issuer\"\x1a\n\x18PasswordConnectionConfig*R\n\x11\x43onfigurationType\x12\"\n\x1e\x43ONFIGURATION_TYPE_UNSPECIFIED\x10\x00\x12\r\n\tDISCOVERY\x10\x01\x12\n\n\x06MANUAL\x10\x02*a\n\x0cNameIdFormat\x12\x16\n\x12NAME_ID_FORMAT_NIL\x10\x00\x12\x0f\n\x0bUNSPECIFIED\x10\x01\x12\t\n\x05\x45MAIL\x10\x02\x12\r\n\tTRANSIENT\x10\x03\x12\x0e\n\nPERSISTENT\x10\x04*\xb0\x01\n\x12SAMLSigningOptions\x12$\n SAML_SIGNING_OPTIONS_UNSPECIFIED\x10\x00\x12\x0e\n\nNO_SIGNING\x10\x01\x12\x1e\n\x1aSAML_ONLY_RESPONSE_SIGNING\x10\x02\x12\x1f\n\x1bSAML_ONLY_ASSERTION_SIGNING\x10\x03\x12#\n\x1fSAML_RESPONSE_ASSERTION_SIGNING\x10\x04*S\n\x0eRequestBinding\x12\x1f\n\x1bREQUEST_BINDING_UNSPECIFIED\x10\x00\x12\r\n\tHTTP_POST\x10\x01\x12\x11\n\rHTTP_REDIRECT\x10\x02*P\n\rTokenAuthType\x12\x1f\n\x1bTOKEN_AUTH_TYPE_UNSPECIFIED\x10\x00\x12\x0e\n\nURL_PARAMS\x10\x01\x12\x0e\n\nBASIC_AUTH\x10\x02*c\n\tOIDCScope\x12\x1a\n\x16OIDC_SCOPE_UNSPECIFIED\x10\x00\x12\n\n\x06openid\x10\x01\x12\x0b\n\x07profile\x10\x02\x12\t\n\x05\x65mail\x10\x03\x12\x0b\n\x07\x61\x64\x64ress\x10\x04\x12\t\n\x05phone\x10\x05*?\n\x0e\x43onnectionType\x12\x0b\n\x07INVALID\x10\x00\x12\x08\n\x04OIDC\x10\x01\x12\x08\n\x04SAML\x10\x02\x12\x0c\n\x08PASSWORD\x10\x03*`\n\x10\x43onnectionStatus\x12!\n\x1d\x43ONNECTION_STATUS_UNSPECIFIED\x10\x00\x12\t\n\x05\x44RAFT\x10\x01\x12\x0f\n\x0bIN_PROGRESS\x10\x02\x12\r\n\tCOMPLETED\x10\x03*\xa8\x01\n\x12\x43onnectionProvider\x12#\n\x1f\x43ONNECTION_PROVIDER_UNSPECIFIED\x10\x00\x12\x08\n\x04OKTA\x10\x01\x12\n\n\x06GOOGLE\x10\x02\x12\x10\n\x0cMICROSOFT_AD\x10\x03\x12\t\n\x05\x41UTH0\x10\x04\x12\x0c\n\x08ONELOGIN\x10\x05\x12\x11\n\rPING_IDENTITY\x10\x06\x12\r\n\tJUMPCLOUD\x10\x07\x12\n\n\x06\x43USTOM\x10\x08\x32\xf1\x0e\n\x11\x43onnectionService\x12\xfa\x01\n\x10\x43reateConnection\x12\x30.scalekit.v1.connections.CreateConnectionRequest\x1a\x31.scalekit.v1.connections.CreateConnectionResponse\"\x80\x01\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02t\"3/api/v1/organizations/{organization_id}/connections:\nconnectionZ1\"#/api/v1/organizations/-/connections:\nconnection\x12\xe2\x01\n\rGetConnection\x12-.scalekit.v1.connections.GetConnectionRequest\x1a..scalekit.v1.connections.GetConnectionResponse\"r\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02\x66\x12\x38/api/v1/organizations/{organization_id}/connections/{id}Z*\x12(/api/v1/organizations/-/connections/{id}\x12\xde\x01\n\x0fListConnections\x12/.scalekit.v1.connections.ListConnectionsRequest\x1a\x30.scalekit.v1.connections.ListConnectionsResponse\"h\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02\\\x12\x33/api/v1/organizations/{organization_id}/connectionsZ%\x12#/api/v1/organizations/-/connections\x12\x84\x02\n\x10UpdateConnection\x12\x30.scalekit.v1.connections.UpdateConnectionRequest\x1a\x31.scalekit.v1.connections.UpdateConnectionResponse\"\x8a\x01\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02~28/api/v1/organizations/{organization_id}/connections/{id}:\nconnectionZ62(/api/v1/organizations/-/connections/{id}:\nconnection\x12\xd0\x01\n\x10\x44\x65leteConnection\x12\x30.scalekit.v1.connections.DeleteConnectionRequest\x1a\x16.google.protobuf.Empty\"r\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02\x66*8/api/v1/organizations/{organization_id}/connections/{id}Z**(/api/v1/organizations/-/connections/{id}\x12\xc0\x01\n\x15GetConnectionByDomain\x12\x35.scalekit.v1.connections.GetConnectionByDomainRequest\x1a\x36.scalekit.v1.connections.GetConnectionByDomainResponse\"8\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02,\x12*/api/v1/organizations/-/connections:search\x12\xfa\x01\n\x10\x45nableConnection\x12\x30.scalekit.v1.connections.EnableConnectionRequest\x1a\x31.scalekit.v1.connections.ToggleConnectionResponse\"\x80\x01\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02t2?/api/v1/organizations/{organization_id}/connections/{id}:enableZ12//api/v1/organizations/-/connections/{id}:enable\x12\xfe\x01\n\x11\x44isableConnection\x12\x31.scalekit.v1.connections.DisableConnectionRequest\x1a\x31.scalekit.v1.connections.ToggleConnectionResponse\"\x82\x01\x82\xb5\x18\x02\x18\x34\x82\xd3\xe4\x93\x02v2@/api/v1/organizations/{organization_id}/connections/{id}:disableZ220/api/v1/organizations/-/connections/{id}:disableB?Z=github.com/scalekit_sdk-inc/scalekit_sdk/pkg/grpc/connectionsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'scalekit.v1.connections.connections_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/scalekit_sdk-inc/scalekit_sdk/pkg/grpc/connections'
  _globals['_CREATECONNECTIONREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_CREATECONNECTIONREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_CREATECONNECTIONREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_CREATECONNECTIONREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_CREATECONNECTIONREQUEST'].fields_by_name['connection']._loaded_options = None
  _globals['_CREATECONNECTIONREQUEST'].fields_by_name['connection']._serialized_options = b'\272H\003\310\001\001'
  _globals['_CREATECONNECTION'].fields_by_name['provider']._loaded_options = None
  _globals['_CREATECONNECTION'].fields_by_name['provider']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_CREATECONNECTION'].fields_by_name['type']._loaded_options = None
  _globals['_CREATECONNECTION'].fields_by_name['type']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_CONNECTION_ATTRIBUTEMAPPINGENTRY']._loaded_options = None
  _globals['_CONNECTION_ATTRIBUTEMAPPINGENTRY']._serialized_options = b'8\001'
  _globals['_CONNECTION'].fields_by_name['attribute_mapping']._loaded_options = None
  _globals['_CONNECTION'].fields_by_name['attribute_mapping']._serialized_options = b'\272H\026\232\001\023\020\n\"\006r\004\020\001\030\031*\007r\005\020\001\030\200\002'
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['connection']._loaded_options = None
  _globals['_UPDATECONNECTIONREQUEST'].fields_by_name['connection']._serialized_options = b'\272H\003\310\001\001'
  _globals['_UPDATECONNECTION_ATTRIBUTEMAPPINGENTRY']._loaded_options = None
  _globals['_UPDATECONNECTION_ATTRIBUTEMAPPINGENTRY']._serialized_options = b'8\001'
  _globals['_UPDATECONNECTION'].fields_by_name['provider']._loaded_options = None
  _globals['_UPDATECONNECTION'].fields_by_name['provider']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_UPDATECONNECTION'].fields_by_name['type']._loaded_options = None
  _globals['_UPDATECONNECTION'].fields_by_name['type']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_UPDATECONNECTION'].fields_by_name['configuration_type']._loaded_options = None
  _globals['_UPDATECONNECTION'].fields_by_name['configuration_type']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_UPDATECONNECTION'].fields_by_name['attribute_mapping']._loaded_options = None
  _globals['_UPDATECONNECTION'].fields_by_name['attribute_mapping']._serialized_options = b'\272H\026\232\001\023\020\n\"\006r\004\020\001\030\031*\007r\005\020\001\030\200\002'
  _globals['_DELETECONNECTIONREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_DELETECONNECTIONREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DELETECONNECTIONREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_DELETECONNECTIONREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DELETECONNECTIONREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_DELETECONNECTIONREQUEST'].fields_by_name['id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_GETCONNECTIONREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_GETCONNECTIONREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_GETCONNECTIONREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_GETCONNECTIONREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_GETCONNECTIONREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_GETCONNECTIONREQUEST'].fields_by_name['id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_LISTCONNECTIONSREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_LISTCONNECTIONSREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_LISTCONNECTIONSREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_LISTCONNECTIONSREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_ENABLECONNECTIONREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_ENABLECONNECTIONREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_ENABLECONNECTIONREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_ENABLECONNECTIONREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_ENABLECONNECTIONREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_ENABLECONNECTIONREQUEST'].fields_by_name['id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DISABLECONNECTIONREQUEST'].fields_by_name['organization_id']._loaded_options = None
  _globals['_DISABLECONNECTIONREQUEST'].fields_by_name['organization_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DISABLECONNECTIONREQUEST'].fields_by_name['external_id']._loaded_options = None
  _globals['_DISABLECONNECTIONREQUEST'].fields_by_name['external_id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_DISABLECONNECTIONREQUEST'].fields_by_name['id']._loaded_options = None
  _globals['_DISABLECONNECTIONREQUEST'].fields_by_name['id']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_GETCONNECTIONBYDOMAINREQUEST'].fields_by_name['domain']._loaded_options = None
  _globals['_GETCONNECTIONBYDOMAINREQUEST'].fields_by_name['domain']._serialized_options = b'\272H\006r\004\020\001\030 '
  _globals['_OIDCMETADATAREQUEST'].fields_by_name['issuer']._loaded_options = None
  _globals['_OIDCMETADATAREQUEST'].fields_by_name['issuer']._serialized_options = b'\272H\007r\005\020\001\030\310\001'
  _globals['_SAMLMETADATAREQUEST'].fields_by_name['metadata_url']._loaded_options = None
  _globals['_SAMLMETADATAREQUEST'].fields_by_name['metadata_url']._serialized_options = b'\272H\007r\005\020\001\030\310\001'
  _globals['_SAMLCERTIFICATEREQUEST'].fields_by_name['text']._loaded_options = None
  _globals['_SAMLCERTIFICATEREQUEST'].fields_by_name['text']._serialized_options = b'\272H\004r\002\020\001'
  _globals['_CONNECTIONSERVICE'].methods_by_name['CreateConnection']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['CreateConnection']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002t\"3/api/v1/organizations/{organization_id}/connections:\nconnectionZ1\"#/api/v1/organizations/-/connections:\nconnection'
  _globals['_CONNECTIONSERVICE'].methods_by_name['GetConnection']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['GetConnection']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002f\0228/api/v1/organizations/{organization_id}/connections/{id}Z*\022(/api/v1/organizations/-/connections/{id}'
  _globals['_CONNECTIONSERVICE'].methods_by_name['ListConnections']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['ListConnections']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002\\\0223/api/v1/organizations/{organization_id}/connectionsZ%\022#/api/v1/organizations/-/connections'
  _globals['_CONNECTIONSERVICE'].methods_by_name['UpdateConnection']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['UpdateConnection']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002~28/api/v1/organizations/{organization_id}/connections/{id}:\nconnectionZ62(/api/v1/organizations/-/connections/{id}:\nconnection'
  _globals['_CONNECTIONSERVICE'].methods_by_name['DeleteConnection']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['DeleteConnection']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002f*8/api/v1/organizations/{organization_id}/connections/{id}Z**(/api/v1/organizations/-/connections/{id}'
  _globals['_CONNECTIONSERVICE'].methods_by_name['GetConnectionByDomain']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['GetConnectionByDomain']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002,\022*/api/v1/organizations/-/connections:search'
  _globals['_CONNECTIONSERVICE'].methods_by_name['EnableConnection']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['EnableConnection']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002t2?/api/v1/organizations/{organization_id}/connections/{id}:enableZ12//api/v1/organizations/-/connections/{id}:enable'
  _globals['_CONNECTIONSERVICE'].methods_by_name['DisableConnection']._loaded_options = None
  _globals['_CONNECTIONSERVICE'].methods_by_name['DisableConnection']._serialized_options = b'\202\265\030\002\0304\202\323\344\223\002v2@/api/v1/organizations/{organization_id}/connections/{id}:disableZ220/api/v1/organizations/-/connections/{id}:disable'
  _globals['_CONFIGURATIONTYPE']._serialized_start=9530
  _globals['_CONFIGURATIONTYPE']._serialized_end=9612
  _globals['_NAMEIDFORMAT']._serialized_start=9614
  _globals['_NAMEIDFORMAT']._serialized_end=9711
  _globals['_SAMLSIGNINGOPTIONS']._serialized_start=9714
  _globals['_SAMLSIGNINGOPTIONS']._serialized_end=9890
  _globals['_REQUESTBINDING']._serialized_start=9892
  _globals['_REQUESTBINDING']._serialized_end=9975
  _globals['_TOKENAUTHTYPE']._serialized_start=9977
  _globals['_TOKENAUTHTYPE']._serialized_end=10057
  _globals['_OIDCSCOPE']._serialized_start=10059
  _globals['_OIDCSCOPE']._serialized_end=10158
  _globals['_CONNECTIONTYPE']._serialized_start=10160
  _globals['_CONNECTIONTYPE']._serialized_end=10223
  _globals['_CONNECTIONSTATUS']._serialized_start=10225
  _globals['_CONNECTIONSTATUS']._serialized_end=10321
  _globals['_CONNECTIONPROVIDER']._serialized_start=10324
  _globals['_CONNECTIONPROVIDER']._serialized_end=10492
  _globals['_CREATECONNECTIONREQUEST']._serialized_start=327
  _globals['_CREATECONNECTIONREQUEST']._serialized_end=549
  _globals['_CREATECONNECTION']._serialized_start=552
  _globals['_CREATECONNECTION']._serialized_end=724
  _globals['_CONNECTION']._serialized_start=727
  _globals['_CONNECTION']._serialized_end=1705
  _globals['_CONNECTION_ATTRIBUTEMAPPINGENTRY']._serialized_start=1626
  _globals['_CONNECTION_ATTRIBUTEMAPPINGENTRY']._serialized_end=1693
  _globals['_CREATECONNECTIONRESPONSE']._serialized_start=1707
  _globals['_CREATECONNECTIONRESPONSE']._serialized_end=1802
  _globals['_UPDATECONNECTIONREQUEST']._serialized_start=1805
  _globals['_UPDATECONNECTIONREQUEST']._serialized_end=2054
  _globals['_UPDATECONNECTION']._serialized_start=2057
  _globals['_UPDATECONNECTION']._serialized_end=2916
  _globals['_UPDATECONNECTION_ATTRIBUTEMAPPINGENTRY']._serialized_start=1626
  _globals['_UPDATECONNECTION_ATTRIBUTEMAPPINGENTRY']._serialized_end=1693
  _globals['_UPDATECONNECTIONRESPONSE']._serialized_start=2918
  _globals['_UPDATECONNECTIONRESPONSE']._serialized_end=3013
  _globals['_DELETECONNECTIONREQUEST']._serialized_start=3016
  _globals['_DELETECONNECTIONREQUEST']._serialized_end=3182
  _globals['_GETCONNECTIONREQUEST']._serialized_start=3185
  _globals['_GETCONNECTIONREQUEST']._serialized_end=3348
  _globals['_GETCONNECTIONRESPONSE']._serialized_start=3350
  _globals['_GETCONNECTIONRESPONSE']._serialized_end=3442
  _globals['_LISTCONNECTIONSREQUEST']._serialized_start=3445
  _globals['_LISTCONNECTIONSREQUEST']._serialized_end=3626
  _globals['_LISTCONNECTIONSRESPONSE']._serialized_start=3628
  _globals['_LISTCONNECTIONSRESPONSE']._serialized_end=3728
  _globals['_LISTCONNECTION']._serialized_start=3731
  _globals['_LISTCONNECTION']._serialized_end=4071
  _globals['_ENABLECONNECTIONREQUEST']._serialized_start=4074
  _globals['_ENABLECONNECTIONREQUEST']._serialized_end=4240
  _globals['_DISABLECONNECTIONREQUEST']._serialized_start=4243
  _globals['_DISABLECONNECTIONREQUEST']._serialized_end=4410
  _globals['_TOGGLECONNECTIONRESPONSE']._serialized_start=4412
  _globals['_TOGGLECONNECTIONRESPONSE']._serialized_end=4524
  _globals['_OIDCCONNECTIONCONFIG']._serialized_start=4527
  _globals['_OIDCCONNECTIONCONFIG']._serialized_end=5293
  _globals['_SAMLCONNECTIONCONFIGREQUEST']._serialized_start=5296
  _globals['_SAMLCONNECTIONCONFIGREQUEST']._serialized_end=6464
  _globals['_SAMLCONNECTIONCONFIGRESPONSE']._serialized_start=6467
  _globals['_SAMLCONNECTIONCONFIGRESPONSE']._serialized_end=7779
  _globals['_IDPCERTIFICATE']._serialized_start=7782
  _globals['_IDPCERTIFICATE']._serialized_end=7994
  _globals['_GETCONNECTIONBYDOMAINREQUEST']._serialized_start=7996
  _globals['_GETCONNECTIONBYDOMAINREQUEST']._serialized_end=8061
  _globals['_GETCONNECTIONBYDOMAINRESPONSE']._serialized_start=8064
  _globals['_GETCONNECTIONBYDOMAINRESPONSE']._serialized_end=8300
  _globals['_GETOIDCMETADATAREQUEST']._serialized_start=8302
  _globals['_GETOIDCMETADATAREQUEST']._serialized_end=8400
  _globals['_OIDCMETADATAREQUEST']._serialized_start=8402
  _globals['_OIDCMETADATAREQUEST']._serialized_end=8459
  _globals['_GETOIDCMETADATARESPONSE']._serialized_start=8462
  _globals['_GETOIDCMETADATARESPONSE']._serialized_end=8677
  _globals['_GETSAMLMETADATAREQUEST']._serialized_start=8679
  _globals['_GETSAMLMETADATAREQUEST']._serialized_end=8777
  _globals['_SAMLMETADATAREQUEST']._serialized_start=8779
  _globals['_SAMLMETADATAREQUEST']._serialized_end=8847
  _globals['_GETSAMLMETADATARESPONSE']._serialized_start=8850
  _globals['_GETSAMLMETADATARESPONSE']._serialized_end=9158
  _globals['_GETSAMLCERTIFICATEDETAILSREQUEST']._serialized_start=9160
  _globals['_GETSAMLCERTIFICATEDETAILSREQUEST']._serialized_end=9277
  _globals['_SAMLCERTIFICATEREQUEST']._serialized_start=9279
  _globals['_SAMLCERTIFICATEREQUEST']._serialized_end=9332
  _globals['_GETSAMLCERTIFICATEDETAILSRESPONSE']._serialized_start=9335
  _globals['_GETSAMLCERTIFICATEDETAILSRESPONSE']._serialized_end=9500
  _globals['_PASSWORDCONNECTIONCONFIG']._serialized_start=9502
  _globals['_PASSWORDCONNECTIONCONFIG']._serialized_end=9528
  _globals['_CONNECTIONSERVICE']._serialized_start=10495
  _globals['_CONNECTIONSERVICE']._serialized_end=12400
# @@protoc_insertion_point(module_scope)

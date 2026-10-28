"""Offline tests for client.actions connection methods: the gRPC layer is stubbed, no environment needed."""
import unittest
from unittest.mock import MagicMock

from google.protobuf.empty_pb2 import Empty

from scalekit.actions.actions import ActionClient
from scalekit.actions.connections import (
    AuthMode, GoogleDWDSettings, OAuthSettings, OptionalScopes, ProviderConfigurations,
    TokenEndpointAuthMethod, errors,
)
from scalekit.common.exceptions import (
    ScalekitBadRequestException, ScalekitNotFoundException, ScalekitServiceUnavailableException,
)
from scalekit.v1.connections import connections_pb2 as pb


def _app_connection(**kw) -> pb.AppConnection:
    conn = pb.AppConnection(id=kw.pop("id", "conn_1"), provider="GMAIL", connection_name="gmail-work",
                            type=pb.ConnectionType.OAUTH, auth_mode=pb.ConnectionAuthMode.USER)
    conn.oauth_config.scopes.extend(["a", "b"])
    return conn


def _server_error(cls, message, code=""):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


class ConnectionMethodsTest(unittest.TestCase):
    def setUp(self):
        self.core = MagicMock()
        self.client = ActionClient(MagicMock(core_client=self.core), MagicMock())
        self.calls = []

    def _reply(self, *responses):
        """Queue (response, call) tuples; exceptions are raised."""
        queue = list(responses)

        def grpc_exec(rpc, request, **kwargs):
            self.calls.append((rpc, request, kwargs))
            item = queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return (item, None)

        self.core.grpc_exec.side_effect = grpc_exec

    # -- create / get / list ------------------------------------------------

    def test_create_sends_only_given_fields_and_is_not_retried(self):
        self._reply(pb.CreateAppConnectionResponse(connection=_app_connection()))
        result = self.client.create_connection(" gmail ", connection_name="gmail-work", auth_mode=AuthMode.ORG_WIDE)
        _, request, kwargs = self.calls[0]
        self.assertEqual(request.connection.provider, "gmail")
        self.assertEqual(request.connection.auth_mode, pb.ConnectionAuthMode.ORG_WIDE)
        self.assertFalse(request.connection.HasField("provider_configurations"))
        self.assertFalse(kwargs["retry_on_unavailable"])
        self.assertEqual((result.id, result.provider, result.type), ("conn_1", "GMAIL", "OAUTH"))

    def test_create_with_provider_domain(self):
        self._reply(pb.CreateAppConnectionResponse(connection=_app_connection()))
        self.client.create_connection("MIXPANELMCP", provider_domain="mcp-eu.mixpanel.com")
        self.assertEqual(self.calls[0][1].connection.provider_configurations.provider_domain, "mcp-eu.mixpanel.com")

    def test_create_requires_provider(self):
        with self.assertRaises(ValueError):
            self.client.create_connection("  ")

    def test_get_by_name_or_id_uses_one_identifier(self):
        self._reply(pb.GetAppConnectionResponse(connection=_app_connection()),
                    pb.GetAppConnectionResponse(connection=_app_connection()))
        self.client.get_connection("Gmail-Work")
        self.client.get_connection(connection_id="conn_123")
        self.assertEqual(self.calls[0][1].connection_identifier, "Gmail-Work")
        self.assertEqual(self.calls[1][1].connection_identifier, "conn_123")

    def test_list_passes_filters(self):
        summary = pb.AppConnectionSummary(id="conn_1", connection_name="x", provider="GMAIL",
                                          type=pb.ConnectionType.OAUTH, auth_mode=pb.ConnectionAuthMode.USER)
        self._reply(pb.ListAppConnectionSummariesResponse(connections=[summary], next_page_token="n", total_size=7))
        result = self.client.list_app_connections(provider="gmail", query="mail", page_size=5)
        request = self.calls[0][1]
        self.assertEqual((request.provider, request.query, request.page_size), ("gmail", "mail", 5))
        self.assertEqual((result.total_size, result.next_page_token, result.connections[0].provider), (7, "n", "GMAIL"))

    # -- update ---------------------------------------------------------------

    def test_update_by_id_sends_partial_body_and_no_mask(self):
        self._reply(pb.UpdateAppConnectionResponse(connection=_app_connection()))
        self.client.update_connection(connection_id="conn_9", oauth=OAuthSettings(
            client_id="id", scopes=["a"], token_endpoint_auth_method=TokenEndpointAuthMethod.BASIC_AUTH))
        self.assertEqual(len(self.calls), 1)  # no name lookup
        request = self.calls[0][1]
        self.assertEqual(request.connection_id, "conn_9")
        cfg = request.connection.oauth_config
        self.assertEqual(cfg.client_id.value, "id")
        self.assertFalse(cfg.HasField("client_secret"))
        self.assertFalse(cfg.HasField("use_scalekit_creds"))
        self.assertEqual(list(cfg.scopes), ["a"])
        self.assertEqual(cfg.token_endpoint_auth_method, pb.AppOAuthConfig.BASIC_AUTH)
        self.assertEqual(list(request.update_mask.paths), [])

    def test_update_by_name_resolves_id_first(self):
        self._reply(pb.GetAppConnectionResponse(connection=_app_connection(id="conn_42")),
                    pb.UpdateAppConnectionResponse(connection=_app_connection(id="conn_42")))
        self.client.update_connection("gmail-work", oauth=OAuthSettings(use_scalekit_creds=True))
        self.assertEqual(self.calls[0][1].connection_identifier, "gmail-work")
        self.assertEqual(self.calls[1][1].connection_id, "conn_42")
        self.assertTrue(self.calls[1][1].connection.oauth_config.use_scalekit_creds.value)

    def test_empty_lists_and_maps_are_named_in_update_mask(self):
        self._reply(pb.UpdateAppConnectionResponse(connection=_app_connection()))
        self.client.update_connection(connection_id="conn_9", oauth=OAuthSettings(
            scopes=[], required_scopes=[], required_optional_scopes=[], extra_authorize_params={},
            optional_scopes=OptionalScopes(scopes=[]), prompt=""))
        request = self.calls[0][1]
        self.assertEqual(set(request.update_mask.paths), {
            "oauth_config.scopes", "oauth_config.required_scopes", "oauth_config.required_optional_scopes",
            "oauth_config.extra_authorize_params", "oauth_config.optional_scopes.scopes"})
        self.assertTrue(request.connection.oauth_config.HasField("prompt"))  # "" is sent, not dropped

    def test_dwd_clear_and_provider_configurations_and_rename(self):
        self._reply(pb.UpdateAppConnectionResponse(connection=_app_connection()))
        self.client.update_connection(connection_id="conn_9", new_connection_name="renamed",
                                      google_dwd=GoogleDWDSettings(required_scopes=[]))
        request = self.calls[0][1]
        self.assertEqual(list(request.update_mask.paths), ["google_dwd_config.required_scopes"])
        self.assertEqual(request.connection.connection_name, "renamed")

        self.calls.clear()
        self._reply(pb.UpdateAppConnectionResponse(connection=_app_connection()))
        self.client.update_connection(connection_id="conn_9", oauth=OAuthSettings(client_id="x"),
                                      provider_configurations=ProviderConfigurations(slack_connection_type="BOT"))
        self.assertEqual(self.calls[0][1].connection.provider_configurations.slack_connection_type, "BOT")

    def test_provider_domain_on_update_is_sent_so_the_server_refuses_it(self):
        self._reply(_server_error(ScalekitBadRequestException,
                                  "provider_configurations.provider_domain cannot be changed after the connection is created",
                                  "INVALID_ARGUMENT"))
        with self.assertRaises(errors.InvalidConfigurationError) as ctx:
            self.client.update_connection(connection_id="conn_9",
                                          provider_configurations=ProviderConfigurations(provider_domain="eu.example.com"))
        self.assertEqual(self.calls[0][1].connection.provider_configurations.provider_domain, "eu.example.com")
        self.assertIn("cannot be changed", ctx.exception.message)

    def test_update_validates_before_sending(self):
        with self.assertRaises(errors.InvalidConfigurationError):
            self.client.update_connection(connection_id="conn_9")
        with self.assertRaises(errors.InvalidConfigurationError):
            self.client.update_connection(connection_id="conn_9", oauth=OAuthSettings(), google_dwd=GoogleDWDSettings(scopes=["x"]))
        with self.assertRaises(errors.InvalidConnectionIdError):
            self.client.update_connection(connection_id="gmail", oauth=OAuthSettings(client_id="x"))
        with self.assertRaises(ValueError):
            self.client.update_connection("a", connection_id="conn_1", oauth=OAuthSettings(client_id="x"))
        self.assertEqual(self.calls, [])

    def test_unknown_setting_name_is_rejected(self):
        with self.assertRaises(Exception):
            OAuthSettings(use_platform_creds=True)

    # -- enable / disable / delete -------------------------------------------

    def test_delete_uses_the_environment_rpc_and_is_not_retried(self):
        self._reply(Empty())
        self.assertIsNone(self.client.delete_connection(connection_id="conn_5"))
        self.assertEqual(self.calls[0][1].connection_id, "conn_5")
        self.assertFalse(self.calls[0][2]["retry_on_unavailable"])

    # -- error mapping ----------------------------------------------------------

    def _expect(self, exc, error_type, call):
        self._reply(exc)
        with self.assertRaises(error_type) as ctx:
            call()
        self.assertIs(ctx.exception.cause, exc)
        return ctx.exception

    def test_validation_error_message_includes_field_violations(self):
        from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo
        info = ErrorInfo(error_code="INVALID_ARGUMENT")
        violation = info.validation_error_info.field_violations.add()
        violation.field = "connection.provider_configurations.slack_connection_type"
        violation.description = "must be in list [BOT, USER]"
        exc = _server_error(ScalekitBadRequestException, "Validation error", "INVALID_ARGUMENT")
        exc._unpacked_details = [info]
        err = self._expect(exc, errors.InvalidConfigurationError, lambda: self.client.create_connection("x"))
        self.assertIn("provider_configurations.slack_connection_type: must be in list [BOT, USER]", err.message)
        self.assertNotIn("connection.provider_configurations", err.message)

    def test_error_mapping(self):
        create = lambda: self.client.create_connection("x")
        self._expect(_server_error(ScalekitBadRequestException, 'connection_name "x" is already used', "DUPLICATE_IDENTIFIER"),
                     errors.ConnectionNameConflictError, create)
        self._expect(_server_error(ScalekitBadRequestException, 'connector "x" not found; use an identifier from the list'),
                     errors.ProviderNotFoundError, create)
        self._expect(_server_error(ScalekitBadRequestException, 'connector "x" has several auth types configured.'),
                     errors.AmbiguousAuthTypeError, create)
        self._expect(_server_error(ScalekitBadRequestException, "provider is required"),
                     errors.InvalidConfigurationError, create)
        err = self._expect(_server_error(ScalekitServiceUnavailableException, "unavailable"),
                           errors.OutcomeUnknownError, create)
        self.assertEqual(err.step, "create")
        self._expect(_server_error(ScalekitNotFoundException, "connection not found"),
                     errors.ConnectionNotFoundError, lambda: self.client.get_connection("nope"))
        err = self._expect(_server_error(ScalekitServiceUnavailableException, "unavailable"),
                           errors.ConnectionUnavailableError, lambda: self.client.get_connection("x"))
        self.assertTrue(err.retryable)
        self._expect(_server_error(ScalekitBadRequestException, "connection has connected accounts"),
                     errors.ConnectionInUseError, lambda: self.client.delete_connection(connection_id="conn_1"))


if __name__ == "__main__":
    unittest.main()

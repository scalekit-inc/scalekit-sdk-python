"""Offline tests for the AgentKit connection settings of custom connectors, set with ``client.actions``: how Scalekit
sends client credentials to the provider's token URL (``OAuthSettings.token_endpoint_auth_method``) and the
create-only ``provider_domain``. The gRPC layer is stubbed; no environment is needed."""
import unittest
from unittest.mock import MagicMock

from pydantic import ValidationError

from scalekit.actions.actions import ActionClient
from scalekit.actions.connections import OAuthSettings, TokenEndpointAuthMethod, errors
from scalekit.common.exceptions import ScalekitBadRequestException
from scalekit.v1.connections import connections_pb2 as pb

METHOD = pb.AppOAuthConfig.TokenEndpointAuthMethod


def _server_error(cls, message, code=""):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


def _app_connection(method=None, **kw) -> pb.AppConnection:
    conn = pb.AppConnection(id=kw.pop("id", "conn_1"), provider=kw.pop("provider", "ACME_MCP:1"),
                            connection_name="acme-mcp", type=pb.ConnectionType.OAUTH,
                            auth_mode=pb.ConnectionAuthMode.USER)
    conn.oauth_config.scopes.extend(["a"])
    if method is not None:
        conn.oauth_config.token_endpoint_auth_method = method
    return conn


class ConnectionTestCase(unittest.TestCase):
    def setUp(self):
        self.core = MagicMock()
        self.client = ActionClient(MagicMock(core_client=self.core), MagicMock())
        self.calls = []

    def _reply(self, *responses):
        """Queue replies for grpc_exec; an exception in the queue is raised."""
        queue = list(responses)

        def grpc_exec(rpc, request, **kwargs):
            self.calls.append((rpc, request, kwargs))
            item = queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return (item, None)

        self.core.grpc_exec.side_effect = grpc_exec

    def _update(self, **oauth):
        self._reply(pb.UpdateAppConnectionResponse(connection=_app_connection()))
        result = self.client.update_connection(connection_id="conn_9", oauth=OAuthSettings(**oauth))
        return self.calls[-1][1], result


class TokenEndpointAuthMethodTest(ConnectionTestCase):
    def test_each_value_is_sent_as_the_enum_of_the_agentkit_api(self):
        for member in TokenEndpointAuthMethod:
            with self.subTest(member.name):
                request, _ = self._update(token_endpoint_auth_method=member)
                cfg = request.connection.oauth_config
                self.assertEqual(request.connection_id, "conn_9")
                self.assertTrue(cfg.HasField("token_endpoint_auth_method"))
                self.assertEqual(cfg.token_endpoint_auth_method, METHOD.Value(member.value))
                self.assertNotEqual(cfg.token_endpoint_auth_method, METHOD.Value("TOKEN_ENDPOINT_AUTH_METHOD_UNSPECIFIED"))

    def test_leaving_it_out_is_different_from_choosing_default(self):
        """Left out, the stored value is kept; DEFAULT is a value of its own that clears it."""
        omitted, _ = self._update(client_id="id")
        self.assertFalse(omitted.connection.oauth_config.HasField("token_endpoint_auth_method"))
        chosen, _ = self._update(token_endpoint_auth_method=TokenEndpointAuthMethod.DEFAULT)
        self.assertTrue(chosen.connection.oauth_config.HasField("token_endpoint_auth_method"))
        self.assertEqual(chosen.connection.oauth_config.token_endpoint_auth_method, METHOD.DEFAULT)

    def test_it_is_set_by_name_not_by_the_text_of_the_token_request(self):
        """The AgentKit API takes the names NONE, BASIC_AUTH, REQUEST_BODY and DEFAULT; the OAuth spelling is refused."""
        self.assertIs(OAuthSettings(token_endpoint_auth_method="BASIC_AUTH").token_endpoint_auth_method,
                      TokenEndpointAuthMethod.BASIC_AUTH)
        for spelling in ("client_secret_basic", "client_secret_post", "none", "URL_PARAMS", ""):
            with self.subTest(spelling):
                with self.assertRaises(ValidationError):
                    OAuthSettings(token_endpoint_auth_method=spelling)
        self.assertEqual(self.calls, [], "nothing is sent for a value the enum does not have")

    def test_a_read_reports_the_method(self):
        for member in TokenEndpointAuthMethod:
            with self.subTest(member.name):
                self._reply(pb.GetAppConnectionResponse(connection=_app_connection(METHOD.Value(member.value))))
                connection = self.client.get_connection(connection_id="conn_1")
                self.assertIs(connection.oauth.token_endpoint_auth_method, member)

    def test_a_read_without_a_method_has_none(self):
        self._reply(pb.GetAppConnectionResponse(connection=_app_connection()))
        self.assertIsNone(self.client.get_connection(connection_id="conn_1").oauth.token_endpoint_auth_method)

    def test_an_update_returns_the_connection_as_the_server_stored_it(self):
        self._reply(pb.UpdateAppConnectionResponse(connection=_app_connection(METHOD.REQUEST_BODY)))
        result = self.client.update_connection(
            connection_id="conn_9",
            oauth=OAuthSettings(token_endpoint_auth_method=TokenEndpointAuthMethod.REQUEST_BODY),
        )
        self.assertIs(result.oauth.token_endpoint_auth_method, TokenEndpointAuthMethod.REQUEST_BODY)

    def test_a_rejected_value_reaches_the_caller_as_an_agentkit_error(self):
        self._reply(_server_error(ScalekitBadRequestException, "Validation error", "INVALID_ARGUMENT"))
        with self.assertRaises(errors.InvalidConfigurationError):
            self.client.update_connection(
                connection_id="conn_9", oauth=OAuthSettings(token_endpoint_auth_method=TokenEndpointAuthMethod.NONE)
            )
        self.assertEqual(len(self.calls), 1)

    def test_the_enum_has_every_value_of_the_api(self):
        self.assertEqual({m.name for m in TokenEndpointAuthMethod}, {"NONE", "BASIC_AUTH", "REQUEST_BODY", "DEFAULT"})
        for name in ("NONE", "BASIC_AUTH", "REQUEST_BODY", "DEFAULT"):
            self.assertIn(name, METHOD.keys())
            self.assertEqual(TokenEndpointAuthMethod(name).value, name)


class ProviderDomainTest(ConnectionTestCase):
    """``provider_domain`` is how a custom MCP connector's regional host name is given: on create, and only there."""

    def test_the_domain_is_sent_with_the_create_of_a_connection_on_a_custom_connector(self):
        self._reply(pb.CreateAppConnectionResponse(connection=_app_connection()))
        self.client.create_connection("ACME_MCP:1", connection_name="acme-mcp", provider_domain="mcp-eu.example.com")
        _, request, kwargs = self.calls[0]
        self.assertEqual(request.connection.provider, "ACME_MCP:1")
        self.assertEqual(request.connection.connection_name, "acme-mcp")
        self.assertEqual(request.connection.provider_configurations.provider_domain, "mcp-eu.example.com")
        self.assertFalse(kwargs["retry_on_unavailable"], "the first attempt may have created the connection")

    def test_without_it_no_provider_configurations_are_sent(self):
        self._reply(pb.CreateAppConnectionResponse(connection=_app_connection()))
        self.client.create_connection("ACME_MCP:1")
        self.assertFalse(self.calls[0][1].connection.HasField("provider_configurations"))

    def test_it_is_never_returned(self):
        conn = _app_connection()
        conn.provider_configurations.provider_domain = "mcp-eu.example.com"
        self._reply(pb.CreateAppConnectionResponse(connection=conn))
        created = self.client.create_connection("ACME_MCP:1", provider_domain="mcp-eu.example.com")
        self.assertIsNone(created.provider_configurations)
        self.assertNotIn("mcp-eu.example.com", created.model_dump_json())


if __name__ == "__main__":
    unittest.main()

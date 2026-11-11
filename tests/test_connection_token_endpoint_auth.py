"""Offline tests for connection settings of custom connectors: the token endpoint auth type and the
templated proxy_url context. The gRPC layer is stubbed; no environment is needed."""
import unittest
from unittest.mock import MagicMock

from google.protobuf import struct_pb2
from google.protobuf.wrappers_pb2 import StringValue

from scalekit.actions.connections import TokenEndpointAuthMethod
from scalekit.common.exceptions import ScalekitBadRequestException
from scalekit.connection import ConnectionClient
from scalekit.v1.connections import connections_pb2 as pb


def _server_error(cls, message, code):
    exc = cls.__new__(cls)
    Exception.__init__(exc, message)
    exc._message = message
    exc._error_code = code
    return exc


class ConnectionTestCase(unittest.TestCase):
    def setUp(self):
        self.core = MagicMock()
        self.calls = []
        self.client = ConnectionClient(self.core)

    def _reply(self, *responses):
        queue = list(responses)

        def grpc_exec(rpc, request, **kwargs):
            self.calls.append((rpc, request, kwargs))
            item = queue.pop(0)
            if isinstance(item, Exception):
                raise item
            return (item, None)

        self.core.grpc_exec.side_effect = grpc_exec


class TokenEndpointAuthTypeTest(ConnectionTestCase):
    def _update(self, **oauth):
        self._reply(pb.UpdateConnectionResponse())
        self.client.update_environment_connection(
            "conn_123", pb.UpdateConnection(oauth_config=pb.OAuthConnectionConfig(**oauth))
        )
        return self.calls[-1][1]

    def test_each_value_is_sent(self):
        for name in ("BASIC_AUTH", "URL_PARAMS", "NONE"):
            with self.subTest(name):
                request = self._update(token_endpoint_auth_type=pb.TokenAuthType.Value(name))
                self.assertEqual(request.connection_id, "conn_123")
                self.assertEqual(request.connection.oauth_config.token_endpoint_auth_type, pb.TokenAuthType.Value(name))

    def test_none_is_the_public_client_value(self):
        self.assertEqual(pb.TokenAuthType.Name(pb.NONE), "NONE")
        self.assertEqual(pb.TokenAuthType.Value("BASIC_AUTH"), pb.BASIC_AUTH)

    def test_leaving_it_out_is_different_from_resetting_it(self):
        """Omitted keeps the stored value; an explicit TOKEN_AUTH_TYPE_UNSPECIFIED resets it to Default."""
        omitted = self._update()
        self.assertFalse(omitted.connection.oauth_config.HasField("token_endpoint_auth_type"))
        reset = self._update(token_endpoint_auth_type=pb.TOKEN_AUTH_TYPE_UNSPECIFIED)
        self.assertTrue(reset.connection.oauth_config.HasField("token_endpoint_auth_type"))
        self.assertEqual(reset.connection.oauth_config.token_endpoint_auth_type, pb.TOKEN_AUTH_TYPE_UNSPECIFIED)

    def test_the_deprecated_string_still_reaches_the_server(self):
        request = self._update(token_endpoint_auth_method=StringValue(value="client_secret_basic"))
        self.assertEqual(request.connection.oauth_config.token_endpoint_auth_method.value, "client_secret_basic")
        self.assertFalse(request.connection.oauth_config.HasField("token_endpoint_auth_type"))

    def test_a_read_without_a_type_has_no_value(self):
        self._reply(pb.GetConnectionResponse(connection=pb.Connection(id="conn_123", oauth_config=pb.OAuthConnectionConfig())))
        response, _ = self.client.get_environment_connection("conn_123")
        self.assertFalse(response.connection.oauth_config.HasField("token_endpoint_auth_type"))

    def test_a_read_with_a_type_reports_it(self):
        self._reply(
            pb.GetConnectionResponse(
                connection=pb.Connection(
                    id="conn_123", oauth_config=pb.OAuthConnectionConfig(token_endpoint_auth_type=pb.TokenAuthType.NONE)
                )
            )
        )
        response, _ = self.client.get_environment_connection("conn_123")
        self.assertEqual(response.connection.oauth_config.token_endpoint_auth_type, pb.TokenAuthType.NONE)

    def test_a_rejected_combination_reaches_the_caller(self):
        self._reply(
            _server_error(ScalekitBadRequestException, "Validation error", "INVALID_ARGUMENT"),
        )
        with self.assertRaises(ScalekitBadRequestException):
            self.client.update_environment_connection(
                "conn_123",
                pb.UpdateConnection(
                    oauth_config=pb.OAuthConnectionConfig(token_endpoint_auth_type=pb.TokenAuthType.NONE)
                ),
            )

    def test_the_agentkit_enum_documents_every_value(self):
        self.assertEqual(
            {member.name for member in TokenEndpointAuthMethod}, {"NONE", "BASIC_AUTH", "REQUEST_BODY", "DEFAULT"}
        )
        for name in ("NONE", "BASIC_AUTH", "REQUEST_BODY", "DEFAULT"):
            self.assertIn(name, pb.AppOAuthConfig.TokenEndpointAuthMethod.keys())


class TemplatedProxyUrlContextTest(ConnectionTestCase):
    def test_the_context_is_sent_with_the_connection(self):
        self._reply(
            pb.CreateConnectionResponse(
                connection=pb.Connection(id="conn_1", resolved_proxy_url="https://mcp-eu.example.com/mcp")
            )
        )
        context = struct_pb2.Struct()
        context.update({"domain": "mcp-eu.example.com"})
        response, _ = self.client.create_environment_connection(
            pb.CreateConnection(
                provider=pb.ConnectionProvider.CUSTOM,
                type=pb.ConnectionType.OAUTH,
                provider_key="ACME_MCP:1",
                key_id="acme-mcp",
                context=context,
            ),
            flags=pb.Flags(is_app=True, is_login=False),
        )
        sent = self.calls[0][1].connection
        self.assertEqual(dict(sent.context.items()), {"domain": "mcp-eu.example.com"})
        self.assertTrue(self.calls[0][1].flags.is_app)
        self.assertEqual(response.connection.resolved_proxy_url, "https://mcp-eu.example.com/mcp")

    def test_a_connection_without_a_template_has_no_resolved_url(self):
        self._reply(pb.GetConnectionResponse(connection=pb.Connection(id="conn_1")))
        response, _ = self.client.get_environment_connection("conn_1")
        self.assertFalse(response.connection.HasField("resolved_proxy_url"))

    def test_a_missing_value_is_a_400_the_caller_can_read(self):
        self._reply(
            _server_error(
                ScalekitBadRequestException,
                "connection context is missing a value required by provider \"ACME_MCP:1\"'s proxy_url template",
                "INVALID_ARGUMENT",
            )
        )
        with self.assertRaises(ScalekitBadRequestException) as ctx:
            self.client.create_environment_connection(pb.CreateConnection(key_id="acme-mcp"))
        self.assertIn("proxy_url template", ctx.exception.message)


if __name__ == "__main__":
    unittest.main()

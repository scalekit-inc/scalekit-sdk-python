"""
Tests that the HTTP calls in CoreClient pass a bounded timeout, and that a
timeout/connection failure raised by requests is translated into the SDK's
own exception hierarchy rather than leaking a raw requests exception past the
SDK's exception boundary — the same contract the Node SDK's
ScalekitGatewayTimeoutException.fromAxiosTimeout enforces for its HTTP path
(SK-1208).

requests has no default timeout, so a black-holed connection would block the
calling thread indefinitely. authenticate() and get_jwks() must pass a
non-None timeout to requests.post / requests.get.
"""
import json
import unittest
from unittest.mock import MagicMock, patch

import requests


def _make_core_client():
    """Return a CoreClient instance with __init__ bypassed (no real network calls)."""
    from scalekit.core import CoreClient
    client = CoreClient.__new__(CoreClient)
    client.access_token = "test-token"
    client.host = "example.com"
    client.env_url = "https://example.com"
    client.client_id = "cid"
    client.client_secret = "csec"
    client.keys = {}
    client.grpc_secure_channel = None
    return client


class TestHttpTimeout(unittest.TestCase):
    def setUp(self):
        self.client = _make_core_client()

    def test_authenticate_passes_timeout_to_requests_post(self):
        """authenticate() must pass a non-None timeout to requests.post."""
        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch("scalekit.core.requests.post", return_value=mock_response) as mock_post:
            self.client.authenticate(data={"grant_type": "client_credentials"})

        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        self.assertIn("timeout", kwargs)
        self.assertIsNotNone(kwargs["timeout"])

    def test_get_jwks_passes_timeout_to_requests_get(self):
        """get_jwks() must pass a non-None timeout to requests.get."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = json.dumps({"keys": []}).encode("utf-8")

        with patch("scalekit.core.requests.get", return_value=mock_response) as mock_get:
            self.client.get_jwks()

        mock_get.assert_called_once()
        _, kwargs = mock_get.call_args
        self.assertIn("timeout", kwargs)
        self.assertIsNotNone(kwargs["timeout"])

    def test_authenticate_accepts_non_200_success_status(self):
        """A strict != 200 check is a footgun: it would misclassify any other
        legitimate 2xx (e.g. 201) as an error. authenticate() must accept the
        whole 2xx range, not just 200."""
        mock_response = MagicMock()
        mock_response.status_code = 201

        with patch("scalekit.core.requests.post", return_value=mock_response):
            result = self.client.authenticate(data={"grant_type": "client_credentials"})

        self.assertIs(result, mock_response)

    def test_get_jwks_accepts_non_200_success_status(self):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = json.dumps({"keys": []}).encode("utf-8")

        with patch("scalekit.core.requests.get", return_value=mock_response):
            self.client.get_jwks()  # must not raise

    def test_authenticate_timeout_raises_gateway_timeout_exception(self):
        """A requests.Timeout from the token endpoint must surface as
        ScalekitGatewayTimeoutException (504/DEADLINE_EXCEEDED), not leak the
        raw requests exception."""
        from grpc import StatusCode
        from scalekit.common.exceptions import ScalekitGatewayTimeoutException

        with patch(
            "scalekit.core.requests.post",
            side_effect=requests.exceptions.ReadTimeout("Read timed out"),
        ):
            with self.assertRaises(ScalekitGatewayTimeoutException) as ctx:
                self.client.authenticate(data={"grant_type": "client_credentials"})

        self.assertEqual(ctx.exception.http_status.value, 504)
        self.assertEqual(ctx.exception.grpc_status, StatusCode.DEADLINE_EXCEEDED)

    def test_get_jwks_timeout_raises_gateway_timeout_exception(self):
        """A requests.Timeout from the JWKS endpoint must surface as
        ScalekitGatewayTimeoutException (504/DEADLINE_EXCEEDED), not leak the
        raw requests exception."""
        from grpc import StatusCode
        from scalekit.common.exceptions import ScalekitGatewayTimeoutException

        with patch(
            "scalekit.core.requests.get",
            side_effect=requests.exceptions.ConnectTimeout("Connect timed out"),
        ):
            with self.assertRaises(ScalekitGatewayTimeoutException) as ctx:
                self.client.get_jwks()

        self.assertEqual(ctx.exception.http_status.value, 504)
        self.assertEqual(ctx.exception.grpc_status, StatusCode.DEADLINE_EXCEEDED)

    def test_authenticate_connection_error_raises_scalekit_exception(self):
        """A non-timeout requests failure (e.g. a reset connection) must still
        raise a ScalekitException, not the raw requests exception."""
        from scalekit.common.exceptions import ScalekitException

        with patch(
            "scalekit.core.requests.post",
            side_effect=requests.exceptions.ConnectionError("Connection reset by peer"),
        ):
            with self.assertRaises(ScalekitException):
                self.client.authenticate(data={"grant_type": "client_credentials"})

    def test_get_jwks_connection_error_raises_scalekit_exception(self):
        from scalekit.common.exceptions import ScalekitException

        with patch(
            "scalekit.core.requests.get",
            side_effect=requests.exceptions.ConnectionError("Connection reset by peer"),
        ):
            with self.assertRaises(ScalekitException):
                self.client.get_jwks()

    def test_get_jwks_non_200_raises_scalekit_server_exception(self):
        """A non-200 JWKS response must not reach json.loads()/["keys"] — that
        path raises a bare KeyError/JSONDecodeError which escapes the SDK's
        exception boundary entirely, the same class of leak
        _as_gateway_timeout_response was added to prevent for timeouts."""
        from scalekit.common.exceptions import ScalekitServerException

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.reason = "INTERNAL_SERVER_ERROR"
        mock_response.text = "internal error"

        with patch("scalekit.core.requests.get", return_value=mock_response):
            with self.assertRaises(ScalekitServerException):
                self.client.get_jwks()


if __name__ == "__main__":
    unittest.main()

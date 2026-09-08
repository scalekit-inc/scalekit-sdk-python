"""
Tests that the HTTP calls in CoreClient pass a bounded timeout.

requests has no default timeout, so a black-holed connection would block the
calling thread indefinitely. authenticate() and get_jwks() must pass a
non-None timeout to requests.post / requests.get.
"""
import json
import unittest
from unittest.mock import MagicMock, patch


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
        mock_response.content = json.dumps({"keys": []}).encode("utf-8")

        with patch("scalekit.core.requests.get", return_value=mock_response) as mock_get:
            self.client.get_jwks()

        mock_get.assert_called_once()
        _, kwargs = mock_get.call_args
        self.assertIn("timeout", kwargs)
        self.assertIsNotNone(kwargs["timeout"])


if __name__ == "__main__":
    unittest.main()

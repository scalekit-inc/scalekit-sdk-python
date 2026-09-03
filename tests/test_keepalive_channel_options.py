"""
Tests for gRPC keepalive channel options in CoreClient.

Covers the runtime escape hatch (keepalive_time_ms=0 disables keepalive) and
the sub-10s validation guard (gRPC clamps values below 10s up to 10s, which
the Scalekit server rejects).

These tests never touch the network: __authenticate_client is mocked and
grpc.secure_channel is mocked, so only the channel-option wiring is exercised.
"""
import unittest
from unittest.mock import patch

from scalekit.core import (
    CoreClient,
    DEFAULT_KEEPALIVE_TIME_MS,
    DEFAULT_KEEPALIVE_TIMEOUT_MS,
)


def _build_client(**kwargs):
    """Construct a CoreClient with auth and channel creation stubbed.

    Returns (client, mock_secure_channel) so tests can assert on the options
    passed to grpc.secure_channel.
    """
    with patch.object(CoreClient, "_CoreClient__authenticate_client"), \
            patch("scalekit.core.grpc.secure_channel") as mock_secure_channel, \
            patch("scalekit.core.grpc.ssl_channel_credentials"), \
            patch("scalekit.core.grpc.access_token_call_credentials"), \
            patch("scalekit.core.grpc.composite_channel_credentials"):
        client = CoreClient(
            env_url="https://example.com",
            client_id="cid",
            client_secret="csec",
            **kwargs,
        )
    return client, mock_secure_channel


class TestKeepaliveChannelOptions(unittest.TestCase):
    def _options_from(self, mock_secure_channel):
        """Extract the options kwarg from the secure_channel call."""
        mock_secure_channel.assert_called_once()
        _, kwargs = mock_secure_channel.call_args
        return kwargs["options"]

    def test_disabled_passes_empty_options(self):
        """keepalive_time_ms=0 must call secure_channel with options=[]."""
        _, mock_secure_channel = _build_client(keepalive_time_ms=0)
        self.assertEqual(self._options_from(mock_secure_channel), [])

    def test_default_construction_includes_all_four_options(self):
        """Default construction must include all four expected option tuples."""
        _, mock_secure_channel = _build_client()
        options = self._options_from(mock_secure_channel)
        self.assertEqual(
            options,
            [
                ('grpc.keepalive_time_ms', DEFAULT_KEEPALIVE_TIME_MS),
                ('grpc.keepalive_timeout_ms', DEFAULT_KEEPALIVE_TIMEOUT_MS),
                ('grpc.keepalive_permit_without_calls', 1),
                ('grpc.http2.max_pings_without_data', 0),
            ],
        )
        # Explicit check on the documented default value.
        self.assertIn(('grpc.keepalive_time_ms', 60000), options)

    def test_below_minimum_raises_value_error(self):
        """keepalive_time_ms below the 30s minimum must raise ValueError."""
        with self.assertRaises(ValueError):
            _build_client(keepalive_time_ms=5000)

    def test_thirty_seconds_boundary_accepted(self):
        """keepalive_time_ms=30000 is the boundary and must be accepted."""
        _, mock_secure_channel = _build_client(keepalive_time_ms=30000)
        options = self._options_from(mock_secure_channel)
        self.assertIn(('grpc.keepalive_time_ms', 30000), options)


if __name__ == "__main__":
    unittest.main()

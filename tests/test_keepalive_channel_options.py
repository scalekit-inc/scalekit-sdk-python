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
    CLIENT_IDLE_TIMEOUT_CEILING_MS,
    CLIENT_IDLE_TIMEOUT_PING_CYCLES,
    _client_idle_timeout_ms_for,
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

    def test_default_construction_includes_all_five_options(self):
        """Default construction must include all five expected option tuples."""
        _, mock_secure_channel = _build_client()
        options = self._options_from(mock_secure_channel)
        self.assertEqual(
            options,
            [
                ('grpc.keepalive_time_ms', DEFAULT_KEEPALIVE_TIME_MS),
                ('grpc.keepalive_timeout_ms', DEFAULT_KEEPALIVE_TIMEOUT_MS),
                ('grpc.keepalive_permit_without_calls', 1),
                ('grpc.http2.max_pings_without_data', 0),
                ('grpc.client_idle_timeout_ms', CLIENT_IDLE_TIMEOUT_CEILING_MS),
            ],
        )
        # Explicit check on the documented default values.
        self.assertIn(('grpc.keepalive_time_ms', 60000), options)
        self.assertIn(('grpc.client_idle_timeout_ms', 240000), options)

    def test_below_minimum_raises_value_error(self):
        """keepalive_time_ms below the 60s minimum must raise ValueError."""
        with self.assertRaises(ValueError):
            _build_client(keepalive_time_ms=5000)

    def test_thirty_seconds_now_raises_value_error(self):
        """keepalive_time_ms=30000 is below the 60s minimum and must raise ValueError."""
        with self.assertRaises(ValueError):
            _build_client(keepalive_time_ms=30000)

    def test_sixty_seconds_boundary_accepted(self):
        """keepalive_time_ms=60000 is the boundary and must be accepted."""
        _, mock_secure_channel = _build_client(keepalive_time_ms=60000)
        options = self._options_from(mock_secure_channel)
        self.assertIn(('grpc.keepalive_time_ms', 60000), options)


class TestClientIdleTimeout(unittest.TestCase):
    """Regression tests for the grpc.client_idle_timeout_ms option — the
    client-side idle-close equivalent of the Go SDK's grpcIdleConnTimeout /
    Node SDK's idleConnectionTimeoutMs, which this SDK previously omitted."""

    # The backend's own grpc.max_connection_idle enforcement (scalekit's
    # cmd/grpc.go, grpcKeepaliveMaxConnectionIdle) — kept here as a literal,
    # not imported, so this test independently pins the actual production
    # value rather than trusting whatever CLIENT_IDLE_TIMEOUT_CEILING_MS
    # happens to be set to.
    _BACKEND_MAX_CONNECTION_IDLE_MS = 5 * 60 * 1000

    def test_ceiling_is_strictly_below_backend_max_connection_idle(self):
        """Landing exactly on (or above) the backend's own bound is a race —
        whichever side's timer fires first wins, and the loser is a request
        written into a socket the other side just closed."""
        self.assertLess(CLIENT_IDLE_TIMEOUT_CEILING_MS, self._BACKEND_MAX_CONNECTION_IDLE_MS)

    def test_derived_value_scales_with_keepalive_time_when_below_ceiling(self):
        small = 1000  # hypothetically below the real MIN_KEEPALIVE_TIME_MS floor, to exercise scaling
        self.assertEqual(
            _client_idle_timeout_ms_for(small),
            small * CLIENT_IDLE_TIMEOUT_PING_CYCLES,
        )

    def test_derived_value_clamps_to_ceiling_at_default_keepalive(self):
        self.assertEqual(
            _client_idle_timeout_ms_for(DEFAULT_KEEPALIVE_TIME_MS),
            CLIENT_IDLE_TIMEOUT_CEILING_MS,
        )

    def test_disabled_keepalive_derives_to_zero(self):
        self.assertEqual(_client_idle_timeout_ms_for(0), 0)

    def test_disabling_keepalive_omits_idle_timeout_option_too(self):
        """keepalive_time_ms=0 must disable BOTH the ping-based and the
        idle-close detection — a partial disable would be a surprising,
        undocumented middle state."""
        _, mock_secure_channel = _build_client(keepalive_time_ms=0)
        mock_secure_channel.assert_called_once()
        _, kwargs = mock_secure_channel.call_args
        options = kwargs["options"]
        self.assertEqual(options, [])
        self.assertNotIn(
            "grpc.client_idle_timeout_ms",
            [name for name, _ in options],
        )


if __name__ == "__main__":
    unittest.main()

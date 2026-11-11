"""Offline tests for reading an OAuth pattern back from the server: no environment needed."""
import unittest

from google.protobuf.json_format import MessageToDict

from scalekit.actions.types import AuthPattern, OAuthConfig
from scalekit.providers import _patterns_to_list_value


def _wire(pattern: AuthPattern) -> dict:
    """The pattern as it reaches the server."""
    return MessageToDict(_patterns_to_list_value([pattern]))[0]


class OAuthReadBackTest(unittest.TestCase):
    """The server leaves pkce_enabled out of a pattern when it is false (the key is omitted when empty)."""

    def test_an_absent_pkce_enabled_reads_as_false(self):
        pattern = AuthPattern.from_dict(
            {"type": "OAUTH", "display_name": "OAuth", "oauth_config": {"authorize_uri": "https://a.example.com/auth"}}
        )
        self.assertFalse(pattern.oauth_config.pkce_enabled)

    def test_an_explicit_value_is_kept(self):
        for value in (True, False):
            with self.subTest(value):
                pattern = AuthPattern.from_dict(
                    {"type": "OAUTH", "display_name": "OAuth", "oauth_config": {"pkce_enabled": value}}
                )
                self.assertIs(pattern.oauth_config.pkce_enabled, value)

    def test_authoring_still_defaults_to_pkce_on(self):
        self.assertTrue(OAuthConfig().pkce_enabled)
        self.assertTrue(OAuthConfig().to_dict()["pkce_enabled"])

    def test_a_pattern_read_back_without_pkce_is_never_sent_back_as_true(self):
        """Sending the pattern back unchanged is how an OpenAPI-sourced connector is updated; flipping pkce_enabled
        to true would make the server see a different pattern and refuse the update."""
        stored = {"type": "OAUTH", "display_name": "OAuth", "is_open_api": True, "fields": [], "oauth_config": {}}
        pattern = AuthPattern.from_dict(stored)
        resent = _wire(pattern)
        # Unchanged, it goes back as stored: no pkce_enabled key, which the server reads as false.
        self.assertEqual(resent, stored)
        self.assertNotEqual(resent["oauth_config"].get("pkce_enabled"), True)
        # Once the config is edited it is built from its values, and pkce_enabled is still false.
        pattern.oauth_config.authorize_uri = "https://a.example.com/auth"
        self.assertIs(_wire(pattern)["oauth_config"]["pkce_enabled"], False)


if __name__ == "__main__":
    unittest.main()

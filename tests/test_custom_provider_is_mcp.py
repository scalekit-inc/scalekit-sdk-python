"""Offline tests: ``is_mcp`` on the custom provider requests.

``is_mcp`` can be set on ``CreateCustomProviderRequest`` and
``UpdateCustomProviderRequest``. ``AuthPattern.is_mcp`` is deprecated but still
works and is still sent, so existing calls build the same request they always
did. A request-level value that contradicts the pattern's raises before any
request is made. No test here needs credentials or a network.
"""

import unittest
import warnings
from unittest.mock import MagicMock

from google.protobuf.json_format import MessageToDict
from pydantic import ValidationError

from scalekit.actions.actions import ActionProviders
from scalekit.actions.types import (
    AuthPattern,
    CreateCustomProviderRequest,
    OAuthConfig,
    UpdateCustomProviderRequest,
)
from scalekit.providers import ProvidersClient
from scalekit.v1.providers.providers_pb2 import CreateProviderResponse, UpdateProviderResponse

BASE = {"display_name": "Acme MCP", "proxy_url": "https://mcp.acme.com/mcp"}


def make_pattern(**kwargs) -> AuthPattern:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return AuthPattern(type="OAUTH", display_name="Acme OAuth", oauth_config=OAuthConfig(), **kwargs)


def make_providers():
    """ActionProviders over a real ProvidersClient whose gRPC call is mocked."""
    core = MagicMock()
    core.grpc_exec.return_value = (CreateProviderResponse(), MagicMock())
    return ActionProviders(ProvidersClient(core)), core


def sent_patterns(core) -> list:
    """The auth_patterns the SDK put on the wire, as plain dicts."""
    request = core.grpc_exec.call_args[0][1]
    return MessageToDict(request.provider.auth_patterns)


class QuietDeprecations(unittest.TestCase):
    """Tests that use the deprecated pattern flag on purpose should not print its warning."""

    def setUp(self):
        context = warnings.catch_warnings()
        context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        warnings.simplefilter("ignore", DeprecationWarning)


class TestPatternFlagStillWorks(QuietDeprecations):
    def test_pattern_flag_is_sent_as_before(self):
        providers, core = make_providers()
        request = CreateCustomProviderRequest(**BASE, auth_patterns=[make_pattern(is_mcp=True)])
        providers.create_custom_provider(request)
        self.assertIs(sent_patterns(core)[0]["is_mcp"], True)

    def test_no_flag_sends_no_is_mcp_key(self):
        providers, core = make_providers()
        providers.create_custom_provider(CreateCustomProviderRequest(**BASE, auth_patterns=[make_pattern()]))
        self.assertNotIn("is_mcp", sent_patterns(core)[0])

    def test_update_pattern_flag_is_sent_as_before(self):
        providers, core = make_providers()
        core.grpc_exec.return_value = (UpdateProviderResponse(), MagicMock())
        providers.update_custom_provider(
            UpdateCustomProviderRequest(identifier="ACME:1", **BASE, auth_patterns=[make_pattern(is_mcp=True)])
        )
        self.assertIs(sent_patterns(core)[0]["is_mcp"], True)


class TestRequestLevelIsMcp(QuietDeprecations):
    def test_create_flag_marks_the_pattern_mcp(self):
        providers, core = make_providers()
        providers.create_custom_provider(
            CreateCustomProviderRequest(**BASE, is_mcp=True, auth_patterns=[make_pattern()])
        )
        self.assertIs(sent_patterns(core)[0]["is_mcp"], True)

    def test_create_flag_does_not_change_the_callers_pattern(self):
        providers, _ = make_providers()
        pattern = make_pattern()
        providers.create_custom_provider(CreateCustomProviderRequest(**BASE, is_mcp=True, auth_patterns=[pattern]))
        self.assertFalse(pattern.is_mcp)

    def test_create_false_sends_no_is_mcp_key(self):
        providers, core = make_providers()
        providers.create_custom_provider(
            CreateCustomProviderRequest(**BASE, is_mcp=False, auth_patterns=[make_pattern()])
        )
        self.assertNotIn("is_mcp", sent_patterns(core)[0])

    def test_update_flag_marks_the_pattern_mcp(self):
        providers, core = make_providers()
        core.grpc_exec.return_value = (UpdateProviderResponse(), MagicMock())
        providers.update_custom_provider(
            UpdateCustomProviderRequest(identifier="ACME:1", **BASE, is_mcp=True, auth_patterns=[make_pattern()])
        )
        self.assertIs(sent_patterns(core)[0]["is_mcp"], True)

    def test_flag_defaults_to_none_on_both_requests(self):
        self.assertIsNone(CreateCustomProviderRequest(**BASE).is_mcp)
        self.assertIsNone(UpdateCustomProviderRequest(identifier="ACME:1", **BASE).is_mcp)

    def test_same_value_on_request_and_pattern_is_accepted(self):
        request = CreateCustomProviderRequest(**BASE, is_mcp=True, auth_patterns=[make_pattern(is_mcp=True)])
        self.assertTrue(request.is_mcp)


class TestConflicts(QuietDeprecations):
    def test_false_on_request_with_true_on_pattern(self):
        with self.assertRaises(ValidationError) as ctx:
            CreateCustomProviderRequest(**BASE, is_mcp=False, auth_patterns=[make_pattern(is_mcp=True)])
        message = str(ctx.exception)
        self.assertIn("is_mcp=False on the request conflicts with is_mcp=True on auth_patterns[0]", message)
        self.assertIn("deprecated", message)

    def test_true_on_request_with_explicit_false_on_pattern(self):
        with self.assertRaises(ValidationError) as ctx:
            CreateCustomProviderRequest(**BASE, is_mcp=True, auth_patterns=[make_pattern(is_mcp=False)])
        self.assertIn("is_mcp=True on the request conflicts with is_mcp=False on auth_patterns[0]", str(ctx.exception))

    def test_the_conflicting_pattern_is_named_by_index(self):
        with self.assertRaises(ValidationError):
            UpdateCustomProviderRequest(
                identifier="ACME:1", **BASE, is_mcp=False, auth_patterns=[make_pattern(is_mcp=True)]
            )

    def test_update_flag_needs_auth_patterns(self):
        with self.assertRaises(ValidationError) as ctx:
            UpdateCustomProviderRequest(identifier="ACME:1", **BASE, is_mcp=True)
        self.assertIn("can only be sent together with auth_patterns", str(ctx.exception))

    def test_a_conflict_makes_no_request(self):
        providers, core = make_providers()
        with self.assertRaises(ValidationError):
            providers.create_custom_provider(
                CreateCustomProviderRequest(**BASE, is_mcp=False, auth_patterns=[make_pattern(is_mcp=True)])
            )
        core.grpc_exec.assert_not_called()


class TestPatternFlagDeprecation(unittest.TestCase):
    def deprecations(self, caught):
        return [w for w in caught if issubclass(w.category, DeprecationWarning) and "AuthPattern.is_mcp" in str(w.message)]

    def test_setting_it_on_a_pattern_warns(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            AuthPattern(type="NO_AUTH", display_name="Public", is_mcp=True)
        self.assertEqual(len(self.deprecations(caught)), 1)

    def test_the_warning_points_at_the_callers_code(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            AuthPattern(type="NO_AUTH", display_name="Public", is_mcp=True)
        self.assertEqual(self.deprecations(caught)[0].filename, __file__)

    def test_a_pattern_without_it_does_not_warn(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            AuthPattern(type="NO_AUTH", display_name="Public")
        self.assertEqual(self.deprecations(caught), [])

    def test_the_request_level_flag_does_not_warn(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            providers, _ = make_providers()
            providers.create_custom_provider(
                CreateCustomProviderRequest(
                    **BASE, is_mcp=True, auth_patterns=[AuthPattern(type="NO_AUTH", display_name="Public")]
                )
            )
        self.assertEqual(self.deprecations(caught), [])

    def test_a_pattern_decoded_from_a_response_does_not_warn(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            decoded = AuthPattern.from_dict({"type": "NO_AUTH", "display_name": "Public", "is_mcp": True})
        self.assertEqual(self.deprecations(caught), [])
        self.assertTrue(decoded.is_mcp)


if __name__ == "__main__":
    unittest.main()

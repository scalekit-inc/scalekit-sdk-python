"""Offline tests: ``source`` (``ConnectorSource``) on the custom provider requests.

``source=ConnectorSource.MCP_SERVER`` can be set on ``CreateCustomProviderRequest``
and ``UpdateCustomProviderRequest``; leaving it unset means an API connector.
``AuthPattern.is_mcp`` is deprecated but still works and is still sent, so
existing calls build the same request they always did. A ``source`` that
contradicts the pattern's own flag raises before any request is made. No test
here needs credentials or a network.
"""

import unittest
import warnings
from unittest.mock import MagicMock

from google.protobuf.json_format import MessageToDict
from pydantic import ValidationError

from scalekit.actions.actions import ActionProviders
from scalekit.actions.types import (
    AuthPattern,
    ConnectorSource,
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


class TestRequestLevelSource(QuietDeprecations):
    def test_create_source_marks_the_pattern_mcp(self):
        providers, core = make_providers()
        providers.create_custom_provider(
            CreateCustomProviderRequest(**BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern()])
        )
        self.assertIs(sent_patterns(core)[0]["is_mcp"], True)

    def test_create_source_does_not_change_the_callers_pattern(self):
        providers, _ = make_providers()
        pattern = make_pattern()
        providers.create_custom_provider(
            CreateCustomProviderRequest(**BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[pattern])
        )
        self.assertFalse(pattern.is_mcp)

    def test_no_source_sends_no_is_mcp_key(self):
        providers, core = make_providers()
        providers.create_custom_provider(CreateCustomProviderRequest(**BASE, auth_patterns=[make_pattern()]))
        self.assertNotIn("is_mcp", sent_patterns(core)[0])

    def test_update_source_marks_the_pattern_mcp(self):
        providers, core = make_providers()
        core.grpc_exec.return_value = (UpdateProviderResponse(), MagicMock())
        providers.update_custom_provider(
            UpdateCustomProviderRequest(
                identifier="ACME:1", **BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern()]
            )
        )
        self.assertIs(sent_patterns(core)[0]["is_mcp"], True)

    def test_source_defaults_to_none_on_both_requests(self):
        self.assertIsNone(CreateCustomProviderRequest(**BASE).source)
        self.assertIsNone(UpdateCustomProviderRequest(identifier="ACME:1", **BASE).source)

    def test_mcp_server_on_request_with_the_pattern_flag_also_set_is_accepted(self):
        request = CreateCustomProviderRequest(
            **BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern(is_mcp=True)]
        )
        self.assertEqual(request.source, ConnectorSource.MCP_SERVER)

    def test_the_enum_has_only_mcp_server_for_now(self):
        self.assertEqual([member.name for member in ConnectorSource], ["MCP_SERVER"])

    def test_the_value_can_be_given_as_a_string(self):
        request = CreateCustomProviderRequest(**BASE, source="MCP_SERVER", auth_patterns=[make_pattern()])
        self.assertIs(request.source, ConnectorSource.MCP_SERVER)

    def test_an_unknown_value_is_rejected(self):
        with self.assertRaises(ValidationError):
            CreateCustomProviderRequest(**BASE, source="OPENAPI_SPEC", auth_patterns=[make_pattern()])


class TestConflicts(QuietDeprecations):
    def test_mcp_server_on_request_with_explicit_false_on_pattern(self):
        with self.assertRaises(ValidationError) as ctx:
            CreateCustomProviderRequest(
                **BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern(is_mcp=False)]
            )
        message = str(ctx.exception)
        self.assertIn("source=MCP_SERVER on the request conflicts with is_mcp=False on auth_patterns[0]", message)
        self.assertIn("deprecated", message)

    def test_the_conflicting_pattern_is_named_by_index_on_update(self):
        with self.assertRaises(ValidationError):
            UpdateCustomProviderRequest(
                identifier="ACME:1",
                **BASE,
                source=ConnectorSource.MCP_SERVER,
                auth_patterns=[make_pattern(is_mcp=False)],
            )

    def test_update_source_needs_auth_patterns(self):
        with self.assertRaises(ValidationError) as ctx:
            UpdateCustomProviderRequest(identifier="ACME:1", **BASE, source=ConnectorSource.MCP_SERVER)
        self.assertIn("can only be sent together with auth_patterns", str(ctx.exception))

    def test_a_conflict_makes_no_request(self):
        providers, core = make_providers()
        with self.assertRaises(ValidationError):
            providers.create_custom_provider(
                CreateCustomProviderRequest(
                    **BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern(is_mcp=False)]
                )
            )
        core.grpc_exec.assert_not_called()

    def test_explicit_none_on_update_is_accepted_without_patterns(self):
        request = UpdateCustomProviderRequest(identifier="ACME:1", **BASE, source=None)
        self.assertIsNone(request.source)

    def test_a_conflict_introduced_after_the_request_was_built_is_caught_on_create(self):
        providers, core = make_providers()
        request = CreateCustomProviderRequest(
            **BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern()]
        )
        request.auth_patterns = [make_pattern(is_mcp=False)]
        with self.assertRaises(ValueError) as ctx:
            providers.create_custom_provider(request)
        self.assertIn("conflicts with is_mcp=False on auth_patterns[0]", str(ctx.exception))
        core.grpc_exec.assert_not_called()

    def test_a_pattern_changed_in_place_after_the_request_was_built_is_caught_on_create(self):
        providers, core = make_providers()
        request = CreateCustomProviderRequest(
            **BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern()]
        )
        request.auth_patterns[0].is_mcp = False
        with self.assertRaises(ValueError):
            providers.create_custom_provider(request)
        core.grpc_exec.assert_not_called()

    def test_a_conflict_introduced_after_the_request_was_built_is_caught_on_update(self):
        providers, core = make_providers()
        core.grpc_exec.return_value = (UpdateProviderResponse(), MagicMock())
        request = UpdateCustomProviderRequest(
            identifier="ACME:1", **BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern()]
        )
        request.auth_patterns = [make_pattern(is_mcp=False)]
        with self.assertRaises(ValueError) as ctx:
            providers.update_custom_provider(request)
        self.assertIn("conflicts with is_mcp=False on auth_patterns[0]", str(ctx.exception))
        core.grpc_exec.assert_not_called()

    def test_a_valid_request_is_not_affected_by_the_final_check(self):
        providers, core = make_providers()
        providers.create_custom_provider(
            CreateCustomProviderRequest(**BASE, source=ConnectorSource.MCP_SERVER, auth_patterns=[make_pattern()])
        )
        self.assertIs(sent_patterns(core)[0]["is_mcp"], True)


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

    def test_the_request_level_source_does_not_warn(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            providers, _ = make_providers()
            providers.create_custom_provider(
                CreateCustomProviderRequest(
                    **BASE,
                    source=ConnectorSource.MCP_SERVER,
                    auth_patterns=[AuthPattern(type="NO_AUTH", display_name="Public")],
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

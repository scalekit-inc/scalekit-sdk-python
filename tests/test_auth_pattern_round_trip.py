"""Offline tests: an auth pattern read from the server goes back to it unchanged.

The server rejects a changed auth pattern on an OpenAPI-sourced connector, and decides what
changed by parsing the incoming patterns into its Go structs and comparing them with the stored
ones (reflect.DeepEqual). There a JSON null, an absent key, "" and [] are not all the same value:
"hint" is a *string, "fields", "options", "account_fields" and "allowed_proxy_domains" are
slices, and "oauth_config", "placement" and several OAuth labels are pointers. These tests decode
realistic server dicts, push them through the SDK's wire encoding and check that what arrives is
exactly what was sent, both as a dict and after a Go-style parse. The gRPC layer is stubbed.

The public to_dict() is a different thing: it is the normalised view of the values, as it always
was, and is not what the SDK sends for a pattern it decoded.
"""
import copy
import json
import pickle
import unittest
import warnings
from unittest.mock import MagicMock

from google.protobuf.json_format import MessageToDict, ParseDict

from scalekit.actions.actions import ActionClient
from scalekit.actions.types import (
    AuthField,
    AuthFieldOption,
    AuthPattern,
    CredentialPlacement,
    OAuthConfig,
    Provider,
    UpdateCustomProviderRequest,
)
from scalekit.providers import ProvidersClient, _patterns_to_list_value
from scalekit.v1.providers import providers_pb2 as pb


# --- What the server stores and returns ---------------------------------------------------
#
# Responses carry json.Marshal of the stored []db.AuthPattern: "description", "fields", "hint",
# "label", "input_type" and "required" are always present ("fields" and "hint" may be null),
# the omitempty keys only when set. The dashboard stores "hint": "" on every field.

def _token_field(**kw):
    field = {
        "field_name": "token",
        "input_type": "password",
        "label": "Bearer Token",
        "hint": "",
        "required": True,
    }
    field.update(kw)
    return field


DASHBOARD_BEARER = {
    "type": "BEARER",
    "display_name": "Bearer Token",
    "description": "",
    "is_open_api": True,
    "fields": [_token_field()],
}

DASHBOARD_API_KEY = {
    "type": "API_KEY",
    "display_name": "API Key",
    "description": "Authenticate with an API key",
    "is_open_api": True,
    "fields": [
        {"field_name": "api_key", "input_type": "password", "label": "API Key", "hint": "", "required": True},
        {"field_name": "domain", "input_type": "text", "label": "Domain", "hint": "", "required": False,
         "is_path_param": True},
    ],
    "auth_header_key_override": "x-api-key",
}

DASHBOARD_OAUTH = {
    "type": "OAUTH",
    "display_name": "OAuth",
    "description": "",
    "is_open_api": True,
    "fields": None,
    "oauth_config": {
        "available_scopes": [
            {"scope": "read", "description": None, "required": True, "display_name": "Read"},
            {"scope": "write", "description": "", "required": False, "display_name": "Write"},
        ],
        "authorize_uri": "https://auth.example.com/authorize",
        "token_uri": "https://auth.example.com/token",
        "pkce_enabled": True,
        "custom_scope_name": "",
    },
}

DASHBOARD_NO_AUTH = {
    "type": "NO_AUTH",
    "display_name": "No Auth",
    "description": "",
    "is_open_api": True,
    "fields": None,
}

DASHBOARD_SET = [DASHBOARD_BEARER, DASHBOARD_API_KEY, DASHBOARD_OAUTH, DASHBOARD_NO_AUTH]

# Shapes the server's encoder does not produce today but a stored document or a later server
# could; the SDK must not reshape them either.
ODD_SHAPES = {
    "hint absent": {"type": "BEARER", "display_name": "B", "fields": [{"field_name": "token", "label": "T",
                                                                       "input_type": "password"}]},
    "hint null": {"type": "BEARER", "display_name": "B", "description": "",
                  "fields": [_token_field(hint=None)]},
    "fields empty": {"type": "NO_AUTH", "display_name": "N", "description": "", "fields": []},
    "fields absent": {"type": "NO_AUTH", "display_name": "N"},
    "options empty": {"type": "OAUTH", "display_name": "O", "description": "",
                      "fields": [{"field_name": "mode", "input_type": "select", "label": "Mode",
                                  "hint": None, "required": False, "options": []}],
                      "oauth_config": {"pkce_enabled": True}},
    "options set": {"type": "OAUTH", "display_name": "O", "description": "",
                    "fields": [{"field_name": "access", "input_type": "select", "label": "Access",
                                "hint": "", "required": True,
                                "options": [{"value": "offline", "display_name": "Offline", "description": "",
                                             "default": True},
                                            {"value": "online", "display_name": None}]}],
                    "oauth_config": {}},
    "input_type empty": {"type": "BEARER", "display_name": "B", "description": "",
                         "fields": [_token_field(input_type="")]},
    "label null": {"type": "BEARER", "display_name": "B", "description": "",
                   "fields": [_token_field(label=None, required=None)]},
    "unknown keys": {"type": "API_KEY", "display_name": "K", "description": "", "hide_scopes_display": True,
                     "auth_field_mutations": {"api_key": {"prefix": "Key "}},
                     "fields": [_token_field(field_name="api_key", internal={"source": "spec"},
                                             later_key=[1, "two"])]},
    "placement": {"type": "API_KEY", "display_name": "K", "description": "", "is_open_api": True,
                  "fields": [_token_field(field_name="api_key",
                                          placement={"in": "query", "name": "api_key", "later": None})]},
    "placement without a name": {"type": "API_KEY", "display_name": "K", "description": "",
                                 "fields": [_token_field(field_name="api_key", placement={"in": "query"})]},
    "account fields and domains": {"type": "BEARER", "display_name": "B", "description": "",
                                   "fields": [_token_field()],
                                   "account_fields": [{"field_name": "workspace", "input_type": "text",
                                                       "label": "Workspace", "hint": None, "required": True}],
                                   "allowed_proxy_domains": []},
    "oauth_config null": {"type": "OAUTH", "display_name": "O", "description": "", "fields": [],
                          "oauth_config": None},
    "is_mcp and is_open_api false": {"type": "BEARER", "display_name": "B", "description": "",
                                     "is_mcp": False, "is_open_api": False, "fields": [_token_field()]},
}


def _all_shapes():
    shapes = {p["type"] + " (dashboard)": p for p in DASHBOARD_SET}
    shapes.update(ODD_SHAPES)
    return shapes


# The shapes whose normalised view differs from what the server stored, which is what makes
# sending the normalised view a change in the server's eyes.
NORMALISED_DIFFERS = ("BEARER (dashboard)", "OAUTH (dashboard)", "options empty", "input_type empty",
                      "account fields and domains")


# --- A model of the server's comparison ---------------------------------------------------
#
# Mirrors encoding/json decoding into db.AuthPattern, db.Field, db.Option, db.OauthConfig and
# friends at v0.1.162.1: unknown keys are dropped, an absent or null key leaves the zero value,
# a pointer or slice is nil (None) unless the key holds a value, [] is an empty non-nil slice,
# and a null element of a []*Option is a nil pointer. Two patterns are "unchanged" for the
# server exactly when these parses are equal.

def _s(d, k):
    v = d.get(k)
    return v if isinstance(v, str) else ""


def _b(d, k):
    return d.get(k) is True


def _ptr_str(d, k):
    v = d.get(k)
    return None if v is None else v


def _slice(d, k, elem):
    v = d.get(k)
    return None if v is None else [elem(x) for x in v]


def _ptr(d, k, conv):
    v = d.get(k)
    return None if v is None else conv(v)


def _go_option(o):
    if o is None:
        return None
    return (_s(o, "value"), _s(o, "display_name"), _s(o, "description"), _b(o, "default"))


def _go_field(f):
    return (
        _s(f, "field_name"), _s(f, "input_type"), _s(f, "label"), _ptr_str(f, "hint"), _b(f, "required"),
        _slice(f, "options", _go_option), f.get("internal"), _b(f, "is_path_param"), _s(f, "header_name"),
        _ptr(f, "placement", lambda p: (_s(p, "in"), _s(p, "name"))),
    )


def _go_scope(s):
    return (_s(s, "scope"), _ptr_str(s, "description"), _b(s, "required"), _s(s, "display_name"),
            _slice(s, "token_types", lambda t: t), _b(s, "scalekit_cred_allowed"))


def _go_oauth(c):
    return (
        _slice(c, "available_scopes", _go_scope), _s(c, "authorize_uri"), _s(c, "token_uri"),
        _s(c, "user_info_uri"), _b(c, "allow_use_scalekit_credentials"), _ptr_str(c, "custom_scope_name"),
        _b(c, "pkce_enabled"),
        _ptr(c, "optional_scopes", lambda o: (_s(o, "field_name"), _ptr_str(o, "description"),
                                              _s(o, "display_name"), _b(o, "required"))),
        _ptr_str(c, "primary_scope_bucket"), _ptr_str(c, "scopes_label"), _ptr_str(c, "client_id_label"),
        _ptr_str(c, "client_secret_label"), _s(c, "token_endpoint_auth_method"),
    )


def _go_mutation(m):
    return (_s(m, "prefix"), _s(m, "suffix"), _s(m, "default"))


def _go_pattern(p):
    return (
        _s(p, "type"), _s(p, "display_name"), _s(p, "description"), _b(p, "is_mcp"), _b(p, "is_open_api"),
        _slice(p, "account_fields", _go_field), _slice(p, "fields", _go_field),
        _ptr(p, "oauth_config", _go_oauth), _s(p, "auth_header_key_override"),
        _ptr(p, "auth_field_mutations", lambda m: tuple(
            _ptr(m, k, _go_mutation) for k in ("api_key", "token", "username", "password"))),
        _slice(p, "allowed_proxy_domains", lambda x: x), _b(p, "hide_scopes_display"),
    )


def _server_parse(wire_patterns):
    """What the server compares: its JSON text of the ListValue, parsed the Go way."""
    return [_go_pattern(p) for p in json.loads(json.dumps(wire_patterns))]


def _served(pattern_dicts):
    """Decode as Provider.from_proto does: through the auth_patterns ListValue of a response."""
    provider = pb.Provider(id="prvd_1", identifier="PETSTORE:12", display_name="Petstore", is_custom=True)
    ParseDict(pattern_dicts, provider.auth_patterns)
    return Provider.from_proto(provider)


def _wire(patterns):
    """The patterns as they reach the server."""
    return MessageToDict(_patterns_to_list_value(patterns))


def _through_the_wire(d):
    """A server dict as the SDK receives it (protobuf Struct numbers become floats)."""
    return MessageToDict(ParseDict([d], pb.Provider().auth_patterns))[0]


class ServedPatternsGoBackUnchangedTest(unittest.TestCase):
    """The wire form: what the SDK sends to the server for a pattern it decoded."""

    def test_every_served_shape_is_sent_exactly(self):
        for name, served in _all_shapes().items():
            with self.subTest(name):
                pattern = _served([served]).auth_patterns[0]
                self.assertEqual(_wire([pattern]), [_through_the_wire(served)])

    def test_every_nested_model_is_sent_exactly_on_its_own(self):
        """Also when the pattern around it changed and is rebuilt from its values."""
        for name, served in _all_shapes().items():
            served = _through_the_wire(served)
            pattern = AuthPattern.from_dict(served)
            pattern.display_name = "Changed"
            wire = _wire([pattern])[0]
            with self.subTest(name):
                self.assertEqual(wire["display_name"], "Changed")
                for key in ("fields", "account_fields"):
                    for i, field in enumerate(served.get(key) or []):
                        self.assertEqual(getattr(pattern, key)[i]._to_wire_dict(), field)
                        self.assertEqual(wire[key][i], field)
                        for j, option in enumerate(field.get("options") or []):
                            self.assertEqual(getattr(pattern, key)[i].options[j]._to_wire_dict(), option)
                        if field.get("placement") is not None:
                            self.assertEqual(getattr(pattern, key)[i].placement._to_wire_dict(), field["placement"])
                if served.get("oauth_config") is not None:
                    self.assertEqual(pattern.oauth_config._to_wire_dict(), served["oauth_config"])
                    self.assertEqual(wire["oauth_config"], served["oauth_config"])

    def test_the_server_sees_no_change_for_any_served_shape(self):
        for name, served in _all_shapes().items():
            with self.subTest(name):
                pattern = _served([served]).auth_patterns[0]
                self.assertEqual(_server_parse(_wire([pattern])), _server_parse([served]))

    def test_the_dashboard_set_goes_back_unchanged_together(self):
        provider = _served(DASHBOARD_SET)
        self.assertEqual(_wire(provider.auth_patterns), DASHBOARD_SET)
        self.assertEqual(_server_parse(_wire(provider.auth_patterns)), _server_parse(DASHBOARD_SET))

    def test_the_server_model_tells_the_normalised_shapes_apart(self):
        """The control for the tests above: rebuilding a pattern from its values would be a change."""
        for name in NORMALISED_DIFFERS:
            with self.subTest(name):
                served = _all_shapes()[name]
                rebuilt = AuthPattern.model_validate(_served([served]).auth_patterns[0].model_dump(),
                                                     context={"decoding": True})
                self.assertNotEqual(_server_parse(_wire([rebuilt])), _server_parse([served]))

    def test_to_dict_is_not_what_is_sent(self):
        """The control for the public view: the server reads the normalised view as a change."""
        for name in NORMALISED_DIFFERS:
            with self.subTest(name):
                served = _all_shapes()[name]
                pattern = _served([served]).auth_patterns[0]
                self.assertNotEqual(_server_parse([pattern.to_dict()]), _server_parse([served]))
                self.assertEqual(_server_parse(_wire([pattern])), _server_parse([served]))

    def test_the_typed_update_sends_the_stored_patterns_back_unchanged(self):
        core = MagicMock()
        sent = []
        core.grpc_exec.side_effect = lambda rpc, request, **kw: (
            sent.append(request) or (pb.UpdateProviderResponse(provider=pb.Provider()), None)
        )
        client = ActionClient(MagicMock(), MagicMock(), providers_client=ProvidersClient(core))
        current = _served([DASHBOARD_BEARER])
        client.providers.update_custom_provider(
            UpdateCustomProviderRequest(
                identifier=current.identifier,
                display_name="Petstore Two",
                auth_patterns=current.auth_patterns,
                proxy_enabled=current.proxy_enabled,
                proxy_url=current.proxy_url,
            )
        )
        wire = MessageToDict(sent[0].provider.auth_patterns)
        self.assertEqual(wire, [DASHBOARD_BEARER])
        self.assertEqual(wire[0]["fields"][0]["hint"], "")
        self.assertEqual(_server_parse(wire), _server_parse([DASHBOARD_BEARER]))

    def test_the_served_dict_is_copied_in_and_out(self):
        served = copy.deepcopy(DASHBOARD_API_KEY)
        pattern = AuthPattern.from_dict(served)
        served["fields"][0]["hint"] = "changed by the caller"
        out = pattern._to_wire_dict()
        self.assertEqual(out, DASHBOARD_API_KEY)
        out["fields"][0]["hint"] = "changed again"
        self.assertEqual(pattern._to_wire_dict(), DASHBOARD_API_KEY)


class ToDictIsTheNormalisedViewTest(unittest.TestCase):
    """The public to_dict() builds the normalised view from the values, whatever the pattern's history."""

    # What a decoded pattern gives, by shape. Defaults are left out, null and "" collapse, "fields"
    # is always a list, "oauth_config" is absent when there is none, and keys the SDK does not
    # declare are re-emitted unchanged.
    EXPECTED = {
        "BEARER (dashboard)": {
            "type": "BEARER", "display_name": "Bearer Token", "is_open_api": True,
            "fields": [{"field_name": "token", "label": "Bearer Token", "input_type": "password",
                        "required": True}],
        },
        "API_KEY (dashboard)": {
            "type": "API_KEY", "display_name": "API Key", "description": "Authenticate with an API key",
            "is_open_api": True, "auth_header_key_override": "x-api-key",
            "fields": [{"field_name": "api_key", "label": "API Key", "input_type": "password", "required": True},
                       {"field_name": "domain", "label": "Domain", "input_type": "text", "is_path_param": True}],
        },
        "OAUTH (dashboard)": {
            "type": "OAUTH", "display_name": "OAuth", "is_open_api": True, "fields": [],
            "oauth_config": DASHBOARD_OAUTH["oauth_config"],
        },
        "NO_AUTH (dashboard)": {"type": "NO_AUTH", "display_name": "No Auth", "is_open_api": True, "fields": []},
        "hint absent": {"type": "BEARER", "display_name": "B",
                        "fields": [{"field_name": "token", "label": "T", "input_type": "password"}]},
        "hint null": {"type": "BEARER", "display_name": "B",
                      "fields": [{"field_name": "token", "label": "Bearer Token", "input_type": "password",
                                  "required": True}]},
        "fields empty": {"type": "NO_AUTH", "display_name": "N", "fields": []},
        "fields absent": {"type": "NO_AUTH", "display_name": "N", "fields": []},
        "options empty": {"type": "OAUTH", "display_name": "O", "oauth_config": {"pkce_enabled": True},
                          "fields": [{"field_name": "mode", "label": "Mode", "input_type": "select"}]},
        "options set": {"type": "OAUTH", "display_name": "O",
                        "oauth_config": {"pkce_enabled": False},  # an empty config: the server leaves false out
                        "fields": [{"field_name": "access", "label": "Access", "input_type": "select",
                                    "required": True,
                                    "options": [{"value": "offline", "display_name": "Offline", "description": "",
                                                 "default": True},
                                                {"value": "online", "display_name": "", "description": "",
                                                 "default": False}]}]},
        "input_type empty": {"type": "BEARER", "display_name": "B",
                             "fields": [{"field_name": "token", "label": "Bearer Token", "input_type": "text",
                                         "required": True}]},
        "label null": {"type": "BEARER", "display_name": "B",
                       "fields": [{"field_name": "token", "label": "", "input_type": "password"}]},
        "unknown keys": {"type": "API_KEY", "display_name": "K", "hide_scopes_display": True,
                         "auth_field_mutations": {"api_key": {"prefix": "Key "}},
                         "fields": [{"field_name": "api_key", "label": "Bearer Token", "input_type": "password",
                                     "required": True, "internal": {"source": "spec"},
                                     "later_key": [1.0, "two"]}]},
        "placement": {"type": "API_KEY", "display_name": "K", "is_open_api": True,
                      "fields": [{"field_name": "api_key", "label": "Bearer Token", "input_type": "password",
                                  "required": True,
                                  "placement": {"in": "query", "name": "api_key", "later": None}}]},
        "oauth_config null": {"type": "OAUTH", "display_name": "O", "fields": []},
        "account fields and domains": {
            "type": "BEARER", "display_name": "B",
            "fields": [{"field_name": "token", "label": "Bearer Token", "input_type": "password",
                        "required": True}],
            "account_fields": [{"field_name": "workspace", "label": "Workspace", "input_type": "text",
                                "required": True}],
        },
    }

    def test_a_decoded_pattern_gives_the_normalised_view(self):
        for name, expected in self.EXPECTED.items():
            with self.subTest(name):
                self.assertEqual(AuthPattern.from_dict(_through_the_wire(_all_shapes()[name])).to_dict(), expected)

    def test_a_decoded_pattern_gives_what_one_built_from_its_values_gives(self):
        """to_dict() depends on the values alone, not on the dict the pattern was decoded from."""
        for name, served in _all_shapes().items():
            with self.subTest(name):
                decoded = AuthPattern.from_dict(_through_the_wire(served))
                rebuilt = AuthPattern.model_validate(decoded.model_dump(), context={"decoding": True})
                self.assertEqual(decoded.to_dict(), rebuilt.to_dict())

    def test_a_served_null_is_a_list_and_a_missing_oauth_config_is_absent(self):
        pattern = AuthPattern.from_dict(DASHBOARD_OAUTH)
        self.assertEqual(pattern.to_dict()["fields"], [])
        self.assertIs(pattern.to_dict()["oauth_config"]["pkce_enabled"], True)
        pattern = AuthPattern.from_dict({"type": "OAUTH", "display_name": "O", "fields": None, "oauth_config": None})
        self.assertEqual(pattern.to_dict(), {"type": "OAUTH", "display_name": "O", "fields": []})
        self.assertEqual(AuthField.from_dict(_token_field(input_type="", hint=None)).to_dict()["input_type"], "text")
        self.assertIs(AuthPattern.from_dict(
            {"type": "OAUTH", "display_name": "O", "oauth_config": {}}).to_dict()["oauth_config"]["pkce_enabled"],
                      False)

    def test_a_decoded_nested_model_gives_the_normalised_view_too(self):
        field = AuthField.from_dict(_token_field(hint=None, input_type="", label=None))
        self.assertEqual(field.to_dict(), {"field_name": "token", "label": "", "input_type": "text",
                                           "required": True})
        option = AuthFieldOption.from_dict({"value": "online", "display_name": None})
        self.assertEqual(option.to_dict(), {"value": "online", "display_name": "", "description": "",
                                            "default": False})
        self.assertEqual(OAuthConfig.from_dict({}).to_dict(), {"pkce_enabled": False})
        self.assertEqual(CredentialPlacement.from_dict({"in": "query"}).to_dict(), {"in": "query", "name": ""})

    def test_unchanged_children_of_an_edited_pattern_are_normalised_too(self):
        pattern = AuthPattern.from_dict(DASHBOARD_API_KEY)
        pattern.display_name = "Renamed"
        view = pattern.to_dict()
        self.assertEqual(view["display_name"], "Renamed")
        self.assertNotIn("hint", view["fields"][0])
        self.assertEqual(view["fields"][0], AuthField(field_name="api_key", label="API Key", input_type="password",
                                                      required=True).to_dict())

    def test_sending_a_pattern_does_not_change_its_view(self):
        pattern = AuthPattern.from_dict(DASHBOARD_API_KEY)
        before = pattern.to_dict()
        _wire([pattern])
        self.assertEqual(pattern.to_dict(), before)
        self.assertNotIn("hint", pattern.to_dict()["fields"][0])


class ChangedPatternsTest(unittest.TestCase):
    def test_a_changed_field_value_is_sent(self):
        pattern = AuthPattern.from_dict(DASHBOARD_API_KEY)
        pattern.fields[0].hint = "Find it under Settings"
        wire = _wire([pattern])[0]
        self.assertEqual(wire["fields"][0]["hint"], "Find it under Settings")
        # The untouched field still goes back as served.
        self.assertEqual(wire["fields"][1], DASHBOARD_API_KEY["fields"][1])
        self.assertNotEqual(_server_parse([wire]), _server_parse([DASHBOARD_API_KEY]))

    def test_a_changed_pattern_value_is_sent(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        pattern.display_name = "Token"
        wire = _wire([pattern])[0]
        self.assertEqual(wire["display_name"], "Token")
        self.assertEqual(wire["fields"], DASHBOARD_BEARER["fields"])

    def test_the_unchanged_children_of_a_changed_one_keep_their_served_form_at_every_depth(self):
        pattern = AuthPattern.from_dict(ODD_SHAPES["options set"])
        pattern.fields[0].label = "Access level"  # the field is rebuilt; its options were not touched
        field = _wire([pattern])[0]["fields"][0]
        self.assertEqual(field["label"], "Access level")
        self.assertEqual(field["options"], _through_the_wire(ODD_SHAPES["options set"])["fields"][0]["options"])
        self.assertEqual(field["options"][1], {"value": "online", "display_name": None})
        self.assertNotIn("hint", field)  # the field itself was rebuilt in the normalised form

    def test_list_changes_count_as_changes(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        pattern.fields.append(AuthField(field_name="extra", label="Extra"))
        self.assertEqual([f["field_name"] for f in _wire([pattern])[0]["fields"]], ["token", "extra"])

        option_field = AuthField.from_dict(ODD_SHAPES["options set"]["fields"][0])
        option_field.options[0].default = False
        self.assertIs(option_field._to_wire_dict()["options"][0]["default"], False)

    def test_changed_nested_oauth_config_and_placement_are_sent(self):
        pattern = AuthPattern.from_dict(DASHBOARD_OAUTH)
        pattern.oauth_config.pkce_enabled = False
        self.assertIs(_wire([pattern])[0]["oauth_config"]["pkce_enabled"], False)

        field = AuthField.from_dict(ODD_SHAPES["placement"]["fields"][0])
        field.placement.in_ = CredentialPlacement.BODY
        self.assertEqual(field._to_wire_dict()["placement"]["in"], "body")

    def test_changing_a_value_back_restores_the_served_form(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        pattern.fields[0].hint = "temporary"
        pattern.fields[0].hint = ""
        self.assertEqual(_wire([pattern]), [DASHBOARD_BEARER])

    def test_model_copy_with_an_update_is_a_change(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        renamed = pattern.model_copy(update={"display_name": "Renamed"})
        self.assertEqual(_wire([renamed])[0]["display_name"], "Renamed")
        self.assertEqual(_wire([pattern]), [DASHBOARD_BEARER])


class TypeSensitiveChangeDetectionTest(unittest.TestCase):
    """An edit to a value that compares equal in Python is still an edit: 1, 1.0 and True are not alike in JSON."""

    def _pattern_with_flag(self, value):
        return _served([{"type": "BEARER", "display_name": "B", "description": "",
                         "fields": [_token_field(internal={"flag": value})]}]).auth_patterns[0]

    def test_a_free_form_key_changed_to_an_equal_value_of_another_type_is_sent(self):
        for served, assigned in ((1, True), (0, False), (True, 1), (False, 0), (True, 1.0)):
            with self.subTest(f"{served!r} -> {assigned!r}"):
                pattern = self._pattern_with_flag(served)
                before = _wire([pattern])[0]["fields"][0]["internal"]["flag"]
                pattern.fields[0].internal["flag"] = assigned
                sent = _wire([pattern])[0]["fields"][0]["internal"]["flag"]
                expected = _through_the_wire({"x": assigned})["x"]
                self.assertIs(type(sent), type(expected))
                self.assertIsNot(type(sent), type(before))
                self.assertEqual(sent, expected)

    def test_a_declared_field_changed_to_an_equal_value_of_another_type_is_sent(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        self.assertEqual(_wire([pattern]), [DASHBOARD_BEARER])
        pattern.fields[0].required = 1  # not validated on assignment: the field now holds an int
        sent = _wire([pattern])[0]["fields"][0]
        self.assertNotEqual(sent, DASHBOARD_BEARER["fields"][0])  # rebuilt from the values: no "hint" any more
        self.assertNotIn("hint", sent)
        self.assertIs(sent["required"], True)

    def test_an_extra_key_added_or_changed_is_sent(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        pattern.hide_scopes_display = True
        self.assertIs(_wire([pattern])[0]["hide_scopes_display"], True)
        pattern = AuthPattern.from_dict({**DASHBOARD_BEARER, "hide_scopes_display": False})
        pattern.hide_scopes_display = True
        self.assertIs(_wire([pattern])[0]["hide_scopes_display"], True)

    def test_a_reordered_dict_is_not_a_change(self):
        served = _token_field(internal={"a": 1, "b": 2})
        pattern = AuthPattern.from_dict({"type": "BEARER", "display_name": "B", "description": "",
                                         "fields": [served]})
        pattern.fields[0].internal = {"b": 2, "a": 1}
        self.assertEqual(_wire([pattern])[0]["fields"][0], _through_the_wire(
            {"type": "BEARER", "fields": [served]})["fields"][0])
        self.assertEqual(_wire([pattern])[0]["fields"][0]["hint"], "")

    def test_assigning_the_value_the_sdk_already_decoded_is_not_a_change(self):
        """hint is a null on the wire and "" in the model: assigning "" does not turn the null into one."""
        pattern = AuthPattern.from_dict(ODD_SHAPES["hint null"])
        pattern.fields[0].hint = ""
        self.assertIsNone(_wire([pattern])[0]["fields"][0]["hint"])

    def test_noticing_a_change_does_not_warn(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # a pydantic serializer warning would surface here
            pattern.fields[0].required = 1
            pattern.fields[0].label = 5
            _wire([pattern])


class AuthoredPatternsTest(unittest.TestCase):
    def test_an_authored_pattern_keeps_the_minimal_form(self):
        pattern = AuthPattern(
            type="BEARER",
            display_name="Bearer Token",
            fields=[AuthField(field_name="token", label="Bearer Token", input_type="password", required=True)],
        )
        expected = {
            "type": "BEARER",
            "display_name": "Bearer Token",
            "fields": [{"field_name": "token", "label": "Bearer Token", "input_type": "password",
                        "required": True}],
        }
        self.assertEqual(pattern.to_dict(), expected)
        self.assertEqual(_wire([pattern]), [expected])
        self.assertEqual(AuthField(field_name="x").to_dict(), {"field_name": "x", "label": "", "input_type": "text"})
        self.assertEqual(OAuthConfig().to_dict(), {"pkce_enabled": True})
        self.assertEqual(
            AuthFieldOption(value="a").to_dict(),
            {"value": "a", "display_name": "", "description": "", "default": False},
        )
        self.assertEqual(CredentialPlacement(in_="query", name="k").to_dict(), {"in": "query", "name": "k"})

    def test_a_pattern_built_from_a_view_is_sent_as_that_view(self):
        """to_dict() then from_dict() rebuilds the pattern in the normalised form, which is then what is sent."""
        decoded = AuthPattern.from_dict(DASHBOARD_BEARER)
        again = AuthPattern.from_dict(decoded.to_dict())
        self.assertEqual(_wire([again]), [decoded.to_dict()])
        self.assertNotEqual(_wire([again]), [DASHBOARD_BEARER])
        rebuilt = AuthPattern.model_validate(decoded.model_dump(), context={"decoding": True})
        self.assertEqual(_wire([rebuilt]), [decoded.to_dict()])


class ModelBehaviourTest(unittest.TestCase):
    def test_copies_and_pickles_keep_the_served_form(self):
        pattern = _served([DASHBOARD_OAUTH]).auth_patterns[0]
        for clone in (copy.copy(pattern), copy.deepcopy(pattern), pattern.model_copy(),
                      pattern.model_copy(deep=True), pickle.loads(pickle.dumps(pattern))):
            self.assertEqual(_wire([clone]), [DASHBOARD_OAUTH])
            self.assertEqual(clone, pattern)

    def test_a_deep_copy_changes_independently(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        clone = pattern.model_copy(deep=True)
        clone.fields[0].hint = "only on the copy"
        self.assertEqual(_wire([pattern]), [DASHBOARD_BEARER])
        self.assertEqual(_wire([clone])[0]["fields"][0]["hint"], "only on the copy")

    def test_equality_compares_values_not_the_served_form(self):
        decoded = AuthPattern.from_dict(DASHBOARD_BEARER)
        authored = AuthPattern(
            type="BEARER",
            display_name="Bearer Token",
            is_open_api=True,
            fields=[AuthField(field_name="token", label="Bearer Token", input_type="password", required=True)],
        )
        self.assertEqual(decoded, authored)
        self.assertNotEqual(decoded, AuthPattern.from_dict({**DASHBOARD_BEARER, "display_name": "Other"}))
        self.assertNotEqual(AuthField(field_name="a"), AuthField(field_name="a", extra_key=1))
        self.assertNotEqual(AuthField(field_name="a"), "a")

    def test_repr_and_model_dump_do_not_show_the_served_dict(self):
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        self.assertNotIn("_served", repr(pattern))
        self.assertNotIn("_served", json.dumps(pattern.model_dump()))
        self.assertEqual(pattern.model_dump()["fields"][0]["hint"], "")

    def test_a_model_dump_round_trip_does_not_keep_the_served_form(self):
        """Documented: the served form is kept by copy, deepcopy and pickle, not by model_dump()."""
        pattern = AuthPattern.from_dict(DASHBOARD_BEARER)
        rebuilt = AuthPattern.model_validate(pattern.model_dump(), context={"decoding": True})
        self.assertEqual(rebuilt, pattern)
        self.assertNotEqual(_wire([rebuilt]), [DASHBOARD_BEARER])

    def test_the_decoded_values_are_unchanged(self):
        """Decoding still normalises the typed values; only the wire form is preserved."""
        field = AuthField.from_dict(_token_field(hint=None, input_type=""))
        self.assertEqual((field.hint, field.input_type), ("", "text"))
        pattern = AuthPattern.from_dict(DASHBOARD_OAUTH)
        self.assertEqual(pattern.fields, [])
        self.assertEqual(pattern.oauth_config.authorize_uri, "https://auth.example.com/authorize")

    def test_an_edit_of_a_decoded_catalogue_shape_is_still_allowed(self):
        pattern = AuthPattern.from_dict({"type": "OAUTH", "display_name": "OAuth"})  # no oauth_config
        pattern.description = "edited"
        self.assertEqual(pattern.to_dict()["description"], "edited")
        self.assertEqual(_wire([pattern])[0]["description"], "edited")


if __name__ == "__main__":
    unittest.main()

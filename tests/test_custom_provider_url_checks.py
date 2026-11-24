"""Offline tests: the URL checks of the custom connector request models are the server's checks.

The server validates proxy_url and openapi_spec_url on create and on update with the proto options
``pattern: "^https://"`` (anchored, case-sensitive, nothing is trimmed) and ``max_len: 2048``, and answers
400 INVALID_ARGUMENT at once, which the SDK never retries. ``urllib.parse.urlparse`` alone accepts
'HTTPS://x', ' https://x' and URLs of any length, so the four validators (two models, two fields each) must
be stricter than that. No network and no environment are needed.
"""
import unittest

from buf.validate import validate_pb2 as validate
from pydantic import ValidationError

from scalekit.actions.models.requests._https_url import HTTPS_PREFIX, MAX_URL_LENGTH
from scalekit.actions.types import (
    AuthField,
    AuthPattern,
    CreateCustomProviderRequest,
    UpdateCustomProviderRequest,
)
from scalekit.v1.providers import providers_pb2 as pb

URL_FIELDS = ("proxy_url", "openapi_spec_url")
HOST = "https://x.example.com/"


def _url_of_length(length: int) -> str:
    return HOST + "a" * (length - len(HOST))


def _pattern() -> AuthPattern:
    return AuthPattern(
        type="API_KEY",
        display_name="API Key",
        fields=[AuthField(field_name="api_key", label="API Key", input_type="password", required=True)],
    )


def _create(field: str, url: str) -> CreateCustomProviderRequest:
    return CreateCustomProviderRequest(display_name="Acme", auth_patterns=[_pattern()], **{field: url})


def _update(field: str, url: str) -> UpdateCustomProviderRequest:
    return UpdateCustomProviderRequest(
        identifier="ACME:1", display_name="Acme", auth_patterns=[_pattern()], **{field: url}
    )


MODELS = {"CreateCustomProviderRequest": _create, "UpdateCustomProviderRequest": _update}

ACCEPTED = {
    "an ordinary URL": "https://x.example.com/mcp",
    "a bare host": "https://x",
    "a templated host": "https://{{domain}}/mcp",
    "a templated part of the host and the path": "https://{{subdomain}}.example.com/{{version}}/mcp",
    "exactly 2048 characters": _url_of_length(2048),
}

# Each of these is refused by the server's pattern or length (or has no host), so the call would fail with
# a 400 that is never retried: the model refuses it before anything is sent.
REJECTED = {
    "an upper-case scheme": "HTTPS://x.example.com/mcp",
    "a mixed-case scheme": "Https://x.example.com/mcp",
    "a leading space": " https://x.example.com/mcp",
    "a leading tab": "\thttps://x.example.com/mcp",
    "a leading newline": "\nhttps://x.example.com/mcp",
    "http": "http://x.example.com/mcp",
    "no scheme": "x.example.com/mcp",
    "a tab inside the scheme, which urlparse would drop": "htt\tps://x.example.com/mcp",
    "no host": "https://",
    "no host and a path": "https:///mcp",
    "2049 characters": _url_of_length(2049),
}


class UrlChecksTest(unittest.TestCase):
    def test_what_the_server_accepts_is_accepted_by_all_four_validators(self):
        for model, build in MODELS.items():
            for field in URL_FIELDS:
                for label, url in ACCEPTED.items():
                    with self.subTest(model=model, field=field, url=label):
                        self.assertEqual(getattr(build(field, url), field), url, "the value is kept as it is")

    def test_what_the_server_refuses_is_refused_by_all_four_validators(self):
        for model, build in MODELS.items():
            for field in URL_FIELDS:
                for label, url in REJECTED.items():
                    with self.subTest(model=model, field=field, url=label):
                        with self.assertRaises(ValidationError) as refused:
                            build(field, url)
                        self.assertIn(f"{field} must be a valid HTTPS URL", str(refused.exception))

    def test_the_length_limit_counts_characters_and_names_the_limit(self):
        for model, build in MODELS.items():
            for field in URL_FIELDS:
                with self.subTest(model=model, field=field):
                    with self.assertRaises(ValidationError) as refused:
                        build(field, _url_of_length(2049))
                    self.assertIn("at most 2048 characters (got 2049)", str(refused.exception))
                    # a character outside the Basic Multilingual Plane is one character, not two
                    build(field, HOST + "\U0001f600" * (2048 - len(HOST)))
                    with self.assertRaises(ValidationError):
                        build(field, HOST + "\U0001f600" * (2049 - len(HOST)))

    def test_a_refused_scheme_says_what_to_write(self):
        with self.assertRaises(ValidationError) as refused:
            _create("proxy_url", "HTTPS://x.example.com/mcp")
        message = str(refused.exception)
        self.assertIn("proxy_url must be a valid HTTPS URL (e.g. 'https://server.example.com/mcp')", message)
        self.assertIn("lower-case 'https://'", message)

    def test_the_checks_also_run_on_assignment(self):
        for model, build in MODELS.items():
            for field in URL_FIELDS:
                with self.subTest(model=model, field=field):
                    kept = "https://x.example.com/mcp"
                    request = build(field, kept)
                    for url in ("HTTPS://x.example.com/mcp", " https://x.example.com/mcp", _url_of_length(2049)):
                        with self.assertRaises(ValidationError):
                            setattr(request, field, url)
                    self.assertEqual(getattr(request, field), kept, "a refused value is not kept")

    def test_an_update_still_takes_none_and_an_empty_string_for_both_fields(self):
        """"" is what Provider.proxy_url holds until the first run fills in the base URL: it is sent back as read."""
        for field in URL_FIELDS:
            with self.subTest(field=field):
                self.assertEqual(getattr(_update(field, ""), field), "")
                self.assertIsNone(getattr(UpdateCustomProviderRequest(identifier="ACME:1", display_name="Acme"), field))

    def test_a_create_still_needs_exactly_one_source(self):
        self.assertEqual(_create("proxy_url", "https://x.example.com/mcp").proxy_url, "https://x.example.com/mcp")
        with self.assertRaises(ValidationError):
            _create("proxy_url", "")  # an empty URL is not a source
        with self.assertRaises(ValidationError):
            CreateCustomProviderRequest(
                display_name="Acme",
                proxy_url="https://x.example.com/mcp",
                openapi_spec_url="https://x.example.com/openapi.json",
                auth_patterns=[_pattern()],
            )


class ServerRuleTest(unittest.TestCase):
    """The checks mirror the proto options of the four fields: a proto sync that changes them fails here."""

    def test_the_models_use_the_proto_pattern_and_length(self):
        for message in ("CreateCustomProvider", "UpdateCustomProvider"):
            fields = pb.DESCRIPTOR.message_types_by_name[message].fields_by_name
            for name in URL_FIELDS:
                with self.subTest(message=message, field=name):
                    rules = fields[name].GetOptions().Extensions[validate.field].string
                    self.assertEqual(rules.pattern, "^" + HTTPS_PREFIX)
                    self.assertEqual(rules.max_len, MAX_URL_LENGTH)


if __name__ == "__main__":
    unittest.main()

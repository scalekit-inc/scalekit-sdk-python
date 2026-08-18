from scalekit.middleware.csrf_state import (
    generate_state,
    sanitize_return_to,
    verify_state,
)


class TestGenerateStateVerifyState:
    def test_verifies_a_matching_state(self):
        state = generate_state()
        assert verify_state(state, state) is True

    def test_rejects_a_mismatched_state(self):
        assert verify_state(generate_state(), generate_state()) is False

    def test_rejects_when_either_side_is_missing(self):
        state = generate_state()
        assert verify_state(None, state) is False
        assert verify_state(state, None) is False
        assert verify_state(None, None) is False


class TestSanitizeReturnTo:
    def test_accepts_a_same_origin_relative_path(self):
        assert sanitize_return_to("/account") == "/account"
        assert sanitize_return_to("/account?tab=billing") == "/account?tab=billing"

    def test_rejects_an_absolute_url(self):
        assert sanitize_return_to("https://evil.com") is None

    def test_rejects_a_protocol_relative_url(self):
        assert sanitize_return_to("//evil.com") is None

    def test_rejects_embedded_tab_cr_lf_bypass(self):
        # Browsers strip these during URL parsing (WHATWG URL spec), so
        # "/\t/evil.com" would otherwise normalize to the protocol-relative
        # "//evil.com" after a naive startswith('/') check passed it through.
        assert sanitize_return_to("/\t/evil.com") is None
        assert sanitize_return_to("/\r/evil.com") is None
        assert sanitize_return_to("/\n/evil.com") is None

    def test_rejects_a_value_not_starting_with_a_slash(self):
        assert sanitize_return_to("account") is None

    def test_returns_none_for_missing_input(self):
        assert sanitize_return_to(None) is None
        assert sanitize_return_to("") is None

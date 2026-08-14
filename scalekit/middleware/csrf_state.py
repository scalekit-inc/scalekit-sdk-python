from __future__ import annotations

import secrets

# Short-lived cookie carrying the OAuth `state` value between the login and
# callback views, so the callback can verify the provider's callback wasn't
# forged (CSRF: an attacker's own authorization code smuggled into a
# victim's browser session). Shared by every framework extra -- not
# framework-specific -- so a future fix here applies to all of them at once
# instead of risking one adapter drifting out of sync with the others.
STATE_COOKIE_NAME = "sk_oauth_state"
STATE_COOKIE_MAX_AGE = 600  # 10 minutes -- generous for a slow login, still short-lived


def generate_state() -> str:
    """A fresh, random OAuth state value for the login view to issue."""
    return secrets.token_urlsafe(32)


def verify_state(stored_state, returned_state) -> bool:
    """
    True only if both values are present and match, using a timing-safe
    comparison. Missing/mismatched state means this callback did not
    originate from a login this browser actually made.
    """
    if not stored_state or not returned_state:
        return False
    return secrets.compare_digest(stored_state, returned_state)


# Short-lived cookie carrying a validated post-login redirect target between
# the login and callback views, so `requires_auth`/`login_required` can send
# a user back to the page they originally requested instead of a fixed
# `post_login_redirect`. Shared by every framework extra, same as the OAuth
# state cookie above.
RETURN_TO_COOKIE_NAME = "sk_return_to"


def sanitize_return_to(value):
    """
    Validates a candidate post-login redirect target, accepting only
    same-origin relative paths. The value is attacker-influenceable (read
    from a query string on the login redirect), so this is a real
    open-redirect guard, not a cosmetic check: rejects absolute URLs
    (`https://evil.com`), protocol-relative URLs (`//evil.com`), and
    embedded tab/CR/LF characters -- browsers strip these during URL
    parsing per the WHATWG URL spec, so a naive `startswith('/')` check
    alone would let `"/\\t/evil.com"` normalize to the protocol-relative
    `"//evil.com"` after the fact.
    """
    if not value:
        return None
    if not value.startswith("/") or value.startswith("//"):
        return None
    if any(ch in value for ch in ("\t", "\r", "\n")):
        return None
    return value

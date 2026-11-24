"""The URL check of the custom connector request models, shared by create and update.

The server validates ``proxy_url`` and ``openapi_spec_url`` on both calls with the proto options
``pattern: "^https://"`` and ``max_len: 2048``: the pattern is anchored and case-sensitive, nothing is
trimmed, and the length counts characters. A value it refuses comes back at once as 400 INVALID_ARGUMENT and
is never retried. ``urllib.parse.urlparse`` alone is more lenient (it lowercases the scheme, ignores leading
whitespace and has no length limit), so ``'HTTPS://x'`` or ``' https://x'`` would pass here and fail there.
"""
from urllib.parse import urlparse

HTTPS_PREFIX = "https://"
MAX_URL_LENGTH = 2048


def check_https_url(field: str, value: str, example: str) -> str:
    """Return ``value`` when the server accepts it, or raise ``ValueError`` (which pydantic reports).

    The host check is the SDK's own and stays on top of the server's rule, so ``'https://'`` alone is
    refused. A templated value such as ``'https://{{domain}}/mcp'`` passes: its host is the placeholder.
    """
    if not value.startswith(HTTPS_PREFIX) or not urlparse(value).netloc:
        raise ValueError(
            f"{field} must be a valid HTTPS URL (e.g. '{example}'): it has to start with a lower-case "
            f"'{HTTPS_PREFIX}', with nothing in front of it, and name a host"
        )
    if len(value) > MAX_URL_LENGTH:
        raise ValueError(
            f"{field} must be a valid HTTPS URL of at most {MAX_URL_LENGTH} characters (got {len(value)})"
        )
    return value

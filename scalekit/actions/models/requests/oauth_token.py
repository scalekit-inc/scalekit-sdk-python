"""Build an ``OauthToken`` proto from the ``authorization_details["oauth_token"]`` dict."""

from typing import Any, Dict

from scalekit._convert import datetime_to_timestamp
from scalekit.v1.connected_accounts.connected_accounts_pb2 import OauthToken


def build_oauth_token(oauth_data: Dict[str, Any]) -> OauthToken:
    """Build the ``OauthToken`` proto sent on create/update connected account.

    ``expires_at`` is optional: a timezone-aware ``datetime``, sent as UTC. It is left unset
    when absent or ``None``. A naive ``datetime`` raises ``ValueError`` and any other type
    raises ``TypeError`` (see ``scalekit._convert.datetime_to_timestamp``).
    """
    oauth_token = OauthToken(
        access_token=oauth_data.get("access_token", ""),
        refresh_token=oauth_data.get("refresh_token", ""),
        scopes=oauth_data.get("scopes", []),
    )
    expires_at = oauth_data.get("expires_at")
    if expires_at is not None:
        oauth_token.expires_at.CopyFrom(datetime_to_timestamp(expires_at, "expires_at"))
    return oauth_token

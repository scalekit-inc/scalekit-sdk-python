"""Typed models and errors for the AgentKit connection methods on ``client.actions``."""
from scalekit.actions.connections import errors
from scalekit.actions.connections.models import (
    AgentKitConnection,
    AgentKitConnectionList,
    AgentKitConnectionSummary,
    AuthMode,
    GoogleDWDSettings,
    OAuthSettings,
    OptionalScopes,
    ProviderConfigurations,
    TokenEndpointAuthMethod,
)

__all__ = [
    "errors",
    "AgentKitConnection",
    "AgentKitConnectionList",
    "AgentKitConnectionSummary",
    "AuthMode",
    "GoogleDWDSettings",
    "OAuthSettings",
    "OptionalScopes",
    "ProviderConfigurations",
    "TokenEndpointAuthMethod",
]

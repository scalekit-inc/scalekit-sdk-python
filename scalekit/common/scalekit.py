from enum import Enum
from typing import Optional, List


class GrantType(Enum):
    """Enum class definition for Grant Types"""

    AuthorizationCode = "authorization_code"
    RefreshToken = "refresh_token"
    ClientCredentials = "client_credentials"


class AuthorizationUrlOptions:
    """Class definition for Authorization URL params"""

    def __init__(self):
        """ """
        self.connection_id: Optional[str] = None
        self.organization_id: Optional[str] = None
        self.scopes: Optional[str] = None
        self.state: Optional[str] = None
        self.nonce: Optional[str] = None
        self.domain_hint: Optional[str] = None
        self.login_hint: Optional[str] = None
        self.provider: Optional[str] = None
        self.prompt: Optional[str] = None


class CodeAuthenticationOptions:
    """Class definition for Code Authentication URL params"""

    def __init__(self):
        """ """
        self.code_verifier: Optional[str] = None


class RefreshTokenAuthenticationOptions:
    """Class definition for Refresh Authentication option params"""

    def __init__(self):
        """ """
        self.code: Optional[str] = None
        self.redirect_uri: Optional[str] = None


class AuthenticationOptions:
    """Class definition for Authentication option params"""

    def __init__(self):
        """ """
        self.refresh_token: Optional[str] = None


class IdpInitiatedLoginClaims:
    """Class definition for IDP Initiated Login Claims"""

    def __init__(self) -> None:
        self.connection_id: str
        self.organization_id: str
        self.login_hint: str
        self.relay_state: Optional[str] = None


class LogoutUrlOptions:
    """Options for logout URL generation"""
    def __init__(
            self,
            id_token_hint: Optional[str] = None,
            post_logout_redirect_uri: Optional[str] = None,
            state: Optional[str] = None
    ):
        self.id_token_hint = id_token_hint
        self.post_logout_redirect_uri = post_logout_redirect_uri
        self.state = state


class TokenValidationOptions:
    """Options for token validation including issuer, audience, and scope validation"""
    def __init__(
            self,
            issuer: Optional[str] = None,
            audience: Optional[List[str]] = None,
            required_scopes: Optional[List[str]] = None
    ):
        self.issuer = issuer
        self.audience = audience
        self.required_scopes = required_scopes


from enum import Enum


class GrantType(Enum):
    """ """
    AuthorizationCode = 'authorization_code'
    RefreshToken = 'refresh_token'
    ClientCredentials = 'client_credentials'


class AuthorizationUrlOptions:
    """ """
    def __init__(self):
        """ """
        self.connection_id = str | None
        self.organization_id = str | None
        self.scopes = [str]
        self.state = str | None
        self.nonce = str | None
        self.domain_hint = str | None
        self.login_hint = str | None


class CodeAuthenticationOptions:
    """ """
    def __init__(self):
        """ """
        self.code = str | None
        self.redirect_uri = str | None
        self.code_verifier = str | None


class RefreshTokenAuthenticationOptions:
    """ """
    def __init__(self):
        """ """
        self.code = str | None
        self.redirect_uri = str | None


class AuthenticationOptions:
    """ """
    def __init__(self):
        """ """
        self.refreshToken = str | None

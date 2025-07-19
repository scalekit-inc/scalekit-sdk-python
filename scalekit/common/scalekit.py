from enum import Enum
from typing import Optional


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


class ScalekitException(Exception):
    def __init__(self, messages: list, grpc_status):
        self.grpc_status = grpc_status
        self.http_status = GrpcToHttpStatus[grpc_status.name]
        self.err_details = messages
        super().__init__(str(messages))

    def __str__(self):
        return (f"ScalekitException: \n"
                f"gRPC - {self.grpc_status.name}: {self.grpc_status.value}\n"
                f"HTTP - {self.http_status.description()}: {self.http_status.code()}\n"
                f"Error Details: {self.err_details}")


class GrpcToHttpStatus(Enum):
    OK = (200, "OK")
    INVALID_ARGUMENT = (400, "Bad Request - Invalid Argument")
    FAILED_PRECONDITION = (400, "Bad Request - Failed Precondition")
    OUT_OF_RANGE = (400, "Bad Request - Out of Range")
    UNAUTHENTICATED = (401, "Unauthorized")
    PERMISSION_DENIED = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    ALREADY_EXISTS = (409, "Conflict - Already Exists")
    ABORTED = (409, "Conflict - Aborted")
    RESOURCE_EXHAUSTED = (429, "Too Many Requests")
    CANCELLED = (499, "Client Closed Request")
    UNKNOWN = (500, "Internal Server Error")
    INTERNAL = (500, "Internal Server Error")
    DATA_LOSS = (500, "Internal Server Error - Data Loss")
    UNIMPLEMENTED = (501, "Not Implemented")
    UNAVAILABLE = (503, "Service Unavailable")
    DEADLINE_EXCEEDED = (504, "Gateway Timeout")

    def code(self):
        return self.value[0]

    def description(self):
        return self.value[1]

    def __str__(self):
        return f"{self.code()}: {self.description()}"

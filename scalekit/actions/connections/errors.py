"""Errors raised by the AgentKit connection methods on ``client.actions``.

Every error carries:

* ``code``      a stable machine-readable string (see the constants below),
* ``step``      where it happened: ``"resolve"``, ``"read"``, ``"validate"``, ``"write"``,
* ``retryable`` whether trying the same call again can succeed,
* ``cause``     the original SDK/server exception, when there is one
                (a ``ScalekitServerException`` subclass), so the server error code,
                gRPC status and message are never lost.
"""
from typing import Optional

from scalekit.common.exceptions import ScalekitException

INVALID_CONNECTION_ID = "INVALID_CONNECTION_ID"
CONNECTION_NOT_FOUND = "CONNECTION_NOT_FOUND"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
READ_FAILED = "READ_FAILED"
CONNECTION_UNREADABLE = "CONNECTION_UNREADABLE"
READ_UNAVAILABLE = "READ_UNAVAILABLE"
NOT_AN_AGENTKIT_CONNECTION = "NOT_AN_AGENTKIT_CONNECTION"
INVALID_CONFIGURATION = "INVALID_CONFIGURATION"
CONNECTION_NAME_CONFLICT = "CONNECTION_NAME_CONFLICT"
CONNECTION_IN_USE = "CONNECTION_IN_USE"
PROVIDER_NOT_FOUND = "PROVIDER_NOT_FOUND"
AMBIGUOUS_AUTH_TYPE = "AMBIGUOUS_AUTH_TYPE"
OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"
WRITE_FAILED = "WRITE_FAILED"


class AgentKitConnectionError(ScalekitException):
    """Base class for every error raised by ``client.actions``."""

    code: str = WRITE_FAILED

    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        step: str = "write",
        retryable: bool = False,
        cause: Optional[BaseException] = None,
    ):
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        self.step = step
        self.retryable = retryable
        self.cause = cause

    def __str__(self) -> str:
        text = f"[{self.code}] {self.message} (step={self.step}, retryable={self.retryable})"
        if self.cause is not None:
            server_code = getattr(self.cause, "error_code", None)
            if server_code:
                text += f" | server error code: {server_code}"
        return text


class InvalidConnectionIdError(AgentKitConnectionError):
    code = INVALID_CONNECTION_ID


class ConnectionNotFoundError(AgentKitConnectionError):
    code = CONNECTION_NOT_FOUND


class NotAuthorizedError(AgentKitConnectionError):
    code = NOT_AUTHORIZED


class ConnectionReadError(AgentKitConnectionError):
    """The connection could not be read (server error). Nothing was changed."""

    code = READ_FAILED


class ConnectionUnreadableError(AgentKitConnectionError):
    """The server found the connection but could not return it (for example stored data cannot be decoded).

    Nothing was changed, and retrying will not help. Fix it in the dashboard or contact support
    with the server error details from ``cause``.
    """

    code = CONNECTION_UNREADABLE


class ConnectionUnavailableError(AgentKitConnectionError):
    """The read failed because the service was unavailable or timed out. Nothing was changed."""

    code = READ_UNAVAILABLE


class NotAnAgentKitConnectionError(AgentKitConnectionError):
    """The connection exists but is not an AgentKit connection (for example a login connection)."""

    code = NOT_AN_AGENTKIT_CONNECTION


class InvalidConfigurationError(AgentKitConnectionError):
    """The requested configuration is not valid. Raised before any request is sent when possible."""

    code = INVALID_CONFIGURATION


class ConnectionNameConflictError(AgentKitConnectionError):
    """The connection name is already used, or is reserved."""

    code = CONNECTION_NAME_CONFLICT


class ConnectionInUseError(AgentKitConnectionError):
    """The connection cannot be deleted because connected accounts or MCP configs still use it."""

    code = CONNECTION_IN_USE


class ProviderNotFoundError(AgentKitConnectionError):
    code = PROVIDER_NOT_FOUND


class AmbiguousAuthTypeError(AgentKitConnectionError):
    """The connector has several auth types configured, which AgentKit connections do not support.

    Contact support@scalekit.com if it is a Scalekit provider.
    """

    code = AMBIGUOUS_AUTH_TYPE


class OutcomeUnknownError(AgentKitConnectionError):
    """The request was sent but the outcome is unknown (timeout or service unavailable).

    The change may or may not have been applied. Read the connection to check. Updating,
    deleting, enabling and disabling can be safely repeated. For ``create_connection``, check
    ``list_connections`` before repeating the call.
    """

    code = OUTCOME_UNKNOWN


class ConnectionWriteError(AgentKitConnectionError):
    """The server rejected or failed the change."""

    code = WRITE_FAILED

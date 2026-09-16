
import enum

import grpc
from grpc import StatusCode
from http import HTTPStatus
from grpc_status import rpc_status
from requests.models import Response
from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo


class NonStandardHTTPStatus(enum.IntEnum):
    """HTTP status codes not in the stdlib http.HTTPStatus enum, needed so
    __str__ can read .name/.value the same way it does for every HTTPStatus
    entry in GRPC_TO_HTTP."""
    CLIENT_CLOSED_REQUEST = 499


GRPC_TO_HTTP = {
    StatusCode.OK: HTTPStatus.OK,
    StatusCode.INVALID_ARGUMENT: HTTPStatus.BAD_REQUEST,
    StatusCode.FAILED_PRECONDITION: HTTPStatus.BAD_REQUEST,
    StatusCode.OUT_OF_RANGE: HTTPStatus.BAD_REQUEST,
    StatusCode.UNAUTHENTICATED: HTTPStatus.UNAUTHORIZED,
    StatusCode.PERMISSION_DENIED: HTTPStatus.FORBIDDEN,
    StatusCode.NOT_FOUND: HTTPStatus.NOT_FOUND,
    StatusCode.ALREADY_EXISTS: HTTPStatus.CONFLICT,
    StatusCode.ABORTED: HTTPStatus.CONFLICT,
    StatusCode.RESOURCE_EXHAUSTED: HTTPStatus.TOO_MANY_REQUESTS,
    StatusCode.CANCELLED: NonStandardHTTPStatus.CLIENT_CLOSED_REQUEST,
    StatusCode.DATA_LOSS: HTTPStatus.INTERNAL_SERVER_ERROR,
    StatusCode.UNKNOWN: HTTPStatus.INTERNAL_SERVER_ERROR,
    StatusCode.INTERNAL: HTTPStatus.INTERNAL_SERVER_ERROR,
    StatusCode.UNIMPLEMENTED: HTTPStatus.NOT_IMPLEMENTED,
    StatusCode.UNAVAILABLE: HTTPStatus.SERVICE_UNAVAILABLE,
    StatusCode.DEADLINE_EXCEEDED: HTTPStatus.GATEWAY_TIMEOUT,
}

HTTP_TO_GRPC = {
    HTTPStatus.OK: StatusCode.OK,
    HTTPStatus.BAD_REQUEST: StatusCode.INVALID_ARGUMENT,
    HTTPStatus.UNAUTHORIZED: StatusCode.UNAUTHENTICATED,
    HTTPStatus.FORBIDDEN: StatusCode.PERMISSION_DENIED,
    HTTPStatus.NOT_FOUND: StatusCode.NOT_FOUND,
    HTTPStatus.CONFLICT: StatusCode.ALREADY_EXISTS,
    HTTPStatus.TOO_MANY_REQUESTS: StatusCode.RESOURCE_EXHAUSTED,
    HTTPStatus.INTERNAL_SERVER_ERROR: StatusCode.INTERNAL,
    HTTPStatus.NOT_IMPLEMENTED: StatusCode.UNIMPLEMENTED,
    HTTPStatus.SERVICE_UNAVAILABLE: StatusCode.UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT: StatusCode.DEADLINE_EXCEEDED,
}


HTTP_STATUS = {
    'OK': HTTPStatus.OK,
    'BAD_REQUEST': HTTPStatus.BAD_REQUEST,
    'UNAUTHORIZED': HTTPStatus.UNAUTHORIZED,
    'FORBIDDEN': HTTPStatus.FORBIDDEN,
    'NOT_FOUND': HTTPStatus.NOT_FOUND,
    'CONFLICT': HTTPStatus.CONFLICT,
    'TOO_MANY_REQUESTS': HTTPStatus.TOO_MANY_REQUESTS,
    'INTERNAL_SERVER_ERROR': HTTPStatus.INTERNAL_SERVER_ERROR,
    'NOT_IMPLEMENTED': HTTPStatus.NOT_IMPLEMENTED,
    'SERVICE_UNAVAILABLE': HTTPStatus.SERVICE_UNAVAILABLE,
    'GATEWAY_TIMEOUT': HTTPStatus.GATEWAY_TIMEOUT,
}


class ScalekitException(Exception):
    """ Base class for all scalekit exceptions """
    def __init__(self, error):
        super().__init__(error)


class WebhookVerificationError(ScalekitException):
    """ Exception raised for webhook verification failure """
    def __init__(self, error):
        super().__init__(error)


class ScalekitValidateTokenFailureException(ScalekitException):
    """ Exception raised for token validation failure """
    def __init__(self, error):
        super().__init__(error)


class ScalekitServerException(ScalekitException):
    """ Base class for all scalekit server exceptions """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)
        self._unpacked_details = list()
        if isinstance(error, Response):
            if error.reason and isinstance(error.reason, str):
                self._http_status = HTTP_STATUS.get(error.reason.upper(), HTTPStatus.INTERNAL_SERVER_ERROR)
            else:
                self._http_status = HTTP_STATUS.get('INTERNAL_SERVER_ERROR')
            self._grpc_status = HTTP_TO_GRPC.get(error.status_code, StatusCode.UNKNOWN)
            self._error_code = error.reason
            self._err_details = error.text
            self._message = None
        elif isinstance(error, grpc.RpcError):
            self._grpc_status = error.code()
            # Every current StatusCode is mapped, so this default is latent today —
            # but without it, any future/unmapped code gives None here and __str__
            # crashes on None.name, the same shape as the CANCELLED-as-bare-int bug.
            self._http_status = GRPC_TO_HTTP.get(self._grpc_status, HTTPStatus.INTERNAL_SERVER_ERROR)
            try:
                # rpc_status.from_call raises ValueError (not just returning None)
                # when grpc-status-details-bin is present but internally
                # inconsistent with the call's own code/message — a malformed or
                # tampered status must not crash the exception meant to describe it.
                status = rpc_status.from_call(error)
            except ValueError:
                status = None
            if status:
                self._message = status.message
            else:
                # error.details() is grpc's documented accessor for the plain-text
                # message; str(error) falls back to _InactiveRpcError's multi-line
                # debug repr (or '' for other RpcError subclasses), which is a
                # weaker signal than what details() gives when it's available.
                details_fn = getattr(error, "details", None)
                details_text = details_fn() if callable(details_fn) else None
                self._message = details_text or str(error)
            self._err_details = status.details if status else []
            self._error_code = None

            for detail in self._err_details:
                info = ErrorInfo()
                detail.Unpack(info)
                self._unpacked_details.append(info)
                if not self._error_code:
                    self._error_code = info.error_code

    @staticmethod
    def _extract_error_code(error: grpc.RpcError) -> str | None:
        """ Extract error_code from gRPC trailing metadata without constructing a full exception """
        from grpc_status import rpc_status
        try:
            status = rpc_status.from_call(error)
            if status is None:
                return None
            for detail in status.details:
                info = ErrorInfo()
                detail.Unpack(info)
                if info.error_code:
                    return info.error_code
        except Exception:
            pass
        return None

    @staticmethod
    def promote(error: Response | grpc.RpcError):
        """ Promote a ScalekitServerException (Response or RpcError) to a specific error type """
        grpc_status = HTTP_TO_GRPC.get(error.status_code) if isinstance(error, Response) else error.code()

        # Check for upstream provider errors signaled by error_code == "TOOL_ERROR"
        if isinstance(error, grpc.RpcError):
            error_code = ScalekitServerException._extract_error_code(error)
            if error_code == "TOOL_ERROR":
                if grpc_status == StatusCode.RESOURCE_EXHAUSTED:
                    return ScalekitToolRateLimitException(error)
                elif grpc_status == StatusCode.UNAUTHENTICATED:
                    return ScalekitToolUnauthorizedException(error)
                elif grpc_status == StatusCode.PERMISSION_DENIED:
                    return ScalekitToolForbiddenException(error)
                else:
                    return ScalekitToolException(error)

        if grpc_status == StatusCode.INVALID_ARGUMENT:
            return ScalekitBadRequestException(error)
        elif grpc_status == StatusCode.FAILED_PRECONDITION:
            return ScalekitBadRequestException(error)
        elif grpc_status == StatusCode.OUT_OF_RANGE:
            return ScalekitBadRequestException(error)
        elif grpc_status == StatusCode.UNAUTHENTICATED:
            return ScalekitUnauthorizedException(error)
        elif grpc_status == StatusCode.PERMISSION_DENIED:
            return ScalekitForbiddenException(error)
        elif grpc_status == StatusCode.NOT_FOUND:
            return ScalekitNotFoundException(error)
        elif grpc_status == StatusCode.ALREADY_EXISTS:
            return ScalekitConflictException(error)
        elif grpc_status == StatusCode.ABORTED:
            return ScalekitConflictException(error)
        elif grpc_status == StatusCode.RESOURCE_EXHAUSTED:
            return ScalekitTooManyRequestsException(error)
        elif grpc_status == StatusCode.CANCELLED:
            return ScalekitCancelledException(error)
        elif grpc_status == StatusCode.DATA_LOSS:
            return ScalekitInternalServerException(error)
        elif grpc_status == StatusCode.UNKNOWN:
            return ScalekitInternalServerException(error)
        elif grpc_status == StatusCode.INTERNAL:
            return ScalekitInternalServerException(error)
        elif grpc_status == StatusCode.UNIMPLEMENTED:
            return ScalekitNotImplementedException(error)
        elif grpc_status == StatusCode.UNAVAILABLE:
            return ScalekitServiceUnavailableException(error)
        elif grpc_status == StatusCode.DEADLINE_EXCEEDED:
            return ScalekitGatewayTimeoutException(error)
        else:
            return ScalekitUnknownException(error)

    def __str__(self):
        if self._unpacked_details:
            border = "=" * 40
            details_str = str(self._unpacked_details)
            if details_str.startswith("[") and "\n" in details_str:
                details_str = details_str.replace("[", "[\n", 1)
            return (f"\n{border}\n"
                    f"Error Code: {self._error_code}\n"
                    f"GRPC: ({self._grpc_status.name}: {self._grpc_status.value})\n"
                    f"HTTP: ({self._http_status.name}: {self._http_status.value})\n"
                    f"Error Details:\n"
                    f"{self._message}: {details_str}\n{border}\n")
        else:
            border = "=" * 40
            # _err_details is empty exactly when there was no trailing
            # google.rpc.Status to unpack (e.g. a transport-level failure with
            # no response from the server) — _message is where the real error
            # text lives in that case, so fall back to it rather than printing
            # an empty list and hiding the one thing this render is for.
            return (f"\n{border}\n"
                    f"Error Code: {self._error_code}\n"
                    f"GRPC: ({self._grpc_status.name}: {self._grpc_status.value})\n"
                    f"HTTP: ({self._http_status.name}: {self._http_status.value})\n"
                    f"Error Details: {self._err_details or self._message}\n{border}\n")

    @property
    def http_status(self):
        """ Getter for HTTP status code """
        return self._http_status

    @property
    def error_code(self):
        """ Getter for Error code """
        return self._error_code

    @property
    def err_details(self):
        """ Getter for Error details object """
        return self._err_details

    @property
    def grpc_status(self):
        """ Getter for GRPC status code """
        return self._grpc_status

    @property
    def message(self):
        """ Getter for Exception message """
        return self._message


class ScalekitBadRequestException(ScalekitServerException):
    """ Scalekit Exception raised for bad requests """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitUnauthorizedException(ScalekitServerException):
    """ Scalekit Exception raised for unauthorized access """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitForbiddenException(ScalekitServerException):
    """ Scalekit Exception raised for forbidden access """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitNotFoundException(ScalekitServerException):
    """ Scalekit Exception raised when a resource is not found """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitConflictException(ScalekitServerException):
    """ Scalekit Exception raised for conflicts, such as duplicate resources """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitTooManyRequestsException(ScalekitServerException):
    """ Scalekit Exception raised when too many requests are made in a short time """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitInternalServerException(ScalekitServerException):
    """ Scalekit Exception raised for internal server errors """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitNotImplementedException(ScalekitServerException):
    """ Scalekit Exception raised when a feature is not implemented """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitServiceUnavailableException(ScalekitServerException):
    """ Scalekit Exception raised when the service is unavailable """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitGatewayTimeoutException(ScalekitServerException):
    """ Scalekit Exception raised when a gateway timeout occurs """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitCancelledException(ScalekitServerException):
    """ Scalekit Exception raised when an operation is cancelled """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitUnknownException(ScalekitServerException):
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)


class ScalekitToolException(ScalekitServerException):
    """ Base class for upstream provider tool errors (error_code == 'TOOL_ERROR') """
    def __init__(self, error: Response | grpc.RpcError):
        super().__init__(error)
        # Extract ToolErrorInfo from the unpacked ErrorInfo details
        self._tool_error_code = None
        self._tool_error_message = None
        self._execution_id = None
        for info in self._unpacked_details:
            if info.HasField("tool_error_info"):
                self._tool_error_code = info.tool_error_info.tool_error_code or None
                self._tool_error_message = info.tool_error_info.tool_error_message or None
                self._execution_id = info.tool_error_info.execution_id or None
                break

    @property
    def tool_error_code(self):
        """ Provider-specific error code from tool execution """
        return self._tool_error_code

    @property
    def tool_error_message(self):
        """ Provider-specific error message from tool execution """
        return self._tool_error_message

    @property
    def execution_id(self):
        """ Execution ID for the tool call that failed """
        return self._execution_id


class ScalekitToolRateLimitException(ScalekitToolException, ScalekitTooManyRequestsException):
    """ Provider returned 429/rate-limit during tool execution """
    def __init__(self, error: Response | grpc.RpcError):
        ScalekitToolException.__init__(self, error)


class ScalekitToolUnauthorizedException(ScalekitToolException, ScalekitUnauthorizedException):
    """ Provider returned 401/unauthorized during tool execution """
    def __init__(self, error: Response | grpc.RpcError):
        ScalekitToolException.__init__(self, error)


class ScalekitToolForbiddenException(ScalekitToolException, ScalekitForbiddenException):
    """ Provider returned 403/forbidden during tool execution """
    def __init__(self, error: Response | grpc.RpcError):
        ScalekitToolException.__init__(self, error)

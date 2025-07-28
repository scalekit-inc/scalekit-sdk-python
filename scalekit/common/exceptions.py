
import grpc
from grpc import StatusCode
from http import HTTPStatus
from grpc_status import rpc_status
from requests.models import Response
from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo


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
    StatusCode.CANCELLED: 499,
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
            self._http_status = GRPC_TO_HTTP.get(self._grpc_status)
            self._message = rpc_status.from_call(error).message
            self._err_details = rpc_status.from_call(error).details
            self._error_code = None

            for detail in self._err_details:
                info = ErrorInfo()
                detail.Unpack(info)
                self._unpacked_details.append(info)
                if not self._error_code:
                    self._error_code = info.error_code

    @staticmethod
    def promote(error: Response | grpc.RpcError):
        """ Promote a ScalekitServerException (Response or RpcError) to a specific error type """
        grpc_status = HTTP_TO_GRPC.get(error.status_code) if isinstance(error, Response) else error.code()

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
            return (f"\n{border}\n"
                    f"Error Code: {self._error_code}\n"
                    f"GRPC: ({self._grpc_status.name}: {self._grpc_status.value})\n"
                    f"HTTP: ({self._http_status.name}: {self._http_status.value})\n"
                    f"Error Details: {self._err_details}\n{border}\n")

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

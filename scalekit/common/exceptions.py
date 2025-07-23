
import grpc
from grpc import StatusCode
from http import HTTPStatus
from grpc_status import rpc_status
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


class ScalekitClientException(Exception):
    """ Base class for all scalekit client exceptions """
    pass


class ScalekitServerException(grpc.RpcError):
    """ Common base class for all scalekit exceptions """
    def __init__(self, exception: grpc.RpcError):
        self._grpc_status = exception.code()
        self._http_status = GRPC_TO_HTTP.get(self._grpc_status)
        self._message = rpc_status.from_call(exception).message
        self._err_details = rpc_status.from_call(exception).details
        self._error_code = None

        self._unpacked_details = list()
        for detail in self._err_details:
            info = ErrorInfo()
            detail.Unpack(info)
            self._unpacked_details.append(info)
            if not self._error_code:
                self._error_code = info.error_code

    def __str__(self):
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

    @property
    def grpc_status(self):
        """ Getter for GRPC status code """
        return self._grpc_status

    @property
    def http_status(self):
        """ Getter for HTTP status code """
        return self._http_status

    def error_code(self):
        """ Getter for Error code """
        return self._error_code

    @property
    def message(self):
        """ Getter for Exception message """
        return self._message

    @property
    def err_details(self):
        """ Getter for Error details object """
        return self._err_details


class ScalekitInvalidArgumentException(ScalekitServerException):
    """ Common base class for all non-exit exceptions. """
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitFailedPreconditionException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitNotFoundException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitUnauthenticatedException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitPermissionDeniedException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitInternalServerException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitServiceUnavailableException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitConflictException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitResourceExhaustedException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitUnknownException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitUnimplementedException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitDeadlineExceededException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitDataLossException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitOutOfRangeException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


class ScalekitCancelledException(ScalekitServerException):
    def __init__(self, exception):
        super().__init__(exception)


def scalekit_exception(grpc_error: grpc.RpcError) -> ScalekitServerException:
    grpc_status = grpc_error.code()

    if grpc_status == StatusCode.INVALID_ARGUMENT:
        return ScalekitInvalidArgumentException(grpc_error)
    elif grpc_status == StatusCode.FAILED_PRECONDITION:
        return ScalekitFailedPreconditionException(grpc_error)
    elif grpc_status == StatusCode.OUT_OF_RANGE:
        return ScalekitOutOfRangeException(grpc_error)
    elif grpc_status == StatusCode.UNAUTHENTICATED:
        return ScalekitUnauthenticatedException(grpc_error)
    elif grpc_status == StatusCode.PERMISSION_DENIED:
        return ScalekitPermissionDeniedException(grpc_error)
    elif grpc_status == StatusCode.NOT_FOUND:
        return ScalekitNotFoundException(grpc_error)
    elif grpc_status == StatusCode.ALREADY_EXISTS or grpc_status == StatusCode.ABORTED:
        return ScalekitConflictException(grpc_error)
    elif grpc_status == StatusCode.RESOURCE_EXHAUSTED:
        return ScalekitResourceExhaustedException(grpc_error)
    elif grpc_status == StatusCode.CANCELLED:
        return ScalekitCancelledException(grpc_error)
    elif grpc_status == StatusCode.DATA_LOSS:
        return ScalekitDataLossException(grpc_error)
    elif grpc_status == StatusCode.UNKNOWN:
        return ScalekitUnknownException(grpc_error)
    elif grpc_status == StatusCode.INTERNAL:
        return ScalekitInternalServerException(grpc_error)
    elif grpc_status == StatusCode.UNIMPLEMENTED:
        return ScalekitUnimplementedException(grpc_error)
    elif grpc_status == StatusCode.UNAVAILABLE:
        return ScalekitServiceUnavailableException(grpc_error)
    elif grpc_status == StatusCode.DEADLINE_EXCEEDED:
        return ScalekitDeadlineExceededException(grpc_error)

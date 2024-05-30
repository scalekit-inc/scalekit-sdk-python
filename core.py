from typing import TypeVar, Optional, Protocol

import grpc
import jwt
import json
import requests
import platform
from urllib.parse import urlparse
from grpc_status import rpc_status
from common.scalekit import GrantType
from pkg.scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")
TMetadata = TypeVar("TMetadata")

TOKEN_ENDPOINT = "/oauth/token"
JWKS_ENDPOINT = "/keys"


class WithCall(Protocol):
    def __call__(self, request: TRequest, metadata: TMetadata) -> TResponse: ...


class CoreClient:
    """Class definition for Core Client"""

    sdk_version = "Scalekit-Python/0.1"
    api_version = "20240430"
    user_agent = f"{sdk_version} Python/{platform.python_version()} ({platform.system()}; {platform.architecture()}"

    def __init__(self, env_url, client_id, client_secret):
        """
        Initializer for Core client

        :param env_url        : Environment URL
        :type                 : ``` str ```
        :param client_id      : Client ID
        :type                 : ``` str ```
        :param client_secret  : Client Secret
        :type                 : ``` str ```
        :returns
            None
        """
        parsed_url = urlparse(env_url)
        self.host = parsed_url.netloc
        self.env_url = env_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.keys = None
        self.access_token = None
        self.grpc_secure_channel = None
        self.__authenticate_client()
        self.__grpc_secure_channel()

    def __grpc_secure_channel(self):
        """
        Method to authenticate grpc and create secure grpc channel
        :params
            None
        :returns
            None
        """
        channel_credentials = grpc.ssl_channel_credentials()
        call_credentials = grpc.access_token_call_credentials(self.access_token)
        composite_credentials = grpc.composite_channel_credentials(
            channel_credentials,
            call_credentials,
        )
        self.grpc_secure_channel = grpc.secure_channel(self.host, composite_credentials)

    def __authenticate_client(self):
        """
        Method to authenticate client  and return access token

        :returns
            access_token
        """
        params = {
            "grant_type": GrantType.ClientCredentials.value,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = self.authenticate(data=json.dumps(params))
        response = json.loads(response.content)
        self.access_token = response["access_token"]

    def authenticate(self, data: str):
        """
        Method to execute post request for authentication with given user params

        :param data : params for authentication request
        :type       : ``` str ```
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            self.env_url + TOKEN_ENDPOINT,
            headers=self.get_headers(headers=headers),
            data=json.loads(data),
            verify=True,
        )
        return response

    def get_jwks(self):
        """ Method to get JWT Keys """
        if self.keys and len(self.keys) > 0:
            return
        response = requests.get(
            self.env_url + JWKS_ENDPOINT, headers=self.get_headers()
        )
        response = json.loads(response.content)
        keys = response["keys"]

        for key in keys:
            kid = key["kid"]
            self.keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

    def grpc_exec(
        self,
        func: WithCall,
        data: TRequest,
        retry=1,
    ) -> TResponse:
        try:
            resp = func(
                data,
                metadata=tuple(self.get_headers().items()),
            )
            return resp
        except grpc.RpcError as exp:
            if retry > 0:
                return self.grpc_exec(func, data, retry - 1)
            else:
                status_code = exp.code()
                status = rpc_status.from_call(exp)
                messages = [status.message]
                if status_code == grpc.StatusCode.INVALID_ARGUMENT:
                    for detail in status.details:
                        if detail.Is(ErrorInfo.DESCRIPTOR):
                            info = ErrorInfo()
                            detail.Unpack(info)
                            if info.validation_error_info:
                                for fv in info.validation_error_info.field_violations:
                                    messages.append(f"{fv.field}: {fv.description}")

                raise Exception("\n".join(messages))
        except Exception as exp:
            raise exp

    def get_headers(self, headers: Optional[dict] = None) -> dict:
        """
        Method to get user defined headers and returns collated header params

        :param headers : User defined header dictionary
        :type          : ``` dict ```
        :returns
            dict
        """
        default_headers = {
            "user-agent": f"{self.user_agent}",
            "x-api-version": f"{self.api_version}",
            "x-sdk-version": f"{self.sdk_version}",
        }
        if self.access_token:
            default_headers.update({"authorization": f"Bearer {self.access_token}"})
        if headers:
            return {**default_headers, **headers}
        return default_headers

import time
from typing import TypeVar, Optional, Protocol

import grpc
import jwt
import json
import requests
import platform
from urllib.parse import urlparse

from cryptography.hazmat.primitives import serialization
from grpc_status import rpc_status
from scalekit._version import __version__ as _sdk_version
from scalekit.common.scalekit import GrantType
from scalekit.common.exceptions import ScalekitServerException, ScalekitException
from scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")
TMetadata = TypeVar("TMetadata")

TOKEN_ENDPOINT = "/oauth/token"
JWKS_ENDPOINT = "/keys"


class WithCall(Protocol):
    def __call__(self, request: TRequest, metadata: TMetadata) -> TResponse: ...


class CoreClient:
    """Class definition for Core Client"""

    sdk_version = f"Scalekit-Python/{_sdk_version}"
    # YYYYMMDD
    api_version = "20260603"
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
        self.keys = {}
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

        response = self.authenticate(data=params)
        if response.status_code != 200:
            raise ScalekitServerException.promote(response)
        response = json.loads(response.content)
        self.access_token = response["access_token"]

    def authenticate(self, data: dict):
        """
        Method to execute post request for authentication with given user params

        :param data : params for authentication request
        :type       : ``` str ```
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            self.env_url + TOKEN_ENDPOINT,
            headers=self.get_headers(headers=headers),
            data=data,
            verify=True,
        )
        if response.status_code != 200:
            raise ScalekitServerException.promote(response)
        return response

    def get_jwks(self):
        """Method to get JWT Keys"""
        if self.keys and len(self.keys) > 0:
            return
        response = requests.get(
            self.env_url + JWKS_ENDPOINT, headers=self.get_headers()
        )
        response = json.loads(response.content)
        keys = response["keys"]

        for key in keys:
            kid = key["kid"]
            rsa_key = jwt.PyJWK.from_dict(key).key

            pem_key = rsa_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            self.keys[kid] = pem_key.decode("utf-8")

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

    def _token_needs_refresh(self) -> bool:
        if not self.access_token or not self.access_token.strip():
            return True
        try:
            claims = jwt.decode(self.access_token, options={"verify_signature": False})
            return time.time() >= (float(claims["exp"]) - 300)
        except Exception:
            return True

    @staticmethod
    def _is_tool_error(exp: grpc.RpcError) -> bool:
        """Return True if the error originated from tool execution.

        Tool errors always carry a populated tool_error_info in ErrorInfo.
        This structural check is resilient to server-side error code renames.
        """
        try:
            status = rpc_status.from_call(exp)
            if status is None:
                return False
            for detail in status.details:
                info = ErrorInfo()
                if not detail.Unpack(info):
                    continue
                if info.HasField("tool_error_info"):
                    return True
        except Exception:
            pass
        return False

    def grpc_exec(
        self,
        func: WithCall,
        data: TRequest,
        _retry: int = 2,
    ) -> TResponse:
        if self._token_needs_refresh():
            try:
                self.__authenticate_client()
            except Exception:
                pass  # token still valid within buffer; let call proceed and handle reactively
        try:
            return func(
                data,
                metadata=tuple(self.get_headers().items()),
            )
        except grpc.RpcError as exp:
            if exp.code() == grpc.StatusCode.UNAUTHENTICATED:
                if self._is_tool_error(exp):
                    raise ScalekitServerException.promote(exp)
                if _retry > 0:
                    try:
                        self.__authenticate_client()
                    except Exception:
                        raise ScalekitServerException.promote(exp)
                    return self.grpc_exec(func, data, _retry=_retry - 1)
            elif _retry > 0:
                return self.grpc_exec(func, data, _retry=_retry - 1)
            raise ScalekitServerException.promote(exp)
        except Exception as exp:
            raise ScalekitException(exp)

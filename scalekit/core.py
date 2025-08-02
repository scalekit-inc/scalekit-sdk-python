from typing import TypeVar, Optional, Protocol

import grpc
import jwt
import json
import requests
import platform
from urllib.parse import urlparse

from cryptography.hazmat.primitives import serialization
from scalekit.common.scalekit import GrantType
from scalekit.common.exceptions import ScalekitServerException, ScalekitException

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")
TMetadata = TypeVar("TMetadata")

TOKEN_ENDPOINT = "/oauth/token"
JWKS_ENDPOINT = "/keys"


class WithCall(Protocol):
    def __call__(self, request: TRequest, metadata: TMetadata) -> TResponse: ...


class CoreClient:
    """Class definition for Core Client"""

    sdk_version = "Scalekit-Python/2.3.2"
    api_version = "20250718"
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

        response = self.authenticate(data=json.dumps(params))
        if response.status_code != 200:
            raise ScalekitServerException.promote(response)
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
                return self.grpc_exec(func, data, retry=retry - 1)
            else:
                raise ScalekitServerException.promote(exp)
        except Exception as exp:
            raise ScalekitException(exp)

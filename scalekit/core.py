import random
import time
from typing import TypeVar, Optional, Protocol

import grpc
import jwt
import json
import requests
import platform
from urllib.parse import urlparse

from cryptography.hazmat.primitives import serialization
from scalekit._version import __version__ as _sdk_version
from scalekit.common.scalekit import GrantType
from scalekit.common.exceptions import ScalekitServerException, ScalekitException, ScalekitTooManyRequestsException

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")
TMetadata = TypeVar("TMetadata")

TOKEN_ENDPOINT = "/oauth/token"
JWKS_ENDPOINT = "/keys"

# gRPC call deadline for control-plane RPCs (organizations, users, connections, etc).
# Kept below typical infra timeouts (e.g. GCP LB = 30s) so the SDK surfaces a clean
# DeadlineExceeded error rather than a raw TCP abort on a silently dropped connection.
DEFAULT_TIMEOUT_MS = 20_000

# gRPC call deadline for tool-execution RPCs (ToolsClient / ActionClient.execute_tool,
# ActionClient.request). These proxy to third-party provider APIs (Google Calendar,
# Slack, etc.) and can legitimately run longer than typical control-plane calls, so
# they use their own, longer deadline instead of DEFAULT_TIMEOUT_MS.
DEFAULT_TOOL_TIMEOUT_MS = 60_000


class WithCall(Protocol):
    def __call__(
        self, request: TRequest, metadata: TMetadata, timeout: Optional[float] = None
    ) -> TResponse: ...


class CoreClient:
    """Class definition for Core Client"""

    sdk_version = f"Scalekit-Python/{_sdk_version}"
    # YYYYMMDD
    api_version = "20260603"
    user_agent = f"{sdk_version} Python/{platform.python_version()} ({platform.system()}; {platform.architecture()}"

    def __init__(
        self,
        env_url,
        client_id,
        client_secret,
        timeout_ms: int = DEFAULT_TIMEOUT_MS,
        tool_timeout_ms: int = DEFAULT_TOOL_TIMEOUT_MS,
    ):
        """
        Initializer for Core client

        :param env_url        : Environment URL
        :type                 : ``` str ```
        :param client_id      : Client ID
        :type                 : ``` str ```
        :param client_secret  : Client Secret
        :type                 : ``` str ```
        :param timeout_ms     : gRPC call deadline in ms for control-plane RPCs. Defaults to 20000 (20s).
        :type                 : ``` int ```
        :param tool_timeout_ms : gRPC call deadline in ms for tool-execution RPCs, which proxy to
                                  third-party provider APIs and can legitimately run longer. Defaults to 60000 (60s).
        :type                 : ``` int ```
        :returns
            None
        """
        parsed_url = urlparse(env_url)
        self.host = parsed_url.netloc
        self.env_url = env_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout_ms = timeout_ms
        self.tool_timeout_ms = tool_timeout_ms
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

    def grpc_exec(
        self,
        func: WithCall,
        data: TRequest,
        retry=2,
        attempt=0,
        timeout_ms: Optional[int] = None,
    ) -> TResponse:
        effective_timeout_ms = timeout_ms if timeout_ms is not None else self.timeout_ms
        timeout_seconds = (
            effective_timeout_ms / 1000 if effective_timeout_ms and effective_timeout_ms > 0 else None
        )
        try:
            resp = func(
                data,
                metadata=tuple(self.get_headers().items()),
                timeout=timeout_seconds,
            )
            return resp
        except grpc.RpcError as exp:
            # Check for upstream provider errors first — never retry, never refresh M2M
            error_code = ScalekitServerException._extract_error_code(exp)
            if error_code == "TOOL_ERROR":
                raise ScalekitServerException.promote(exp)

            if exp.code() == grpc.StatusCode.UNAUTHENTICATED:
                if retry <= 0:
                    raise ScalekitServerException.promote(exp)
                try:
                    self.__authenticate_client()
                    return self.grpc_exec(func, data, retry=retry-1, attempt=attempt + 1, timeout_ms=timeout_ms)
                except Exception as refresh_exp:
                    raise ScalekitServerException.promote(exp)
            elif exp.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                # Surface Scalekit rate-limits immediately — retrying triples the damage
                raise ScalekitServerException.promote(exp)
            elif exp.code() == grpc.StatusCode.UNAVAILABLE and retry > 0:
                # Retry transient infrastructure errors with backoff, mirroring the Node SDK.
                base_backoff = min(1 * 2 ** attempt, 30)
                backoff_seconds = base_backoff * (0.5 + random.random() * 0.5)
                time.sleep(backoff_seconds)
                return self.grpc_exec(func, data, retry=retry - 1, attempt=attempt + 1, timeout_ms=timeout_ms)
            elif retry > 0:
                return self.grpc_exec(func, data, retry=retry - 1, attempt=attempt + 1, timeout_ms=timeout_ms)
            else:
                raise ScalekitServerException.promote(exp)
        except Exception as exp:
            raise ScalekitException(exp)

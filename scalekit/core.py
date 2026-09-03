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

# Must clear the backend's EnforcementPolicy.MinTime (30s, scalekit's
# cmd/grpc.go) with real margin, not just match it: grpc-core pings on this
# exact interval for as long as the channel is open (keepalive_permit_without_calls
# below), so a value equal to MinTime leaves zero room for jitter between the
# client's timer and the server's strike window — one early ping is a strike,
# three and the server GOAWAYs the connection, recreating the bug this fixes.
# 60s matches the Java SDK's default for the same reason.
DEFAULT_KEEPALIVE_TIME_MS = 60_000
DEFAULT_KEEPALIVE_TIMEOUT_MS = 10_000

# The Scalekit backend's EnforcementPolicy.MinTime is 30s, so any keepalive
# below 30s is treated as abuse and the server GOAWAYs the connection. (gRPC
# also silently clamps sub-10s values up to 10s per grpc/proposal A8, so a
# small value never even reaches the wire as requested.) Reject 1..29999.
MIN_KEEPALIVE_TIME_MS = 30_000

# requests defaults to no timeout, so a black-holed connection blocks the
# calling thread until the OS abandons the socket. Bound the connect and read
# phases separately with a (connect, read) tuple.
DEFAULT_HTTP_CONNECT_TIMEOUT_S = 10
DEFAULT_HTTP_READ_TIMEOUT_S = 30
DEFAULT_HTTP_TIMEOUT = (DEFAULT_HTTP_CONNECT_TIMEOUT_S, DEFAULT_HTTP_READ_TIMEOUT_S)


class WithCall(Protocol):
    def __call__(self, request: TRequest, metadata: TMetadata) -> TResponse: ...


class CoreClient:
    """Class definition for Core Client"""

    sdk_version = f"Scalekit-Python/{_sdk_version}"
    # YYYYMMDD
    api_version = "20260727"
    user_agent = f"{sdk_version} Python/{platform.python_version()} ({platform.system()}; {platform.architecture()}"

    def __init__(
        self,
        env_url,
        client_id,
        client_secret,
        keepalive_time_ms: int = DEFAULT_KEEPALIVE_TIME_MS,
        keepalive_timeout_ms: int = DEFAULT_KEEPALIVE_TIMEOUT_MS,
    ):
        """
        Initializer for Core client

        :param env_url               : Environment URL
        :type                        : ``` str ```
        :param client_id             : Client ID
        :type                        : ``` str ```
        :param client_secret         : Client Secret
        :type                        : ``` str ```
        :param keepalive_time_ms     : How often, in milliseconds, an idle gRPC
                                        connection is verified before reuse.
                                        Must stay above the backend's keepalive
                                        MinTime (30s) with real margin, or the
                                        server treats this ping as abuse. Defaults
                                        to 60000. Set to 0 to disable keepalive
                                        entirely.
        :type                        : ``` int ```
        :param keepalive_timeout_ms  : How long, in milliseconds, to wait for a
                                        keepalive response before treating an
                                        idle connection as dead. Defaults to
                                        10000.
        :type                        : ``` int ```
        :returns
            None
        """
        parsed_url = urlparse(env_url)
        self.host = parsed_url.netloc
        self.env_url = env_url
        self.client_id = client_id
        self.client_secret = client_secret
        # 0 means "disabled" and is allowed through deliberately; only 1..29999
        # is rejected, because the Scalekit server rejects keepalive below its
        # 30s MinTime as abusive (and gRPC silently raises sub-10s values to
        # 10s, so a small value is never what the caller asked for anyway).
        if keepalive_time_ms and keepalive_time_ms < MIN_KEEPALIVE_TIME_MS:
            raise ValueError(
                f"keepalive_time_ms must be 0 (disabled) or >= {MIN_KEEPALIVE_TIME_MS}; "
                f"got {keepalive_time_ms}. The Scalekit server rejects keepalive below "
                "its 30s MinTime as abusive, and gRPC silently raises sub-10s values to 10s."
            )
        self.keepalive_time_ms = keepalive_time_ms
        self.keepalive_timeout_ms = keepalive_timeout_ms
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
        # keepalive_time_ms == 0 disables keepalive entirely: no options are
        # passed, so grpc-core falls back to its own defaults (no idle pings).
        channel_options = []
        if self.keepalive_time_ms:
            # keepalive_permit_without_calls=1 so an idle channel is still
            # periodically verified: without it, grpc-core only sends HTTP/2
            # keepalive PINGs while there are active calls, so a connection
            # silently dropped by a network intermediary while idle isn't
            # detected until the next real call is written to it.
            channel_options = [
                ('grpc.keepalive_time_ms', self.keepalive_time_ms),
                ('grpc.keepalive_timeout_ms', self.keepalive_timeout_ms),
                ('grpc.keepalive_permit_without_calls', 1),
                ('grpc.http2.max_pings_without_data', 0),
            ]
        self.grpc_secure_channel = grpc.secure_channel(
            self.host, composite_credentials, options=channel_options
        )

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
            timeout=DEFAULT_HTTP_TIMEOUT,
        )
        if response.status_code != 200:
            raise ScalekitServerException.promote(response)
        return response

    def get_jwks(self):
        """Method to get JWT Keys"""
        if self.keys and len(self.keys) > 0:
            return
        response = requests.get(
            self.env_url + JWKS_ENDPOINT,
            headers=self.get_headers(),
            timeout=DEFAULT_HTTP_TIMEOUT,
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
    ) -> TResponse:
        try:
            resp = func(
                data,
                metadata=tuple(self.get_headers().items()),
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
                    return self.grpc_exec(func, data, retry=retry-1)
                except Exception as refresh_exp:
                    raise ScalekitServerException.promote(exp)
            elif exp.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                # Surface Scalekit rate-limits immediately — retrying triples the damage
                raise ScalekitServerException.promote(exp)
            elif retry > 0:
                return self.grpc_exec(func, data, retry=retry - 1)
            else:
                raise ScalekitServerException.promote(exp)
        except Exception as exp:
            raise ScalekitException(exp)

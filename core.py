from typing import TypeVar, Callable

import grpc
import jwt
import json
import requests
from authlib.jose import JsonWebKey
from grpc_status import rpc_status

from options.scalekit import GrantType
from pkg.scalekit.v1.errdetails.errdetails_pb2 import ErrorInfo

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")

TOKEN_ENDPOINT = '/oauth/token'
JWT_KEYS_ENDPOINT = "/keys"


class CoreClient:
    """ Class definition for Core Client """
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
        try:
            self.keys: JsonWebKey = []
            self.public_keys = {}
            self.env_url = env_url
            self.client_id = client_id
            self.client_secret = client_secret
        except Exception as exp:
            raise exp

    def authenticate_client(self):
        """
        Method to authenticate client  and return access token
        
        :returns
            access_token
        """
        try:
            params = {
                "grant_type": GrantType.ClientCredentials.value,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }

            response = self.authenticate(data=json.dumps(params))
            response = json.loads(response.content)
            return response['access_token']
        except Exception as exp:
            raise exp

    def authenticate(self, data: str):
        """
        Method to execute post request for authentication with given user params
        
        :param data : params for authentication request
        :type       : ``` str ```
        """
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(self.env_url + TOKEN_ENDPOINT, headers=headers, data=json.loads(data), verify=True)
            return response
        except Exception as exp:
            raise exp

    def get_jwks(self):
        """ Method to get JWT Keys """
        try:
            if self.keys:
                return
            response = requests.get(self.env_url + JWT_KEYS_ENDPOINT)
            response = json.loads(response.content)
            self.keys = response['keys']
            print(response)
            print(self.keys)

            for jwk in self.keys:
                kid = jwk['kid']
                self.public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        except Exception as exp:
            raise exp

    @staticmethod
    def grpc_exec(func: Callable[[TRequest], TResponse], data: TRequest, retry=1) -> TResponse:
        try:
            val = func(data)
            return val
        except grpc.RpcError as exp:
            if retry > 0:
                print('Trial:' + str(retry))
                return CoreClient.grpc_exec(func, data, retry - 1)
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
                                    messages.append(f'{fv.field}: {fv.description}')

                raise Exception('\n'.join(messages))

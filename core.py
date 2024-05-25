
import jwt
import json
import requests
from authlib.jose import JsonWebKey

from options.scalekit import GrantType

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
        self.keys: JsonWebKey = []
        self.public_keys = {}
        self.env_url = env_url
        self.client_id = client_id
        self.client_secret = client_secret

    def authenticate_client(self):
        """
        Method to authenticate client  and return access token
        
        :returns
            access_token
        """
        params = {
            "grant_type": GrantType.ClientCredentials.value,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = self.authenticate(data=json.dumps(params))
        response = json.loads(response.content)
        return response['access_token']

    def authenticate(self, data: str):
        """
        Method to execute post request for authentication with given user params
        
        :param data : params for authentication request
        :type       : ``` str ```
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.env_url + TOKEN_ENDPOINT, headers=headers, data=json.loads(data))
        return response

    def get_jwks(self):
        """ Method to get JWT Keys """
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

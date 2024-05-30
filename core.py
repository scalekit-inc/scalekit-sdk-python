
import json
import requests
from jose import jwt, jwk

from types.scalekit import GrantType

TOKEN_ENDPOINT = '/oauth/token'
JWT_KEYS_ENDPOINT = "/keys"


class CoreClient:
    """ """
    def __init__(self, env_url, client_id, client_secret):
        """ """
        self.keys: jwk = []
        self.env_url = env_url
        self.client_id = client_id
        self.client_secret = client_secret

    def authenticate_client(self):
        """ """
        params = {
            "grant_type": GrantType.ClientCredentials.value,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = self.authenticate(data=json.dumps(params))
        response = json.loads(response.content)
        return response['access_token']

    async def authenticate(self, data: str):
        """ """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.env_url + TOKEN_ENDPOINT, headers=headers, data=json.loads(data), verify=True)
        return response

    async def get_jwks(self):
        """ """
        if self.keys:
            return
        response = requests.get(self.env_url + JWT_KEYS_ENDPOINT)
        response = json.loads(response.content)
        self.keys = response

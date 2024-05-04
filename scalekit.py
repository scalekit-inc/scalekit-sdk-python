import json
from urllib.parse import urlencode

import jose.jwt

from constants.user import *
from core import CoreClient
from domain import DomainClient
from connection import ConnectionClient
from organization import OrganizationClient
from types.scalekit import AuthorizationUrlOptions, CodeAuthenticationOptions, GrantType


AUTHORIZE_ENDPOINT = "oauth/authorize"


class Scalekit:
    """ """
    def __init__(self, env_url: str, client_id: str, client_secret: str):
        """ """
        # self.env_url = env_url
        # self.client_id = client_id
        # self.client_secret = client_secret
        self.core_client = CoreClient(env_url=env_url, client_id=client_id, client_secret=client_secret)
        self.domain_client = DomainClient(env_url=env_url, client_id=client_id, client_secret=client_secret)
        self.connection_client = ConnectionClient(env_url=env_url, client_id=client_id, client_secret=client_secret)
        self.organization_client = OrganizationClient(env_url=env_url, client_id=client_id, client_secret=client_secret)

    def get_authorization_url(self, redirect_uri: str, options: AuthorizationUrlOptions | None):
        """ """
        scopes = options.scopes | ["openid", "profile"]
        query_string = urlencode({
            'response_type': 'code',
            'client_id': self.core_client.env_url,
            'redirect_uri': redirect_uri,
            'scope': scopes.join(" "),
            'state': options.state | None,
            'nonce': options.nonce | None,
            'login_hint': options.login_hint | None,
            'domain_hint': options.domain_hint | None,
            'connection_id': options.connection_id | None,
            'organization_id': options.organization_id | None
        })

        return f'{self.core_client.env_url}/{AUTHORIZE_ENDPOINT}?{query_string}'

    async def authenticate_with_code(self, options: CodeAuthenticationOptions):
        """ """
        response = self.core_client.authenticate(json.dumps({
            'code': options.code,
            'redirect_uri': options.redirect_uri,
            'grant_type': GrantType.AuthorizationCode.value,
            'client_id': self.core_client.client_id,
            'client_secret': self.core_client.client_secret,
            'code_verifier': options.code_verifier | None,
        }))
        response = json.loads(response.content)
        id_token = response['id_token']
        access_token = response['access_token']

        claims = jose.jwt.decode(id_token, self.core_client.keys)
        user = {}
        for k,v in claims.items():
            if id_token_claim_to_user_map[k]:
                user[id_token_claim_to_user_map[k]] = v

        user.update({'id_token': id_token})
        user.update({'access_token': access_token})
        return user

    async def validate_access_token(self, token: str) -> bool:
        """ """
        await self.core_client.get_jwks()

        try:
            claims = jose.jwt.decode(token, self.core_client.keys)
            return True
        except jose.JWTError:
            print('token verification failed!')
            return False

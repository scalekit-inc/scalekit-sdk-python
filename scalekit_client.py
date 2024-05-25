import json
from urllib.parse import urlencode

import jwt
from constants.user import *
from core import CoreClient
from domain import DomainClient
from connection import ConnectionClient
from organization import OrganizationClient
from options.scalekit import AuthorizationUrlOptions, CodeAuthenticationOptions, GrantType


AUTHORIZE_ENDPOINT = "oauth/authorize"


class Scalekit:
    """ """
    def __init__(self, env_url: str, client_id: str, client_secret: str):
        """
        Initializer for Scalekit base class 
        
        :param env_url        : ``` str ```
        :param client_id      : ``` str ```
        :param client_secret  : ``` str ```
        :returns
            None
        """
        try:
            self.core_client = CoreClient(env_url=env_url, client_id=client_id, client_secret=client_secret)
            self.domain_client = DomainClient(
                env_url=env_url, client_id=client_id, client_secret=client_secret)
            self.connection_client = ConnectionClient(
                env_url=env_url, client_id=client_id, client_secret=client_secret)
            self.organization_client = OrganizationClient(
                env_url=env_url, client_id=client_id, client_secret=client_secret)
        except Exception as exp:
            raise exp

    def get_authorization_url(self, redirect_uri: str, options: AuthorizationUrlOptions | None):
        """
        Method to get authorization URL
        
        :param redirect_uri : ``` str```
        :param options      : ``` Auth URL options ```
        :returns
            Authorization URL 
        """
        try:
            scopes = options.scopes if options.scopes else ["openid", "profile"]
            query_string = urlencode({
                'response_type': 'code',
                'client_id': self.core_client.client_id,
                'redirect_uri': redirect_uri,
                'scope': " ".join(scopes),
                'state': options.state,
                'nonce': options.nonce,
                'login_hint': options.login_hint,
                'domain_hint': options.domain_hint,
                'connection_id': options.connection_id,
                'organization_id': options.organization_id
            })

            return f'{self.core_client.env_url}/{AUTHORIZE_ENDPOINT}?{query_string}'
        except Exception as exp:
            raise exp

    def authenticate_with_code(self, options: CodeAuthenticationOptions):
        """
        Method to authenticate with code options
        
        :param options: ``` CodeAuthenticationOptions ```
        :returns:
            dict with user and id/access token 
        """
        try:
            response = self.core_client.authenticate(json.dumps({
                'code': options.code,
                'redirect_uri': options.redirect_uri,
                'grant_type': GrantType.AuthorizationCode.value,
                'client_id': self.core_client.client_id,
                'client_secret': self.core_client.client_secret,
                'code_verifier': options.code_verifier,
            }))
            response = json.loads(response.content)
            id_token = response['id_token']
            access_token = response['access_token']

            self.core_client.get_jwks()
            kid = jwt.get_unverified_header(id_token)['kid']
            key = self.core_client.public_keys[kid]

            claims = jwt.decode(id_token, key=key, options={'verify_aud': False})
            user = {}
            for k, v in claims.items():
                if id_token_claim_to_user_map.get(k, None):
                    user[id_token_claim_to_user_map[k]] = v

            return {'user': user, 'id_token': id_token, 'access_token': access_token}

        except Exception as exp:
            raise exp

    def validate_access_token(self, token: str) -> bool:
        """
        Method to validate access token

        :param token : ``` str ```
        :returns
            None
        """
        try:
            self.core_client.get_jwks()

            try:
                claims = jwt.decode(token, self.core_client.keys)
                return True
            except jwt.exceptions.InvalidTokenError:
                print('token verification failed!')
                return False

        except Exception as exp:
            raise exp

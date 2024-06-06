import json
from urllib.parse import urlencode

import jwt
from scalekit.core import CoreClient
from scalekit.domain import DomainClient
from scalekit.connection import ConnectionClient
from scalekit.organization import OrganizationClient
from scalekit.common.scalekit import (
    AuthorizationUrlOptions,
    CodeAuthenticationOptions,
    GrantType,
)
from scalekit.constants.user import id_token_claim_to_user_map

AUTHORIZE_ENDPOINT = "oauth/authorize"


class ScalekitClient:
    """ """

    def __init__(self, env_url: str, client_id: str, client_secret: str):
        """
        Initializer for Scalekit base class

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
            self.core_client = CoreClient(
                env_url=env_url, client_id=client_id, client_secret=client_secret
            )
            self.domain = DomainClient(self.core_client)
            self.connection = ConnectionClient(self.core_client)
            self.organization = OrganizationClient(self.core_client)
        except Exception as exp:
            raise exp

    def get_authorization_url(
        self, redirect_uri: str, options: AuthorizationUrlOptions | None
    ):
        """
        Method to get authorization URL

        :param redirect_uri   : Redirect URI for SAML SSO
        :type                 : ``` str ```
        :param options        : ``` Auth URL options object```
        :type                 : ``` obj ```
        :returns
            Authorization URL
        """
        try:
            scopes = (
                options.scopes if options.scopes else ["openid", "profile", "email"]
            )
            query_string = urlencode(
                {
                    "response_type": "code",
                    "client_id": self.core_client.client_id,
                    "redirect_uri": redirect_uri,
                    "scope": " ".join(scopes),
                    "state": options.state,
                    "nonce": options.nonce,
                    "login_hint": options.login_hint,
                    "domain_hint": options.domain_hint,
                    "connection_id": options.connection_id,
                    "organization_id": options.organization_id,
                }
            )

            return f"{self.core_client.env_url}/{AUTHORIZE_ENDPOINT}?{query_string}"
        except Exception as exp:
            raise exp

    def authenticate_with_code(
        self, code, redirect_uri, options: CodeAuthenticationOptions
    ):
        """
        Method to authenticate with code options

        :param code           : authorization_code
        :type                 : ``` str ```
        :param redirect_uri   : Redirect URI
        :type                 : ``` str ```
        :param options        : ``` CodeAuthenticationOptions Object ```
        :type                 : ``` obj ```
        :returns:
            dict with user, id token & access token
        """
        try:
            response = self.core_client.authenticate(
                json.dumps(
                    {
                        "code": code,
                        "redirect_uri": redirect_uri,
                        "grant_type": GrantType.AuthorizationCode.value,
                        "client_id": self.core_client.client_id,
                        "client_secret": self.core_client.client_secret,
                        "code_verifier": options.code_verifier,
                    }
                )
            )
            response = json.loads(response.content)
            id_token = response["id_token"]
            access_token = response["access_token"]

            self.core_client.get_jwks()
            kid = jwt.get_unverified_header(id_token)["kid"]
            key = self.core_client.keys[kid]
            claims = jwt.decode(
                id_token, key=key, algorithms="RS256", options={"verify_aud": False}
            )
            user = {}
            for k, v in claims.items():
                if id_token_claim_to_user_map.get(k, None):
                    user[id_token_claim_to_user_map[k]] = v

            return {"user": user, "id_token": id_token, "access_token": access_token}

        except Exception as exp:
            raise exp

    def validate_access_token(self, token: str) -> bool:
        """
        Method to validate access token

        :param token : access token
        :type        : ``` str ```
        :returns
            bool
        """
        self.core_client.get_jwks()
        try:
            jwt.decode(token, self.core_client.keys)
            return True
        except jwt.exceptions.InvalidTokenError:
            return False

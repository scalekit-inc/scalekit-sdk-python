import json
from typing import Dict, Tuple
from urllib.parse import urlencode

import jwt
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
from core import CoreClient
from domain import DomainClient
from connection import ConnectionClient
from organization import OrganizationClient
from directory import DirectoryClient
from common.scalekit import (
    AuthorizationUrlOptions,
    CodeAuthenticationOptions,
    GrantType,
)
from constants.user import id_token_claim_to_user_map

AUTHORIZE_ENDPOINT = "oauth/authorize"
webhook_tolerance_in_seconds = timedelta(minutes=5)  # Check on this
webhook_signature_version = "v1"


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
            self.directory = DirectoryClient(self.core_client)
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
            url_params_dict = {
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
                    "provider": options.provider,
            }

            valid_auth_params = {k: v for k, v in url_params_dict.items() if v}
            query_string = urlencode(valid_auth_params)

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

    def verify_webhook_payload(self, secret: str, headers: Dict[str, str], payload: bytes) -> Tuple[bool, Exception]:
        """ """
        webhook_id = headers.get("webhook-id")
        webhook_timestamp = headers.get("webhook-timestamp")
        webhook_signature = headers.get("webhook-signature")

        if not all([webhook_id, webhook_timestamp, webhook_signature]):
            return False, Exception("Missing required headers")

        secret_parts = secret.split("_")
        if len(secret_parts) < 2:
            return False, Exception("Invalid secret")

        try:
            secret_bytes = base64.b64decode(secret_parts[1])
        except Exception as e:
            return False, e

        try:
            timestamp = self.verify_timestamp(webhook_timestamp)
        except Exception as e:
            return False, e

        data = f"{webhook_id}.{timestamp}.{payload.decode('utf-8')}"
        computed_signature = self.compute_signature(secret_bytes, data)

        received_signatures = webhook_signature.split(" ")
        for versioned_signature in received_signatures:
            signature_parts = versioned_signature.split(",")
            if len(signature_parts) < 2:
                continue

            version = signature_parts[0]
            signature = signature_parts[1]

            if version != webhook_signature_version:
                continue

            if hmac.compare_digest(signature.encode('utf-8'), computed_signature.encode('utf-8')):
                return True, None

        return False, Exception("Invalid signature")

    @staticmethod
    def verify_timestamp(timestamp_str: str):
        """ """
        now = datetime.now()
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError as e:
            return None, e

        if timestamp < (now - webhook_tolerance_in_seconds):
            return None, Exception("Message timestamp too old")

        if timestamp > (now + webhook_tolerance_in_seconds):
            return None, Exception("Message timestamp too new")

        return timestamp, None

    @staticmethod
    def compute_signature(secret: bytes, data: str) -> str:
        """ """
        hash_object = hmac.new(secret, data.encode('utf-8'), hashlib.sha256)
        signature = hash_object.digest()
        return base64.b64encode(signature).decode('utf-8')

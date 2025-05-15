
import json
from math import floor
from typing import Any, Optional, Dict
from urllib.parse import urlencode

import jwt
import hmac
import hashlib
import base64
from datetime import datetime, timedelta, timezone
from scalekit.core import CoreClient
from scalekit.domain import DomainClient
from scalekit.connection import ConnectionClient
from scalekit.m2m_client import M2MClient
from scalekit.organization import OrganizationClient
from scalekit.directory import DirectoryClient
from scalekit.common.scalekit import (
    AuthorizationUrlOptions,
    CodeAuthenticationOptions,
    GrantType,
    IdpInitiatedLoginClaims,
)
from scalekit.constants.user import id_token_claim_to_user_map

AUTHORIZE_ENDPOINT = "oauth/authorize"
webhook_tolerance_in_seconds = timedelta(minutes=5)
webhook_signature_version = "v1"


class WebhookVerificationError(Exception):
    pass


class ScalekitClient:
    """ Class definition for scalekit client """

    def __init__(self, env_url: str, client_id: str, client_secret: str):
        """
        Initializer for Scalekit base class

        :param env_url        : Environment URL
        :type                 : ``` str ```
        :param client_id      : Client ID
        :type                 : ``` str ```
        :param client_secret  : Client Secret
        :type                 : ``` str ```

        :returns:
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
            self.m2m_client = M2MClient(self.core_client)
        except Exception as exp:
            raise exp

    def get_authorization_url(
        self, redirect_uri: str, options: AuthorizationUrlOptions | None
    ):
        """
        Method to get authorization URL

        :param redirect_uri   : Redirect URI for SAML SSO
        :type                 : ``` str ```
        :param options        : Auth URL options object
        :type                 : ``` obj ```

        :returns:
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
        :param options        : CodeAuthenticationOptions Object
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
            # Validate id_token
            claims = self.__validate_token(id_token, {"verify_aud": False})
            user = {}
            connection_id = claims['amr'][0]
            organization_id = claims['oid']
            for k, v in claims.items():
                if id_token_claim_to_user_map.get(k, None):
                    user[id_token_claim_to_user_map[k]] = v

            return {
                "user": user,
                "id_token": id_token,
                "access_token": access_token,
                "connection_id": connection_id,
                "organization_id": organization_id
            }

        except Exception as exp:
            raise exp

    def validate_access_token(self, token: str) -> bool:
        """
        Method to validate access token

        :param token : access token
        :type        : ``` str ```

        :returns:
            bool
        """
        try:
            self.__validate_token(token)
            return True
        except jwt.exceptions.InvalidTokenError:
            return False

    def generate_client_token(self, client_id: str, client_secret: str) -> str:
        """
        Method to generate access token

        :param client_id        : Client Id for access token
        :type                           : ``` str ```
        :param client_secret : Client Secret for access token
        :type                            : ``` str ```
        :returns:
            access token
        """
        try:
            response = self.core_client.authenticate(
                json.dumps(
                    {
                        "grant_type": GrantType.ClientCredentials.value,
                        "client_id": client_id,
                        "client_secret": client_secret,
                    }
                )
            )
            response = json.loads(response.content)
            return response
        except Exception as exp:
            raise exp

    def validate_access_token_and_get_claims(self, token: str, options: Optional[Dict] = None, audience = None) -> Dict[str, Any]:
        """
        Method to validate access token and get claims

        :param token : access token
        :type        : ``` str ```

        :returns:
            claims
        """

        options = options if options else {}
        options["verify_aud"] = False if not audience else True
        
        try:
            claims = self.__validate_token(token, options=options, audience=audience)
            return claims
        except Exception as exp:
            raise exp        

    def get_idp_initiated_login_claims(self, idp_initiated_login_token: str) -> IdpInitiatedLoginClaims:
        """
        Method to get IDP initiated login claims

        :param idp_initiated_login_token : IDP initiated login token
        :type        : ``` str ```

        :returns:
            ``` IdpInitiatedLoginClaims ```
        """
        try:
            claims = self.__validate_token(idp_initiated_login_token, {"verify_aud": False})
            return claims
        except Exception as exp:
            raise exp

    def __validate_token(
        self, token: str, options: Optional[Dict] = None, audience: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Method to validate token

        :param token : token
        :type        : ``` str ```

        :returns:
            payload
        """
        self.core_client.get_jwks()
        kid = jwt.get_unverified_header(token)["kid"]
        key = self.core_client.keys[kid]

        return jwt.decode(token, key=key, algorithms="RS256", options=options, audience=audience)

    def verify_webhook_payload(self, secret: str, headers: Dict[str, str], payload: [str | bytes]) -> bool:
        """
        Method to verify webhook payload

        :param secret      :     Secret for webhook verification
        :type              :     ``` str ```
        :param headers     :     Webhook request headers
        :type              :     ``` dict[str, str] ```
        :param payload     :     Webhook payload in str or bytes
        :type              :     ``` str | bytes ```

        :returns:
            bool
        """
        payload = payload if isinstance(payload, str) else payload.decode()
        webhook_id = headers.get("webhook-id")
        webhook_timestamp = headers.get("webhook-timestamp")
        webhook_signature = headers.get("webhook-signature")

        if not all([webhook_id, webhook_timestamp, webhook_signature]):
            raise WebhookVerificationError("Missing required headers")

        secret_parts = secret.split("_")
        if len(secret_parts) < 2:
            raise WebhookVerificationError("Invalid secret")

        try:
            secret_bytes = base64.b64decode(secret_parts[1])
        except Exception as exp:
            raise exp

        try:
            timestamp = self.__verify_timestamp(webhook_timestamp)
        except Exception as exp:
            raise exp

        timestamp_str = str(floor(timestamp.replace(tzinfo=timezone.utc).timestamp()))
        data = f"{webhook_id}.{timestamp_str}.{payload}"
        computed_signature = base64.b64decode(self.__compute_signature(secret_bytes, data).split(',')[1])

        received_signatures = webhook_signature.split(" ")
        for versioned_signature in received_signatures:
            signature_parts = versioned_signature.split(",")
            if len(signature_parts) < 2:
                continue

            version = signature_parts[0]
            signature = base64.b64decode(signature_parts[1])

            if version != webhook_signature_version:
                continue

            if hmac.compare_digest(signature, computed_signature):
                return True

        raise WebhookVerificationError("Invalid signature")

    @staticmethod
    def __verify_timestamp(timestamp_str: str):
        """
        Method to verify time stamp

        :param timestamp_str   :     Timestamp for verification
        :type                  :     ``` str ```

        :returns:
            None
        """
        now = datetime.now(tz=timezone.utc)
        try:
            timestamp = datetime.fromtimestamp(float(timestamp_str), tz=timezone.utc)
        except Exception:
            raise WebhookVerificationError("Invalid Signature Headers")

        if timestamp < (now - webhook_tolerance_in_seconds):
            raise Exception("Message timestamp too old")

        if timestamp > (now + webhook_tolerance_in_seconds):
            raise Exception("Message timestamp too new")

        return timestamp

    @staticmethod
    def __compute_signature(secret: bytes, data: str) -> str:
        """
        Method to compute signature

        :param secret   :     secret for signature
        :type           :     ``` bytes ```
        :param data     :     data for signature
        :type           :     ``` str ```

        :returns:
            None
        """
        signature = hmac.new(secret, data.encode(), hashlib.sha256).digest()
        return f"v1, {base64.b64encode(signature).decode('utf-8')}"

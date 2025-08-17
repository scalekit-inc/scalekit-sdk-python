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
from scalekit.users import UserClient
from scalekit.role import RoleClient
from scalekit.connected_accounts import ConnectedAccountsClient
from scalekit.tools import ToolsClient
from scalekit.connect import ConnectClient
from scalekit.passwordless import PasswordlessClient
from scalekit.mcp import McpClient
from scalekit.common.scalekit import (
    AuthorizationUrlOptions,
    CodeAuthenticationOptions,
    GrantType,
    IdpInitiatedLoginClaims,
    LogoutUrlOptions,
    TokenValidationOptions,
)
from scalekit.constants.user import id_token_claim_to_user_map
from scalekit.common.exceptions import (WebhookVerificationError,
                                        ScalekitValidateTokenFailureException)

AUTHORIZE_ENDPOINT = "oauth/authorize"
LOGOUT_ENDPOINT = "oidc/logout" 
webhook_tolerance_in_seconds = timedelta(minutes=5)
webhook_signature_version = "v1"


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
                env_url=env_url, client_id=client_id, client_secret=client_secret)
            self.domain = DomainClient(self.core_client)
            self.connection = ConnectionClient(self.core_client)
            self.organization = OrganizationClient(self.core_client)
            self.directory = DirectoryClient(self.core_client)
            self.m2m_client = M2MClient(self.core_client)
            self.users = UserClient(self.core_client)
            self.roles = RoleClient(self.core_client)
            self.connected_accounts = ConnectedAccountsClient(self.core_client)
            self.tools = ToolsClient(self.core_client)
            self.mcp = McpClient(self.core_client)
            self.connect = ConnectClient(self.tools, self.connected_accounts, self.mcp)
            self.passwordless = PasswordlessClient(self.core_client)
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
                "prompt": options.prompt,  
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
            dict with user, id token, optionally access token & refresh token
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
            refresh_token = response.get("refresh_token")
            # Validate id_token
            claims = self.__validate_token(id_token, options=None)
            user = {}
            amr_claims = claims.get('amr', [])
            connection_id = amr_claims[0] if amr_claims else None
            organization_id = claims.get('oid')
            for k, v in claims.items():
                if id_token_claim_to_user_map.get(k, None):
                    user[id_token_claim_to_user_map[k]] = v

            return {
                "user": user,
                "id_token": id_token,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "connection_id": connection_id,
                "organization_id": organization_id
            }

        except jwt.exceptions.InvalidTokenError as exp:
            raise ScalekitValidateTokenFailureException(exp)
        except Exception as exp:
            raise exp

    def validate_access_token(self, token: str, options: Optional[TokenValidationOptions] = None, audience = None) -> bool:
        """
        Method to validate access token

        :param token : access token
        :type        : ``` str ```
        :param options : Optional validation options for issuer, audience, and scopes
        :type        : ``` TokenValidationOptions ```
        :param audience : audience for validation (deprecated, use options.audience instead)
        :type        : ``` str ```

        :returns:
            bool
        """
        try:
            self.validate_token(token, options=options, audience=audience)
            return True
        except Exception:
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

    def validate_access_token_and_get_claims(self, token: str, options: Optional[TokenValidationOptions] = None, audience = None) -> Dict[str, Any]:
        """
        Method to validate access token and get claims

        :param token : access token
        :type        : ``` str ```
        :param options : Optional validation options for issuer, audience, and scopes
        :type        : ``` TokenValidationOptions ```
        :param audience : audience for validation (deprecated, use options.audience instead)
        :type        : ``` str ```

        :returns:
            claims
        """
        
        try:
            claims = self.validate_token(token, options=options, audience=audience)
            return claims
        except jwt.exceptions.InvalidTokenError as exp:
            raise ScalekitValidateTokenFailureException(exp)
        except Exception as exp:
            raise exp

    def get_idp_initiated_login_claims(self, idp_initiated_login_token: str, options: Optional[TokenValidationOptions] = None, audience = None) -> IdpInitiatedLoginClaims:
        """
        Method to get IDP initiated login claims

        :param idp_initiated_login_token : IDP initiated login token
        :type        : ``` str ```
        :param options : Optional validation options for issuer and audience
        :type        : ``` TokenValidationOptions ```
        :param audience : audience for validation (deprecated, use options.audience instead)
        :type        : ``` str ```

        :returns:
            ``` IdpInitiatedLoginClaims ```
        """
        try:
            claims = self.validate_token(idp_initiated_login_token, options=options, audience=audience)
            return claims
        except jwt.exceptions.InvalidTokenError as exp:
            raise ScalekitValidateTokenFailureException(exp)
        except Exception as exp:
            raise exp

    def validate_token(
        self, token: str, options: Optional[TokenValidationOptions] = None, audience: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Method to validate token

        :param token : token
        :type        : ``` str ```
        :param options : validation options for issuer, audience, and scopes
        :type        : ``` TokenValidationOptions ```
        :param audience : audience for validation
        :type        : ``` str ```

        :returns:
            payload
        """
        # Convert TokenValidationOptions to jwt decode options if provided
        jwt_options = {}
        if options:
            if options.issuer:
                jwt_options["issuer"] = options.issuer
                jwt_options["verify_iss"] = True
            if options.audience:
                jwt_options["audience"] = options.audience
                jwt_options["verify_aud"] = True
            elif audience is not None:
                jwt_options["audience"] = [audience]
                jwt_options["verify_aud"] = True
            else:
                jwt_options["verify_aud"] = False
        
        self.core_client.get_jwks()
        kid = jwt.get_unverified_header(token)["kid"]
        key = self.core_client.keys[kid]

        decode_opts = {
            "verify_iss": jwt_options.pop("verify_iss", False),
            "verify_aud": jwt_options.pop("verify_aud", False)
        }

        payload = jwt.decode(
            token,
            key=key,
            algorithms=["RS256"],
            options=decode_opts,
            **jwt_options,
        )
        
        # Validate scopes if required
        if options and options.required_scopes:
            self.verify_scopes(token, options.required_scopes)
        
        return payload



    def verify_scopes(self, token: str, required_scopes: list[str]) -> bool:
        """
        Verify that the token contains the required scopes

        :param token : The token to verify
        :type        : ``` str ```
        :param required_scopes : The scopes that must be present in the token
        :type        : ``` list[str] ```

        :returns:
            bool: Returns True if all required scopes are present
        :raises:
            Error: If required scopes are missing, with details about which scopes are missing
        """
        payload = jwt.decode(token, options={"verify_signature": False})
        scopes = self.__extract_scopes_from_payload(payload)
        
        missing_scopes = [scope for scope in required_scopes if scope not in scopes]
        
        if missing_scopes:
            raise ScalekitValidateTokenFailureException(f"Token missing required scopes: {', '.join(missing_scopes)}")
        
        return True

    def __extract_scopes_from_payload(self, payload: Dict[str, Any]) -> list[str]:
        """
        Extract scopes from token payload

        :param payload : The token payload
        :type        : ``` Dict[str, Any] ```

        :returns:
            list[str]: Array of scopes found in the token
        """
        scopes = payload.get("scopes", [])
        return [scope for scope in scopes if scope and scope.strip()]

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
            raise WebhookVerificationError("Message timestamp too old")

        if timestamp > (now + webhook_tolerance_in_seconds):
            raise WebhookVerificationError("Message timestamp too new")

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

    def refresh_access_token(self, refresh_token: str):
        """
        Method to refresh access token using refresh token

        :param refresh_token  : Refresh token to get new access token
        :type                 : ``` str ```

        :returns:
            dict with access token & refresh token
        """
        try:
            response = self.core_client.authenticate(
                json.dumps(
                    {
                        "refresh_token": refresh_token,
                        "grant_type": GrantType.RefreshToken.value,
                        "client_id": self.core_client.client_id,
                        "client_secret": self.core_client.client_secret,
                    }
                )
            )
            response = json.loads(response.content)
            return {
                "access_token": response["access_token"],
                "refresh_token": response["refresh_token"]
            }

        except Exception as exp:
            raise exp

    def get_logout_url(self, options: LogoutUrlOptions) -> str:
        """
        Method to get logout URL

        :param options        : Logout URL options object
        :type                 : ``` LogoutUrlOptions ```

        :returns:
            str: The logout URL
        """
        try:
            url_params_dict = {
                "id_token_hint": options.id_token_hint,
                "post_logout_redirect_uri": options.post_logout_redirect_uri,
                "state": options.state
            }

            valid_params = {k: v for k, v in url_params_dict.items() if v is not None}
            query_string = urlencode(valid_params)

            return f"{self.core_client.env_url}/{LOGOUT_ENDPOINT}?{query_string}"
        except Exception as exp:
            raise exp

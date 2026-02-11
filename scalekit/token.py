from typing import Optional, Dict

from scalekit.core import CoreClient
from scalekit.common.exceptions import ScalekitValidateTokenFailureException
from scalekit.v1.tokens.tokens_pb2 import (
    CreateToken,
    CreateTokenRequest,
    CreateTokenResponse,
    ValidateTokenRequest,
    ValidateTokenResponse,
    InvalidateTokenRequest,
    ListTokensRequest,
    ListTokensResponse,
)
from scalekit.v1.tokens.tokens_pb2_grpc import ApiTokenServiceStub


class TokenClient:
    """Class definition for Token Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Token Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.token_service = ApiTokenServiceStub(
            self.core_client.grpc_secure_channel
        )

    def create_token(
        self,
        organization_id: str,
        user_id: Optional[str] = None,
        custom_claims: Optional[Dict[str, str]] = None,
        expiry=None,
        description: Optional[str] = None,
    ) -> CreateTokenResponse:
        """
        Method to create an API token for an organization or user

        :param organization_id : Organization ID for token scope
        :type                  : ``` str ```
        :param user_id         : Optional User ID to scope token to a specific user
        :type                  : ``` str ```
        :param custom_claims   : Optional custom claims key-value pairs
        :type                  : ``` dict[str, str] ```
        :param expiry          : Optional expiry timestamp
        :type                  : ``` google.protobuf.Timestamp ```
        :param description     : Optional human-readable label
        :type                  : ``` str ```
        :returns:
            CreateTokenResponse with token, token_id, and token_info
        """
        if not organization_id:
            raise ValueError("organization_id is required")
        token = CreateToken(
            organization_id=organization_id,
        )
        if user_id:
            token.user_id = user_id
        if custom_claims:
            token.custom_claims.update(custom_claims)
        if expiry:
            token.expiry.CopyFrom(expiry)
        if description:
            token.description = description

        return self.core_client.grpc_exec(
            self.token_service.CreateToken.with_call,
            CreateTokenRequest(token=token),
        )

    def validate_token(self, token: str) -> ValidateTokenResponse:
        """
        Method to validate an API token and return associated context

        :param token  : Opaque token string or token_id (apit_xxxxx)
        :type         : ``` str ```
        :returns:
            ValidateTokenResponse with token_info
        :raises ScalekitValidateTokenFailureException: If the token is invalid, expired, or not found
        """
        if not token:
            raise ValueError("token is required")
        try:
            return self.core_client.grpc_exec(
                self.token_service.ValidateToken.with_call,
                ValidateTokenRequest(token=token),
            )
        except Exception as e:
            raise ScalekitValidateTokenFailureException(e) from e

    def invalidate_token(self, token: str):
        """
        Method to invalidate (soft delete) an API token

        :param token  : Opaque token string or token_id (apit_xxxxx)
        :type         : ``` str ```
        :returns:
            Empty response (idempotent operation)
        """
        if not token:
            raise ValueError("token is required")
        return self.core_client.grpc_exec(
            self.token_service.InvalidateToken.with_call,
            InvalidateTokenRequest(token=token),
        )

    def list_tokens(
        self,
        organization_id: str,
        user_id: Optional[str] = None,
        page_size: int = 10,
        page_token: Optional[str] = None,
    ) -> ListTokensResponse:
        """
        Method to list API tokens for an organization

        :param organization_id : Organization ID to filter tokens
        :type                  : ``` str ```
        :param user_id         : Optional User ID to filter tokens
        :type                  : ``` str ```
        :param page_size       : Page size (default 10, max 30)
        :type                  : ``` int ```
        :param page_token      : Pagination cursor for next page
        :type                  : ``` str ```
        :returns:
            ListTokensResponse with tokens, total_count, and pagination cursors
        """
        if not organization_id:
            raise ValueError("organization_id is required")
        request = ListTokensRequest(
            organization_id=organization_id,
            page_size=page_size,
        )
        if user_id:
            request.user_id = user_id
        if page_token:
            request.page_token = page_token

        return self.core_client.grpc_exec(
            self.token_service.ListTokens.with_call,
            request,
        )

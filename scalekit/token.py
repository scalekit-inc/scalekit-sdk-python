from typing import Optional, Dict

import grpc

from scalekit.core import CoreClient
from scalekit.common.exceptions import ScalekitServerException, ScalekitValidateTokenFailureException
from scalekit.v1.tokens.tokens_pb2 import (
    CreateToken,
    CreateTokenRequest,
    CreateTokenResponse,
    ValidateTokenRequest,
    ValidateTokenResponse,
    InvalidateTokenRequest,
    ListTokensRequest,
    ListTokensResponse,
    UpdateTokenRequest,
    UpdateTokenResponse,
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
            raise ValueError("Invalid organization_id")
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
            self.token_service.CreateToken,
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
            raise ValueError("Invalid token")
        try:
            return self.core_client.grpc_exec(
                self.token_service.ValidateToken,
                ValidateTokenRequest(token=token),
            )
        except ScalekitServerException as e:
            validation_codes = {
                grpc.StatusCode.UNAUTHENTICATED,
                grpc.StatusCode.NOT_FOUND,
                grpc.StatusCode.INVALID_ARGUMENT,
                grpc.StatusCode.PERMISSION_DENIED,
            }
            if e.grpc_status in validation_codes:
                raise ScalekitValidateTokenFailureException(e) from e
            raise

    def invalidate_token(self, token: str):
        """
        Method to invalidate (soft delete) an API token

        :param token  : Opaque token string or token_id (apit_xxxxx)
        :type         : ``` str ```
        :returns:
            Empty response (idempotent operation)
        """
        if not token:
            raise ValueError("Invalid token")
        return self.core_client.grpc_exec(
            self.token_service.InvalidateToken,
            InvalidateTokenRequest(token=token),
        )

    def update_token(
        self,
        token: str,
        custom_claims: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
    ) -> UpdateTokenResponse:
        """
        Method to update the custom claims and/or description of an existing API token

        Custom claims are merged into the existing set. To remove a claim, set its value to an empty string.

        :param token       : Opaque token string or token_id (apit_xxxxx)
        :type              : ``` str ```
        :param custom_claims : Claims to merge; set value to "" to remove a claim
        :type              : ``` dict[str, str] ```
        :param description : Replacement description; empty string clears it
        :type              : ``` str ```
        :returns:
            UpdateTokenResponse with updated token_info
        """
        if not token:
            raise ValueError("Invalid token")
        request = UpdateTokenRequest(token=token)
        if custom_claims is not None:
            # Fetch current token to get existing claims for merge
            current = self.validate_token(token)
            merged_claims = dict(current.token_info.custom_claims)
            # Apply updates and removals (empty string means remove)
            for key, value in custom_claims.items():
                if value == "":
                    merged_claims.pop(key, None)
                else:
                    merged_claims[key] = value
            request.custom_claims.update(merged_claims)
        if description is not None:
            request.description = description
        return self.core_client.grpc_exec(
            self.token_service.UpdateToken,
            request,
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
            raise ValueError("Invalid organization_id")
        request = ListTokensRequest(
            organization_id=organization_id,
            page_size=page_size,
        )
        if user_id:
            request.user_id = user_id
        if page_token:
            request.page_token = page_token

        return self.core_client.grpc_exec(
            self.token_service.ListTokens,
            request,
        )

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from scalekit.v1.connected_accounts.connected_accounts_pb2 import (
    UpdateConnectedAccount,
    AuthorizationDetails,
    OauthToken,
    StaticAuth
)
from google.protobuf import struct_pb2


class UpdateConnectedAccountRequest(BaseModel):
    """Update connected account request model"""

    connection_name: str = Field(..., description="Connector identifier")
    identifier: str = Field(..., description="Connected account identifier")
    authorization_details: Optional[Dict[str, Any]] = Field(None, description="Authorization details (OAuth token or static auth)")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    user_id: Optional[str] = Field(None, description="User ID")
    connected_account_id: Optional[str] = Field(None, description="Connected account ID")
    api_config: Optional[Dict[str, Any]] = Field(None, description="Optional API configuration for the connected account")

    def to_proto(self) -> UpdateConnectedAccount:
        """
        Convert to protobuf UpdateConnectedAccount object

        :returns:
            UpdateConnectedAccount protobuf object
        """
        auth_details = None

        if self.authorization_details and "oauth_token" in self.authorization_details:
            oauth_data = self.authorization_details["oauth_token"]
            oauth_token = OauthToken(
                access_token=oauth_data.get("access_token", ""),
                refresh_token=oauth_data.get("refresh_token", ""),
                scopes=oauth_data.get("scopes", [])
            )
            auth_details = AuthorizationDetails(oauth_token=oauth_token)

        elif self.authorization_details and "static_auth" in self.authorization_details:
            static_data = self.authorization_details["static_auth"]
            # Convert dict to protobuf Struct
            struct_details = struct_pb2.Struct()
            struct_details.update(static_data)
            static_auth = StaticAuth(details=struct_details)
            auth_details = AuthorizationDetails(static_auth=static_auth)

        # Handle api_config if provided
        api_config_struct = None
        if self.api_config:
            api_config_struct = struct_pb2.Struct()
            api_config_struct.update(self.api_config)

        return UpdateConnectedAccount(
            authorization_details=auth_details,
            api_config=api_config_struct
        )

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
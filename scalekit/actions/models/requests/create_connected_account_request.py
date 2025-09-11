from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from scalekit.v1.connected_accounts.connected_accounts_pb2 import (
    CreateConnectedAccount,
    AuthorizationDetails,
    OauthToken,
    StaticAuth
)
from google.protobuf import struct_pb2


class CreateConnectedAccountRequest(BaseModel):
    """Create connected account request model"""
    
    connection_name: str = Field(..., description="Connector identifier")
    identifier: str = Field(..., description="Connected account identifier")
    authorization_details: Dict[str, Any] = Field(default_factory=dict, description="Authorization details (OAuth token or static auth)")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    user_id: Optional[str] = Field(None, description="User ID")

    def to_proto(self) -> CreateConnectedAccount:
        """
        Convert to protobuf CreateConnectedAccount object
        
        :returns:
            CreateConnectedAccount protobuf object
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
        
        elif not self.authorization_details:
            # Create empty OAuth token for empty authorization details
            oauth_token = OauthToken(
                access_token="",
                refresh_token="",
                scopes=[]
            )
            auth_details = AuthorizationDetails(oauth_token=oauth_token)
        
        return CreateConnectedAccount(authorization_details=auth_details)

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
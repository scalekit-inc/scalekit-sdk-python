from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from scalekit.v1.connected_accounts.connected_accounts_pb2 import ConnectedAccount as ProtoConnectedAccount, ConnectorStatus, ConnectorType


class ConnectedAccount(BaseModel):
    """Connected account information"""
    
    id: Optional[str] = Field(None, description="Unique connected account ID")
    identifier: Optional[str] = Field(None, description="Connected account identifier")
    provider: Optional[str] = Field(None, description="Provider name")
    status: Optional[str] = Field(None, description="Connection status")
    authorization_type: Optional[str] = Field(None, description="Authorization type")
    authorization_details: Optional[Dict[str, Any]] = Field(None, description="Authorization details")
    token_expires_at: Optional[datetime] = Field(None, description="Token expiry time")
    updated_at: Optional[datetime] = Field(None, description="Last updated time")
    connector: Optional[str] = Field(None, description="Connector name")
    last_used_at: Optional[datetime] = Field(None, description="Last used time")

    @classmethod
    def from_proto(cls, proto_account: ProtoConnectedAccount) -> 'ConnectedAccount':
        """
        Create ConnectedAccount from protobuf ConnectedAccount
        
        :param proto_account: The protobuf ConnectedAccount object
        :type proto_account: ProtoConnectedAccount
        
        :returns:
            ConnectedAccount instance
        """
        # Convert protobuf timestamps to datetime
        token_expires_at = None
        if proto_account.token_expires_at:
            token_expires_at = proto_account.token_expires_at.ToDatetime()
            
        updated_at = None
        if proto_account.updated_at:
            updated_at = proto_account.updated_at.ToDatetime()
            
        last_used_at = None
        if proto_account.last_used_at:
            last_used_at = proto_account.last_used_at.ToDatetime()

        # Convert authorization details
        authorization_details = None
        if proto_account.authorization_details:
            authorization_details = {}
            if proto_account.authorization_type == ConnectorType.OAUTH :
                oauth_token = proto_account.authorization_details.oauth_token
                authorization_details["oauth_token"] = {
                    "access_token": oauth_token.access_token,
                    "refresh_token": oauth_token.refresh_token,
                    "scopes": list(oauth_token.scopes)
                }
            else:
                static_auth = proto_account.authorization_details.static_auth
                # Convert protobuf Struct to dict
                from google.protobuf.json_format import MessageToDict
                authorization_details["static_auth"] = MessageToDict(static_auth.details)

        return cls(
            id=proto_account.id if proto_account.id else None,
            identifier=proto_account.identifier,
            provider=proto_account.provider,
            status= ConnectorStatus.Name(proto_account.status) if proto_account.status else None,
            authorization_type=ConnectorType.Name(proto_account.authorization_type) if proto_account.authorization_type else None,
            authorization_details=authorization_details,
            token_expires_at=token_expires_at,
            updated_at=updated_at,
            connector=proto_account.connector,
            last_used_at=last_used_at
        )


class GetConnectedAccountAuthResponse(BaseModel):
    """Get connected account auth response with one-to-one mapping to proto GetConnectedAccountByIdentifierResponse"""
    
    connected_account: Optional[ConnectedAccount] = Field(
        None,
        description="Connected account details"
    )

    @classmethod
    def from_proto(cls, proto_response) -> 'GetConnectedAccountAuthResponse':
        """
        Create GetConnectedAccountAuthResponse from protobuf GetConnectedAccountByIdentifierResponse
        
        :param proto_response: The protobuf GetConnectedAccountByIdentifierResponse object
        :type proto_response: GetConnectedAccountByIdentifierResponse (from connected_accounts_pb2)
        
        :returns:
            GetConnectedAccountAuthResponse instance
        """
        connected_account = None
        if proto_response.connected_account:
            connected_account = ConnectedAccount.from_proto(proto_response.connected_account)
            
        return cls(connected_account=connected_account)

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation
        
        :returns:
            Dictionary representation of the response
        """
        return {
            "connected_account": self.connected_account.model_dump() if self.connected_account else None
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from google.protobuf import timestamp_pb2

from scalekit.v1.connected_accounts.connected_accounts_pb2 import ConnectorStatus, ConnectorType


class ConnectedAccountForList(BaseModel):
    """Connected account item in list response with one-to-one mapping to proto ConnectedAccountForList"""
    
    identifier: Optional[str] = Field(
        None,
        description="Unique identifier for the connected account"
    )
    provider: Optional[str] = Field(
        None,
        description="Provider of the connected account (e.g., 'google', 'slack')"
    )
    status: Optional[str] = Field(
        None, 
        description="Status of the connected account"
    )
    authorization_type: Optional[str] = Field(
        None,
        description="Type of authorization used for the connected account"
    )
    token_expires_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the token expires"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the connected account was last updated"
    )
    connector: Optional[str] = Field(
        None,
        description="Connector identifier"
    )
    last_used_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the connected account was last used"
    )

    @classmethod
    def from_proto(cls, proto_account) -> 'ConnectedAccountForList':
        """
        Create ConnectedAccountForList from protobuf ConnectedAccountForList
        
        :param proto_account: The protobuf ConnectedAccountForList object
        :type proto_account: ConnectedAccountForList (from connected_accounts_pb2)
        
        :returns:
            ConnectedAccountForList instance
        """
        # Convert protobuf Timestamps to datetime
        token_expires_at = None
        if proto_account.token_expires_at:
            token_expires_at = proto_account.token_expires_at.ToDatetime()
            
        updated_at = None
        if proto_account.updated_at:
            updated_at = proto_account.updated_at.ToDatetime()
            
        last_used_at = None
        if proto_account.last_used_at:
            last_used_at = proto_account.last_used_at.ToDatetime()
            
        return cls(
            identifier=proto_account.identifier if proto_account.identifier else None,
            provider=proto_account.provider if proto_account.provider else None,
            status= ConnectorStatus.Name(proto_account.status) if proto_account.status else None,
            authorization_type=ConnectorType.Name(proto_account.authorization_type) if proto_account.authorization_type else None,
            token_expires_at=token_expires_at,
            updated_at=updated_at,
            connector=proto_account.connector if proto_account.connector else None,
            last_used_at=last_used_at
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation
        
        :returns:
            Dictionary representation of the connected account
        """
        return {
            "identifier": self.identifier,
            "provider": self.provider,
            "status": self.status,
            "authorization_type": self.authorization_type,
            "token_expires_at": self.token_expires_at.isoformat() if self.token_expires_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "connector": self.connector,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ListConnectedAccountsResponse(BaseModel):
    """List connected accounts response with one-to-one mapping to proto ListConnectedAccountsResponse"""
    
    connected_accounts: List[ConnectedAccountForList] = Field(
        default_factory=list,
        description="List of connected accounts"
    )
    total_count: Optional[int] = Field(
        None,
        description="Total number of connected accounts matching the request",
        alias="total_size"
    )
    next_page_token: Optional[str] = Field(
        None,
        description="Token for the next page of results"
    )
    previous_page_token: Optional[str] = Field(
        None,
        description="Token for the previous page of results",
        alias="prev_page_token"
    )

    @classmethod
    def from_proto(cls, proto_response) -> 'ListConnectedAccountsResponse':
        """
        Create ListConnectedAccountsResponse from protobuf ListConnectedAccountsResponse
        
        :param proto_response: The protobuf ListConnectedAccountsResponse object
        :type proto_response: ListConnectedAccountsResponse (from connected_accounts_pb2)
        
        :returns:
            ListConnectedAccountsResponse instance
        """
        # Convert protobuf connected accounts to our model
        connected_accounts = []
        for proto_account in proto_response.connected_accounts:
            connected_accounts.append(ConnectedAccountForList.from_proto(proto_account))
            
        return cls(
            connected_accounts=connected_accounts,
            total_count=proto_response.total_size if proto_response.total_size else None,
            next_page_token=proto_response.next_page_token if proto_response.next_page_token else None,
            previous_page_token=proto_response.prev_page_token if proto_response.prev_page_token else None
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation
        
        :returns:
            Dictionary representation of the response
        """
        return {
            "connected_accounts": [account.to_dict() for account in self.connected_accounts],
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
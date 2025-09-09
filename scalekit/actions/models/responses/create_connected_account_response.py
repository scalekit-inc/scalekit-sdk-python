from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .get_connected_account_auth_response import ConnectedAccount


class CreateConnectedAccountResponse(BaseModel):
    """Create connected account response with one-to-one mapping to proto CreateConnectedAccountResponse"""
    
    connected_account: Optional[ConnectedAccount] = Field(
        None,
        description="Created connected account details"
    )

    @classmethod
    def from_proto(cls, proto_response) -> 'CreateConnectedAccountResponse':
        """
        Create CreateConnectedAccountResponse from protobuf CreateConnectedAccountResponse
        
        :param proto_response: The protobuf CreateConnectedAccountResponse object
        :type proto_response: CreateConnectedAccountResponse (from connected_accounts_pb2)
        
        :returns:
            CreateConnectedAccountResponse instance
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
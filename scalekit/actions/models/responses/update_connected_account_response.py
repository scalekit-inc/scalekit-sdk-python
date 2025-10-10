from typing import Optional
from pydantic import BaseModel, Field
from scalekit.v1.connected_accounts.connected_accounts_pb2 import UpdateConnectedAccountResponse as ProtoUpdateConnectedAccountResponse
from .get_connected_account_auth_response import ConnectedAccount


class UpdateConnectedAccountResponse(BaseModel):
    """Update connected account response model"""

    connected_account: Optional[ConnectedAccount] = Field(None, description="Updated connected account details")

    @classmethod
    def from_proto(cls, proto: ProtoUpdateConnectedAccountResponse) -> 'UpdateConnectedAccountResponse':
        """
        Convert from protobuf UpdateConnectedAccountResponse to response model

        :param proto: Protobuf UpdateConnectedAccountResponse object
        :type proto: ProtoUpdateConnectedAccountResponse

        :returns:
            UpdateConnectedAccountResponse model instance
        """
        connected_account = None
        if proto.connected_account:
            connected_account = ConnectedAccount.from_proto(proto.connected_account)

        return cls(connected_account=connected_account)

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
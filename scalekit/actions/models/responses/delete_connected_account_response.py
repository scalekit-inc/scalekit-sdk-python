from pydantic import BaseModel


class DeleteConnectedAccountResponse(BaseModel):
    """Delete connected account response with one-to-one mapping to proto DeleteConnectedAccountResponse"""

    @classmethod
    def from_proto(cls, proto_response) -> 'DeleteConnectedAccountResponse':
        """
        Create DeleteConnectedAccountResponse from protobuf DeleteConnectedAccountResponse
        
        :param proto_response: The protobuf DeleteConnectedAccountResponse object
        :type proto_response: DeleteConnectedAccountResponse (from connected_accounts_pb2)
        
        :returns:
            DeleteConnectedAccountResponse instance
        """

        # Since the DeleteConnectedAccountResponse does not have any fields
        return cls()

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation
        
        :returns:
            Dictionary representation of the response
        """
        return {}

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
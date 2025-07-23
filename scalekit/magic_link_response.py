from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from google.protobuf import timestamp_pb2


class MagicLinkResponse(BaseModel):
    """Magic link response with one-to-one mapping to proto GetMagicLinkForConnectedAccountResponse"""
    
    link: Optional[str] = Field(
        None,
        description="Magic link URL for connected account authorization"
    )
    expiry: Optional[datetime] = Field(
        None,
        description="Expiry timestamp for the magic link"
    )

    @classmethod
    def from_proto(cls, proto_response) -> 'MagicLinkResponse':
        """
        Create MagicLinkResponse from protobuf GetMagicLinkForConnectedAccountResponse
        
        :param proto_response: The protobuf GetMagicLinkForConnectedAccountResponse object
        :type proto_response: GetMagicLinkForConnectedAccountResponse (from connected_accounts_pb2)
        
        :returns:
            MagicLinkResponse instance
        """
        # Convert protobuf Timestamp to datetime
        expiry = None
        if proto_response.expiry:
            expiry = proto_response.expiry.ToDatetime()
            
        return cls(
            link=proto_response.link if proto_response.link else None,
            expiry=expiry
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation
        
        :returns:
            Dictionary representation of the response
        """
        return {
            "link": self.link,
            "expiry": self.expiry.isoformat() if self.expiry else None
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
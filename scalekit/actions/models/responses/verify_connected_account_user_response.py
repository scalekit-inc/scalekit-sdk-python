from typing import Optional
from pydantic import BaseModel, Field


class VerifyConnectedAccountUserResponse(BaseModel):
    """Verify connected account user response with one-to-one mapping to proto VerifyConnectedAccountUserResponse"""

    post_user_verify_redirect_url: Optional[str] = Field(
        None,
        description="URL to redirect the user to after successful verification"
    )

    @classmethod
    def from_proto(cls, proto_response) -> 'VerifyConnectedAccountUserResponse':
        """
        Create VerifyConnectedAccountUserResponse from protobuf VerifyConnectedAccountUserResponse

        :param proto_response: The protobuf VerifyConnectedAccountUserResponse object
        :type proto_response: VerifyConnectedAccountUserResponse (from connected_accounts_pb2)

        :returns:
            VerifyConnectedAccountUserResponse instance
        """
        return cls(
            post_user_verify_redirect_url=proto_response.post_user_verify_redirect_url or None
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary representation

        :returns:
            Dictionary representation of the response
        """
        return {
            "post_user_verify_redirect_url": self.post_user_verify_redirect_url
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True

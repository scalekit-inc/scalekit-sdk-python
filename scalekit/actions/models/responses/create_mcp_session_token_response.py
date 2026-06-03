from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateMcpSessionTokenResponse(BaseModel):
    """Response from ``create_session_token``.

    A short-lived session token that an end-user or service can use to
    authenticate against an MCP server endpoint.

    Attributes:
        token: Opaque bearer token string. Pass this as the ``Authorization``
            header value (``Bearer <token>``) when calling the MCP server URL.
        expires_at: UTC datetime at which the token becomes invalid. Your
            application should refresh before this time.

    Example::

        from datetime import timedelta

        resp = client.actions.mcp.create_session_token(
            mcp_config_id="cfg_abc123",
            identifier="user@example.com",
            expiry=timedelta(hours=8),
        )
        print(resp.token)        # "eyJ..."
        print(resp.expires_at)   # 2026-06-03 20:00:00
    """

    token: Optional[str] = Field(None, description="Bearer token for MCP server authentication")
    expires_at: Optional[datetime] = Field(None, description="UTC expiry time for the token")

    @classmethod
    def from_proto(cls, proto_response) -> "CreateMcpSessionTokenResponse":
        expires_at = None
        if proto_response.HasField("expires_at"):
            expires_at = proto_response.expires_at.ToDatetime()
        return cls(
            token=proto_response.token or None,
            expires_at=expires_at,
        )

    def to_dict(self) -> dict:
        return {
            "token": self.token,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

    class Config:
        validate_assignment = True

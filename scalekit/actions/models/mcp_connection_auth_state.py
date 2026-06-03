from typing import Optional

from pydantic import BaseModel, Field

from scalekit.v1.mcp.mcp_pb2 import McpConnectionAuthState as ProtoMcpConnectionAuthState


class McpConnectionAuthState(BaseModel):
    """Authentication status for a single connection within an MCP config.

    Returned by ``list_mcp_connected_accounts`` to show whether each connection
    backing an MCP configuration is authorised for a given user identifier.

    Attributes:
        connection_id: Internal Scalekit identifier for the connection.
        connection_name: Slug name of the connection, e.g. ``"github"``.
        provider: OAuth/API-key provider backing the connection, e.g. ``"github"``.
        connected_account_id: Scalekit identifier for the user's connected account,
            if one exists.
        connected_account_status: Current authorisation status of the connected
            account. Common values: ``"active"``, ``"expired"``, ``"disconnected"``.
        authentication_link: One-time URL the end-user can open to authorise or
            re-authorise the connection. Only populated when ``include_auth_link``
            was ``True`` in the request and the account is not currently active.
    """

    connection_id: Optional[str] = Field(None, description="Internal connection identifier")
    connection_name: Optional[str] = Field(None, description="Slug name of the connection")
    provider: Optional[str] = Field(None, description="Provider backing the connection")
    connected_account_id: Optional[str] = Field(None, description="Scalekit connected account ID")
    connected_account_status: Optional[str] = Field(
        None,
        description="Authorisation status: 'active', 'expired', 'disconnected'",
    )
    authentication_link: Optional[str] = Field(
        None,
        description="One-time auth URL; only present when include_auth_link=True and account is not active",
    )

    @classmethod
    def from_proto(cls, proto_state: ProtoMcpConnectionAuthState) -> "McpConnectionAuthState":
        return cls(
            connection_id=proto_state.connection_id or None,
            connection_name=proto_state.connection_name or None,
            provider=proto_state.provider or None,
            connected_account_id=proto_state.connected_account_id or None,
            connected_account_status=proto_state.connected_account_status or None,
            authentication_link=proto_state.authentication_link or None,
        )

    def to_dict(self) -> dict:
        return {
            "connection_id": self.connection_id,
            "connection_name": self.connection_name,
            "provider": self.provider,
            "connected_account_id": self.connected_account_id,
            "connected_account_status": self.connected_account_status,
            "authentication_link": self.authentication_link,
        }

    class Config:
        validate_assignment = True

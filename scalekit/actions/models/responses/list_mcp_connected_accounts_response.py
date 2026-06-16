from typing import List

from pydantic import BaseModel, Field

from scalekit.actions.models.mcp_connection_auth_state import McpConnectionAuthState


class ListMcpConnectedAccountsResponse(BaseModel):
    """Response from ``list_mcp_connected_accounts``.

    Contains the per-connection authentication state for every connection
    that is part of the requested MCP configuration, for a specific user
    identifier.

    Attributes:
        connected_accounts: One entry per connection in the MCP config. Each
            entry carries the connection name, provider, the user's connected
            account ID/status, and optionally an auth link if the account is
            not active and ``include_auth_link`` was requested.

    Example::

        response = client.actions.mcp.list_mcp_connected_accounts(
            config_id="cfg_abc123",
            identifier="user@example.com",
            include_auth_link=True,
        )
        for account in response.connected_accounts:
            if account.connected_account_status != "active":
                print(f"Re-auth needed for {account.connection_name}: {account.authentication_link}")
    """

    connected_accounts: List[McpConnectionAuthState] = Field(
        default_factory=list,
        description="Auth state per connection in the MCP config",
    )

    @classmethod
    def from_proto(cls, proto_response) -> "ListMcpConnectedAccountsResponse":
        connected_accounts = [
            McpConnectionAuthState.from_proto(proto_state)
            for proto_state in getattr(proto_response, "connected_accounts", [])
        ]
        return cls(connected_accounts=connected_accounts)

    def to_dict(self) -> dict:
        return {
            "connected_accounts": [account.to_dict() for account in self.connected_accounts],
        }

    class Config:
        validate_assignment = True

from typing import Optional, Dict, Any
from scalekit.tool_request import ToolRequest


class ConnectClient:
    """Class definition for Connect Client"""

    def __init__(self,tools_client, connected_accounts_client):
        """
        Initialize ConnectClient with tools and connected accounts dependencies
        
        :param tools_client: ToolsClient instance
        :type: ToolsClient
        :param connected_accounts_client: ConnectedAccountsClient instance
        :type: ConnectedAccountsClient
        
        :returns:
            None
        """

        self.tools = tools_client
        self.connected_accounts = connected_accounts_client

    def execute_tool(
        self,
        input_data: Dict[str, Any],
        tool_name: str,
        identifier: str,
        tool_request: Optional[ToolRequest] = None,
        context: Optional[Dict[str, Any]] = None,
        connector: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a tool with the given parameters.
        
        Args:
            input_data: Input data for the tool execution (required)
            tool_name: Name of the tool to execute (required)
            identifier: Unique identifier for this execution (required)
            tool_request: Optional ToolRequest configuration object
            context: Optional context dictionary
            connector: Optional connector string
            connected_account_id: Optional connected account ID string
            **kwargs: Additional optional parameters
            
        Returns:
            Dict containing execution results
        """
        # Validate required parameters
        if not input_data:
            raise ValueError("input_data is required")
        if not tool_name:
            raise ValueError("tool_name is required")
        if not identifier:
            raise ValueError("identifier is required")
        
        # For now, use the existing tools.execute_tool with input_data as params
        return self.tools.execute_tool(
            tool_name=tool_name,
            identifier=identifier,
            params=input_data
        )
    
    def get_authorization_link(self, connector: str, identifier: str):
        """
        Get authorization magic link for a connected account
        
        :param connector: Connector identifier
        :type: str
        :param identifier: Connected account identifier
        :type: str
        
        :returns:
            Magic link response
        """
        return self.connected_accounts.get_magic_link_for_connected_account(
            connector=connector,
            identifier=identifier
        )
    
    def list_connected_accounts(
        self, 
        connector: Optional[str] = None,
        identifier: Optional[str] = None,
        provider: Optional[str] = None
    ):
        """
        List connected accounts with optional filtering
        
        :param connector: Connector identifier (optional)
        :type: str
        :param identifier: Identifier filter (optional)
        :type: str
        :param provider: Provider filter (optional)
        :type: str
        
        :returns:
            List of connected accounts
        """
        return self.connected_accounts.list_connected_accounts(
            connector=connector,
            identifier=identifier,
            provider=provider
        )
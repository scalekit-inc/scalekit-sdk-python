from typing import Optional, Dict, Any
from scalekit.connect.types import ToolRequest,ExecuteToolResponse,MagicLinkResponse,ListConnectedAccountsResponse


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
        tool_input: Dict[str, Any],
        tool_name: str,
        identifier: Optional[str] = None,
        tool_request: Optional[ToolRequest] = None,
        context: Optional[Dict[str, Any]] = None,
        connection_name: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        connection_id: Optional[str] = None,
        **kwargs
    ) -> ExecuteToolResponse:
        """
        Execute a tool with the given parameters.
        
        Args:
            tool_input: Input data for the tool execution (required)
            tool_name: Name of the tool to execute (required)
            identifier: Unique identifier for this execution (required)
            tool_request: Optional ToolRequest configuration object
            context: Optional context dictionary
            connection_name: Optional connector string
            connected_account_id: Optional connected account ID string
            connection_id: Optional connection ID string
            **kwargs: Additional optional parameters
            
        Returns:
            ExecuteToolResponse containing execution results
        """
        # Validate required parameters
        if not tool_input:
            raise ValueError("tool_input is required")
        if not tool_name:
            raise ValueError("tool_name is required")
        if not identifier:
            raise ValueError("identifier is required")
        
        # Call the existing tools.execute_tool which returns (response, metadata) tuple
        result_tuple = self.tools.execute_tool(
            tool_name=tool_name,
            identifier=identifier,
            params=tool_input
        )
        
        # Extract the response[0] (the actual ExecuteToolResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our ExecuteToolResponse class
        return ExecuteToolResponse.from_proto(proto_response)
    
    def get_authorization_link(
            self,
            identifier: Optional[str] = None,
            connection_name: Optional[str] = None,
            connected_account_id: Optional[str] = None,
            **kwargs
    ) -> MagicLinkResponse:
        """
        Get authorization magic link for a connected account
        
        :param connection_name: Connector identifier
        :type: str
        :param identifier: Connected account identifier
        :type: str
        :param connected_account_id: Connected account ID (optional)
        :type: str
        
        :returns:
            MagicLinkResponse containing magic link and expiry
        """
        # Call the existing connected_accounts method which returns (response, metadata) tuple
        result_tuple = self.connected_accounts.get_magic_link_for_connected_account(
            connector=connection_name,
            identifier=identifier
        )
        
        # Extract the response[0] (the actual GetMagicLinkForConnectedAccountResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our MagicLinkResponse class
        return MagicLinkResponse.from_proto(proto_response)
    
    def list_connected_accounts(
        self, 
        connection_name: Optional[str] = None,
        identifier: Optional[str] = None,
        provider: Optional[str] = None,
        **kwargs
    ) -> ListConnectedAccountsResponse:
        """
        List connected accounts with optional filtering
        
        :param connection_name: Connector identifier (optional)
        :type: str
        :param identifier: Identifier filter (optional)
        :type: str
        :param provider: Provider filter (optional)
        :type: str
        
        :returns:
            ListConnectedAccountsResponse containing list of connected accounts
        """
        # Call the existing connected_accounts method which returns (response, metadata) tuple
        result_tuple = self.connected_accounts.list_connected_accounts(
            connector=connection_name,
            identifier=identifier,
            provider=provider
        )
        
        # Extract the response[0] (the actual ListConnectedAccountsResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our ListConnectedAccountsResponse class
        return ListConnectedAccountsResponse.from_proto(proto_response)
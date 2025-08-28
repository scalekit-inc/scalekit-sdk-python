from typing import Optional, Any, List, Dict
from scalekit.v1.mcp.mcp_pb2 import Mcp
from scalekit.v1.mcp.mcp_pb2 import ToolMapping as ProtoToolMapping

from scalekit.connect.models.tool_mapping import ToolMapping
from scalekit.connect.types import ToolRequest,ExecuteToolResponse,MagicLinkResponse,ListConnectedAccountsResponse,DeleteConnectedAccountResponse,GetConnectedAccountAuthResponse,ToolInput, \
    McpRequest,CreateMcpResponse,GetMcpResponse
from scalekit.connect.models.responses.create_connected_account_response import CreateConnectedAccountResponse
from scalekit.connect.models.requests.create_connected_account_request import CreateConnectedAccountRequest
from scalekit.connect.modifier import (
    Modifier, ModifierType, ToolNames,
    apply_pre_modifiers, apply_post_modifiers
)
from scalekit.connect.frameworks.langchain import LangChain
from scalekit.common.exceptions import ScalekitNotFoundException




class ConnectClient:
    """Class definition for Connect Client"""

    def __init__(self,tools_client, connected_accounts_client, mcp_client=None):
        """
        Initialize ConnectClient with tools, connected accounts, and MCP dependencies
        
        :param tools_client: ToolsClient instance
        :type: ToolsClient
        :param connected_accounts_client: ConnectedAccountsClient instance
        :type: ConnectedAccountsClient
        :param mcp_client: McpClient instance (optional)
        :type: McpClient
        
        :returns:
            None
        """

        self.tools = tools_client
        self.connected_accounts = connected_accounts_client
        self.mcp = mcp_client
        self._modifiers: List[Modifier] = []
        
        # Initialize LangChain with tools client and execute callback
        self.langchain = LangChain(tools_client, execute_callback=self.execute_tool)

    def execute_tool(
        self,
        tool_input:ToolInput,
        tool_name: str,
        identifier: Optional[str] = None,
        tool_request: Optional[ToolRequest] = None,
        connected_account_id: Optional[str] = None,
        **kwargs
    ) -> ExecuteToolResponse:
        """
        Execute a tool with the given parameters.
        
        Args:
            tool_input: Input data for the tool execution (required)
            tool_name: Name of the tool to execute (required)
            identifier: Unique identifier for this execution (required)
            tool_request: Optional ToolRequest configuration object
            connected_account_id: Optional connected account ID string
            **kwargs: Additional optional parameters
            
        Returns:
            ExecuteToolResponse containing execution results
        """
        # Validate required parameters
        if not tool_name:
            raise ValueError("tool_name is required")
        
        # Apply pre-modifications to the input parameters
        modified_tool_input = apply_pre_modifiers(tool_name, tool_input, self._modifiers)
        
        # Call the existing tools.execute_tool which returns (response, metadata) tuple
        result_tuple = self.tools.execute_tool(
            tool_name=tool_name,
            identifier=identifier,
            params=modified_tool_input,
            connected_account_id=connected_account_id
        )
        
        # Extract the response[0] (the actual ExecuteToolResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our ExecuteToolResponse class
        response = ExecuteToolResponse.from_proto(proto_response)
        
        # Apply post-modifications to the result
        modified_response = apply_post_modifiers(tool_name, response.data, self._modifiers)

        response.data = modified_response
        
        return response
    
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
            identifier=identifier,
            connected_account_id=connected_account_id
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
    
    def delete_connected_account(
        self,
        connection_name: Optional[str] = None,
        identifier: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        **kwargs
    ) -> DeleteConnectedAccountResponse:
        """
        Delete a connected account
        
        :param connection_name: Connector identifier (required)
        :type: str
        :param identifier: Connected account identifier (required)
        :type: str
        :param connected_account_id: Connected account ID (optional)
        :type: str
        
        :returns:
            DeleteConnectedAccountResponse containing deletion status
        """
            
        # Call the existing connected_accounts method which returns (response, metadata) tuple
        result_tuple = self.connected_accounts.delete_connected_account(
            connector=connection_name,
            identifier=identifier,
            connected_account_id=connected_account_id
        )
        
        # Extract the response[0] (the actual DeleteConnectedAccountResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our DeleteConnectedAccountResponse class
        return DeleteConnectedAccountResponse.from_proto(proto_response)
    
    def get_connected_account(
        self,
        connection_name: Optional[str] = None,
        identifier: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        **kwargs
    ) -> GetConnectedAccountAuthResponse:
        """
        Get connected account authorization details by identifier
        
        :param connection_name: Connector identifier (required)
        :type: str
        :param identifier: Connected account identifier (required)
        :type: str
        :param connected_account_id: Connected account ID (optional)
        :type: str
        
        :returns:
            GetConnectedAccountAuthResponse containing connected account details
        """


            
        # Call the existing connected_accounts method which returns (response, metadata) tuple
        result_tuple = self.connected_accounts.get_connected_account_by_identifier(
            connector=connection_name,
            identifier=identifier,
            connected_account_id=connected_account_id
        )
        
        # Extract the response[0] (the actual GetConnectedAccountByIdentifierResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our GetConnectedAccountAuthResponse class
        return GetConnectedAccountAuthResponse.from_proto(proto_response)
    
    def add_modifier(self, modifier: Modifier) -> None:
        """Add a modifier to the private list"""
        self._modifiers.append(modifier)
    
    def get_modifiers(
        self, 
        tool_name: Optional[str] = None, 
        modifier_type: Optional[ModifierType] = None
    ) -> List[Modifier]:
        """Get modifiers, optionally filtered by tool_name and/or type"""
        filtered = self._modifiers
        
        if tool_name:
            filtered = [m for m in filtered if tool_name in m.tool_names]
        
        if modifier_type:
            filtered = [m for m in filtered if m.type == modifier_type]
            
        return filtered
    
    def pre_modifier(self, tool_names: ToolNames, **kwargs: Any):
        """Decorator for pre-modification that registers with this Connect instance
        
        Usage:
            @connect.premodifier(tool_names="my_tool", priority=1)
            def my_modifier(tool_name, data):
                return modified_data
        """
        def decorator(func):
            modifier = Modifier(tool_names=tool_names, modifier_type="pre", **kwargs)
            modifier.func = func
            self.add_modifier(modifier)
            return func
        return decorator
    
    def post_modifier(self, tool_names: ToolNames, **kwargs: Any):
        """Decorator for post-modification that registers with this Connect instance
        
        Usage:
            @connect.postmodifier(tool_names=["tool1", "tool2"])
            def my_modifier(tool_name, result):
                return modified_result
        """
        def decorator(func):
            modifier = Modifier(tool_names=tool_names, modifier_type="post", **kwargs)
            modifier.func = func
            self.add_modifier(modifier)
            return func
        return decorator

    def get_mcp(
        self,
        mcp_id: str,
        mcp_request: Optional[McpRequest] = None,
        **kwargs
    ) -> GetMcpResponse:
        """
        Get an existing MCP by ID via the connect interface
        
        :param mcp_id: ID of the MCP to retrieve (required)
        :type: str
        :param mcp_request: Optional McpRequest configuration object
        :type: McpRequest
        
        :returns:
            GetMcpResponse containing MCP details
        """
        if not self.mcp:
            raise ValueError("MCP client not initialized. Please ensure MCP client is available.")
        
        if not mcp_id:
            raise ValueError("mcp_id is required")
        
        # Call the MCP client's get_mcp method which returns (response, metadata) tuple
        result_tuple = self.mcp.get_mcp(mcp_id=mcp_id)
        
        # Extract the response[0] (the actual GetMcpResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our GetMcpResponse class
        return GetMcpResponse.from_proto(proto_response)

    def create_mcp(
        self,
        identifier: str,
        tool_mappings: List[ToolMapping],
        mcp_request: Optional[McpRequest] = None,
        **kwargs
    ) -> CreateMcpResponse:
        """
        Create or return existing MCP with given configuration via the connect interface
        
        :param identifier: Identifier for the connected account (required)
        :type: str
        :param tool_mappings: List of tool mappings for the MCP (required)
        :type: List[ToolMapping]
        :param mcp_request: Optional McpRequest configuration object
        :type: McpRequest
        
        :returns:
            CreateMcpResponse containing created MCP details
        """
        if not self.mcp:
            raise ValueError("MCP client not initialized. Please ensure MCP client is available.")
        
        # Validate required parameters
        if not identifier:
            raise ValueError("connected_account_identifier is required")
        if not tool_mappings:
            raise ValueError("tool_mappings is required")



        # Create ToolMapping objects from the provided tool_mappings
        proto_tool_mappings = []
        for mapping in tool_mappings:
            proto_mapping = ProtoToolMapping(
                tool_names=mapping.tool_names,
                connection_name=mapping.connection_name,
            )
            proto_tool_mappings.append(proto_mapping)
        
        # Create the MCP proto object
        mcp_proto = Mcp(
            connected_account_identifier=identifier,
            tool_mappings=proto_tool_mappings,
        )

        result_tuple = self.mcp.create_mcp(mcp=mcp_proto)
        
        # Extract the response[0] (the actual CreateMcpResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our CreateMcpResponse class
        return CreateMcpResponse.from_proto(proto_response)

    def create_connected_account(
        self,
        connection_name: str,
        identifier: str, 
        authorization_details: Dict[str, Any],
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs
    ) -> CreateConnectedAccountResponse:
        """
        Create a new connected account
        
        :param connection_name: Connector identifier (required)
        :type: str
        :param identifier: Connected account identifier (required)
        :type: str
        :param authorization_details: Authorization details (OAuth token or static auth) (required)
        :type: Dict[str, Any]
        :param organization_id: Organization ID (optional)
        :type: str
        :param user_id: User ID (optional)
        :type: str
        
        :returns:
            CreateConnectedAccountResponse containing created connected account details
        """
        # Validate required parameters
        if not connection_name:
            raise ValueError("connection_name is required")
        if not identifier:
            raise ValueError("identifier is required")
        if not authorization_details:
            raise ValueError("authorization_details is required")
        
        # Create request model
        request = CreateConnectedAccountRequest(
            connection_name=connection_name,
            identifier=identifier,
            authorization_details=authorization_details,
            organization_id=organization_id,
            user_id=user_id
        )
        
        # Convert to protobuf
        connected_account_proto = request.to_proto()
        
        # Call the existing connected_accounts method which returns (response, metadata) tuple
        result_tuple = self.connected_accounts.create_connected_account(
            connector=connection_name,
            identifier=identifier,
            connected_account=connected_account_proto,
            organization_id=organization_id,
            user_id=user_id
        )
        
        # Extract the response[0] (the actual CreateConnectedAccountResponse proto object)
        proto_response = result_tuple[0]
        
        # Convert proto to our CreateConnectedAccountResponse class
        return CreateConnectedAccountResponse.from_proto(proto_response)

    def get_or_create_connected_account(
        self,
        connection_name: str,
        identifier: str,
        authorization_details: Optional[Dict[str, Any]] = None,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        **kwargs
    ) -> CreateConnectedAccountResponse:
        """
        Get an existing connected account or create a new one if it doesn't exist
        
        :param connection_name: Connector identifier (required)
        :type: str
        :param identifier: Connected account identifier (required)
        :type: str
        :param authorization_details: Authorization details (OAuth token or static auth) (optional, empty auth will be used if not provided)
        :type: Optional[Dict[str, Any]]
        :param organization_id: Organization ID (optional)
        :type: str
        :param user_id: User ID (optional)
        :type: str
        
        :returns:
            CreateConnectedAccountResponse containing connected account details (either existing or newly created)
        """
        if not connection_name:
            raise ValueError("connection_name is required")
        if not identifier:
            raise ValueError("identifier is required")

        try:
            # First, try to get the existing connected account
            existing_response = self.get_connected_account(
                connection_name=connection_name,
                identifier=identifier,
                organization_id=organization_id,
                user_id=user_id
            )
            
            # If we found it, convert the GetConnectedAccountAuthResponse to CreateConnectedAccountResponse format
            return CreateConnectedAccountResponse(connected_account=existing_response.connected_account)
            
        except ScalekitNotFoundException:
            # Connected account doesn't exist, create a new one
            # Use empty authorization details if none provided
            auth_details = authorization_details if authorization_details is not None else {}
            
            return self.create_connected_account(
                connection_name=connection_name,
                identifier=identifier,
                authorization_details=auth_details,
                organization_id=organization_id,
                user_id=user_id
            )
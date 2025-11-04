from typing import Optional, Any, List, Dict
from scalekit.actions.types import ToolRequest,ExecuteToolResponse,MagicLinkResponse,ListConnectedAccountsResponse,DeleteConnectedAccountResponse,GetConnectedAccountAuthResponse,ToolInput, \
    UpdateConnectedAccountResponse,CreateMcpConfigResponse,ListMcpConfigsResponse,UpdateMcpConfigResponse,DeleteMcpConfigResponse, \
    EnsureMcpInstanceResponse,UpdateMcpInstanceResponse,GetMcpInstanceResponse,ListMcpInstancesResponse,DeleteMcpInstanceResponse,GetMcpInstanceAuthStateResponse, \
    McpConfig,McpConfigConnectionToolMapping
from scalekit.actions.models.responses.create_connected_account_response import CreateConnectedAccountResponse
from scalekit.actions.models.requests.create_connected_account_request import CreateConnectedAccountRequest
from scalekit.actions.models.requests.update_connected_account_request import UpdateConnectedAccountRequest
from scalekit.actions.modifier import (
    Modifier, ModifierType, ToolNames,
    apply_pre_modifiers, apply_post_modifiers
)
from scalekit.common.exceptions import ScalekitNotFoundException




class ActionClient:
    """Class definition for Connect Client"""

    def __init__(self,tools_client, connected_accounts_client, mcp_client=None):
        """
        Initialize ActionClient with tools, connected accounts, and MCP dependencies
        
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
        self._mcp_client = mcp_client
        self._mcp_actions = None
        self._modifiers: List[Modifier] = []
        self._google = None
        self._langchain = None
        
        # Initialize LangChain with tools client and execute callback

        
        # Initialize Google ADK with tools client and execute callback
        #self.google = GoogleADK(tools_client, execute_callback=self.execute_tool)

    @property
    def langchain(self):
        """Get LangChain framework instance"""
        if self._langchain is None:
            try:
                from scalekit.actions.frameworks.langchain import LangChain
                self._langchain = LangChain(self.tools, execute_callback=self.execute_tool)
            except ImportError as e:
                raise ImportError(
                    "LangChain not found. To use LangChain integration, please install:\n"
                    "pip install langchain\n\n"
                    "For more information, see: https://python.langchain.com/docs/\n"
                )
        return self._langchain


    @property
    def google(self):
        """Get Google ADK framework instance"""
        if self._google is None:
            try:
                from scalekit.actions.frameworks.google_adk import GoogleADK
                self._google = GoogleADK(self.tools, execute_callback=self.execute_tool)
            except ImportError as e:
                raise ImportError(
                    "Google ADK not found. To use Google ADK integration, please install:\n"
                    "pip install google-adk\n\n"
                    "For more information, see: https://google.github.io/adk-docs/\n"
                )

        return self._google

    @property
    def mcp(self) -> "ActionMcp":
        """Expose MCP-related operations behind a dedicated helper."""
        if self._mcp_actions is None:
            self._mcp_actions = ActionMcp(self)
        return self._mcp_actions

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

    def list_configs(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_id: Optional[str] = None,
        filter_provider: Optional[str] = None,
        filter_name: Optional[str] = None,
        search: Optional[str] = None,
        **kwargs,
    ) -> ListMcpConfigsResponse:
        """List MCP configurations with optional filters via the action layer."""

        return self.mcp.list_configs(
            page_size=page_size,
            page_token=page_token,
            filter_id=filter_id,
            filter_provider=filter_provider,
            filter_name=filter_name,
            search=search,
        )

    def create_config(
        self,
        name: str,
        description: Optional[str] = None,
        connection_tool_mappings: Optional[List[McpConfigConnectionToolMapping]] = None,
        **kwargs,
    ) -> CreateMcpConfigResponse:
        """Create a new MCP configuration via the action layer."""

        return self.mcp.create_config(
            name=name,
            description=description,
            connection_tool_mappings=connection_tool_mappings,
        )

    def update_config(
        self,
        config_id: str,
        description: Optional[str] = None,
        connection_tool_mappings: Optional[List[McpConfigConnectionToolMapping]] = None,
        **kwargs,
    ) -> UpdateMcpConfigResponse:
        """Update an existing MCP configuration via the action layer."""

        return self.mcp.update_config(
            config_id=config_id,
            description=description,
            connection_tool_mappings=connection_tool_mappings,
        )

    def delete_config(
        self,
        config_id: str,
        **kwargs,
    ) -> DeleteMcpConfigResponse:
        """Delete an MCP configuration via the action layer."""

        return self.mcp.delete_config(config_id=config_id)

    def ensure_instance(
        self,
        config_name: str,
        user_identifier: str,
        name: Optional[str] = None,
        **kwargs,
    ) -> EnsureMcpInstanceResponse:
        """Ensure (create or return) an MCP instance for a given config and user."""

        return self.mcp.ensure_instance(
            config_name=config_name,
            user_identifier=user_identifier,
            name=name,
        )

    def update_instance(
        self,
        instance_id: str,
        name: Optional[str] = None,
        config_name: Optional[str] = None,
        **kwargs,
    ) -> UpdateMcpInstanceResponse:
        """Update mutable fields on an MCP instance."""

        return self.mcp.update_instance(
            instance_id=instance_id,
            name=name,
            config_name=config_name,
        )

    def get_instance(
        self,
        instance_id: str,
        **kwargs,
    ) -> GetMcpInstanceResponse:
        """Fetch a single MCP instance by ID."""

        return self.mcp.get_instance(instance_id=instance_id)

    def list_instances(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_id: Optional[str] = None,
        filter_name: Optional[str] = None,
        filter_config_name: Optional[str] = None,
        filter_user_identifier: Optional[str] = None,
        **kwargs,
    ) -> ListMcpInstancesResponse:
        """List MCP instances with optional filters applied."""

        return self.mcp.list_instances(
            page_size=page_size,
            page_token=page_token,
            filter_id=filter_id,
            filter_name=filter_name,
            filter_config_name=filter_config_name,
            filter_user_identifier=filter_user_identifier,
        )

    def delete_instance(
        self,
        instance_id: str,
        **kwargs,
    ) -> DeleteMcpInstanceResponse:
        """Delete an MCP instance by ID."""

        return self.mcp.delete_instance(instance_id=instance_id)

    def get_instance_auth_state(
        self,
        instance_id: str,
        include_auth_links: Optional[bool] = None,
        **kwargs,
    ) -> GetMcpInstanceAuthStateResponse:
        """Retrieve authentication state for the connections used by an MCP instance.

        :param instance_id: ID of the MCP instance (required)
        :type instance_id: str
        :param include_auth_links: When True, generate fresh auth links for connections
        :type include_auth_links: Optional[bool]
        """

        return self.mcp.get_instance_auth_state(
            instance_id=instance_id,
            include_auth_links=include_auth_links,
        )

    def create_connected_account(
        self,
        connection_name: str,
        identifier: str,
        authorization_details: Dict[str, Any],
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        api_config: Optional[Dict[str, Any]] = None,
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
        :param api_config: Optional API configuration for the connected account (optional)
        :type: Optional[Dict[str, Any]]

        :returns:
            CreateConnectedAccountResponse containing created connected account details
        """
        # Validate required parameters
        if not connection_name:
            raise ValueError("connection_name is required")
        if not identifier:
            raise ValueError("identifier is required")
        
        # Create request model
        request = CreateConnectedAccountRequest(
            connection_name=connection_name,
            identifier=identifier,
            authorization_details=authorization_details,
            organization_id=organization_id,
            user_id=user_id,
            api_config=api_config
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
        api_config: Optional[Dict[str, Any]] = None,
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
        :param api_config: Optional API configuration for the connected account (optional, only used when creating)
        :type: Optional[Dict[str, Any]]

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
                user_id=user_id,
                api_config=api_config
            )

    def update_connected_account(
        self,
        connection_name: str,
        identifier: str,
        authorization_details: Optional[Dict[str, Any]] = None,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        api_config: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> UpdateConnectedAccountResponse:
        """
        Update an existing connected account

        :param connection_name: Connector identifier (required)
        :type: str
        :param identifier: Connected account identifier (required)
        :type: str
        :param authorization_details: Authorization details (OAuth token or static auth) (optional)
        :type: Optional[Dict[str, Any]]
        :param organization_id: Organization ID (optional)
        :type: str
        :param user_id: User ID (optional)
        :type: str
        :param connected_account_id: Connected account ID (optional)
        :type: str
        :param api_config: Optional API configuration for the connected account (optional)
        :type: Optional[Dict[str, Any]]

        :returns:
            UpdateConnectedAccountResponse containing updated connected account details
        """
        # Validate required parameters
        if not connection_name:
            raise ValueError("connection_name is required")
        if not identifier:
            raise ValueError("identifier is required")

        # Create request model
        request = UpdateConnectedAccountRequest(
            connection_name=connection_name,
            identifier=identifier,
            authorization_details=authorization_details,
            organization_id=organization_id,
            user_id=user_id,
            connected_account_id=connected_account_id,
            api_config=api_config
        )

        # Convert to protobuf
        connected_account_proto = request.to_proto()

        # Call the existing connected_accounts method which returns (response, metadata) tuple
        result_tuple = self.connected_accounts.update_connected_account(
            connector=connection_name,
            identifier=identifier,
            connected_account=connected_account_proto,
            organization_id=organization_id,
            user_id=user_id,
            connected_account_id=connected_account_id
        )

        # Extract the response[0] (the actual UpdateConnectedAccountResponse proto object)
        proto_response = result_tuple[0]

        # Convert proto to our UpdateConnectedAccountResponse class
        return UpdateConnectedAccountResponse.from_proto(proto_response)


class ActionMcp:
    """Helper that exposes MCP-specific actions through the ActionClient."""

    def __init__(self, action_client: ActionClient) -> None:
        self._actions = action_client

    def _client(self):
        """Return the underlying MCP client, ensuring it has been configured.

        Returns:
            The low-level MCP client bound to the parent `ActionClient`.

        Raises:
            ValueError: If no MCP client has been provided to the `ActionClient`.
        """
        client = self._actions._mcp_client
        if not client:
            raise ValueError("MCP client not initialized. Please ensure MCP client is available.")
        return client

    def list_configs(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_id: Optional[str] = None,
        filter_provider: Optional[str] = None,
        filter_name: Optional[str] = None,
        search: Optional[str] = None,
    ) -> ListMcpConfigsResponse:
        """List MCP configurations with optional pagination and filtering.

        Args:
            page_size: Maximum number of configs to include in the current page.
            page_token: Cursor token returned by a previous `list_configs` call.
            filter_id: Restrict results to a specific configuration identifier.
            filter_provider: Restrict results to configs for a given provider slug.
            filter_name: Restrict results to configs whose names match exactly.
            search: Free-form search query applied to name field.

        Returns:
            ListMcpConfigsResponse: Parsed wrapper around the proto response.

        Raises:
            ValueError: If an MCP client has not been configured on the action client.
        """
        client = self._client()
        result_tuple = client.list_configs(
            page_size=page_size,
            page_token=page_token,
            filter_id=filter_id,
            filter_provider=filter_provider,
            filter_name=filter_name,
            search=search,
        )
        return ListMcpConfigsResponse.from_proto(result_tuple[0])

    def create_config(
        self,
        name: str,
        description: Optional[str] = None,
        connection_tool_mappings: Optional[List[McpConfigConnectionToolMapping]] = None,
    ) -> CreateMcpConfigResponse:
        """Create a new MCP configuration from the supplied metadata and tool mappings.

        Args:
            name: Human readable name for the configuration.
            description: Optional summary that surfaces in dashboards and APIs.
            connection_tool_mappings: Explicit mapping between connectors and tools.

        Returns:
            CreateMcpConfigResponse: Wrapper containing the created configuration payload.

        Raises:
            ValueError: If `name` is blank or the MCP client is not available.
        """
        if not name:
            raise ValueError("name is required")
        proto_config = McpConfig.to_proto_static(
            name=name,
            description=description,
            connection_tool_mappings=connection_tool_mappings or [],
        )
        result_tuple = self._client().create_config(mcp_config=proto_config)
        return CreateMcpConfigResponse.from_proto(result_tuple[0])

    def update_config(
        self,
        config_id: str,
        description: Optional[str] = None,
        connection_tool_mappings: Optional[List[McpConfigConnectionToolMapping]] = None,
    ) -> UpdateMcpConfigResponse:
        """Update mutable fields on an existing MCP configuration.

        Args:
            config_id: Identifier of the configuration to update.
            description: New description to persist, if provided.
            connection_tool_mappings: Replacement connector-to-tool mappings.

        Returns:
            UpdateMcpConfigResponse: Wrapper containing the updated configuration payload.

        Raises:
            ValueError: If `config_id` is blank or the MCP client is not available.
        """
        if not config_id:
            raise ValueError("config_id is required")
        proto_mappings = None
        if connection_tool_mappings is not None:
            proto_mappings = [mapping.to_proto() for mapping in connection_tool_mappings]
        result_tuple = self._client().update_config(
            config_id=config_id,
            description=description,
            connection_tool_mappings=proto_mappings,
        )
        return UpdateMcpConfigResponse.from_proto(result_tuple[0])

    def delete_config(self, config_id: str) -> DeleteMcpConfigResponse:
        """Delete an MCP configuration so it can no longer be used to create instances.

        Args:
            config_id: Identifier of the configuration to remove.

        Returns:
            DeleteMcpConfigResponse: Wrapper confirming deletion status.

        Raises:
            ValueError: If `config_id` is blank or the MCP client is not available.
        """
        if not config_id:
            raise ValueError("config_id is required")
        result_tuple = self._client().delete_config(config_id=config_id)
        return DeleteMcpConfigResponse.from_proto(result_tuple[0])

    def ensure_instance(
        self,
        config_name: str,
        user_identifier: str,
        name: Optional[str] = None,
    ) -> EnsureMcpInstanceResponse:
        """Create or return an MCP instance matching a configuration and user.

        Args:
            config_name: Name of the MCP configuration to instantiate.
            user_identifier: Identifier that represents the end user or tenant.
            name: Optional name applied to the generated instance.

        Returns:
            EnsureMcpInstanceResponse: Wrapper containing the ensured instance payload.

        Raises:
            ValueError: If required identifiers are missing or the MCP client is absent.
        """
        if not config_name:
            raise ValueError("config_name is required")
        if not user_identifier:
            raise ValueError("user_identifier is required")
        result_tuple = self._client().ensure_instance(
            name=name,
            config_name=config_name,
            user_identifier=user_identifier,
        )
        return EnsureMcpInstanceResponse.from_proto(result_tuple[0])

    def update_instance(
        self,
        instance_id: str,
        name: Optional[str] = None,
        config_name: Optional[str] = None,
    ) -> UpdateMcpInstanceResponse:
        """Apply updates to an existing MCP instance's identifying fields.

        Args:
            instance_id: Identifier of the MCP instance to update.
            name: New display name to assign to the instance.
            config_name: New backing configuration to associate with the instance.

        Returns:
            UpdateMcpInstanceResponse: Wrapper containing the updated instance payload.

        Raises:
            ValueError: If `instance_id` is blank, no updates are provided, or the client is absent.
        """
        if not instance_id:
            raise ValueError("instance_id is required")
        if name is None and config_name is None:
            raise ValueError("At least one of name or config_name must be provided")
        result_tuple = self._client().update_instance(
            instance_id=instance_id,
            name=name,
            config_name=config_name,
        )
        return UpdateMcpInstanceResponse.from_proto(result_tuple[0])

    def get_instance(self, instance_id: str) -> GetMcpInstanceResponse:
        """Fetch a single MCP instance by its identifier.

        Args:
            instance_id: Identifier of the MCP instance to retrieve.

        Returns:
            GetMcpInstanceResponse: Wrapper containing the fetched instance payload.

        Raises:
            ValueError: If `instance_id` is blank or the MCP client is not available.
        """
        if not instance_id:
            raise ValueError("instance_id is required")
        result_tuple = self._client().get_instance(instance_id=instance_id)
        return GetMcpInstanceResponse.from_proto(result_tuple[0])

    def list_instances(
        self,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
        filter_id: Optional[str] = None,
        filter_name: Optional[str] = None,
        filter_config_name: Optional[str] = None,
        filter_user_identifier: Optional[str] = None,
    ) -> ListMcpInstancesResponse:
        """List MCP instances, allowing pagination and filtering by common fields.

        Args:
            page_size: Maximum number of instances to include in the current page.
            page_token: Cursor token returned by a previous `list_instances` call.
            filter_id: Restrict results to a specific instance identifier.
            filter_name: Restrict results to instances with a matching name.
            filter_config_name: Restrict results to instances bound to a configuration name.
            filter_user_identifier: Restrict results to instances for a specific user.

        Returns:
            ListMcpInstancesResponse: Wrapper containing the page of instances.

        Raises:
            ValueError: If the MCP client is not available.
        """
        result_tuple = self._client().list_instances(
            page_size=page_size,
            page_token=page_token,
            filter_id=filter_id,
            filter_name=filter_name,
            filter_config_name=filter_config_name,
            filter_user_identifier=filter_user_identifier,
        )
        return ListMcpInstancesResponse.from_proto(result_tuple[0])

    def delete_instance(self, instance_id: str) -> DeleteMcpInstanceResponse:
        """Delete a specific MCP instance by identifier.

        Args:
            instance_id: Identifier of the MCP instance to delete.

        Returns:
            DeleteMcpInstanceResponse: Wrapper confirming deletion status.

        Raises:
            ValueError: If `instance_id` is blank or the MCP client is not available.
        """
        if not instance_id:
            raise ValueError("instance_id is required")
        result_tuple = self._client().delete_instance(instance_id=instance_id)
        return DeleteMcpInstanceResponse.from_proto(result_tuple[0])

    def get_instance_auth_state(
        self,
        instance_id: str,
        include_auth_links: Optional[bool] = None,
    ) -> GetMcpInstanceAuthStateResponse:
        """Retrieve authorization health for the connectors backing an MCP instance and create new authorization links.

        Args:
            instance_id: Identifier of the MCP instance whose auth state to inspect.
            include_auth_links: When true, mint new auth links for authorization or re-authorization.

        Returns:
            GetMcpInstanceAuthStateResponse: Wrapper containing per-connector auth status.

        Raises:
            ValueError: If `instance_id` is blank or the MCP client is not available.
        """
        if not instance_id:
            raise ValueError("instance_id is required")
        result_tuple = self._client().get_instance_auth_state(
            instance_id=instance_id,
            include_auth_links=include_auth_links,
        )
        return GetMcpInstanceAuthStateResponse.from_proto(result_tuple[0])

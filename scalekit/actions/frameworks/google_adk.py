from typing import Optional, Any, Dict, List, Callable
from scalekit.tools import ToolsClient
from scalekit.v1.tools.tools_pb2 import Filter, ScopedToolFilter
from scalekit.actions.frameworks.types.google_adk_tool import (
    create_scalekit_google_adk_tool, 
    ScalekitGoogleAdkTool,
    check_google_adk_availability,
    get_missing_dependencies
)
from scalekit.actions.frameworks.util import extract_tool_metadata, convert_to_mcp_input_schema


class GoogleADK:
    def __init__(self, tools_client: ToolsClient, execute_callback: Callable):
        if not execute_callback:
            raise ValueError("execute_callback is required. GoogleADK must be initialized with ActionClient's execute_tool method.")
        
        self.tools = tools_client
        self.execute_callback = execute_callback
        self._availability_checked = False
        self._is_available = False
    
    def is_available(self) -> bool:
        """
        Check if Google ADK dependencies are available
        
        :returns: True if all Google ADK dependencies are installed, False otherwise
        """
        if not self._availability_checked:
            self._is_available = check_google_adk_availability()
            self._availability_checked = True
        return self._is_available
    
    def get_missing_dependencies(self) -> Dict[str, str]:
        """
        Get information about missing Google ADK dependencies
        
        :returns: Dictionary mapping dependency names to installation commands
        """
        return get_missing_dependencies()
    
    def get_tools(
        self,
        identifier: str,
        providers: Optional[List[str]] = None,
        tool_names: Optional[List[str]] = None,
        connection_names: Optional[List[str]] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> List[ScalekitGoogleAdkTool]:
        """
        Get scoped tools from Scalekit and convert them to Google ADK compatible tools
        
        :param identifier: Identifier to scope the tools list
        :param providers: List of provider names to filter by
        :param tool_names: List of tool names to filter by
        :param connection_names: List of connection names to filter by
        :param page_size: Maximum number of tools to return per page  
        :param page_token: Token from a previous response for pagination
        :returns: List of Google ADK compatible tools
        :raises ImportError: If Google ADK dependencies are not installed
        """
        if identifier is None or identifier == "":
            raise ValueError("Identifier must be provided to get tools")
        
        # Check if Google ADK dependencies are available
        if not self.is_available():
            missing = self.get_missing_dependencies()
            missing_deps = list(missing.keys())
            install_commands = list(missing.values())
            
            raise ImportError(
                f"Google ADK not found: {', '.join(missing_deps)}\n"
                f"To use Google ADK integration, please install:\n"
                + "\n".join(f"  {cmd}" for cmd in install_commands) + "\n\n"
                "Note: MCP is already included as a Scalekit SDK dependency.\n"
                "For more information, see: https://google.github.io/adk-docs/"
            )

        # Create ScopedToolFilter if any filter parameters are provided
        scoped_filter = None
        if providers or tool_names or connection_names:
            scoped_filter = ScopedToolFilter(
                providers=providers or [],
                tool_names=tool_names or [],
                connection_names=connection_names or []
            )

        # Call list_scoped_tools which returns (response, metadata) tuple
        result_tuple = self.tools.list_scoped_tools(identifier, scoped_filter, page_size, page_token)
        
        # Extract the response[0] (the actual ListScopedToolsResponse proto object)
        response = result_tuple[0]
        
        google_adk_tools = []
        for scoped_tool in response.tools:
            google_adk_tool = self._convert_tool_to_google_adk_tool(
                scoped_tool.tool,
                scoped_tool.connected_account_id
            )
            google_adk_tools.append(google_adk_tool)
            
        return google_adk_tools
    
    def _convert_tool_to_google_adk_tool(self, tool, connected_account_id: str):
        """Convert a Scalekit Tool to Google ADK compatible tool"""
        
        # Extract tool metadata using common utility
        tool_name, tool_description, definition_dict = extract_tool_metadata(tool)
        
        # Convert Scalekit tool to MCP input schema
        input_schema = convert_to_mcp_input_schema(definition_dict)
        
        # Create and return ScalekitGoogleAdkTool instance
        return create_scalekit_google_adk_tool(
            tool_name=tool_name,
            tool_description=tool_description,
            input_schema=input_schema,
            connected_account_id=connected_account_id,
            execute_callback=self.execute_callback
        )
    

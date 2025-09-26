from typing import Optional, Any, Dict, List, Callable
from scalekit.tools import ToolsClient
from scalekit.v1.tools.tools_pb2 import Filter, ScopedToolFilter
from scalekit.actions.frameworks.types.google_adk_tool import (
    ScalekitGoogleAdkTool,
)
from scalekit.actions.frameworks.util import  build_mcp_tool_from_spec, struct_to_dict


class GoogleADK:
    def __init__(self, tools_client: ToolsClient, execute_callback: Callable):
        if not execute_callback:
            raise ValueError("execute_callback is required. GoogleADK must be initialized with ActionClient's execute_tool method.")
        
        self.tools = tools_client
        self.execute_callback = execute_callback

    
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
        

        spec = struct_to_dict(tool)
        mcp_tool = build_mcp_tool_from_spec(spec)

        return ScalekitGoogleAdkTool(
            mcp_tool=mcp_tool,
            connected_account_id=connected_account_id,
            execute_callback=self.execute_callback
        )
    

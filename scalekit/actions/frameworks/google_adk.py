from typing import Optional, Any, Dict, List, Callable
from scalekit.tools import ToolsClient
from scalekit.v1.tools.tools_pb2 import Filter, ScopedToolFilter
from scalekit.actions.frameworks.types.google_adk_tool import (
    ScalekitGoogleAdkTool,
)
from scalekit.actions.frameworks.util import  build_mcp_tool_from_spec, struct_to_dict, warn_truncated_tools


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
        page_token: Optional[str] = None,
        fetch_all: bool = False
    ) -> List[ScalekitGoogleAdkTool]:
        """
        Get scoped tools from Scalekit and convert them to Google ADK compatible tools
        
        :param identifier: Identifier to scope the tools list
        :param providers: List of provider names to filter by
        :param tool_names: List of tool names to filter by
        :param connection_names: List of connection names to filter by
        :param page_size: Maximum number of tools to fetch per underlying request
        :param page_token: Start from this cursor and return only that one page.
            Omit it (the normal case) to receive every matching tool.
        :returns: List of Google ADK compatible tools
        :raises ImportError: If Google ADK dependencies are not installed

        Pagination: this returns a plain list, so there is no cursor for the
        caller to continue with. A single page therefore used to truncate the
        agent's toolset silently. The default is still one page; truncation now
        emits a warning naming how many tools were dropped. Pass
        ``fetch_all=True`` for the whole set, or prefer ``tools.search_tools``
        for a large catalog.
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

        cursor = page_token
        google_adk_tools = []
        seen_cursors = set()

        while True:
            response = self.tools.list_scoped_tools(
                identifier, scoped_filter, page_size, cursor
            )

            for scoped_tool in response.tools:
                google_adk_tools.append(
                    self._convert_tool_to_google_adk_tool(
                        scoped_tool.tool,
                        scoped_tool.connected_account_id,
                    )
                )

            cursor = getattr(response, "next_page_token", "") or ""
            if not cursor:
                break
            if page_token or cursor in seen_cursors:
                break
            if not fetch_all:
                warn_truncated_tools(
                    len(google_adk_tools), getattr(response, "total_size", 0)
                )
                break
            seen_cursors.add(cursor)

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
    

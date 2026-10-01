from typing import Optional, Any, Dict, List, Callable
from langchain_core.tools import StructuredTool
from scalekit.tools import ToolsClient
from scalekit.v1.tools.tools_pb2 import ScopedToolFilter
from scalekit.actions.frameworks.util import extract_tool_metadata, warn_truncated_tools


class LangChain:
    def __init__(self, tools_client: ToolsClient, execute_callback: Callable):
        if not execute_callback:
            raise ValueError("execute_callback is required. LangChain must be initialized with ConnectClient's execute_tool method.")
        
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
    ) -> List[StructuredTool]:
        """
        Get scoped tools from Scalekit and convert them to LangChain StructuredTools
        
        :param identifier: Identifier to scope the tools list
        :param providers: List of provider names to filter by
        :param tool_names: List of tool names to filter by
        :param connection_names: List of connection names to filter by
        :param page_size: Maximum number of tools per request
        :param page_token: Cursor from a previous call; returns just that page
        :param fetch_all: Follow pagination to the end and return every matching
            tool. Off by default -- see the note below.
        :returns: List of LangChain StructuredTools

        Pagination: this returns a plain list, so there is no cursor for the
        caller to continue with. A single page therefore used to truncate the
        agent's toolset *silently* -- a connector with 217 tools handed back 100
        and the agent simply could not see the rest.

        The default is still one page, because auto-paging everything would hide
        an unbounded number of round trips behind one innocuous call (a workspace
        catalog here runs to ~20,000 tools) and would produce a tool list far too
        large to bind to a model usefully. Instead, truncation now emits a warning
        naming exactly how many tools were dropped, so it cannot pass unnoticed.

        Narrow with ``connection_names``/``providers``, raise ``page_size``, or
        pass ``fetch_all=True`` when you genuinely want the whole set. For a large
        catalog prefer ``tools.search_tools``, which ranks by the job to be done
        instead of returning everything.
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
        structured_tools = []
        seen_cursors = set()

        while True:
            response = self.tools.list_scoped_tools(
                identifier, scoped_filter, page_size, cursor
            )

            for scoped_tool in response.tools:
                structured_tools.append(
                    self._convert_tool_to_structured_tool(
                        scoped_tool.tool,
                        scoped_tool.connected_account_id,
                    )
                )

            cursor = getattr(response, "next_page_token", "") or ""
            if not cursor:
                break
            # Caller drove the cursor, or the server repeated one: stop either way.
            if page_token or cursor in seen_cursors:
                break
            if not fetch_all:
                warn_truncated_tools(
                    len(structured_tools), getattr(response, "total_size", 0)
                )
                break
            seen_cursors.add(cursor)

        return structured_tools
    
    def _convert_tool_to_structured_tool(self, tool, connected_account_id: str) -> StructuredTool:
        """Convert a Scalekit Tool to LangChain StructuredTool"""
        
        tool_name, tool_description, definition_dict = extract_tool_metadata(tool)

        args_schema = definition_dict.get("input_schema", {})
        

        def _call(**arguments: Dict[str, Any]) -> str:
            try:
                # Call connect.execute_tool via callback (includes modifiers and enhanced handling)
                response = self.execute_callback(
                    tool_input=arguments,
                    tool_name=tool_name,
                    connected_account_id=connected_account_id
                )


                result_data = response.data if hasattr(response, 'data') else {}

                execution_id = response.execution_id if hasattr(response, 'execution_id') else None
                
                # Format the response
                result_dict = dict(result_data) if result_data else {}
                if execution_id:
                    result_dict['execution_id'] = execution_id
                
                return str(result_dict) if result_dict else f"Tool {tool_name} executed successfully"
                
            except Exception as e:
                return f"Error executing tool {tool_name}: {str(e)}"
        
        # Sync wrapper
        def call_tool_sync(**arguments: Dict[str, Any]) -> str:
            return _call(**arguments)
        
        # Async wrapper
        async def call_tool_async(**arguments: Dict[str, Any]) -> str:
            return _call(**arguments)

        # TODO add metadata to the tool if available
        return StructuredTool(
            name=tool_name,
            description=tool_description,
            args_schema=args_schema,
            func=call_tool_sync,
            coroutine=call_tool_async,
        )
    

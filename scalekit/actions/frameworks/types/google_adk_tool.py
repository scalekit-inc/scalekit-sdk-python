from typing import Any, Dict, Callable, Protocol, runtime_checkable



from mcp.types import Tool as McpBaseTool

# Dynamic imports with helpful error messages
def _import_google_adk():
    """Import Google ADK with helpful error message if not available"""
    try:
        from google.adk.tools.mcp_tool.mcp_tool import MCPTool
        from google.adk.tools.tool_context import ToolContext
        from google.adk.auth.auth_credential import AuthCredential
        return MCPTool, AuthCredential, ToolContext
    except ImportError as e:
        raise ImportError(
            "Google ADK not found. To use Google ADK integration, please install:\n"
            "pip install google-adk\n\n"
            "For more information, see: https://google.github.io/adk-docs/\n"
            f"Original error: {e}"
        )

McpTool,AuthCredential,ToolContext = _import_google_adk()

@runtime_checkable
class McpToolProtocol(Protocol):
    """Protocol for Google ADK McpTool compatibility"""
    def _get_declaration(self): ...
    async def _run_async_impl(self, *, args, tool_context, credentials):  ...





class ScalekitGoogleAdkTool(McpTool,McpToolProtocol):
    """Google ADK Tool wrapper for Scalekit tools inheriting from Google BaseTool"""
    
    def __init__(
        self, 
        mcp_tool: McpBaseTool,
        connected_account_id: str,
        execute_callback: Callable
    ):
        """
        Initialize ScalekitGoogleAdkTool
        :param connected_account_id: Connected account ID for execution
        :param execute_callback: Callback function for tool execution (ActionClient.execute_tool)
        """

        super().__init__(
            mcp_tool=mcp_tool,
            mcp_session_manager=None,
            auth_scheme=None,
            auth_credential=None,
        )

        self.connected_account_id = connected_account_id
        self.execute_callback = execute_callback
        self.name = mcp_tool.name
        self.description = mcp_tool.description






    async def _run_async_impl(self, *, args, **kwargs) -> str:

        try:
            # Call connect.execute_tool via callback (includes modifiers and enhanced handling)
            response = self.execute_callback(
                tool_input=args,
                tool_name=self.name,
                connected_account_id=self.connected_account_id
            )

            result_data = response.data if hasattr(response, 'data') else {}

            execution_id = response.execution_id if hasattr(response, 'execution_id') else None

            # Format the response
            result_dict = dict(result_data) if result_data else {}
            if execution_id:
                result_dict['execution_id'] = execution_id

            return str(result_dict) if result_dict else f"Tool {self.name} executed successfully"

        except Exception as e:
            return f"Error executing tool {self.name}: {str(e)}"






def check_google_adk_availability() -> bool:
    """
    Check if Google ADK dependencies are available
    
    :returns: True if Google ADK is installed, False otherwise
    """
    try:
        _import_google_adk()
        return True
    except ImportError:
        return False


def get_missing_dependencies() -> Dict[str, str]:
    """
    Get information about missing Google ADK dependencies
    
    :returns: Dictionary mapping dependency names to installation commands
    """
    missing = {}
    
    try:
        _import_google_adk()
    except ImportError:
        missing["google-adk"] = "pip install google-adk"
    
    return missing
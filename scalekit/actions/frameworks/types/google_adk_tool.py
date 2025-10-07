from typing import Callable
from mcp.types import Tool as McpBaseTool

# Dynamic imports with helpful error messages
def _import_google_adk():
    """Import Google ADK with helpful error message if not available"""
    try:
        from google.adk.tools.mcp_tool.mcp_tool import McpTool
        from google.adk.tools.tool_context import ToolContext
        from google.adk.auth.auth_credential import AuthCredential
        return McpTool, AuthCredential, ToolContext
    except ImportError as e:
        raise ImportError(
            "Google ADK not found. To use Google ADK integration, please install:\n"
            "pip install google-adk\n\n"
            "For more information, see: https://google.github.io/adk-docs/\n"
            f"Original error: {e}"
        )

McpTool,AuthCredential,ToolContext = _import_google_adk()


class ScalekitGoogleAdkTool(McpTool):
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

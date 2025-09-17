from typing import Any, Dict, Callable, Protocol, runtime_checkable


@runtime_checkable
class McpToolProtocol(Protocol):
    """Protocol for Google ADK McpTool compatibility"""
    def _get_declaration(self): ...
    async def _run_async_impl(self, *, args: Dict[str, Any], tool_context, credential): ...


@runtime_checkable
class AuthCredentialProtocol(Protocol):
    """Protocol for Google ADK AuthCredential compatibility"""
    pass


@runtime_checkable
class ToolContextProtocol(Protocol):
    """Protocol for Google ADK ToolContext compatibility"""
    pass


@runtime_checkable
class McpToolTypeProtocol(Protocol):
    """Protocol for MCP Tool type compatibility"""
    name: str
    description: str
    inputSchema: Dict[str, Any]


@runtime_checkable
class FunctionDeclarationProtocol(Protocol):
    """Protocol for Google AI FunctionDeclaration compatibility"""
    pass


# Dynamic imports with helpful error messages
def _import_google_adk():
    """Import Google ADK with helpful error message if not available"""
    try:
        from google.genai.adk import McpTool
        from google.genai.adk.core import AuthCredential, ToolContext
        return McpTool, AuthCredential, ToolContext
    except ImportError as e:
        raise ImportError(
            "Google ADK not found. To use Google ADK integration, please install:\n"
            "pip install google-genai-adk\n\n"
            "For more information, see: https://github.com/google/generative-ai-adk\n"
            f"Original error: {e}"
        )


def _import_mcp_types():
    """Import MCP types with helpful error message if not available"""
    try:
        from mcp import types as mcp_types
        return mcp_types
    except ImportError as e:
        raise ImportError(
            "MCP (Model Context Protocol) not found. To use Google ADK integration, please install:\n"
            "pip install mcp\n\n"
            "For more information, see: https://github.com/modelcontextprotocol/python-sdk\n"
            f"Original error: {e}"
        )


def _import_function_declaration():
    """Import Google AI FunctionDeclaration with helpful error message if not available"""
    try:
        from google.ai.generativelanguage import FunctionDeclaration
        return FunctionDeclaration
    except ImportError as e:
        raise ImportError(
            "Google AI Generative Language not found. To use Google ADK integration, please install:\n"
            "pip install google-ai-generativelanguage\n\n"
            "For more information, see: https://googleapis.dev/python/generativelanguage/latest/\n"
            f"Original error: {e}"
        )


class ScalekitGoogleAdkTool:
    """Google ADK Tool wrapper for Scalekit tools using MCP protocol"""
    
    def __init__(
        self, 
        tool_name: str,
        tool_description: str,
        input_schema: Dict[str, Any],
        connected_account_id: str,
        execute_callback: Callable
    ):
        """
        Initialize ScalekitGoogleAdkTool
        
        :param tool_name: Name of the Scalekit tool
        :param tool_description: Description of the tool
        :param input_schema: Input schema in MCP format
        :param connected_account_id: Connected account ID for execution
        :param execute_callback: Callback function for tool execution (ActionClient.execute_tool)
        """
        # Import dependencies dynamically
        McpTool, AuthCredential, ToolContext = _import_google_adk()
        mcp_types = _import_mcp_types()
        FunctionDeclaration = _import_function_declaration()
        
        # Store types for later use
        self._McpTool = McpTool
        self._AuthCredential = AuthCredential
        self._ToolContext = ToolContext
        self._FunctionDeclaration = FunctionDeclaration
        
        # Create MCP tool definition
        mcp_tool_def = mcp_types.Tool(
            name=tool_name,
            description=tool_description,
            inputSchema=input_schema
        )
        
        # Initialize as McpTool-like object
        self._mcp_tool = McpTool(
            mcp_tool=mcp_tool_def,
            mcp_session_manager=None,
            auth_scheme=None,
            auth_credential=None,
        )
        
        # Store Scalekit-specific properties
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.input_schema = input_schema
        self.connected_account_id = connected_account_id
        self.execute_callback = execute_callback
    
    def _get_declaration(self):
        """
        Get Google ADK function declaration for this tool
        Delegates to wrapped McpTool which handles MCP -> Google ADK conversion
        """
        return self._mcp_tool._get_declaration()
    
    async def _run_async_impl(
        self, 
        *, 
        args: Dict[str, Any], 
        tool_context, 
        credential
    ) -> str:
        """
        Execute the Scalekit tool using the execute_callback
        
        :param args: Tool execution arguments
        :param tool_context: Google ADK tool context
        :param credential: Authentication credential
        :returns: Tool execution result as string
        """
        try:
            # Call the execute_callback (ActionClient.execute_tool)
            response = await self.execute_callback(
                tool_input=args,
                tool_name=self.tool_name,
                connected_account_id=self.connected_account_id
            )
            
            # Extract result data
            result_data = response.data if hasattr(response, 'data') else {}
            execution_id = response.execution_id if hasattr(response, 'execution_id') else None
            
            # Format the response
            result_dict = dict(result_data) if result_data else {}
            if execution_id:
                result_dict['execution_id'] = execution_id
            
            return str(result_dict) if result_dict else f"Tool {self.tool_name} executed successfully"
            
        except Exception as e:
            return f"Error executing tool {self.tool_name}: {str(e)}"


def create_scalekit_google_adk_tool(
    tool_name: str,
    tool_description: str,
    input_schema: Dict[str, Any],
    connected_account_id: str,
    execute_callback: Callable
) -> ScalekitGoogleAdkTool:
    """
    Factory function to create ScalekitGoogleAdkTool instances
    
    This function will raise ImportError with helpful messages if required
    Google ADK dependencies are not installed.
    
    :param tool_name: Name of the Scalekit tool
    :param tool_description: Description of the tool  
    :param input_schema: Input schema in MCP format
    :param connected_account_id: Connected account ID for execution
    :param execute_callback: Callback function for tool execution
    :returns: ScalekitGoogleAdkTool instance
    :raises ImportError: If Google ADK dependencies are not installed
    """
    try:
        return ScalekitGoogleAdkTool(
            tool_name=tool_name,
            tool_description=tool_description,
            input_schema=input_schema,
            connected_account_id=connected_account_id,
            execute_callback=execute_callback
        )
    except ImportError:
        # Re-raise with context about where the error occurred
        raise


def check_google_adk_availability() -> bool:
    """
    Check if Google ADK dependencies are available
    
    :returns: True if all dependencies are available, False otherwise
    """
    try:
        _import_google_adk()
        _import_mcp_types()
        _import_function_declaration()
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
        missing["google-genai-adk"] = "pip install google-genai-adk"
    
    try:
        _import_mcp_types()
    except ImportError:
        missing["mcp"] = "pip install mcp"
    
    try:
        _import_function_declaration()
    except ImportError:
        missing["google-ai-generativelanguage"] = "pip install google-ai-generativelanguage"
    
    return missing
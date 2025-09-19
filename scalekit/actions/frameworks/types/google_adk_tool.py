from typing import Any, Dict, Callable, Protocol, runtime_checkable


from mcp import types as mcp_types


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
        from google.adk.tools import BaseTool
        from google.adk.core import AuthCredential, ToolContext
        return BaseTool, AuthCredential, ToolContext
    except ImportError as e:
        raise ImportError(
            "Google ADK not found. To use Google ADK integration, please install:\n"
            "pip install google-adk\n\n"
            "For more information, see: https://google.github.io/adk-docs/\n"
            f"Original error: {e}"
        )


class ScalekitGoogleAdkTool:
    """Google ADK Tool wrapper for Scalekit tools inheriting from Google BaseTool"""
    
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
        # Import Google ADK dependencies dynamically  
        BaseTool, AuthCredential, ToolContext = _import_google_adk()
        
        # Store types for later use
        self._BaseTool = BaseTool
        self._AuthCredential = AuthCredential
        self._ToolContext = ToolContext
        
        # Create dynamic class that inherits from BaseTool
        class _DynamicScalekitTool(BaseTool):
            def __init__(self_inner, tool_name, tool_description, input_schema, connected_account_id, execute_callback):
                # Initialize parent BaseTool
                super().__init__()
                
                # Store Scalekit-specific properties
                self_inner.tool_name = tool_name
                self_inner.tool_description = tool_description
                self_inner.input_schema = input_schema
                self_inner.connected_account_id = connected_account_id
                self_inner.execute_callback = execute_callback
            
            def _get_declaration(self_inner):
                """
                Get Google ADK function declaration for this tool
                Override from BaseTool to provide Scalekit tool definition
                """
                # Convert MCP input schema to Google ADK format
                from google.ai.generativelanguage import FunctionDeclaration, Schema, Type
                
                # Create function declaration from Scalekit tool
                return FunctionDeclaration(
                    name=self_inner.tool_name,
                    description=self_inner.tool_description,
                    parameters=Schema(
                        type=Type.OBJECT,
                        properties=self_inner.input_schema.get('properties', {}),
                        required=self_inner.input_schema.get('required', [])
                    )
                )
            
            async def _run_async_impl(
                self_inner, 
                *, 
                args: Dict[str, Any], 
                tool_context, 
                credential
            ) -> str:
                """
                Execute the Scalekit tool using the execute_callback
                Override from BaseTool to provide Scalekit execution
                
                :param args: Tool execution arguments
                :param tool_context: Google ADK tool context
                :param credential: Authentication credential
                :returns: Tool execution result as string
                """
                try:
                    # Call the execute_callback (ActionClient.execute_tool)
                    response = await self_inner.execute_callback(
                        tool_input=args,
                        tool_name=self_inner.tool_name,
                        connected_account_id=self_inner.connected_account_id
                    )
                    
                    # Extract result data
                    result_data = response.data if hasattr(response, 'data') else {}
                    execution_id = response.execution_id if hasattr(response, 'execution_id') else None
                    
                    # Format the response
                    result_dict = dict(result_data) if result_data else {}
                    if execution_id:
                        result_dict['execution_id'] = execution_id
                    
                    return str(result_dict) if result_dict else f"Tool {self_inner.tool_name} executed successfully"
                    
                except Exception as e:
                    return f"Error executing tool {self_inner.tool_name}: {str(e)}"
        
        # Create instance of the dynamic class
        self._tool_instance = _DynamicScalekitTool(
            tool_name, tool_description, input_schema, connected_account_id, execute_callback
        )
        
        # Store properties for external access
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.input_schema = input_schema
        self.connected_account_id = connected_account_id
        self.execute_callback = execute_callback
    
    def _get_declaration(self):
        """Delegate to the BaseTool instance"""
        return self._tool_instance._get_declaration()
    
    async def _run_async_impl(self, *, args: Dict[str, Any], tool_context, credential) -> str:
        """Delegate to the BaseTool instance"""
        return await self._tool_instance._run_async_impl(args=args, tool_context=tool_context, credential=credential)
    
    def get_tool_instance(self):
        """Get the actual Google ADK BaseTool instance"""
        return self._tool_instance


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
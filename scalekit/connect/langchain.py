from typing import Optional, Any, Dict, List, Callable
from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel, Field, create_model
from scalekit.tools import ToolsClient
from scalekit.v1.tools.tools_pb2 import Filter


class LangChain:
    def __init__(self, tools_client: ToolsClient, execute_callback: Callable):
        if not execute_callback:
            raise ValueError("execute_callback is required. LangChain must be initialized with ConnectClient's execute_tool method.")
        
        self.tools = tools_client
        self.execute_callback = execute_callback
    
    def get_tools(
        self,
        identifier:str,
        filter: Optional[Filter] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> List[StructuredTool]:
        """
        Get tools from Scalekit and convert them to LangChain StructuredTools
        
        :param filter: Filter parameters for listing tools
        :param page_size: Maximum number of tools to return per page  
        :param page_token: Token from a previous response for pagination
        :returns: List of LangChain StructuredTools
        """
        # Get tools from Scalekit

        if identifier is None or identifier == "":
            raise ValueError("Identifier must be provided to get tools")

        # Call list_tools which returns (response, metadata) tuple
        result_tuple = self.tools.list_tools(filter, page_size, page_token)
        
        # Extract the response[0] (the actual ListToolsResponse proto object)
        response = result_tuple[0]
        
        structured_tools = []
        for tool in response.tools:
            structured_tool = self._convert_tool_to_structured_tool(tool, identifier)
            structured_tools.append(structured_tool)
            
        return structured_tools
    
    def _convert_tool_to_structured_tool(self, tool, identifier: str) -> StructuredTool:
        """Convert a Scalekit Tool to LangChain StructuredTool"""
        
        # Extract definition dict
        definition_dict = self._struct_to_dict(tool.definition) if hasattr(tool, 'definition') and tool.definition else {}
        
        # Use definition fields directly
        tool_name = definition_dict.get('name', getattr(tool, 'provider', 'unknown') + '_tool')
        tool_description = definition_dict.get('description', 'Scalekit tool')
        
        # Create args schema from tool definition input_schema
        args_schema = definition_dict.get("input_schema", {})
        
        # Single implementation of tool execution logic
        def _call(**arguments: Dict[str, Any]) -> str:
            try:
                # Import here to avoid circular imports
                from scalekit.connect.types import ToolInput

                
                # Call connect.execute_tool via callback (includes modifiers and enhanced handling)
                response = self.execute_callback(
                    tool_input=arguments,
                    tool_name=tool_name,
                    identifier=identifier
                )

                # Handle the ConnectClient ExecuteToolResponse
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
    
    def _struct_to_dict(self, struct) -> Dict[str, Any]:
        """Convert protobuf Struct to Python dict"""
        from google.protobuf.json_format import MessageToDict
        return MessageToDict(struct)
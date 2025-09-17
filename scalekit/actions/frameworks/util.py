from typing import Dict, Any


def struct_to_dict(struct) -> Dict[str, Any]:
    """
    Convert protobuf Struct to Python dict
    
    :param struct: Protobuf Struct object
    :returns: Python dictionary representation
    """
    from google.protobuf.json_format import MessageToDict
    return MessageToDict(struct)


def extract_tool_metadata(tool, default_provider: str = 'unknown'):
    """
    Extract common tool metadata from Scalekit tool definition
    
    :param tool: Scalekit tool object
    :param default_provider: Default provider name if not found
    :returns: Tuple of (tool_name, tool_description, definition_dict)
    """
    definition_dict = struct_to_dict(tool.definition) if hasattr(tool, 'definition') and tool.definition else {}
    
    tool_name = definition_dict.get('name', getattr(tool, 'provider', default_provider) + '_tool')
    tool_description = definition_dict.get('description', 'Scalekit tool')
    
    return tool_name, tool_description, definition_dict


def convert_to_mcp_input_schema(definition_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Scalekit tool definition to MCP input schema format
    
    :param definition_dict: Scalekit tool definition dictionary
    :returns: MCP-compatible input schema
    """
    input_schema = definition_dict.get("input_schema", {})
    
    return {
        "type": "object",
        "properties": input_schema.get("properties", {}),
        "required": input_schema.get("required", [])
    }
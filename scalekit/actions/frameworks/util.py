from typing import Dict, Any
from mcp.types import Tool as McpBaseTool, ToolAnnotations


def struct_to_dict(struct) -> Dict[str, Any]:
    """
    Convert protobuf Struct to Python dict

    Despite the shared name, this is NOT the same operation as
    scalekit.utils.proto.struct_to_dict and the two are deliberately not
    consolidated. That one converts a google.protobuf.Struct; this one is
    called on whole messages too -- google_adk.py passes an entire Tool
    here to get {"provider": ..., "definition": {...}} -- which only
    MessageToDict can do. It also returns {} rather than None for an
    empty input, because both callers below go straight on to .get(...).

    Use scalekit.utils.proto.struct_to_dict (or the .data_dict /
    .definition_dict / .metadata_dict properties) for Struct fields.

    :param struct: Protobuf Struct object, or any protobuf message
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

def build_mcp_tool_from_spec(spec: Dict[str, Any]) -> McpBaseTool:
    """Converts the raw spec dict into an MCP Tool instance.

    Mapping performed:
      definition.input_schema -> inputSchema
      definition.annotations.* snake_case -> ToolAnnotations camelCase
    """
    definition = spec["definition"]
    ann_raw = definition.get("annotations", {})
    ann_map = {
        "title": ann_raw.get("title"),
        "readOnlyHint": ann_raw.get("read_only_hint"),
        "destructiveHint": ann_raw.get("destructive_hint"),
        "idempotentHint": ann_raw.get("idempotent_hint"),
        "openWorldHint": ann_raw.get("open_world_hint"),
    }
    # Filter out None values
    ann_clean = {k: v for k, v in ann_map.items() if v is not None}
    annotations = ToolAnnotations(**ann_clean) if ann_clean else None

    mcp_tool = McpBaseTool(
        name=definition["name"],
        description=definition.get("description"),
        inputSchema=definition["input_schema"],
        annotations=annotations,
    )
    return mcp_tool
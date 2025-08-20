from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

from scalekit.connect.models.tool_mapping import ToolMapping

# TODO: Add validation for tool_mappings to ensure unique tool names across mappings
class McpRequest(BaseModel):
    """MCP request configuration with validation"""


    identifier: Optional[str] = Field(
        None,
        description="Identifier for the connected account", 
        min_length=1,
        max_length=255
    )
    tool_mappings: List[ToolMapping]
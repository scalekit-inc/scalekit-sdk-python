from typing import List, Union, Any, Dict, Optional, Literal, Callable
from .models.tool_input_output import ToolInput, ToolOutput

# Type definitions
ModifierType = Literal["pre", "post"]
ToolNames = Union[str, List[str]]
PreModifierFunction = Callable[[ToolInput], ToolInput]
PostModifierFunction = Callable[[ToolOutput], ToolOutput]
ToolModifierFunction = Union[PreModifierFunction, PostModifierFunction]
ToolIO = Union[ToolInput, ToolOutput]

class Modifier:
    """A modifier that can transform inputs (pre) or outputs (post) for specific tools"""
    
    def __init__(
        self, 
        tool_names: ToolNames, 
        modifier_type: ModifierType, 
        **kwargs: Any
    ) -> None:
        # Convert single tool name to list for consistency
        if isinstance(tool_names, str):
            self.tool_names: List[str] = [tool_names]
        else:
            self.tool_names = tool_names
            
        self.type: ModifierType = modifier_type
        self.func:Optional[ToolModifierFunction] = None  # Will hold the actual modifier function
        
    def apply(self, tool_name: str, data: ToolIO) -> ToolIO:
        """Apply this modifier if the tool_name matches"""
        if tool_name in self.tool_names and self.func is not None:
            return self.func(data)
        return data

# Stateless utility functions
def apply_modifiers(
    tool_name: str, 
    data: ToolIO,
    modifiers: List[Modifier], 
    modifier_type: ModifierType
) -> ToolIO:
    """Apply all modifiers of a specific type for a tool"""
    modified_data = data

    """
    TODO optimize this filtering with a dict, 
    Add validation to ensure modifiers are unique per tool
    """

    applicable_modifiers = [
        m for m in modifiers 
        if m.type == modifier_type and tool_name in m.tool_names
    ]
    
    # Apply each modifier in sequence
    for modifier in applicable_modifiers:
        modified_data = modifier.apply(tool_name, modified_data)
    
    return modified_data

def apply_pre_modifiers(tool_name: str, data: ToolIO, modifiers: List[Modifier]) -> ToolIO:
    """Convenience function to apply pre-modifiers"""
    return apply_modifiers(tool_name, data, modifiers, "pre")

def apply_post_modifiers(tool_name: str, data: ToolIO, modifiers: List[Modifier]) -> ToolIO:
    """Convenience function to apply post-modifiers"""
    return apply_modifiers(tool_name, data, modifiers, "post")
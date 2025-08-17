from typing import List, Union, Any, Dict, Optional, Literal

# Type definitions
ModifierType = Literal["pre", "post"]
ToolNames = Union[str, List[str]]

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
        self.func = None  # Will hold the actual modifier function
        self.params: Dict[str, Any] = kwargs  # Store additional parameters
        
    def apply(self, tool_name: str, data: Any) -> Any:
        """Apply this modifier if the tool_name matches"""
        if tool_name in self.tool_names and self.func is not None:
            return self.func(tool_name, data)
        return data

# Stateless utility functions
def apply_modifiers(
    tool_name: str, 
    data: Any, 
    modifiers: List[Modifier], 
    modifier_type: ModifierType
) -> Any:
    """Apply all modifiers of a specific type for a tool"""
    modified_data = data
    
    # Filter modifiers that match the tool and type
    applicable_modifiers = [
        m for m in modifiers 
        if m.type == modifier_type and tool_name in m.tool_names
    ]
    
    # Apply each modifier in sequence
    for modifier in applicable_modifiers:
        modified_data = modifier.apply(tool_name, modified_data)
    
    return modified_data

def apply_pre_modifiers(tool_name: str, data: Any, modifiers: List[Modifier]) -> Any:
    """Convenience function to apply pre-modifiers"""
    return apply_modifiers(tool_name, data, modifiers, "pre")

def apply_post_modifiers(tool_name: str, data: Any, modifiers: List[Modifier]) -> Any:
    """Convenience function to apply post-modifiers"""
    return apply_modifiers(tool_name, data, modifiers, "post")
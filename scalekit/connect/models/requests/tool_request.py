from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ToolRequest(BaseModel):
    """Tool request configuration with validation"""
    
    tool_version: Optional[str] = Field(
        None, 
        description="Version of the tool to use",
        min_length=1,
        max_length=50
    )
    tool_name: Optional[str] = Field(
        None, 
        description="Name of the tool",
        min_length=1,
        max_length=100
    )
    identifier: Optional[str] = Field(
        None, 
        description="Unique identifier for execution",
        min_length=1,
        max_length=255
    )

    @field_validator('tool_version')
    @classmethod
    def validate_tool_version(cls, v):
        """Validate tool version format"""
        if v is not None:
            if not isinstance(v, str):
                raise ValueError('tool_version must be a string')
            v = v.strip()
            if not v:
                raise ValueError('tool_version cannot be empty or whitespace only')
            # Basic semantic version validation (optional)
            if '.' in v and not all(part.isdigit() for part in v.split('.')):
                raise ValueError('tool_version should follow semantic versioning (e.g., 1.0.0)')
        return v

    @field_validator('tool_name')
    @classmethod
    def validate_tool_name(cls, v):
        """Validate tool name format"""
        if v is not None:
            if not isinstance(v, str):
                raise ValueError('tool_name must be a string')
            v = v.strip()
            if not v:
                raise ValueError('tool_name cannot be empty or whitespace only')
            # Tool name should contain valid characters
            if not all(c.isalnum() or c in '.-_' for c in v):
                raise ValueError('tool_name can only contain alphanumeric characters, dots, hyphens, and underscores')
        return v

    @field_validator('identifier')
    @classmethod
    def validate_identifier(cls, v):
        """Validate identifier format"""
        if v is not None:
            if not isinstance(v, str):
                raise ValueError('identifier must be a string')
            v = v.strip()
            if not v:
                raise ValueError('identifier cannot be empty or whitespace only')
            # Identifier should be alphanumeric with some special characters
            if not all(c.isalnum() or c in '-_.' for c in v):
                raise ValueError('identifier can only contain alphanumeric characters, hyphens, underscores, and dots')
        return v

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        str_strip_whitespace = True
        use_enum_values = True
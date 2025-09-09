from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class ToolMapping(BaseModel):
    """Tool mapping configuration with validation"""
    
    tool_names: Optional[List[str]]
    connection_name: Optional[str]
    status: Optional[str] = None


    def to_proto_dict(self) -> dict:
        """
        Convert to dictionary format suitable for protobuf
        
        :returns:
            Dictionary representation for protobuf conversion
        """
        return {
            'tool_names': self.tool_names or [],
            'connection_name': self.connection_name or '',
        }

    @classmethod
    def from_proto(cls, proto_mapping) -> 'ToolMapping':
        """
        Create ToolMapping from protobuf ToolMapping
        
        :param proto_mapping: The protobuf ToolMapping object
        :type proto_mapping: ToolMapping (from mcp_pb2)
        
        :returns:
            ToolMapping instance
        """
        return cls(
            tool_names=list(proto_mapping.tool_names) if proto_mapping.tool_names else None,
            connection_name=proto_mapping.connection_name if proto_mapping.connection_name else None,
            status = proto_mapping.status if proto_mapping.status else None
        )


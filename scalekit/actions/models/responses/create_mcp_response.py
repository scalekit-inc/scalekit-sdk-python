from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from google.protobuf.json_format import MessageToDict

from scalekit.connect.models.tool_mapping import ToolMapping


class CreateMcpResponse(BaseModel):
    """Create MCP response with one-to-one mapping to proto CreateMcpResponse"""
    
    id: Optional[str]
    identifier: Optional[str]
    url: Optional[str]
    tool_mappings: Optional[List[ToolMapping]]

    @classmethod
    def from_proto(cls, proto_response) -> 'CreateMcpResponse':
        """
        Create CreateMcpResponse from protobuf CreateMcpResponse
        
        :param proto_response: The protobuf CreateMcpResponse object
        :type proto_response: CreateMcpResponse (from mcp_pb2)
        
        :returns:
            CreateMcpResponse instance
        """
        mcp = proto_response.mcp if proto_response.mcp else None
        
        if mcp:
            # Convert tool_mappings from protobuf to dict
            tool_mappings = []
            if mcp.tool_mappings:
                for mapping in mcp.tool_mappings:
                    tool_mappings.append(
                        ToolMapping.from_proto(mapping)
                    )
            
            return cls(
                id=mcp.id if mcp.id else None,
                identifier=mcp.connected_account_identifier if mcp.connected_account_identifier else None,
                tool_mappings=tool_mappings if tool_mappings else None,
                url=mcp.url if mcp.url else None
            )
        
        return cls()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation
        
        :returns:
            Dictionary representation of the response
        """
        return {
            "id": self.mcp_id,
            "identifier": self.connected_account_identifier,
            "tool_mappings": self.tool_mappings,
            "url": self.url
        }
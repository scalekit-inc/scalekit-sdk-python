from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from google.protobuf.json_format import MessageToDict

from scalekit.connect.models.tool_mapping import ToolMapping


class GetMcpResponse(BaseModel):
    """Get MCP response with one-to-one mapping to proto GetMcpResponse"""
    
    mcp_id: Optional[str]
    connected_account_identifier: Optional[str]
    tool_mappings: Optional[List[ToolMapping]]
    url: Optional[str]

    @classmethod
    def from_proto(cls, proto_response) -> 'GetMcpResponse':
        """
        Create GetMcpResponse from protobuf GetMcpResponse
        
        :param proto_response: The protobuf GetMcpResponse object
        :type proto_response: GetMcpResponse (from mcp_pb2)
        
        :returns:
            GetMcpResponse instance
        """
        mcp = proto_response.mcp if proto_response.mcp else None
        
        if mcp:
            # Convert tool_mappings from protobuf to dict
            tool_mappings = []
            if mcp.tool_mappings:
                for mapping in mcp.tool_mappings:
                    tool_mappings.append({
                        'tool_names': list(mapping.tool_names) if mapping.tool_names else [],
                        'connection_name': mapping.connection_name if mapping.connection_name else None,
                        'status': mapping.status if mapping.status else None
                    })
            
            return cls(
                mcp_id=mcp.id if mcp.id else None,
                connected_account_identifier=mcp.connected_account_identifier if mcp.connected_account_identifier else None,
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
            "mcp_id": self.mcp_id,
            "connected_account_identifier": self.connected_account_identifier,
            "tool_mappings": self.tool_mappings,
            "url": self.url
        }
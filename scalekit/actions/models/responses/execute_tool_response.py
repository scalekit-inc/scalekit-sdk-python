from typing import Optional, Dict, Any

from  ..tool_input_output import ToolOutput
from pydantic import BaseModel, Field
from google.protobuf.json_format import MessageToDict



class ExecuteToolResponse(BaseModel):
    """Execute tool response with one-to-one mapping to proto ExecuteToolResponse"""
    
    data: Optional[ToolOutput] = Field(
        None,
        description="Free-flowing JSON parameters for the tool execution"
    )
    execution_id: Optional[str] = Field(
        None,
        description="Unique identifier for the tool execution"
    )

    @classmethod
    def from_proto(cls, proto_response) -> 'ExecuteToolResponse':
        """
        Create ExecuteToolResponse from protobuf ExecuteToolResponse
        
        :param proto_response: The protobuf ExecuteToolResponse object
        :type proto_response: ExecuteToolResponse (from tools_pb2)
        
        :returns:
            ExecuteToolResponse instance
        """
        # Convert protobuf Struct to dict
        data = None
        if proto_response.data:
            data = MessageToDict(proto_response.data)

        return cls(
            data=data,
            execution_id=proto_response.execution_id if proto_response.execution_id else None
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation
        
        :returns:
            Dictionary representation of the response
        """
        return {
            "data": self.data,
            "execution_id": self.execution_id
        }

    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        arbitrary_types_allowed = True
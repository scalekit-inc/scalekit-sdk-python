from typing import Optional

from scalekit.core import CoreClient
from scalekit.v1.tools.tools_pb2 import *
from scalekit.v1.tools.tools_pb2_grpc import ToolServiceStub
from google.protobuf import empty_pb2


class ToolsClient:
    """Class definition for Tools Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for Tools Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.tool_service = ToolServiceStub(
            self.core_client.grpc_secure_channel
        )



    def list_tools(
        self,
        filter: Optional[Filter] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListToolsResponse:
        """
        Method to list tools

        :param filter           : Filter parameters for listing tools
        :type                   : ``` Filter ```
        :param page_size        : Maximum number of tools to return per page
        :type                   : ``` int ```
        :param page_token       : Token from a previous response for pagination
        :type                   : ``` str ```

        :returns:
            List Tools Response
        """
        return self.core_client.grpc_exec(
            self.tool_service.ListTools.with_call,
            ListToolsRequest(
                filter=filter,
                page_size=page_size,
                page_token=page_token
            ),
        )





    def list_scoped_tools(
        self,
        identifier: str,
        filter: Optional[ScopedToolFilter] = None,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListScopedToolsResponse:
        """
        Method to list scoped tools for a specific identifier

        :param identifier       : Identifier to scope the tools list
        :type                   : ``` str ```
        :param filter           : Filter parameters for scoped tools
        :type                   : ``` ScopedToolFilter ```
        :param page_size        : Maximum number of tools to return per page
        :type                   : ``` int ```
        :param page_token       : Token from a previous response for pagination
        :type                   : ``` str ```

        :returns:
            List Scoped Tools Response
        """
        return self.core_client.grpc_exec(
            self.tool_service.ListScopedTools.with_call,
            ListScopedToolsRequest(
                identifier=identifier,
                filter=filter,
                page_size=page_size,
                page_token=page_token
            ),
        )

    def execute_tool(
        self,
        tool_name: str,
        identifier: str,
        params: Optional[dict] = None,
        connected_account_id: Optional[str] = None
    ) -> ExecuteToolResponse:
        """
        Method to execute a tool using a connected account

        :param tool_name        : Name of the tool to execute
        :type                   : ``` str ```
        :param identifier       : Identifier of the connected account
        :type                   : ``` str ```
        :param params           : Parameters for tool execution
        :type                   : ``` dict ```
        :param connected_account_id : ID of the connected account to use for tool execution
        :type                   : ``` str ```

        :returns:
            Execute Tool Response
        """
        from google.protobuf import struct_pb2
        
        params_struct = None
        if params:
            params_struct = struct_pb2.Struct()
            params_struct.update(params)
        
        return self.core_client.grpc_exec(
            self.tool_service.ExecuteTool.with_call,
            ExecuteToolRequest(
                tool_name=tool_name,
                identifier=identifier,
                params=params_struct,
                connected_account_id=connected_account_id
            ),
        )
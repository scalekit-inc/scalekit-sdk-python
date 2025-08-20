from typing import Optional, List, Dict, Any

from scalekit.core import CoreClient
from scalekit.v1.mcp.mcp_pb2 import *
from scalekit.v1.mcp.mcp_pb2_grpc import McpServiceStub


class McpClient:
    """Class definition for MCP Client"""

    def __init__(self, core_client: CoreClient):
        """
        Initializer for MCP Client

        :param core_client    : CoreClient Object
        :type                 : ``` obj ```
        :returns
            None
        """
        self.core_client = core_client
        self.mcp_service = McpServiceStub(
            self.core_client.grpc_secure_channel
        )

    def create_mcp(self, mcp: Mcp) -> CreateMcpResponse:
        """
        Method to create or return existing MCP with given configuration

        :param mcp            : MCP configuration to create or update
        :type                 : ``` Mcp ```

        :returns:
            Create MCP Response
        """
        return self.core_client.grpc_exec(
            self.mcp_service.CreateMcp.with_call,
            CreateMcpRequest(mcp=mcp),
        )

    def get_mcp(self, mcp_id: str) -> GetMcpResponse:
        """
        Method to get an existing MCP by ID

        :param mcp_id         : ID of the MCP to retrieve
        :type                 : ``` str ```

        :returns:
            Get MCP Response
        """
        return self.core_client.grpc_exec(
            self.mcp_service.GetMcp.with_call,
            GetMcpRequest(mcp_id=mcp_id),
        )

    def list_mcps(
        self,
        connected_account_identifier: Optional[str] = None,
        link_token: Optional[str] = None
    ) -> ListMcpResponse:
        """
        Method to list MCPs with optional filters

        :param connected_account_identifier : Filter by connected account identifier
        :type                              : ``` str ```
        :param link_token                  : Filter by link token
        :type                              : ``` str ```

        :returns:
            List MCP Response
        """
        filter_obj = None
        if connected_account_identifier is not None or link_token is not None:
            filter_obj = ListMcpRequest.Filter(
                connected_account_identifier=connected_account_identifier,
                link_token=link_token
            )
        
        return self.core_client.grpc_exec(
            self.mcp_service.ListMcp.with_call,
            ListMcpRequest(filter=filter_obj),
        )

    def delete_mcp(self, mcp_id: str) -> DeleteMcpResponse:
        """
        Method to delete an MCP by ID

        :param mcp_id         : ID of the MCP to delete
        :type                 : ``` str ```

        :returns:
            Delete MCP Response
        """
        return self.core_client.grpc_exec(
            self.mcp_service.DeleteMcp.with_call,
            DeleteMcpRequest(mcp_id=mcp_id),
        )
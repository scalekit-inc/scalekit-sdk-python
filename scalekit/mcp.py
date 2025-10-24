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

    def list_configs(
            self,
            page_size: Optional[int] = None,
            page_token: Optional[str] = None,
            filter_id: Optional[str] = None,
            filter_provider: Optional[str] = None,
            filter_name: Optional[str] = None,
            search: Optional[str] = None,
    ) -> ListMcpConfigsResponse:
        """
        Method to list MCP Configurations with optional filters

        :param page_size          : Number of items per page
        :type                     : ``` int ```
        :param page_token         : Token for the page to retrieve
        :type                     : ``` str ```
        :param filter_id          : Filter by MCP Config ID
        :type                     : ``` str ```
        :param filter_provider    : Filter by provider
        :type                     : ``` str ```
        :param filter_name        : Filter by name
        :type                     : ``` str ```
        :param search             : Search term
        :type                     : ``` str ```

        :returns:
            List MCP Configs Response
        """
        filter_obj = None
        if any(x is not None for x in (filter_id, filter_provider, filter_name, search)):
            filter_obj = ListMcpConfigsRequest.Filter(
                id=filter_id or "",
                provider=filter_provider or "",
                name=filter_name or "",
            )

        return self.core_client.grpc_exec(
            self.mcp_service.ListMcpConfigs.with_call,
            ListMcpConfigsRequest(
                page_size=page_size or 0,
                page_token=page_token or "",
                filter=filter_obj,
                search=search or ""
            ),
        )

    def create_config(self, mcp_config: McpConfig) -> CreateMcpConfigResponse:
        """
        Method to create a new MCP Configuration

        :param mcp_config        : MCP Configuration to create
        :type                     : ``` McpConfig ```

        :returns:
            Create MCP Config Response
        """
        return self.core_client.grpc_exec(
            self.mcp_service.CreateMcpConfig.with_call,
            CreateMcpConfigRequest(config=mcp_config),
        )

    def update_config(self,
                      config_id: str,
                      description: Optional[str] = None,
                      connection_tool_mappings: Optional[List[McpConfigConnectionToolMapping]] = None) -> UpdateMcpConfigResponse:
        """
        Method to update an existing MCP Configuration
        :param config_id                 : ID of the MCP Configuration to update
        :type                            : ``` str ```
        :param description               : New description for the MCP Configuration
        :type                            : ``` str ```
        :param connection_tool_mappings  : New connection tool mappings for the MCP Configuration
        :type                            : ``` List[McpConfigConnectionToolMapping] ```
        :returns:
            Update MCP Config Response
        """
        request = UpdateMcpConfigRequest(config_id=config_id)
        if description is not None:
            request.description = description
        if connection_tool_mappings is not None:
            request.connection_tool_mappings.extend(connection_tool_mappings)
        return self.core_client.grpc_exec(
            self.mcp_service.UpdateMcpConfig.with_call,
            request,
    )

    def delete_config(self, config_id: str) -> DeleteMcpConfigResponse:
        """
        Method to delete an MCP Configuration by ID

        :param config_id      : ID of the MCP Configuration to delete
        :type                 : ``` str ```

        :returns:
            Delete MCP Config Response
        """
        return self.core_client.grpc_exec(
            self.mcp_service.DeleteMcpConfig.with_call,
            DeleteMcpConfigRequest(config_id=config_id),
        )

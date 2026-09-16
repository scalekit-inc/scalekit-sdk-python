from typing import Optional

from scalekit.core import CoreClient
from scalekit.util import struct_to_dict
from scalekit.v1.tools.tools_pb2 import *
from scalekit.v1.tools.tools_pb2_grpc import ToolServiceStub
from google.protobuf import empty_pb2

# Purely additive convenience properties -- see struct_to_dict's docstring
# for why `dict(response.data)` / `dict(tool.definition)` are not enough
# for any tool response/definition with nested objects or lists. This does
# not change what `.data`/`.definition` return or their type in any way
# (both are still the exact same google.protobuf.Struct as before), so
# every existing call site keeps working unmodified -- these are new
# attributes, not replacements. Registered here (rather than as a method on
# ToolsClient) so they're available directly on any Tool/ExecuteToolResponse
# instance, including ones nested inside list/search responses.
ExecuteToolResponse.data_dict = property(lambda self: struct_to_dict(self.data))
Tool.definition_dict = property(lambda self: struct_to_dict(self.definition))


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
            timeout=self.core_client.tool_call_timeout_s,
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

        Each returned tool's `.tool.definition` is a google.protobuf.Struct.
        Use `.tool.definition_dict` to get a fully-converted native dict
        (handles nested objects like `input_schema.properties` correctly) --
        `dict(.tool.definition)` only shallow-converts and leaves nested
        fields as raw protobuf objects.
        """
        return self.core_client.grpc_exec(
            self.tool_service.ListScopedTools.with_call,
            ListScopedToolsRequest(
                identifier=identifier,
                filter=filter,
                page_size=page_size,
                page_token=page_token
            ),
            timeout=self.core_client.tool_call_timeout_s,
        )

    def search_tools(
        self,
        query: str,
        identifier: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> SearchToolsResponse:
        """
        Method to search tools ranked by relevance to a natural-language query

        Each result's ``score`` is a relevance score where higher is better; it is only
        comparable within the results of a single response, not across separate calls.

        ``connections`` on each result is populated only when ``identifier`` is set: an
        empty list means the identifier has no connection at all for that tool's provider
        (not an error, and different from ``NEEDS_CONNECTION``, which means a connected
        account row exists but is inactive); more than one entry means the identifier has
        accounts on multiple connections for that provider (for example, two Slack
        workspaces) -- inspect each entry's own ``readiness_state`` rather than assuming
        one answer for the whole tool.

        :param query            : Natural-language query or keywords describing the job to be done
        :type                   : ``` str ```
        :param identifier       : Optional connected-account identifier; when set, each result is
                                  annotated with readiness for this identifier's connections
        :type                   : ``` str ```
        :param top_k            : Maximum number of ranked results to return (default 10, capped at 50)
        :type                   : ``` int ```

        :returns:
            Search Tools Response
        """
        return self.core_client.grpc_exec(
            self.tool_service.SearchTools.with_call,
            SearchToolsRequest(
                query=query,
                identifier=identifier,
                top_k=top_k
            ),
            timeout=self.core_client.tool_call_timeout_s,
        )

    def execute_tool(
        self,
        tool_name: str,
        identifier: str,
        params: Optional[dict] = None,
        connected_account_id: Optional[str] = None,
        connection_name: Optional[str] = None
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
        :param connection_name  : Name of the connector/provider (e.g., 'Google Workspace', 'Slack')
        :type                   : ``` str ```

        :returns:
            Execute Tool Response

        The response's `.data` is a google.protobuf.Struct. Use
        `.data_dict` to get a fully-converted native dict/list -- a real
        tool response often has nested objects or lists (e.g. a GitHub
        repo's `owner`/`permissions`/`topics`), and `dict(response.data)`
        only shallow-converts, leaving those nested fields as raw protobuf
        objects instead of plain dict/list.
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
                connected_account_id=connected_account_id,
                connector=connection_name
            ),
            timeout=self.core_client.tool_call_timeout_s,
            # A retry on UNAVAILABLE can double-execute a non-idempotent call —
            # sending an email twice, for example. Opt out here specifically;
            # see grpc_exec's retry_on_unavailable for the broader rationale.
            retry_on_unavailable=False,
        )

import json
from typing import Iterable, Optional

from scalekit.common.exceptions import ScalekitException
from scalekit.core import CoreClient
from scalekit.v1.tools.tools_pb2 import *
from scalekit.v1.tools.tools_pb2_grpc import ToolServiceStub
from google.protobuf import empty_pb2, struct_pb2

# List requests ask the server for each tool definition as JSON text
# (definition_json) instead of a google.protobuf.Struct. A Struct costs 2-3
# protobuf nesting levels per JSON level, and Python protobuf (upb) refuses to
# decode past 100 levels with no way to raise that, so one deeply nested
# input_schema made the whole page fail with "Exception deserializing
# response!" (SK-3047). A string adds no nesting.
_LIST_DEFINITION_FORMAT = DEFINITION_FORMAT_JSON_STRING


def _restore_definitions(tools: Iterable[Tool]) -> None:
    """Rebuild each tool's ``definition`` from ``definition_json`` and clear
    ``definition_json``, so callers get the same ``Tool`` as before. A server
    that does not know ``definition_format`` keeps sending ``definition``, and
    the tool is left as it is.

    Building a deep Struct in memory is fine; only decoding one from protobuf
    bytes hits the limit. So a definition nested deeper than about 33 levels
    can be read, compared, deep-copied and converted with ``MessageToDict``,
    but anything that serializes and re-parses it (pickle, ``copy.copy``,
    ``MergeFrom``, passing it to a message constructor) still fails in Python
    protobuf. Before this change, listing such a tool failed outright."""
    for tool in tools:
        if not tool.HasField("definition_json"):
            continue
        try:
            definition = json.loads(tool.definition_json)
            if not isinstance(definition, dict):
                raise ValueError("expected a JSON object")
            restored = struct_pb2.Struct()
            restored.update(definition)
        except (ValueError, TypeError, AttributeError, OverflowError) as exc:
            raise ScalekitException(f"Tool {tool.id} has an invalid definition: {exc}") from exc
        # CopyFrom keeps the deep Struct in memory; MergeFrom would re-parse it.
        tool.definition.CopyFrom(restored)
        tool.ClearField("definition_json")


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
        result = self.core_client.grpc_exec(
            self.tool_service.ListTools.with_call,
            ListToolsRequest(
                filter=filter,
                page_size=page_size,
                page_token=page_token,
                definition_format=_LIST_DEFINITION_FORMAT,
            ),
            timeout=self.core_client.tool_call_timeout_s,
        )
        _restore_definitions(result[0].tools)
        return result





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
        result = self.core_client.grpc_exec(
            self.tool_service.ListScopedTools.with_call,
            ListScopedToolsRequest(
                identifier=identifier,
                filter=filter,
                page_size=page_size,
                page_token=page_token,
                definition_format=_LIST_DEFINITION_FORMAT,
            ),
            timeout=self.core_client.tool_call_timeout_s,
        )
        _restore_definitions(scoped.tool for scoped in result[0].tools if scoped.HasField("tool"))
        return result

    def list_available_tools(
        self,
        identifier: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListAvailableToolsResponse:
        """
        Method to list every tool available to an identifier across its connected accounts

        :param identifier       : Connected-account identifier: your app's ID for the user, such as user_123
        :type                   : ``` str ```
        :param page_size        : Maximum number of tools to return per page
        :type                   : ``` int ```
        :param page_token       : Token from a previous response for pagination
        :type                   : ``` str ```

        :returns:
            List Available Tools Response
        """
        result = self.core_client.grpc_exec(
            self.tool_service.ListAvailableTools.with_call,
            ListAvailableToolsRequest(
                identifier=identifier,
                page_size=page_size,
                page_token=page_token,
                definition_format=_LIST_DEFINITION_FORMAT,
            ),
            timeout=self.core_client.tool_call_timeout_s,
        )
        _restore_definitions(result[0].tools)
        return result

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

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

        Tools of a custom connector are listed too, under the names the server gives them:
        ``a-<connector>_<operation>`` for a connector created from an OpenAPI spec, and
        ``c-<connector>_<tool>`` for a custom MCP connector. A custom MCP connector's tools
        belong to a connected account, so name that account with ``Filter.connector`` (the
        connection name) together with ``Filter.identifier``, or with
        ``Filter.connected_account_id``. A connector created from an OpenAPI spec has one set
        of tools for every connected account: list them with ``Filter.provider`` set to the
        connector's identifier (at most 50 characters), or with ``Filter.connector`` set to
        the name of a connection on it. They are not listed where OpenAPI-sourced
        connectors are not enabled for the environment.

        ``Filter.query`` (3 to 100 characters) searches the names of global tools only, so
        it never returns a custom connector's tools, and a page of search results holds at
        most 100 tools.

        :param filter           : Filter parameters for listing tools
        :type                   : ``` Filter ```
        :param page_size        : Maximum number of tools to return per page. The server
                                  uses 300 when this is omitted or 0, and reduces a value
                                  above 1000 to 1000 instead of rejecting it
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

        A connector created from an OpenAPI spec has one set of tools for every connected
        account, so they are listed with the connected account of this identifier on that
        connector (add the connector's identifier to ``ScopedToolFilter.providers``, its
        connection name to ``connection_names``, or the tool names to ``tool_names``). A
        custom MCP connector's tools are those of that identifier's connected account.

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

    def list_available_tools(
        self,
        identifier: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListAvailableToolsResponse:
        """
        Method to list every tool available to a connected account identifier

        Returns the tools of all the connectors this identifier has a connected account on,
        including a connector created from an OpenAPI spec (its tools are shared by every
        account) and a custom MCP connector's tools for that identifier's account. An
        identifier with no connected account gets an empty list rather than an error.

        Each Tool.definition arrives as a ``google.protobuf.Struct``. Python protobuf
        decodes at most about 100 levels of nested messages, and each JSON object in a
        definition takes several, so a single tool definition nested about 30 objects deep
        makes the whole call fail to decode. The same limit already applies to ``list_tools``. The
        server can return definitions as JSON text instead (``definition_format``), but this
        SDK version does not request that yet.

        :param identifier       : Identifier of the connected account. Required
        :type                   : ``` str ```
        :param page_size        : Maximum number of tools to return per page. The server
                                  uses 100 when this is omitted or 0
        :type                   : ``` int ```
        :param page_token       : Token from a previous response for pagination
        :type                   : ``` str ```

        :returns:
            List Available Tools Response
        """
        return self.core_client.grpc_exec(
            self.tool_service.ListAvailableTools.with_call,
            ListAvailableToolsRequest(
                identifier=identifier,
                page_size=page_size,
                page_token=page_token
            ),
            timeout=self.core_client.tool_call_timeout_s,
        )

    def refresh_tools(
        self,
        identifier: Optional[str] = None,
        connected_account_id: Optional[str] = None,
        connection_name: Optional[str] = None,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> RefreshToolsResponse:
        """
        Method to resync the tools of a custom MCP connected account

        Re-queries the upstream MCP server for its tool list and updates the cached
        catalog of the connected account: new and changed tools are added, tools the server
        no longer offers are removed, and the full refreshed list comes back. Use it when
        the upstream server has added, renamed or removed tools; the catalog is also
        resynced when an account is created, authenticated again or has its metadata updated.

        It works only for a custom MCP connector. A connector created from an OpenAPI spec
        gets its tools from a tool collection run instead; use
        ``trigger_tool_collection`` on the providers client.

        Each Tool.definition arrives as a ``google.protobuf.Struct``. Python protobuf
        decodes at most about 100 levels of nested messages, and each JSON object in a
        definition takes several, so a single tool definition nested about 30 objects deep
        makes the whole call fail to decode. The same limit already applies to ``list_tools``. The
        server can return definitions as JSON text instead (``definition_format``), but this
        SDK version does not request that yet.

        Name the connected account with ``connected_account_id``, or with
        ``connection_name`` together with ``identifier`` (and, when the same identifier
        exists in more than one organization or for more than one user, ``organization_id``
        or ``user_id``). An account that was created with ``organization_id`` (and ``user_id``)
        and no ``identifier`` is named by ``connection_name`` together with those IDs. A call
        that gives only ``connection_name`` or only ``identifier`` names no account: it raises
        ValueError before anything is sent, where the server would answer 400.

        Errors surface as ScalekitServerException subclasses: ScalekitBadRequestException
        (400) when the account is not a custom MCP connector ('connected account is not a
        custom MCP connector') or custom MCP tools are not enabled for the environment;
        ScalekitNotFoundException (404) when no connected account matches;
        ScalekitTooManyRequestsException (429, error code DISCOVERY_IN_PROGRESS) when a
        refresh of the same account is already running, in which case retry in a few seconds;
        and ScalekitInternalServerException (500) when the upstream server cannot be queried.

        :param identifier           : Identifier of the connected account, used together
                                      with connection_name
        :type                       : ``` str ```
        :param connected_account_id : ID of the connected account to refresh
        :type                       : ``` str ```
        :param connection_name      : Name of the connection the account belongs to; pass it
                                      with identifier, or with organization_id
        :type                       : ``` str ```
        :param organization_id      : Organization ID to narrow the account lookup, or, with
                                      connection_name and no identifier, to name an account
                                      that was created without one
        :type                       : ``` str ```
        :param user_id              : User ID to narrow the account lookup
        :type                       : ``` str ```

        :returns:
            Refresh Tools Response

        :raises ValueError: If neither connected_account_id nor connection_name together with
                            identifier (or organization_id) is given
        """
        if not (connected_account_id or (connection_name and (identifier or organization_id))):
            raise ValueError(
                "connected_account_id, or connection_name together with identifier (or organization_id), "
                "is required to refresh tools"
            )
        return self.core_client.grpc_exec(
            self.tool_service.RefreshTools.with_call,
            RefreshToolsRequest(
                identifier=identifier,
                connected_account_id=connected_account_id,
                connector=connection_name,
                organization_id=organization_id,
                user_id=user_id
            ),
            timeout=self.core_client.tool_call_timeout_s,
        )

    def delete_custom_tool(
        self,
        tool_name: str,
        provider_identifier: Optional[str] = None
    ):
        """
        Method to delete one tool of a connector created from an OpenAPI spec, by its name

        Deletes the tool now, for example to keep one operation of an API away from your
        agents. Name it as ``list_tools`` lists it: ``a-<connector>_<operation>``. The name
        alone picks the tool, because it carries its connector's name and an environment has
        one OpenAPI-sourced connector of that name. The server matches the name in lower case
        (ASCII letters only), as it stores tool names, so this method sends ``tool_name``
        exactly as given: it does not change the case and does not trim spaces.

        Only a tool of an OpenAPI-sourced connector of your environment can be deleted this
        way. Any other name (an MCP tool, a global tool, another environment's tool, a tool
        whose connector is missing or not OpenAPI-sourced, an unknown name) is answered with
        404, and the answer does not say which of these it was.

        The deletion is not permanent. A full sync of the connector creates the tool again
        (same name, new id) while its operation is still in the spec, for example after the
        spec's content or the connector's base URL has changed; a sync that is skipped because
        nothing changed does not. To drop an operation for good, remove it from the spec.
        Connections and virtual MCP configurations that listed the tool keep its name: running
        it fails with 400 ``custom tool not found: <name>``, a virtual MCP server does not
        serve it, and saving a configuration that still names it is refused with 400, until
        the name is removed or a sync brings the tool back.

        While a sync of the connector is queued or running, nothing is deleted, because that
        sync would create the tool again: the call fails with 409 and you call it again after
        the run has finished. ``get_tool_collection_run`` with ``run_id="latest"`` usually shows
        that run, but not always: the server refuses while any run of the connector has not
        finished, and an older unfinished run can sit behind a newer finished one. The 409 is
        what counts, so call again until it stops; the server fails a run that makes no
        progress after about 30 minutes. The server checks this when the call arrives, so a
        sync that starts right afterwards can still bring the tool back.

        The call uses the client's tool-call timeout (``tool_call_timeout_s``). It is sent
        again when the service is unavailable, like most calls of this client, because
        deleting by name is safe to repeat: the repeat of a delete that already happened is
        answered with 404 and changes nothing. A 404 therefore means "not there now", not
        "never there": after a call that was sent again, or after a timeout (a timeout is not
        sent again, but the server may have finished the delete all the same), the tool may be
        gone because of the first attempt. (``trigger_tool_collection`` is not sent again,
        because a repeat of it queues a second run.)

        Errors surface as ScalekitServerException subclasses: ScalekitBadRequestException
        (400) when the name is longer than 2048 characters (an empty name never gets this far:
        it raises ValueError first), when provider_identifier is longer than 512 characters,
        when either has a control character, or when OpenAPI-sourced connectors are not
        enabled for the environment (FEATURE_NOT_ENABLED); ScalekitNotFoundException (404) as
        described above, which includes a leftover tool of a connector that no longer exists
        or is not OpenAPI-sourced; ScalekitConflictException (409), with nothing deleted,
        either with error code RESOURCE_ALREADY_EXISTS while a sync of the connector is queued
        or running, or with TOOL_NAME_AMBIGUOUS when tools of more than one connector of the
        environment have this name (leftover rows of an earlier connector), whose message
        names two of the connectors: call again with provider_identifier set to the full
        identifier of the OpenAPI-sourced connector whose tool should be deleted; and
        ScalekitInternalServerException (500) when the server failed, which does not say
        whether the tool is gone: list the connector's tools with ``list_tools`` before
        calling again.

        :param tool_name           : Name of the tool to delete, as listed for its connector.
                                     Required; at most 2048 characters
        :type                      : ``` str ```
        :param provider_identifier : Full identifier of the connector that owns the tool,
                                     exactly as the connector's identifier is returned (for
                                     example "ACME:1234"); unlike the tool name it is matched
                                     exactly, case included. Optional: needed only to answer
                                     the 409 TOOL_NAME_AMBIGUOUS case. It must name an
                                     OpenAPI-sourced connector that still exists. At most 512
                                     characters
        :type                      : ``` str ```

        :returns:
            Tuple of (google.protobuf.Empty, grpc.Call). The response has no content;
            ``response[1].code().name == 'OK'`` on success.

        :raises ValueError: If tool_name is not a non-empty string (one that is only whitespace
                            counts as empty); nothing is sent
        """
        if not isinstance(tool_name, str) or not tool_name.strip():
            raise ValueError("tool_name must be a non-empty string to delete a custom tool")
        return self.core_client.grpc_exec(
            self.tool_service.DeleteCustomTool.with_call,
            DeleteCustomToolRequest(
                tool_name=tool_name,
                provider_identifier=provider_identifier
            ),
            timeout=self.core_client.tool_call_timeout_s,
            # Default retry on UNAVAILABLE, unlike execute_tool and trigger_tool_collection:
            # a delete by name can be repeated without harm. See the docstring for what the
            # caller sees when the first attempt had already done the work.
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

        A custom connector's tools run like any other: ``a-<connector>_<operation>`` for a
        connector created from an OpenAPI spec, ``c-<connector>_<tool>`` for a custom MCP
        connector. Use a connected account of a connection on the tool's own connector. A name
        that does not exist for the account's connector, which includes an OpenAPI-sourced
        tool where that capability is not enabled for the environment, fails with 400
        ``custom tool not found: <name>``.

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

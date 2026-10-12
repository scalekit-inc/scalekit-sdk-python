from typing import Any, Iterator, Optional

from scalekit.core import CoreClient
from scalekit.v1.tools.tools_pb2 import *
from scalekit.v1.tools.tools_pb2_grpc import ToolServiceStub
from google.protobuf import empty_pb2


class _ToolsResult(tuple):
    """A ``.with_call`` result that behaves as both the tuple and the message.

    The stubs are invoked through ``<Rpc>.with_call``, which returns a
    ``(response, call)`` pair. Returning that pair made every annotation on this
    client wrong: callers were told they had a ``ListToolsResponse`` and actually
    held a tuple, so ``response.tools`` raised AttributeError -- while mypy and
    pyright validated the broken access and would have rejected the correct one.

    Returning the bare message would fix the annotation but break every caller
    doing ``response[0]``, which is exactly what the published reference taught
    for ``search_tools``. So this subclasses ``tuple`` -- indexing, unpacking and
    ``isinstance(x, tuple)`` all keep working -- and forwards attribute access to
    the response message, so ``response.tools`` works too.

    Both spellings are therefore valid and no existing code has to change.
    """

    __slots__ = ()

    def __new__(cls, result: Any):
        if isinstance(result, tuple):
            return super().__new__(cls, result)
        # Tolerate a plain message, in case a call site stops using with_call.
        return super().__new__(cls, (result, None))

    @property
    def response(self):
        """The response message, named explicitly for readability."""
        return self[0]

    def __getattr__(self, name: str) -> Any:
        # Only reached when normal lookup fails, so tuple's own attributes win.
        try:
            return getattr(self[0], name)
        except AttributeError as exc:
            raise AttributeError(name) from exc

    def __repr__(self) -> str:
        return repr(self[0])


def _unwrap(result: Any) -> Any:
    """Wrap a ``.with_call`` result so it reads as the message or the tuple."""
    return _ToolsResult(result)


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
        return _unwrap(self.core_client.grpc_exec(
            self.tool_service.ListTools.with_call,
            ListToolsRequest(
                filter=filter,
                page_size=page_size,
                page_token=page_token
            ),
            timeout=self.core_client.tool_call_timeout_s,
        ))





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
        return _unwrap(self.core_client.grpc_exec(
            self.tool_service.ListScopedTools.with_call,
            ListScopedToolsRequest(
                identifier=identifier,
                filter=filter,
                page_size=page_size,
                page_token=page_token
            ),
            timeout=self.core_client.tool_call_timeout_s,
        ))

    def iter_scoped_tools(
        self,
        identifier: str,
        filter: Optional[ScopedToolFilter] = None,
        page_size: Optional[int] = None
    ) -> Iterator[Any]:
        """Yield every scoped tool for an identifier, following pagination.

        Removes the cursor bookkeeping from the caller::

            for scoped in scalekit_client.tools.iter_scoped_tools(
                "user@example.com",
                ScopedToolFilter(connection_names=["github-connect"]),
            ):
                ...

        Lazy: pages are fetched as you consume them, so nothing is buffered up
        front and ``itertools.islice`` gives you a hard cap.

        Before reaching for this, consider whether you want every tool at all.
        Binding a whole connector to a model is expensive -- 217 GitHub tools is
        roughly 85k tokens of schema on every request, and large tool counts hurt
        selection accuracy. :meth:`search_tools` answers "which tools fit this
        job" in a fraction of that and annotates each result with readiness.
        This method is for the cases that genuinely need the full set: catalog
        UIs, admin tooling, sync jobs.
        """
        cursor = None
        seen_cursors = set()
        while True:
            response = self.list_scoped_tools(identifier, filter, page_size, cursor)
            for scoped_tool in response.tools:
                yield scoped_tool
            cursor = getattr(response, "next_page_token", "") or ""
            if not cursor or cursor in seen_cursors:
                break
            seen_cursors.add(cursor)

    def list_available_tools(
        self,
        identifier: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> ListAvailableToolsResponse:
        """
        Method to list tools that can be made available for one identifier

        Use this instead of ``list_scoped_tools`` when you need the candidate set --
        what this identifier *could* connect -- rather than the tools already bound
        to an active connected account.

        :param identifier       : Identifier to list available tools for
        :type                   : ``` str ```
        :param page_size        : Maximum number of tools to return per page
        :type                   : ``` int ```
        :param page_token       : Token from a previous response for pagination
        :type                   : ``` str ```

        :returns:
            List Available Tools Response
        """
        return _unwrap(self.core_client.grpc_exec(
            self.tool_service.ListAvailableTools.with_call,
            ListAvailableToolsRequest(
                identifier=identifier,
                page_size=page_size,
                page_token=page_token
            ),
            timeout=self.core_client.tool_call_timeout_s,
        ))

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
        return _unwrap(self.core_client.grpc_exec(
            self.tool_service.SearchTools.with_call,
            SearchToolsRequest(
                query=query,
                identifier=identifier,
                top_k=top_k
            ),
            timeout=self.core_client.tool_call_timeout_s,
        ))

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

        return _unwrap(self.core_client.grpc_exec(
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
        ))

"""Response models for the ``list_scoped_tools`` tool-discovery method."""

from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.responses.list_tools_response import Tool
from scalekit.v1.tools.tools_pb2 import ListScopedToolsResponse as ListScopedToolsResponseProto
from scalekit.v1.tools.tools_pb2 import ScopedTool as ScopedToolProto


class ScopedTool(BaseModel):
    """A tool together with the identifier and connected account it is scoped to.

    Attributes:
        tool: The tool itself. ``None`` when the server sent no tool for this
            entry.
        identifier: The connected-account identifier the tool is scoped to, e.g.
            an end user's email or workspace ID.
        connected_account_id: ID of the connected account (``ca_...``) that backs
            the tool for this identifier. Pass it to ``execute_tool``.

    Example:
        from scalekit.v1.tools.tools_pb2 import ScopedToolFilter

        page = client.actions.list_scoped_tools(
            "user@example.com",
            filter=ScopedToolFilter(providers=["slack"]),
        )
        for scoped in page.tools:
            print(scoped.identifier, scoped.connected_account_id)

    """

    tool: Optional[Tool] = Field(
        None,
        description="The tool scoped to the identifier",
    )
    identifier: Optional[str] = Field(
        None,
        description="Connected-account identifier the tool is scoped to",
    )
    connected_account_id: Optional[str] = Field(
        None,
        description="ID of the connected account (ca_...) backing this tool",
    )

    @classmethod
    def from_proto(cls, proto_scoped_tool: ScopedToolProto) -> "ScopedTool":
        """Build the model from the ``ScopedTool`` proto message.

        Args:
            proto_scoped_tool: One entry of ``ListScopedToolsResponse.tools``.

        Returns:
            The mapped scoped tool. ``tool`` is ``None`` only when the message
            field is absent, checked with ``HasField`` rather than truthiness, so
            a tool whose fields are all empty is still returned.

        Example:
            scoped = ScopedTool.from_proto(response.tools[0])

        """
        tool = (
            Tool.from_proto(proto_scoped_tool.tool) if proto_scoped_tool.HasField("tool") else None
        )
        return cls(
            tool=tool,
            identifier=proto_scoped_tool.identifier or None,
            connected_account_id=proto_scoped_tool.connected_account_id or None,
        )

    def to_dict(self) -> dict:
        """Serialise the scoped tool to a dictionary.

        Returns:
            A dictionary with the model's field names; ``tool`` is converted by
            ``Tool.to_dict`` or left as ``None``.

        """
        return {
            "tool": self.tool.to_dict() if self.tool else None,
            "identifier": self.identifier,
            "connected_account_id": self.connected_account_id,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True


class ListScopedToolsResponse(BaseModel):
    """One page of the tools already scoped to an identifier.

    Returned by ``client.actions.list_scoped_tools``. Unlike
    ``ListAvailableToolsResponse``, every entry names the connected account that
    backs the tool for that identifier.

    Attributes:
        tools: The scoped tools on this page. Empty when nothing is scoped to the
            identifier.
        total_count: Total number of scoped tools across all pages
            (``total_size`` on the wire). ``0`` when there are none -- the wire
            field has no presence, so zero is never reported as ``None``.
        next_page_token: Pass as ``page_token`` to fetch the next page. ``None``
            on the last page.
        previous_page_token: Token for the previous page (``prev_page_token`` on
            the wire). ``None`` on the first page.

    Example:
        from scalekit.v1.tools.tools_pb2 import ScopedToolFilter

        page = client.actions.list_scoped_tools(
            "user@example.com",
            filter=ScopedToolFilter(providers=["slack"]),
            page_size=20,
        )
        for scoped in page.tools:
            print(scoped.connected_account_id, scoped.tool.provider)

    """

    tools: List[ScopedTool] = Field(
        default_factory=list,
        description="Tools scoped to the identifier on this page",
    )
    total_count: Optional[int] = Field(
        None,
        description="Total number of scoped tools across all pages",
        alias="total_size",
    )
    next_page_token: Optional[str] = Field(
        None,
        description="Token for the next page of results",
    )
    previous_page_token: Optional[str] = Field(
        None,
        description="Token for the previous page of results",
        alias="prev_page_token",
    )

    @classmethod
    def from_proto(cls, proto_response: ListScopedToolsResponseProto) -> "ListScopedToolsResponse":
        """Build the model from the ``ListScopedToolsResponse`` proto message.

        Args:
            proto_response: The proto message returned by
                ``ToolsClient.list_scoped_tools``.

        Returns:
            The mapped page. Empty page tokens become ``None``;
            ``total_count`` carries ``total_size`` as sent, including ``0``;
            ``tools`` is always a list, never ``None``.

        Example:
            from scalekit.v1.tools.tools_pb2 import ScopedToolFilter

            response, _ = client.tools.list_scoped_tools(
                "user@example.com", filter=ScopedToolFilter()
            )
            page = ListScopedToolsResponse.from_proto(response)

        """
        return cls(
            tools=[ScopedTool.from_proto(proto_tool) for proto_tool in proto_response.tools],
            total_count=proto_response.total_size,
            next_page_token=proto_response.next_page_token or None,
            previous_page_token=proto_response.prev_page_token or None,
        )

    def to_dict(self) -> dict:
        """Serialise the page to a dictionary.

        Returns:
            A dictionary with the same keys as the model's field names, with
            every nested scoped tool converted by ``ScopedTool.to_dict``.

        """
        return {
            "tools": [scoped_tool.to_dict() for scoped_tool in self.tools],
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True

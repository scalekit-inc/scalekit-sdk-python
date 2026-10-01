"""Response model for the ``list_available_tools`` tool-discovery methods."""

from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.actions.models.responses.list_tools_response import Tool
from scalekit.v1.tools.tools_pb2 import (
    ListAvailableToolsResponse as ListAvailableToolsResponseProto,
)


class ListAvailableToolsResponse(BaseModel):
    """One page of the tools an identifier can use, across all of its connections.

    Returned by ``client.actions.list_available_tools``. Reuses the same ``Tool``
    model as ``ListToolsResponse``, so code that reads a listed tool reads an
    available tool unchanged.

    Attributes:
        tools: The tools on this page. Empty when the identifier has no
            connection that exposes a tool.
        total_count: Total number of available tools across all pages
            (``total_size`` on the wire). ``0`` when there are none -- the wire
            field has no presence, so zero is never reported as ``None``.
        next_page_token: Pass as ``page_token`` to fetch the next page. ``None``
            on the last page.
        previous_page_token: Token for the previous page (``prev_page_token`` on
            the wire). ``None`` on the first page.

    Example:
        page = client.actions.list_available_tools("user@example.com", page_size=20)
        for tool in page.tools:
            print(tool.provider, tool.definition)

    """

    tools: List[Tool] = Field(
        default_factory=list,
        description="Tools available to the identifier on this page",
    )
    total_count: Optional[int] = Field(
        None,
        description="Total number of available tools across all pages",
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
    def from_proto(
        cls, proto_response: ListAvailableToolsResponseProto
    ) -> "ListAvailableToolsResponse":
        """Build the model from the ``ListAvailableToolsResponse`` proto message.

        Args:
            proto_response: The proto message returned by
                ``ToolsClient.list_available_tools``.

        Returns:
            The mapped page. Empty page tokens become ``None``;
            ``total_count`` carries ``total_size`` as sent, including ``0``;
            ``tools`` is always a list, never ``None``.

        Example:
            response, _ = client.tools.list_available_tools("user@example.com")
            page = ListAvailableToolsResponse.from_proto(response)

        """
        return cls(
            tools=[Tool.from_proto(proto_tool) for proto_tool in proto_response.tools],
            total_count=proto_response.total_size,
            next_page_token=proto_response.next_page_token or None,
            previous_page_token=proto_response.prev_page_token or None,
        )

    def to_dict(self) -> dict:
        """Serialise the page to a dictionary.

        Returns:
            A dictionary with the same keys as the model's field names, with
            every nested tool converted by ``Tool.to_dict``.

        """
        return {
            "tools": [tool.to_dict() for tool in self.tools],
            "total_count": self.total_count,
            "next_page_token": self.next_page_token,
            "previous_page_token": self.previous_page_token,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True

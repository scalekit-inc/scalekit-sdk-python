"""Response models for the ``search_tools`` tool-discovery method."""

from typing import List, Optional

from pydantic import BaseModel, Field

from scalekit.v1.tools.tools_pb2 import ConnectionReadiness as ConnectionReadinessProto
from scalekit.v1.tools.tools_pb2 import SearchedTool as SearchedToolProto
from scalekit.v1.tools.tools_pb2 import SearchToolsResponse as SearchToolsResponseProto
from scalekit.v1.tools.tools_pb2 import ToolReadinessState


def _readiness_state_name(value: int) -> str:
    """Map a ``ToolReadinessState`` wire value to its name without ever raising.

    ``ToolReadinessState.Name`` raises ``ValueError`` for a value these generated
    stubs do not know about, which is exactly what happens when the backend ships
    a new readiness state before the SDK is regenerated. Falling back to the
    decimal value keeps an older SDK readable instead of crashing the caller.

    Args:
        value: The enum value as it arrived on the wire.

    Returns:
        The enum name, e.g. ``"TOOL_READINESS_STATE_READY"``, or the decimal value
        as a string when the name is unknown to this build of the SDK.

    """
    try:
        return str(ToolReadinessState.Name(value))
    except ValueError:
        return str(int(value))


class ConnectionReadiness(BaseModel):
    """Whether one of an identifier's connections can run a searched tool now.

    Only populated when ``search_tools`` is called with an ``identifier``. An
    empty ``connections`` list on a result means the identifier has no connection
    at all for that tool's provider -- which is not an error, and is different
    from ``TOOL_READINESS_STATE_NEEDS_CONNECTION``, which means a connected
    account exists but is inactive.

    Attributes:
        connection_name: Name of the connection this readiness applies to.
        connected_account_id: ID of the connected account (``ca_...``). Pass it to
            ``execute_tool`` only when ``readiness_state`` is
            ``"TOOL_READINESS_STATE_READY"``.
        readiness_state: The readiness state name, e.g.
            ``"TOOL_READINESS_STATE_READY"``,
            ``"TOOL_READINESS_STATE_NEEDS_CONNECTION"`` or
            ``"TOOL_READINESS_STATE_NEEDS_REAUTH"``. A state this SDK build does
            not know is reported as its decimal value rather than raising, so
            compare against the names you handle and treat anything else as not
            ready.

    Example:
        for connection in result.tools[0].connections:
            if connection.readiness_state == "TOOL_READINESS_STATE_READY":
                print(connection.connected_account_id)

    """

    connection_name: Optional[str] = Field(
        None,
        description="Name of the connection this readiness applies to",
    )
    connected_account_id: Optional[str] = Field(
        None,
        description="ID of the connected account (ca_...) backing this connection",
    )
    readiness_state: Optional[str] = Field(
        None,
        description="Readiness state name, or its decimal value if unknown to this SDK build",
    )

    @classmethod
    def from_proto(cls, proto_connection: ConnectionReadinessProto) -> "ConnectionReadiness":
        """Build the model from the ``ConnectionReadiness`` proto message.

        Args:
            proto_connection: One entry of ``SearchedTool.connections``.

        Returns:
            The mapped readiness. ``readiness_state`` is always set when built
            from a proto message, including for the unspecified state.

        Example:
            readiness = ConnectionReadiness.from_proto(tool.connections[0])

        """
        return cls(
            connection_name=proto_connection.connection_name or None,
            connected_account_id=proto_connection.connected_account_id or None,
            readiness_state=_readiness_state_name(proto_connection.readiness_state),
        )

    def to_dict(self) -> dict:
        """Serialise the readiness to a dictionary.

        Returns:
            A dictionary with the model's field names.

        """
        return {
            "connection_name": self.connection_name,
            "connected_account_id": self.connected_account_id,
            "readiness_state": self.readiness_state,
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True


class SearchedTool(BaseModel):
    """One ranked result of a tool search.

    Attributes:
        name: Tool name, as passed to ``execute_tool``.
        provider: Provider that exposes the tool, e.g. ``"slack"``.
        description: What the tool does, as indexed for search.
        score: Relevance score, higher is better. Only comparable within the
            results of a single response, never across separate calls.
        connections: Per-connection readiness for the identifier that was
            searched. Empty when ``search_tools`` was called without an
            ``identifier``, or when that identifier has no connection for this
            tool's provider.

    Example:
        result = client.actions.search_tools("send a slack message", identifier="user@example.com")
        for tool in result.tools:
            print(tool.name, tool.score)

    """

    name: Optional[str] = Field(
        None,
        description="Tool name, as passed to execute_tool",
    )
    provider: Optional[str] = Field(
        None,
        description="Provider that exposes this tool (e.g., 'slack', 'github')",
    )
    description: Optional[str] = Field(
        None,
        description="What the tool does, as indexed for search",
    )
    score: float = Field(
        0.0,
        description="Relevance score; higher is better, comparable only within one response",
    )
    connections: List[ConnectionReadiness] = Field(
        default_factory=list,
        description="Per-connection readiness for the searched identifier",
    )

    @classmethod
    def from_proto(cls, proto_tool: SearchedToolProto) -> "SearchedTool":
        """Build the model from the ``SearchedTool`` proto message.

        Args:
            proto_tool: One entry of ``SearchToolsResponse.tools``.

        Returns:
            The mapped result. ``connections`` is always a list, never ``None``,
            and ``score`` is always a float.

        Example:
            tool = SearchedTool.from_proto(response.tools[0])

        """
        return cls(
            name=proto_tool.name or None,
            provider=proto_tool.provider or None,
            description=proto_tool.description or None,
            score=proto_tool.score,
            connections=[
                ConnectionReadiness.from_proto(proto_connection)
                for proto_connection in proto_tool.connections
            ],
        )

    def to_dict(self) -> dict:
        """Serialise the result to a dictionary.

        Returns:
            A dictionary with the model's field names, with every nested
            readiness converted by ``ConnectionReadiness.to_dict``.

        """
        return {
            "name": self.name,
            "provider": self.provider,
            "description": self.description,
            "score": self.score,
            "connections": [connection.to_dict() for connection in self.connections],
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True


class SearchToolsResponse(BaseModel):
    """Tools ranked by relevance to a natural-language query.

    Returned by ``client.actions.search_tools``. The server caps the result set
    with ``top_k`` (default 10, maximum 50), so this response is not paginated and
    carries no page tokens.

    Attributes:
        tools: The ranked results, best first. Empty when nothing matched.

    Example:
        result = client.actions.search_tools("send a message to a slack channel", top_k=5)
        for tool in result.tools:
            print(tool.name, tool.score)

    """

    tools: List[SearchedTool] = Field(
        default_factory=list,
        description="Ranked search results, best first",
    )

    @classmethod
    def from_proto(cls, proto_response: SearchToolsResponseProto) -> "SearchToolsResponse":
        """Build the model from the ``SearchToolsResponse`` proto message.

        Args:
            proto_response: The proto message returned by
                ``ToolsClient.search_tools``.

        Returns:
            The mapped results, in the order the server ranked them.

        Example:
            response, _ = client.tools.search_tools(query="send an email")
            result = SearchToolsResponse.from_proto(response)

        """
        return cls(
            tools=[SearchedTool.from_proto(proto_tool) for proto_tool in proto_response.tools],
        )

    def to_dict(self) -> dict:
        """Serialise the results to a dictionary.

        Returns:
            A dictionary with a single ``tools`` key, each entry converted by
            ``SearchedTool.to_dict``.

        """
        return {
            "tools": [tool.to_dict() for tool in self.tools],
        }

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        populate_by_name = True

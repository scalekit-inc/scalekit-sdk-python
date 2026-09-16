"""User-scoped convenience wrappers over the AgentKit clients.

Nothing here is new capability. Every method composes calls that already exist on
``actions`` and ``tools``. The point is the shape: building an agent means
repeating one ``identifier`` across three different clients, checking a status
enum by hand, filtering search results by readiness, and unwrapping a tool
payload -- and the SDK offers five top-level clients with eight duplicated
methods between them, so there is no obvious place to start.

``scalekit_client.for_identifier(identifier)`` binds the identifier once and exposes
the three things an agent actually does::

    user = scalekit_client.for_identifier("usr_8f3a2c")

    state = user.ensure_connected("github-connect")
    if not state.is_active:
        send_to_user(state.authorization_link)

    tools = user.find_tools("star a repository")
    repos = user.run(tools[0].name, {"owner": "scalekit-inc", "repo": "scalekit"})

Reach past it to ``actions``/``tools`` whenever you need something this does not
cover; the two styles mix freely.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Readiness constants from the tools proto. Named here so callers never compare
# against a bare integer.
_READY = 1


@dataclass(frozen=True)
class ConnectionState:
    """Where one user stands with one connection."""

    connection_name: str
    status: str
    connected_account_id: Optional[str] = None
    authorization_link: Optional[str] = None

    @property
    def is_active(self) -> bool:
        """True when tools can be called right now."""
        return self.status == "ACTIVE"


@dataclass(frozen=True)
class ReadyTool:
    """A tool this user can call right now, with the account to call it on."""

    name: str
    connected_account_id: str
    connection_name: str
    provider: str = ""
    score: float = 0.0
    description: str = ""


@dataclass
class UserScope:
    """AgentKit bound to one end user. Created by ``ScalekitClient.for_identifier``."""

    identifier: str
    _actions: Any = field(repr=False)
    _tools: Any = field(repr=False)

    def ensure_connected(self, connection_name: str) -> ConnectionState:
        """Return this user's state for a connection, with a link if action is needed.

        Composes ``actions.get_or_create_connected_account`` and, when the account
        is not yet active, ``actions.get_authorization_link``. Nothing is executed
        and no tool is called.

        :param connection_name: Connection name exactly as it appears in the
            dashboard under **AgentKit > Connections**. It is case-sensitive.
        :returns: A :class:`ConnectionState`. Check ``.is_active``; when false,
            send ``.authorization_link`` to the user and call again afterwards.
        """
        response = self._actions.get_or_create_connected_account(
            connection_name=connection_name,
            identifier=self.identifier,
        )
        account = response.connected_account
        status = getattr(account, "status", None) or "UNKNOWN"
        account_id = getattr(account, "id", None)

        if status == "ACTIVE":
            return ConnectionState(connection_name, status, account_id, None)

        link_response = self._actions.get_authorization_link(
            connection_name=connection_name,
            identifier=self.identifier,
        )
        return ConnectionState(
            connection_name, status, account_id, getattr(link_response, "link", None)
        )

    def find_tools(self, goal: str, limit: int = 5) -> List[ReadyTool]:
        """Find tools that fit a goal and that this user can actually call.

        Composes ``tools.search_tools`` and keeps only results with a connection
        in the READY state, pairing each with the account id to execute against.
        Results that need connecting or re-authorizing are dropped -- use
        :meth:`ensure_connected` to resolve those first.

        Prefer this over listing a whole connector: binding 217 tools to a model
        is roughly 85k tokens of schema per request and measurably worsens tool
        selection.

        :param goal: The job to be done, in plain language.
        :param limit: Maximum ranked results to consider.
        :returns: Ready tools, best match first. May be empty.
        """
        response = self._tools.search_tools(
            query=goal, identifier=self.identifier, top_k=limit
        )
        ready: List[ReadyTool] = []
        for tool in response.tools:
            for connection in tool.connections:
                if connection.readiness_state == _READY:
                    ready.append(
                        ReadyTool(
                            name=tool.name,
                            connected_account_id=connection.connected_account_id,
                            connection_name=connection.connection_name,
                            provider=getattr(tool, "provider", ""),
                            score=getattr(tool, "score", 0.0),
                            description=getattr(tool, "description", ""),
                        )
                    )
                    break
        return ready

    def run(
        self,
        tool_name: str,
        inputs: Optional[Dict[str, Any]] = None,
        connected_account_id: Optional[str] = None,
        connection_name: Optional[str] = None,
    ) -> Any:
        """Execute a tool for this user and return the payload.

        Composes ``actions.execute_tool``. Results cross the wire as a protobuf
        ``Struct``, so a list-returning tool arrives wrapped as
        ``{"array": [...]}``; this unwraps that so you get the list directly.
        Note that every number in the payload is a float as a result of that
        encoding -- cast before formatting.

        Pass ``connected_account_id`` (from :meth:`find_tools`) when you have it.
        Otherwise supply ``connection_name`` and the account is resolved from this
        scope's identifier.

        :returns: The tool's payload -- a list for list-returning tools, a dict
            otherwise. Use ``actions.execute_tool`` directly if you need the
            execution id.
        """
        kwargs: Dict[str, Any] = {
            "tool_name": tool_name,
            "tool_input": inputs or {},
        }
        if connected_account_id:
            kwargs["connected_account_id"] = connected_account_id
        else:
            kwargs["identifier"] = self.identifier
            if connection_name:
                kwargs["connection_name"] = connection_name

        response = self._actions.execute_tool(**kwargs)
        data = response.data
        if isinstance(data, dict) and set(data.keys()) == {"array"}:
            return data["array"]
        return data

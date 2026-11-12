# AgentKit API reference (Python)

This document lists **AgentKit** Scalekit SDK surfaces: tools, connected accounts, the `ActionClient` facade (`connect` / `actions`, including custom connectors and triggers), and the low-level `McpClient` (Python).

For the full SDK surface (organizations, SSO **connections**, users, sessions, etc.), see [`REFERENCE.md`](REFERENCE.md).

**Note:** `client.connection` (enterprise SSO IdP **connections**) is not part of AgentKit; it remains documented only in `REFERENCE.md`.

## Initialize the client

Create a single [`ScalekitClient`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py) with your environment URL, client ID, and client secret from **Scalekit Dashboard → Developers → API credentials**. All sections below use the same instance.

```python
import os
from scalekit import ScalekitClient

scalekit_client = ScalekitClient(
    os.environ["SCALEKIT_ENV_URL"],
    os.environ["SCALEKIT_CLIENT_ID"],
    os.environ["SCALEKIT_CLIENT_SECRET"],
)
```

Install: `pip install scalekit-sdk-python`. Load credentials from the environment (or a secret manager) in production; do not commit secrets.

## AgentKit namespaces

These attributes on `scalekit_client` are the AgentKit-related entry points:

| Namespace | Role |
|-----------|------|
| `tools` | List and execute tools against connected accounts. |
| `connected_accounts` | List, create, update, delete connected accounts; magic links. |
| `connect` and `actions` | Same [`ActionClient`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py) — ergonomic facade over tools + connected accounts + MCP helpers. |
| `mcp` | Low-level MCP server configuration and instances (gRPC protos). |
| `actions.triggers` | Manage AgentKit triggers (catalogue, subscriptions, webhook URL and signing secret, activity, usage, deliveries) and verify delivered trigger events. See [Managing triggers](#managing-triggers). |
| `actions.providers` | Create and manage custom connectors, from an MCP server or from an OpenAPI spec, and follow the runs that generate an OpenAPI connector's tools. See [Custom connectors](#custom-connectors). |

OAuth login (`get_authorization_url`, `authenticate_with_code`, …) and MCP **Bring-your-own-auth** (`client.auth.update_login_user_details`) are documented under **ScalekitClient** / **Auth** in [`REFERENCE.md`](REFERENCE.md), not in this AgentKit guide.

## Tools

Low-level gRPC helpers on `client.tools` ([`scalekit/tools.py`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py)).

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_tools</a>(filter?, page_size?, page_token?) -> ListToolsResponse</code></summary>
<dl>
<dd>

### 📝 Description

Lists tools available in your workspace with optional filtering and pagination.

The tools of a custom connector are listed under the names the server gives them: `a-<connector>_<operation>` for a connector created from an OpenAPI spec, `c-<connector>_<tool>` for a custom MCP connector.

- An OpenAPI-sourced connector has one set of tools for every connected account. List them with `Filter.provider` set to the connector's identifier (at most 50 characters), or with `Filter.connector` set to the name of a connection on it. They are not listed where OpenAPI-sourced connectors are not enabled for the environment.
- A custom MCP connector's tools belong to a connected account, so name that account: `Filter.connector` (the connection name) together with `Filter.identifier`, or `Filter.connected_account_id`.
- `Filter.query` (3 to 100 characters) searches the names of global tools only, so it never returns a custom connector's tools, and a page of search results holds at most 100 tools.

### 🔌 Usage

```python
from scalekit.v1.tools.tools_pb2 import Filter

response = scalekit_client.tools.list_tools(
    filter=Filter(query="calendar"),
    page_size=50,
)

# The tools generated from an OpenAPI-sourced connector
response, _ = scalekit_client.tools.list_tools(filter=Filter(provider=connector.identifier))
print([tool.definition["name"] for tool in response.tools])
```

### ⚙️ Parameters

**filter:** `Optional[Filter]` — Filter on provider, identifier, tool metadata, etc.

**page_size:** `Optional[int]` — Maximum number of tools per page. The server uses 300 when this is omitted or `0`, and lowers a value above 1000 to 1000 instead of rejecting it.

**page_token:** `Optional[str]` — Pagination cursor.

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_scoped_tools</a>(identifier, filter?, page_size?, page_token?) -> ListScopedToolsResponse</code></summary>
<dl>
<dd>

### 📝 Description

Lists tools scoped to a specific connected-account identifier (for example workspace or email).

A connector created from an OpenAPI spec has one set of tools for every connected account, so they are listed with this identifier's connected account on that connector: add the connector's identifier to `ScopedToolFilter.providers`, its connection name to `connection_names`, or tool names to `tool_names`. A custom MCP connector's tools are those of this identifier's connected account.

### 🔌 Usage

```python
from scalekit.v1.tools.tools_pb2 import ScopedToolFilter

response = scalekit_client.tools.list_scoped_tools(
    "user@example.com",
    filter=ScopedToolFilter(),
)
```

### ⚙️ Parameters

**identifier:** `str` — Connected account identifier.

**filter:** `Optional[ScopedToolFilter]` — Optional; the example passes an empty `ScopedToolFilter()` — populate fields as required by your workspace.

**page_size:** `Optional[int]` — Page size.

**page_token:** `Optional[str]` — Pagination cursor.

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">search_tools</a>(query, identifier?, top_k?) -> SearchToolsResponse</code></summary>
<dl>
<dd>

### 📝 Description

Searches tools ranked by relevance to a natural-language query — the job to be done, not an
exact tool name. Pass `identifier` to also get per-connection readiness (usable now,
needs a new connection, or needs re-auth) so you can gate execution on the right auth step.

`needs_connection` means an existing connected account for that provider is inactive; an
empty `connections` list means no account exists for the provider at all (not an error).
Only pass a result's `connected_account_id` to `ExecuteTool` when `readiness_state` is
`TOOL_READINESS_STATE_READY`.

### 🔌 Usage

```python
response, call = scalekit_client.tools.search_tools(
    query="send a message to a slack channel",
    identifier="user@example.com",
    top_k=10,
)

for tool in response.tools:
    print(tool.name, tool.score)
    for connection in tool.connections:
        print(" ", connection.connection_name, connection.readiness_state, connection.connected_account_id)
```

### ⚙️ Parameters

**query:** `str` — Natural-language query or keywords describing the job to be done. 1-256 characters.

**identifier:** `Optional[str]` — Connected-account identifier (e.g. the end user's email or ID).
When set, each result is annotated with readiness for this identifier's connections.

**top_k:** `Optional[int]` — Maximum number of ranked results to return. Defaults to 10, capped at 50.

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_available_tools</a>(identifier, page_size?, page_token?) -> ListAvailableToolsResponse</code></summary>
<dl>
<dd>

### 📝 Description

Lists every tool available to a connected-account identifier: the tools of all the connectors the identifier has a connected account on, including a connector created from an OpenAPI spec (its tools are shared by every account) and a custom MCP connector's tools for that identifier's account. An identifier with no connected account gets an empty list, not an error. Each `Tool.definition` is a `google.protobuf.Struct`, and Python protobuf decodes at most about 100 levels of nested messages, so one tool definition nested about 30 objects deep makes the whole call fail to decode. The same limit already applies to `list_tools`; the server can return definitions as JSON text instead, but this SDK version does not request that yet.

### 🔌 Usage

```python
response, _ = scalekit_client.tools.list_available_tools("user@example.com", page_size=50)

for tool in response.tools:
    print(tool.definition["name"])
```

### ⚙️ Parameters

**identifier:** `str` — Connected account identifier. Required.

**page_size:** `Optional[int]` — Maximum number of tools per page. The server uses 100 when this is omitted or `0`.

**page_token:** `Optional[str]` — Pagination cursor (`next_page_token` of the previous response).

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">refresh_tools</a>(identifier?, connected_account_id?, connection_name?, organization_id?, user_id?) -> RefreshToolsResponse</code></summary>
<dl>
<dd>

### 📝 Description

Resyncs the tools of a custom MCP connected account: the server re-queries the upstream MCP server, adds new and changed tools, removes the ones it no longer offers, and returns the full refreshed list. Use it when the upstream server has added, renamed or removed tools. The server marks this endpoint as a preview API. It works only for a custom MCP connector; a connector created from an OpenAPI spec gets its tools from a tool collection run instead (see [Custom connectors](#custom-connectors)). Each `Tool.definition` is a `google.protobuf.Struct`, and Python protobuf decodes at most about 100 levels of nested messages, so one tool definition nested about 30 objects deep makes the whole call fail to decode. The same limit already applies to `list_tools`; the server can return definitions as JSON text instead, but this SDK version does not request that yet.

Name the connected account with `connected_account_id`, or with `connection_name` together with `identifier` (or with `organization_id`, for an account created without an `identifier`). A call that gives only `connection_name` or only `identifier` names no account and raises `ValueError` before anything is sent. `ScalekitBadRequestException` means the account is not a custom MCP connector, or custom MCP tools are not enabled for the environment; `ScalekitNotFoundException`, that no connected account matches; `ScalekitTooManyRequestsException` (`DISCOVERY_IN_PROGRESS`), that a refresh of the same account is already running, so retry in a few seconds; `ScalekitInternalServerException`, that the upstream server could not be queried.

### 🔌 Usage

```python
response, _ = scalekit_client.tools.refresh_tools(connected_account_id="ca_123")
print(response.total_size, [tool.definition["name"] for tool in response.tools])
```

### ⚙️ Parameters

**connected_account_id:** `Optional[str]` — ID of the connected account to refresh.

**connection_name:** `Optional[str]` — Name of the connection the account belongs to. Pass it with `identifier`, or with `organization_id`.

**identifier:** `Optional[str]` — Identifier of the connected account, used together with `connection_name`.

**organization_id:** `Optional[str]` — Narrows the account lookup when the same identifier exists in more than one organization. With `connection_name` and no `identifier`, it names an account that was created without one.

**user_id:** `Optional[str]` — Narrows the account lookup when the same identifier exists for more than one user.

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">execute_tool</a>(tool_name, identifier, params?, connected_account_id?, connection_name?) -> ExecuteToolResponse</code></summary>
<dl>
<dd>

### 📝 Description

Executes a named tool using credentials from a connected account.

A custom connector's tools run like any other: use a connected account of a connection on the tool's own connector. A name that does not exist for that connector fails with 400 `custom tool not found: <name>`; that includes an OpenAPI-sourced tool where OpenAPI-sourced connectors are not enabled for the environment.

### 🔌 Usage

```python
response = scalekit_client.tools.execute_tool(
    tool_name="gmail.messages.list",
    identifier="user@example.com",
    params={"maxResults": 10},
)
```

### ⚙️ Parameters

**tool_name:** `str` — Tool identifier.

**identifier:** `str` — Connected account identifier.

**params:** `Optional[dict]` — JSON-serializable tool arguments.

**connected_account_id:** `Optional[str]` — Use a specific connected account by id.

**connection_name:** `Optional[str]` — The connection's own name (for example `slack-b1fqL2Dr`, not the provider name). Pass it with `identifier` to pick the connected account, or pass `connected_account_id` instead.

</dd>
</dl>
</details>

## Connected Accounts

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">list_connected_accounts</a>(organization_id?, user_id?, connector?, identifier?, provider?, page_size?, page_token?, connection_names?) -> ListConnectedAccountsResponse</code></summary>
<dl>
<dd>

### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all connected accounts with optional filtering.
</dd>
</dl>
</dd>
</dl>

### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
response = scalekit_client.connected_accounts.list_connected_accounts(
    organization_id='org_123456',
    user_id='usr_123456',
    page_size=50
)

for account in response[0].connected_accounts:
    print(f'Account: {account.id}')
```
</dd>
</dl>
</dd>
</dl>

### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `Optional[str]` - Organization ID

</dd>
</dl>

<dl>
<dd>

**user_id:** `Optional[str]` - User ID

</dd>
</dl>

<dl>
<dd>

**connector:** `Optional[str]` - Connector identifier

</dd>
</dl>

<dl>
<dd>

**identifier:** `Optional[str]` - Identifier for the connector

</dd>
</dl>

<dl>
<dd>

**provider:** `Optional[str]` - Provider name

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Number of results per page

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Page token for pagination

</dd>
</dl>

<dl>
<dd>

**connection_names:** `Optional[List[str]]` - Return only accounts that belong to these connections, by connection name (for example `["github", "slack"]`, up to 20). It cannot be combined with `connector`; the API rejects a request that sets both.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">get_connected_account_by_identifier</a>(connector, identifier, organization_id?, user_id?, connected_account_id?) -> GetConnectedAccountByIdentifierResponse</code></summary>
<dl>
<dd>

### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a connected account by identifier.
</dd>
</dl>
</dd>
</dl>

### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
response = scalekit_client.connected_accounts.get_connected_account_by_identifier(
    'slack',
    'workspace_id',
    organization_id='org_123456',
    user_id='usr_123456'
)
```
</dd>
</dl>
</dd>
</dl>

### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connector:** `str` - Connector identifier

</dd>
</dl>

<dl>
<dd>

**identifier:** `str` - Identifier for the connector

</dd>
</dl>

<dl>
<dd>

**organization_id:** `Optional[str]` - Organization ID

</dd>
</dl>

<dl>
<dd>

**user_id:** `Optional[str]` - User ID

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - ID of the connected account

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">create_connected_account</a>(connector, identifier, connected_account, organization_id?, user_id?) -> CreateConnectedAccountResponse</code></summary>
<dl>
<dd>

### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new connected account.
</dd>
</dl>
</dd>
</dl>

### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.v1.connected_accounts.connected_accounts_pb2 import CreateConnectedAccount

account = CreateConnectedAccount()

response = scalekit_client.connected_accounts.create_connected_account(
    'slack',
    'workspace_id',
    account,
    organization_id='org_123456',
    user_id='usr_123456'
)
```
</dd>
</dl>
</dd>
</dl>

### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connector:** `str` - Connector identifier

</dd>
</dl>

<dl>
<dd>

**identifier:** `str` - Identifier for the connector

</dd>
</dl>

<dl>
<dd>

**connected_account:** `CreateConnectedAccount` - Connected account details

</dd>
</dl>

<dl>
<dd>

**organization_id:** `Optional[str]` - Organization ID

</dd>
</dl>

<dl>
<dd>

**user_id:** `Optional[str]` - User ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">update_connected_account</a>(connector, identifier, connected_account, organization_id?, user_id?, connected_account_id?) -> UpdateConnectedAccountResponse</code></summary>
<dl>
<dd>

### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing connected account.
</dd>
</dl>
</dd>
</dl>

### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.v1.connected_accounts.connected_accounts_pb2 import UpdateConnectedAccount

account = UpdateConnectedAccount()

response = scalekit_client.connected_accounts.update_connected_account(
    'slack',
    'workspace_id',
    account,
    organization_id='org_123456',
    user_id='usr_123456'
)
```
</dd>
</dl>
</dd>
</dl>

### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connector:** `str` - Connector identifier

</dd>
</dl>

<dl>
<dd>

**identifier:** `str` - Identifier for the connector

</dd>
</dl>

<dl>
<dd>

**connected_account:** `UpdateConnectedAccount` - Updated connected account details

</dd>
</dl>

<dl>
<dd>

**organization_id:** `Optional[str]` - Organization ID

</dd>
</dl>

<dl>
<dd>

**user_id:** `Optional[str]` - User ID

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - ID of the connected account to update

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">delete_connected_account</a>(connector, identifier, organization_id?, user_id?, connected_account_id?) -> DeleteConnectedAccountResponse</code></summary>
<dl>
<dd>

### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a connected account.
</dd>
</dl>
</dd>
</dl>

### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
scalekit_client.connected_accounts.delete_connected_account(
    'slack',
    'workspace_id',
    organization_id='org_123456',
    user_id='usr_123456'
)
```
</dd>
</dl>
</dd>
</dl>

### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connector:** `str` - Connector identifier

</dd>
</dl>

<dl>
<dd>

**identifier:** `str` - Identifier for the connector

</dd>
</dl>

<dl>
<dd>

**organization_id:** `Optional[str]` - Organization ID

</dd>
</dl>

<dl>
<dd>

**user_id:** `Optional[str]` - User ID

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - ID of the connected account to delete

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">get_magic_link_for_connected_account</a>(connector, identifier, organization_id?, user_id?, connected_account_id?, state?, user_verify_url?) -> GetMagicLinkForConnectedAccountResponse</code></summary>
<dl>
<dd>

### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a magic link for a connected account.
</dd>
</dl>
</dd>
</dl>

### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
response = scalekit_client.connected_accounts.get_magic_link_for_connected_account(
    'slack',
    'workspace_id',
    organization_id='org_123456',
    user_id='usr_123456'
)

print(f'Magic Link: {response[0].link}')
```
</dd>
</dl>
</dd>
</dl>

### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connector:** `str` - Connector identifier

</dd>
</dl>

<dl>
<dd>

**identifier:** `str` - Identifier for the connector

</dd>
</dl>

<dl>
<dd>

**organization_id:** `Optional[str]` - Organization ID

</dd>
</dl>

<dl>
<dd>

**user_id:** `Optional[str]` - User ID

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - ID of the connected account

</dd>
</dl>

<dl>
<dd>

**state:** `Optional[str]` - Opaque value (up to 512 characters). It is added to the query parameters of the user verify redirect URL, so your app can validate the user verification.

</dd>
</dl>

<dl>
<dd>

**user_verify_url:** `Optional[str]` - Your app's user verify redirect URL (must start with `http://` or `https://`, up to 2048 characters). Use it for the user verification redirect flow; see `verify_connected_account_user`.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Connect and Actions (`ActionClient`)

`ScalekitClient.connect` and `ScalekitClient.actions` are the same [`ActionClient`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py) instance — a facade over `tools`, `connected_accounts`, and `mcp` with typed helpers, modifiers, and optional framework integrations.

### Properties

- **`langchain`** — Lazy `LangChain` helper (requires `langchain` installed).
- **`google`** — Lazy Google ADK helper (requires `google-adk` installed).
- **`mcp`** — [`ActionMcp`](#actionmcp-helper) for MCP operations that return parsed response wrappers.
- **`triggers`** — [`ActionTriggers`](#trigger-events) to verify and parse trigger events delivered to your endpoint, and to [manage triggers](#managing-triggers) (subscriptions, webhook URL, signing secret, deliveries).

### Tool execution

<details><summary><code>client.connect.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">execute_tool</a>(tool_input, tool_name, identifier?, tool_request?, connected_account_id?, **kwargs) -> ExecuteToolResponse</code></summary>
<dl><dd>

Runs pre/post modifiers then delegates to `client.tools.execute_tool`. `tool_name` is required.

</dd></dl>
</details>

### OAuth and connected accounts

<details><summary><code>get_authorization_link</code> / <code>verify_connected_account_user</code> / <code>list_connected_accounts</code> / <code>delete_connected_account</code> / <code>get_connected_account</code></summary>
<dl><dd>

High-level wrappers around `connected_accounts` with friendlier parameter names (`connection_name` vs `connector`) and typed response objects. See source for full signatures.

</dd></dl>
</details>

<details><summary><code>create_connected_account</code> / <code>get_or_create_connected_account</code> / <code>update_connected_account</code></summary>
<dl><dd>

Create, upsert, or update accounts using dict-based auth payloads converted to protobuf.

</dd></dl>
</details>

### HTTP proxy

<details><summary><code>client.connect.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">request</a>(connection_name, identifier, path, method?, ...)</code></summary>
<dl><dd>

Proxied REST call via `{env_url}/proxy` with `connection_name` and `identifier` headers. Returns a `requests.Response`.

The request times out after **30 seconds** by default, for connecting and for waiting for a response separately. For a provider call that can take longer, pass a larger value as a keyword argument, for example `request(..., timeout=90)`; a request that exceeds the timeout raises `requests.exceptions.Timeout`. Other keyword arguments are passed to the underlying `requests` call.

A `path` that resolves outside the proxy prefix (for example through `..` segments, including percent-encoded or backslash forms) raises `ValueError` before any request is sent. With an `http://` environment URL, this also covers the URL a forward proxy would receive, even when none is configured. Redirects are followed as before, but a redirect to a location outside the proxy prefix is sent without the client's bearer token and without the `connection_name` and `identifier` headers.

</dd></dl>
</details>

<details><summary><code>client.actions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">upload_resumable</a>(connection_name, identifier, path, *, data, total_bytes?, content_type?, metadata?, method?, query_params?, chunk_size?, max_retries?, timeout?, on_progress?) -> dict</code></summary>
<dl>
<dd>

### 📝 Description

Uploads content of any size to Google Drive, Cloud Storage or YouTube through the Scalekit proxy, using Google's resumable upload protocol. The content is sent in chunks (4 MiB by default) and read about one chunk at a time; resending the rest of a chunk briefly copies it. A chunk that fails with a timeout, a connection error or HTTP 408, 429, 500, 502, 503 or 504 is resumed from what the server stored instead of restarting (exponential backoff with jitter, or `Retry-After` on 429 and 503, capped at 30 seconds). The request that starts the session is never retried, because a retry would open a second session; the only exception is a single resend after the SDK refreshes an expired Scalekit access token (a 401 from Scalekit itself, not from Google). Returns the created or updated resource as a dict, for example the Drive file (`{}` when the final response is empty).

Errors (all in `scalekit.common.exceptions`):

- `ScalekitUploadSessionExpiredException` (subclass of `ScalekitUploadException`): the session expired or was cancelled (HTTP 404 or 410 after it started). Start a new upload; the SDK never restarts one on its own.
- `ScalekitUploadException`: the session-start request failed, a chunk failed with a non-retryable status (such as 403), or a retryable failure persisted after `max_retries` retries. `status_code` is `None` when no response arrived.
- `ScalekitUploadProtocolException`: the server's answer does not follow the protocol (for example, no `upload_id` in the session-start response, or every byte confirmed without the upload completing).

These three upload exceptions carry `status_code`, `headers`, `body`, `upload_id` and `bytes_committed`.

If the Scalekit access token cannot be refreshed after a 401 from Scalekit, the client's own authentication error (for example `ScalekitUnauthorizedException`) is raised unchanged, as with `request`; it is not a `ScalekitUploadException`.

Invalid arguments raise `ValueError` or `TypeError` before any network call. A path that cannot be opened raises `OSError` (for example `FileNotFoundError`), and errors from reading your stream propagate unchanged. The call blocks; in async code use `await asyncio.to_thread(...)`.

### 🔌 Usage

```python
from pathlib import Path
from scalekit.actions.types import UploadProgress
from scalekit.common.exceptions import ScalekitUploadSessionExpiredException

def show(p: UploadProgress) -> None:
    print(p.bytes_committed, "of", p.total_bytes)

try:
    file = scalekit_client.actions.upload_resumable(
        "googledrive",
        "user_123",
        "/upload/drive/v3/files",
        data=Path("video.mp4"),
        content_type="video/mp4",
        metadata={"name": "video.mp4", "parents": ["<folderId>"]},
        on_progress=show,
    )
    print(file["id"])
except ScalekitUploadSessionExpiredException:
    ...  # start a new upload
```

### ⚙️ Parameters

**connection_name:** `str` — Connection name, for example `"googledrive"`.

**identifier:** `str` — Identifier of the connected account.

**path:** `str` — Provider upload path: `/upload/drive/v3/files` (Drive), `/upload/drive/v3/files/<fileId>` with `method="PATCH"` to replace a file's content, `/upload/storage/v1/b/<bucket>/o` (Cloud Storage) or `/upload/youtube/v3/videos` (YouTube). A leading `/` is added when missing. Must not contain `?`, `#`, spaces, control characters, or `.`/`..` segments.

**data:** `bytes | bytearray | memoryview | IO[bytes] | os.PathLike[str]` — The content. A binary stream is read from its current position. A path (for example `pathlib.Path`) is opened and closed by the SDK. Errors raised while reading your stream propagate unchanged.

**total_bytes:** `Optional[int]` — Total size in bytes. Known automatically for bytes, a path to a regular file and a seekable stream. For other streams, pass it if you know it; otherwise the size is discovered at the end of the stream. A stream shorter or longer than `total_bytes` raises `ValueError` before its last chunk is sent.

**content_type:** `str` — MIME type of the content (default `application/octet-stream`).

**metadata:** `Optional[Mapping[str, object]]` — JSON object sent when the session starts, for example `{"name": "report.pdf", "parents": ["<folderId>"]}`. Without it the start request has no body.

**method:** `Literal["POST", "PATCH", "PUT"]` — Method of the session-start request (default `POST`). Case-insensitive.

**query_params:** `Optional[Mapping[str, str | int | bool]]` — Extra query parameters for the session-start request only, for example `{"supportsAllDrives": True}` or `{"part": "snippet,status"}`. Booleans are sent as `true`/`false`. The key `uploadType` (exact, case-sensitive) is rejected, because the SDK always sends `uploadType=resumable`.

**chunk_size:** `int` — Bytes per chunk, a positive multiple of 262144 (256 KiB). Default 4 MiB.

**max_retries:** `int` — Retries in a row allowed for one chunk, counting chunk resends, status queries and answers that store no new data (default 3). The count resets only when the server confirms data beyond the highest offset so far. `0` disables retries.

**timeout:** `Optional[float]` — Timeout in seconds for each HTTP request. Defaults to the client's tool-call timeout (60 seconds).

**on_progress:** `Optional[Callable[[UploadProgress], None]]` — Called with `UploadProgress(bytes_committed, total_bytes)` each time the server confirms more data, and once on completion. `total_bytes` is `None` while the size is unknown. A zero-length upload reports `UploadProgress(0, 0)` once. An exception raised by the callback aborts the upload.

</dd>
</dl>
</details>

### Modifiers

<details><summary><code>add_modifier</code>, <code>get_modifiers</code>, <code>pre_modifier</code>, <code>post_modifier</code></summary>
<dl><dd>

Register optional pre/post hooks around tool execution (`Modifier` types).

</dd></dl>
</details>

### MCP passthrough on `ActionClient`

The `ActionClient` also exposes `list_configs`, `create_config`, `update_config`, `delete_config`, `ensure_instance`, `update_instance`, `get_instance`, `list_instances`, `delete_instance`, and `get_instance_auth_state` that forward to `client.mcp` with convenience arguments. Prefer `client.mcp` for raw protos or `client.connect.mcp` for wrapped responses.

### `ActionMcp` helper

`create_config` and `update_config` take an optional `tool_exposure` (`"DIRECT"` or `"META"`). `DIRECT` (the default when unset) lists every mapped tool and allows at most 25 connections. `META` gives agents five tools (`search_available_tools`, `list_available_tools`, `get_tool_details`, `execute_tool`, `connect_account`) with no connection limit; it must be enabled for your environment, otherwise the call fails with `FEATURE_NOT_ENABLED`. An update that omits `tool_exposure` never changes the stored mode, and switching to `DIRECT` fails above 25 connections or with overlapping tool names. `McpConfig.tool_exposure` reports the mode.

**Custom connectors in a configuration.** A configuration's `connection_tool_mappings` can include a connection on a custom connector, in either mode, and the tools are served under the connector's own names (`a-...` for an OpenAPI-sourced connector, `c-...` for a custom MCP connector).

```python
from scalekit.actions.types import McpConfigConnectionToolMapping

config = scalekit_client.actions.mcp.create_config(
    name="my-config",
    description="Acme API tools",
    connection_tool_mappings=[
        # tools=[] exposes every tool the connection has
        McpConfigConnectionToolMapping(connection_name="acme-api", tools=["a-acmeapi_listpets"]),
    ],
    tool_exposure="META",
)
```

- A connection on an OpenAPI-sourced connector is accepted where OpenAPI-sourced connectors are enabled for the environment. A connection on a custom MCP connector is accepted where Scalekit has enabled that for the environment. A connector that is neither (a plain REST connector) is always refused. A refusal raises `ScalekitBadRequestException`: `custom connectors are not supported yet. please contact support@scalekit.com`.
- Leave `tools` empty to expose all of the connection's tools: the server resolves them to the full list of the connection's tools when it saves the configuration.
- A tool name the connector does not have is refused (`invalid tool '<tool>' for connection '<connection>'`), and so is a custom MCP connection that has no connected account with discovered tools yet (`authorize a connected account to view the tools for connection '<connection>'`).
- A configuration that already has such a connection stops serving its tools where the capability is turned off for the environment.

Access via `client.connect.mcp` / `client.actions.mcp`. Requires `McpClient` to be initialized on the parent `ScalekitClient`. Methods include `list_configs`, `create_config` (builds `McpConfig` from `name` / `description` / mappings), `update_config`, `delete_config`, `ensure_instance`, `update_instance`, `get_instance`, `list_instances`, `delete_instance`, `get_instance_auth_state`, and `create_session_token`, returning parsed wrapper types instead of raw gRPC tuples.

### AgentKit connections

New methods on `client.actions` that manage AgentKit connections. Types and errors live in `scalekit.actions.connections`. They are additive: every existing method is unchanged.

```python
from scalekit.actions.connections import AuthMode, OAuthSettings, ProviderConfigurations

conn = client.actions.create_connection("gmail", connection_name="gmail-work", auth_mode=AuthMode.USER)

# Only what you pass changes. Pass the name (one extra read) or connection_id="conn_...".
client.actions.update_connection(
    "gmail-work",
    oauth=OAuthSettings(client_id="...", client_secret="...", scopes=["https://www.googleapis.com/auth/gmail.readonly"]),
)
client.actions.update_connection("gmail-work", oauth=OAuthSettings(extra_authorize_params={}))  # {} / [] clears

conn = client.actions.get_connection("gmail-work")          # by name or id
page = client.actions.list_app_connections(provider="gmail", page_size=20)
client.actions.delete_connection("gmail-work")              # raises ConnectionInUseError while accounts or MCP configs use it
```

| Method | Notes |
|---|---|
| `create_connection(provider, connection_name=None, auth_mode=None, provider_domain=None)` | The type comes from the connector (a connector with several auth types is refused). `provider_domain` is only for regional connectors such as `MIXPANELMCP` and is never returned. Never retried after a timeout. |
| `get_connection(connection_name=None, *, connection_id=None)` | Name is case-insensitive. Secrets come back masked (`****1234`). |
| `list_app_connections(provider=None, query=None, page_size=None, page_token=None)` | Summaries only (no settings), newest first, from the AgentKit-only API; not the same as `client.connection.list_app_connections`, which is unchanged. `page_size` defaults to 10, max 100. `query` needs 3+ characters. |
| `update_connection(connection_name=None, *, connection_id=None, new_connection_name=None, oauth=None, google_dwd=None, provider_configurations=None)` | Partial merge. `None` keeps a value; `[]` or `{}` clears a list or map. Pass at most one of `oauth` or `google_dwd`; a rename or a `provider_configurations` change needs neither. `provider_configurations` goes with `oauth` or on its own, never with `google_dwd`. Sending your own `client_id` or `client_secret` turns `use_scalekit_creds` off unless you set it. |
| `delete_connection(connection_name=None, *, connection_id=None)` | Uses the existing connection RPC; never retried after a timeout. Raises `ConnectionInUseError` while connected accounts or MCP configs use the connection. |

`OAuthSettings.token_endpoint_auth_method` chooses how Scalekit sends client credentials to the provider's token endpoint: `TokenEndpointAuthMethod.BASIC_AUTH` (`client_id` and `client_secret` in a Basic `Authorization` header, `client_secret_basic`), `REQUEST_BODY` (as POST body parameters, `client_secret_post`), `NONE` (only the `client_id`, for public PKCE clients) or `DEFAULT` (clears the stored value; the platform makes a best-effort match on the method per request). Set it only when the provider's token endpoint documentation requires a specific method: a wrong value makes token exchange or refresh fail, and every connected account on the connection then has to authenticate again. It applies to the authorization_code exchange, MCP token refresh and `OAUTH_M2M` client_credentials; refreshing a token on a non-MCP OAuth connection always detects the method itself. A connection that never set a method reads as `DEFAULT`.

```python
from scalekit.actions.connections import OAuthSettings, TokenEndpointAuthMethod

client.actions.update_connection(
    "my-connection",
    oauth=OAuthSettings(token_endpoint_auth_method=TokenEndpointAuthMethod.REQUEST_BODY),
)
```

Errors derive from `AgentKitConnectionError` and carry `code`, `step`, `retryable` and the original server error in `cause`. `OutcomeUnknownError` means a write timed out and may have been applied; read the connection (or `list_app_connections` after a create) before repeating it.

### Custom connectors

`client.actions.providers` creates and manages connectors of your own. A connector gets its tools from one source, and you set exactly one when you create it: an **MCP server** (`proxy_url`; its tools belong to each connected account) or an **OpenAPI spec** (`openapi_spec_url`; its tools are generated from the spec and shared by every connected account). Per-method details: [REFERENCE.md → Custom Providers](REFERENCE.md#custom-providers).

**Create a connector from an OpenAPI spec**

1. `actions.providers.create_custom_provider(...)` with `openapi_spec_url` (HTTPS) and `auth_patterns` (required). The server fetches and validates the spec before it stores anything, answers, and queues the first tool collection run in the background. The tools do not exist until that run completes.
2. `actions.providers.get_tool_collection_run(...)` reads the latest run. Poll until `run.is_terminal`: the run is then `COMPLETED` or `FAILED`.
3. List and run the tools (below). Create a connection on the connector and a connected account for each user as for any other connector.

```python
import time
from scalekit.actions.types import (
    AuthField, AuthPattern, CreateCustomProviderRequest, GetToolCollectionRunRequest, ToolCollectionRunStatus,
    TriggerToolCollectionRequest,
)
from scalekit.common.exceptions import ScalekitConflictException, ScalekitNotFoundException

providers = scalekit_client.actions.providers

connector = providers.create_custom_provider(
    CreateCustomProviderRequest(
        display_name="Acme API",
        openapi_spec_url="https://api.acme.com/openapi.json",
        auth_patterns=[
            AuthPattern(
                type="API_KEY",
                display_name="API key",
                fields=[AuthField(field_name="api_key", label="API key", input_type="password", required=True)],
            )
        ],
    )
).provider

identifier = connector.identifier
started = time.monotonic()
deadline = started + 600
triggered = False
while True:
    try:
        run = providers.get_tool_collection_run(GetToolCollectionRunRequest(provider_identifier=identifier))
    except ScalekitNotFoundException:
        run = None  # the first run is queued in the background and may not exist yet
        if not triggered and time.monotonic() - started > 45:
            # The server gave up queueing it and does not say so: queue a run yourself, once.
            triggered = True
            try:
                providers.trigger_tool_collection(TriggerToolCollectionRequest(provider_identifier=identifier))
            except ScalekitConflictException:
                pass  # a run was queued in the meantime
    if run is not None and run.is_terminal:
        break
    if time.monotonic() > deadline:
        raise TimeoutError("the tool collection run did not finish")
    time.sleep(2)

if run.status == ToolCollectionRunStatus.FAILED:
    raise RuntimeError(run.error_message)
print(f"{run.tools_created} tools created, {len(run.skipped_tools)} operations skipped")
for skipped in run.skipped_tools:
    print(skipped.method, skipped.path, "-", skipped.reason)
```

The server does not report a failure to queue the first run, and gives up queueing it after 30 seconds, so the loop calls `trigger_tool_collection` once when `get_tool_collection_run` still answers 404 after 45 seconds. If the connector does not exist, that call raises `ScalekitNotFoundException` and ends the loop.

**What a run does**

A run fetches the spec, converts every operation it can into a tool, and records what it did in a `ToolCollectionRun`. One is queued when the connector is created, when its base URL or spec URL changes, and when you call `trigger_tool_collection`. A connector has at most one run queued or running; a call that would queue another raises `ScalekitConflictException`.

- **Names.** `a-<connector>_<operation>`, for example `a-acmeapi_listpets`. `<connector>` is the connector's identifier before the colon, lowercased. `<operation>` is the operation's `operationId`, or `<method>_<path>` when the spec gives none, lowercased, with every run of characters other than letters, digits and `_` replaced by one `_`, leading and trailing `_` removed, and an `f_` prefix when it starts with a digit. A name that is already taken gets `_2`, `_3` and so on.
- **Operations.** Only `GET`, `POST`, `PUT`, `PATCH` and `DELETE` operations become tools. One that cannot be converted is skipped and listed in `run.skipped_tools` with its reason, and the run still completes; a run that converts none fails and lists them. Reasons include a multipart, binary or XML request body, a path parameter the operation does not declare, no resolvable base URL, an operation that needs authentication the connector has no auth pattern for, and an HTTP method that is not converted. A `reason` is text for people, not a code to match on.
- **Counts.** `total_endpoints` is `tools_created + tools_updated` plus the skipped operations, and is `0` until the run completes. A tool whose operation is no longer in the spec is deleted (`tools_deleted`). A run that finds the spec, base URL and auth patterns unchanged since the last completed run creates, updates and deletes nothing and repeats that run's `total_endpoints` and `skipped_tools`; the server does not take that shortcut for a spec that references external files.
- **What the run fills in.** The connector's base URL (`proxy_url`) from the spec's server URL, only when that URL starts with `https://` and no base URL is set. For an `OAUTH` pattern, `authorize_uri`, `token_uri` and the scopes the spec's OAuth 2 security scheme declares, each only while it is still empty. This changes the stored `auth_patterns`, so read them again before an update.

| Limit | Value |
|-------|-------|
| One fetched file (the spec, and each file it references) | 5 MB by default; the error names your environment's limit |
| All fetched files together | 50 MB |
| Distinct external files a spec may reference | 500 |
| Fetching the spec URL | 20 seconds, up to 5 redirects |
| Validating the spec when you create the connector, change its spec URL or call `trigger_tool_collection` | 2 minutes, including every file the spec references |
| One run | 3 minutes. A run that makes no progress for 30 minutes is marked `FAILED`. |

The client does not wait those 2 minutes: it sends `create_custom_provider` and `update_custom_provider` with `openapi_spec_url`, and `trigger_tool_collection`, with its tool-call timeout of 60 seconds by default and does not retry a `DEADLINE_EXCEEDED`, so a spec that takes longer to validate fails on the client first with `ScalekitGatewayTimeoutException` (the server may still finish the create). Raise the timeout with `ScalekitClient(env_url, client_id, client_secret, tool_call_timeout_s=150)`; it also applies to every `client.tools` call.

A spec URL that fails validation raises `ScalekitBadRequestException` (`INVALID_ARGUMENT`, a message starting `openapi_spec_url failed validation:`) and nothing is stored. The reasons are: not a valid URL, the URL must use https, the URL points to a host that cannot be reached for security reasons, the URL could not be reached, the response could not be read, the response is not a valid OpenAPI/Swagger document, and the size limits above. `ScalekitInternalServerException` (`validating the spec url was interrupted — please retry`) means try again.

**Credentials**

A static credential (`API_KEY`, `BEARER`, `BASIC`) is sent in an HTTP header unless its `AuthField` sets a `placement`: `CredentialPlacement(in_="query", name="api_key")` sends it as a query parameter, `"body"` as a top-level JSON body field, and `"path"` fills a `{{name}}` placeholder in the path of the connector's `proxy_url`. An `API_KEY` connector that sends several headers gives each field a `header_name` (at most 10). Rules, limits and errors: [REFERENCE.md → create_custom_provider](REFERENCE.md#custom-providers).

**Change a connector**

An OpenAPI-sourced connector can only change its name, description, icon, metadata and base URL (`proxy_url`). `update_custom_provider` needs `display_name` and `auth_patterns` every time, clears `metadata` and turns `proxy_enabled` off when you leave them out, and treats `auth_patterns` and `proxy_enabled` as changed when they differ from the stored values. So read the connector first and send those back as read. The server compares the patterns key for key after parsing them, where `"hint": ""` and a missing hint, or `"fields": []` and `"fields": null`, differ; an `AuthPattern` the SDK decoded is sent back exactly as the server returned it as long as you do not change it or its fields, so pass `current.auth_patterns` through untouched rather than rebuilding them. That form survives `copy`, `deepcopy` and `pickle`, but not `model_dump()` or JSON, nor `to_dict()` (which always returns the normalised view) followed by `from_dict()` or a constructor, which rebuild the pattern in the normalised form, so for an OpenAPI-sourced connector always pass the patterns that `list_providers` returned through as they are:

```python
from scalekit.actions.types import ListProvidersRequest, UpdateCustomProviderRequest
from scalekit.v1.providers.providers_pb2 import ProviderType

stored = providers.list_providers(
    ListProvidersRequest(provider_type=ProviderType.CUSTOM, identifier=connector.identifier)
).providers
if not stored:  # an identifier that matches nothing comes back as an empty list, not as an error
    raise LookupError(f"No connector with identifier {connector.identifier!r}")
current = stored[0]

providers.update_custom_provider(
    UpdateCustomProviderRequest(
        identifier=current.identifier,
        display_name=current.display_name,
        auth_patterns=current.auth_patterns,  # as read: sent back exactly as the server returned them
        proxy_enabled=current.proxy_enabled,
        metadata=current.metadata,
        proxy_url="https://eu.api.acme.com",  # a new base URL queues a run that regenerates every tool
    )
)
```

A change to the base URL is saved even when the call raises `ScalekitConflictException` because a run was already in progress: call `trigger_tool_collection` once that run completes. Changing `openapi_spec_url` is not enabled for every workspace (`FEATURE_NOT_ENABLED`). To pick up changes to the spec itself, call `trigger_tool_collection`.

**Use the tools**

```python
from scalekit.v1.tools.tools_pb2 import Filter

response, _ = scalekit_client.tools.list_tools(filter=Filter(provider=connector.identifier), page_size=100)
print([tool.definition["name"] for tool in response.tools])  # ['a-acmeapi_listpets', ...]

result, _ = scalekit_client.tools.execute_tool(
    tool_name="a-acmeapi_listpets",
    identifier="user@example.com",
    connection_name="acme-api",  # a connection on the connector
    params={"limit": 10},
)
```

`list_tools`, `list_scoped_tools`, `list_available_tools` and `execute_tool` serve a custom connector's tools like any others (see [Tools](#tools)), and `refresh_tools` re-reads a custom MCP connector's tools. `delete_custom_tool(tool_name)` deletes one tool of a connector created from an OpenAPI spec, by its name: a later full sync creates it again while its operation is still in the spec, and a sync that is queued or running makes the call raise `ScalekitConflictException` (details and errors: [REFERENCE.md](REFERENCE.md#tools)). To expose a custom connector's tools through a virtual MCP server, see [`ActionMcp` helper](#actionmcp-helper).

**Errors**

| Exception | `error_code` | When |
|-----------|--------------|------|
| `ScalekitBadRequestException` | `INVALID_ARGUMENT` | Invalid request: a spec URL that fails validation, a locked field of an OpenAPI-sourced connector changed, a broken credential placement, `trigger_tool_collection` on a connector that is not OpenAPI-sourced, an invalid `run_id` |
| `ScalekitBadRequestException` | `FEATURE_NOT_ENABLED` | OpenAPI-sourced connectors, multiple-headers `API_KEY` connectors, or changing `openapi_spec_url` are not enabled |
| `ScalekitBadRequestException` | `INVALID_HEADER_CONFIG` | A multiple-headers `API_KEY` rule is broken, or the connector was switched between single-key and multiple-headers mode |
| `ScalekitNotFoundException` | `NOT_FOUND` | `get_tool_collection_run` or `trigger_tool_collection` found no such connector, or no such run, or `delete_custom_tool` found no deletable tool of that name |
| `ScalekitConflictException` | `RESOURCE_ALREADY_EXISTS` | An OpenAPI connector with that name exists, or a run is already queued or running (`delete_custom_tool` and `delete_custom_provider` raise it then too, and delete nothing) |
| `ScalekitConflictException` | `TOOL_NAME_AMBIGUOUS` | `delete_custom_tool` found tools of more than one connector with that name and deleted nothing: call it again with `provider_identifier` |
| `ScalekitInternalServerException` | `INTERNAL_ERROR` | Validating the spec URL was interrupted, or the server failed |

### Trigger events

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">verify_event</a>(body, /, *, headers, secret) -> TriggerEvent</code></summary>
<dl><dd>

Verifies the signature of a trigger event Scalekit delivered to your endpoint, then parses it into an immutable [`TriggerEvent`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/models/trigger_event.py). The same function is available without a client as `scalekit.verify_trigger_event(body, /, *, headers, secret)`; both are local checks (no network call), so they are safe inside `async def` handlers.

- The signature is checked first: `webhook-signature` must be a `v1` HMAC-SHA256 of `"{webhook-id}.{webhook-timestamp}.{body}"` keyed with your `whsec_` secret, and `webhook-timestamp` must be within five minutes of now, given as Unix seconds in plain digits. Header names match case-insensitively. Every `webhook-signature` value is a candidate; a repeated `webhook-id` or `webhook-timestamp` must repeat the same value.
- Any verification failure raises `WebhookVerificationError`. A correctly signed body that is not a valid trigger event raises `ScalekitTriggerEventParseException`, a subclass, so one `except WebhookVerificationError` answering `400` covers both. Raises `TypeError` when called with arguments of the wrong type.
- Delivery is at least once, and a redelivery can arrive while the first delivery is still being handled. Use `dedupe_key` plus the connected account you act as as the idempotency key:
  - Claim it atomically before handling the event, so two concurrent deliveries cannot both handle it. For example, use a row with a unique key on both, inserted with a lease (an expiry time). The claim succeeds only when no row exists, or when the row is unfinished and its lease has expired.
  - Make the lease longer than handling can take. A claim left by a worker that stopped mid-handling then expires, and a later redelivery can take it, but an active claim is never taken.
  - Mark the claim finished after handling, so a finished event is never handled again. Release it if handling fails, so a redelivery can retry at once.
  - Answer `2xx` only once the event is finished, handled, or durably queued. When another delivery still holds an unexpired claim, answer a non-`2xx` status such as `409`, so Scalekit delivers the event again later instead of treating it as done.
- Branch on `delivery_scope`: `DeliveryScope.ACCOUNT` events carry `connected_account_id`; `DeliveryScope.CONNECTION` events apply to the whole connection and have `connected_account_id == ""`.
- When `payload_state` is `PayloadState.REFERENCE`, `payload` is `None`: fetch the resource by `resource_type` and `resource_id`.
- Enum fields hold the enum member for known values and the raw `str` for newer ones; fields this SDK version does not know are kept in `event.model_extra`. `occurred_at` is a timezone-aware UTC `datetime` or `None`; fractional seconds are truncated to microseconds.

```python
import os
from flask import Flask, request
from scalekit import DeliveryScope, PayloadState, verify_trigger_event
from scalekit.common.exceptions import WebhookVerificationError

app = Flask(__name__)

@app.post("/scalekit/triggers")
def scalekit_trigger():
    try:
        event = verify_trigger_event(
            request.get_data(),  # raw body, before any JSON parsing
            headers=request.headers,
            secret=os.environ["SCALEKIT_TRIGGER_SECRET"],
        )
    except WebhookVerificationError:  # bad signature, stale timestamp, or malformed event
        return "", 400

    if event.delivery_scope == DeliveryScope.ACCOUNT:
        account_ids = [event.connected_account_id]
    elif event.delivery_scope == DeliveryScope.CONNECTION:
        account_ids = accounts_for_connection(event.connection_id)  # your lookup
    else:
        return "", 204  # a scope this code does not handle yet

    in_progress = False
    for account_id in account_ids:
        # Atomic, with a lease longer than handling takes. Returns "claimed",
        # "finished" (already handled) or "in_progress" (another delivery holds
        # an unexpired lease).
        claim = claim_delivery(event.dedupe_key, account_id, lease_seconds=900)
        if claim == "finished":
            continue
        if claim == "in_progress":
            in_progress = True
            continue
        try:
            data = (
                fetch_resource(account_id, event.resource_type, event.resource_id)
                if event.payload_state == PayloadState.REFERENCE
                else event.payload
            )
            handle(account_id, event.trigger_type, data)
        except Exception:
            release_delivery(event.dedupe_key, account_id)  # let a redelivery retry
            raise
        finish_delivery(event.dedupe_key, account_id)  # never handled again
    if in_progress:
        return "", 409  # not done yet: Scalekit delivers it again later
    return "", 204
```

**Parameters:** `body: str | bytes` (positional) - the raw request body · `headers: HeadersLike` - the request headers (`request.headers` from Flask/Werkzeug, Starlette/FastAPI or Django, or a `dict`/`Mapping`) · `secret: str` - the trigger signing secret (`whsec_...`).

</dd></dl>
</details>


### Managing triggers

`client.actions.triggers` also manages triggers over the network: which triggers a connection offers, who is subscribed, the webhook URL and signing secret a provider uses, and what happened to the events Scalekit delivered to your endpoints. Every method returns a typed, frozen model (fields cannot be reassigned, though nested lists and dicts are ordinary mutable copies; enum members for known values, a plain `str` for newer ones; aware UTC `datetime`; `timedelta`; empty page tokens are `None`). Per-method details: [REFERENCE.md → Triggers](REFERENCE.md#triggers).

**Subscribe connected accounts**

1. `actions.triggers.list_available(connection_id)` returns the catalogue. Each `AvailableTrigger` says how it detects changes (`mode`: `DetectionMode.WEBHOOK` or `DetectionMode.POLL`), whether it is usable here (`available`, with `reason`, `remedy`, `refusal_code`), its `config_fields` and, for poll triggers, `min_interval` / `default_interval`.
2. `actions.triggers.list_eligible_accounts(connection_id, trigger_name)` pages through the connected accounts and whether each can subscribe; `health.action` says how to fix one that cannot.
3. `actions.triggers.create_subscription(...)` subscribes one account; `actions.triggers.batch_create_subscriptions(...)` subscribes up to 100 and reports an outcome per account instead of raising. For a connection-scoped trigger, leave the account out.
4. `actions.triggers.list_subscriptions`, `actions.triggers.delete_subscription` and `actions.triggers.batch_delete_subscriptions` manage what exists.

```python
from datetime import timedelta
from scalekit.actions import DetectionMode, TriggerSubscribeOutcome
from scalekit.common.exceptions import ScalekitConflictException

catalogue = scalekit_client.actions.triggers.list_available("conn_123")
poll = next(t for t in catalogue.triggers if t.mode == DetectionMode.POLL and t.available)

try:
    sub = scalekit_client.actions.triggers.create_subscription(
        "conn_123", poll.name, connected_account_id="ca_123", interval=timedelta(minutes=5)
    )
except ScalekitConflictException:  # already subscribed with the same config
    sub = None

page = scalekit_client.actions.triggers.list_eligible_accounts("conn_123", poll.name, page_size=100)
batch = scalekit_client.actions.triggers.batch_create_subscriptions(
    "conn_123", poll.name, connected_account_ids=[a.id for a in page.accounts if a.eligible]
)
retry_later = [
    r.connected_account_id for r in batch.results
    if r.outcome in (TriggerSubscribeOutcome.FAILED, TriggerSubscribeOutcome.NOT_ATTEMPTED)
]
```

`actions.triggers.create_subscription` is never retried on `UNAVAILABLE`, because a retry could create the subscription twice; `actions.triggers.batch_create_subscriptions` is safe to call again (an existing one comes back as `ALREADY_SUBSCRIBED`).

**Webhook URL and signing secret** (webhook triggers)

1. `actions.triggers.create_ingress_endpoint(connection_id)` returns the URL to paste into the provider's app configuration (safe to call again; `actions.triggers.get_ingress_endpoint` reads it later). Treat `url` as confidential.
2. If the provider shows you a signing secret, store it with `actions.triggers.set_signing_secret(connection_id, signing_secret=...)`. If Scalekit creates the secret for this provider (`actions.triggers.set_signing_secret` raises `ScalekitBadRequestException` with `error_code` `TRIGGER_SIGNING_SECRET_GENERATED_ONLY`), call `actions.triggers.generate_signing_secret(connection_id)` instead: its `signing_secret` and `url_with_secret` are returned only once and are left out of `repr()`.
3. To rotate, call `actions.triggers.set_signing_secret` with the new secret. Both secrets are accepted until you confirm, or for 24 hours (`previous_signing_secret_expires_at`). Once the provider uses the new one, confirm:

```python
import os

endpoint = scalekit_client.actions.triggers.set_signing_secret("conn_123", signing_secret=os.environ["NEW_PROVIDER_SECRET"])
# Both secrets are accepted now. Confirm only once the provider signs with the new
# secret: after confirming, events signed with the old one fail verification.
if endpoint.rotation_in_progress:
    scalekit_client.actions.triggers.confirm_signing_secret_rotation(
        "conn_123", signing_secret_rotation_id=endpoint.signing_secret_rotation_id
    )
```

`actions.triggers.set_signing_secret` and `actions.triggers.generate_signing_secret` are never retried on `UNAVAILABLE`. Until a secret is stored the URL answers events with `503`, so the provider retries them.

**One URL per connected account.** Some webhook triggers are delivered through one URL per connected account instead of one per connection; `actions.triggers.list_available` marks them with `ingress_per_account=True`. For those, pass `connected_account_id` (keyword-only, `ca_...`) to `create_ingress_endpoint`, `get_ingress_endpoint`, `set_signing_secret`, `confirm_signing_secret_rotation` and `generate_signing_secret`, and register each account's URL in that account's own provider settings. The returned `TriggerIngressEndpoint` has `scope` (`DeliveryScope.ACCOUNT` or `DeliveryScope.CONNECTION`) and `connected_account_id`. Leaving `connected_account_id` out keeps acting on the connection's URL; an empty string raises `ValueError`.

```python
endpoint = scalekit_client.actions.triggers.create_ingress_endpoint("conn_123", connected_account_id="ca_456")
print("paste into this account's provider settings:", endpoint.url)
```

**Activity, usage and deliveries**

- `actions.triggers.get_activity()` counts recent trigger events by outcome. `signature_banner` means many events failed signature verification (the stored secret probably does not match the provider's); while `degraded` is true, zero counts are not reliable.
- `actions.triggers.get_usage(period="24h" | "7d" | "30d")` or `actions.triggers.get_usage(from_date=..., to_date=...)` reads metered deliveries per UTC hour or day.
- For one of your delivery endpoints: `actions.triggers.list_deliveries(endpoint_id, ...)` (filter by `status`, `channel`, `after`, `before`), `actions.triggers.list_delivery_attempts_by_endpoint`, `actions.triggers.list_delivery_attempts_by_message`, `actions.triggers.lookup_delivery(delivery_id)` (a `msg_` ID or the `dedupe_key` your handler received), `actions.triggers.batch_lookup_deliveries`.
- To send messages again: `actions.triggers.batch_resend_deliveries([...])` for specific messages, or `actions.triggers.recover_deliveries(endpoint_id, since=...)` for everything that failed in a time range. Neither is retried on `UNAVAILABLE`. If `actions.triggers.recover_deliveries` raises `ScalekitInternalServerException`, the recovery may be running anyway: check the endpoint's deliveries before calling again.

```python
from datetime import datetime, timedelta, timezone
from scalekit.actions import TriggerDeliveryStatus

failed = scalekit_client.actions.triggers.list_deliveries(
    "ep_123", status=TriggerDeliveryStatus.FAILED, after=datetime.now(timezone.utc) - timedelta(hours=6)
)
if failed.deliveries:
    scalekit_client.actions.triggers.batch_resend_deliveries(
        [{"msg_id": d.msg_id, "endpoint_id": d.endpoint_id} for d in failed.deliveries]
    )
```

**Errors**

Server errors raise the `ScalekitServerException` subclass for the status (all importable from `scalekit.common.exceptions`); branch on `error_code` for the reason. Arguments that cannot be sent (an empty required ID, a naive `datetime`, an interval that is not whole seconds, an unknown enum name) raise `ValueError` before any request. Batch methods report per-item outcomes in `results` and do not raise for them.

| Exception | `error_code` | When |
|-----------|--------------|------|
| `ScalekitNotFoundException` | `RESOURCE_NOT_FOUND` | Unknown connection, trigger, account, subscription or recovery endpoint; also when triggers are not enabled for the environment |
| `ScalekitNotFoundException` | `TRIGGER_INGRESS_ENDPOINT_NOT_CREATED` | No webhook URL yet: call `actions.triggers.create_ingress_endpoint` |
| `ScalekitNotFoundException` | `TRIGGER_USAGE_NOT_METERED` | Usage is not metered for this environment |
| `ScalekitNotFoundException` | `NOT_FOUND` | `actions.triggers.lookup_delivery` found no such message or event |
| `ScalekitBadRequestException` | `INVALID_ARGUMENT` | Invalid argument, or an account refused for a subscription (the message says how to fix it). The delivery listing methods also answer an unknown endpoint with this (400), unlike `actions.triggers.recover_deliveries` (404) |
| `ScalekitBadRequestException` | `TRIGGER_INGRESS_NOT_APPLICABLE` | The connection has no webhook trigger |
| `ScalekitBadRequestException` | `TRIGGER_INGRESS_DEFINITIONS_UNAVAILABLE` | The connection's trigger definitions cannot be read right now |
| `ScalekitBadRequestException` | `TRIGGER_SIGNING_SECRET_GENERATED_ONLY` | Use `actions.triggers.generate_signing_secret` for this provider |
| `ScalekitBadRequestException` | `TRIGGER_SIGNING_SECRET_NOT_GENERATABLE` | The provider signs its own events: use `actions.triggers.set_signing_secret` |
| `ScalekitConflictException` | `RESOURCE_ALREADY_EXISTS` | The subscription already exists, or a secret rotation is already in progress |
| `ScalekitTooManyRequestsException` | `RATE_LIMITED` or none | Rate limited; never retried by the SDK |
| `ScalekitServiceUnavailableException` | none | Temporarily unavailable (for `actions.triggers.create_subscription`: it may or may not have been created; check `actions.triggers.list_subscriptions` before calling again) |
| `ScalekitGatewayTimeoutException` | none | The deadline passed; for `actions.triggers.create_subscription` (and the other calls that could apply twice), the request may still have taken effect: check before calling again |
| `ScalekitInternalServerException` | `INTERNAL_ERROR` | Server error; for `actions.triggers.recover_deliveries`, the recovery may be running |

**Async code**

These methods block the calling thread (only `verify_event` is local). Inside `async def`, run them in a worker thread so the event loop keeps serving requests:

```python
import asyncio

page = await asyncio.to_thread(scalekit_client.actions.triggers.list_subscriptions, "conn_123")
```

## MCP (`McpClient`)

Low-level MCP configuration and instance APIs on `client.mcp` ([`scalekit/mcp.py`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py)). For higher-level helpers that return parsed wrappers, use `client.connect.mcp` / `client.actions.mcp` (see [ActionMcp](#connect-and-actions-actionclient)).

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">list_configs</a>(page_size?, page_token?, filter_id?, filter_provider?, filter_name?, filter_mcp_server_url?, search?) -> ListMcpConfigsResponse</code></summary>
<dl><dd>

### 📝 Description

Lists MCP server configurations with optional filters.

### ⚙️ Parameters

**page_size**, **page_token** — Pagination.

**filter_id**, **filter_provider**, **filter_name**, **filter_mcp_server_url**, **search** — Restrict or search configs. `filter_mcp_server_url` returns the config behind one MCP server URL (it is found from the last path segment of the URL).

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">create_config</a>(mcp_config: McpConfig) -> CreateMcpConfigResponse</code></summary>
<dl><dd>

### 📝 Description

Creates a configuration from a protobuf `McpConfig` message.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">update_config</a>(config_id, description?, connection_tool_mappings?) -> UpdateMcpConfigResponse</code></summary>
<dl><dd>

### 📝 Description

Updates description and/or connector–tool mappings.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">delete_config</a>(config_id) -> DeleteMcpConfigResponse</code></summary>
<dl><dd>

### 📝 Description

Deletes a configuration by id.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">ensure_instance</a>(name, config_name, user_identifier) -> EnsureMcpInstanceResponse</code></summary>
<dl><dd>

### 📝 Description

Creates or returns an MCP instance for a config and user.

`name` (the display name of the instance) is a required positional argument, in this order: `name`, `config_name`, `user_identifier`. Pass `None` to leave it unset, for example `ensure_instance(None, 'my-config', 'user@example.com')`. Leaving the argument out raises `TypeError`.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">update_instance</a>(instance_id, name?, config_name?) -> UpdateMcpInstanceResponse</code></summary>
<dl><dd>

### 📝 Description

Updates mutable fields on an instance.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">get_instance</a>(instance_id) -> GetMcpInstanceResponse</code></summary>
<dl><dd>

### 📝 Description

Fetches one instance by id.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">list_instances</a>(page_size?, page_token?, filter_id?, filter_name?, filter_config_name?, filter_user_identifier?) -> ListMcpInstancesResponse</code></summary>
<dl><dd>

### 📝 Description

Lists instances with optional filters.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">delete_instance</a>(instance_id) -> DeleteMcpInstanceResponse</code></summary>
<dl><dd>

### 📝 Description

Deletes an instance.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">get_instance_auth_state</a>(instance_id, include_auth_links?) -> GetMcpInstanceAuthStateResponse</code></summary>
<dl><dd>

### 📝 Description

Returns authorization state for connectors used by the instance; optional fresh auth links.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">create_session_token</a>(mcp_config_id?, identifier, expiry?, access_level?, *, connection_name?) -> (CreateMcpSessionTokenResponse, grpc.Call)</code></summary>
<dl><dd>

### 📝 Description

Mints a short-lived session token for an end user. Pass exactly one of `mcp_config_id` or `connection_name` (keyword-only); the token works only on the MCP server of that target:

- `mcp_config_id`: the MCP configuration's server, at the config's `mcp_server_url`, serving the tools the configuration exposes.
- `connection_name`: the connection's own MCP server, at `<environment_url>/mcp/v3/connections/<connection_name>`, serving every tool of that connection with no MCP configuration. The name is matched without regard to case, but the URL path is case-sensitive: connect using the name exactly as stored, e.g. copied from the dashboard.

`identifier` (1 to 255 characters) is required: the user of the configuration's instance, or the user whose connected account on the connection is used. `expiry` is a `timedelta` from 60 seconds to 24 hours (default 1 hour). `access_level` is `"FULL"` (default) or `"READ_ONLY"`, which limits the token to tools annotated read-only: other tools are left out of the tool list and refused when called.

Raises `ValueError` before any request when neither `mcp_config_id` nor `connection_name` is passed, or, with `connection_name`, when `mcp_config_id` is also given, `connection_name` is empty, or `identifier` is missing or empty. With `mcp_config_id`, `client.mcp` sends the arguments as given and the server validates them; `client.actions.mcp` raises `ValueError` when `mcp_config_id` or `identifier` is empty, as before. Raises `ScalekitNotFoundException` when no active connection has that name, and `ScalekitBadRequestException` for any other invalid request, e.g. an invalid `identifier`, `expiry` or `access_level`, or a connection that is not an AgentKit connection. Depending on the environment's configuration, a connection token also requires `identifier` to have an active connected account on the connection; otherwise the server creates a pending connected account for `identifier` if it has none on the connection, a token is minted, and the account is reported as not connected when tools are called.

### 🔌 Usage

```python
from datetime import timedelta

# MCP configuration (positional arguments keep working)
response, _ = scalekit_client.mcp.create_session_token("cfg_01abc123", "user_123")

# A connection's MCP server, read-only tools for 15 minutes
response, _ = scalekit_client.mcp.create_session_token(
    connection_name="gmail",
    identifier="user_123",
    expiry=timedelta(minutes=15),
    access_level="READ_ONLY",
)
headers = {"Authorization": f"Bearer {response.token}"}
```

`client.connect.mcp.create_session_token(...)` / `client.actions.mcp.create_session_token(...)` take the same arguments and return a parsed `CreateMcpSessionTokenResponse` with `token` and `expires_at` (a naive `datetime` in UTC).

</dd></dl>
</details>


# AgentKit API reference (Python)

This document lists **AgentKit** Scalekit SDK surfaces: tools, connected accounts, the `ActionClient` facade (`connect` / `actions`), and the low-level `McpClient` (Python).

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

OAuth login (`get_authorization_url`, `authenticate_with_code`, …) and MCP **Bring-your-own-auth** (`client.auth.update_login_user_details`) are documented under **ScalekitClient** / **Auth** in [`REFERENCE.md`](REFERENCE.md), not in this AgentKit guide.

## Tools

Low-level gRPC helpers on `client.tools` ([`scalekit/tools.py`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py)).

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_tools</a>(filter?, page_size?, page_token?) -> ListToolsResponse</code></summary>
<dl>
<dd>

### 📝 Description

Lists tools available in your workspace with optional filtering and pagination.

### 🔌 Usage

```python
from scalekit.v1.tools.tools_pb2 import Filter

response = scalekit_client.tools.list_tools(
    filter=Filter(query="calendar"),
    page_size=50,
)
```

### ⚙️ Parameters

**filter:** `Optional[Filter]` — Filter on provider, identifier, tool metadata, etc.

**page_size:** `Optional[int]` — Page size.

**page_token:** `Optional[str]` — Pagination cursor.

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_scoped_tools</a>(identifier, filter?, page_size?, page_token?) -> ListScopedToolsResponse</code></summary>
<dl>
<dd>

### 📝 Description

Lists tools scoped to a specific connected-account identifier (for example workspace or email).

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

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">execute_tool</a>(tool_name, identifier, params?, connected_account_id?) -> ExecuteToolResponse</code></summary>
<dl>
<dd>

### 📝 Description

Executes a named tool using credentials from a connected account.

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

</dd>
</dl>
</details>

## Connected Accounts

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">list_connected_accounts</a>(organization_id?, user_id?, connector?, identifier?, provider?, page_size?, page_token?) -> ListConnectedAccountsResponse</code></summary>
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

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">get_magic_link_for_connected_account</a>(connector, identifier, organization_id?, user_id?, connected_account_id?) -> GetMagicLinkForConnectedAccountResponse</code></summary>
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

print(f'Magic Link: {response[0].magic_link}')
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

## Connect and Actions (`ActionClient`)

`ScalekitClient.connect` and `ScalekitClient.actions` are the same [`ActionClient`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py) instance — a facade over `tools`, `connected_accounts`, and `mcp` with typed helpers, modifiers, and optional framework integrations.

### Properties

- **`langchain`** — Lazy `LangChain` helper (requires `langchain` installed).
- **`google`** — Lazy Google ADK helper (requires `google-adk` installed).
- **`mcp`** — [`ActionMcp`](#actionmcp-helper) for MCP operations that return parsed response wrappers.

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

</dd></dl>
</details>

<details><summary><code>client.actions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">upload_resumable</a>(connection_name, identifier, path, *, data, total_bytes?, content_type?, metadata?, method?, query_params?, chunk_size?, max_retries?, timeout?, on_progress?) -> dict</code></summary>
<dl>
<dd>

### 📝 Description

Uploads content of any size to Google Drive, Cloud Storage or YouTube through the Scalekit proxy, using Google's resumable upload protocol. The content is sent in chunks (4 MiB by default) and at most one chunk is held in memory. A chunk that fails with a timeout, a connection error or HTTP 408, 429, 500, 502, 503 or 504 is resumed from what the server stored instead of restarting (exponential backoff with jitter, or `Retry-After` on 429 and 503, capped at 30 seconds). The request that starts the session is never retried, because a retry would open a second session; the only exception is a single resend after the SDK refreshes an expired Scalekit access token (a 401 from Scalekit itself, not from Google). Returns the created or updated resource as a dict, for example the Drive file (`{}` when the final response is empty).

Errors (all in `scalekit.common.exceptions`):

- `ScalekitUploadSessionExpiredException` (subclass of `ScalekitUploadException`): the session expired or was cancelled (HTTP 404 or 410 after it started). Start a new upload; the SDK never restarts one on its own.
- `ScalekitUploadException`: the session-start request failed, a chunk failed with a non-retryable status (such as 403), or a retryable failure persisted after `max_retries` retries. `status_code` is `None` when no response arrived.
- `ScalekitUploadProtocolException`: the server's answer does not follow the protocol (for example, no `upload_id` in the session-start response).

Each carries `status_code`, `headers`, `body`, `upload_id` and `bytes_committed`. Invalid arguments raise `ValueError` or `TypeError` before any network call. A path that cannot be opened raises `OSError` (for example `FileNotFoundError`), and errors from reading your stream propagate unchanged. The call blocks; in async code use `await asyncio.to_thread(...)`.

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

Access via `client.connect.mcp` / `client.actions.mcp`. Requires `McpClient` to be initialized on the parent `ScalekitClient`. Methods include `list_configs`, `create_config` (builds `McpConfig` from `name` / `description` / mappings), `update_config`, `delete_config`, `ensure_instance`, `update_instance`, `get_instance`, `list_instances`, `delete_instance`, and `get_instance_auth_state`, returning parsed wrapper types instead of raw gRPC tuples.


## MCP (`McpClient`)

Low-level MCP configuration and instance APIs on `client.mcp` ([`scalekit/mcp.py`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py)). For higher-level helpers that return parsed wrappers, use `client.connect.mcp` / `client.actions.mcp` (see [ActionMcp](#connect-and-actions-actionclient)).

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">list_configs</a>(page_size?, page_token?, filter_id?, filter_provider?, filter_name?, search?) -> ListMcpConfigsResponse</code></summary>
<dl><dd>

### 📝 Description

Lists MCP server configurations with optional filters.

### ⚙️ Parameters

**page_size**, **page_token** — Pagination.

**filter_id**, **filter_provider**, **filter_name**, **search** — Restrict or search configs.

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

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">ensure_instance</a>(name?, config_name, user_identifier) -> EnsureMcpInstanceResponse</code></summary>
<dl><dd>

### 📝 Description

Creates or returns an MCP instance for a config and user.

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


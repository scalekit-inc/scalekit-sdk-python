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


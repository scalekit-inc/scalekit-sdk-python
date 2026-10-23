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

**Which one to use:** use `actions` for almost everything. `connect` is the same object under another name. `tools`, `connected_accounts` and `mcp` are the lower layers it wraps: they return the raw `(response, call)` tuple, and the lower `connected_accounts` layer calls the connection name `connector`.

Two words appear in almost every call:

- **`connection_name`** is the name of a connection, for example `slack-b1fqL2Dr`, as shown for the connection in the dashboard. It is not the provider's name (`Slack`).
- **`identifier`** is the identifier a connected account was created with, usually your end user's ID or email. It is yours to choose, and it is how Scalekit finds that user's account.

## How the pieces fit together

To run a tool for one of your users:

1. **Create the connection** for the service in the dashboard. Its name is your `connection_name`.
2. **Send the user an authorization link.** This is also how a connected account is created:

   ```python
   link = client.actions.get_authorization_link(
       connection_name="gmail-b1fqL2Dr",
       identifier="user_123",
   )
   print(link.link, link.expiry)  # send link.link to the user before it expires
   ```

3. **The user authorizes.** If you passed `user_verify_url`, they are redirected there with an `auth_request_id`. Confirm the user with `client.actions.verify_connected_account_user(auth_request_id=..., identifier="user_123")`.
4. **Run the tool:**

   ```python
   result = client.actions.execute_tool(
       tool_name="gmail.messages.list",
       tool_input={"maxResults": 10},
       identifier="user_123",
       connection_name="gmail-b1fqL2Dr",
   )
   print(result.data)
   ```

   `identifier` alone is enough when that user has exactly one account for the tool's provider. If there is none the call fails as not found, and if there are several it fails as a bad request: then add `connection_name` or pass `connected_account_id`.

To give a user access to a virtual MCP server instead, see [MCP](#mcp-mcpclient).

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

**identifier:** `str` — The identifier the connected account was created with, usually your end user's ID or email.

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

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">execute_tool</a>(tool_name, identifier, params?, connected_account_id?, connection_name?) -> ExecuteToolResponse</code></summary>
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

**identifier:** `str` — The identifier the connected account was created with, usually your end user's ID or email.

**params:** `Optional[dict]` — JSON-serializable tool arguments.

**connected_account_id:** `Optional[str]` — Use a specific connected account by id.

**connection_name:** `Optional[str]` — Connection name, for example `slack-b1fqL2Dr`, not the provider's name. Use it with `identifier` to pick the account on that connection.

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

**connector:** `Optional[str]` - Connection name, for example `slack-b1fqL2Dr`, not the provider's name. The `actions` facade calls this `connection_name`.

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

**connector:** `str` - Connection name, for example `slack-b1fqL2Dr`, not the provider's name. The `actions` facade calls this `connection_name`.

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

**connector:** `str` - Connection name, for example `slack-b1fqL2Dr`, not the provider's name. The `actions` facade calls this `connection_name`.

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

**connector:** `str` - Connection name, for example `slack-b1fqL2Dr`, not the provider's name. The `actions` facade calls this `connection_name`.

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

**connector:** `str` - Connection name, for example `slack-b1fqL2Dr`, not the provider's name. The `actions` facade calls this `connection_name`.

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

**connector:** `str` - Connection name, for example `slack-b1fqL2Dr`, not the provider's name. The `actions` facade calls this `connection_name`.

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

<details><summary><code>client.connect.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">execute_tool</a>(tool_input, tool_name, identifier?, tool_request?, connected_account_id?, connection_name?, **kwargs) -> ExecuteToolResponse</code></summary>
<dl><dd>

Runs pre/post modifiers then delegates to `client.tools.execute_tool`. `tool_name` is required. The response has `data` (the tool's output) and `execution_id`.

Which connected account is used: `identifier` alone is enough when that user has exactly one account for the tool's provider. If there is none the call fails as not found (`ScalekitNotFoundException`), and if there are several it fails as a bad request (`ScalekitBadRequestException`): then add `connection_name` or pass `connected_account_id`. `connected_account_id` picks the account directly, and `connection_name` with `identifier` picks the account on that connection. With none of these the server rejects the call; this method does not check that itself.

`tool_request` and unknown keyword arguments are accepted and ignored.

</dd></dl>
</details>

### OAuth and connected accounts

<details><summary><code>get_authorization_link</code> / <code>verify_connected_account_user</code> / <code>list_connected_accounts</code> / <code>delete_connected_account</code> / <code>get_connected_account</code></summary>
<dl><dd>

High-level wrappers around `connected_accounts` with friendlier parameter names (`connection_name` vs `connector`) and typed response objects. Identify an account by `connected_account_id`, or by `connection_name` with `identifier`. Unknown keyword arguments are accepted and ignored.

| Method | What it does | Returns |
|--------|--------------|---------|
| `get_authorization_link(identifier?, connection_name?, connected_account_id?, state?, user_verify_url?)` | Link the user opens to connect or re-authorize an account. | `MagicLinkResponse` (`link`, `expiry`) |
| `verify_connected_account_user(auth_request_id, identifier)` | Confirms the user after the redirect back to your `user_verify_url`. | `VerifyConnectedAccountUserResponse` |
| `list_connected_accounts(connection_name?, identifier?, provider?, connection_names?, page_size?, page_token?)` | Lists accounts, optionally filtered. | `ListConnectedAccountsResponse` |
| `get_connected_account(connection_name?, identifier?, connected_account_id?)` | One account **with its credentials**. Treat the result as a secret. | `GetConnectedAccountAuthResponse` |
| `get_connected_account_details(connection_name?, identifier?, connected_account_id?)` | The same account **without credentials**. | `GetConnectedAccountDetailsResponse` |
| `delete_connected_account(connection_name?, identifier?, connected_account_id?)` | Deletes an account. | `DeleteConnectedAccountResponse` |
| `list_tools(connection_name?, identifier?, provider?, tool_name?, query?, organization_id?, user_id?, connected_account_id?, summary?, page_size?, page_token?)` | Lists tools, optionally scoped to one account. | `ListToolsResponse` |

</dd></dl>
</details>

<details><summary><code>create_connected_account</code> / <code>get_or_create_connected_account</code> / <code>update_connected_account</code></summary>
<dl><dd>

Create, upsert, or update accounts using dict-based auth payloads converted to protobuf. To connect a user's account, prefer `get_authorization_link`: it creates the account if needed and the user completes authorization through the link. OAuth credentials cannot be supplied directly.

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

To give users access to a virtual MCP server, create one configuration per agent role (`create_config`) and mint a short-lived session token per user (`create_session_token`). The instance methods (`ensure_instance`, `get_instance`, `list_instances`, `update_instance`, `delete_instance`, `get_instance_auth_state`) are preview in the API and may change. `ensure_instance` takes its arguments in a different order here than on `client.mcp`, so pass them as keywords.

Access via `client.connect.mcp` / `client.actions.mcp`. Requires `McpClient` to be initialized on the parent `ScalekitClient`. Methods include `list_configs`, `create_config` (builds `McpConfig` from `name` / `description` / mappings), `update_config`, `delete_config`, `ensure_instance`, `update_instance`, `get_instance`, `list_instances`, `delete_instance`, `get_instance_auth_state`, and `create_session_token`, returning parsed wrapper types instead of raw gRPC tuples.


## MCP (`McpClient`)

Configurations, `create_session_token` and `list_mcp_connected_accounts` are generally available. The instance methods are preview in the API and may change. `ensure_instance` takes `name` first here but last on `client.actions.mcp`: pass keywords.

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


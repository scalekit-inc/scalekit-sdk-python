# AgentKit API reference (Python)

This document lists **AgentKit-related** Scalekit SDK methods: Bring-your-own-auth for MCP, tools, connected accounts, M2M clients, the `ActionClient` facade (`connect` / `actions`), and the low-level `McpClient`.

For the full SDK surface (organizations, SSO **connections**, users, sessions, etc.), see [`REFERENCE.md`](REFERENCE.md).

**Note:** `client.connection` (enterprise SSO IdP **connections**) is not part of AgentKit; it remains documented only in `REFERENCE.md`.

## Table of contents

- [Auth](#auth)
- [Tools](#tools)
- [Connected Accounts](#connected-accounts)
- [M2M Client](#m2m-client)
- [Connect and Actions (`ActionClient`)](#connect-and-actions-actionclient)
- [MCP (`McpClient`)](#mcp-mcpclient)

## Auth

<details><summary><code>client.auth.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/auth.py">update_login_user_details</a>(connection_id, login_request_id, user?) -> Empty</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates user details for an ongoing authentication request.

If you are using Auth for MCP solution of Scalekit in "Bring your own Auth" mode, this method helps updating Scalekit with the currently logged in user details for the ongoing authentication request.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
scalekit_client.auth.update_login_user_details(
    'conn_abc123',
    'login_xyz789',
    {
        'email': 'john.doe@company.com',
        'sub': 'unique_user_id_456',
    }
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**connection_id:** `str` - The SSO connection ID being used for authentication

</dd>
</dl>

<dl>
<dd>

**login_request_id:** `str` - The unique login request identifier from the auth flow

</dd>
</dl>

<dl>
<dd>

**user:** `Optional[Mapping[str, Any]]` - User details to update
- `email: Optional[str]` - User's email address
- `sub: Optional[str]` - Unique user identifier (subject)
- `given_name: Optional[str]` - User's first name
- `family_name: Optional[str]` - User's last name
- `email_verified: Optional[bool]` - Whether email is verified
- `phone_number: Optional[str]` - User's primary phone number
- `phone_number_verified: Optional[bool]` - Whether phone is verified
- `name: Optional[str]` - Full display name of the user
- `preferred_username: Optional[str]` - User's preferred username
- `picture: Optional[str]` - URL to user's profile picture
- `gender: Optional[str]` - User's gender
- `locale: Optional[str]` - User's locale preference
- `groups: Optional[list[str]]` - List of group names or IDs
- `custom_attributes: Optional[dict]` - Custom attributes as dict

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>


## Tools

Low-level gRPC helpers on `client.tools` ([`scalekit/tools.py`](https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py)).

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_tools</a>(filter?, page_size?, page_token?) -> ListToolsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

Lists tools available in your workspace with optional filtering and pagination.

#### 🔌 Usage

```python
from scalekit.v1.tools.tools_pb2 import Filter

response = scalekit_client.tools.list_tools(
    filter=Filter(query="calendar"),
    page_size=50,
)
```

#### ⚙️ Parameters

**filter:** `Optional[Filter]` — Filter on provider, identifier, tool metadata, etc.

**page_size:** `Optional[int]` — Page size.

**page_token:** `Optional[str]` — Pagination cursor.

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_scoped_tools</a>(identifier, filter?, page_size?, page_token?) -> ListScopedToolsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

Lists tools scoped to a specific connected-account identifier (for example workspace or email).

#### 🔌 Usage

```python
from scalekit.v1.tools.tools_pb2 import ScopedToolFilter

response = scalekit_client.tools.list_scoped_tools(
    "user@example.com",
    filter=ScopedToolFilter(),
)
```

#### ⚙️ Parameters

**identifier:** `str` — Connected account identifier.

**filter:** `Optional[ScopedToolFilter]` — Required filter for scoped listing.

**page_size:** `Optional[int]` — Page size.

**page_token:** `Optional[str]` — Pagination cursor.

</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">execute_tool</a>(tool_name, identifier, params?, connected_account_id?) -> ExecuteToolResponse</code></summary>
<dl>
<dd>

#### 📝 Description

Executes a named tool using credentials from a connected account.

#### 🔌 Usage

```python
response = scalekit_client.tools.execute_tool(
    tool_name="gmail.messages.list",
    identifier="user@example.com",
    params={"maxResults": 10},
)
```

#### ⚙️ Parameters

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

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all connected accounts with optional filtering.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

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

#### ⚙️ Parameters

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

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a connected account by identifier.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

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

#### ⚙️ Parameters

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

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new connected account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

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

#### ⚙️ Parameters

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

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing connected account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

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

#### ⚙️ Parameters

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

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a connected account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

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

#### ⚙️ Parameters

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

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a magic link for a connected account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

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

#### ⚙️ Parameters

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

## M2M Client

<details><summary><code>client.m2m_client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/m2m_client.py">list_organization_clients</a>(organization_id, page_size?, page_token?) -> ListOrganizationClientsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all machine-to-machine clients for an organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
response = scalekit_client.m2m_client.list_organization_clients(
    'org_123456',
    page_size=50
)

for client in response[0].clients:
    print(f'Client: {client.id}')
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `str` - Organization ID to list clients for

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Page size for pagination (between 10 and 100)

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

<details><summary><code>client.m2m_client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/m2m_client.py">get_organization_client</a>(organization_id, client_id) -> GetOrganizationClientResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves an organization client by ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
response = scalekit_client.m2m_client.get_organization_client(
    'org_123456',
    'client_123456'
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.m2m_client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/m2m_client.py">create_organization_client</a>(organization_id, m2m_client) -> CreateOrganizationClientResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new machine-to-machine client for an organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.v1.clients.clients_pb2 import OrganizationClient

client = OrganizationClient()
client.name = "My M2M Client"

response = scalekit_client.m2m_client.create_organization_client(
    'org_123456',
    client
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `str` - Organization ID to create client for

</dd>
</dl>

<dl>
<dd>

**m2m_client:** `OrganizationClient` - Client object with desired client properties

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.m2m_client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/m2m_client.py">update_organization_client</a>(organization_id, client_id, m2m_client) -> UpdateOrganizationClientResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing machine-to-machine client.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.v1.clients.clients_pb2 import OrganizationClient

client = OrganizationClient()
client.name = "Updated M2M Client"

response = scalekit_client.m2m_client.update_organization_client(
    'org_123456',
    'client_123456',
    client
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client ID

</dd>
</dl>

<dl>
<dd>

**m2m_client:** `OrganizationClient` - Organization Client object

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.m2m_client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/m2m_client.py">delete_organization_client</a>(organization_id, client_id) -> None</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a machine-to-machine client from an organization.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
scalekit_client.m2m_client.delete_organization_client(
    'org_123456',
    'client_123456'
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.m2m_client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/m2m_client.py">add_organization_client_secret</a>(organization_id, client_id) -> CreateOrganizationClientSecretResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Adds a new secret to an organization client.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
response = scalekit_client.m2m_client.add_organization_client_secret(
    'org_123456',
    'client_123456'
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.m2m_client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/m2m_client.py">remove_organization_client_secret</a>(organization_id, client_id, secret_id) -> None</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes a secret from an organization client.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
scalekit_client.m2m_client.remove_organization_client_secret(
    'org_123456',
    'client_123456',
    'secret_123456'
)
```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**organization_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client ID

</dd>
</dl>

<dl>
<dd>

**secret_id:** `str` - Secret ID

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

#### 📝 Description

Lists MCP server configurations with optional filters.

#### ⚙️ Parameters

**page_size**, **page_token** — Pagination.

**filter_id**, **filter_provider**, **filter_name**, **search** — Restrict or search configs.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">create_config</a>(mcp_config: McpConfig) -> CreateMcpConfigResponse</code></summary>
<dl><dd>

#### 📝 Description

Creates a configuration from a protobuf `McpConfig` message.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">update_config</a>(config_id, description?, connection_tool_mappings?) -> UpdateMcpConfigResponse</code></summary>
<dl><dd>

#### 📝 Description

Updates description and/or connector–tool mappings.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">delete_config</a>(config_id) -> DeleteMcpConfigResponse</code></summary>
<dl><dd>

#### 📝 Description

Deletes a configuration by id.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">ensure_instance</a>(name?, config_name, user_identifier) -> EnsureMcpInstanceResponse</code></summary>
<dl><dd>

#### 📝 Description

Creates or returns an MCP instance for a config and user.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">update_instance</a>(instance_id, name?, config_name?) -> UpdateMcpInstanceResponse</code></summary>
<dl><dd>

#### 📝 Description

Updates mutable fields on an instance.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">get_instance</a>(instance_id) -> GetMcpInstanceResponse</code></summary>
<dl><dd>

#### 📝 Description

Fetches one instance by id.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">list_instances</a>(page_size?, page_token?, filter_id?, filter_name?, filter_config_name?, filter_user_identifier?) -> ListMcpInstancesResponse</code></summary>
<dl><dd>

#### 📝 Description

Lists instances with optional filters.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">delete_instance</a>(instance_id) -> DeleteMcpInstanceResponse</code></summary>
<dl><dd>

#### 📝 Description

Deletes an instance.

</dd></dl>
</details>

<details><summary><code>client.mcp.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/mcp.py">get_instance_auth_state</a>(instance_id, include_auth_links?) -> GetMcpInstanceAuthStateResponse</code></summary>
<dl><dd>

#### 📝 Description

Returns authorization state for connectors used by the instance; optional fresh auth links.

</dd></dl>
</details>


## ScalekitClient

<details><summary><code>client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py">get_authorization_url</a>(redirect_uri, options?) -> str</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Utility method to generate the OAuth 2.0 authorization URL to initiate the SSO authentication flow.

This method doesn't make any network calls but instead generates a fully formed Authorization URL as a string that you can redirect your users to initiate authentication.
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
from scalekit import ScalekitClient, AuthorizationUrlOptions

# Initiate Enterprise SSO authentication for a given org_id
options = AuthorizationUrlOptions()
options.state = 'random-state-value'
options.organization_id = 'org_123456'

auth_url = scalekit_client.get_authorization_url(
    'https://yourapp.com/auth/callback',
    options
)
# Redirect user to auth_url
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

**redirect_uri:** `str` - The URL where users will be redirected after authentication. Must match one of the redirect URIs configured in your Scalekit dashboard.

</dd>
</dl>

<dl>
<dd>

**options:** `AuthorizationUrlOptions` - Optional configuration for the authorization request
- `scopes: Optional[list[str]]` - OAuth scopes to request (default: ['openid', 'profile', 'email'])
- `state: Optional[str]` - Opaque value to maintain state between request and callback
- `nonce: Optional[str]` - String value used to associate a client session with an ID Token
- `login_hint: Optional[str]` - Hint about the login identifier the user might use
- `domain_hint: Optional[str]` - Domain hint to identify which organization's IdP to use
- `connection_id: Optional[str]` - Specific SSO connection ID to use for authentication
- `organization_id: Optional[str]` - Organization ID to authenticate against
- `provider: Optional[str]` - Social login provider (e.g., 'google', 'github', 'microsoft')
- `prompt: Optional[str]` - Controls authentication behavior (e.g., 'login', 'consent', 'create')

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py">authenticate_with_code</a>(code, redirect_uri, options?) -> dict</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Exchanges an authorization code for access tokens and user information.

This method completes the OAuth 2.0 authorization code flow by exchanging the code received in the callback for access tokens, ID tokens, and user profile information. Call this method in your redirect URI handler after receiving the authorization code.
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
from scalekit import ScalekitClient

@app.get('/auth/callback')
async def auth_callback(request):
    code = request.query_params.get('code')

    result = scalekit_client.authenticate_with_code(
        code,
        'https://yourapp.com/auth/callback'
    )

    request.session['access_token'] = result['access_token']
    request.session['user'] = result['user']

    return RedirectResponse('/dashboard')
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

**code:** `str` - The authorization code received in the callback URL after user authentication

</dd>
</dl>

<dl>
<dd>

**redirect_uri:** `str` - The same redirect URI used in get_authorization_url(). Must match exactly.

</dd>
</dl>

<dl>
<dd>

**options:** `CodeAuthenticationOptions` - Optional authentication configuration
- `code_verifier: Optional[str]` - PKCE code verifier to validate the code challenge (required if PKCE was used)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py">get_idp_initiated_login_claims</a>(idp_initiated_login_token, options?) -> IdpInitiatedLoginClaims</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Extracts and validates claims from an IdP-initiated login token.

Use this method when handling IdP-initiated SSO flows, where the authentication is initiated from the identity provider's portal rather than your application. This validates the token and returns the necessary information to initiate a new SP Initiated SSO workflow.
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
@app.get('/auth/callback')
async def auth_callback(request):
    idp_initiated_login = request.query_params.get('idp_initiated_login')

    if idp_initiated_login:
        claims = scalekit_client.get_idp_initiated_login_claims(idp_initiated_login)

        options = AuthorizationUrlOptions()
        options.connection_id = claims['connection_id']
        options.organization_id = claims['organization_id']
        options.login_hint = claims.get('login_hint')
        if claims.get('relay_state'):
            options.state = claims['relay_state']

        auth_url = scalekit_client.get_authorization_url(
            'https://yourapp.com/auth/callback',
            options
        )

        return RedirectResponse(auth_url)
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

**idp_initiated_login_token:** `str` - The token received in the 'idp_initiated_login' query parameter

</dd>
</dl>

<dl>
<dd>

**options:** `TokenValidationOptions` - Optional token validation configuration

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py">validate_access_token</a>(token, options?) -> bool</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Validates the access token and returns a boolean result.
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
is_valid = scalekit_client.validate_access_token(token)
if is_valid:
    # Token is valid, proceed with request
    pass
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

**token:** `str` - The token to be validated

</dd>
</dl>

<dl>
<dd>

**options:** `TokenValidationOptions` - Optional validation options for issuer, audience, and scopes

`options.issuer` accepts a `str` or a `List[str]`. With a list, the token is valid if its `iss` claim exactly equals any entry, e.g. `TokenValidationOptions(issuer=[env_url, f"{env_url}/resources/res_123"])`. An unset, empty-string or empty-list issuer skips the issuer check.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py">get_logout_url</a>(options?) -> str</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the logout URL that can be used to log out the user.
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
options = LogoutUrlOptions()
options.post_logout_redirect_uri = 'https://example.com'
options.state = 'some-state'

logout_url = scalekit_client.get_logout_url(options)
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

**options:** `LogoutUrlOptions` - Logout URL options
- `id_token_hint: Optional[str]` - The ID Token previously issued to the client
- `post_logout_redirect_uri: Optional[str]` - URL to redirect after logout
- `state: Optional[str]` - Opaque value to maintain state between request and callback

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py">verify_webhook_payload</a>(secret, headers, payload) -> bool</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Verifies the webhook payload signature using the provided secret.
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
@app.post('/webhooks')
async def webhook_handler(request):
    payload = await request.body()
    headers = dict(request.headers)

    is_valid = scalekit_client.verify_webhook_payload(
        'your_webhook_secret',
        headers,
        payload
    )

    if is_valid:
        # Process webhook
        pass
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

**secret:** `str` - Secret for webhook verification

</dd>
</dl>

<dl>
<dd>

**headers:** `Dict[str, str]` - Webhook request headers

</dd>
</dl>

<dl>
<dd>

**payload:** `str | bytes` - Webhook payload in str or bytes

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">verify_event</a>(body, /, *, headers, secret) -> TriggerEvent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Verifies a trigger event's signature (`whsec_` secret, `v1` HMAC-SHA256, five-minute timestamp window, case-insensitive header names), then parses the body into an immutable `TriggerEvent`. Also available without a client as `scalekit.verify_trigger_event(body, /, *, headers, secret)`. `occurred_at` is a timezone-aware UTC `datetime`; fractional seconds are truncated to microseconds. Raises `WebhookVerificationError` on any verification failure; a correctly signed but malformed event raises its subclass `ScalekitTriggerEventParseException`. Raises `TypeError` when called with arguments of the wrong type. Delivery is at least once: deduplicate on `dedupe_key` plus the connected account you act as. Full example: [AGENTKIT.md → Trigger events](AGENTKIT.md#trigger-events).
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
from scalekit import DeliveryScope, PayloadState
from scalekit.common.exceptions import WebhookVerificationError

try:
    event = scalekit_client.actions.triggers.verify_event(
        request.get_data(),  # raw body
        headers=request.headers,
        secret=os.environ["SCALEKIT_TRIGGER_SECRET"],
    )
except WebhookVerificationError:  # bad signature, stale timestamp or malformed event
    return "", 400

if event.payload_state == PayloadState.REFERENCE:
    print("fetch", event.resource_type, event.resource_id)  # payload is None
if event.delivery_scope == DeliveryScope.ACCOUNT:
    print("one connected account:", event.connected_account_id, event.dedupe_key)
elif event.delivery_scope == DeliveryScope.CONNECTION:
    print("whole connection:", event.connection_id, event.dedupe_key)  # connected_account_id == ""
else:
    print("unknown delivery scope, skipped:", event.delivery_scope)  # added after this SDK version
return "", 204
```

Full Flask handler with deduplication: [AGENTKIT.md → Trigger events](AGENTKIT.md#trigger-events).
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**body:** `str | bytes` - The raw request body (positional only)

</dd>
</dl>

<dl>
<dd>

**headers:** `HeadersLike` - The request headers (keyword only): `request.headers` from Flask/Werkzeug, Starlette/FastAPI or Django, or a `dict`/`Mapping`

</dd>
</dl>

<dl>
<dd>

**secret:** `str` - The trigger signing secret, starting with `whsec_` (keyword only)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/client.py">refresh_access_token</a>(refresh_token) -> dict</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Refreshes an access token using a refresh token.
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
result = scalekit_client.refresh_access_token(refresh_token)
new_access_token = result['access_token']
new_refresh_token = result['refresh_token']
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

**refresh_token:** `str` - Refresh token to get new access token

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Organization

<details><summary><code>client.organization.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/organization.py">list_organizations</a>(page_size, page_token?) -> ListOrganizationsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all organizations with pagination support.
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
response = scalekit_client.organization.list_organizations(
    page_size=50,
    page_token='next_page_token'
)

for org in response[0].organizations:
    print(f"Organization: {org.display_name}")
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

**page_size:** `int` - Page size for organization list fetch

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

<details><summary><code>client.organization.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/organization.py">create_organization</a>(organization) -> CreateOrganizationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new organization with the provided details.
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
from scalekit.v1.organizations.organizations_pb2 import CreateOrganization

org = CreateOrganization()
org.display_name = "Acme Corp"
org.external_id = "acme_123"

response = scalekit_client.organization.create_organization(org)
print(f"Created organization: {response[0].organization.id}")
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

**organization:** `CreateOrganization` - Organization object with details for creation

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.organization.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/organization.py">get_organization</a>(organization_id) -> GetOrganizationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves organization details by organization ID.
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
response = scalekit_client.organization.get_organization('org_123456')
organization = response[0].organization
print(f"Organization: {organization.display_name}")
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
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.organization.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/organization.py">get_organization_by_external_id</a>(external_id) -> GetOrganizationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves organization details by external ID.
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
response = scalekit_client.organization.get_organization_by_external_id('acme_123')
organization = response[0].organization
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

**external_id:** `str` - External ID to fetch organization details

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.organization.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/organization.py">update_organization</a>(organization_id, organization) -> UpdateOrganizationResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing organization with new information.
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
from scalekit.v1.organizations.organizations_pb2 import UpdateOrganization

org = UpdateOrganization()
org.display_name = "Acme Corporation"

response = scalekit_client.organization.update_organization('org_123456', org)
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

**organization_id:** `str` - Organization ID to update

</dd>
</dl>

<dl>
<dd>

**organization:** `UpdateOrganization` - Parameters for update organization operation

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.organization.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/organization.py">delete_organization</a>(organization_id)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes an organization by organization ID.
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
scalekit_client.organization.delete_organization('org_123456')
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
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.organization.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/organization.py">generate_portal_link</a>(organization_id, features?) -> str</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a customer portal link for the organization.
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
portal_link = scalekit_client.organization.generate_portal_link('org_123456')
print(f"Portal Link: {portal_link}")
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

**organization_id:** `str` - Organization ID to fetch portal link for

</dd>
</dl>

<dl>
<dd>

**features:** `Optional[list[Feature]]` - Feature list to generate portal link for

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Connection

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">list_connections</a>(organization_id, include?) -> ListConnectionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all SSO connections for an organization.
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
response = scalekit_client.connection.list_connections(
    'org_123456',
    include='all'
)

for conn in response[0].connections:
    print(f"Connection: {conn.id}")
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

**organization_id:** `str` - Organization ID to get connections

</dd>
</dl>

<dl>
<dd>

**include:** `Optional[str]` - Return active connections or all (e.g., 'all')

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">list_connections_by_domain</a>(domain, include?) -> ListConnectionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all SSO connections for a domain.
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
response = scalekit_client.connection.list_connections_by_domain(
    'acme.com',
    include='all'
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

**domain:** `str` - Domain to get connections

</dd>
</dl>

<dl>
<dd>

**include:** `Optional[str]` - Return active connections or all

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">get_connection</a>(organization_id, conn_id) -> GetConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a specific SSO connection by ID.
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
response = scalekit_client.connection.get_connection(
    'org_123456',
    'conn_123456'
)
connection = response[0].connection
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

**conn_id:** `str` - Connection ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">create_connection</a>(organization_id, connection) -> CreateConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new SSO connection for an organization.
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
from scalekit.v1.connections.connections_pb2 import CreateConnection

connection = CreateConnection()
connection.type = "SAML"

response = scalekit_client.connection.create_connection(
    'org_123456',
    connection
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

**connection:** `CreateConnection` - Connection object with expected values

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">enable_connection</a>(organization_id, conn_id) -> ToggleConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Enables an SSO connection for an organization.
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
scalekit_client.connection.enable_connection('org_123456', 'conn_123456')
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

**conn_id:** `str` - Connection ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">disable_connection</a>(organization_id, conn_id) -> ToggleConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Disables an SSO connection for an organization.
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
scalekit_client.connection.disable_connection('org_123456', 'conn_123456')
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

**conn_id:** `str` - Connection ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">delete_connection</a>(organization_id, connection_id)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes an SSO connection from an organization.
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
scalekit_client.connection.delete_connection('org_123456', 'conn_123456')
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

**connection_id:** `str` - Connection ID to be deleted

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">list_app_connections</a>(page_size?, page_token?, provider?, query?) -> ListAppConnectionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all environment-level app connections. These are connections configured at the environment level (not tied to a specific organization), such as OAuth integrations (e.g., HubSpot) or Google Domain-Wide Delegation connections.
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
# List all app connections
response = scalekit_client.connection.list_app_connections()

for conn in response[0].connections:
    print(f"Connection: {conn.id}, Provider: {conn.provider_key}")

# Filter by provider
response = scalekit_client.connection.list_app_connections(provider='HUBSPOT', page_size=10)

# Free-text search across app connections
response = scalekit_client.connection.list_app_connections(query='hubspot')
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

**page_size:** `Optional[int]` - Maximum number of connections to return (max 30)

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Pagination token from a previous response

</dd>
</dl>

<dl>
<dd>

**provider:** `Optional[str]` - Filter by provider key (e.g., `'HUBSPOT'`, `'GOOGLEDWD'`)

</dd>
</dl>

<dl>
<dd>

**query:** `Optional[str]` - Free-text search that matches app connections by connection name (key ID) or provider. Must be 3-100 characters.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">get_environment_connection</a>(connection_id) -> GetConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves an environment-level connection by its ID.

`connection.resolved_proxy_url` is the URL the connector's templated `proxy_url` was resolved to when the connection was created (see `create_environment_connection`); it is not set when the connector's `proxy_url` has no template, or when the connection is older than the field. For an OAuth connection, `connection.oauth_config.token_endpoint_auth_type` is not set while the connection uses the Default, where Scalekit picks the method per request (see `update_environment_connection`).
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
response = scalekit_client.connection.get_environment_connection('conn_123456')
conn = response[0].connection
print(f"Provider: {conn.provider_key}, Type: {conn.type}")
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

**connection_id:** `str` - The ID of the environment-level connection to retrieve

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">create_environment_connection</a>(connection, flags?) -> CreateConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new environment-level connection. Supports OAuth connections (e.g., HubSpot) and Google Domain-Wide Delegation (GOOGLE_DWD) connections. Pass `Flags(is_app=True)` to mark the connection as an app-level integration.

A connector whose `proxy_url` is a template with `{{domain}}` or `{{version}}` placeholders, for example an MCP connector with a host per data region, is resolved once, when the connection is created. Put the values in `CreateConnection.context`. The context itself is not stored; the resolved URL is, and `connection.resolved_proxy_url` in the response shows it. If the template needs a value the context does not supply, the call fails with 400 (`connection context is missing a value required by provider ... proxy_url template`).
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
from scalekit.v1.connections.connections_pb2 import (
    CreateConnection, ConnectionType, Flags
)

# Create an OAuth app connection (e.g., HubSpot)
response = scalekit_client.connection.create_environment_connection(
    connection=CreateConnection(
        provider_key='HUBSPOT',
        type=ConnectionType.OAUTH
    ),
    flags=Flags(is_app=True)
)
conn = response[0].connection
print(f"Created: {conn.id}, Key: {conn.key_id}")

# Create a Google Domain-Wide Delegation connection
response = scalekit_client.connection.create_environment_connection(
    connection=CreateConnection(
        provider_key='GOOGLEDWD',
        type=ConnectionType.GOOGLE_DWD,
        key_id='my-gdwd-connection'
    ),
    flags=Flags(is_app=True)
)
```

For a connector with a templated `proxy_url`, pass the values it needs as `context`:

```python
from google.protobuf import struct_pb2

context = struct_pb2.Struct()
context.update({'domain': 'mcp-eu.example.com'})

response = scalekit_client.connection.create_environment_connection(
    connection=CreateConnection(
        provider_key=provider.identifier,  # Provider.identifier of the custom connector
        type=ConnectionType.OAUTH,
        context=context
    ),
    flags=Flags(is_app=True)
)
print(response[0].connection.resolved_proxy_url)
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

**connection:** `CreateConnection` - Connection configuration object
- `provider_key: str` - Provider identifier (e.g., `'HUBSPOT'`, `'GOOGLEDWD'`)
- `type: ConnectionType` - Connection type (`ConnectionType.OAUTH` or `ConnectionType.GOOGLE_DWD`)
- `key_id: Optional[str]` - Unique key identifier for the connection (required for GOOGLE_DWD)
- `context: Optional[google.protobuf.Struct]` - Values that resolve the connector's templated `proxy_url`, once, at creation. Only `domain` and `version` are recognized, and any other key is rejected with 400. `domain` is the actual host name that replaces `{{domain}}`, not a region code; `version` replaces `{{version}}`.

</dd>
</dl>

<dl>
<dd>

**flags:** `Optional[Flags]` - Connection flags
- `is_app: bool` - Set to `True` to create an environment-level app connection

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.connection.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connection.py">update_environment_connection</a>(connection_id, connection) -> UpdateConnectionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an environment-level connection. This is a PATCH operation — only fields provided in the `UpdateConnection` object are changed; unspecified fields remain unchanged. Always include the `type` field to avoid server-side errors.

To choose how Scalekit authenticates to an OAuth connection's token endpoint, set `oauth_config.token_endpoint_auth_type` to a `TokenAuthType`:

| `TokenAuthType` | Sent to the token endpoint |
|-----------------|----------------------------|
| `BASIC_AUTH` | `client_id` and `client_secret` in an HTTP Basic `Authorization` header (`client_secret_basic`) |
| `URL_PARAMS` | `client_id` and `client_secret` as POST body parameters (`client_secret_post`) |
| `NONE` | Only the `client_id`, for public (PKCE) clients. Rejected on an OIDC connection. |

Leave the field unset to keep the current value, and send `TOKEN_AUTH_TYPE_UNSPECIFIED` to reset it to the Default, where Scalekit picks the method per request. It applies to the authorization_code exchange, MCP token refresh and `OAUTH_M2M` client_credentials; refreshing a token on a non-MCP OAuth connection always detects the method itself. Set it only when the provider's token endpoint documentation requires a specific method: a wrong value makes token exchange or refresh fail, and every connected account on the connection then has to authenticate again.

`oauth_config.token_endpoint_auth_method`, a string (`"client_secret_basic"`, `"client_secret_post"` or `"none"`), is deprecated. It maps onto the same stored value, and the server rejects any other non-empty string. Send one of the two fields: when both are sent with different values, the request is rejected unless one of them equals the stored value.
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
from scalekit.v1.connections.connections_pb2 import (
    UpdateConnection, ConnectionType, OAuthConnectionConfig, GoogleDWDConfig, TokenAuthType
)

# Update OAuth connection credentials
response = scalekit_client.connection.update_environment_connection(
    connection_id='conn_123456',
    connection=UpdateConnection(
        provider_key='HUBSPOT',
        key_id='hubspot-key',
        type=ConnectionType.OAUTH,
        oauth_config=OAuthConnectionConfig(
            client_id={'value': 'my-client-id'},
            client_secret={'value': 'my-client-secret'}
        )
    )
)

# Send the client credentials in the request body (client_secret_post)
response = scalekit_client.connection.update_environment_connection(
    connection_id='conn_123456',
    connection=UpdateConnection(
        provider_key='HUBSPOT',
        key_id='hubspot-key',
        type=ConnectionType.OAUTH,
        oauth_config=OAuthConnectionConfig(
            token_endpoint_auth_type=TokenAuthType.URL_PARAMS
        )
    )
)

# Update Google DWD connection
response = scalekit_client.connection.update_environment_connection(
    connection_id='conn_123456',
    connection=UpdateConnection(
        provider_key='GOOGLEDWD',
        key_id='my-gdwd-connection',
        type=ConnectionType.GOOGLE_DWD,
        google_dwd_config=GoogleDWDConfig(
            service_account_json={'value': '{"type":"service_account",...}'},
            scopes=['https://www.googleapis.com/auth/admin.directory.user.readonly'],
            token_uri={'value': 'https://oauth2.googleapis.com/token'}
        )
    )
)
conn = response[0].connection
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

**connection_id:** `str` - The ID of the environment-level connection to update

</dd>
</dl>

<dl>
<dd>

**connection:** `UpdateConnection` - Fields to update on the connection
- `provider_key: str` - Provider identifier (e.g., `'HUBSPOT'`, `'GOOGLEDWD'`)
- `key_id: str` - Key identifier of the connection
- `type: ConnectionType` - Connection type — must always be provided (`ConnectionType.OAUTH` or `ConnectionType.GOOGLE_DWD`)
- `oauth_config: Optional[OAuthConnectionConfig]` - OAuth settings to update (`client_id`, `client_secret`, `token_endpoint_auth_type`)
- `google_dwd_config: Optional[GoogleDWDConfig]` - Google DWD config to update (`service_account_json`, `scopes`, `token_uri`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Domain

<details><summary><code>client.domain.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/domain.py">create_domain</a>(organization_id, domain_name, domain_type?) -> CreateDomainResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new domain for an organization.
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
response = scalekit_client.domain.create_domain(
    'org_123456',
    'acme.com',
    domain_type='ORGANIZATION_DOMAIN'
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

**organization_id:** `str` - Organization ID to create domain for

</dd>
</dl>

<dl>
<dd>

**domain_name:** `str` - Domain name for new creation

</dd>
</dl>

<dl>
<dd>

**domain_type:** `Optional[str | DomainType]` - Type of domain ("ALLOWED_EMAIL_DOMAIN", "ORGANIZATION_DOMAIN", or "UNSPECIFIED")

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.domain.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/domain.py">list_domains</a>(organization_id, domain_type?) -> ListDomainResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all domains for an organization.
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
response = scalekit_client.domain.list_domains(
    'org_123456',
    domain_type='ORGANIZATION_DOMAIN'
)

for domain in response[0].domains:
    print(f"Domain: {domain.domain}")
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

**organization_id:** `str` - Organization ID to list domains for

</dd>
</dl>

<dl>
<dd>

**domain_type:** `Optional[str | DomainType]` - Type of domain to filter by

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.domain.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/domain.py">get_domain</a>(organization_id, domain_id) -> GetDomainResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a specific domain by ID.
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
response = scalekit_client.domain.get_domain('org_123456', 'domain_123456')
domain = response[0].domain
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

**domain_id:** `str` - Domain ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.domain.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/domain.py">delete_domain</a>(organization_id, domain_id)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a domain from an organization.
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
scalekit_client.domain.delete_domain('org_123456', 'domain_123456')
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

**domain_id:** `str` - Domain ID to delete

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Directory

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">list_directories</a>(organization_id) -> ListDirectoriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all directories for an organization.
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
response = scalekit_client.directory.list_directories('org_123456')

for directory in response[0].directories:
    print(f"Directory: {directory.id}")
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

**organization_id:** `str` - Organization ID to fetch directory list

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">get_directory</a>(organization_id, directory_id) -> GetDirectoryResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a specific directory by ID.
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
response = scalekit_client.directory.get_directory(
    'org_123456',
    'directory_123456'
)
directory = response[0].directory
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

**directory_id:** `str` - Directory ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">create_directory</a>(organization_id, directory) -> CreateDirectoryResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new directory for an organization.
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
from scalekit.v1.directories.directories_pb2 import CreateDirectory

directory = CreateDirectory()
directory.provider = "azure"

response = scalekit_client.directory.create_directory(
    'org_123456',
    directory
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

**organization_id:** `str` - Organization ID to create directory for

</dd>
</dl>

<dl>
<dd>

**directory:** `CreateDirectory` - Directory object with expected values for creation

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">list_directory_users</a>(organization_id, directory_id, page_size?, page_token?, include_detail?, updated_after?) -> tuple[ListDirUsersResponse, Any]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all users in a directory with pagination support.
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
response = scalekit_client.directory.list_directory_users(
    'org_123456',
    'directory_123456',
    page_size=50
)

for user in response[0].users:
    print(f"User: {user.email}")
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

**directory_id:** `str` - Directory ID

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Page size for pagination

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Page token for pagination

</dd>
</dl>

<dl>
<dd>

**include_detail:** `Optional[bool]` - Include detailed data

</dd>
</dl>

<dl>
<dd>

**updated_after:** `Optional[str]` - Get updated after detail

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">list_directory_groups</a>(organization_id, directory_id, page_size?, page_token?, include_detail?, updated_after?) -> tuple[ListDirGroupsResponse, Any]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all groups in a directory with pagination support.
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
response = scalekit_client.directory.list_directory_groups(
    'org_123456',
    'directory_123456',
    page_size=50
)

for group in response[0].groups:
    print(f"Group: {group.display_name}")
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

**directory_id:** `str` - Directory ID

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Page size for pagination

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Page token for pagination

</dd>
</dl>

<dl>
<dd>

**include_detail:** `Optional[bool]` - Include detailed data

</dd>
</dl>

<dl>
<dd>

**updated_after:** `Optional[str]` - Get updated after detail

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">enable_directory</a>(organization_id, directory_id) -> ToggleDirectoryResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Enables a directory for an organization.
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
scalekit_client.directory.enable_directory('org_123456', 'directory_123456')
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

**directory_id:** `str` - Directory ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">disable_directory</a>(organization_id, directory_id) -> ToggleDirectoryResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Disables a directory for an organization.
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
scalekit_client.directory.disable_directory('org_123456', 'directory_123456')
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

**directory_id:** `str` - Directory ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.directory.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/directory.py">delete_directory</a>(organization_id, directory_id)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a directory from an organization.
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
scalekit_client.directory.delete_directory('org_123456', 'directory_123456')
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

**directory_id:** `str` - Directory ID for directory to be deleted

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## User

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">list_users</a>(page_size?, page_token?) -> ListUsersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all users in the environment with pagination support.
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
response = scalekit_client.users.list_users(
    page_size=50,
    page_token='next_page_token'
)

for user in response[0].users:
    print(f"User: {user.email}")
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

**page_size:** `Optional[int]` - Page size for pagination

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

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">list_organization_users</a>(organization_id, page_size?, page_token?) -> ListOrganizationUsersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all users in a specific organization with pagination support.
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
response = scalekit_client.users.list_organization_users(
    'org_123456',
    page_size=50
)

for user in response[0].users:
    print(f"User: {user.email}")
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

**organization_id:** `str` - Organization ID to list users for

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Page size for pagination

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

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">get_user</a>(user_id) -> GetUserResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves user details by user ID.
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
response = scalekit_client.users.get_user('usr_123456')
user = response[0].user
print(f"User: {user.email}")
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

**user_id:** `str` - User ID to get user details

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">get_user_by_external_id</a>(external_id) -> GetUserResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves user details by external ID.
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
response = scalekit_client.users.get_user_by_external_id('external_123')
user = response[0].user
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

**external_id:** `str` - External ID to get user details

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">create_user_and_membership</a>(organization_id, user, send_invitation_email?) -> CreateUserAndMembershipResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new user and adds them to an organization.
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
from scalekit.v1.users.users_pb2 import CreateUser

user = CreateUser()
user.email = "john.doe@example.com"
user.given_name = "John"
user.family_name = "Doe"

response = scalekit_client.users.create_user_and_membership(
    'org_123456',
    user,
    send_invitation_email=True
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

**organization_id:** `str` - Organization ID to create user for

</dd>
</dl>

<dl>
<dd>

**user:** `CreateUser` - User object with expected values for user creation

</dd>
</dl>

<dl>
<dd>

**send_invitation_email:** `bool` - Whether to send invitation email to the user (default: True)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">update_user</a>(user_id, user) -> UpdateUserResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing user by user ID.
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
from scalekit.v1.users.users_pb2 import UpdateUser

user = UpdateUser()
user.given_name = "John"

response = scalekit_client.users.update_user('usr_123456', user)
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

**user_id:** `str` - User ID to update

</dd>
</dl>

<dl>
<dd>

**user:** `UpdateUser` - User object with expected values for user update

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">delete_user</a>(user_id)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a user by user ID.
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
scalekit_client.users.delete_user('usr_123456')
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

**user_id:** `str` - User ID to be deleted

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">create_membership</a>(organization_id, user_id, membership, send_invitation_email?) -> CreateMembershipResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a membership for a user in an organization.
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
from scalekit.v1.users.users_pb2 import CreateMembership

membership = CreateMembership()

response = scalekit_client.users.create_membership(
    'org_123456',
    'usr_123456',
    membership,
    send_invitation_email=True
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

**user_id:** `str` - User ID

</dd>
</dl>

<dl>
<dd>

**membership:** `CreateMembership` - Membership object

</dd>
</dl>

<dl>
<dd>

**send_invitation_email:** `bool` - Whether to send invitation email (default: True)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">update_membership</a>(organization_id, user_id, membership) -> UpdateMembershipResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a membership for a user in an organization.
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
from scalekit.v1.users.users_pb2 import UpdateMembership

membership = UpdateMembership()

response = scalekit_client.users.update_membership(
    'org_123456',
    'usr_123456',
    membership
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

**user_id:** `str` - User ID

</dd>
</dl>

<dl>
<dd>

**membership:** `UpdateMembership` - Membership object

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">delete_membership</a>(organization_id, user_id)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a membership for a user in an organization.
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
scalekit_client.users.delete_membership('org_123456', 'usr_123456')
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

**user_id:** `str` - User ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.users.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/users.py">resend_invite</a>(organization_id, user_id) -> ResendInviteResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Resends an invitation email to a user who has a pending invitation.
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
response = scalekit_client.users.resend_invite('org_123456', 'usr_123456')
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

**organization_id:** `str` - Organization ID containing the pending invitation

</dd>
</dl>

<dl>
<dd>

**user_id:** `str` - User ID who has a pending invitation

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Role

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">list_roles</a>() -> ListRolesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all roles in the environment.
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
response = scalekit_client.roles.list_roles()

for role in response[0].roles:
    print(f"Role: {role.name}")
```
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">get_role</a>(role_name) -> GetRoleResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves role details by role name.
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
response = scalekit_client.roles.get_role('admin')
role = response[0].role
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

**role_name:** `str` - Role name to get role details

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">create_role</a>(role) -> CreateRoleResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new role.
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
from scalekit.v1.roles.roles_pb2 import CreateRole

role = CreateRole()
role.name = "editor"
role.display_name = "Editor"

response = scalekit_client.roles.create_role(role)
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

**role:** `CreateRole` - Role object with expected values for role creation

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">update_role</a>(role_name, role) -> UpdateRoleResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing role by name.
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
from scalekit.v1.roles.roles_pb2 import UpdateRole

role = UpdateRole()
role.display_name = "Senior Editor"

response = scalekit_client.roles.update_role('editor', role)
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

**role_name:** `str` - Role name to update

</dd>
</dl>

<dl>
<dd>

**role:** `UpdateRole` - Role object with expected values for role update

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">delete_role</a>(role_name, reassign_role_name?)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a role by name.
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
scalekit_client.roles.delete_role('editor', reassign_role_name='viewer')
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

**role_name:** `str` - Role name to be deleted

</dd>
</dl>

<dl>
<dd>

**reassign_role_name:** `Optional[str]` - Role name to reassign users to when deleting this role

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">get_role_users_count</a>(role_name) -> GetRoleUsersCountResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets the count of users associated with a role.
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
response = scalekit_client.roles.get_role_users_count('admin')
print(f"User count: {response[0].count}")
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

**role_name:** `str` - Role name to get user count for

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">list_organization_roles</a>(org_id) -> ListOrganizationRolesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all organization-specific roles.
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
response = scalekit_client.roles.list_organization_roles('org_123456')

for role in response[0].roles:
    print(f"Role: {role.name}")
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

**org_id:** `str` - Organization ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">create_organization_role</a>(org_id, role) -> CreateOrganizationRoleResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new organization-specific role.
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
from scalekit.v1.roles.roles_pb2 import CreateOrganizationRole

role = CreateOrganizationRole()
role.name = "org_admin"
role.display_name = "Organization Admin"

response = scalekit_client.roles.create_organization_role('org_123456', role)
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

**org_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**role:** `CreateOrganizationRole` - Role object with expected values

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">get_organization_role</a>(org_id, role_name) -> GetOrganizationRoleResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves organization-specific role details by name.
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
response = scalekit_client.roles.get_organization_role('org_123456', 'org_admin')
role = response[0].role
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

**org_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**role_name:** `str` - Role name to get role details

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">update_organization_role</a>(org_id, role_name, role) -> UpdateOrganizationRoleResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing organization-specific role.
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
from scalekit.v1.roles.roles_pb2 import UpdateRole

role = UpdateRole()
role.display_name = "Organization Administrator"

response = scalekit_client.roles.update_organization_role(
    'org_123456',
    'org_admin',
    role
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

**org_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**role_name:** `str` - Role name to update

</dd>
</dl>

<dl>
<dd>

**role:** `UpdateRole` - Role object with expected values

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.roles.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/role.py">delete_organization_role</a>(org_id, role_name, reassign_role_name?)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes an organization-specific role.
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
scalekit_client.roles.delete_organization_role(
    'org_123456',
    'org_admin',
    reassign_role_name='member'
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

**org_id:** `str` - Organization ID

</dd>
</dl>

<dl>
<dd>

**role_name:** `str` - Role name to be deleted

</dd>
</dl>

<dl>
<dd>

**reassign_role_name:** `Optional[str]` - Role name to reassign users to

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Permission

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">list_permissions</a>(page_token?, page_size?) -> ListPermissionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all permissions with pagination support.
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
response = scalekit_client.permissions.list_permissions(
    page_size=50
)

for permission in response[0].permissions:
    print(f"Permission: {permission.name}")
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

**page_token:** `Optional[str]` - Token for pagination

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Number of permissions per page

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">get_permission</a>(permission_name) -> GetPermissionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves permission details by permission name.
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
response = scalekit_client.permissions.get_permission('write:articles')
permission = response[0].permission
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

**permission_name:** `str` - Permission name to get permission details

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">create_permission</a>(permission) -> CreatePermissionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new permission.
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
from scalekit.v1.roles.roles_pb2 import CreatePermission

permission = CreatePermission()
permission.name = "write:articles"
permission.description = "Permission to write articles"

response = scalekit_client.permissions.create_permission(permission)
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

**permission:** `CreatePermission` - Permission object with expected values

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">update_permission</a>(permission_name, permission) -> UpdatePermissionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates an existing permission by name.
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
from scalekit.v1.roles.roles_pb2 import CreatePermission

permission = CreatePermission()
permission.description = "Updated description"

response = scalekit_client.permissions.update_permission(
    'write:articles',
    permission
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

**permission_name:** `str` - Permission name to update

</dd>
</dl>

<dl>
<dd>

**permission:** `CreatePermission` - Permission object with expected values

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">delete_permission</a>(permission_name)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a permission by name.
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
scalekit_client.permissions.delete_permission('write:articles')
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

**permission_name:** `str` - Permission name to be deleted

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">list_role_permissions</a>(role_name) -> ListRolePermissionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all permissions associated with a role.
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
response = scalekit_client.permissions.list_role_permissions('editor')

for permission in response[0].permissions:
    print(f"Permission: {permission.name}")
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

**role_name:** `str` - Role name to get permissions for

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">add_permissions_to_role</a>(role_name, permission_names)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Adds permissions to a role.
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
scalekit_client.permissions.add_permissions_to_role(
    'editor',
    ['write:articles', 'edit:articles']
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

**role_name:** `str` - Role name to add permissions to

</dd>
</dl>

<dl>
<dd>

**permission_names:** `list[str]` - List of permission names to add

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">remove_permission_from_role</a>(role_name, permission_name)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes a permission from a role.
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
scalekit_client.permissions.remove_permission_from_role(
    'editor',
    'write:articles'
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

**role_name:** `str` - Role name to remove permission from

</dd>
</dl>

<dl>
<dd>

**permission_name:** `str` - Permission name to remove

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.permissions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/permissions.py">list_effective_role_permissions</a>(role_name) -> ListEffectiveRolePermissionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all effective permissions for a role including both direct and inherited permissions.

This returns the complete set of capabilities available through the role hierarchy.
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
response = scalekit_client.permissions.list_effective_role_permissions('senior_editor')

print(f'Total effective permissions: {len(response[0].permissions)}')
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

**role_name:** `str` - Role to analyze

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Passwordless

<details><summary><code>client.passwordless.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/passwordless.py">send_passwordless_email</a>(email, template?, magiclink_auth_uri?, state?, expires_in?, template_variables?) -> SendPasswordlessResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Send a passwordless authentication email with OTP or magic link.
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
response = scalekit_client.passwordless.send_passwordless_email(
    'user@example.com',
    template='SIGNIN',
    state='random-state',
    expires_in=3600
)

print(f'Auth Request ID: {response[0].auth_request_id}')
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

**email:** `str` - The email address to send the passwordless link to

</dd>
</dl>

<dl>
<dd>

**template:** `Optional[str | TemplateType]` - The template type (SIGNIN/SIGNUP)

</dd>
</dl>

<dl>
<dd>

**magiclink_auth_uri:** `Optional[str]` - Optional auth URI for magic link

</dd>
</dl>

<dl>
<dd>

**state:** `Optional[str]` - Optional state parameter

</dd>
</dl>

<dl>
<dd>

**expires_in:** `Optional[int]` - Optional expiration time in seconds (default: 300)

</dd>
</dl>

<dl>
<dd>

**template_variables:** `Optional[Dict[str, str]]` - Optional template variables

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.passwordless.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/passwordless.py">verify_passwordless_email</a>(code?, link_token?, auth_request_id?) -> VerifyPasswordLessResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Verify a passwordless authentication code or link token.
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
response = scalekit_client.passwordless.verify_passwordless_email(
    code='123456',
    auth_request_id='auth_request_id'
)

print(f'Email: {response[0].email}')
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

**code:** `Optional[str]` - The one-time code received via email

</dd>
</dl>

<dl>
<dd>

**link_token:** `Optional[str]` - The link token received via email

</dd>
</dl>

<dl>
<dd>

**auth_request_id:** `Optional[str]` - Optional auth request ID from the send response

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.passwordless.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/passwordless.py">resend_passwordless_email</a>(auth_request_id) -> SendPasswordlessResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Resend a passwordless authentication email.
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
response = scalekit_client.passwordless.resend_passwordless_email('auth_request_id')
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

**auth_request_id:** `str` - The auth request ID from the original send response

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## WebAuthn

<details><summary><code>client.webauthn.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/webauthn.py">list_credentials</a>(user_id) -> ListCredentialsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all WebAuthn credentials for a user.
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
response = scalekit_client.webauthn.list_credentials('usr_123456')
print(f'Credentials: {response[0].credentials}')
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

**user_id:** `str` - The user ID to list credentials for

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webauthn.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/webauthn.py">update_credential</a>(credential_id, display_name) -> UpdateCredentialResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update a WebAuthn credential's display name.
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
response = scalekit_client.webauthn.update_credential(
    'cred_123',
    'My YubiKey'
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

**credential_id:** `str` - The credential ID to update

</dd>
</dl>

<dl>
<dd>

**display_name:** `str` - The new display name for the credential

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webauthn.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/webauthn.py">delete_credential</a>(credential_id) -> DeleteCredentialResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a WebAuthn credential.
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
response = scalekit_client.webauthn.delete_credential('cred_123')
print(f'Deleted: {response[0].success}')
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

**credential_id:** `str` - The credential ID to delete

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Auth

<details><summary><code>client.auth.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/auth.py">update_login_user_details</a>(connection_id, login_request_id, user?) -> UpdateLoginUserDetailsResponse</code></summary>
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
response = scalekit_client.auth.update_login_user_details(
    'conn_abc123',
    'login_xyz789',
    {
        'email': 'john.doe@company.com',
        'sub': 'unique_user_id_456',
    }
)
print(response[0].auth_request_id)
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

## Events

<details><summary><code>client.events.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/events.py">list_events_paginated</a>(page_size?, page_token?, filter?) -> ListEventsPaginatedResponse</code></summary>
<dl>
<dd>

### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists events with pagination, optionally narrowing results with an event filter.
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
response = scalekit_client.events.list_events_paginated(
    page_size=10,
    page_token=''
)
for event in response[0].events:
    print(event)
print(response[0].next_page_token)
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

**page_size:** `Optional[int]` - Page size for the events list fetch (uses server default if not provided)

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Page token for fetching the next page of events

</dd>
</dl>

<dl>
<dd>

**filter:** `Optional[EventFilter]` - Filter to narrow the events returned

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Sessions

<details><summary><code>client.sessions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/sessions.py">get_session</a>(session_id) -> SessionDetails</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves session details by session ID.
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
response = scalekit_client.sessions.get_session('session_123456')
session = response[0]
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

**session_id:** `str` - Session ID to get session details

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.sessions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/sessions.py">get_user_sessions</a>(user_id, page_size?, page_token?, filter?) -> UserSessionDetails</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves all session details for a user with pagination and filtering support.
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
response = scalekit_client.sessions.get_user_sessions(
    'usr_123456',
    page_size=50
)

for session in response[0].sessions:
    print(f'Session: {session.session_id}')
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

**user_id:** `str` - User ID to get all session details for

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Number of sessions to return per page

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Token for pagination

</dd>
</dl>

<dl>
<dd>

**filter:** `Optional[UserSessionFilter]` - Filter to apply to sessions (status, time range)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.sessions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/sessions.py">revoke_session</a>(session_id) -> RevokeSessionResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Revokes a session for a user.
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
response = scalekit_client.sessions.revoke_session('session_123456')
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

**session_id:** `str` - Session ID to revoke

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.sessions.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/sessions.py">revoke_all_user_sessions</a>(user_id) -> RevokeAllUserSessionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Revokes all sessions for a user.
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
response = scalekit_client.sessions.revoke_all_user_sessions('usr_123456')
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

**user_id:** `str` - User ID to revoke all sessions for

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
    print(f'Client: {client.client_id}')
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

## Resources

Manage the resource clients scoped to a resource (such as an MCP server), and access the consents your end users grant against one. A consent records that one end user allowed a specific resource client to act on their behalf. Each consent identifies the user by `external_user_id` — the identifier your application supplied when the consent was granted.

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">get_resource</a>(resource_id) -> GetResourceResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a single resource by id.
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
response = scalekit_client.resources.get_resource('res_123456')
print(response[0].resource)
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

**resource_id:** `str` - Resource to fetch (format: `res_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">list_resources</a>(resource_type, page_size?, page_token?) -> ListResourcesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists resources of a given type in the environment, with pagination.
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
from scalekit.v1.clients.clients_pb2 import ResourceType

response = scalekit_client.resources.list_resources(
    ResourceType.MCP_SERVER,
    page_size=20,
)

for resource in response[0].resources:
    print(resource)
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

**resource_type:** `ResourceType` - Resource type to filter by (e.g. `ResourceType.MCP_SERVER`)

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Page size for pagination (max 30)

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

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">create_resource_client</a>(resource_id, client) -> CreateResourceClientResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a resource client.

Returns the created `client` plus a `plain_secret` — the plaintext client secret, only available at creation time.
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
from scalekit.v1.clients.clients_pb2 import ResourceClient

resource_response = scalekit_client.resources.get_resource('res_123456')
allowed_scopes = [s.name for s in resource_response[0].resource.scopes if s.enabled]
print(allowed_scopes)

response = scalekit_client.resources.create_resource_client(
    'res_123456',
    ResourceClient(name='My Resource Client', scopes=allowed_scopes),
)
print(response[0].client.client_id, response[0].plain_secret)
```

`client` also accepts `description`, `custom_claims`, `expiry` and `redirect_uris` — see Parameters below.
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**resource_id:** `str` - Resource to create the client for (format: `res_...`)

</dd>
</dl>

<dl>
<dd>

**client:** `ResourceClient` (proto message from `scalekit.v1.clients.clients_pb2`) - Desired client properties
- `name: str` - Human-readable name for the client. Defaults to "Resource Client" if omitted.
- `description: str` - Optional description
- `scopes: List[str]` - Scopes to grant. These scopes should be the same or subset of the scopes available for the resource.
- `audience: List[str]` - Not settable through this SDK — audience is always server-determined. Passing a non-empty list raises `ValueError`.
- `custom_claims: List[CustomClaim]` - Custom claims to embed in access tokens, as `CustomClaim(key, value)` messages. Keep this to the essentials, as it increases token size.
- `expiry: int` - Access token lifetime in seconds. Defaults to the resource's configured expiry, or one day.
- `redirect_uris: List[str]` - Allowed redirect URIs, for a pre-registered (non-DCR) client

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">get_resource_client</a>(resource_id, client_id) -> GetResourceClientResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetches a single resource client, along with the end-users who have granted it consent.
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
response = scalekit_client.resources.get_resource_client('res_123456', 'm2m_123456')

print(response[0].client.name)
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

**resource_id:** `str` - Resource the client must belong to (format: `res_...`)

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client id (format: `m2m_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">list_resource_clients</a>(resource_id) -> ListResourceClientsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists resource clients.
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
response = scalekit_client.resources.list_resource_clients('res_123456')

print(response[0].total_dcr_clients, response[0].total_static_clients)
for c in response[0].clients:
    print(c.client_id, c.name)
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

**resource_id:** `str` - Resource whose clients to list (format: `res_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">update_resource_client</a>(resource_id, client_id, name?, description?, scopes?, custom_claims?, expiry?, redirect_uris?) -> UpdateResourceClientResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a resource client.
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
resource_response = scalekit_client.resources.get_resource('res_123456')
allowed_scopes = [s.name for s in resource_response[0].resource.scopes if s.enabled]
print(allowed_scopes)

response = scalekit_client.resources.update_resource_client(
    'res_123456',
    'm2m_123456',
    name='Updated Name',
    scopes=allowed_scopes,
)

print(response[0].client.name, response[0].client.scopes)
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

**resource_id:** `str` - Resource the client must belong to (format: `res_...`)

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client id to update (format: `m2m_...`)

</dd>
</dl>

<dl>
<dd>

**name:** `Optional[str]` - Updated name, if changing it. An empty string is a no-op server-side, not a clear.

</dd>
</dl>

<dl>
<dd>

**description:** `Optional[str]` - Updated description, if changing it. An empty string is a no-op server-side, not a clear.

</dd>
</dl>

<dl>
<dd>

**scopes:** `Optional[List[str]]` - Updated scopes, if changing them (replaces existing; pass `[]` to clear). These scopes should be the same or subset of the scopes available for the resource.

</dd>
</dl>

<dl>
<dd>

**custom_claims:** `Optional[List[CustomClaim]]` - Updated custom claims, if changing them, as `CustomClaim(key, value)` messages (replaces existing; pass `[]` to clear).

</dd>
</dl>

<dl>
<dd>

**expiry:** `Optional[int]` - Updated access token lifetime in seconds, if changing it

</dd>
</dl>

<dl>
<dd>

**redirect_uris:** `Optional[List[str]]` - Updated redirect URIs, if changing them (replaces existing; pass `[]` to clear)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">delete_resource_client</a>(resource_id, client_id) -> DeleteResourceClientResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes resource clients. Raises if the client is missing or scoped to a different resource.
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
scalekit_client.resources.delete_resource_client('res_123456', 'm2m_123456')
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

**resource_id:** `str` - Resource the client must belong to (format: `res_...`)

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client id to delete (format: `m2m_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">create_resource_client_secret</a>(resource_id, client_id) -> CreateClientSecretResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new secret for a resource client. Only 2 client secrets are recommended to exist at a given point in time - use `delete_resource_client_secret` to remove an existing one first if you need more.

The plaintext client secret is only ever returned here, at creation time.
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
response = scalekit_client.resources.create_resource_client_secret('res_123456', 'm2m_123456')

print(response[0].plain_secret, response[0].secret.id)
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

**resource_id:** `str` - Resource the client must belong to (format: `res_...`)

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client id to create a secret for (format: `m2m_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">delete_resource_client_secret</a>(resource_id, client_id, secret_id) -> Tuple[Empty, grpc.Call]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Permanently deletes a secret from a resource client. A client must always keep at least 1 secret - calling this on a client's last remaining secret raises an error.
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
scalekit_client.resources.delete_resource_client_secret('res_123456', 'm2m_123456', 'ksec_123456')
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

**resource_id:** `str` - Resource the client must belong to (format: `res_...`)

</dd>
</dl>

<dl>
<dd>

**client_id:** `str` - Client id the secret belongs to (format: `m2m_...`)

</dd>
</dl>

<dl>
<dd>

**secret_id:** `str` - Secret id to delete (format: `sks_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">list_user_consents</a>(resource_id, search?, page_size?, page_token?, user_ids?, consent_ids?) -> ListResourceUserConsentsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists the end-user consents granted against a resource, with pagination. Use this to audit who authorized a client, and to find the `consent_id` you need before revoking.

Filter in one of three ways. Pass `consent_ids` to fetch specific consents by ID, for example to find the `client_id` you need to revoke a consent you already hold the ID of. Pass `user_ids` to match external user IDs exactly and case-sensitively. Pass `search` for a case-insensitive substring match. When you give more than one, the priority is `consent_ids`, then `user_ids`, then `search`, and the lower-priority ones are ignored without an error. Blank-only `consent_ids` values are ignored, so the next filter applies instead.

When you filter by `consent_ids`, check that every returned `id` is one you asked for before you revoke anything. A server that predates this filter ignores it and returns the unfiltered first page. Do not combine `consent_ids` with `user_ids` as an ownership check, because `consent_ids` overrides `user_ids`. Compare `external_user_id` on the returned consent instead.

Consents with `id`, `external_user_id`, `client_id`, `client_name`, `scopes`, and `granted_at`, plus `total_size` and the `next_page_token` / `prev_page_token` cursors.
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
response = scalekit_client.resources.list_user_consents(
    'res_123456',
    page_size=20,
    consent_ids=['usrcnst_102709535608668163', 'usrcnst_102709535608668164']  # optional; takes precedence over user_ids and search
)

print(response[0].total_size, response[0].next_page_token)
for consent in response[0].consents:
    print(consent.id, consent.external_user_id, consent.client_id, consent.scopes)
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

**resource_id:** `str` - Resource whose consents to list (format: `res_...`)

</dd>
</dl>

<dl>
<dd>

**search:** `Optional[str]` - Case-insensitive substring match on external user IDs. Ignored when `consent_ids` or `user_ids` is set.

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Page size for pagination (max 30)

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Page token for pagination

</dd>
</dl>

<dl>
<dd>

**user_ids:** `Optional[List[str]]` - Exact match on external user IDs, max 25. Ignored when `consent_ids` is set; takes precedence over `search`.

</dd>
</dl>

<dl>
<dd>

**consent_ids:** `Optional[List[str]]` - Exact match on consent IDs (format `usrcnst_xxxxx`), max 25 distinct. IDs that do not exist or belong to another resource are omitted from the result. Takes precedence over `user_ids` and `search`.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.resources.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/resource.py">revoke_user_consent</a>(client_id, consent_id) -> RevokeUserConsentResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Revokes a single end-user consent held by an API client.

Deletes the consent, so the client is prompted for consent again on its next authorization attempt, and revokes every active refresh token issued to that client for the same user. Access tokens already issued stay valid until they expire.

Note that `client_id` is the API client that holds the consent (format: `m2m_...`), not the resource id. This matches the underlying route `DELETE /clients/{client_id}/consents/{consent_id}`.
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
scalekit_client.resources.revoke_user_consent(
    'm2m_123456',
    'usrcnst_123456'
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

**client_id:** `str` - Resource client holding the consent (format: `m2m_...`)

</dd>
</dl>

<dl>
<dd>

**consent_id:** `str` - Consent to revoke (format: `usrcnst_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Connected Accounts

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">list_connected_accounts</a>(organization_id?, user_id?, connector?, identifier?, provider?, page_size?, page_token?, connection_names?) -> ListConnectedAccountsResponse</code></summary>
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

<details><summary><code>client.connected_accounts.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/connected_accounts.py">get_magic_link_for_connected_account</a>(connector, identifier, organization_id?, user_id?, connected_account_id?, state?, user_verify_url?) -> GetMagicLinkForConnectedAccountResponse</code></summary>
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

print(f'Magic Link: {response[0].link}')
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

## Custom Providers

`client.actions.providers` creates and manages custom connectors. A connector gets its tools from one source, and you set exactly one of the two when you create it:

- `proxy_url`: an MCP server. The tools are the ones the server offers, kept per connected account (`client.tools.refresh_tools` re-reads them).
- `openapi_spec_url`: an OpenAPI spec. The server converts the spec's operations into tools in an asynchronous tool collection run that it queues for you. Follow it with `get_tool_collection_run`; queue another with `trigger_tool_collection`; delete one of its tools with `client.tools.delete_custom_tool`.

Walkthrough: [AGENTKIT.md → Custom connectors](AGENTKIT.md#custom-connectors).

<details><summary><code>client.actions.providers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">create_custom_provider</a>(request) -> CreateCustomProviderResponse</code></summary>
<dl>
<dd>

**📝 Description**

<dl>
<dd>

<dl>
<dd>

Creates a new custom provider (a connector) in the Scalekit catalog. Once created, the provider can be selected by organizations when setting up connections.

Set exactly one of `proxy_url` (an MCP server) and `openapi_spec_url` (an OpenAPI spec); building a request with both or neither raises a validation error before anything is sent. `auth_patterns` is required: the server rejects a request without one.

For an OpenAPI-sourced connector the server fetches and validates the spec before it stores anything, answers, and then queues the first tool collection run in the background. The connector exists when the call returns but its tools do not until that run completes: follow it with `get_tool_collection_run`. A spec URL that cannot be fetched, or whose content is not a valid OpenAPI or Swagger document, raises `ScalekitBadRequestException` (400, `INVALID_ARGUMENT`, a message starting `openapi_spec_url failed validation`) and nothing is stored. Where OpenAPI-sourced connectors are not enabled for the environment the call raises `ScalekitBadRequestException` with `error_code` `FEATURE_NOT_ENABLED`, and a second OpenAPI connector with the same name in the environment raises `ScalekitConflictException` (`RESOURCE_ALREADY_EXISTS`).

The server allows up to 2 minutes to validate a spec, including every file it references, but the client sends this call with `openapi_spec_url` (like `update_custom_provider` with `openapi_spec_url` and `trigger_tool_collection`) with its tool-call timeout of 60 seconds by default and does not retry a `DEADLINE_EXCEEDED`, so a spec that takes longer fails on the client first with `ScalekitGatewayTimeoutException` (the server may still finish the create). Raise the timeout with `ScalekitClient(env_url, client_id, client_secret, tool_call_timeout_s=150)`; it also applies to every `client.tools` call. With `openapi_spec_url` the call is also not retried on `UNAVAILABLE`: the create is not idempotent, and a retry after a lost response would raise `ScalekitConflictException` for the connector the first attempt created, so check with `list_providers` before creating it again. An MCP-sourced create keeps the retry.
</dd>
</dl>
</dd>
</dl>

**🔌 Usage**

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.actions.types import (
    AuthPattern,
    AuthField,
    OAuthConfig,
    CreateCustomProviderRequest,
)

# OAuth MCP provider
response = scalekit_client.actions.providers.create_custom_provider(
    CreateCustomProviderRequest(
        display_name="Acme MCP",
        description="Acme integration via MCP",
        proxy_url="https://mcp.acme.com/mcp",
        proxy_enabled=True,
        icon_src="https://acme.com/icon.png",
        metadata={"team": "integrations", "tier": "premium"},
        auth_patterns=[
            AuthPattern(
                type="OAUTH",
                display_name="OAuth 2.1",
                description="Authenticate via browser OAuth.",
                is_mcp=True,
                oauth_config=OAuthConfig(),  # pkce_enabled=True by default
            )
        ],
    )
)
provider = response.provider
print(f"Created provider: {provider.identifier}, metadata: {provider.metadata}")

# Bearer token MCP provider
response = scalekit_client.actions.providers.create_custom_provider(
    CreateCustomProviderRequest(
        display_name="Apify MCP",
        description="Apify platform via MCP",
        proxy_url="https://mcp.apify.com/mcp",
        proxy_enabled=True,
        auth_patterns=[
            AuthPattern(
                type="BEARER",
                display_name="Apify Token",
                description="Authenticate with your Apify API Token.",
                is_mcp=True,
                fields=[
                    AuthField(
                        field_name="token",
                        label="Apify Token",
                        input_type="password",
                        hint="Your Apify API Token",
                        required=True,
                    )
                ],
            )
        ],
    )
)
```

For an OpenAPI-sourced connector, pass `openapi_spec_url` instead of `proxy_url`. The server queues the first tool collection run for you:

```python
from scalekit.actions.types import (
    AuthField,
    AuthPattern,
    CreateCustomProviderRequest,
    CredentialPlacement,
)

response = scalekit_client.actions.providers.create_custom_provider(
    CreateCustomProviderRequest(
        display_name="Acme API",
        description="Acme REST API",
        openapi_spec_url="https://api.acme.com/openapi.json",
        auth_patterns=[
            AuthPattern(
                type="API_KEY",
                display_name="API key",
                fields=[
                    AuthField(
                        field_name="api_key",
                        label="API key",
                        input_type="password",
                        required=True,
                        # Without a placement the key is sent in a header. This sends ?api_key=<key>.
                        placement=CredentialPlacement(in_="query", name="api_key"),
                    )
                ],
            )
        ],
    )
)
connector = response.provider
print(connector.identifier, connector.openapi_spec_url)
```

An `API_KEY` connector that sends several headers gives each field a `header_name`:

```python
AuthPattern(
    type="API_KEY",
    display_name="Key and tenant",
    fields=[
        AuthField(field_name="x_api_key", label="API key", input_type="password", required=True, header_name="X-Api-Key"),
        AuthField(field_name="x_tenant_id", label="Tenant ID", input_type="text", required=True, header_name="X-Tenant-Id"),
    ],
)
```
</dd>
</dl>
</dd>
</dl>

**⚙️ Parameters**

<dl>
<dd>

<dl>
<dd>

**request:** `CreateCustomProviderRequest` - Request object for creating a custom provider
- `display_name: str` - Human-readable name. Accepted characters: a-z, A-Z, 0-9, and spaces. Suffix with 'MCP' for MCP server providers (e.g., "Acme MCP").
- `proxy_url: Optional[str]` - The MCP server URL of an MCP-sourced connector (e.g., `https://mcp.acme.com/mcp`). HTTPS, at most 2048 characters. Required unless `openapi_spec_url` is set, and not accepted together with it.
- `openapi_spec_url: Optional[str]` - URL of an OpenAPI spec (JSON or YAML; a Swagger 2.0 document is converted) that the connector's tools are generated from. HTTPS, at most 2048 characters. Required unless `proxy_url` is set, and not accepted together with it: an OpenAPI-sourced connector's base URL comes from the spec itself, and `update_custom_provider` can override it later. Each fetched file (the spec, and every file it references) is limited to 5 MB by default, and all of them together to 50 MB.
- `proxy_enabled: bool` - Whether to enable Scalekit request proxying. Defaults to `True`.
- `description: str` - Short description of the provider. Defaults to empty string.
- `auth_patterns: List[AuthPattern]` - Required. Authentication options for users. Currently only a single element is supported — the list type is intentional for future multi-pattern support.
  - `type: str` - Auth mechanism. Use `"OAUTH"`, `"BEARER"`, `"API_KEY"`, `"BASIC"` (username and password), or `"NO_AUTH"` for custom connectors. Reading providers back can surface further types the managed catalogue uses (`"OAUTH_M2M"`, `"GOOGLE_DWD"`, …), so any string is accepted. The type of an existing connector cannot be changed.
  - `display_name: str` - Display name for this auth option.
  - `description: str` - Short description of this auth option.
  - `is_mcp: bool` - Set `True` for MCP server providers.
  - `is_open_api: bool` - Read-only: `True` on the pattern of an OpenAPI-sourced connector. The server sets it and ignores what you send, so leave it `False` when you create a connector; keep it as read when you send a pattern back to `update_custom_provider`.
  - `oauth_config: Optional[OAuthConfig]` - Required when `type="OAUTH"`. `OAuthConfig(pkce_enabled=True)` by default.
  - `fields: List[AuthField]` - Input fields shown during connection setup. Credentials for `BEARER` and `API_KEY`; `OAUTH` patterns use them for options collected before the browser flow (e.g. `access_type`).
    - `field_name: str` - Machine-readable key for the field.
    - `label: str` / `hint: str` - Label and helper text shown in the UI.
    - `input_type: str` - How the input renders: `"text"` (default), `"password"`, `"select"`, `"textarea"`. Not a fixed set — the catalogue owns this vocabulary.
    - `required: bool` - Whether the user must fill the field.
    - `options: List[AuthFieldOption]` - Choices for a `"select"` field, each with `value`, `display_name`, `description`, and `default`.
    - `is_path_param: bool` - The value is substituted into the request path rather than sent as a credential.
    - `header_name: str` - On `API_KEY`, send this field's value as this exact HTTP header (case preserved). Giving it to a field puts the pattern in multiple-headers mode; see the rules below.
    - `placement: Optional[CredentialPlacement]` - Send the value in the URL path, the query string or the JSON body instead of an HTTP header; see the rules below. `CredentialPlacement(in_="query", name="api_key")` is sent on the wire as `{"in": "query", "name": "api_key"}`.
  - `account_fields: List[AuthField]` - Inputs collected per connected account rather than once per connection.
  - `allowed_proxy_domains: List[str]` - Domains proxied requests may be routed to.
- `icon_src: str` - URL of the provider's icon image. Defaults to empty string.
- `metadata: Dict[str, str]` - Arbitrary string key-value pairs attached to the provider. Keys 3-25 chars, values 1-256 chars, max 20 pairs. Defaults to empty dict.

**Multiple headers (`header_name`)**

- Every credential field of the pattern needs a `header_name` (an `is_path_param` field is exempt), and a pattern has at most 10 headers.
- A header name may contain only letters, `.`, `-` and `_` (no digits or spaces), must be unique ignoring case, and cannot be `connection`, `keep-alive`, `proxy-authenticate`, `proxy-authorization`, `te`, `trailer`, `transfer-encoding`, `upgrade`, `host` or `content-length`.
- The server replaces each `field_name` with a slug of its header name (lowercased, with runs of `-`, `.` and spaces turned into `_`), so `X-Api-Key` is stored as `x_api_key`.
- A violation raises `ScalekitBadRequestException` with `error_code` `INVALID_HEADER_CONFIG`, and so does switching a connector between single-key and multiple-headers mode after it is created. Where multiple-headers connectors are not enabled for the environment, create and update raise `ScalekitBadRequestException` with `error_code` `FEATURE_NOT_ENABLED`.
- Renaming or removing a header later breaks the connected accounts created before the change: their tool calls fail with `MISSING_REQUIRED_HEADER` until they authorize again.

**Credential placement (`placement`)**

By default a static credential is sent in an HTTP header. A placement sends it somewhere else:

| `in` | Where the value goes |
|------|----------------------|
| `"query"` | The query parameter `name`. It replaces a value the caller sent for that parameter. |
| `"body"` | The top-level JSON body field `name`. A request without a body gets `{name: value}`. A tool that sends a form-encoded body cannot use it. |
| `"path"` | The `{{name}}` placeholder in the path of `proxy_url`, path-escaped, for example `https://api.telegram.org/bot{{bot_token}}`. The placeholder must be in the path, not in the host or the query string. |

- It applies to the `api_key` field of an `API_KEY` pattern, the `token` field of a `BEARER` pattern, and the `username` and `password` fields of a `BASIC` pattern (place both or neither). The field needs `input_type="password"`; a `BASIC` `username` may be `"text"`.
- `name` is required and at most 64 characters. For `query` and `body` it may contain only letters, digits, `_`, `.` and `-`. For `path` it may contain only letters, digits and `_`, and it cannot be `domain`, `version` or the name of one of the pattern's `is_path_param` fields. Two fields cannot place into the same location under the same name.
- A placement is not allowed together with `header_name`, `is_path_param` or `auth_field_mutations`, on `account_fields`, on an `OAUTH` or `NO_AUTH` pattern, or on an MCP connector.
- A placed credential is never also sent in a header, the server does not follow redirects on a request that carries one, and its value is redacted from the error text and the upstream error body of a failed call.
- A broken rule raises `ScalekitBadRequestException` (400, `INVALID_ARGUMENT`, a message starting `invalid credential placement:`) on create and on update. An update that removes the `{{name}}` placeholder from `proxy_url` is rejected too.

</dd>
</dl>
</dd>
</dl>

**📦 Response**

`CreateCustomProviderResponse` with a `provider` attribute (`Provider`) containing `identifier`, `display_name`, `description`, `proxy_url`, `proxy_enabled`, `openapi_spec_url`, `icon_src`, `metadata`, `is_custom`, `is_custom_mcp`, and `auth_patterns`.

</dd>
</dl>
</details>

<details><summary><code>client.actions.providers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">update_custom_provider</a>(request) -> UpdateCustomProviderResponse</code></summary>
<dl>
<dd>

**📝 Description**

<dl>
<dd>

<dl>
<dd>

Updates an existing custom provider. The server requires `display_name` and `auth_patterns` on every update, and `proxy_url` as well for an MCP-sourced connector (otherwise `ScalekitBadRequestException`: `proxy_url is required for an MCP-sourced connector`). The rest of the request is not a patch: `description` and `icon_src` left out keep their stored values, but `metadata` left out is cleared and `proxy_enabled` left out becomes `False`. To change one field and keep the others, read the provider with `list_providers` and send its `auth_patterns`, `proxy_enabled` and `metadata` back with your change.

An OpenAPI-sourced connector (one created with `openapi_spec_url`) can only change `display_name`, `description`, `icon_src`, `metadata` and `proxy_url`, which is its base URL; its tools and auth are managed by the ingestion pipeline. A request that changes anything else raises `ScalekitBadRequestException` (400, `INVALID_ARGUMENT`): `an OpenAPI-sourced connector can only update metadata, display_name, description, icon_src and proxy_url — its tools and auth are managed by the ingestion pipeline`. `auth_patterns` and `proxy_enabled` count as changed only when their content differs from the stored value, so send them back exactly as `list_providers` returned them, including `is_open_api`. The server compares them key for key after parsing, where `"hint": ""` and a missing hint, or `"fields": []` and `"fields": null`, are different values. An `AuthPattern` the SDK decoded is sent back exactly as the server returned it as long as you do not change it or its fields, so pass `Provider.auth_patterns` through untouched rather than rebuilding them. That form survives `copy`, `deepcopy` and `pickle`, but not `model_dump()` or JSON, nor `to_dict()` (which always returns the normalised view) followed by `from_dict()` or a constructor, which rebuild the pattern in the normalised form, so for an OpenAPI-sourced connector always pass the patterns that `list_providers` returned through as they are.

- A changed `proxy_url` (a trailing slash does not count) is saved and queues a tool collection run that regenerates every tool against the new base URL. If a run is already in progress the value is still saved, but the call raises `ScalekitConflictException` (409, `RESOURCE_ALREADY_EXISTS`): call `trigger_tool_collection` once that run completes. If the run cannot be queued for another reason the value is saved too, and the call raises `ScalekitInternalServerException` (`... was saved, but failed to queue the tool collection run`): call `trigger_tool_collection` to retry.
- A changed `openapi_spec_url` raises `ScalekitBadRequestException` with `error_code` `FEATURE_NOT_ENABLED` (`updating the OpenAPI spec URL of an existing connector is not enabled for this workspace`) unless that capability is on for your workspace. Where it is, the new URL is validated before anything is saved, and every tool is regenerated. Sending the stored value again does nothing. A connector that was not created from a spec cannot gain one (`ScalekitBadRequestException`, 400).
</dd>
</dl>
</dd>
</dl>

**🔌 Usage**

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.actions.types import ListProvidersRequest, UpdateCustomProviderRequest
from scalekit.v1.providers.providers_pb2 import ProviderType

providers = scalekit_client.actions.providers

# Read the stored connector first: the update sends back what you do not change.
# An identifier that matches nothing comes back as an empty list, not as an error.
stored = providers.list_providers(
    ListProvidersRequest(provider_type=ProviderType.CUSTOM, identifier="prv_abc123")
).providers
if not stored:
    raise LookupError("No connector with identifier 'prv_abc123'")
current = stored[0]

response = providers.update_custom_provider(
    UpdateCustomProviderRequest(
        identifier=current.identifier,
        display_name=current.display_name,    # required on every update
        auth_patterns=current.auth_patterns,  # required on every update; send them back as read
        proxy_url=current.proxy_url,          # required for an MCP-sourced connector
        proxy_enabled=current.proxy_enabled,  # left out, it becomes False
        metadata=current.metadata,            # left out, it is cleared
        description="Updated description",
    )
)
updated = response.provider
print(f"Updated: {updated.description}")
```

For an OpenAPI-sourced connector, only `proxy_url` (its base URL) changes the tools. The new value is saved and a tool collection run regenerates every tool against it. Read that connector in the same way, so that the update does not send the base URL of another connector:

```python
from scalekit.actions.types import ListProvidersRequest, UpdateCustomProviderRequest
from scalekit.v1.providers.providers_pb2 import ProviderType

providers = scalekit_client.actions.providers

stored = providers.list_providers(
    ListProvidersRequest(provider_type=ProviderType.CUSTOM, identifier="prv_openapi_id")
).providers
if not stored:
    raise LookupError("No connector with identifier 'prv_openapi_id'")
current = stored[0]

response = providers.update_custom_provider(
    UpdateCustomProviderRequest(
        identifier=current.identifier,
        display_name=current.display_name,
        auth_patterns=current.auth_patterns,  # sent back exactly as returned; do not rebuild the pattern
        proxy_enabled=current.proxy_enabled,
        metadata=current.metadata,
        proxy_url="https://eu.api.acme.com",
    )
)
```
</dd>
</dl>
</dd>
</dl>

**⚙️ Parameters**

<dl>
<dd>

<dl>
<dd>

**request:** `UpdateCustomProviderRequest` - Request object for updating a custom provider
- `identifier: str` - Identifier of the provider to update. Obtained from `Provider.identifier`.
- `display_name: str` - Required on every update. Accepted characters: a-z, A-Z, 0-9, and spaces.
- `auth_patterns: List[AuthPattern]` - Required on every update; a request without any is rejected with 400. When they differ from the stored ones they replace the list, they are not merged. To keep the current patterns, send the ones `list_providers` returned.
- `proxy_url: Optional[str]` - For an MCP-sourced connector, its MCP server URL, required on every update. For an OpenAPI-sourced connector, its base URL: omit it, or send `""`, to keep the stored one (`Provider.proxy_url` is `""` until the first tool collection run fills it in, so sending it back as read works); a changed value regenerates every tool. Must be a valid HTTPS URL or `""`.
- `openapi_spec_url: Optional[str]` - Leave it `None` unless you mean to change the spec source (see above). Must be a valid HTTPS URL; `""` is treated like `None`.
- `proxy_enabled: Optional[bool]` - Whether Scalekit proxies requests for this provider. The server applies it on every update, and an update that does not send it sets it to `False`: send `Provider.proxy_enabled` to keep it. For an OpenAPI-sourced connector a value that differs from the stored one is rejected.
- `description: Optional[str]` - New description. `None` keeps the stored one.
- `icon_src: Optional[str]` - New icon URL. `None` keeps the stored one.
- `metadata: Optional[Dict[str, str]]` - The provider's metadata map; it replaces the stored map entirely, it is not merged. Keys 3-25 chars, values 1-256 chars, max 20 pairs. `None` clears all metadata: send `Provider.metadata` to keep it.

</dd>
</dl>
</dd>
</dl>

**📦 Response**

`UpdateCustomProviderResponse` with a `provider` attribute (`Provider`) containing the updated provider details.

</dd>
</dl>
</details>

<details><summary><code>client.actions.providers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">list_providers</a>(request) -> ListProvidersResponse</code></summary>
<dl>
<dd>

**📝 Description**

<dl>
<dd>

<dl>
<dd>

Lists providers in the Scalekit catalog, optionally filtered by type.
</dd>
</dl>
</dd>
</dl>

**🔌 Usage**

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.actions.types import ListProvidersRequest
from scalekit.v1.providers.providers_pb2 import ProviderType

# List only custom providers
response = scalekit_client.actions.providers.list_providers(
    ListProvidersRequest(
        provider_type=ProviderType.CUSTOM,
        page_size=50,
    )
)

for provider in response.providers:
    print(f"{provider.identifier}: {provider.display_name}")

# List all providers (custom + built-in)
response = scalekit_client.actions.providers.list_providers(
    ListProvidersRequest(provider_type=ProviderType.ALL, page_size=100)
)
```

Page through the whole catalog. Pass `page_token=None` (or omit it) for the
first page, then feed back `next_page_token` until it comes back empty:

```python
page_token = None
while True:
    response = scalekit_client.actions.providers.list_providers(
        ListProvidersRequest(
            provider_type=ProviderType.ALL,
            page_size=100,
            page_token=page_token,
        )
    )
    for provider in response.providers:
        print(provider.identifier)

    page_token = response.next_page_token
    if not page_token:
        break
```

Inspect what a provider asks the user for. `auth_patterns` is fully decoded, so
there is no protobuf left to unpack — and a `select` field carries its choices
in `options`:

An `identifier` that matches nothing comes back as an empty list rather than an
error, so check before indexing:

```python
response = scalekit_client.actions.providers.list_providers(
    ListProvidersRequest(identifier="my-connector")
)
if not response.providers:
    raise LookupError("No provider with identifier 'my-connector'")

provider = response.providers[0]

for pattern in provider.auth_patterns:
    print(f"{pattern.type} — {pattern.display_name}")

    for field in pattern.fields:
        required = " (required)" if field.required else ""
        print(f"  {field.field_name}: {field.input_type}{required}")

        # Only populated when input_type == "select"
        for option in field.options:
            default = " [default]" if option.default else ""
            print(f"    - {option.value} — {option.display_name}{default}")

    if pattern.oauth_config:
        print(f"  pkce_enabled={pattern.oauth_config.pkce_enabled}")
```

`input_type` and `pattern.type` are plain strings, not fixed enums — the
vocabulary belongs to the provider catalog and grows over time. Compare against
the values you care about and let anything else fall through rather than
matching exhaustively:

```python
if field.input_type == "password":
    ...  # mask the input
elif field.input_type == "select":
    ...  # render field.options
else:
    ...  # "text", "textarea", or something newer — render a plain input
```
</dd>
</dl>
</dd>
</dl>

**⚙️ Parameters**

<dl>
<dd>

<dl>
<dd>

**request:** `ListProvidersRequest` - Request object for listing providers
- `provider_type: Optional[int]` - `ProviderType.CUSTOM` (custom only), `ProviderType.DEFAULT` (built-in only), or `ProviderType.ALL` (built-in and custom). Omit it and only built-in providers are returned, the same as `ProviderType.DEFAULT`; pass `ProviderType.ALL` or `ProviderType.CUSTOM` to include custom providers.
- `page_size: Optional[int]` - Maximum number of providers to return.
- `page_token: Optional[str]` - Pagination cursor from a previous response's `next_page_token`.
- `identifier: Optional[str]` - Filter to a specific provider by identifier.

</dd>
</dl>
</dd>
</dl>

**📦 Response**

`ListProvidersResponse` with a `providers` attribute (list of `Provider`) and `next_page_token` for pagination. An OpenAPI-sourced connector has `openapi_spec_url` set and its `auth_patterns` carry `is_open_api=True`; its `proxy_url` is the base URL its tools call.

</dd>
</dl>
</details>

<details><summary><code>client.actions.providers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">delete_custom_provider</a>(request) -> DeleteCustomProviderResponse</code></summary>
<dl>
<dd>

**📝 Description**

<dl>
<dd>

<dl>
<dd>

Permanently deletes a custom provider. The provider is removed from the Scalekit catalog and can no longer be used for new connections. While a tool collection run of the connector is queued or processing, nothing is deleted and the call raises `ScalekitConflictException` (409, `RESOURCE_ALREADY_EXISTS`; the message names the run): poll that run with `get_tool_collection_run` (pass its ID as `run_id`) and retry once it has finished. The server fails a run that makes no progress after about 30 minutes.
</dd>
</dl>
</dd>
</dl>

**🔌 Usage**

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.actions.types import DeleteCustomProviderRequest

scalekit_client.actions.providers.delete_custom_provider(
    DeleteCustomProviderRequest(identifier="prv_abc123")
)
```
</dd>
</dl>
</dd>
</dl>

**⚙️ Parameters**

<dl>
<dd>

<dl>
<dd>

**request:** `DeleteCustomProviderRequest` - Request object for deleting a custom provider
- `identifier: str` - Identifier of the custom provider to delete. Obtained from `Provider.identifier`.

</dd>
</dl>
</dd>
</dl>

**📦 Response**

`DeleteCustomProviderResponse` (empty — success is indicated by no exception being raised).

</dd>
</dl>
</details>

<details><summary><code>client.actions.providers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">trigger_tool_collection</a>(request) -> ToolCollectionRun</code></summary>
<dl>
<dd>

**📝 Description**

<dl>
<dd>

<dl>
<dd>

Queues a new tool collection run on an OpenAPI-sourced connector and returns it at once with status `QUEUED`. The server first re-fetches and validates the connector's current spec URL, then regenerates the connector's tools in the background. A connector is also re-synced automatically when it is created and when its base URL or spec URL changes, so call this to pick up changes to the spec itself or to retry after a failed run. Follow the run with `get_tool_collection_run`. It is not retried on `UNAVAILABLE`, because the first attempt may already have queued a run. It uses the client's tool-call timeout (`tool_call_timeout_s`, 60 seconds by default) while the server allows up to 2 minutes to validate the spec; see `create_custom_provider`.

A connector has at most one active (`QUEUED` or `PROCESSING`) run. Errors:

- `ScalekitConflictException` (409, `RESOURCE_ALREADY_EXISTS`: `an ingestion run is already in progress for this connector`): wait for the active run to finish and call again.
- `ScalekitNotFoundException` (404, `NOT_FOUND`): no connector with that identifier in the environment.
- `ScalekitBadRequestException` (400): the connector is not sourced from an OpenAPI spec (`INVALID_ARGUMENT`: `this connector is not sourced from an OpenAPI spec`), its stored spec URL fails validation (`openapi_spec_url failed validation: ...`), or OpenAPI-sourced connectors are not enabled for the environment (`FEATURE_NOT_ENABLED`).
</dd>
</dl>
</dd>
</dl>

**🔌 Usage**

<dl>
<dd>

<dl>
<dd>

```python
from scalekit.actions.types import TriggerToolCollectionRequest

run = scalekit_client.actions.providers.trigger_tool_collection(
    TriggerToolCollectionRequest(provider_identifier="prv_abc123")
)
print(run.run_id, run.status)  # ToolCollectionRunStatus.QUEUED
```
</dd>
</dl>
</dd>
</dl>

**⚙️ Parameters**

<dl>
<dd>

<dl>
<dd>

**request:** `TriggerToolCollectionRequest` - Request object for queueing a tool collection run
- `provider_identifier: str` - Identifier of the OpenAPI-sourced connector, 1-255 characters. Obtained from `Provider.identifier`.

</dd>
</dl>
</dd>
</dl>

**📦 Response**

A `ToolCollectionRun` (see `get_tool_collection_run`) with status `QUEUED`.

</dd>
</dl>
</details>

<details><summary><code>client.actions.providers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/actions.py">get_tool_collection_run</a>(request) -> ToolCollectionRun</code></summary>
<dl>
<dd>

**📝 Description**

<dl>
<dd>

<dl>
<dd>

Reads one tool collection run of an OpenAPI-sourced connector. Pass `run_id="latest"` (the default, the same as an empty string) for the connector's most recent run, for example the one `create_custom_provider` queued. Poll until `run.is_terminal`: the run is then `COMPLETED` or `FAILED` and does not change again.

The server queues the first run in the background after `create_custom_provider` has answered, and does not report a failure to queue it, so right after a create the call can answer 404 until the run exists. The server gives up queueing it after 30 seconds: if the 404 outlasts that, call `trigger_tool_collection`, as the example below does after 45 seconds.

Errors: `ScalekitNotFoundException` (404, `NOT_FOUND`) when the connector does not exist (`provider not found`), it has no run yet, or `run_id` names no run of this connector (`tool collection run not found`); `ScalekitBadRequestException` (400, `INVALID_ARGUMENT`: `invalid run_id`) when `run_id` is not a run ID.
</dd>
</dl>
</dd>
</dl>

**🔌 Usage**

<dl>
<dd>

<dl>
<dd>

```python
import time

from scalekit.actions.types import GetToolCollectionRunRequest, ToolCollectionRunStatus, TriggerToolCollectionRequest
from scalekit.common.exceptions import ScalekitConflictException, ScalekitNotFoundException

providers = scalekit_client.actions.providers
identifier = "prv_abc123"  # run_id defaults to "latest"

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

print(f"{run.tools_created} created, {run.tools_updated} updated, {run.tools_deleted} deleted")
for skipped in run.skipped_tools:
    print(skipped.method, skipped.path, "-", skipped.reason)
```
</dd>
</dl>
</dd>
</dl>

**⚙️ Parameters**

<dl>
<dd>

<dl>
<dd>

**request:** `GetToolCollectionRunRequest` - Request object for reading a tool collection run
- `provider_identifier: str` - Identifier of the OpenAPI-sourced connector, 1-255 characters. Obtained from `Provider.identifier`.
- `run_id: str` - A `ToolCollectionRun.run_id`, or `"latest"` (the default) for the connector's most recent run. At most 255 characters.

</dd>
</dl>
</dd>
</dl>

**📦 Response**

`ToolCollectionRun`, a frozen model (its fields cannot be reassigned):

- `run_id: str`, `provider_identifier: str` - The run's own ID and the connector it belongs to.
- `status: ToolCollectionRunStatus | str` - `QUEUED`, `PROCESSING`, `COMPLETED` or `FAILED`. A status this SDK version does not know is the plain string. `is_terminal` is `True` for `COMPLETED` and `FAILED`.
- `total_endpoints: int` - The operations found in the spec before the ones that cannot become tools are filtered out: `tools_created + tools_updated` plus the skipped operations. `0` until the run completes.
- `tools_created`, `tools_updated`, `tools_deleted: int` - Tools this run created, refreshed, and deleted because their operation is no longer in the spec. A run that finds the spec, base URL and auth patterns unchanged since the last completed run reports `0` created, updated and deleted and repeats that run's `total_endpoints` and skipped operations; the server does not take that shortcut for a spec that references external files.
- `skipped_tools: List[SkippedTool]` - The operations the run could not convert into tools, each with `operation_id`, `method`, `path` and a human-readable `reason` (text to show, not a stable code to match on). Empty until the run reaches a terminal status. A run that skips some operations still completes; one that cannot convert any operation fails and lists them here. The entry the server adds when removed tools could not be cleaned up has only a `reason`.
- `skipped_tools_json: str` - The server's own JSON text behind `skipped_tools`, which the server calls provisional. Empty until the run is terminal, and it can be the text `null`; both read as no skipped tools.
- `error_message: str` - Why the run failed. Empty unless the status is `FAILED`.
- `created_at`, `started_at`, `finished_at: Optional[datetime]` - Timezone-aware UTC instants. `started_at` is `None` while the run is `QUEUED`, and `finished_at` is `None` until the run is terminal.

An operation is skipped, for example, when its request body is multipart, binary or another structured format that is not JSON (such as XML), when its path uses a `{parameter}` it does not declare, when no base URL can be resolved for it, when it requires authentication and the connector has no auth pattern that supports it, or when its HTTP method is not one of `GET`, `POST`, `PUT`, `PATCH` and `DELETE`. Read `reason` for the exact cause.

</dd>
</dl>
</details>

## Tools

`list_tools`, `list_scoped_tools` and `execute_tool` are documented in [AGENTKIT.md → Tools](AGENTKIT.md#tools), together with how the tools of a custom connector are listed and named.

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">search_tools</a>(query, identifier?, top_k?) -> SearchToolsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Searches tools ranked by relevance to a natural-language query — the job to be done, not an exact tool name.

Pass `identifier` to also get per-connection readiness (`TOOL_READINESS_STATE_READY`, `TOOL_READINESS_STATE_NEEDS_CONNECTION`, or `TOOL_READINESS_STATE_NEEDS_REAUTH`) on each result, so you can gate execution on the right auth step before calling `execute_tool`. `TOOL_READINESS_STATE_NEEDS_CONNECTION` means an existing connected account for that provider is inactive; an empty `connections` list means no account exists for the provider at all (not an error). Only pass a result's `connected_account_id` to `execute_tool` when `readiness_state` is `TOOL_READINESS_STATE_READY`.
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
from scalekit.v1.tools.tools_pb2 import TOOL_READINESS_STATE_READY

response = scalekit_client.tools.search_tools(
    query="send a message to a slack channel",
    identifier="user@example.com",
    top_k=10
)

for tool in response[0].tools:
    print(tool.name, tool.score)
    for connection in tool.connections:
        # readiness_state is an int at runtime -- always compare against the
        # named enum constant, never a raw int or a string.
        is_ready = connection.readiness_state == TOOL_READINESS_STATE_READY
        print(" ", connection.connection_name, is_ready, connection.connected_account_id)
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

**query:** `str` - Natural-language query or keywords describing the job to be done. 1-256 characters.

</dd>
</dl>

<dl>
<dd>

**identifier:** `Optional[str]` - Connected-account identifier (e.g. the end user's email or ID). When set, each result is annotated with readiness for this identifier's connections.

</dd>
</dl>

<dl>
<dd>

**top_k:** `Optional[int]` - Maximum number of ranked results to return. Defaults to 10, capped at 50.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">list_available_tools</a>(identifier, page_size?, page_token?) -> ListAvailableToolsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists every tool available to a connected-account identifier: the tools of all the connectors the identifier has a connected account on, including a connector created from an OpenAPI spec (its tools are shared by every account) and a custom MCP connector's tools for that identifier's account. An identifier with no connected account gets an empty list, not an error. The server uses a page size of 100 when `page_size` is omitted or `0`. Each `Tool.definition` is a `google.protobuf.Struct`, and Python protobuf decodes at most about 100 levels of nested messages, so one tool definition nested about 30 objects deep makes the whole call fail to decode. The same limit already applies to `list_tools`; the server can return definitions as JSON text instead, but this SDK version does not request that yet.
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
response, _ = scalekit_client.tools.list_available_tools("user@example.com", page_size=50)

for tool in response.tools:
    print(tool.definition["name"])

# More pages: pass response.next_page_token as page_token until it is empty.
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

**identifier:** `str` - Identifier of the connected account (for example the end user's email or ID). Required.

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Maximum number of tools per page.

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - Pagination cursor from a previous response's `next_page_token`.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">refresh_tools</a>(identifier?, connected_account_id?, connection_name?, organization_id?, user_id?) -> RefreshToolsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Resyncs the tools of a custom MCP connected account: the server re-queries the upstream MCP server, adds new and changed tools, removes the ones it no longer offers, and returns the full refreshed list. Use it when the upstream server has added, renamed or removed tools; the catalog is also resynced when an account is created, authenticated again or has its metadata updated. The server marks this endpoint as a preview API.

It works only for a custom MCP connector. A connector created from an OpenAPI spec gets its tools from a tool collection run instead: use `client.actions.providers.trigger_tool_collection`. Each `Tool.definition` is a `google.protobuf.Struct`, and Python protobuf decodes at most about 100 levels of nested messages, so one tool definition nested about 30 objects deep makes the whole call fail to decode. The same limit already applies to `list_tools`; the server can return definitions as JSON text instead, but this SDK version does not request that yet.

Name the connected account with `connected_account_id`, or with `connection_name` together with `identifier` (and `organization_id` or `user_id` when the same identifier exists in more than one organization or for more than one user). An account created with `organization_id` (and `user_id`) and no `identifier` is named by `connection_name` together with those IDs. A call that gives only `connection_name` or only `identifier` names no account and raises `ValueError` before anything is sent. Other errors:

- `ScalekitBadRequestException` (400): the connected account is not a custom MCP connector (`connected account is not a custom MCP connector`), or custom MCP tools are not enabled for the environment (`custom MCP tools are not enabled for this environment`).
- `ScalekitNotFoundException` (404): no connected account matches.
- `ScalekitTooManyRequestsException` (429, `error_code` `DISCOVERY_IN_PROGRESS`): a refresh of the same account is already running. Retry in a few seconds.
- `ScalekitInternalServerException` (500): the upstream server could not be queried.
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
response, _ = scalekit_client.tools.refresh_tools(connected_account_id="ca_123")
print(response.total_size, [tool.definition["name"] for tool in response.tools])

# Or name the account by connection and identifier:
response, _ = scalekit_client.tools.refresh_tools(
    connection_name="acme-mcp",
    identifier="user@example.com",
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

**connected_account_id:** `Optional[str]` - ID of the connected account to refresh (`ca_...`).

</dd>
</dl>

<dl>
<dd>

**connection_name:** `Optional[str]` - Name of the connection the account belongs to. Use it with `identifier`, or with `organization_id`.

</dd>
</dl>

<dl>
<dd>

**identifier:** `Optional[str]` - Identifier of the connected account, used together with `connection_name`.

</dd>
</dl>

<dl>
<dd>

**organization_id:** `Optional[str]` - Narrows the account lookup when the same identifier exists in more than one organization. With `connection_name` and no `identifier`, it names an account that was created without one.

</dd>
</dl>

<dl>
<dd>

**user_id:** `Optional[str]` - Narrows the account lookup when the same identifier exists for more than one user.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tools.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/tools.py">delete_custom_tool</a>(tool_name, provider_identifier?) -> (Empty, grpc.Call)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes one tool of a connector created from an OpenAPI spec, by its name, now. Use it to keep a single operation of an API away from your agents. Name the tool as `list_tools` lists it: `a-<connector>_<operation>`. The name alone picks the tool, because it carries the connector's name and an environment has one OpenAPI-sourced connector of that name. The server matches the name in lower case (ASCII letters only), as it stores tool names, so the SDK sends `tool_name` exactly as given: it changes neither the case nor the spaces.

Only a tool of an OpenAPI-sourced connector of your environment can be deleted this way. Any other name (an MCP tool, a global tool, another environment's tool, a tool whose connector is missing or not OpenAPI-sourced, an unknown name) raises `ScalekitNotFoundException`, and the error does not say which of these it was.

**The deletion is not permanent.** A full sync of the connector creates the tool again (same name, new id) while its operation is still in the spec, for example after the spec's content or the connector's base URL has changed; a sync that is skipped because nothing changed does not. To drop an operation for good, remove it from the spec. Connections and virtual MCP configurations that listed the tool keep its name: running it fails with 400 `custom tool not found: <name>`, a virtual MCP server does not serve it, and saving a configuration that still names it is refused with 400, until the name is removed or a sync brings the tool back.

**A sync in progress blocks the delete.** While a sync of the connector is queued or running, nothing is deleted, because that sync would create the tool again: the call raises `ScalekitConflictException` and you call it again once the run has finished. `get_tool_collection_run` with `run_id="latest"` (the default) usually shows that run, but not always: the server refuses while any run of the connector has not finished, and an older unfinished run can sit behind a newer finished one. The 409 is what counts, so call again until it stops; the server fails a run that makes no progress after about 30 minutes. The server checks this when the call arrives, so a sync that starts right afterwards can still bring the tool back.

**Retries.** The call uses the client's tool-call timeout, `tool_call_timeout_s`. It is sent again when the service is unavailable, like most calls of this client, because deleting by name is safe to repeat. The repeat of a delete that already happened is answered with 404 and changes nothing, so a `ScalekitNotFoundException` means "not there now", not "never there": after a call that was sent again, or after a timeout (a timeout is not sent again, but the server may have finished the delete all the same), the tool may be gone because of the first attempt. (`trigger_tool_collection` is not sent again, because a repeat of it queues a second run.)

Errors:

- `ValueError`: `tool_name` is not a non-empty string (a name of only whitespace counts as empty). Raised before anything is sent.
- `ScalekitBadRequestException` (400): the name is longer than 2048 characters (an empty name never gets this far: it raises `ValueError` first), `provider_identifier` is longer than 512 characters, either has a control character, or OpenAPI-sourced connectors are not enabled for the environment (`error_code` `FEATURE_NOT_ENABLED`).
- `ScalekitNotFoundException` (404): no deletable tool has this name (see above). A leftover tool of a connector that no longer exists, or is not OpenAPI-sourced, cannot be deleted this way and answers 404 too.
- `ScalekitConflictException` (409), with nothing deleted: `error_code` `RESOURCE_ALREADY_EXISTS` while a sync of the connector is queued or running (call again after it has finished), or `TOOL_NAME_AMBIGUOUS` when tools of more than one connector of the environment have this name, which leftover rows of an earlier connector cause. The message of the second names two of the connectors: call again with `provider_identifier` set to the full identifier of the OpenAPI-sourced connector whose tool should be deleted.
- `ScalekitInternalServerException` (500): the server failed. It does not say whether the tool is gone: list the connector's tools with `list_tools` before calling again.

The response is `(google.protobuf.Empty, grpc.Call)`: it has no content, and `response[1].code().name == 'OK'` on success.
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
# The name as list_tools shows it: a-<connector>_<operation>
scalekit_client.tools.delete_custom_tool("a-acmeapi_deletepet")

# Tools of two connectors share this name (leftovers of an earlier connector): say which one
scalekit_client.tools.delete_custom_tool("a-acmeapi_deletepet", provider_identifier="ACMEAPI:1234")
```

A bounded wait for a sync that is queued or running:

```python
import time

from scalekit.common.exceptions import ScalekitConflictException

# This gives up after about 5 minutes (20 x 15 s). A run that is stuck is failed by the server only
# after about 30 minutes, so the TimeoutError below does not mean that the server will not clear it.
for _ in range(20):
    try:
        scalekit_client.tools.delete_custom_tool("a-acmeapi_deletepet")
        break
    except ScalekitConflictException as exc:
        if exc.error_code != "RESOURCE_ALREADY_EXISTS":  # TOOL_NAME_AMBIGUOUS: pass provider_identifier
            raise
        time.sleep(15)  # a sync of the connector is queued or running: ask again once it has finished
else:
    raise TimeoutError("the connector's sync did not finish: the tool was not deleted")
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

**tool_name:** `str` - Name of the tool to delete, as `list_tools` lists it for the connector (`a-<connector>_<operation>`). Required; at most 2048 characters. The server matches it in lower case (ASCII letters only); the SDK sends it as given.

</dd>
</dl>

<dl>
<dd>

**provider_identifier:** `Optional[str]` - Full identifier of the connector that owns the tool, exactly as the connector's identifier is returned (for example `ACME:1234`); unlike the tool name it is matched exactly, case included. Optional: it is needed only for the `TOOL_NAME_AMBIGUOUS` case. It must name an OpenAPI-sourced connector that still exists. At most 512 characters.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Triggers

`client.actions.triggers` manages AgentKit triggers: the trigger catalogue of a connection, subscriptions, the webhook URL and signing secret, activity, usage and deliveries to your endpoints. Every method except `delete_subscription` (which returns `None`) returns a typed, frozen model (fields cannot be reassigned; nested lists and dicts such as `config` are plain, mutable copies); enum fields hold members for known values and a plain `str` for newer ones, instants are timezone-aware UTC `datetime`, durations are `timedelta`. Server errors raise the matching `Scalekit*Exception` with a stable `error_code`; batch methods report per-item outcomes instead. `verify_event` (verifying a delivered event) is documented under ScalekitClient above. Walkthrough: [AGENTKIT.md → Managing triggers](AGENTKIT.md#managing-triggers).

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">list_available</a>(connection_id) -> ListAvailableTriggersResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists every trigger a connection offers (not paginated), with its detection mode, required scopes, config fields, interval limits and whether it is usable on this connection (`available`, `reason`, `remedy`, `refusal_code`). An unknown connection raises `ScalekitNotFoundException` (`RESOURCE_NOT_FOUND`).
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
page = scalekit_client.actions.triggers.list_available("conn_123")
for trigger in page.triggers:
    print(trigger.name, trigger.mode, trigger.available, trigger.min_interval)
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">list_eligible_accounts</a>(connection_id, trigger_name, *, query?, page_size?, page_token?) -> ListEligibleAccountsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists one page of a connection's connected accounts and whether each can subscribe to the trigger, with its health and how to fix it. Each account's `id` is the connected account ID (`ca_...`) to pass as `connected_account_id` when you subscribe; its `identifier` is the identifier the account was created with (such as your app's user ID or the user's email address), or the connected account ID when it has none. Empty page tokens are `None`.
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
page = scalekit_client.actions.triggers.list_eligible_accounts("conn_123", "item.created", page_size=50)
eligible = [a.id for a in page.accounts if a.eligible]
if page.next_page_token:
    page = scalekit_client.actions.triggers.list_eligible_accounts(
        "conn_123", "item.created", page_token=page.next_page_token
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**trigger_name:** `str` - `AvailableTrigger.name`

</dd>
</dl>

<dl>
<dd>

**query:** `Optional[str]` - Filter accounts by identifier

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Accounts per page; server default 10, values above 100 are capped

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - `next_page_token` or `prev_page_token` of a previous page

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">list_subscriptions</a>(connection_id, *, trigger_name?, statuses?, page_size?, page_token?) -> ListTriggerSubscriptionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists one page of a connection's trigger subscriptions, with `total_size` and `status_counts` (per status name, ignoring the `statuses` filter).
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
from scalekit.actions import TriggerSubscriptionStatus

page = scalekit_client.actions.triggers.list_subscriptions(
    "conn_123", statuses=[TriggerSubscriptionStatus.PAUSED_CREDENTIAL]
)
for sub in page.subscriptions:
    print(sub.id, sub.connected_account_id, sub.status)
print(page.status_counts.get("ACTIVE", 0))
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**trigger_name:** `Optional[str]` - Only subscriptions to this trigger

</dd>
</dl>

<dl>
<dd>

**statuses:** `Optional[Sequence[TriggerSubscriptionStatus | str | int]]` - Only these states: members, their names, or raw numbers

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Subscriptions per page; capped at 100 by the server

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - `next_page_token` or `prev_page_token` of a previous page

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">create_subscription</a>(connection_id, trigger_name, *, connected_account_id?, interval?, config?) -> TriggerSubscription</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Subscribes a connected account (or, for a connection-scoped trigger, the whole connection) to a trigger. Not retried on `UNAVAILABLE`, because a retry could create it twice. The same subscription again raises `ScalekitConflictException` (`RESOURCE_ALREADY_EXISTS`); a refused account (missing scopes, unhealthy, no consent) raises `ScalekitBadRequestException` with a message that says how to fix it.
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
from datetime import timedelta

sub = scalekit_client.actions.triggers.create_subscription(
    "conn_123",
    "item.created",
    connected_account_id="ca_123",
    interval=timedelta(minutes=5),  # poll triggers only
)
print(sub.id, sub.status, sub.effective_interval)
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**trigger_name:** `str` - `AvailableTrigger.name`

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - The account (`ca_...`); leave out only for a connection-scoped trigger

</dd>
</dl>

<dl>
<dd>

**interval:** `Optional[timedelta]` - Poll interval in whole seconds, at least the trigger's `min_interval`; leave out for the default and for webhook triggers

</dd>
</dl>

<dl>
<dd>

**config:** `Optional[Mapping[str, str]]` - Values for the trigger's `config_fields`

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">batch_create_subscriptions</a>(connection_id, trigger_name, *, connected_account_ids?, interval?, config?) -> BatchCreateTriggerSubscriptionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Subscribes up to 100 connected accounts in one call. Not atomic: every account gets an outcome in `results` (`CREATED`, `ALREADY_SUBSCRIBED`, `REFUSED`, `NOT_FOUND`, `FAILED`, `NOT_ATTEMPTED`) and those never raise. Safe to call again for the `FAILED` and `NOT_ATTEMPTED` ones. Leave `connected_account_ids` out for a connection-scoped trigger.
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
from scalekit.actions import TriggerSubscribeOutcome

batch = scalekit_client.actions.triggers.batch_create_subscriptions(
    "conn_123", "item.created", connected_account_ids=["ca_1", "ca_2"]
)
retry = [
    r.connected_account_id for r in batch.results
    if r.outcome in (TriggerSubscribeOutcome.FAILED, TriggerSubscribeOutcome.NOT_ATTEMPTED)
]
print(batch.created_count, retry)
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**trigger_name:** `str` - `AvailableTrigger.name`

</dd>
</dl>

<dl>
<dd>

**connected_account_ids:** `Optional[Sequence[str]]` - The accounts (`ca_...`), unique, up to 100

</dd>
</dl>

<dl>
<dd>

**interval:** `Optional[timedelta]` - Poll interval in whole seconds (see `create_subscription`)

</dd>
</dl>

<dl>
<dd>

**config:** `Optional[Mapping[str, str]]` - Values for the trigger's `config_fields`

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">delete_subscription</a>(connection_id, subscription_id) -> None</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes one trigger subscription. Retried on `UNAVAILABLE`, so a `ScalekitNotFoundException` can also mean an earlier attempt of the same call already deleted it.
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
scalekit_client.actions.triggers.delete_subscription("conn_123", "trgs_123")
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**subscription_id:** `str` - The subscription (`trgs_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">batch_delete_subscriptions</a>(connection_id, *, subscription_ids?, trigger_name?, connected_account_ids?) -> BatchDeleteTriggerSubscriptionsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes many subscriptions in one call. Pass exactly one selector: `subscription_ids`, or `trigger_name` with `connected_account_ids` (up to 100 each; the server rejects any other combination). Every subscription gets an outcome in `results` (`DELETED`, `NOT_FOUND`, `FAILED`, `NOT_ATTEMPTED`) and those never raise. Safe to call again; rate limiting raises `ScalekitTooManyRequestsException`.
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
batch = scalekit_client.actions.triggers.batch_delete_subscriptions(
    "conn_123", trigger_name="item.created", connected_account_ids=["ca_1", "ca_2"]
)
print(batch.deleted_count, [(r.subscription_id, r.outcome) for r in batch.results])
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**subscription_ids:** `Optional[Sequence[str]]` - Subscriptions to delete (`trgs_...`)

</dd>
</dl>

<dl>
<dd>

**trigger_name:** `Optional[str]` - With `connected_account_ids`: the trigger to unsubscribe from

</dd>
</dl>

<dl>
<dd>

**connected_account_ids:** `Optional[Sequence[str]]` - With `trigger_name`: the accounts (`ca_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">get_activity</a>() -> GetTriggerActivityResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Counts what happened to this environment's trigger events over the recent `window` (`received`, `filtered`, `unresolved`, `delivered`, `delivery_failed`, `duplicate`, `signature_failed`, `discarded`; every key is present). `signature_banner` means the signing secret probably does not match the provider's; while `degraded` is true, zeroes are not reliable.
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
activity = scalekit_client.actions.triggers.get_activity()
print(activity.window, activity.counts["delivered"])
if activity.signature_banner:
    print("check the signing secret")
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

None.

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">get_usage</a>(*, period?, from_date?, to_date?) -> GetTriggerUsageResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Reads metered trigger deliveries: pass `period` (`"24h"` hourly, `"7d"` or `"30d"` daily) or both `from_date` and `to_date` (UTC dates, inclusive; the server clamps the range to the last 30 days). Days and hours without deliveries are absent. Not metered raises `ScalekitNotFoundException` (`TRIGGER_USAGE_NOT_METERED`).
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
from datetime import date

usage = scalekit_client.actions.triggers.get_usage(from_date=date(2026, 10, 1), to_date=date(2026, 10, 28))
print(usage.from_date, usage.to_date, [(d.date, d.units) for d in usage.days])

hourly = scalekit_client.actions.triggers.get_usage(period="24h")
print(hourly.current_hour, [(h.start, h.units) for h in hourly.hours])
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

**period:** `Optional[str]` - `"24h"`, `"7d"` or `"30d"`

</dd>
</dl>

<dl>
<dd>

**from_date:** `Optional[date | str]` - First UTC date: a `date`, an aware `datetime` (its UTC date) or `"YYYY-MM-DD"`

</dd>
</dl>

<dl>
<dd>

**to_date:** `Optional[date | str]` - Last UTC date, in the same forms

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">get_ingress_endpoint</a>(connection_id, *, connected_account_id?) -> TriggerIngressEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Reads the webhook URL a provider sends events to, and the state of its signing secret (never the secret itself). Pass `connected_account_id` to read one connected account's own URL (triggers with `ingress_per_account`); leave it out for the connection's URL. A malformed `connected_account_id` raises `ScalekitBadRequestException`. No URL yet raises `ScalekitNotFoundException` with `error_code` `TRIGGER_INGRESS_ENDPOINT_NOT_CREATED`; an unknown connection uses `RESOURCE_NOT_FOUND`.
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
endpoint = scalekit_client.actions.triggers.get_ingress_endpoint("conn_123")
print(endpoint.signing_secret_configured, endpoint.masked_signing_secret, endpoint.rotation_in_progress)

# One connected account's own URL (a trigger with ingress_per_account)
account_endpoint = scalekit_client.actions.triggers.get_ingress_endpoint(
    "conn_123", connected_account_id="ca_456"
)
print(account_endpoint.scope, account_endpoint.connected_account_id)
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - Act on this connected account's own webhook URL (`ca_...`), for a trigger whose `ingress_per_account` is `True`; leave it out to act on the connection's URL. An empty string raises `ValueError` (keyword only)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">create_ingress_endpoint</a>(connection_id, *, connected_account_id?) -> TriggerIngressEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates the connection's webhook URL, or returns the existing one (safe to call again). Pass `connected_account_id` to create one connected account's own URL (triggers with `ingress_per_account`); a malformed ID, or an inactive or consent-pending account, raises `ScalekitBadRequestException`. Paste `url` into the provider's app configuration and treat it as confidential. A connection without a webhook trigger raises `ScalekitBadRequestException` (`TRIGGER_INGRESS_NOT_APPLICABLE`).
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
endpoint = scalekit_client.actions.triggers.create_ingress_endpoint("conn_123")
print("paste into the provider:", endpoint.url)

# One connected account's own URL (a trigger with ingress_per_account)
account_endpoint = scalekit_client.actions.triggers.create_ingress_endpoint(
    "conn_123", connected_account_id="ca_456"
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - Act on this connected account's own webhook URL (`ca_...`), for a trigger whose `ingress_per_account` is `True`; leave it out to act on the connection's URL. An empty string raises `ValueError` (keyword only)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">set_signing_secret</a>(connection_id, *, signing_secret, connected_account_id?) -> TriggerIngressEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Stores the secret the provider signs its events with, for the connection's URL or, with `connected_account_id`, one connected account's own URL (a malformed ID raises `ScalekitBadRequestException`). Setting a different secret later starts a rotation: both are accepted until `confirm_signing_secret_rotation` or for 24 hours; a third secret while a rotation is open raises `ScalekitConflictException`. Not retried on `UNAVAILABLE`. Providers whose secret Scalekit generates raise `ScalekitBadRequestException` (`TRIGGER_SIGNING_SECRET_GENERATED_ONLY`).
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
import os

endpoint = scalekit_client.actions.triggers.set_signing_secret(
    "conn_123", signing_secret=os.environ["PROVIDER_SIGNING_SECRET"]
)
print(endpoint.masked_signing_secret, endpoint.rotation_in_progress)

# One connected account's own URL (a trigger with ingress_per_account)
scalekit_client.actions.triggers.set_signing_secret(
    "conn_123",
    signing_secret=os.environ["PROVIDER_SIGNING_SECRET"],
    connected_account_id="ca_456",
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**signing_secret:** `str` - The secret from the provider's app configuration, 8-4096 characters (keyword only)

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - Act on this connected account's own webhook URL (`ca_...`), for a trigger whose `ingress_per_account` is `True`; leave it out to act on the connection's URL. An empty string raises `ValueError` (keyword only)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">confirm_signing_secret_rotation</a>(connection_id, *, signing_secret_rotation_id?, connected_account_id?) -> TriggerIngressEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Finishes a signing-secret rotation so only the new secret is accepted, on the connection's URL or, with `connected_account_id`, one connected account's own URL (a malformed ID raises `ScalekitBadRequestException`). Pass the rotation's ID while one is in progress; a missing or outdated ID raises `ScalekitBadRequestException`.
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
endpoint = scalekit_client.actions.triggers.get_ingress_endpoint("conn_123")
if endpoint.rotation_in_progress:
    scalekit_client.actions.triggers.confirm_signing_secret_rotation(
        "conn_123", signing_secret_rotation_id=endpoint.signing_secret_rotation_id
    )

# One connected account's own URL (a trigger with ingress_per_account)
account_endpoint = scalekit_client.actions.triggers.get_ingress_endpoint(
    "conn_123", connected_account_id="ca_456"
)
if account_endpoint.rotation_in_progress:
    scalekit_client.actions.triggers.confirm_signing_secret_rotation(
        "conn_123",
        signing_secret_rotation_id=account_endpoint.signing_secret_rotation_id,
        connected_account_id="ca_456",
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**signing_secret_rotation_id:** `Optional[int]` - `TriggerIngressEndpoint.signing_secret_rotation_id` of the rotation to confirm

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - Act on this connected account's own webhook URL (`ca_...`), for a trigger whose `ingress_per_account` is `True`; leave it out to act on the connection's URL. An empty string raises `ValueError` (keyword only)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">generate_signing_secret</a>(connection_id, *, connected_account_id?) -> GenerateTriggerSigningSecretResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a signing secret for providers that use one Scalekit creates, for the connection's URL or, with `connected_account_id`, one connected account's own URL (a malformed ID raises `ScalekitBadRequestException`). The plaintext `signing_secret` and `url_with_secret` are returned only in this response and are left out of `repr()`. Not retried on `UNAVAILABLE`, because a retry would replace the secret. Providers that sign their own events raise `ScalekitBadRequestException` (`TRIGGER_SIGNING_SECRET_NOT_GENERATABLE`).
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
generated = scalekit_client.actions.triggers.generate_signing_secret("conn_123")
save_to_provider(generated.url_with_secret)  # your code; store it securely

# One connected account's own URL (a trigger with ingress_per_account)
generated = scalekit_client.actions.triggers.generate_signing_secret(
    "conn_123", connected_account_id="ca_456"
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

**connection_id:** `str` - The connection (`conn_...`)

</dd>
</dl>

<dl>
<dd>

**connected_account_id:** `Optional[str]` - Act on this connected account's own webhook URL (`ca_...`), for a trigger whose `ingress_per_account` is `True`; leave it out to act on the connection's URL. An empty string raises `ValueError` (keyword only)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">list_delivery_attempts_by_endpoint</a>(endpoint_id, *, page_size?) -> ListTriggerDeliveryAttemptsByEndpointResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists the most recent attempts to deliver trigger events to one of your endpoints (one page, no token). An unknown endpoint raises `ScalekitBadRequestException` (400), not `ScalekitNotFoundException`.
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
page = scalekit_client.actions.triggers.list_delivery_attempts_by_endpoint("ep_123", page_size=20)
for attempt in page.attempts:
    print(attempt.msg_id, attempt.status, attempt.response_status_code, attempt.response_duration)
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

**endpoint_id:** `str` - Your delivery endpoint

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Attempts to return; server default 20, capped at 100

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">list_deliveries</a>(endpoint_id, *, page_size?, page_token?, status?, channel?, after?, before?) -> ListTriggerDeliveriesByEndpointResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists trigger events sent to one of your endpoints, newest first, one page at a time. `after` and `before` must be timezone-aware. An unknown endpoint or `channel` raises `ScalekitBadRequestException` (400).
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
from datetime import datetime, timedelta, timezone
from scalekit.actions import TriggerDeliveryStatus

page = scalekit_client.actions.triggers.list_deliveries(
    "ep_123",
    status=TriggerDeliveryStatus.FAILED,
    after=datetime.now(timezone.utc) - timedelta(days=1),
)
print([d.msg_id for d in page.deliveries], page.next_page_token)
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

**endpoint_id:** `str` - Your delivery endpoint

</dd>
</dl>

<dl>
<dd>

**page_size:** `Optional[int]` - Messages per page; server default 20, capped at 100

</dd>
</dl>

<dl>
<dd>

**page_token:** `Optional[str]` - `next_page_token` of a previous page, with the same filters

</dd>
</dl>

<dl>
<dd>

**status:** `Optional[TriggerDeliveryStatus | str | int]` - Only messages in this delivery state

</dd>
</dl>

<dl>
<dd>

**channel:** `Optional[str]` - Only messages for this connection (`conn_...`) or subscription (`trgs_...`)

</dd>
</dl>

<dl>
<dd>

**after:** `Optional[datetime]` - Only messages after this aware instant (at most 90 days back)

</dd>
</dl>

<dl>
<dd>

**before:** `Optional[datetime]` - Only messages before this aware instant

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">list_delivery_attempts_by_message</a>(endpoint_id, msg_id) -> ListTriggerDeliveryAttemptsByMessageResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists up to 50 attempts to deliver one message to one endpoint, oldest first; `truncated` says whether more exist. An unknown endpoint or message raises `ScalekitBadRequestException` (400).
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
page = scalekit_client.actions.triggers.list_delivery_attempts_by_message("ep_123", "msg_123")
print([(a.status, a.response_status_code) for a in page.attempts], page.truncated)
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

**endpoint_id:** `str` - Your delivery endpoint

</dd>
</dl>

<dl>
<dd>

**msg_id:** `str` - The message (`msg_...`)

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">lookup_delivery</a>(delivery_id) -> LookupTriggerDeliveryResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Looks up one delivered message by its message ID (`msg_...`) or by the event ID your endpoint received (`TriggerEvent.dedupe_key`), with up to 50 attempts. Not found raises `ScalekitNotFoundException` with `error_code` `NOT_FOUND`.
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
found = scalekit_client.actions.triggers.lookup_delivery(event.dedupe_key)
print(found.msg_id, found.trigger_name, [a.status for a in found.attempts])
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

**delivery_id:** `str` - A message ID (`msg_...`) or an event ID

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">batch_lookup_deliveries</a>(delivery_ids) -> BatchLookupTriggerDeliveriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Looks up 1 to 25 messages by message ID or event ID. Every ID gets an outcome in `results` (`FOUND`, `NOT_FOUND`, `RATE_LIMITED`, `FAILED`, `NOT_ATTEMPTED`) and those never raise; attempts carry no response bodies.
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
batch = scalekit_client.actions.triggers.batch_lookup_deliveries(["msg_1", "msg_2"])
found = [r.delivery for r in batch.results if r.delivery is not None]
print(batch.found_count)
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

**delivery_ids:** `Sequence[str]` - Message IDs or event IDs, unique

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">batch_resend_deliveries</a>(targets) -> BatchResendTriggerDeliveriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Sends 1 to 50 messages to endpoints again; each target makes a real delivery attempt and gets an outcome in `results` (`QUEUED`, `NOT_FOUND`, `RATE_LIMITED`, `FAILED`, `NOT_ATTEMPTED`) that never raises. Not retried on `UNAVAILABLE`, because a retry could deliver twice.
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
batch = scalekit_client.actions.triggers.batch_resend_deliveries(
    [{"msg_id": "msg_123", "endpoint_id": "ep_123"}]
)
print(batch.queued_count, [(r.msg_id, r.outcome) for r in batch.results])
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

**targets:** `Sequence[TriggerDeliveryResendTarget | TriggerDeliveryResendTargetParam]` - Models or `{"msg_id": ..., "endpoint_id": ...}` dicts

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.actions.triggers.<a href="https://github.com/scalekit-inc/scalekit-sdk-python/blob/main/scalekit/actions/triggers.py">recover_deliveries</a>(endpoint_id, *, since, until?) -> RecoverTriggerDeliveriesResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Resends every message that failed to reach an endpoint between `since` and `until` (default now; at most 14 days, not in the future). Not retried on `UNAVAILABLE`. `ScalekitInternalServerException` means the recovery may be running anyway: check the endpoint's deliveries before calling again. An unknown endpoint raises `ScalekitNotFoundException` (`RESOURCE_NOT_FOUND`).
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
from datetime import datetime, timedelta, timezone

task = scalekit_client.actions.triggers.recover_deliveries(
    "ep_123", since=datetime.now(timezone.utc) - timedelta(hours=6)
)
print(task.task_id, task.status)  # "running" or "finished"
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

**endpoint_id:** `str` - Your delivery endpoint (`ep_...`)

</dd>
</dl>

<dl>
<dd>

**since:** `datetime` - Start of the range, timezone-aware (keyword only)

</dd>
</dl>

<dl>
<dd>

**until:** `Optional[datetime]` - End of the range, timezone-aware; default now

</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

# Reference

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
    print(f'Session: {session.id}')
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

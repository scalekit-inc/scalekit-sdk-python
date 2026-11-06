# Changelog

All notable changes to this SDK are documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

Sections up to and including 2.20.0 were imported from [GitHub Releases](https://github.com/scalekit-inc/scalekit-sdk-python/releases). Their wording is kept, with small corrections.

## [2.24.0] - 2026-11-06

This release adds per-connected-account trigger webhook URLs and signing secrets through an optional `connected_account_id` on the trigger ingress methods, a `NOT_ATTEMPTED` outcome for batch trigger subscriptions, and a `consent_ids` filter on `client.resources.list_user_consents` for fetching specific consents by ID. `ScalekitClient` now sends API version `20261106`.

### Added

- `client.actions.triggers.create_ingress_endpoint` and the other ingress and signing-secret methods take a keyword-only `connected_account_id` for triggers that deliver to one webhook URL per connected account (`AvailableTrigger.ingress_per_account`). `TriggerIngressEndpoint` gains `scope` and `connected_account_id`. Leaving it out still acts on the connection's URL. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.24.0/REFERENCE.md#triggers)

  ```python
  endpoint = client.actions.triggers.create_ingress_endpoint(
      "conn_123", connected_account_id="ca_456"
  )
  ```

- `TriggerSubscribeOutcome.NOT_ATTEMPTED` reports accounts that `client.actions.triggers.batch_create_subscriptions` did not try because an earlier account stopped the batch or time ran out. Nothing was created for them, so call again for those accounts. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.24.0/REFERENCE.md#triggers)

- `client.resources.list_user_consents(resource_id, consent_ids=[...])` fetches specific end-user consents by ID, for example to look up the `client_id` needed to revoke a consent. `consent_ids` takes up to 25 distinct IDs in the `usrcnst_<positive integer>` format and takes precedence over `user_ids` and `search`; IDs that do not exist or belong to another resource are omitted from the result. An older server ignores `consent_ids`, so confirm each returned `id` is one you asked for before revoking. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.24.0/REFERENCE.md#resources)

  ```python
  response = client.resources.list_user_consents(
      "res_123456",
      consent_ids=["usrcnst_102709535608668163", "usrcnst_102709535608668164"],
  )
  for consent in response[0].consents:
      print(consent.id, consent.client_id)
  ```

### Changed

- `ScalekitClient` now sends API version `20261106` in the `x-api-version` header on every request, so calls are served at that API version. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.24.0/REFERENCE.md#scalekitclient)

## [2.23.0] - 2026-10-30

This release adds `client.actions.triggers` for managing AgentKit triggers: subscriptions, webhook URLs and signing secrets, activity and usage, and deliveries.

### Added

- `client.actions.triggers` now manages AgentKit triggers: list a connection's triggers and eligible accounts, create and delete subscriptions singly or in batches, set up the webhook URL and rotate its signing secret, read activity and usage, and inspect, resend or recover deliveries. Results are typed, frozen models with timezone-aware `datetime`, `timedelta` and enum fields, and calls that could apply twice are not retried. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.23.0/REFERENCE.md#triggers)

  ```python
  page = client.actions.triggers.list_eligible_accounts("conn_123", "example.item.created")
  batch = client.actions.triggers.batch_create_subscriptions(
      "conn_123",
      "example.item.created",
      connected_account_ids=[a.id for a in page.accounts if a.eligible],
  )
  for r in batch.results:
      print(r.connected_account_id, r.outcome)  # TriggerSubscribeOutcome.CREATED, .REFUSED, ...
  ```

## [2.22.0] - 2026-10-28

This release fixes `client.actions.request` and `client.connect.request` sending credentials outside the proxy path (affects `>=2.4.17, <2.22.0`); upgrade promptly if you run an older version. It also adds `client.actions.upload_resumable` for large uploads, trigger event verification, AgentKit connection management, `tool_exposure` on MCP configurations, and new filters and response fields for connected accounts.

### Added

- `client.actions.upload_resumable(connection_name, identifier, path, data=...)` uploads a file of any size to Google Drive, Cloud Storage and YouTube through a connected account: the content is sent in chunks (4 MiB by default), a failed chunk resumes instead of restarting, and the call returns the created resource as a dict. `data` takes `bytes`, a binary file object or a `pathlib.Path`; if the upload session expires, the call raises `ScalekitUploadSessionExpiredException` and does not start a new one. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.22.0/AGENTKIT.md#http-proxy)

  ```python
  from pathlib import Path

  file = client.actions.upload_resumable(
      "googledrive",
      "user_123",
      "/upload/drive/v3/files",
      data=Path("video.mp4"),
      content_type="video/mp4",
      metadata={"name": "video.mp4"},
      on_progress=lambda p: print(p.bytes_committed, p.total_bytes),
  )
  print(file["id"])
  ```

- `scalekit.verify_trigger_event(body, headers=..., secret=...)` and `client.actions.triggers.verify_event(...)` verify the signature of a trigger event delivered to your endpoint and return it as a typed `TriggerEvent`; the standalone function needs no client. Any verification failure raises `WebhookVerificationError`, and a correctly signed body that is not a valid trigger event raises the new subclass `ScalekitTriggerEventParseException`. Delivery is at least once, so deduplicate on `dedupe_key` plus the connected account. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.22.0/AGENTKIT.md#trigger-events)

  ```python
  import os
  from flask import Flask, request
  from scalekit import verify_trigger_event
  from scalekit.common.exceptions import WebhookVerificationError

  app = Flask(__name__)

  @app.post("/triggers")
  def triggers():
      try:  # pass the raw body, before any JSON parsing
          event = verify_trigger_event(request.get_data(), headers=request.headers, secret=os.environ["SCALEKIT_TRIGGER_SECRET"])
      except WebhookVerificationError:  # bad signature, stale timestamp or malformed event
          return "", 400
      enqueue(event)  # your handler: deduplicate on event.dedupe_key + the connected account
      return "", 204
  ```

- `client.actions` responses now include fields the API already returned but the Python models left out. A connected account from `list_connected_accounts` gains `id`, `connection_id` and `is_org_wide_credential`, so you can pass its `id` straight to `get`, `update` and `delete` by connected account id. A connected account from `get_connected_account_auth` gains `connection_id` and `is_org_wide_credential`. A provider from `list_providers` gains `id`, `categories`, `display_priority` and `coming_soon`, and the `list_providers` response gains `prev_page_token` for paging backwards. All new fields have defaults, so existing code keeps working and nothing you read today changes. The `list_providers` documentation now says what it does: with no `provider_type` it returns only the built-in providers, and `ProviderType.ALL` or `ProviderType.CUSTOM` includes your custom providers (it used to say it returns all providers). The `get_magic_link_for_connected_account` example in `AGENTKIT.md` and `REFERENCE.md` now reads the link from `response[0].link`; it used `response[0].magic_link`, which does not exist and raised `AttributeError`. The `request` docs now say that the proxy call times out after 30 seconds by default and that you can pass `timeout=<seconds>` for slower provider calls. The method documentation now lists parameters that existed but were not documented: `connection_name` on `client.tools.execute_tool`, `connection_names` on `list_connected_accounts`, `state` and `user_verify_url` on `get_magic_link_for_connected_account`, and `filter_mcp_server_url` on `client.mcp.list_configs`. `ensure_instance` is documented with `name` as the required first argument (it was shown as optional, and leaving it out raises `TypeError`). Two `REFERENCE.md` examples that read `session.id` and `client.id` now use `session.session_id` and `client.client_id`, which are the real field names. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.22.0/REFERENCE.md#connected-accounts)

- `list_connected_accounts` (on `client.connected_accounts` and `client.actions`) now takes `query` and `is_org_wide_credential`. `query` searches connected accounts by text (up to 100 characters, ignoring case) across the account identifier, the provider, the connection name and the provider's display name. Before, `client.actions.list_connected_accounts(query=...)` was accepted but silently ignored, and returned every account. `is_org_wide_credential=True` returns only the account that holds the shared credential of an organization-wide connection, and `False` returns only the per-user accounts; leave it unset to get both. When `query` is given, only the connection name and the paging options narrow the search, so use `identifier`, `provider`, `connection_names` and `is_org_wide_credential` without it. Both parameters are optional and added after the existing ones, so existing calls behave as before. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.22.0/REFERENCE.md#connected-accounts)

- `client.actions.mcp.create_config(...)` and `update_config(...)` take an optional `tool_exposure` (`"DIRECT"` or `"META"`), and `McpConfig.tool_exposure` reports it. `DIRECT` (the default) lists every mapped tool and allows at most 25 connections; `META` gives agents five search and execute tools with no connection limit and must be enabled for your environment. Existing code keeps working: leave `tool_exposure` out and you get `DIRECT`, and an update that omits it never changes the stored mode. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.22.0/AGENTKIT.md#mcp-mcpclient)

  ```python
  config = client.actions.mcp.create_config(
      name="support-agent",
      connection_tool_mappings=[...],
      tool_exposure="META",
  )
  client.actions.mcp.update_config(config_id, tool_exposure="DIRECT")
  ```

- New `client.actions` methods manage AgentKit connections: `create_connection`, `get_connection`, `list_app_connections`, `update_connection` and `delete_connection`. Updates send only what you pass (a list or map passed empty clears it), connections are addressed by name or id, and failures raise typed `AgentKitConnectionError` subclasses with `code`, `step` and `retryable`. Typed settings (`OAuthSettings`, `GoogleDWDSettings`, `ProviderConfigurations`, `AuthMode`) live in `scalekit.actions.connections`. Existing methods are unchanged. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.22.0/AGENTKIT.md#agentkit-connections)

  ```python
  from scalekit.actions.connections import OAuthSettings

  client.actions.create_connection("gmail", connection_name="gmail-work")
  client.actions.update_connection("gmail-work", oauth=OAuthSettings(client_id="...", client_secret="..."))
  conn = client.actions.get_connection("gmail-work")
  ```

### Security

- `client.actions.request(...)` and `client.connect.request(...)` could send the client's bearer token and the `connection_name` and `identifier` headers outside `<environment URL>/proxy/` when `path` resolved outside that prefix or a proxied API redirected outside it. They now raise `ValueError` before sending anything when `path` could be routed outside the prefix: for example through `..` segments, including percent-encoded or backslash forms, or `v1/users`, which without a leading `/` would be sent to `/proxyv1/users`. With an `http://` environment URL, the check also covers the URL a forward proxy would receive, whether or not one is configured. A redirect outside the prefix is still followed, but without those credentials. Every other path and redirect is sent exactly as before.

  - **Affected versions:** `>=2.4.17, <2.22.0`
  - **Patched versions:** `2.22.0`
  - **Action:** upgrade. This matters most if you build `path` from untrusted input, such as values supplied by end users or by an AI agent, or call APIs whose responses you do not control. If a call now raises `ValueError` for a path such as `v1/users`, add the leading `/`.

## [2.21.0] - 2026-10-12

This release adds `connection_name` to `client.actions.mcp.create_session_token`, for minting a session token for a connection's own MCP server.

### Added

- `client.actions.mcp.create_session_token(connection_name=..., identifier=...)` mints a session token for a connection's own MCP server (`<environment URL>/mcp/v3/connections/<connection name>`), which serves all of that connection's tools without an MCP configuration. Pass exactly one of `mcp_config_id` or the new keyword-only `connection_name`; `expiry` and `access_level` work for both, and `access_level="READ_ONLY"` limits the token to read-only tools. The URL path is case-sensitive, so connect with the connection's name exactly as stored. Existing calls with `mcp_config_id`, positional or keyword, are unchanged. `client.mcp.create_session_token` takes the same arguments and returns the raw `(response, call)` tuple. [Reference](https://github.com/scalekit-inc/scalekit-sdk-python/blob/v2.21.0/AGENTKIT.md#mcp-mcpclient)

  ```python
  from datetime import timedelta

  resp = client.actions.mcp.create_session_token(
      connection_name="gmail",
      identifier="user_123",
      expiry=timedelta(minutes=15),
      access_level="READ_ONLY",
  )
  headers = {"Authorization": f"Bearer {resp.token}"}
  ```

## [2.20.0] - 2026-10-05

### Changes

- [SK-2030] fix: accept every auth-pattern shape the API serves (was Literal-constrained) ([#206](https://github.com/scalekit-inc/scalekit-sdk-python/pull/206))
- [SK-2043] chore: update proto to v0.1.150.0 (v2.19.2) ([#207](https://github.com/scalekit-inc/scalekit-sdk-python/pull/207))
- chore: add PyPI alias packages for scalekit and scalekit-sdk (SK-2063) ([#208](https://github.com/scalekit-inc/scalekit-sdk-python/pull/208))
- fix: forward page_size and page_token in actions.list_connected_accounts ([#211](https://github.com/scalekit-inc/scalekit-sdk-python/pull/211))
- Add Create/Update/Delete/List/Get to ResourceClient ([#204](https://github.com/scalekit-inc/scalekit-sdk-python/pull/204))
- feat: accept multiple issuers in token validation (SK-2080) ([#212](https://github.com/scalekit-inc/scalekit-sdk-python/pull/212))

## [2.19.1] - 2026-09-11

### Changes

- [SK-1912] feat: add resources client for listing and revoking user consents ([#200](https://github.com/scalekit-inc/scalekit-sdk-python/pull/200))
- [SK-1867] fix: add client-side idle-connection timeout (grpc.client_idle_timeout_ms) ([#203](https://github.com/scalekit-inc/scalekit-sdk-python/pull/203))

## [2.19.0] - 2026-09-10

### Changes

- [SK-1291] feat(tools): add SearchTools RPC support ([#197](https://github.com/scalekit-inc/scalekit-sdk-python/pull/197))
- [SK-1867] fix: add configurable per-call gRPC timeout to grpc_exec ([#198](https://github.com/scalekit-inc/scalekit-sdk-python/pull/198))
- Add list_tools method to actions facade with ListToolsResponse ([#201](https://github.com/scalekit-inc/scalekit-sdk-python/pull/201))

## [2.18.0] - 2026-09-03

### Changes

- [SK-1867] fix: add gRPC keepalive options to detect dead idle connections ([#195](https://github.com/scalekit-inc/scalekit-sdk-python/pull/195))

## [2.17.0] - 2026-08-18

### Changes

#### Native middleware support for (Flask, FastAPI, Django) based Python webapps!

## [2.16.0] - 2026-07-27

### Changes

- [SK-111] Add new members as code owners ([#186](https://github.com/scalekit-inc/scalekit-sdk-python/pull/186))
- [SK-1339] feat: typed UpdateLoginUserDetails response + listEventsPaginated ([#187](https://github.com/scalekit-inc/scalekit-sdk-python/pull/187))

## [2.15.0] - 2026-07-17

### Changes

- chore: update proto to v0.1.138.0 (v2.15.0); add metadata/icon_src to actions provider facade ([#182](https://github.com/scalekit-inc/scalekit-sdk-python/pull/182))

## [2.14.0] - 2026-07-17

### Changes

- chore(deps): bump proto version to v0.1.136.1 and regenerate SDK ([#177](https://github.com/scalekit-inc/scalekit-sdk-python/pull/177))
- [SK-1276] Bump proto to v0.1.137.0 and expand custom-connector support (NO_AUTH, icon_src/metadata, auth_header_key_override) ([#179](https://github.com/scalekit-inc/scalekit-sdk-python/pull/179))
- [SK-1276] Bump SDK version to 2.14.0 and API version to 20260716 ([#180](https://github.com/scalekit-inc/scalekit-sdk-python/pull/180))

## [2.13.0] - 2026-07-07

### Changes

- [SK-631] chore(deps): bump 5 low-risk Python deps ([#167](https://github.com/scalekit-inc/scalekit-sdk-python/pull/167))
- [SK-636] chore(deps): align grpcio + grpcio-status to >=1.81.0 ([#168](https://github.com/scalekit-inc/scalekit-sdk-python/pull/168))
- [SK-641] chore(deps): unpin cryptography to >=46.0.6,<49 ([#169](https://github.com/scalekit-inc/scalekit-sdk-python/pull/169))
- [SK-642] chore(deps): bump protobuf upper bound to >=5.29.5,<8.0.0 ([#170](https://github.com/scalekit-inc/scalekit-sdk-python/pull/170))
- [SK-646] chore(deps): bump 5 low-risk Python deps ([#171](https://github.com/scalekit-inc/scalekit-sdk-python/pull/171))
- fix(SK-819, SK-821): provider error differentiation, blind retry fix, and upsert credentials ([#174](https://github.com/scalekit-inc/scalekit-sdk-python/pull/174))

## [2.12.0] - 2026-06-08

### Changes

- Redshift connectors ([#165](https://github.com/scalekit-inc/scalekit-sdk-python/pull/165))

## [2.11.0] - 2026-06-04

### Changes

- feat: regenerate protos from v0.1.123.0 and add slug/logo_url to CreateOrganizationOptions ([#162](https://github.com/scalekit-inc/scalekit-sdk-python/pull/162))
- feat: SDK support for proto v0.1.127.0 — MCP session tokens, connected account auth state, and filter improvements ([#164](https://github.com/scalekit-inc/scalekit-sdk-python/pull/164))

## [2.10.0] - 2026-05-13

### Changes

- docs: add AGENTKIT.md for AgentKit APIs ([#142](https://github.com/scalekit-inc/scalekit-sdk-python/pull/142))
- Update protos with v0.1.121.2 ([#157](https://github.com/scalekit-inc/scalekit-sdk-python/pull/157))
- feat: custom provider CRUD for MCP connectors ([#159](https://github.com/scalekit-inc/scalekit-sdk-python/pull/159))
- feat: add Google Domain-Wide Delegation (GOOGLE_DWD) auth support ([#153](https://github.com/scalekit-inc/scalekit-sdk-python/pull/153))
- feat: organization session policy SDK methods ([#152](https://github.com/scalekit-inc/scalekit-sdk-python/pull/152))

## [2.9.0] - 2026-04-29

### Changes

- Support XML/SOAP proxy requests and expose connected account details ([#148](https://github.com/scalekit-inc/scalekit-sdk-python/pull/148))

## [2.8.0] - 2026-04-22

### Changes

- Fix Makefile and bump up api_version ([#146](https://github.com/scalekit-inc/scalekit-sdk-python/pull/146))
- Sync proto updates for providers/tools and add custom MCP tests ([#147](https://github.com/scalekit-inc/scalekit-sdk-python/pull/147))
- Add GitHub Actions release workflow to publish to PyPI ([#145](https://github.com/scalekit-inc/scalekit-sdk-python/pull/145))

## [2.7.3] - 2026-04-16

### Changes

- add-enum-m2m ([#143](https://github.com/scalekit-inc/scalekit-sdk-python/pull/143))
- Regenerate pb2 to include OAUTH_M2M; bump to 2.7.3 ([#144](https://github.com/scalekit-inc/scalekit-sdk-python/pull/144))

## [2.7.1] - 2026-04-15

### Changes

- make authorization optional ([#132](https://github.com/scalekit-inc/scalekit-sdk-python/pull/132))
- docs: rename reference.md to REFERENCE.md ([#134](https://github.com/scalekit-inc/scalekit-sdk-python/pull/134))
- [SK-2671] feat(roles): add update_default_roles and list_dependent_roles ([#135](https://github.com/scalekit-inc/scalekit-sdk-python/pull/135))
- [SK-2668] feat(users): add list_user_roles and list_user_permissions ([#133](https://github.com/scalekit-inc/scalekit-sdk-python/pull/133))
- [SK-2659] feat(token): add update_token method ([#130](https://github.com/scalekit-inc/scalekit-sdk-python/pull/130))
- fix: docstring fixes, method additions, and version bump to 2.6.0 ([#131](https://github.com/scalekit-inc/scalekit-sdk-python/pull/131))
- Removed redundant connected account test cases ([#138](https://github.com/scalekit-inc/scalekit-sdk-python/pull/138))
- Updated dependency versions to fix vulnerabilities reported by dependabot ([#141](https://github.com/scalekit-inc/scalekit-sdk-python/pull/141))
- Add connected account user verification flow ([#136](https://github.com/scalekit-inc/scalekit-sdk-python/pull/136))

## [2.6.0] - 2026-03-10

### Changes

- Fix incorrect :returns: docstrings
- feat: add delete_role_base for env-level role inheritance removal
- fix: make page_size optional in list_organizations to match other SDKs
- feat: add get_client_access_token to Python SDK
- fix: generate_client_token returns token string, not full response dict
- fix: correct role.py docstrings (role_id -> role_name) and fix tearDown error handling
- fix: tolerate INVALID_ARGUMENT and NOT_FOUND in external_id tearDown cleanup

## [2.5.0] - 2026-02-27

### Changes

Add Proxy Tool Calling - Beta.
API Tokens

## [2.4.16] - 2026-01-14

### Changes

- update mcp module version ([#113](https://github.com/scalekit-inc/scalekit-sdk-python/pull/113))
- remove requirements.txt as its unused ([#114](https://github.com/scalekit-inc/scalekit-sdk-python/pull/114))
- Appended expiry time to response obj from authenticate_with_code() ([#116](https://github.com/scalekit-inc/scalekit-sdk-python/pull/116))
- Add WebAuthn client ([#115](https://github.com/scalekit-inc/scalekit-sdk-python/pull/115))
- Add domain type for create and list domain apis ([#117](https://github.com/scalekit-inc/scalekit-sdk-python/pull/117))

#### Domain API Changes - Release Notes

#### Enhanced Domain Management

#### Domain Type Support
- Added support for domain types to distinguish between different domain configurations:
  - `ALLOWED_EMAIL_DOMAIN`: Trusted domains used to suggest organizations in the organization switcher during sign-in/sign-up
  - `ORGANIZATION_DOMAIN`: SSO discovery domains used to route users to the correct SSO provider and enforce SSO
  - `UNSPECIFIED`: Default type for backward compatibility

#### API Enhancements

**`create_domain()`**
- Added optional `domain_type` parameter (accepts string or `DomainType` enum)
- When not specified, defaults to `ORGANIZATION_DOMAIN` for backward compatibility
- Supports flexible input: strings like `"ALLOWED_EMAIL_DOMAIN"` or enum values

**`list_domains()`**
- Added optional `domain_type` parameter for filtering domains by type
- When not specified, returns all domains regardless of type
- Enables targeted queries for specific domain configurations

## [2.4.14] - 2025-12-22

### Changes

- Update pyjwt requirement from <2.10,>=2.8 to >=2.8,<2.11  in https://github.com/scalekit-inc/scalekit-sdk-python/pull/48
- Library Upgrades & minor performance improvements  in https://github.com/scalekit-inc/scalekit-sdk-python/pull/112

## [2.4.13] - 2025-11-19

### Changes

#### New sdk methods

- Add upsert_user_management_settings sdk method to OrganizationClient ([#110](https://github.com/scalekit-inc/scalekit-sdk-python/pull/110))

## [2.4.12] - 2025-11-13

### Changes

- Add AuthClient for updating login user details and generate proto files to support given_name and family_name in user object  in https://github.com/scalekit-inc/scalekit-sdk-python/pull/109

## [2.4.11] - 2025-11-06

### Changes

- Actions: Dynamic MCP support ([#106](https://github.com/scalekit-inc/scalekit-sdk-python/pull/106))

## [2.4.10] - 2025-10-30

### Changes

- fix authenticate with code ([#105](https://github.com/scalekit-inc/scalekit-sdk-python/pull/105))

## [2.4.9] - 2025-10-30

### Changes

- Refresh Expired Client Access Token

## [2.4.8] - 2025-10-30

### Changes

- add RevokeAllUserSessions method and enhance getUserSessions with filter options ([#100](https://github.com/scalekit-inc/scalekit-sdk-python/pull/100))

## [2.4.7] - 2025-10-10

### Changes

- Google adk support ([#98](https://github.com/scalekit-inc/scalekit-sdk-python/pull/98))
- Connected account update ([#101](https://github.com/scalekit-inc/scalekit-sdk-python/pull/101))

## [2.4.4] - 2025-09-18

### Changes

- Generated proto files -  rename invited_by to inviter_email

## [2.4.3] - 2025-09-16

### Changes

- Upgrade pydantic dependency constraint from ~2.10.6 to ~2.11.2 ([#94](https://github.com/scalekit-inc/scalekit-sdk-python/pull/94))
- Bump version to 2.4.3 ([#95](https://github.com/scalekit-inc/scalekit-sdk-python/pull/95))

## [2.4.2] - 2025-09-15

### Changes

- Use string literal type annotations for TemplateType and DomainType ([#86](https://github.com/scalekit-inc/scalekit-sdk-python/pull/86))
- Enhance README with Agent-First Positioning ([#88](https://github.com/scalekit-inc/scalekit-sdk-python/pull/88))
- Change Connection to actions ([#90](https://github.com/scalekit-inc/scalekit-sdk-python/pull/90))
- Add Permission and Org Role sdk methods ([#89](https://github.com/scalekit-inc/scalekit-sdk-python/pull/89))
- Add SessionsClient  sdk methods ([#91](https://github.com/scalekit-inc/scalekit-sdk-python/pull/91))

## [2.4.0] - 2025-09-03

### Changes

- Feature connected accounts ([#73](https://github.com/scalekit-inc/scalekit-sdk-python/pull/73))
- Add resend_invite method ([#77](https://github.com/scalekit-inc/scalekit-sdk-python/pull/77))
- [SK-2059] Update Test Cases to utilize new error handling capability ([#76](https://github.com/scalekit-inc/scalekit-sdk-python/pull/76))
- Add Langchain support for Scalekit SDK ([#79](https://github.com/scalekit-inc/scalekit-sdk-python/pull/79))
- Relax python-dotenv constraint to >=1.1.0 ([#83](https://github.com/scalekit-inc/scalekit-sdk-python/pull/83))
- Add delete domain sdk method & domain_type parameter to create_domain method and update proto files ([#82](https://github.com/scalekit-inc/scalekit-sdk-python/pull/82))

## [2.3.0] - 2025-08-01

### Changes

- add passwordless sdk methods ([#65](https://github.com/scalekit-inc/scalekit-sdk-python/pull/65))
- Update Error Handling for Python SDK ([#66](https://github.com/scalekit-inc/scalekit-sdk-python/pull/66))
- add scope validation in validate_token method ([#68](https://github.com/scalekit-inc/scalekit-sdk-python/pull/68))

## [2.2.1] - 2025-07-16

### Changes

- Implemented sdk methods for environment roles ([#61](https://github.com/scalekit-inc/scalekit-sdk-python/pull/61))

## [2.2.0] - 2025-07-18

### Changes

- add list_organization_clients sdk method ([#64](https://github.com/scalekit-inc/scalekit-sdk-python/pull/64))

## [2.0.1] - 2025-07-09

### Changes

- Upgrade setuptools version to >=78.1.1 ([#58](https://github.com/scalekit-inc/scalekit-sdk-python/pull/58))
- return refresh token and handle errors in authenticate_with_code ,skip audience validation in validate_access_token if audience is not passed ([#60](https://github.com/scalekit-inc/scalekit-sdk-python/pull/60))

## [2.0.0] - 2025-06-26

### Changes

#### 🚀 What's New?

This is a major release that introduces **Full Stack Authentication (FSA)** capabilities to the Python SDK. This empowers developers to build comprehensive, enterprise-ready authentication and user management into their applications with minimal code.

With this release, developers can now programmatically:
-   Implement passwordless sign-in using magic links and one-time passcodes.
-   Connect to any enterprise identity provider via SAML and OIDC for Single Sign-On (SSO).
-   Manage the entire user lifecycle, including invitations, role-based access control (RBAC), and provisioning.
-   Enforce advanced security policies such as session duration and idle timeouts at the organization level.

#### 🆕 Full Stack Authentication Support Added

The SDK has been significantly updated to provide a complete interface for Scalekit's Full Stack Authentication platform. This includes:

-   **Authentication Methods**: New clients and methods for handling passwordless, social, and enterprise SSO authentication flows in a unified manner.
-   **User Management**: A comprehensive set of APIs to create, read, update, and delete users and their role assignments.
-   **Organization Management**: Full programmatic control over organization settings, including security policies and domain management.

Please refer to the [official documentation](https://docs.scalekit.com) and migration guide to upgrade your application to `v2.0.0`.

## [1.1.0] - 2025-05-16

### Changes

#### :rocket: What's New?
- The `authenticate_with_code` method now returns `organization_id` and `connection_id` in addition to user details and tokens. This provides more context to the frontend upon successful authentication.
---
#### :sparkles: Enhancements
- **Authentication Data Enrichment:** The `authenticate_with_code` method in `scalekit/client.py` has been updated to include `organization_id` and `connection_id` in its return value. This change was implemented to better support frontend requirements by providing these identifiers directly after the authentication process.
- **Type Hint Correction:** Corrected the return type hint for the `list_organizations` method in `scalekit/organization.py` from `CreateOrganizationResponse` to `ListOrganizationsResponse` for better accuracy.

## [1.0.9] - 2025-05-16

### Changes

#### 🚀 What's New?

- Developers can now programmatically:
  - Create and manage M2M clients
  - Handle organization client secrets
  - Validate M2M tokens
  - Update organization client configurations

---

#### 🆕 M2M Client Support Added

- Introduced new Machine-to-Machine (M2M) authentication features to the Python SDK
- Added a new `M2MClient` class (`scalekit/m2m_client.py`) for managing M2M authentication
- Updated `ScalekitClient` to include M2M client management capabilities
- New methods for organization client management in `scalekit/client.py`

---

#### 🧪 Testing Improvements

- Replaced unit tests with comprehensive integration tests
- Introduced Makefile for automated rebuild process
- Enhanced test coverage for M2M client functionality
- Added test documentation in `tests/TEST_README.md`

---

#### ✨ Enhancements

- Added token validation method for enhanced security
- Improved client secret management capabilities
- Minor bug fixes and refactoring across multiple files

---

#### 📚 Notes

- Applications integrating with the SDK can now utilize M2M authentication
- Review new classes and methods for M2M client support

## [1.0.6] - 2025-05-16

### Changes

#### 🚀 What's New

Developers can now delete SSO connections and SCIM directories through the SDK.

---

#### 🛠️ Enhancements & Changes

- Added `delete_connection()` to the Connections API.
- Added `delete_directory()` to the Directories API.
- These methods allow programmatic deletion of connections and directories for a given organization.

## [1.0.5] - 2025-05-16

### Changes

#### 🚀 What's New?

- Developers can now create a SSO connections and directory sync through SDK.
- Generate admin portal specific to an enterprise connection — either an SSO or Directory connection.

---

#### ✨ Enhancements

- The generate_portal_link method now supports generating feature-specific portal links.
- Added a create_connection method for streamlined creation of organization connections.
- Added a create_directory method for easier directory creation by organization ID.

## [1.0.4] - 2025-05-16

### Changes

#### 🚀 What's New?

- Developers can now programmatically:
  - List users and groups from directory.
  - Enable and disable directory sync.
  - Get directory details
- The [security vulnerability](https://cryptography.io/en/42.0.8/security/) identified by crypotography dependency is fixed promptly.

---

#### 🆕 SCIM Support Added

- Introduced new SCIM (System for Cross-domain Identity Management) features to the Python SDK.
- Added a new `DirectoryClient` class (`scalekit/directory.py`) for managing directories, users, and groups.
- Updated `ScalekitClient` to include directory management capabilities.
- New utility classes for directory handling in `scalekit/utils/directory.py`.

---

#### 🔒 Security Improvements

- Fixed OpenSSL vulnerability in core authentication flow.
- Improved error handling during client authentication (`scalekit/core.py`).

---

#### ✨ Enhancements

- Webhook signature verification logic added to `ScalekitClient`.
- Organization settings update method added to `OrganizationClient`.
- Protocol buffer definitions updated for improved client and directory management.
- Minor bug fixes and refactoring across multiple files.

## [1.0.3] - 2024-08-27

### Changes

- Fix version ([#14](https://github.com/scalekit-inc/scalekit-sdk-python/pull/14))
- Feat idp initiated login claim ([#23](https://github.com/scalekit-inc/scalekit-sdk-python/pull/23))
- Release v1.0.3 ([#28](https://github.com/scalekit-inc/scalekit-sdk-python/pull/28))

## [1.0.2] - 2024-07-18

### Changes

- Update readme ([#5](https://github.com/scalekit-inc/scalekit-sdk-python/pull/5))
- Add dependabot ([#6](https://github.com/scalekit-inc/scalekit-sdk-python/pull/6))
- Update proto and add provider support for social connections ([#7](https://github.com/scalekit-inc/scalekit-sdk-python/pull/7))

## [1.0.1] - 2024-06-13

### Changes

- First Release of the official Scalekit Python SDK

[2.24.0]: https://github.com/scalekit-inc/scalekit-sdk-python/compare/v2.23.0...v2.24.0
[2.23.0]: https://github.com/scalekit-inc/scalekit-sdk-python/compare/v2.22.0...v2.23.0
[2.22.0]: https://github.com/scalekit-inc/scalekit-sdk-python/compare/v2.21.0...v2.22.0
[2.21.0]: https://github.com/scalekit-inc/scalekit-sdk-python/compare/v2.20.0...v2.21.0
[2.20.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.20.0
[2.19.1]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.19.1
[2.19.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.19.0
[2.18.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.18.0
[2.17.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.17.0
[2.16.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.16.0
[2.15.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.15.0
[2.14.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.14.0
[2.13.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.13.0
[2.12.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/V2.12.0
[2.11.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.11.0
[2.10.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.10.0
[2.9.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.9.0
[2.8.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.8.0
[2.7.3]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.7.3
[2.7.1]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.7.1
[2.6.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.6.0
[2.5.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.5.0
[2.4.16]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/2.4.16
[2.4.14]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.14
[2.4.13]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.13
[2.4.12]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.12
[2.4.11]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.11
[2.4.10]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.10
[2.4.9]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.9
[2.4.8]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.8
[2.4.7]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.7
[2.4.4]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.4
[2.4.3]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.3
[2.4.2]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.2
[2.4.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.4.0
[2.3.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.3.0
[2.2.1]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.2.1
[2.2.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.2.0
[2.0.1]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.0.1
[2.0.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v2.0.0
[1.1.0]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.1.0
[1.0.9]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.0.9
[1.0.6]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.0.6
[1.0.5]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.0.5
[1.0.4]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.0.4
[1.0.3]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.0.3
[1.0.2]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.0.2
[1.0.1]: https://github.com/scalekit-inc/scalekit-sdk-python/releases/tag/v1.0.1

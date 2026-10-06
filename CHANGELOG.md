# Changelog

All notable changes to this SDK are documented in this file. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/).

Sections up to and including 2.20.0 were imported from [GitHub Releases](https://github.com/scalekit-inc/scalekit-sdk-python/releases). They keep their original wording.

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
- Add resend_invite method  @dhaneshbs in https://github.com/scalekit-inc/scalekit-sdk-python/pull/77
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

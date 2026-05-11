<div align="center">

<a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">
  <picture>
    <img src="./images/scalekit.jpg" alt="Scalekit" height="64">
  </picture>
</a>

<p><strong>Official Python SDK for Scalekit — the auth stack for agents.</strong><br>
authentication, authorization, and tool-calling for human-in-the-loop and autonomous agent flows.</p>

[![PyPI version](https://img.shields.io/pypi/v/scalekit-sdk-python.svg)](https://pypi.org/project/scalekit-sdk-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/pypi/pyversions/scalekit-sdk-python.svg)](https://pypi.org/project/scalekit-sdk-python)

**[📖 Documentation](https://docs.scalekit.com)** · **[🐛 Report an Issue](https://github.com/scalekit-inc/scalekit-sdk-python/issues)** · **[💬 Join our Slack](https://join.slack.com/t/scalekit-community/shared_invite/zt-3gsxwr4hc-0tvhwT2b_qgVSIZQBQCWRw)**

</div>

---

this is the official Python SDK for [Scalekit](https://scalekit.com), — the auth stack for agents. Build secure AI products faster with authentication for humans (SSO, passwordless, full-stack auth) and agents (Mcp/APIs, delegated actions), all unified on one platform.
This Python SDK enables both traditional B2B authentication and cutting-edge agentic workflows.
#### Agent-First Features
- **Agent Identity** — Agents as first-class actors with human ownership and org context
- **MCP-Native OAuth 2.1** — Purpose-built for Model Context Protocol with DCR/PKCE support
- **Ephemeral Credentials** — Time-bound, task-based authorization (minutes, not days)
- **Token Vault** — per-user, per-tool token storage with rotation and progressive consent
- **Human-in-the-Loop** — step-up authentication when risk crosses thresholds
- **Immutable Audit** — track which user initiated, which agent acted, what resource was accessed
#### Human Authentication
- **Enterprise SSO** — support for SAML and OIDC protocols
- **SCIM Provisioning** — automated user provisioning and deprovisioning
- **Passwordless Authentication** — magic links, OTP, and modern auth flows
- **Multi-tenant Architecture** — organization-level authentication policies
- **Social Logins** — support for popular social identity providers
- **Full-Stack Auth** — complete IdP-of-record solution for B2B SaaS
- **Pythonic API** — idiomatic Python with clean, intuitive interfaces
---
### Getting started
#### Prerequisites
- **Python** ≥ 3.8
- [Scalekit account](https://scalekit.com) with `env_url`, `client_id`, and `client_secret`
#### Installation
```sh
pip install scalekit-sdk-python
# or
poetry add scalekit-sdk-python
```
#### Usage
```python
from scalekit import ScalekitClient

scalekit_client = ScalekitClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    env_url="https://your-env.scalekit.com"
)

# use scalekit_client to interact with the Scalekit API
auth_url = scalekit_client.get_authorization_url(
    "https://acme-corp.com/redirect-uri",
    state="state",
    connection_id="con_123456789"
)
```
---
### Example — SSO with FastAPI
```python
from fastapi import FastAPI, Request, Response
from scalekit import ScalekitClient

app = FastAPI()
scalekit_client = ScalekitClient(
    env_url="https://your-env.scalekit.com",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
redirect_uri = "http://localhost:8000/auth/callback"

@app.get("/auth/login")
async def auth_login(request: Request):
    auth_url = scalekit_client.get_authorization_url(
        redirect_uri,
        state="state",
        connection_id="con_123456789"
    )
    return Response(status_code=302, headers={"Location": auth_url})
@app.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    token = scalekit_client.authenticate_with_code(code, redirect_uri)
    response = Response(content="Authenticated successfully")
    response.set_cookie(
        "access_token",
        token["access_token"],
        httponly=True,
        secure=True,
        samesite="Lax"
    )
    return response
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8080)
```
```

| Framework | Repository | Description |
|-----------|------------|-------------|
| **FastAPI** | [scalekit-fastapi-example](https://github.com/scalekit-developers/scalekit-fastapi-example) | Modern async Python API framework |
| **Django** | [scalekit-django-auth-example](https://github.com/scalekit-inc/scalekit-django-auth-example) | Django web framework integration |
| **Flask** | [scalekit-flask-auth-example](https://github.com/scalekit-inc/scalekit-flask-auth-example) | Flask microframework integration |

---
### Helpful links
#### Quickstart Guides
- [SSO Integration](https://docs.scalekit.com/sso/quickstart/) — implement enterprise Single Sign-on
- [Full Stack Auth](https://docs.scalekit.com/fsa/quickstart/) — complete authentication solution
- [Passwordless Auth](https://docs.scalekit.com/passwordless/quickstart/) — modern authentication flows
- [Social Logins](https://docs.scalekit.com/social-logins/quickstart/) — popular social identity providers
- [Machine-to-Machine](https://docs.scalekit.com/m2m/quickstart/) — API authentication
#### Documentation & Reference
- [API Reference](https://docs.scalekit.com/apis) — complete API documentation
- [Developer Kit](https://docs.scalekit.com/dev-kit/) — tools and utilities
- [API authentication guide](https://docs.scalekit.com/guides/authenticate-scalekit-api/) — secure API access
#### Additional resources
- [Setup Guide](https://docs.scalekit.com/guides/setup-scalekit/) — initial platform configuration
- [Code examples](https://docs.scalekit.com/directory/code-examples/) — ready-to-use code snippets
- [Admin Portal Guide](https://docs.scalekit.com/directory/guides/admin-portal/) — administrative interface
- [Launch Checklist](https://docs.scalekit.com/directory/guides/launch-checklist/) — pre-production checklist
---
### Contributing

Contributions are welcome! Coming soon: contribution guidelines.

For now:
1. Fork this repository
2. Create a branch — `git checkout -b fix/my-improvement`
3. Make your changes
4. Run tests — `pytest`
5. Open a Pull Request

---
### License
This project is licensed under the **MIT license**. See the [LICENSE](LICENSE) file for more information.

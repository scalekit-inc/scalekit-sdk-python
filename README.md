<p align="left">
  <a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <img src="https://cdn.scalekit.cloud/v1/scalekit-logo-dark.svg" height="64">
    </picture>
  </a>
  <br/>
</p>

# Official Python SDK

[![PyPI version](https://img.shields.io/pypi/v/scalekit-sdk-python.svg?style=flat-square)](https://pypi.org/project/scalekit-sdk-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/pypi/pyversions/scalekit-sdk-python.svg?style=flat-square)](https://pypi.org/project/scalekit-sdk-python/)

<a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">Scalekit</a> is the **auth stack for AI apps** - from human authentication to agent authorization. Build secure AI products faster with authentication for humans (SSO, passwordless, full-stack auth) and agents (MCP/APIs, delegated actions), all unified on one platform. This Python SDK enables both traditional B2B authentication and cutting-edge agentic workflows.

## 🤖 Agent-First Features

- **🔐 Agent Identity**: Agents as first-class actors with human ownership and org context
- **🎯 MCP-Native OAuth 2.1**: Purpose-built for Model Context Protocol with DCR/PKCE support
- **⏰ Ephemeral Credentials**: Time-bound, task-based authorization (minutes, not days)
- **🔒 Token Vault**: Per-user, per-tool token storage with rotation and progressive consent
- **👥 Human-in-the-Loop**: Step-up authentication when risk crosses thresholds
- **📊 Immutable Audit**: Track which user initiated, which agent acted, what resource was accessed

## 👨‍💼 Human Authentication

- **🔐 Enterprise SSO**: Support for SAML and OIDC protocols
- **👥 SCIM Provisioning**: Automated user provisioning and deprovisioning  
- **🚀 Passwordless Authentication**: Magic links, OTP, and modern auth flows
- **🏢 Multi-tenant Architecture**: Organization-level authentication policies
- **📱 Social Logins**: Support for popular social identity providers
- **🛡️ Full-Stack Auth**: Complete IdP-of-record solution for B2B SaaS
- **🐍 Pythonic API**: Clean, intuitive interface following Python conventions

<div>
📚 <a target="_blank" href="https://docs.scalekit.com">Documentation</a> • 🚀 <a target="_blank" href="https://docs.scalekit.com/sso/quickstart/">SSO Quickstart</a> • 💻 <a target="_blank" href="https://docs.scalekit.com/apis">API Reference</a>
</div>
<hr />

## Pre-requisites

1. [Sign up](https://scalekit.com) for a Scalekit account.
2. Get your ```env_url```, ```client_id``` and ```client_secret``` from the Scalekit dashboard.

## Installation

Install Scalekit SDK using your preferred package manager. 

```sh
pip install scalekit-sdk-python

```

## Usage

```py

from scalekit import ScalekitClient

sc = ScalekitClient(
  env_url, 
  client_id, 
  client_secret
)

# Use the sc object to interact with the Scalekit API
auth_url = sc.get_authorization_url(
  "https://acme-corp.com/redirect-uri",
  state="state",
  connection_id="con_123456789"
)

```

##### Minimum Requirements

To use the Scalekit Python SDK, you must have the following:

| Component | Version |
| --------- | ------- |
| Python    | 3.8+    |

> **Tip:** Although Python 3.8 meets the minimum requirement, using a more recent version (such as Python 3.9 or later) is advisable.


## Examples - SSO with FastAPI

Below is a simple code sample that showcases how to implement Single Sign-on using Scalekit SDK

```py
from fastapi import FastAPI, Request, Response
from scalekit import ScalekitClient
import uvicorn

app = FastAPI()

sc = ScalekitClient(
  env_url, 
  client_id, 
  client_secret
)

redirect_uri = "http://localhost:8000/auth/callback"

@app.get("/auth/login")
async def auth_login(request: Request):
  auth_url = sc.get_authorization_url(
    redirect_uri,
    state="state",
    connection_id="con_123456789"
  )
  return Response(status_code=302, headers={"Location": auth_url})

@app.get("/auth/callback")
async def auth_callback(request: Request):
  code = request.query_params.get("code")
  token = sc.authenticate_with_code(
    code, 
    redirect_uri
  )
  response = JSONResponse(content=token)
  response.set_cookie("access_token", token["access_token"])

  return response

if __name__ == "__main__":
  uvicorn.run(app, port=8080)

```

## 📱 Example Apps

Explore fully functional sample applications built with popular Python frameworks and the Scalekit SDK:

| Framework | Repository | Description |
|-----------|------------|-------------|
| **FastAPI** | [scalekit-fastapi-example](https://github.com/scalekit-developers/scalekit-fastapi-example) | Modern async Python API framework |

## 🔗 Helpful Links

### 📖 Quickstart Guides
- [**SSO Integration**](https://docs.scalekit.com/sso/quickstart/) - Implement enterprise Single Sign-on
- [**Full Stack Auth**](https://docs.scalekit.com/fsa/quickstart/) - Complete authentication solution
- [**Passwordless Auth**](https://docs.scalekit.com/passwordless/quickstart/) - Modern authentication flows
- [**Social Logins**](https://docs.scalekit.com/social-logins/quickstart/) - Popular social identity providers
- [**Machine-to-Machine**](https://docs.scalekit.com/m2m/quickstart/) - API authentication

### 📚 Documentation & Reference
- [**API Reference**](https://docs.scalekit.com/apis) - Complete API documentation
- [**Developer Kit**](https://docs.scalekit.com/dev-kit/) - Tools and utilities
- [**API Authentication Guide**](https://docs.scalekit.com/guides/authenticate-scalekit-api/) - Secure API access

### 🛠️ Additional Resources
- [**Setup Guide**](https://docs.scalekit.com/guides/setup-scalekit/) - Initial platform configuration
- [**Code Examples**](https://docs.scalekit.com/directory/code-examples/) - Ready-to-use code snippets
- [**Admin Portal Guide**](https://docs.scalekit.com/directory/guides/admin-portal/) - Administrative interface
- [**Launch Checklist**](https://docs.scalekit.com/directory/guides/launch-checklist/) - Pre-production checklist

## License

This project is licensed under the **MIT license**.
See the [LICENSE](LICENSE) file for more information.

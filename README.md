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

from scalekit import ScalekitClient, AuthorizationUrlOptions

sc = ScalekitClient(
  env_url, 
  client_id, 
  client_secret
)

# Use the sc object to interact with the Scalekit API
options = AuthorizationUrlOptions()
options.state = "state"
options.connection_id = "con_123456789"

auth_url = sc.get_authorization_url(
  "https://acme-corp.com/redirect-uri",
  options
)

```

##### Minimum Requirements

To use the Scalekit Python SDK, you must have the following:

| Component | Version |
| --------- | ------- |
| Python    | 3.10+   |

> **Tip:** Although Python 3.10 meets the minimum requirement, using a more recent version (such as Python 3.11 or later) is advisable.


## Examples - SSO with FastAPI

Below is a simple code sample that showcases how to implement Single Sign-on using Scalekit SDK

```py
from fastapi import FastAPI, Request, Response
from scalekit import ScalekitClient, AuthorizationUrlOptions
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
  options = AuthorizationUrlOptions()
  options.state = "state"
  options.connection_id = "con_123456789"

  auth_url = sc.get_authorization_url(
    redirect_uri,
    options
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

### Full Stack Auth — encrypted-session middleware for Flask, FastAPI, and Django

The example above is for **Modular SSO**: Scalekit brokers the OAuth exchange with your customer's own IdP via a `connection_id`, and your app owns its own session however it likes.

If instead Scalekit hosts your login UI and you want it to also manage the session lifecycle for you (**Full Stack Auth**), `scalekit-sdk-python` ships optional Flask, FastAPI, and Django extras that handle the encrypted session cookie, transparent token refresh, CSRF-safe login/callback, and full logout for you — no hand-rolled cookies, no manual refresh timing.

Register these under **Dashboard → Authentication → Redirects** before testing:
- **Redirect URI** — your `redirect_uri` (the `/callback` path). Scalekit rejects the exchange if this doesn't match exactly.
- **Post Logout Redirect URI** — where users land after full logout. A relative path gets auto-absolutized against the request host, but the resulting absolute URL must still be registered.
- **Initiate Login URL** — your `/login` path. Scalekit redirects here (not `/callback`) for a bookmarked login page, an IdP portal tile, or an invite/magic link — the login view already handles this correctly, including the `idp_initiated_login` case, with no extra code required.

pip install "scalekit-sdk-python[flask]"  # or "scalekit-sdk-python[fastapi]" or "scalekit-sdk-python[django]"

```python
# Flask
import os
from flask import Flask
from scalekit.frameworks.flask import ScalekitAuth

app = Flask(__name__)
auth = ScalekitAuth(
    app,
    env_url=os.environ["SCALEKIT_ENV_URL"],
    client_id=os.environ["SCALEKIT_CLIENT_ID"],
    client_secret=os.environ["SCALEKIT_CLIENT_SECRET"],
    redirect_uri="https://myapp.com/callback",
    cookie_encryption_secret=os.environ["COOKIE_ENCRYPTION_SECRET"],  # openssl rand -base64 32
)  # registers /login, /callback, /logout

@app.route("/account")
@auth.requires_auth
def account():
    return {"email": auth.current_user["email"]}
```

```python
# FastAPI -- protect routes with Depends(), FastAPI's idiomatic mechanism
import os
from fastapi import Depends, FastAPI
from scalekit.frameworks.fastapi import ScalekitAuth

app = FastAPI()
auth = ScalekitAuth(
    env_url=os.environ["SCALEKIT_ENV_URL"],
    client_id=os.environ["SCALEKIT_CLIENT_ID"],
    client_secret=os.environ["SCALEKIT_CLIENT_SECRET"],
    redirect_uri="https://myapp.com/callback",
    cookie_encryption_secret=os.environ["COOKIE_ENCRYPTION_SECRET"],
)
auth.install(app)  # registers /login, /callback, /logout

@app.get("/account")
async def account(user: dict = Depends(auth.requires_auth)):
    return {"email": user["email"]}
```

```python
# Django -- settings.py
import os

MIDDLEWARE = [..., "scalekit.frameworks.django.ScalekitAuthMiddleware"]
SCALEKIT_ENV_URL = os.environ["SCALEKIT_ENV_URL"]
SCALEKIT_CLIENT_ID = os.environ["SCALEKIT_CLIENT_ID"]
SCALEKIT_CLIENT_SECRET = os.environ["SCALEKIT_CLIENT_SECRET"]
SCALEKIT_REDIRECT_URI = "https://myapp.com/callback"
SCALEKIT_COOKIE_ENCRYPTION_SECRET = os.environ["COOKIE_ENCRYPTION_SECRET"]

# urls.py
from django.urls import include, path
urlpatterns = [path("", include("scalekit.frameworks.django")), ...]  # /login, /callback, /logout

# views.py
from django.http import JsonResponse
from scalekit.frameworks.django import login_required

@login_required
def account(request):
    return JsonResponse(request.scalekit_user)
```

See [`examples/flask`](./examples/flask), [`examples/fastapi`](./examples/fastapi), and [`examples/django`](./examples/django) for complete, runnable versions. For a fuller production-oriented sample app, see the framework repos above.

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

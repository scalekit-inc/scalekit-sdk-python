<p align="left">
  <a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <img src="https://cdn.scalekit.cloud/v1/scalekit-logo-dark.svg" height="64">
    </picture>
  </a>
  <br/>
</p>

# Official Python SDK
<a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">Scalekit</a> is an Enterprise Authentication Platform purpose built for B2B applications. This Python SDK helps implement Enterprise Capabilities like Single Sign-on via SAML or OIDC in your Python applications within a few hours.

<div>
📚 <a target="_blank" href="https://docs.scalekit.com">Documentation</a> - 🚀 <a target="_blank" href="https://docs.scalekit.com">Quick-start Guide</a> - 💻 <a target="_blank" href="https://docs.scalekit.com/apis">API Reference</a>
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

## Example Apps

Fully functional sample applications written using some popular web application frameworks and Scalekit SDK. Feel free to clone the repo and run them locally.

- [FastAPI](https://github.com/scalekit-inc/scalekit-fastapi-example.git)

## API Reference

Refer to our [API reference docs](https://docs.scalekit.com/apis) for detailed information about all our API endpoints and their usage.

## More Information

- Quickstart Guide to implement Single Sign-on in your application: [SSO Quickstart Guide](https://docs.scalekit.com)
- Understand Single Sign-on basics: [SSO Basics](https://docs.scalekit.com/best-practices/single-sign-on)

## License

This project is licensed under the **MIT license**.
See the [LICENSE](LICENSE) file for more information.

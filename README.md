<p align="center">
  <a href="https://scalekit.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <img src="https://cdn.scalekit.cloud/v1/scalekit-logo-dark.svg" height="64">
    </picture>
  </a>
  <br/>
</p>
<h1 align="center">
  Official Scalekit Python SDK
</h1>

<h4 align="center">
Scalekit helps you ship Enterprise Auth in days.

This Python SDK is a wrapper around Scalekit's REST API to help you integrate Scalekit with your Python applications.
</h4>

## Getting Started

1. [Sign up](https://scalekit.com) for a Scalekit account.
2. Get your ```env_url```, ```client_id``` and ```client_secret``` from the Scalekit dashboard.

## Installation

```sh
pip install scalekit-sdk-python
```

## Usage

```javascript
from scalekit_client import Scalekit

scale_kit = Scalekit(
  os.environ['SCALEKIT_ENV_URL'],
  os.environ['SCALEKIT_CLIENT_ID'],
  os.environ['SCALEKIT_CLIENT_SECRET']
)
```

## API Reference
See the [Scalekit API docs](https://docs.scalekit.com) for more information about the API and authentication.

## License
This project is licensed under the **MIT license**.
See the [LICENSE](LICENSE) file for more information.

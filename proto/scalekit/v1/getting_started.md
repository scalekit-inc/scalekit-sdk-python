# Introduction
Scalekit API is modeled around the [REST](https://en.wikipedia.org/wiki/REST) architecture style. That means, our API has predictable resource-oriented URLs, accepts form-encoded request bodies and produces JSON formatted responses, uses standard HTTP verbs and error codes.

## Getting Started
If you are just getting started, you can also refer to our [Quick Start Guide](/single-sign-on/quickstart-sso).

Apart from REST APIs, we have published SDKs in some of the popular languages as shown below. You can use these SDKs and integrate with Scalekit much faster.

- [NodeJS](https://github.com/scalekit-inc/scalekit-sdk-node)
- [Go Lang](https://github.com/scalekit-inc/scalekit-sdk-go)

Some additional instructions around using our APIs

- API Endpoint Host must use the `Environment URL` of the environment you are targeting.
- API requests without appropriate authentication headers will fail with 401 status code.

Read below to understand more about how to authenticate the API calls and how to handle errors appropriately.


# API Authentication
Scalekit API uses [OAuth2 Client Credentials](https://www.oauth.com/oauth2-servers/access-tokens/client-credentials) based authentication. You can view and manage the necessary information from your `API Config` section in the Scalekit Dashboard.

You will need the following information to authenticate with Scalekit APIs
- Client ID
- Client Secret
- Environment URL

You can obtain a secure token by making `POST` call to the `https://{ENV_URL}/oauth/token` endpoint and sending client_id and client_secret as part of the request body.

```shell
$ curl https://{ENV_URL}/oauth/token \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'client_id={client_id}' \
  -d 'client_secret={client_secret}' \
  -d 'grant_type=client_credentials'\
```

Upon successful processing, you will receive the access token as part of the JSON response as shown in example below:
```json
{
  "access_token": "DCRD10-e7c5c8139165228a82e442445fe01c16",
  "token_type": "bearer",
  "expires_in": 1799
}
```
The `access_token` is the OAuth access token you need to use for all subsequent API calls to Scalekit.

To make a request to one of our APIs, you need to include the access token in the Authorization header of the request as Bearer 'access_token' like the following example shows:
```shell
$ curl --request GET "https://{ENV_URL}/api/v1/organizations" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer {access_token}"
```

Please make sure that you keep your Client Secrets safely. Do not share your client secret in publicly accessible areas such as GitHub, client-side code, etc. Refer to [this guide](/security/client-secrets) to understand some of the best practices around keeping client secrets secure.

Our SDKs will automatically handle the API authentication and error handling to make the job of using our APIs much easier for you.

# Error Handling
As mentioned earlier, Scalekit APIs return appropriate HTTP Status Codes along with the detailed error messages in case of invalid usage of APIs.

In general:
- `200 or 201`: API request is successful
- `400`: The request was unacceptable, often due to missing a required parameter.
- `401`: Invalid Authentication Headers found in the request.
- `404`: Resource not found
- `429`: Too many requests hit the API too quickly. Retry the request after a cool-off period.
- `500 or 501 or 504`: Something went wrong at our end. However rare they are, we automatically log these requests for proactive support and fixing the underlying issue.

Along with HTTP Status Codes, we also respond with detailed error messages. An example error message for a 401 error is shown below.

```json
{
    "code": 16,
    "message": "Token empty",
    "details":
    [
        {
            "@type": "type.googleapis.com/scalekit.v1.errdetails.ErrorInfo",
            "error_code": "UNAUTHENTICATED"
        }
    ]
}
```

We strongly recommend you to handle errors gracefully while writing code using our SDKs.

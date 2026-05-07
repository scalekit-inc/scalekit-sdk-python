"""
GoogleDWD (Google Domain-Wide Delegation) Support — Python SDK Implementation Plan
====================================================================================

## Overview
Add GOOGLE_DWD authorization type support to the Python SDK so callers can:
  1. Create/update a connected account with google_dwd auth (subject + scopes)
  2. Receive google_dwd auth details in the response (subject, access_token, scopes, token_expires_at)

The GOOGLE_DWD flow:
  - On create/update:  caller supplies { "google_dwd": { "subject": "<email>", "scopes": ["..."] } }
  - On get/list:       server returns  { "google_dwd": { "subject": "...", "access_token": "...",
                                                         "scopes": [...], "token_expires_at": "..." } }
  - access_token, scopes, token_expires_at are OUTPUT_ONLY — the server fills them via the
    jwt-bearer grant; callers should NEVER send these in requests.

## Files changed

### 1. proto/scalekit/v1/connected_accounts/connected_accounts.proto
  - Add GoogleDWDAuth message after StaticAuth
  - Add  google_dwd = 3  to AuthorizationDetails.details oneof

### 2. scalekit/v1/connected_accounts/connected_accounts_pb2.py  (regenerated)
  - Run:  buf generate --include-imports
  - This adds GoogleDWDAuth message class + AuthorizationDetails_GoogleDwd wrapper

### 3. scalekit/actions/models/requests/create_connected_account_request.py
  - Import GoogleDWDAuth from pb2
  - Add  elif "google_dwd" in self.authorization_details  branch in to_proto()

### 4. scalekit/actions/models/requests/update_connected_account_request.py
  - Same as (3) but for UpdateConnectedAccount

### 5. scalekit/actions/models/responses/get_connected_account_auth_response.py
  - Change ConnectedAccount.from_proto() to use WhichOneof("details") instead of
    checking authorization_type, so GOOGLE_DWD responses are correctly deserialized

### 6. tests/test_actions.py  (unit tests — no live server required)
  - TestGoogleDWDRequest: to_proto() creates correct AuthorizationDetails_GoogleDwd
  - TestGoogleDWDResponse: from_proto() correctly maps google_dwd oneof to dict

## Sample request / response

Create request body:
  {
    "google_dwd": {
      "subject": "user@example.com",
      "scopes": [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email"
      ]
    }
  }

Get response (authorization_details):
  {
    "google_dwd": {
      "subject": "user@example.com",
      "access_token": "ya29.a0AfH6...",
      "scopes": ["openid", "https://www.googleapis.com/auth/userinfo.email"],
      "token_expires_at": "2026-05-07T12:00:00"
    }
  }

## Key design notes
  - authorization_type for GOOGLE_DWD accounts is CONNECTION_TYPE_UNSPECIFIED (0) on the
    wire because the server's connected_accounts ConnectorType enum does not include
    GOOGLE_DWD; the auth type is therefore identified by which oneof field is set.
  - Use WhichOneof("details") not authorization_type checks in from_proto().
  - access_token / scopes / token_expires_at must NOT be sent in create/update requests;
    only subject and scopes are writable.
  - token_expires_at: may be absent; guard with HasField("token_expires_at") before calling
    ToDatetime() to avoid AttributeError on the default zero-timestamp.
"""

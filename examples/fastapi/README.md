# FastAPI example

Minimal FastAPI app using `ScalekitAuth` from `scalekit-sdk-python`'s encrypted-session middleware: login, callback, protected route, full logout — with transparent token refresh handled for you.

## Setup

```bash
cp .env.example .env
# fill in SCALEKIT_ENVIRONMENT_URL, SCALEKIT_CLIENT_ID, SCALEKIT_CLIENT_SECRET
# generate a cookie secret: openssl rand -base64 32
pip install -r requirements.txt
# during development against this checkout instead of PyPI:
#   pip install -e "../..[fastapi]"
python app.py
```

Register `http://localhost:5001/callback` as an allowed redirect URI (and `http://localhost:5001/` as an allowed post-logout redirect URI) in your Scalekit dashboard.

## What this demonstrates

- `auth.install(app)` — registers `/login`, `/callback`, `/logout` and the redirect exception handler.
- `Depends(auth.requires_auth)` — FastAPI's idiomatic protection mechanism (not a decorator); redirects to `/login` on no/invalid session as a real 302 (never a JSON 401 from a raised `HTTPException`), transparently refreshes an expired-but-refreshable session.
- The injected `user` dict is claims from the current **access token** (not id_token), so any custom claims you've configured in the Scalekit dashboard show up here, and stay fresh across refreshes.
- Full logout by default (ends the Scalekit-side session too via `id_token_hint`), not just the local cookie.

## In a real app

```bash
pip install scalekit-sdk-python[fastapi]
```

For a complete, production-oriented sample app (not just this minimal middleware demo), see [`scalekit-fastapi-auth-example`](https://github.com/scalekit-inc/scalekit-fastapi-auth-example).

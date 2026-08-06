# Flask example

Minimal Flask app using `ScalekitAuth` from `scalekit-sdk-python`'s encrypted-session middleware: login, callback, protected route, full logout — with transparent token refresh handled for you.

## Setup

```bash
cp .env.example .env
# fill in SCALEKIT_ENVIRONMENT_URL, SCALEKIT_CLIENT_ID, SCALEKIT_CLIENT_SECRET
# generate a cookie secret: openssl rand -base64 32
pip install -r requirements.txt
# during development against this checkout instead of PyPI:
#   pip install -e "../..[flask]"
python app.py
```

Register `http://localhost:5001/callback` as an allowed redirect URI (and `http://localhost:5001/` as an allowed post-logout redirect URI) in your Scalekit dashboard.

## What this demonstrates

- `ScalekitAuth(app, ...)` — registers `/login`, `/callback`, `/logout` for you.
- `@auth.requires_auth` — protects a view; redirects to `/login` on no/invalid session (never a JSON 401), transparently refreshes an expired-but-refreshable session.
- `auth.current_user` — claims from the current **access token** (not id_token), so any custom claims you've configured in the Scalekit dashboard show up here, and stay fresh across refreshes.
- Full logout by default (ends the Scalekit-side session too via `id_token_hint`), not just the local cookie.

## In a real app

```bash
pip install scalekit-sdk-python[flask]
```

For a complete, production-oriented sample app (not just this minimal middleware demo), see [`scalekit-flask-auth-example`](https://github.com/scalekit-inc/scalekit-flask-auth-example).

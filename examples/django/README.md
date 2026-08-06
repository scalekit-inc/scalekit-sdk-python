# Django example

Minimal Django project using `scalekit.frameworks.django`'s encrypted-session middleware: login, callback, protected route, full logout — with transparent token refresh handled for you.

## Setup

```bash
cp .env.example .env
# fill in SCALEKIT_ENVIRONMENT_URL, SCALEKIT_CLIENT_ID, SCALEKIT_CLIENT_SECRET
# generate a cookie secret: openssl rand -base64 32
pip install -r requirements.txt
# during development against this checkout instead of PyPI:
#   pip install -e "../..[django]"
python manage.py runserver 5001
```

Register these in your Scalekit dashboard: `http://localhost:5001/callback` as an allowed redirect URI, `http://localhost:5001/` as an allowed post-logout redirect URI, and `http://localhost:5001/login` as the Initiate Login URL.

## What this demonstrates

- Config lives in `settings.py` as `SCALEKIT_*` values (matching Django convention) — no `ScalekitAuth` instance to construct yourself.
- `ScalekitAuthMiddleware` in `MIDDLEWARE` — populates `request.scalekit_user` (claims from the current **access token**, not id_token) on every request and transparently refreshes an expired-but-refreshable session.
- `@login_required` (from `scalekit.frameworks.django`, not Django's own) — redirects to the configured login path on no/invalid session as a real 302, never a JSON 401.
- `path("", include("scalekit.frameworks.django"))` — registers `/login`, `/callback`, `/logout`.
- Full logout by default (ends the Scalekit-side session too via `id_token_hint`), not just the local cookie.

## In a real app

```bash
pip install scalekit-sdk-python[django]
```

For a complete, production-oriented sample app (not just this minimal middleware demo), see [`scalekit-django-auth-example`](https://github.com/scalekit-inc/scalekit-django-auth-example).

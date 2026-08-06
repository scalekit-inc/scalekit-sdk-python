import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse

from scalekit.frameworks.fastapi import ScalekitAuth

load_dotenv()

app = FastAPI()

auth = ScalekitAuth(
    env_url=os.environ["SCALEKIT_ENVIRONMENT_URL"],
    client_id=os.environ["SCALEKIT_CLIENT_ID"],
    client_secret=os.environ["SCALEKIT_CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URI"],
    cookie_encryption_secret=os.environ["COOKIE_ENCRYPTION_SECRET"],
)
auth.install(app)


@app.get("/", response_class=HTMLResponse)
async def home():
    return '<a href="/login">Login</a> | <a href="/account">Account</a> | <a href="/logout">Logout</a>'


@app.get("/account")
async def account(user: dict = Depends(auth.requires_auth)):
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=int(os.environ.get("PORT", 5001)))

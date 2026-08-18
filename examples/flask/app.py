import os

from dotenv import load_dotenv
from flask import Flask
from flask import request as flask_request

from scalekit.frameworks.flask import ScalekitAuth

load_dotenv()

app = Flask(__name__)

auth = ScalekitAuth(
    app,
    env_url=os.environ["SCALEKIT_ENVIRONMENT_URL"],
    client_id=os.environ["SCALEKIT_CLIENT_ID"],
    client_secret=os.environ["SCALEKIT_CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URI"],
    cookie_encryption_secret=os.environ["COOKIE_ENCRYPTION_SECRET"],
)


@app.route("/")
def home():
    if auth.manager.cookie_name in flask_request.cookies:
        return '<a href="/account">Account</a> | <a href="/logout">Logout</a>'
    return '<a href="/login">Login</a>'


@app.route("/account")
@auth.requires_auth
def account():
    return auth.current_user


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5001)))

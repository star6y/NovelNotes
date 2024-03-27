from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, send_file
from authlib.integrations.flask_client import OAuth


# Load environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


# Add modules. Specify imports here to avoid circular imports.
from .pages import home, auth, book, search, profile, about, suggest_book
app.register_blueprint(home.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(book.bp)
app.register_blueprint(search.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(about.bp)
app.register_blueprint(suggest_book.bp)

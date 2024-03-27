from os import environ as env
from book_reviews.data.db import create_user, get_user_by_username
from book_reviews.utils.display_objects.session_user import SessionUser
from book_reviews.utils.exceptions import UserNotFoundException
from flask import (
    Blueprint, url_for, redirect, session, jsonify, request
)
from book_reviews import oauth
from urllib.parse import quote_plus, urlencode
from functools import wraps

bp = Blueprint('auth', __name__)

@bp.route("/login")
def login():
    session['original_url'] = request.referrer
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True)
    )

@bp.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()

    db_user = {}
    session_user = SessionUser.from_auth0(
        uid=None,
        created_at=None,
        auth0_response=token
    )

    try:
        db_user = get_user_by_username(session_user.username)
    except UserNotFoundException:
        db_user = create_user(
            email=session_user.email, 
            username=session_user.username
        )

    session["user"] = SessionUser.from_auth0(
        uid=db_user.get("id"),
        created_at=db_user.get("created_at"),
        auth0_response=token
    ).to_dict()

    return redirect(
        session['original_url'] 
        if 'original_url' in session else 
        url_for("home.home")
    )

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home.home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    
    return decorated

def requires_auth_api(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    
    return decorated
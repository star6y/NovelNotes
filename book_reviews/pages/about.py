from flask import (
    Blueprint, render_template, session
)

bp = Blueprint('about', __name__)

@bp.route("/about")
def about():
    return render_template(
        "about.html",
        title="About Book Reviews",
        session=session,
        display_search=True
    )

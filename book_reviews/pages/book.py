import requests
from book_reviews.data.db import *
from book_reviews.pages.auth import *
from book_reviews.utils.constants import BOOKS_API_URL
from book_reviews.utils.display_objects.book import Book
from flask import (
    Blueprint, flash, render_template, session, request, jsonify
)
from functools import wraps
from datetime import datetime

bp = Blueprint('book', __name__)

@bp.route("/book/<string:book_id>")
def book(book_id):
    response = requests.get(f"{BOOKS_API_URL}/{book_id}")
    reviews = get_book_review_info(book_id)
    data = response.json()

    if "error" in data:
        return render_template(
            "notFound.html",
            title="Book not found",
            message="We couldn't find an entry for that Book ID. Please try again.",
            session=session, 
            display_search=True
        )
    else:
        book = Book.from_google_book_api_response(data)
        average_score = sum([review.review_score for review in reviews]) / len(reviews) if len(reviews) > 0 else 0
        average_score = round(average_score, 2)

        uid = session.get("user", {}).get("uid")
        user_review = next((review for review in reviews if review.reviewer.get("id") == uid), None)

        return render_template(
            "book.html",
            title=book.title,
            book=book,
            reviews=reviews,
            user_review=user_review,
            average_score=average_score,
            display_search=True
        )

# api endpoints for reviews
@bp.route("/api/book/<string:book_id>/review/post", methods=["POST"])
@requires_auth_api
def create_review(book_id):
    data = request.form
    existing_review = get_review(session["user"]["uid"], book_id)
    
    if existing_review:
        # Review already exists, you can choose to update or reject the new review
        flash("Review by this reviewer for this book already exists.", "error")
    elif not data["text"] or len(data["text"]) < 2 or len(data["text"]) > 2000:
        flash('Review text must be at least 2 characters and at most 2000 characters long.', 'error')
    else:
        insert_into_reviews(session["user"]["uid"], book_id, data["text"], data["score"])
    return redirect(url_for("book.book", book_id=book_id))


@bp.route("/api/book/<string:book_id>/review/edit", methods = ["POST"])
@requires_auth_api
def edit_review(book_id):
    data = request.form
    
    if not data["text"] or len(data["text"]) < 2 or len(data["text"]) > 2000:
        flash('Review text must be at least 2 characters and at most 2000 characters long.', 'error')
    else:    
        edit_review_data(session["user"]["uid"], book_id, data["text"], data["score"], datetime.utcnow())
    return redirect(url_for("book.book", book_id=book_id))


@bp.route("/api/book/<string:book_id>/review/delete", methods = ["POST"])
@requires_auth_api
def delete_review(book_id):
    delete_review_data(session["user"]["uid"], book_id)
    return redirect(url_for("book.book", book_id=book_id))


@bp.route("/api/book/review/<int:review_id>/like", methods = ["POST"])
@requires_auth_api
def like(review_id):
    existing_like = get_like_data(session["user"]["uid"], review_id)
    if existing_like:
        update_to_like(session["user"]["uid"], review_id)
    else:
        insert_into_likes_pos(session["user"]["uid"], review_id)
    return jsonify({"status": 200})


@bp.route("/api/book/review/<int:review_id>/unlike", methods = ["DELETE"])
@requires_auth_api
def unlike(review_id):
    delete_like(session["user"]["uid"], review_id)
    return jsonify({"status": 200})


@bp.route("/api/book/review/<int:review_id>/dislike", methods = ["POST"])
@requires_auth_api
def dislike(review_id):
    existing_like = get_like_data(session["user"]["uid"], review_id)
    if existing_like:
        update_to_dislike(session["user"]["uid"], review_id)
    else:
        insert_into_likes_neg(session["user"]["uid"], review_id)
    return jsonify({"status": 200})


@bp.route("/api/book/review/<int:review_id>/undislike", methods = ["DELETE"])
@requires_auth_api
def undislike(review_id):
    delete_dislike(session["user"]["uid"], review_id)
    return jsonify({"status": 200})

#api endpoints for comments

# post a comment
@bp.route("/api/book/<string:book_id>/comment/<int:review_id>/post", methods = ["POST"])
@requires_auth_api
def post_comment(book_id, review_id):
    data = request.form
    
    if not data["text"] or len(data["text"]) < 2 or len(data["text"]) > 400:
        flash('Comment text must be at least 2 characters and at most 400 characters long.', 'error')
    else:
        insert_into_comments(session["user"]["uid"], review_id, data["text"])
    return redirect(url_for('book.book', book_id=book_id))

# edit a comment
@bp.route("/api/book/<string:book_id>/comment/<int:comment_id>/edit", methods = ["POST"])
@requires_auth_api
def put_comment(book_id, comment_id):
    data = request.form
    
    if not data["text"] or len(data["text"]) < 2 or len(data["text"]) > 400:
        flash('Comment text must be at least 2 characters and at most 400 characters long.', 'error')
    else:
        edit_comment(session["user"]["uid"], comment_id, data["text"])
    return redirect(url_for('book.book', book_id=book_id))

# delete a comment
@bp.route("/api/book/<string:book_id>/comment/<int:comment_id>/delete", methods = ["POST"])
@requires_auth_api
def delete_user_comment(book_id, comment_id):
    delete_comment(session["user"]["uid"], comment_id)
    return redirect(url_for('book.book', book_id=book_id))

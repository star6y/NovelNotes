import requests
from book_reviews.data.db import search_users
from book_reviews.utils.constants import BOOKS_API_URL
from book_reviews.utils.display_objects.pagination import Pagination
from book_reviews.utils.display_objects.book import Book
from flask import (
    Blueprint, render_template, request,session
)
from libgravatar import Gravatar

bp = Blueprint('search', __name__)

@bp.route("/search")
def search():
    max_results = 12

    page = int(request.args.get("page", 1))
    search_text = request.args.get("search_text", None)
    search_type = request.args.get("search_type", "books")

    books = []
    users = []
    pagination = None

    if search_text and search_type == "book":
        params = {
            "q": search_text,
            "maxResults": max_results,
            "orderBy": "relevance",
            "startIndex": (page-1) * max_results
        }

        response = requests.get(BOOKS_API_URL, params=params)
        books = [
            Book.from_google_book_api_response(book)
            for book in response.json().get("items", [])
        ]

        # Pagination
        total_items = response.json().get("totalItems", 0)
        pagination = Pagination(page, max_results, total_items)

    if search_text and search_type == "user":
        all_users = search_users(search_text)
        users = all_users[(page-1) * max_results: page * max_results]
        pagination = Pagination(page, max_results, len(all_users))

    return render_template(
        "search.html",
        title="Search",
        search_type=search_type,
        search_text=search_text,
        pagination=pagination,
        books=books,
        users=users
    )

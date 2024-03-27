import requests
from flask import (
    Blueprint, render_template, session
)

from book_reviews.data.db import get_highest_rated_books, get_reviews_with_most_likes, get_users_with_most_reviews
from book_reviews.utils.constants import BOOKS_API_URL
from book_reviews.utils.display_objects.review import Review

bp = Blueprint('home', __name__)

@bp.route("/")
def home():
    highest_rated_books = get_highest_rated_books(num_books=3)
    most_active_users = get_users_with_most_reviews(num_users=3)
    most_liked_reviews = get_reviews_with_most_likes(num_reviews=3)
    most_liked_reviews = [
        Review.from_db(review) for review in most_liked_reviews
    ]
    
    books = []

    for book in highest_rated_books:
        response = requests.get(f"{BOOKS_API_URL}/{book['book_id']}")
        if response:
            book_data = response.json()
            book_info = book_data.get('volumeInfo', {})
            book_details = {
                'book_id': book['book_id'],
                'avg_rating': round(book['avg_rating'], 2),
                'title': book_info.get('title', 'Title Unknown'),
                'authors': ', '.join(book_info.get('authors', ['Author Unknown'])),
                'publishedDate': book_info.get('publishedDate', 'Date Unknown'),
                'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', ''),
            }
            books.append(book_details)

    return render_template(
        "home.html",
        title="Home",
        session=session,
        top_books=books,
        most_active_users=most_active_users,
        most_liked_reviews=most_liked_reviews,
        display_search=False
    )

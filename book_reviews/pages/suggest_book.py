import requests
from openai import OpenAI
from os import environ as env
from book_reviews.data.db import *
from book_reviews.pages.auth import requires_auth, requires_auth_api
from book_reviews.utils.display_objects.book import Book
from book_reviews.utils.constants import BOOKS_API_URL
from flask import (
    Blueprint, jsonify, render_template, session, request
)

bp = Blueprint('recommend', __name__)

@bp.route("/suggest")
@requires_auth
def suggest():
    return render_template("suggestBooks.html", title="Suggest a Book", display_search=True)

@bp.route("/api/recommendBooks", methods=["POST"])
@requires_auth_api
def suggest_book():
    prompt = "I am looking for book recommendations for: "

    if len(request.json.get("prompt")) < 3:
        return jsonify({"status": 400, "message": "Prompt too short"})

    if len(request.json.get("prompt")) > 100:
        return jsonify({"status": 400, "message": "Prompt too long"})

    prompt += request.json.get("prompt")
    
    include_preferences = request.json.get("include_preferences")

    if include_preferences:
        reviews = get_reviews_by_user(session["user"].get("username"))
        books = []

        try:
            for review in reviews:
                book = Book.from_google_book_api_response(requests.get(f"{BOOKS_API_URL}/{review['book_id']}").json())
                book.add_fields({'rating': review['review_score']})
                books.append(book)
        except Exception as _:
            return jsonify({"status": 500})

        prompt += "\n\nPlease base the rationale for each recommendation on my preferences from books I've already reviewed. \
                       You should write: 'Based on your preferences, this book is a good fit because ...'\n"
        for book in books:
            prompt += f"- {book.title}: I rated this book a {book.rating} / 5"

    response = OpenAI(api_key=env['OPENAI_API_KEY']).chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "You are an AI that suggests books. \
                            You must suggest 3 books. \
                            Respond in using the following format, with newlines:\
                            [Book title and author] | [Rationale here] \
                            [Book title and author] | [Rationale here] \
                            [Book title and author] | [Rationale here]"
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )

    if not response.choices or not response.choices[0].message.content:
        return jsonify({"status": 500})
    
    
    try:
        results = []
        choices = response.choices[0].message.content.split("\n")

        for choice in choices:
            # Remove empty choices
            if not choice: continue

            book_title, rationale = choice.split("|")
            params = {
                "q": book_title,
                "maxResults": 1
            }
            response = requests.get(BOOKS_API_URL, params=params).json()

            # If there was an error or no results, continue to the next choice
            if "error" in response or len(response.get('items', [])) == 0: continue

            book = Book.from_google_book_api_response(response['items'][0])
            book.add_fields({"rationale": rationale})
            results.append(book)
        
        return jsonify({
            "status": 200, 
            "books": [book.to_dict() for book in results]
        })

    except Exception as e:
        breakpoint()
        return jsonify({"status": 500})

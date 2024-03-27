import io
import requests, math
from openai import OpenAI
from os import environ as env
from book_reviews.data.db import *
from book_reviews.pages.auth import requires_auth
from book_reviews.utils.display_objects.book import Book
from book_reviews.utils.display_objects.comment import Comment
from book_reviews.utils.display_objects.pagination import Pagination
from book_reviews.utils.constants import BOOKS_API_URL
from flask import (
    Blueprint, jsonify, render_template, session, request, flash, url_for, redirect, send_file
)
# https://github.com/pabluk/libgravatar/tree/master?tab=readme-ov-file
from libgravatar import Gravatar
from book_reviews.utils.time_utils import utc_to_local_timezone_string


bp = Blueprint('profile', __name__)


# TODO
# make function to ensure the user editing/deleting is authenticated, else we send them to login page
# If they are authenitcated but not own post (error comes from db, since we don't check if 
#  any post is their own) then we give them error


@bp.route("/editReview", methods=["POST"])
def edit_review():
    
    # is user authenticated
    if 'user' not in session:
        flash('You must be logged in to edit reviews.', 'warning')
        return redirect(url_for('auth.login'))  
    
    # extract data from form 
    review_id = request.form.get('review_id')
    review_text = request.form.get('review_text')
    review_score = request.form.get('review_score')
    user = session["user"].get("username")
    # print(request.form)
    # print(review_score)
    
    # get the book/comment page numebrs from the form
    Book_page = int(request.form.get("Book_page", 1))
    Comment_page = int(request.form.get("Comment_page", 1))

    # do review sanitation or something
    if not review_text or len(review_text) < 2 or len(review_text) > 2000:
        flash('Review text must be at least 2 characters and at most 2000 characters long.', 'error')
        return redirect(url_for('profile.profile', Username=user, Book_page=Book_page, Comment_page=Comment_page))
    if not review_score or float(review_score) not in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]:
        flash('Review score must be between 0 and 5.', 'error')
        return redirect(url_for('profile.profile', Username=user, Book_page=Book_page, Comment_page=Comment_page))
    print(request.form)

    update_user_review(review_text, review_score, review_id, user)
    return redirect(url_for('profile.profile', Username=user, Book_page=Book_page, Comment_page=Comment_page))



@bp.route("/deleteReview", methods=["POST"])
def delete_review():
    # is user authenticated
    if 'user' not in session:
        flash('You must be logged in to edit reviews.', 'warning')
        return redirect(url_for('auth.login')) 
    
    user = session["user"].get("username")

    # extract data from form
    review_id = request.form.get('review_id')
    Book_page = int(request.form.get("Book_page", 1))
    Comment_page = int(request.form.get("Comment_page", 1))
    print(request.form)

    delete_user_review(review_id, user)
    return redirect(url_for('profile.profile', Username=user, Book_page=Book_page, Comment_page=Comment_page))



@bp.route("/editComment", methods=["POST"])
def edit_comment():
    
    # is user authenticated
    if 'user' not in session:
        flash('You must be logged in to edit comments.', 'warning')
        return redirect(url_for('auth.login')) 
     
    user = session["user"].get("username")

    # extract data from form 
    comment_id = request.form.get('comment_id')
    comment_text = request.form.get('comment_text')
    Book_page = int(request.form.get("Book_page", 1))
    Comment_page = int(request.form.get("Comment_page", 1))

    # do comment sanitation or something
    if not comment_text or len(comment_text) < 2 or len(comment_text) > 400:
        flash('Comment text must be at least 2 characters and at most 400 characters long.', 'error')
        return redirect(url_for('profile.profile', Username=user, Book_page=Book_page, Comment_page=Comment_page))

    update_user_comment(comment_text, comment_id, user)
    return redirect(url_for('profile.profile', Username=user, Book_page=Book_page, Comment_page=Comment_page))



@bp.route("/deleteComment", methods=["POST"])
def delete_comment():
    # is user authenticated
    if 'user' not in session:
        flash('You must be logged in to edit reviews.', 'warning')
        return redirect(url_for('auth.login')) 
    
    user = session["user"].get("username")

    # extract data from form
    comment_id = request.form.get('comment_id')
    Book_page = int(request.form.get("Book_page", 1))
    Comment_page = int(request.form.get("Comment_page", 1))
    print(request.form)

    delete_user_comment(comment_id, user)
    return redirect(url_for('profile.profile', Username=user, Book_page=Book_page, Comment_page=Comment_page))



@bp.route("/profile")
def profile():
    # check that the requested user is not None
    UserArg = request.args.get("Username")

    if UserArg is None:
        return render_template("notFound.html",message="No username provided")
    
     # try to fetch the user; will raise UserNotFoundException if user doesn't exist
    try:   
        users_profile = get_user_by_username(UserArg)
        user_exists = True
    except UserNotFoundException:   # user does not exist
        user_exists = False
        users_profile = None

    users_email = users_profile["email"] if users_profile is not None else None


    # render not found page if the user does not exist
    if not user_exists:   
        return render_template("notFound.html", message=f"No user exists with username {UserArg}")
    
    # if user is in session, and they are viewing their own profile, remember that
    logged_in = "user" in session
    is_own_profile = False
    if logged_in:
        session_user = session["user"]
        is_own_profile = (UserArg == session_user.get("username", ""))

    # get pagination for reviews & comments
    Book_pagination =None
    Comment_pagination= None
    max_results = 3
    Book_page = int(request.args.get("Book_page", 1))
    
    Comment_page = int(request.args.get("Comment_page", 1))
    

    #  get all the reviews and comments of this user
    All_reviews = get_reviews_by_user(UserArg)
    All_comments = get_comments_by_user(UserArg)


    # make sure that requested page number exists, otherwise take the max page number
    Book_page = min(math.ceil(len(All_reviews) / max_results), Book_page)
    Comment_page = min(math.ceil(len(All_comments) / max_results), Comment_page)
    Current_Bookpage = Book_page
    Current_Comment_page = Comment_page


    # show only the book reviews for the correct page number
    reviews = All_reviews[(Book_page-1) * max_results: Book_page * max_results]
    Book_pagination = Pagination(Book_page, max_results, len(All_reviews))
    books = []

    for review in reviews:
        response = requests.get(f"{BOOKS_API_URL}/{review['book_id']}")
        if response:
            book_data = response.json()
            book = Book.from_google_book_api_response(book_data)
            book.add_fields({
                'id': review['id'],
                'book_id':review['book_id'],
                'review_text': review['review_text'],
                'review_score': review['review_score'],
                'created_at': utc_to_local_timezone_string(review['created_at']),
                'updated_at': utc_to_local_timezone_string(review['updated_at']),
            })
            books.append(book)
    
    # show only the comments for the correct page number
    comments = All_comments[(Comment_page-1) * max_results: Comment_page * max_results]
    Comment_pagination = Pagination(Comment_page, max_results, len(All_comments))
    User_Comments = [Comment.from_db(comment) for comment in comments]
    # print(User_Comments)

    username = session_user.get("username") if logged_in else "Guest"
    title = f"{UserArg}'s Profile"

    return render_template("profile.html", 
        Profile_username=UserArg, 
        Username=username,
        title=title,
        display_search=True,
        Book_pagination=Book_pagination,
        Current_page=Current_Bookpage, 
        logged_in=logged_in,
        Current_Comment_page=Current_Comment_page,
        User_Comments=User_Comments,
        Comment_pagination=Comment_pagination, 
        is_own_profile=is_own_profile,
        reviews=reviews,
        books = books
    )


@bp.route("/uploadProfilePicture", methods=["POST"])
@requires_auth
def upload_profile_picture():
    update_user_profile_picture(session["user"]["uid"], request.files['profile_picture'].read())
    return redirect(url_for("profile.profile", Username=session["user"]["username"]))


@bp.route("/profilePicture/<string:username>")
def profile_picture(username):
    image = get_user_profile_picture(username)
    if image is not None:
        return send_file(io.BytesIO(image["image_bytes"]), mimetype="image/png")
    else:
        # If no profile picture is found, we create a gravatar image
        # This uses the USERNAME to generate a unique image
        # Gravatar documentation recommends an email, but since we specify custom
        # images internally for users, we use the username as a unique identifier / hash
        gravatar = Gravatar(username)
        image_url = gravatar.get_image(default='identicon', size=100)
        image_bytes = requests.get(image_url).content
        return send_file(io.BytesIO(image_bytes), mimetype="image/png")

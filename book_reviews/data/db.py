from os import environ as env
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

from book_reviews.data.queries import *
from book_reviews.utils.display_objects.review import Review
from book_reviews.utils.exceptions import UserNotFoundException

# pool = ThreadedConnectionPool(
#     1, 
#     100, 
#     dsn=env.get('POSTGRES_CONNECTION_STRING'), 
#     sslmode='require'
# )

pool = ThreadedConnectionPool(
    1, 20,
    dbname='andrei_db',
    user='andrei_db_user',
    password='Dszk8YpIrnRJKCgoYLbKr7DwEjpVdd4N',
    host='dpg-cp3ts18cmk4c73ebmc60-a.ohio-postgres.render.com',
    port='5432',
    sslmode='require'
)

@contextmanager
def _get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def _get_db_cursor(commit=False):
    with _get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()
    
# Define query functions here
def get_user_by_username(username):
    with _get_db_cursor() as cursor:
        cursor.execute(USER_BY_USERNAME_QUERY, (username,))
        if cursor.rowcount == 0:
            raise UserNotFoundException(f"User with username {username} not found")
        else:
            return dict(cursor.fetchone())
        
def get_user_by_id(user_id):
    with _get_db_cursor() as cursor:
        cursor.execute(USER_BY_ID_QUERY, (user_id,))
        return dict(cursor.fetchone())

def create_user(email, username):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(
            CREATE_USER_QUERY,
            (email, username)
        )
        return dict(cursor.fetchone())

def get_book_review_info(book_id):
    with _get_db_cursor() as cursor:
        cursor.execute(BOOK_REVIEWS_QUERY, (book_id,))
        reviews = [dict(review) for review in cursor.fetchall()]
        return [ Review.from_db(review) for review in reviews ] 
    
def get_review(id, book_id):
    with _get_db_cursor() as cursor:
        cursor.execute(GET_SINGLE_REVIEW, (id, book_id))
        return cursor.fetchone()
    
def insert_into_reviews(id, book_id, review_text, review_score):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(INSERT_INTO_REVIEWS, (id, book_id, review_text, review_score))

def edit_review_data(id, book_id, review_text, review_score, new_time):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(UPDATE_SINGLE_REVIEW, (review_text, review_score, new_time, id, book_id))

def delete_review_data(id, book_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(DELETE_SINGLE_REVIEW, (id, book_id))

def get_likes_data():
    with _get_db_cursor() as cursor:
        cursor.execute(GET_ALL_LIKES)
        return [dict(like) for like in cursor.fetchall()]

def get_like_data(user_id, review_id):
    with _get_db_cursor() as cursor:
        cursor.execute(GET_SINGLE_LIKE, (user_id, review_id))
        return cursor.fetchone()

def update_to_like(user_id, review_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(UPDATE_TO_LIKE, (user_id, review_id))

def insert_into_likes_pos(user_id, review_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(INSERT_LIKE, (user_id, review_id))

def delete_like(user_id, review_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(DELETE_SINGLE_LIKE, (user_id, review_id))

def update_to_dislike(user_id, review_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(UPDATE_TO_DISLIKE, (user_id, review_id))

def insert_into_likes_neg(user_id, review_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(INSERT_DISLIKE, (user_id, review_id))

def delete_dislike(user_id, review_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(DELETE_SINGLE_DISLIKE, (user_id, review_id))

def search_users(username_query):
    with _get_db_cursor() as cursor:
        cursor.execute(USER_SEARCH_QUERY, (f"%{username_query}%",f"%{username_query}%"))
        return [dict(user) for user in cursor.fetchall()]
    
def get_total_reviews_by_user(user_id):
    with _get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(REVIEW_COUNT_BY_USER_QUERY, (user_id,))
            total = cursor.fetchone()[0]
    return total


def get_reviews_by_user(username):
    with _get_db_cursor() as cursor:
        cursor.execute(REVIEWS_BY_USER_QUERY, (username,))
        reviews = cursor.fetchall()
    return reviews

def get_comments_by_user(username):
    with _get_db_cursor() as cursor:
        cursor.execute(COMMENTS_BY_USER_QUERY, (username,))
        comments = cursor.fetchall()
    return comments

def update_user_review(text, score, review_id, username):
    with _get_db_cursor(commit=True) as cursor:
        try:
            cursor.execute(UPDATE_REVIEW, (text, score, review_id, username))
        except Exception as e:
            print(f"Database update error: {e}")
        if cursor.rowcount == 0:
            print("Review updated failed.")
        else:
            print("{} changes".format(cursor.rowcount))

def delete_user_review(book_id, username):
    with _get_db_cursor() as cursor:
        try:
            cursor.execute(DELETE_REVIEW, (book_id, username))
            if cursor.rowcount > 0:
                print(f"Deleted {cursor.rowcount} review(s)")
                cursor.connection.commit()
            else:
                print("No review was deleted")
        except Exception as e:
            print(f"Database delete error: {e}")
            # rollback  transaction in case of error
            cursor.connection.rollback()


def update_user_comment(text, comment_id, username):
    print("{} -- {} -- ({})   ".format(text, comment_id, username))

    with _get_db_cursor(commit=True) as cursor:
        try:
            cursor.execute(UPDATE_COMMENT, (text, comment_id, username))
        except Exception as e:
            print(f"Database update error: {e}")
        if cursor.rowcount == 0:
            print("Review updated failed.")
        else:
            print("{} changes".format(cursor.rowcount))


def delete_user_comment(comment_id, username):
    with _get_db_cursor() as cursor:
        try:
            cursor.execute(DELETE_COMMENT_WITH_ID, (comment_id, username))
            if cursor.rowcount > 0:
                print(f"Deleted {cursor.rowcount} comment(s)")
                cursor.connection.commit()
            else:
                print("No comment was deleted")
        except Exception as e:
            print(f"Database delete error: {e}")
            # rollback  transaction in case of error
            cursor.connection.rollback()

def get_comments_data(review_id):
    with _get_db_cursor() as cursor:
        cursor.execute(GET_COMMENTS, (review_id,))
        return [dict(comment) for comment in cursor.fetchall()]
    
def insert_into_comments(user_id, review_id, comment_text):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(INSERT_COMMENTS, (user_id, review_id, comment_text))

def edit_comment(user_id, comment_id, comment_text):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(EDIT_COMMENT, (comment_text, user_id, comment_id))

def delete_comment(user_id, comment_id):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(DELETE_COMMENT, (user_id, comment_id))

def get_highest_rated_books(num_books):
    with _get_db_cursor() as cursor:
        cursor.execute(HIGHEST_RATED_BOOKS_QUERY, (num_books,))
        return [dict(book) for book in cursor.fetchall()]
    
def get_users_with_most_reviews(num_users):
    with _get_db_cursor() as cursor:
        cursor.execute(USERS_WITH_MOST_REVIEWS_QUERY, (num_users,))
        return [dict(user) for user in cursor.fetchall()]
    
def get_reviews_with_most_likes(num_reviews):
    with _get_db_cursor() as cursor:
        cursor.execute(REVIEWS_WITH_MOST_LIKES_QUERY, (num_reviews,))
        return [dict(review) for review in cursor.fetchall()]

def update_user_profile_picture(user_id, image_bytes):
    with _get_db_cursor(commit=True) as cursor:
        cursor.execute(UPDATE_USER_PROFILE_PICTURE, (user_id, image_bytes, image_bytes))

def get_user_profile_picture(username):
    with _get_db_cursor() as cursor:
        cursor.execute(GET_USER_PROFILE_PICTURE, (username,))
        return cursor.fetchone()

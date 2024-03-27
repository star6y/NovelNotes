BOOK_REVIEWS_QUERY = """\
SELECT
    R.id AS review_id,
    R.book_id,
    R.review_text,
    R.review_score,
    R.created_at AS review_created_at,
    R.updated_at AS review_updated_at,
    U.id AS reviewer_id,
    U.email AS reviewer_email,
    U.username AS reviewer_username,
    CASE
        WHEN COUNT(L.user_id) = 0 THEN '[]'::jsonb
        ELSE jsonb_agg(
        DISTINCT jsonb_build_object(
            'user_id', L.user_id, 
            'like_score', L.like_score
        )
    )
    END AS likes,
    CASE
        WHEN COUNT(RC.id) = 0 THEN '[]'::jsonb
        ELSE jsonb_agg(
        DISTINCT jsonb_build_object(
            'id', RC.id, 
            'text', RC.comment_text, 
            'created_at', RC.created_at, 
            'updated_at', RC.updated_at,
            'commenter_id', RC.user_id,
            'commenter_username', UC.username
        )
    )
    END AS comments
FROM Reviews R
JOIN Users U ON R.reviewer_id = U.id
LEFT JOIN Likes L ON R.id = L.review_id
LEFT JOIN ReviewComments RC ON R.id = RC.review_id
LEFT JOIN Users UC ON RC.user_id = UC.id
WHERE R.book_id = %s
GROUP BY R.id, U.id
ORDER BY R.created_at;
"""

USER_BY_USERNAME_QUERY = "SELECT * FROM users WHERE username = %s"

USER_BY_ID_QUERY = "SELECT * FROM users WHERE id = %s"

CREATE_USER_QUERY = "INSERT INTO users (email, username) VALUES (%s, %s) RETURNING *"

GET_SINGLE_REVIEW = "SELECT * FROM Reviews WHERE reviewer_id = %s AND book_id = %s"

INSERT_INTO_REVIEWS = "INSERT INTO Reviews (reviewer_id, book_id, review_text, review_score) VALUES (%s, %s, %s, %s)"

UPDATE_SINGLE_REVIEW = "UPDATE Reviews SET review_text = %s, review_score = %s, updated_at = %s WHERE reviewer_id = %s and book_id = %s"

DELETE_SINGLE_REVIEW = "DELETE FROM Reviews WHERE reviewer_id = %s and book_id = %s"

GET_ALL_LIKES = "SELECT * from Likes"

GET_SINGLE_LIKE = "SELECT * from Likes WHERE user_id = %s and review_id = %s"

UPDATE_TO_LIKE = "UPDATE Likes SET like_score = 1 WHERE user_id = %s and review_id = %s"

INSERT_LIKE = "INSERT INTO Likes (user_id, review_id, like_score) VALUES (%s, %s, 1)"

DELETE_SINGLE_LIKE = "DELETE FROM Likes WHERE user_id = %s and review_id = %s and like_score = 1"

UPDATE_TO_DISLIKE = "UPDATE Likes SET like_score = -1 WHERE user_id = %s and review_id = %s"

INSERT_DISLIKE = "INSERT INTO Likes (user_id, review_id, like_score) VALUES (%s, %s, -1)"

DELETE_SINGLE_DISLIKE = "DELETE FROM Likes WHERE user_id = %s and review_id = %s and like_score = -1"

USER_SEARCH_QUERY = "SELECT * FROM Users WHERE username ILIKE %s OR email ILIKE %s;"


# ------------------
REVIEWS_BY_USER_QUERY = """
SELECT reviews.id, reviews.reviewer_id, reviews.book_id, reviews.review_text, reviews.review_score, reviews.created_at, reviews.updated_at
FROM reviews
JOIN users ON reviews.reviewer_id = users.id
WHERE users.username = %s
ORDER BY reviews.created_at DESC;
"""

REVIEW_COUNT_BY_USER_QUERY="SELECT COUNT(*) FROM Reviews JOIN users ON reviews.reviewer_id = users.id WHERE users.username = %s"

REVIEWS_BY_USER_QUERY = """
SELECT Reviews.*, Users.username FROM Reviews
JOIN Users ON Reviews.reviewer_id = Users.id
WHERE Users.username = %s
ORDER BY Reviews.created_at DESC
"""

COMMENTS_BY_USER_QUERY="""
SELECT 
  ReviewComments.*, 
  Users.username,
  Reviews.book_id
FROM ReviewComments 
JOIN Users ON ReviewComments.user_id = Users.id 
JOIN Reviews ON ReviewComments.review_id = Reviews.id
WHERE Users.username = %s 
ORDER BY reviewcomments.created_at DESC;
"""

UPDATE_REVIEW = """
UPDATE reviews
SET review_text = %s, review_score = %s, updated_at = CURRENT_TIMESTAMP
FROM users
WHERE reviews.reviewer_id = users.id
AND reviews.id = %s
AND users.username = %s;
"""


DELETE_REVIEW ="""
DELETE FROM reviews
USING users
WHERE reviews.reviewer_id = users.id
AND reviews.id = %s
AND users.username = %s;
"""

UPDATE_COMMENT = """
UPDATE reviewcomments
SET comment_text = %s, updated_at = CURRENT_TIMESTAMP
FROM users
WHERE reviewcomments.user_id = users.id
AND reviewcomments.id = %s
AND users.username = %s;
"""


DELETE_COMMENT_WITH_ID ="""
DELETE FROM reviewcomments
USING users
WHERE reviewcomments.user_id = users.id
AND reviewcomments.id = %s
AND users.username = %s;
"""



'''
DELETE FROM reviews USING users WHERE reviews.reviewer_id = users.id
AND reviews.id = 26 AND users.username = 'review';
'''


"""
UPDATE reviews SET review_text = 'test22', review_score = 4 FROM users
WHERE reviews.reviewer_id = users.id AND reviews.book_id = 'cRPKOzWlOfUC' AND users.username = 'review';
"""

# update reviews set review_text ='updated' where reviewer_id =6 and book_id = 'cRPKOzWlOfUC';


GET_COMMENTS = "SELECT * FROM ReviewComments WHERE review_id = %s"

INSERT_COMMENTS = "INSERT INTO ReviewComments (user_id, review_id, comment_text) VALUES (%s, %s, %s)"

EDIT_COMMENT = "UPDATE ReviewComments SET comment_text = %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s and id = %s"

DELETE_COMMENT = "DELETE FROM ReviewComments WHERE user_id = %s and id = %s"

# Homepage queries 
HIGHEST_RATED_BOOKS_QUERY = """
SELECT Reviews.book_id, AVG(Reviews.review_score) AS avg_rating
FROM Reviews
GROUP BY Reviews.book_id
ORDER BY avg_rating DESC
LIMIT %s;
"""

USERS_WITH_MOST_REVIEWS_QUERY = """
SELECT Users.username, COUNT(Reviews.id) AS review_count
FROM Users
JOIN Reviews ON Users.id = Reviews.reviewer_id
GROUP BY Users.username
ORDER BY review_count DESC
LIMIT %s;
"""

REVIEWS_WITH_MOST_LIKES_QUERY = """
SELECT 
  Reviews.id as review_id, 
  Reviews.review_text,
  Reviews.review_score, 
  Reviews.book_id,
  Reviews.updated_at AS review_updated_at,
  Reviews.created_at AS review_created_at,
  Users.id AS reviewer_id,
  Users.email AS reviewer_email,
  Users.username AS reviewer_username,
  COALESCE(SUM(Likes.like_score), 0) AS total_likes,
  CASE
    WHEN COUNT(Likes.user_id) = 0 THEN '[]'::jsonb
        ELSE jsonb_agg(
        DISTINCT jsonb_build_object(
            'user_id', Likes.user_id, 
            'like_score', Likes.like_score
        )
    )
  END AS likes
FROM Reviews
LEFT JOIN Likes ON Reviews.id = Likes.review_id
LEFT JOIN Users ON Reviews.reviewer_id = Users.id
GROUP BY Reviews.id, Users.id
ORDER BY total_likes DESC
LIMIT %s;
"""

UPDATE_USER_PROFILE_PICTURE = "INSERT INTO Images (user_id, image_bytes) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET image_bytes = %s;"

GET_USER_PROFILE_PICTURE = "SELECT image_bytes FROM Images JOIN Users ON Users.id = Images.user_id WHERE username = %s;"

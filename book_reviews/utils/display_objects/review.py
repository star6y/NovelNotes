from book_reviews.utils.display_objects.comment import Comment
from book_reviews.utils.time_utils import utc_to_local_timezone_string
import json 

class Review:

    def __init__(
            self, 
            review_id,
            book_id,
            review_text, 
            review_score, 
            review_created_at, 
            review_updated_at, 
            reviewer, 
            likes, 
            total_likes, 
            comments
    ):
        self.review_id = review_id
        self.book_id = book_id
        self.review_text = review_text
        self.review_score = review_score
        self.review_created_at = utc_to_local_timezone_string(review_created_at)
        self.review_updated_at = utc_to_local_timezone_string(review_updated_at)
        self.reviewer = reviewer
        self.likes = likes
        self.like_uids=[like["user_id"] for like in likes if like["like_score"] == 1]
        self.dislike_uids=[like["user_id"] for like in likes if like["like_score"] == -1]
        self.total_likes = total_likes
        self.comments = [Comment.from_db(comment) for comment in comments]

    @staticmethod
    def from_db(review_json):
        return Review(
            review_id=review_json.get("review_id"),
            book_id=review_json.get("book_id"),
            review_text=review_json.get("review_text"),
            review_score=review_json.get("review_score"),
            review_created_at=review_json.get("review_created_at"),
            review_updated_at=review_json.get("review_updated_at"),
            reviewer={
                "id": review_json.get("reviewer_id"),
                "username": review_json.get("reviewer_username"),
                "email": review_json.get("reviewer_email")
            },
            likes=review_json.get("likes"),
            total_likes=sum([like["like_score"] for like in review_json.get("likes", [])]),
            comments=review_json.get("comments", [])
        )

    def to_js_object(self):
        return json.dumps({
            "review_id": self.review_id,
            "book_id": self.book_id,
            "review_text": self.review_text,
            "review_score": self.review_score,
            "review_created_at":self.review_created_at,
            "review_updated_at": self.review_updated_at,
            "reviewer": self.reviewer,
            "like_uids": self.like_uids,
            "dislike_uids": self.dislike_uids,
            "total_likes": self.total_likes,
            "comments": [comment.to_js_object() for comment in self.comments]
        })

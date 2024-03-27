from book_reviews.utils.time_utils import utc_to_local_timezone_string
from datetime import datetime
import json

class Comment:

    def __init__(self, comment_id, review_id, book_id, text, created_at, updated_at, commenter_id, commenter_username):
        self.comment_id = comment_id
        self.review_id = review_id
        self.book_id = book_id
        self.text = text
        self.created_at = utc_to_local_timezone_string(created_at)
        self.updated_at = utc_to_local_timezone_string(updated_at)
        self.commenter_id = commenter_id
        self.commenter_username = commenter_username
    
    @staticmethod
    def from_db(comment_json):
        if type(comment_json["created_at"]) == str:
            comment_json["created_at"] = datetime.fromisoformat(comment_json["created_at"])
        if type(comment_json["updated_at"]) == str:
            comment_json["updated_at"] = datetime.fromisoformat(comment_json["updated_at"])

        return Comment(
            comment_id=comment_json.get("id"),
            review_id=comment_json.get("review_id"),
            book_id=comment_json.get("book_id"),
            text=comment_json.get("text") or comment_json.get("comment_text"),
            created_at=comment_json["created_at"],
            updated_at=comment_json["updated_at"],
            commenter_id=comment_json.get("commenter_id"),
            commenter_username=comment_json.get("commenter_username")
        )

    def to_js_object(self):
        return json.dumps({
            "comment_id": self.comment_id,
            "review_id": self.review_id,
            "book_id": self.book_id,
            "text": self.text,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "commenter_id": self.commenter_id,
            "commenter_username": self.commenter_username
        })

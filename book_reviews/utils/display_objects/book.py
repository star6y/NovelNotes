from flask import url_for

class Book:
    
    def __init__(self, book_id, title, authors, publisher, published_date, description, thumbnail, pages):
        self.book_id = book_id
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.published_date = published_date
        self.description = description
        self.thumbnail = thumbnail
        self.pages = pages

    def add_fields(self, fields):
        for key, value in fields.items():
            setattr(self, key, value)
    
    @staticmethod
    def from_google_book_api_response(book):
        return Book(
            book_id=book["id"],
            title=book["volumeInfo"]["title"],
            authors=book["volumeInfo"].get("authors", ["Author Unkown"]),
            publisher=book["volumeInfo"].get("publisher", "Publisher Unknown"),
            published_date=book["volumeInfo"].get("publishedDate", "Unknown"),
            description=book["volumeInfo"].get("description", "No description available"),
            thumbnail=book["volumeInfo"]["imageLinks"]["thumbnail"] 
                        if "imageLinks" in book["volumeInfo"]
                        else url_for("static", filename="missing_book.png"),
            pages=book["volumeInfo"].get("pageCount", "Unknown"),
        )
    
    def to_dict(self):
        book_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                book_dict[key] = ", ".join(value)
            else:
                book_dict[key] = value
        return book_dict

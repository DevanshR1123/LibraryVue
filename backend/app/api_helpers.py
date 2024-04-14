from flask_restful import Resource, fields, marshal, reqparse
from flask_restful.fields import Integer, String, DateTime, Boolean, Nested, List, Float, Fixed
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage


# Comment API

comment_resource_fields = {
    "id": Integer,
    "user_id": Integer,
    "book_id": Integer,
    "content": String,
    "timestamp": DateTime,
}

comments_resource_fields = List(Nested(comment_resource_fields))


comment_parser = (
    reqparse.RequestParser()
    .add_argument("user_id", type=int, required=True, location="json", help="User ID is required")
    .add_argument("book_id", type=int, required=True, location="json", help="Book ID is required")
    .add_argument("content", type=str, required=True, location="json", help="Content is required")
)


# Rating API

rating_resource_fields = {
    "user_id": Integer,
    "book_id": Integer,
    "rating": Integer,
}

ratings_resource_fields = List(Nested(rating_resource_fields))


fetch_rating_parser = (
    reqparse.RequestParser()
    .add_argument("user_id", type=int, required=False, location="args", help="User ID is required")
    .add_argument("book_id", type=int, required=False, location="args", help="Book ID is required")
)

new_rating_parser = (
    reqparse.RequestParser()
    .add_argument("user_id", type=int, required=True, location="json", help="User ID is required")
    .add_argument("book_id", type=int, required=True, location="json", help="Book ID is required")
    .add_argument(
        "rating", type=int, required=True, location="json", help="Rating is required", choices=[1, 2, 3, 4, 5]
    )
)


# Book Issue API

issue_resource_fields = {
    "id": Integer,
    "user_id": Integer,
    "book_id": Integer,
    "issue_date": DateTime,
    "return_date": DateTime,
    "returned": Boolean,
}


issue_parser = (
    reqparse.RequestParser()
    .add_argument("user_id", type=int, required=True, location="json", help="User ID is required")
    .add_argument("book_id", type=int, required=True, location="json", help="Book ID is required")
    .add_argument("issue_date", type=str, required=True, location="json", help="Issue date is required")
    .add_argument("return_date", type=str, required=True, location="json", help="Return date is required")
)


# Book API

book_resource_fields = {
    "id": Integer,
    "title": String,
    "author": String,
    "isbn": String,
    "year": Integer,
    "date_added": DateTime,
    "description": String,
    "image": String,
    "section": Nested(
        {
            "id": Integer,
            "name": String,
            "description": String,
            "image": String,
        }
    ),
    "rating": Float,
    "issued": Boolean,
    "comments": List(Nested(comment_resource_fields)),
}

books_resource_fields = List(Nested(book_resource_fields))


book_parser = (
    reqparse.RequestParser()
    .add_argument("title", type=str, required=True, location="form", help="Title is required")
    .add_argument("author", type=str, required=True, location="form", help="Author is required")
    .add_argument("isbn", type=str, required=True, location="form", help="ISBN is required")
    .add_argument("year", type=int, required=True, location="form", help="Year is required")
    .add_argument("description", type=str, required=True, location="form", help="Description is required")
    .add_argument("section_id", type=int, required=True, location="form", help="Section ID is required")
    .add_argument("content", type=FileStorage, required=False, location="files", help="Content is required")
    .add_argument("image", type=FileStorage, required=False, location="files", help="Image is required")
)


# Section API

section_resource_fields = {
    "id": Integer,
    "name": String,
    "description": String,
    "image": String,
    "books": List(Nested(book_resource_fields)),
}

sections_resource_fields = Nested(List(Nested(section_resource_fields)))


section_parser = (
    reqparse.RequestParser()
    .add_argument("name", type=str, required=True, location="form", help="Name is required")
    .add_argument("description", type=str, required=True, location="form", help="Description is required")
    .add_argument("image", type=FileStorage, required=False, location="files", help="Image is required")
)

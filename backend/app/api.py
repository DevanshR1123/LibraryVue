import base64
import datetime
import os
import re
import uuid

from flask import current_app as app
from flask import request
from flask_restful import Resource, marshal
from flask_security import auth_required, roles_accepted, current_user

from app.api_helpers import *
from app.models import Book, Comment, Rating, Section, db, User, BookIssue

BOOKS_DIR = app.config["BOOKS_DIR"]
IMAGE_DIR = app.config["IMAGE_DIR"]


class SearchAPI(Resource):
    def get(self):
        q = request.args.get("q")
        books = list(filter(lambda book: re.search(q, str(book) + str(book.section), re.IGNORECASE), Book.query.all()))
        return marshal(books, book_resource_fields)


class BookAPI(Resource):
    def get(self, id=None):
        if id:
            book: Book = Book.query.get_or_404(id, "Book not found")
            print(book.ratings)
            return marshal(book, book_resource_fields)
        else:
            books: list[Book] = Book.query.all()
            return marshal(books, book_resource_fields)

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def post(self):

        print(current_user)

        data = book_parser.parse_args()

        book: FileStorage = data.get("content")

        if not book:
            return {"message": "Content is required"}, 400

        content = f"{uuid.uuid4()}_{book.filename}"
        book.save(os.path.join(BOOKS_DIR, content))

        if not os.path.exists(os.path.join(BOOKS_DIR, content)):
            return {"message": "Content not saved"}, 500

        image_path = None

        image: FileStorage = data.get("image")
        if image:
            image_path = f"{uuid.uuid4()}_{image.filename}"
            image.save(os.path.join(IMAGE_DIR, image_path))
            if not os.path.exists(os.path.join(IMAGE_DIR, image_path)):
                return {"message": "Image not saved"}, 500

        for key in data:
            print(key, data[key], type(data[key]))

        book = Book(
            title=data.get("title"),
            author=data.get("author"),
            description=data.get("description"),
            isbn=data.get("isbn"),
            year=data.get("year"),
            content=content,
            image=image_path,
            section=Section.query.get_or_404(data.get("section_id"), "Section not found"),
            date_added=datetime.datetime.now(),
        )

        db.session.add(book)
        db.session.commit()
        return marshal(book, book_resource_fields), 201

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def put(self, id):
        data = book_parser.parse_args()
        book: Book = Book.query.get_or_404(id, "Book not found")
        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.description = data.get("description", book.description)
        book.isbn = data.get("isbn", book.isbn)
        book.year = data.get("year", book.year)

        content = data.get("content")
        if content:
            book.content = f"{uuid.uuid4()}_{content.filename}"
            content.save(os.path.join(BOOKS_DIR, book.content))

        image = data.get("image")
        if image:
            book.image = base64.b64encode(image.read()).decode("utf-8")

        section_id = data.get("section_id")
        if section_id:
            book.section = Section.query.get_or_404(section_id, "Section not found")

        db.session.commit()
        return marshal(book, book_resource_fields), 201

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def delete(self, id):
        book = Book.query.get_or_404(id, "Book not found")
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted successfully"}, 204


class SectionAPI(Resource):
    def get(self, id=None):
        if id:
            section = Section.query.get_or_404(id, "Section not found")
            return marshal(section, section_resource_fields)
        else:
            sections = Section.query.all()
            return marshal(sections, section_resource_fields)

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def post(self):
        data = section_parser.parse_args()

        image: FileStorage = data.get("image")

        print(data, image)

        image_path = None

        if image:
            image_path = f"{uuid.uuid4()}_{image.filename}"
            image.save(os.path.join(IMAGE_DIR, image_path))
            if not os.path.exists(os.path.join(IMAGE_DIR, image_path)):
                return {"message": "Image not saved"}, 500

        section = Section(name=data.get("name"), description=data.get("description"), image=image_path)

        db.session.add(section)
        db.session.commit()
        return marshal(section, section_resource_fields), 201

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def put(self, id):
        data = section_parser.parse_args()

        section: Section = Section.query.get_or_404(id, "Section not found")
        section.name = data.get("name")
        section.description = data.get("description")
        section.image = base64.b64encode(data.get("image").read()).decode("utf-8") if data.get("image") else None

        db.session.commit()
        return marshal(section, section_resource_fields), 201

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def delete(self, id):
        section = Section.query.get_or_404(id, "Section not found")
        db.session.delete(section)
        db.session.commit()
        return {"message": "Section deleted successfully"}, 204


class CommentAPI(Resource):
    def get(self, id=None):
        if id:
            comment = Comment.query.get_or_404(id, "Comment not found")
            return marshal(comment, comment_resource_fields)
        else:
            comments = Comment.query.all()
            return marshal(comments, comment_resource_fields)

    @auth_required("token")
    def post(self):
        data = comment_parser.parse_args()
        comment = Comment(
            user_id=data.get("user_id"),
            book_id=data.get("book_id"),
            content=data.get("content"),
        )
        db.session.add(comment)
        db.session.commit()
        return marshal(comment, comment_resource_fields)

    @auth_required("token")
    def put(self, id):
        data = comment_parser.parse_args()
        comment: Comment = Comment.query.get_or_404(id, "Comment not found")
        comment.content = data.get("content")
        db.session.commit()
        return marshal(comment, comment_resource_fields)

    @auth_required("token")
    def delete(self, id):
        comment = Comment.query.get_or_404(id, "Comment not found")
        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted successfully"}


class RatingAPI(Resource):
    @auth_required("token")
    def get(self):
        return marshal(current_user.ratings, rating_resource_fields)

    @auth_required("token")
    def post(self):
        data = new_rating_parser.parse_args()

        user_id = data.get("user_id")
        book_id = data.get("book_id")
        rating_value = data.get("rating")

        print(data)

        rating = Rating.query.filter_by(user_id=user_id, book_id=book_id).first()

        if rating:
            rating.rating = rating_value
        else:
            rating = Rating(user_id=user_id, book_id=book_id, rating=rating_value)
            db.session.add(rating)
        db.session.commit()

        return marshal(rating, rating_resource_fields), 201


class BookIssueAPI(Resource):

    @auth_required("token")
    def get(self):
        active_issues = BookIssue.query.filter_by(user_id=current_user.id, returned=False).all()
        return marshal(active_issues, issue_resource_fields)

    def post(self, id):

        user_id = current_user.id
        issue = BookIssue.query.filter_by(user_id=user_id, book_id=id, returned=False).first()

        if issue:
            return {"message": "Book already issued"}, 400

        issue_date = datetime.datetime.now()
        return_date = issue_date + datetime.timedelta(days=7)
        issue = BookIssue(user_id=user_id, book_id=id, issue_date=issue_date, return_date=return_date)
        db.session.add(issue)
        db.session.commit()
        return marshal(issue, issue_resource_fields), 201

    def put(self, id):
        pass

    @auth_required("token")
    def delete(self, id):
        user_id = current_user.id
        issue = BookIssue.query.filter_by(user_id=user_id, book_id=id, returned=False).first()
        issue.returned = True
        db.session.commit()
        return {"message": "Book returned successfully"}, 204

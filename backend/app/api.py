import base64
import os
import sys
import uuid

from flask import request, current_app as app
from flask_restful import Api, Resource, fields, marshal, reqparse
from flask_security import auth_required, roles_required

from app.api_helpers import *
from app.models import Book, BookIssue, Comment, Rating, Section, User, db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(sys.path)

BOOKS_DIR = os.path.join(sys.path[0], "books")

if not os.path.exists(BOOKS_DIR):
    os.makedirs(BOOKS_DIR)

api: Api = app.api


class SearchAPI(Resource):
    def get(self):
        q = request.args.get("q")
        books = (
            Book.query.filter(Book.title.ilike(f"%{q}%")).all()
            or Book.query.filter(Book.author.ilike(f"%{q}%")).all()
            or Book.query.filter(Book.description.ilike(f"%{q}%")).all()
            or Book.query.filter(Book.isbn.ilike(f"%{q}%")).all()
            or Book.query.filter(Book.year.ilike(f"%{q}%")).all()
            or Book.query.filter(Book.section.name.ilike(f"%{q}%")).all()
        )

        if not books:
            return {"message": "No books found"}, 404

        return marshal({"books": books}, books_resource_fields)


class BookAPI(Resource):
    def get(self, id=None):
        if id:
            book = Book.query.get_or_404(id, "Book not found")
            return marshal(book, book_resource_fields)
        else:
            books = Book.query.all()
            if not books:
                return {"message": "No books found"}, 404

            return marshal({"books": books}, books_resource_fields)

    @auth_required("token")
    @roles_required("admin", "librarian")
    def post(self):
        data = book_parser.parse_args()

        book: FileStorage = data.get("content")

        if not book:
            return {"message": "Content is required"}, 400

        content = f"{uuid.uuid4()}_{book.filename}"
        book.save(os.path.join(BOOKS_DIR, content))

        if not os.path.exists(os.path.join(BOOKS_DIR, content)):
            return {"message": "Content not saved"}, 500

        image = data.get("image")
        image = base64.b64encode(image.read()).decode("utf-8") if image else None

        book = Book(
            title=data.get("title"),
            author=data.get("author"),
            section=data.get("section"),
            description=data.get("description"),
            content=content,
            image=image,
        )

        db.session.add(book)
        db.session.commit()
        return marshal(book, book_resource_fields)

    @auth_required("token")
    @roles_required("admin", "librarian")
    def put(self, id):
        data = book_parser.parse_args()
        book: Book = Book.query.get_or_404(id, "Book not found")
        book.title = data.get("title")
        book.author = data.get("author")
        book.section = data.get("section")
        book.description = data.get("description")

        content = data.get("content")
        if content:
            book.content = f"{uuid.uuid4()}_{content.filename}"
            content.save(os.path.join(BOOKS_DIR, book.content))

        image = data.get("image")
        if image:
            book.image = base64.b64encode(image.read()).decode("utf-8")

        db.session.commit()
        return marshal(book, book_resource_fields)

    @auth_required("token")
    @roles_required("admin", "librarian")
    def delete(self, id):
        book = Book.query.get_or_404(id, "Book not found")
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted successfully"}


class SectionAPI(Resource):
    def get(self, id=None):
        if id:
            section = Section.query.get_or_404(id, "Section not found")
            return marshal(section, section_resource_fields)
        else:
            sections = Section.query.all()
            if not sections:
                return {"message": "No sections found"}, 404

            return marshal({"sections": sections}, sections_resource_fields)

    @auth_required("token")
    @roles_required("admin", "librarian")
    def post(self):
        data = section_parser.parse_args()

        image = base64.b64encode(data.get("image").read()).decode("utf-8") if data.get("image") else None

        section = Section(name=data.get("name"), description=data.get("description"), image=image)

        db.session.add(section)
        db.session.commit()
        return marshal(section, section_resource_fields)

    @auth_required("token")
    @roles_required("admin", "librarian")
    def put(self, id):
        data = section_parser.parse_args()

        section: Section = Section.query.get_or_404(id, "Section not found")
        section.name = data.get("name")
        section.description = data.get("description")
        section.image = base64.b64encode(data.get("image").read()).decode("utf-8") if data.get("image") else None

        db.session.commit()
        return marshal(section, section_resource_fields)

    @auth_required("token")
    @roles_required("admin", "librarian")
    def delete(self, id):
        section = Section.query.get_or_404(id, "Section not found")
        db.session.delete(section)
        db.session.commit()
        return {"message": "Section deleted successfully"}


class CommentAPI(Resource):
    def get(self, id=None):
        if id:
            comment = Comment.query.get_or_404(id, "Comment not found")
            return marshal(comment, comment_resource_fields)
        else:
            comments = Comment.query.all()
            if not comments:
                return {"message": "No comments found"}, 404

            return marshal({"comments": comments}, comments_resource_fields)

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
    def get(self):
        data = fetch_rating_parser.parse_args()
        if data.get("user_id"):
            ratings = Rating.query.filter_by(user_id=data.get("user_id")).all()
        elif data.get("book_id"):
            ratings = Rating.query.filter_by(book_id=data.get("book_id")).all()
        else:
            ratings = Rating.query.all()

        if not ratings:
            return {"message": "No ratings found"}, 404

        return marshal({"ratings": ratings}, ratings_resource_fields)

    @auth_required("token")
    def post(self):
        data = new_rating_parser.parse_args()
        rating = Rating(
            user_id=data.get("user_id"),
            book_id=data.get("book_id"),
            rating=data.get("rating"),
        )
        db.session.add(rating)
        db.session.commit()
        return marshal(rating, rating_resource_fields)

    @auth_required("token")
    def put(self, id):
        data = new_rating_parser.parse_args()
        rating: Rating = Rating.query.get_or_404(id, "Rating not found")
        rating.rating = data.get("rating")
        db.session.commit()
        return marshal(rating, rating_resource_fields)

    @auth_required("token")
    def delete(self, id):
        rating = Rating.query.get_or_404(id, "Rating not found")
        db.session.delete(rating)
        db.session.commit()
        return {"message": "Rating deleted successfully"}


class BookIssueAPI(Resource):
    def get(self, id=None):
        pass

    def post(self):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

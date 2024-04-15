import base64
import os
import re
import uuid

from datetime import datetime, timedelta

from flask import current_app as app
from flask import request
from flask_restful import Resource, marshal
from flask_security import auth_required, roles_accepted, current_user

from app.api_helpers import *
from app.models import Book, Comment, Rating, Section, db, BookIssue
from app.utils import is_valid_isbn

BOOKS_DIR = app.config["BOOKS_DIR"]
IMAGE_DIR = app.config["IMAGE_DIR"]

ISSUE_LIMIT = 5
ISSUE_DURATION = 7


class SearchAPI(Resource):
    def get(self):
        q = request.args.get("q")
        books = list(filter(lambda book: re.search(q, str(book) + str(book.section), re.IGNORECASE), Book.query.all()))
        return marshal(books, book_resource_fields)


class BookAPI(Resource):
    def get(self, id=None):
        if id:
            book: Book = Book.query.get_or_404(id, "Book not found")
            return marshal(book, book_resource_fields)
        else:
            books: list[Book] = Book.query.all()
            return marshal(books, book_resource_fields)

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def post(self):

        data = book_parser.parse_args()

        book: FileStorage = data.get("content")

        if not is_valid_isbn(data.get("isbn")):
            return {"message": "Invalid ISBN"}, 400

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

        book = Book(
            title=data.get("title"),
            author=data.get("author"),
            description=data.get("description"),
            isbn=data.get("isbn"),
            year=data.get("year"),
            content=content,
            image=image_path,
            section=Section.query.get_or_404(data.get("section_id"), "Section not found"),
            date_added=datetime.now(),
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
            book.image = f"{uuid.uuid4()}_{image.filename}"
            image.save(os.path.join(IMAGE_DIR, book.image))

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

        image: FileStorage = data.get("image")
        if image:
            section.image = f"{uuid.uuid4()}_{image.filename}"
            image.save(os.path.join(IMAGE_DIR, section.image))

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
    def get(self):
        return marshal(current_user.comments, comment_resource_fields)

    @auth_required("token")
    def post(self, id):
        data = comment_parser.parse_args()
        comment = Comment(user_id=current_user.id, book_id=id, content=data.get("content"))
        db.session.add(comment)
        db.session.commit()
        return marshal(comment, comment_resource_fields), 201

    @auth_required("token")
    def put(self, id):
        data = comment_parser.parse_args()
        comment = Comment.query.get_or_404(id, "Comment not found")
        comment.content = data.get("content")
        db.session.commit()
        return marshal(comment, comment_resource_fields), 201

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
    def post(self, id):
        data = new_rating_parser.parse_args()

        user_id = current_user.id
        rating_value = data.get("rating")
        rating = Rating.query.filter_by(user_id=user_id, book_id=id).first()

        if rating:
            rating.rating = rating_value
        else:
            rating = Rating(user_id=user_id, book_id=id, rating=rating_value)
            db.session.add(rating)
        db.session.commit()

        return marshal(rating, rating_resource_fields), 201


class BookIssueAPI(Resource):
    @auth_required("token")
    def get(self):
        return marshal(current_user.all_issues, librarian_issue_resource_fields)

    @auth_required("token")
    def post(self, id):

        user_id = current_user.id
        issue = BookIssue.query.filter_by(user_id=user_id, book_id=id, returned=False).first()

        if issue:
            return {"message": "Book already issued"}, 400

        if len(current_user.all_issues) >= ISSUE_LIMIT:
            return {"message": "Book issue limit reached"}, 400

        issue = BookIssue(user_id=user_id, book_id=id, request_date=datetime.now())
        db.session.add(issue)
        db.session.commit()
        return marshal(issue, issue_resource_fields), 201

    @auth_required("token")
    def put(self, id):
        user_id = current_user.id
        issue = BookIssue.query.filter_by(user_id=user_id, book_id=id, returned=False).first()
        if not issue:
            return {"message": "Book not issued yet"}, 404
        issue.returned = True
        db.session.commit()
        return {"message": "Book unissued successfully"}, 204

    @auth_required("token")
    @roles_accepted("admin", "librarian")
    def delete(self, id):
        user_id = current_user.id
        issue = BookIssue.query.filter_by(user_id=user_id, book_id=id, returned=False).first()

        if not issue:
            return {"message": "Book not issued yet"}, 404

        issue.returned = True
        db.session.commit()
        return {"message": "Book returned successfully"}, 204


class LibrarianIssueAPI(Resource):
    @auth_required("token")
    @roles_accepted("librarian")
    def get(self):
        issued_books = BookIssue.query.filter_by(returned=False, rejected=False).all()
        return marshal(issued_books, librarian_issue_resource_fields)

    @auth_required("token")
    @roles_accepted("librarian")
    def post(self, id):
        issue = BookIssue.query.get_or_404(id, "Issue request not found")

        if len(issue.user.active_issues) >= ISSUE_LIMIT:
            return {"message": "Book issue limit reached"}, 400

        if issue.granted:
            return {"message": "Issue request already granted"}, 400

        if not issue:
            return {"message": "Issue request not found"}, 404

        issue.issue_date = datetime.now()
        issue.return_date = issue.issue_date + timedelta(days=ISSUE_DURATION)
        issue.granted = True
        db.session.commit()
        return marshal(issue, issue_resource_fields), 201

    @auth_required("token")
    @roles_accepted("librarian")
    def put(self, id):
        issue = BookIssue.query.get_or_404(id, "Issue request not found")
        if issue.granted:
            return {"message": "Issue request already granted"}, 400
        issue.rejected = True
        db.session.commit()
        return {"message": "Issue request rejected successfully"}, 204

    @auth_required("token")
    @roles_accepted("librarian")
    def delete(self, id):
        issue = BookIssue.query.get_or_404(id, "Issue request not found")
        issue.granted = False
        issue.rejected = True
        db.session.commit()
        return {"message": "Issue request revoked successfully"}, 204

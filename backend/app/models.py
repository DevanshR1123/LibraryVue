from flask import request
from flask_security import RoleMixin, SQLAlchemyUserDatastore, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from datetime import datetime


db = SQLAlchemy()

# User Models


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", Integer(), ForeignKey("user.id"))
    role_id = Column("role_id", Integer(), ForeignKey("role.id"))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String, unique=True)
    password = Column(String(255))

    active = Column(Boolean())
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)

    fs_uniquifier = Column(String(255), unique=True, nullable=False)

    roles = relationship("Role", secondary="roles_users", backref=backref("users", lazy="dynamic"))
    books = relationship("Book", secondary="book_issue", back_populates="users", viewonly=True)
    issues = relationship("BookIssue", backref="user")
    ratings = relationship("Rating", backref="user")

    def get_security_payload(self):
        rv = super().get_security_payload()
        rv["id"] = self.id
        rv["email"] = self.email
        rv["firstname"] = self.firstname
        rv["lastname"] = self.lastname
        rv["roles"] = [role.name for role in self.roles]
        return rv

    def __repr__(self):
        return f"<User {self.email}>"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def all_issues(self):
        return [issue for issue in self.issues if issue.active or issue.requested]

    @property
    def requested_issues(self):
        return [issue for issue in self.issues if issue.requested]

    @property
    def active_issues(self):
        return [issue for issue in self.issues if issue.active]


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


# Library Models


class Section(db.Model):
    __tablename__ = "section"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    image = Column(String(255), nullable=True)
    books = relationship("Book", backref="section")

    def __repr__(self):
        return f"<Section {self.name}>"

    def __str__(self):
        return f"{self.name} - {self.description}"


class Book(db.Model):
    __tablename__ = "book"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    description = Column(String(255))
    isbn = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    content = Column(String(255))  # file path
    image = Column(String(255), nullable=True)  # file path
    date_added = Column(DateTime())
    section_id = Column(Integer, ForeignKey("section.id"), nullable=True)
    users = relationship("User", secondary="book_issue", back_populates="books", viewonly=True)
    issues = relationship("BookIssue", backref="book", cascade="all, delete-orphan")
    comments = relationship("Comment", backref="book", cascade="all, delete-orphan")
    ratings = relationship("Rating", backref="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return f"{self.title} - {self.author} - {self.year} - {self.isbn} - {self.description}"

    @property
    def issued(self):
        return any([issue.returned == False for issue in self.issues])

    @property
    def rating(self):
        ratings = [rating.rating for rating in self.ratings]
        return sum(ratings) / len(ratings) if ratings else 0


class Comment(db.Model):
    __tablename__ = "comment"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id", ondelete="cascade"), nullable=False)
    content = Column(String(255))
    timestamp = Column(DateTime())


class Rating(db.Model):
    __tablename__ = "rating"
    user_id = Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id", ondelete="cascade"), nullable=False, primary_key=True)
    rating = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Rating {self.rating}>"


class BookIssue(db.Model):
    __tablename__ = "book_issue"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    request_date = Column(DateTime())
    issue_date = Column(DateTime())
    return_date = Column(DateTime())
    returned = Column(Boolean(), default=False)
    granted = Column(Boolean(), default=False)
    rejected = Column(Boolean(), default=False)

    def __repr__(self):
        return f"<BookIssue [{self.user_id}, {self.book_id}] - A:{self.active} - R:{self.requested}>"

    @property
    def overdue(self):
        return self.return_date < datetime.now() if self.return_date else False

    @property
    def active(self):
        return not self.returned and self.granted

    @property
    def requested(self):
        return not self.returned and not self.granted


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

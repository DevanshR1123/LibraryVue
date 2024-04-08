from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean


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
    roles = db.relationship("Role", secondary="roles_users", backref=db.backref("users", lazy="dynamic"))

    def get_security_payload(self):
        rv = super().get_security_payload()
        rv["id"] = self.id
        rv["email"] = self.email
        rv["first_name"] = self.firstname
        rv["last_name"] = self.lastname
        rv["roles"] = [role.name for role in self.roles]
        return rv


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
    books = db.relationship("Book", backref="section", lazy="dynamic")


class Book(db.Model):
    __tablename__ = "book"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    description = Column(String(255))
    isbn = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    content = Column(String(255))  # file path
    image = Column(String(255), nullable=True)  # base64 encoded image
    date_added = Column(DateTime())
    section_id = Column(Integer, ForeignKey("section.id"), nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    content = Column(String(255))
    timestamp = Column(DateTime())


class Rating(db.Model):
    __tablename__ = "rating"
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False, primary_key=True)
    rating = Column(Integer, nullable=False)


class BookIssue(db.Model):
    __tablename__ = "book_issue"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    issue_date = Column(DateTime())
    return_date = Column(DateTime())
    returned = Column(Boolean(), default=False)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

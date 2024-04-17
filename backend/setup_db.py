import os
import uuid
from datetime import datetime, timedelta
from random import randint

import numpy as np
import pandas as pd

from application.config import LocalDevelopmentConfig
from application.models import Book, BookIssue, Comment, Rating, Section, db, user_datastore
from flask import Flask
from flask_security import Security, hash_password

# Create app
app = Flask(__name__)

# Create directories for storing books, images and graphs if they do not exist in the static
BOOKS_DIR = os.path.join(os.path.dirname(__file__), "./static/books")
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "./static/images")
GRAPH_DIR = os.path.join(os.path.dirname(__file__), "./static/graphs")

if not os.path.exists(BOOKS_DIR):
    os.makedirs(BOOKS_DIR)

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

if not os.path.exists(GRAPH_DIR):
    os.makedirs(GRAPH_DIR)

app.config["BOOKS_DIR"] = BOOKS_DIR
app.config["IMAGE_DIR"] = IMAGE_DIR
app.config["GRAPH_DIR"] = GRAPH_DIR

# Load configuration
app.config.from_object(LocalDevelopmentConfig)

# Create database connection object
db.init_app(app)

# Setup Flask-Security
app.security = Security(app, user_datastore)

sample_users = [
    {
        "email": "test.user@example.com",
        "password": "password",
        "firstname": "Test",
        "lastname": "User",
        "roles": ["user"],
    },
    {
        "email": "library.admin@example.com",
        "password": "password",
        "firstname": "Library",
        "lastname": "Admin",
        "roles": ["admin"],
    },
    {
        "email": "the.librarian@example.com",
        "password": "password",
        "firstname": "The",
        "lastname": "Librarian",
        "roles": ["librarian"],
    },
    {
        "email": "alice.user@example.com",
        "password": "password",
        "firstname": "Alice",
        "lastname": "User",
        "roles": ["user"],
    },
    {
        "email": "bob.user@example.com",
        "password": "password",
        "firstname": "Bob",
        "lastname": "User",
        "roles": ["user"],
    },
    {
        "email": "charlie.user@example.com",
        "password": "password",
        "firstname": "Charlie",
        "lastname": "User",
        "roles": ["user"],
    },
]

sample_comments = [
    "This book was a real page-turner! I couldn't put it down.",
    "The characters were so well-developed, I felt like I knew them personally.",
    "The writing style was beautiful and engaging.",
    "The plot was suspenseful and kept me guessing until the very end.",
    "This book is a must-read for anyone who enjoys [genre of the book].",
    "I learned so much from this book. It really opened my eyes to a new perspective.",
    "This book was a bit slow to start, but it picked up in the second half.",
    "The ending was a little disappointing, but overall I enjoyed the book.",
    "I found the writing style to be a bit dry.",
    "The characters were one-dimensional and not very relatable.",
    "The plot was predictable and there were no surprises.",
    "I wouldn't recommend this book unless you're a die-hard fan of the author.",
    "I struggled to finish this book. It just wasn't for me.",
]


# one time setup
with app.app_context():
    db.drop_all()
    print("Database tables dropped...")

    if os.path.exists(BOOKS_DIR):
        for file in os.listdir(BOOKS_DIR):
            os.remove(os.path.join(BOOKS_DIR, file))

    if os.path.exists(IMAGE_DIR):
        for file in os.listdir(IMAGE_DIR):
            os.remove(os.path.join(IMAGE_DIR, file))

    print("Files cleaned up...")

    db.create_all()

    print("Database tables created...")

    app.security.datastore.find_or_create_role(name="user", description="User Role")
    app.security.datastore.find_or_create_role(name="admin", description="Admin Role")
    app.security.datastore.find_or_create_role(name="librarian", description="Librarian Role")

    print("Roles created...")

    for user in sample_users:
        if not app.security.datastore.find_user(email=user["email"]):
            new_user = app.security.datastore.create_user(
                email=user["email"],
                password=hash_password(user["password"]),
                firstname=user["firstname"],
                lastname=user["lastname"],
                roles=user["roles"],
            )

            db.session.commit()
            user["id"] = new_user.id

    print("Users created...")

    # Create sections

    sections_to_id = {}

    sections = pd.read_csv("data/sections.csv")
    for _, section in sections.iterrows():
        image = f"{uuid.uuid4()}_{section['Section']}.jpeg"

        with open(os.path.join(IMAGE_DIR, image), "wb") as f:
            f.write(open(f"data/Sections/{section['Section']}.jpeg", "rb").read())

        section = Section(name=section["Section"], description=section["Description"], image=image)

        db.session.add(section)
        db.session.commit()
        sections_to_id[section.name] = section.id

    print("Sections created...")

    # Create books
    books = pd.read_csv("data/books.csv")
    for _, book in books.iterrows():
        image = f"{uuid.uuid4()}_{book['Image']}.jpeg"

        with open(os.path.join(IMAGE_DIR, image), "wb") as f:
            f.write(open(f"data/Covers/{book['Image']}.jpeg", "rb").read())

        content = f"{uuid.uuid4()}_{book['PDF']}.pdf"

        with open(os.path.join(BOOKS_DIR, content), "wb") as f:
            f.write(open(f"data/Books/{book['PDF']}.pdf", "rb").read())

        book = Book(
            title=book["Book"],
            author=book["Author"],
            isbn=book["ISBN"],
            year=book["Year"],
            description=book["Description"],
            image=image,
            content=content,
            section_id=sections_to_id[book["Section"]],
            date_added=datetime.now() - timedelta(days=randint(1, 365)),
        )

        db.session.add(book)

    db.session.commit()

    print("Books created...")

    users = [user for user in sample_users if "user" in user["roles"] and "test" not in user["email"]]

    # Create book issues
    for user in users:

        selected_books = np.random.choice(Book.query.all(), randint(3, 5), replace=False)
        for book in selected_books:

            issue = BookIssue(book=book, user_id=user["id"])

            issue.request_date = datetime.now() - timedelta(days=randint(1, 365))

            if randint(0, 1):
                issue.issue_date = issue.request_date + timedelta(
                    days=randint(1, (datetime.now() - issue.request_date).days)
                )
                issue.granted = True

            if randint(0, 1) and issue.issue_date:
                issue.return_date = issue.issue_date + timedelta(
                    days=randint(1, (datetime.now() - issue.issue_date).days)
                )
                issue.returned = True

            db.session.add(issue)

    db.session.commit()

    print(f"Book issues created...")

    # Create comments
    for book in Book.query.all():
        for _ in range(randint(1, 10)):
            user = np.random.choice(users)
            comment = np.random.choice(sample_comments)
            timestamp = datetime.now() - timedelta(days=randint(1, (datetime.now() - book.date_added).days))
            db.session.add(Comment(book=book, user_id=user["id"], content=comment, timestamp=timestamp))

    db.session.commit()

    print(f"Comments created...")

    # Create ratings
    selected_books = np.random.choice(Book.query.all(), randint(1, 10), replace=False)

    for book in selected_books:
        for user in users:
            rating = randint(1, 5)
            db.session.add(Rating(book=book, user_id=user["id"], rating=rating))

    db.session.commit()

    print(f"Ratings created...")


print("Database setup completed successfully...")

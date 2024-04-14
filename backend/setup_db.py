from flask import Flask
from flask_security import Security, hash_password
from app.config import LocalDevelopmentConfig
from app.models import db, user_datastore, Section

# Create app
app = Flask(__name__)

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


# one time setup
with app.app_context():
    # Create User to test with if it doesn't exist
    db.drop_all()
    db.create_all()

    print("Database tables created...")

    app.security.datastore.find_or_create_role(name="user", description="User Role")
    app.security.datastore.find_or_create_role(name="admin", description="Admin Role")
    app.security.datastore.find_or_create_role(name="librarian", description="Librarian Role")

    print("Roles created...")

    for user in sample_users:
        if not app.security.datastore.find_user(email=user["email"]):
            app.security.datastore.create_user(
                email=user["email"],
                password=hash_password(user["password"]),
                firstname=user["firstname"],
                lastname=user["lastname"],
                roles=user["roles"],
            )

    db.session.commit()

    print("Users created...")


# Clean up files
import os

BOOKS_DIR = os.path.join(os.path.dirname(__file__), "./static/books")
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "./static/images")

if os.path.exists(BOOKS_DIR):
    for file in os.listdir(BOOKS_DIR):
        os.remove(os.path.join(BOOKS_DIR, file))

if os.path.exists(IMAGE_DIR):
    for file in os.listdir(IMAGE_DIR):
        os.remove(os.path.join(IMAGE_DIR, file))

print("Files cleaned up...")


print("Database setup completed successfully...")

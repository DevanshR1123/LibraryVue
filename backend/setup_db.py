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
        "email": "devansh.rathor@example.com",
        "password": "password",
        "firstname": "Devansh",
        "lastname": "Rathor",
        "roles": ["admin"],
    },
    {
        "email": "test.user@example.com",
        "password": "password",
        "firstname": "Test",
        "lastname": "User",
        "roles": ["user"],
    },
    {
        "email": "test.admin@example.com",
        "password": "password",
        "firstname": "Test",
        "lastname": "Admin",
        "roles": ["admin"],
    },
    {
        "email": "test.librarian@example.com",
        "password": "password",
        "firstname": "Test",
        "lastname": "Librarian",
        "roles": ["librarian"],
    },
]


# one time setup
with app.app_context():
    # Create User to test with if it doesn't exist
    db.create_all()

    app.security.datastore.find_or_create_role(name="user", description="User Role")
    app.security.datastore.find_or_create_role(name="admin", description="Admin Role")
    app.security.datastore.find_or_create_role(name="librarian", description="Librarian Role")

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
    
    print("Database setup completed successfully...")

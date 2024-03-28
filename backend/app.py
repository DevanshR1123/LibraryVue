from flask import Flask, render_template_string, request
from flask_security import Security, auth_required, hash_password
from flask_cors import CORS
from flask_restful import Api
from app.models import db, user_datastore, Book
from app.config import LocalDevelopmentConfig
from app.api import TestAPI

# Create app
app = Flask(__name__)

# Load configuration
app.config.from_object(LocalDevelopmentConfig)

# Enable CORS
CORS(app)

# Create database connection object
db.init_app(app)

# Setup Flask-Security
app.security = Security(app, user_datastore)

# Setup Flask-Restful
api = Api(app)

app.app_context().push()


from app.routes import *


# Add resources
api.add_resource(TestAPI, "/api/test")


# one time setup
with app.app_context():
    # Create User to test with if it doesn't exist
    db.create_all()
    app.security.datastore.find_or_create_role(name="user", description="User Role")
    app.security.datastore.find_or_create_role(name="admin", description="Admin Role")
    app.security.datastore.find_or_create_role(
        name="librarian", description="Librarian Role"
    )

    if not app.security.datastore.find_user(email="test@me.com"):
        app.security.datastore.create_user(
            email="test@me.com",
            password=hash_password("password"),
            firstname="Test",
            lastname="Admin",
            roles=["user"],
        )
    db.session.commit()

if __name__ == "__main__":
    app.run()

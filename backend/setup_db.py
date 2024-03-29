from flask import Flask
from flask_security import Security, hash_password
from app.config import LocalDevelopmentConfig
from app.models import db, user_datastore

# Create app
app = Flask(__name__)

# Load configuration
app.config.from_object(LocalDevelopmentConfig)

# Create database connection object
db.init_app(app)

# Setup Flask-Security
app.security = Security(app, user_datastore)

app.app_context().push()


# one time setup
with app.app_context():
    # Create User to test with if it doesn't exist
    db.create_all()
    app.security.datastore.find_or_create_role(name="user", description="User Role")
    app.security.datastore.find_or_create_role(name="admin", description="Admin Role")
    app.security.datastore.find_or_create_role(name="librarian", description="Librarian Role")

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

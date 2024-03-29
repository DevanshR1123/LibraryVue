from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_security import Security

from app.api import TestAPI
from app.config import LocalDevelopmentConfig
from app.models import db, user_datastore

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

# Import routes
from app.routes import *

# Add resources
api.add_resource(TestAPI, "/api/test")


# one time setup
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_security import Security
from flask_caching import Cache

from application.config import LocalDevelopmentConfig
from application.models import db, user_datastore
from application.cache import cache, redis_client

import os

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

# Enable CORS
CORS(app)

# Create database connection object
db.init_app(app)

# Setup Flask-Security
app.security = Security(app, user_datastore)

# Setup Flask-Restful
api = Api(app)

cache.init_app(app)

app.extensions["redis"] = redis_client

# Push app context
app.app_context().push()


# Import Celery
from application.celery.celery import celery

app.extensions["celery"] = celery

app.app_context().push()

# Import routes
from application.routes import *

# Add resources
from application.api import SearchAPI, BookAPI, SectionAPI, CommentAPI, RatingAPI, BookIssueAPI, LibrarianIssueAPI

api.add_resource(SearchAPI, "/search")
api.add_resource(BookAPI, "/books", "/books/<int:id>")
api.add_resource(SectionAPI, "/sections", "/sections/<int:id>")
api.add_resource(CommentAPI, "/comments", "/comments/<int:id>")
api.add_resource(RatingAPI, "/ratings", "/ratings/<int:id>")
api.add_resource(BookIssueAPI, "/issues", "/issues/<int:id>")
api.add_resource(LibrarianIssueAPI, "/librarian/issues", "/librarian/issues/<int:id>")


# one time setup
with app.app_context():
    db.create_all()


# Run app
if __name__ == "__main__":
    app.run()

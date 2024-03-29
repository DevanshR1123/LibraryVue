from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_security import Security

from app.api import SearchAPI, BookAPI, SectionAPI, CommentAPI, RatingAPI, BookIssueAPI
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
api.add_resource(SearchAPI, "/search")
api.add_resource(BookAPI, "/books", "/books/<int:id>")
api.add_resource(SectionAPI, "/sections", "/sections/<int:id>")
api.add_resource(CommentAPI, "/comments", "/comments/<int:id>")
api.add_resource(RatingAPI, "/ratings", "/ratings/<int:id>")
api.add_resource(BookIssueAPI, "/book-issues", "/book-issues/<int:id>")


# one time setup
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()

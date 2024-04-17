from dotenv import load_dotenv

load_dotenv()

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False

    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}

    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_AUTHENTICATION_KEY = "token"
    SECURITY_TOKEN_MAX_AGE = 86400
    SECURITY_TOKEN_URL_SAFE = True

    WTF_CSRF_ENABLED = False

    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"

    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0


class LocalDevelopmentConfig(Config):
    DEBUG = True

    # SQLite database
    SQLITE_DB_DIR = os.path.join(basedir, "../")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "asecretkeythatyouwillneverguess")
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "saltysalt")
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_TRACKABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None

    # Flask-Restful
    WTF_CSRF_ENABLED = False

    # CORS
    CORS_HEADERS = "Content-Type"

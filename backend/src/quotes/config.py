import logging
import os

from dotenv import load_dotenv
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()
mail = Mail()


class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SWAGGER_URL = os.getenv("SWAGGER_URL", "/api/docs")
    API_URL = os.getenv("API_URL", "/static/swagger.yml")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    # SQLALCHEMY_DATABASE_URI = "sqlite:///quotes.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
    )
    SQL_SCRIPTS_DIR = os.getenv("SQL_SCRIPTS_DIR")
    # Flask-Mail configuration for development
    # MAIL_SERVER = "smtp-server"
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_SUPPRESS_SEND = True
    MAIL_DEFAULT_SENDER = "no-reply@localhost"


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

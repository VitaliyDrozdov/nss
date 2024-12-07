import logging
import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


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
    # SQLALCHEMY_DATABASE_URI = (
    #     "postgresql://nss_users_user:nss_users_password@users_db:5432/nss_db"
    # )
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
    )


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

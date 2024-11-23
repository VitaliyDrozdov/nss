import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SWAGGER_URL = os.getenv("SWAGGER_UR", "/api/docs")
    API_URL = os.getenv("API_URL", "/static/swagger.json")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", "sqlite:///quotes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
    )
    # MDM_URL = os.getenv("MDM_URL", "http://mdm-service/api/subjects")

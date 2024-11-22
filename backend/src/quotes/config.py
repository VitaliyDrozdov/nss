import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.json"
    # MDM_URL = os.getenv("MDM_URL", "http://mdm-service/api/subjects")

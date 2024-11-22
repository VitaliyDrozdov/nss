from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from quotes.config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    CORS(app)
    swaggerui_blueprint = get_swaggerui_blueprint(
        base_url=app.config["SWAGGER_URL"],
        api_url=app.config["API_URL"],
        config={"app_name": "Quotes API"},
    )
    from .routes import bp

    app.register_blueprint(
        swaggerui_blueprint, url_prefix=app.config["SWAGGER_URL"]
    )

    app.register_blueprint(bp, url_prefix="/api")
    return app

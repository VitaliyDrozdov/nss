from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from quotes.config import Config
from quotes.routes.auth import bp as bp_auth
from quotes.routes.quotes import bp as bp_quotes


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    CORS(app)
    swaggerui_blueprint = get_swaggerui_blueprint(
        base_url=app.config["SWAGGER_URL"],
        api_url=app.config["API_URL"],
        config={"app_name": "Quotes API"},
    )

    app.register_blueprint(
        swaggerui_blueprint, url_prefix=app.config["SWAGGER_URL"]
    )

    app.register_blueprint(bp_quotes, url_prefix="/api")
    app.register_blueprint(bp_auth, url_prefix="/api/auth")
    return app

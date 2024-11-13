from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    SWAGGER_URL = "/api/docs"
    # TODO: актуализировать схему в сваггере
    API_URL = "/static/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        base_url=SWAGGER_URL,
        api_url=API_URL,
        config={"app_name": "Quotes API"},
    )
    from .routes import bp

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    app.register_blueprint(bp, url_prefix="/api")
    return app

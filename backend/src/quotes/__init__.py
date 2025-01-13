from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from quotes.config import Config, db, mail
from quotes.models.core import Documents  # noqa: F401
from quotes.models.core import Models  # noqa: F401
from quotes.models.core import Products  # noqa: F401
from quotes.models.core import Subjects  # noqa: F401
from quotes.models.dq import Actions  # noqa: F401
from quotes.routes import bp_auth, bp_dq, bp_dwh, bp_quotes


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
    app.register_blueprint(bp_dq, url_prefix="/api/dq")
    app.register_blueprint(bp_dwh, url_prefix="/api/dwh")
    app.register_blueprint(bp_obs, url_prefix="/api/observability")
    db.init_app(app)  # Связь экземпляра бд с приложением
    migrate = Migrate(app, db)  # Создание миграций
    mail.init_app(app)
    return app

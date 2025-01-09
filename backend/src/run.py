import os

from dotenv import load_dotenv
from flask_migrate import Migrate

from quotes import create_app
from quotes.models.auth import db
from quotes.models.core import Documents  # noqa: F401
from quotes.models.core import Models  # noqa: F401
from quotes.models.core import Products  # noqa: F401
from quotes.models.core import Subjects  # noqa: F401
from quotes.utils.db_tables import bulk_insert_data
from quotes.utils.users import create_admin

load_dotenv()

app = create_app()

db.init_app(app)  # Связь экземпляра бд с приложением
migrate = Migrate(app, db)  # Создание миграций


if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()  # Создание таблиц в БД
            create_admin()  # Создание пользователя-админа
            bulk_insert_data()
    except Exception as e:
        print(f"An error occurred: {e}")

    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=os.getenv("FLASK_RUN_PORT", "5000"),
        debug=os.getenv("DEBUG", "True"),
    )

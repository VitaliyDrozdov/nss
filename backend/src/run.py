import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from quotes import create_app
from quotes.models.auth import db
from quotes.utils import create_admin

load_dotenv()

app = create_app()

db.init_app(app)  # Связь экземпляра бд с приложением
migrate = Migrate(app, db)  # Создание миграций

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создание таблиц в БД
        create_admin()
    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=os.getenv("FLASK_RUN_PORT", "5000"),
        debug=app.config["DEBUG"],
    )

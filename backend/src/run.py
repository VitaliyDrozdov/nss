import os

from dotenv import load_dotenv

from quotes import create_app
from quotes.config import Config, db
from quotes.utils import (
    bulk_insert_core_data,
    create_admins,
    create_initial_roles,
)
from scripts.sql_script import execute_sql_file

load_dotenv()

app = create_app()


if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()  # Создание таблиц в БД
            create_initial_roles()
            create_admins()  # Создание пользователей-админов
            bulk_insert_core_data()
            execute_sql_file(f"./src/scripts/{Config.SQL_FILENAME}")
    except Exception as e:
        print(f"An error occurred: {e}")

    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=os.getenv("FLASK_RUN_PORT", "5000"),
        debug=os.getenv("DEBUG", "True"),
    )

import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from quotes import create_app
from quotes.config import logger
from quotes.models.auth import db
from quotes.utils.db_tables import (CREATE_SCHEMAS_COMMANDS,
                                    CREATE_TABLES_COMMANDS)
from quotes.utils.users import create_admin
from sqlalchemy import text

load_dotenv()

app = create_app()

db.init_app(app)  # Связь экземпляра бд с приложением
migrate = Migrate(app, db)  # Создание миграций

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quotes/db")
TEST_SQL_COMMAND_1 = """
CREATE SCHEMA IF NOT EXISTS new_schema;
"""

TEST_SQL_COMMAND_2 = """
CREATE TABLE IF NOT EXISTS new_schema.test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
"""

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()  # Создание таблиц в БД
            create_admin()  # Создание пользователя-админа
            # execute_all(DIR)
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.info(
                    f"Database connection test result: {result.fetchone()}"
                )

                connection.execute(text(TEST_SQL_COMMAND_1))
                connection.execute(text(TEST_SQL_COMMAND_2))
                connection.execute(text(CREATE_SCHEMAS_COMMANDS))
                connection.execute(text(CREATE_TABLES_COMMANDS))
            test_query_2 = connection.execute(
                text(
                    """SELECT schema_name
                    FROM information_schema.schemata;
                    """
                )
            )
            logger.info(f"Database schemas: {test_query_2.fetchall()}")
            test_query = connection.execute(
                text(
                    """
                    SELECT table_schema, table_name
                    FROM information_schema.tables
                WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_schema, table_name;
                        """
                )
            )
            logger.info(f"Database tables: {test_query.fetchall()}")
    except Exception as e:
        print(f"An error occurred: {e}")

    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=os.getenv("FLASK_RUN_PORT", "5000"),
        debug=app.config["DEBUG"],
    )

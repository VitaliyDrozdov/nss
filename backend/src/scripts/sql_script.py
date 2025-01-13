import os

import psycopg2

from quotes.config import Config, logger


def execute_sql_file(sql_file_path):

    try:
        if not os.path.exists(sql_file_path):
            current_dir = os.getcwd()
            raise FileNotFoundError(
                f"SQL файл '{sql_file_path}' не найден."
                f"Текущая рабочая директория: '{current_dir}'"
            )
        with open(sql_file_path, "r") as file:
            sql_script = file.read()

        with psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            dbname=Config.DB_NAME,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)
                conn.commit()
                logger.info(
                    f"SQL-скрипт из '{sql_file_path}' успешно выполнен!"
                )
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except psycopg2.Error as db_error:
        logger.error(f"Ошибка БД: {db_error}")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    sql_file_path = "./src/scripts/update_sql.sql"

import os

from quotes.config import db, logger


def execute_sql(file_path):
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            commands = f.read()
    except Exception as e:
        logger.exception(f"Error: {e}")
    with db.engine.connect() as con:
        try:
            for command in commands.split(";"):
                if com := command.strip():
                    con.execute(com)
            logger.info("SQL executed")
        except Exception as e:
            logger.exception(f"Error executing SQL commands: {e}")


def execute_all(directory="../d"):
    for filename in sorted(os.listdir(directory)):
        try:
            file_path = os.path.join("../d", filename)
            execute_sql(file_path)
        except Exception as e:
            logger.exception(f"Error: {e}")

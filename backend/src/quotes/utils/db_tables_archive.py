# import os
# from sqlalchemy import text

# from quotes.config import db, logger

CREATE_SCHEMAS_COMMANDS = """
CREATE SCHEMA IF NOT EXISTS mdm;
CREATE SCHEMA IF NOT EXISTS ml;
CREATE SCHEMA IF NOT EXISTS fs;
"""
CREATE_TABLES_COMMANDS = """
CREATE TABLE IF NOT EXISTS mdm.subjects (
    id serial PRIMARY key,
    first_name varchar(50),
    second_name varchar(50),
    middle_name varchar(50),
    birth_date date,
    gender varchar(15)
);

CREATE TABLE IF NOT EXISTS mdm.documeents (
    id serial PRIMARY key,
    subject_id int REFERENCES mdm.subjects (id),
    document_type varchar(100),
    document_number int,
    issue_date date
);

CREATE TABLE IF NOT EXISTS fs.products (
    id serial PRIMARY key,
    type text
);

CREATE TABLE IF NOT EXISTS ml.models (
    model_id serial,
    model_name varchar(25) NOT NULL UNIQUE,
    product_id int,
    status bool NOT NULL,
    model_version varchar(5) NOT NULL DEFAULT 1.0,
    model_description varchar(100),
    PRIMARY KEY (model_id),
    FOREIGN KEY (product_id) REFERENCES fs.products (id)
);

CREATE TABLE IF NOT EXISTS fs.products_features (
    product_id int,
    feature_name varchar(150),
    PRIMARY key (product_id, feature_name)
);

CREATE TABLE IF NOT EXISTS features_values (
    subject_id int,
    feature_name varchar(100),
    feature_value varchar(150)
);
"""

# def execute_sql(file_path):
#     try:
#         with open(file_path, mode="r", encoding="utf-8") as f:
#             commands = f.read()
#     except Exception as e:
#         logger.exception(f"Error: {e}")
#     with db.engine.connect() as con:
#         try:
#             logger.info(f"commands: {commands}")
#             for command in commands.split(";"):
#                 if com := command.strip():
#                     con.execute(text(com))
#                     logger.info("SQL command executed")
#                 else:
#                     logger.error("No SQL command found")

#         except Exception as e:
#             logger.exception(f"Error executing SQL commands: {e}")


# def execute_all(directory):
#     dir = sorted(os.listdir(directory))
#     logger.info(f"dir: {dir}")
#     for filename in dir:
#         try:
#             file_path = os.path.join(directory, filename)
#             execute_sql(file_path)
#         except Exception as e:
#             logger.exception(f"Error: {e}")

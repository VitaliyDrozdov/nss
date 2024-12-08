CREATE TABLE
    IF NOT EXISTS mdm.subjects (
        id serial PRIMARY key,
        first_name varchar(50),
        second_name varchar(50),
        middle_name varchar(50),
        birth_date date,
        gender varchar(15)
    );

CREATE table
    IF NOT EXISTS mdm.documeents (
        id serial PRIMARY key,
        subject_id int REFERENCES mdm.subjects (id),
        document_type varchar(100),
        document_number int,
        issue_date date
    );

CREATE TABLE
    if not EXISTS fs.products (id serial PRIMARY key, type text);

CREATE TABLE
    if not EXISTS nl.models (
        model_id serial,
        model_name varchar(25) NOT NULL UNIQUE,
        product_id int,
        status bool NOT NULL,
        model_version varchar(5) NOT NULL DEFAULT 1.0,
        model_description varchar(100),
        PRIMARY KEY (model_id),
        FOREIGN KEY (product_id) REFERENCES fs.products (id)
    );

CREATE TABLE
    if not EXISTS fs.products_features (
        product_id int,
        feature_name varchar(150),
        PRIMARY key (product_id, feature_name)
    );

CREATE TABLE
    if not EXISTS fs.features_values (
        subject_id int,
        feature_name varchar(100),
        feature_value varchar(150)
    );

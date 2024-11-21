CREATE SCHEMA IF NOT EXISTS mdm;

CREATE TABLE
    IF NOT EXISTS subjects (
        id serial,
        first_name varchar(50),
        second_name varchar(50),
        middle_name varchar(50),
        birth_date date,
        gender varchar(15)
    );

CREATE table
    IF NOT EXISTS documeents (
        subject_id serial,
        document_type enum,
        document_number int,
        issue_date date
    );

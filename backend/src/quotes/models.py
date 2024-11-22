"""
Модуль для работы с данными котировок и их валидации.

Содержит определения моделей данных.
Используется Pydantic для валидации данных.


"""

import uuid
from datetime import datetime, timedelta
from typing import List, Literal, Optional

from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, field_validator, model_validator

db = SQLAlchemy()


class Document(BaseModel):
    documentType: str
    documentNumber: str
    issueDate: str

    @field_validator("documentType")
    @classmethod
    def validate_document_type(cls, value):
        if value != "passport":
            raise ValueError('document type must be "passport"')
        return value

    @model_validator(mode="after")
    def check_required(self):
        for field_name, field_value in self.__dict__.items():
            if not field_value:
                raise ValueError(f"{field_name} should not be empty.")
        return self


class Subject(BaseModel):
    firstName: str
    secondName: str
    middleName: Optional[str] = None
    birthDate: str
    gender: str
    documents: List[Document]

    @field_validator(
        "firstName", "secondName", "birthDate", "gender", "documents"
    )
    @classmethod
    def check_not_empty(cls, value):
        if not value or (isinstance(value, list) and len(value) == 0):
            raise ValueError("subject should not be empty")
        return value


class Header(BaseModel):
    runId: str
    quoteId: str
    dateTime: str

    @model_validator(mode="after")
    def check_required(self):
        for field_name, field_value in self.__dict__.items():
            if not field_value:
                raise ValueError(f"{field_name} should not be empty")
        return self


class Product(BaseModel):
    productType: Literal["osago", "life"]
    productCode: str

    @model_validator(mode="after")
    def check_required(self):
        for field_name, field_value in self.__dict__.items():
            if not field_value:
                raise ValueError(f"{field_name} should not be empty.")
        return self


class Quote(BaseModel):
    header: Header
    product: Product
    subjects: List[Subject]

    @model_validator(mode="after")
    def check_required(self):
        for field_name, field_value in self.__dict__.items():
            if field_value is None or not field_value:
                raise ValueError(f"{field_name} should not be empty.")
        return self


class QuoteData(BaseModel):
    quote: Quote


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    token_expiry = db.Column(db.DateTime, nullable=False)
    # role = db.Column(db.String(50), default="user")

    def generate_token(self, expiration=3600):
        token = str(uuid.uuid4())
        self.token = token
        self.token_expiry = datetime.now() + timedelta(seconds=expiration)
        db.session.commit()
        return token

    def check_token(self, token):
        if self.token == token and self.token_expiry > datetime.now():
            return True
        return False

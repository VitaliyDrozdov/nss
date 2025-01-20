"""
Модуль для работы с данными котировок и их валидации.

Содержит определения моделей данных.
Используется Pydantic для валидации данных.


"""

from typing import List, Optional

from pydantic import BaseModel, field_validator, model_validator


class Document(BaseModel):
    documentType: str
    documentNumber: str
    issueDate: str

    # @field_validator("documentType")
    # @classmethod
    # def validate_document_type(cls, value):
    #     if value not in ["passport", "driving license"]:
    #         raise ValueError(
    #             'document type must be "passport" or "driving license"'
    #         )
    #     return value

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
    # productType: Literal["osago", "life"]
    productType: str
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

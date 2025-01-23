import random
from datetime import date

from quotes.config import db, logger
from quotes.models.core import (
    Documents,
    FeaturesValues,
    Models,
    Products,
    ProductsFeatures,
    Subjects,
)
from quotes.models.dq import Actions, CheckProductStatus, Checks

data = {
    Subjects: [
        {
            "first_name": "Петр",
            "second_name": "Петров",
            "middle_name": "Петрович",
            "birth_date": date(1990, 1, 1),
            "gender": "Male",
        },
        {
            "first_name": "Анастасия",
            "second_name": "Титова",
            "middle_name": "Андреевна",
            "birth_date": date(1992, 2, 2),
            "gender": "Female",
        },
        {
            "first_name": "Илья",
            "second_name": "Иванов",
            "middle_name": "Александрович",
            "birth_date": date(1973, 4, 17),
            "gender": "Male",
        },
        {
            "first_name": "Николай",
            "second_name": "Горшков",
            "middle_name": "Сергеев",
            "birth_date": date(1992, 8, 12),
            "gender": "Male",
        },
        {
            "first_name": "Константин",
            "second_name": "Галкин",
            "middle_name": "Максимович",
            "birth_date": date(1989, 2, 21),
            "gender": "Male",
        },
        {
            "first_name": "Софья",
            "second_name": "Малышева",
            "middle_name": "Иванова",
            "birth_date": date(1997, 12, 12),
            "gender": "Female",
        },
        {
            "first_name": "Илья",
            "second_name": "Иванов",
            "middle_name": "Александрович",
            "birth_date": date(1988, 3, 3),
            "gender": "Male",
        },
        {
            "first_name": "Виктория",
            "second_name": "Степанова",
            "middle_name": "Михайловна",
            "birth_date": date(1998, 4, 6),
            "gender": "Female",
        },
    ],
    Documents: [
        {
            "subject_id": 1,
            "document_type": "passport",
            "document_number": 123456789,
            "issue_date": date(2010, 5, 20),
        },
        {
            "subject_id": 2,
            "document_type": "passport",
            "document_number": 987654321,
            "issue_date": date(2015, 8, 15),
        },
        {
            "subject_id": 3,
            "document_type": "passport",
            "document_number": 456123789,
            "issue_date": date(2018, 12, 10),
        },
        {
            "subject_id": 4,
            "document_type": "passport",
            "document_number": 321654987,
            "issue_date": date(2020, 6, 25),
        },
        {
            "subject_id": 5,
            "document_type": "passport",
            "document_number": 123456782,
            "issue_date": date(2001, 5, 20),
        },
        {
            "subject_id": 6,
            "document_type": "passport",
            "document_number": 987654322,
            "issue_date": date(2007, 8, 17),
        },
        {
            "subject_id": 7,
            "document_type": "passport",
            "document_number": 456123782,
            "issue_date": date(2001, 12, 11),
        },
        {
            "subject_id": 8,
            "document_type": "passport",
            "document_number": 321654983,
            "issue_date": date(1999, 6, 26),
        },
    ],
    Products: [
        {"product_code": "prod001", "product_type": "osago"},
        {"product_code": "prod002", "product_type": "life"},
    ],
    ProductsFeatures: [
        {"product_code": "prod001", "feature_name": "driver_region"},
        {"product_code": "prod001", "feature_name": "driver_kvs"},
        {"product_code": "prod001", "feature_name": "driver_gender"},
        {"product_code": "prod001", "feature_name": "driver_age"},
        {"product_code": "prod001", "feature_name": "driver_bonus"},
        {"product_code": "prod002", "feature_name": "client_age"},
        {"product_code": "prod002", "feature_name": "client_gender"},
        {"product_code": "prod002", "feature_name": "client_smoking_status"},
        {"product_code": "prod002", "feature_name": "client_BMI"},
        {"product_code": "prod002", "feature_name": "client_occupation_risk"},
        {"product_code": "prod002", "feature_name": "client_medical_history"},
        {
            "product_code": "prod002",
            "feature_name": "client_residence_region_mortality",
        },
    ],
    Models: [
        {
            "model_name": "randomcop",
            "product_code": "prod001",
            "status": True,
            "model_version": "1.0",
            "model_description": "Скоринговая модель ",
        },
        {
            "model_name": "badcop",
            "product_code": "prod001",
            "status": True,
            "model_version": "1.1",
            "model_description": (
                "Скоринговая модель " "с низкими шансами на одобрение"
            ),
        },
        {
            "model_name": "goodcop",
            "product_code": "prod001",
            "status": True,
            "model_version": "1.1",
            "model_description": "Скоринговая ",
        },
        {
            "model_name": "life_insurance",
            "product_code": "prod002",
            "status": True,
            "model_version": "0.9",
            "model_description": (
                "Модель предназначена для расчета скора по продукту "
                "СТРАХОВАНИЕ ЖИЗНИ"
            ),
        },
    ],
    Actions: [
        {"action_id": 1, "action_name": "delete"},
        {"action_id": 2, "action_name": "enable"},
        {"action_id": 3, "action_name": "disable"},
    ],
    Checks: [
        {
            "check_id": 1,
            "type": "DQ1",
            "check_name": "JSON schema check",
        },
        {
            "check_id": 2,
            "type": "DQ2.1",
            "check_name": "DQ2.1 проверка продутка",
        },
        {
            "check_id": 3,
            "type": "DQ2.2",
            "check_name": "DQ2.2 проверка субъекта",
        },
        {
            "check_id": 4,
            "type": "DQ2.3",
            "check_name": "DQ2.3 проверка документов",
        },
    ],
    CheckProductStatus: [
        {"product_code": "prod001", "check_id": 1, "condition": True},
        {"product_code": "prod001", "check_id": 2, "condition": True},
        {"product_code": "prod002", "check_id": 1, "condition": False},
        {"product_code": "prod002", "check_id": 2, "condition": False},
        {"product_code": "prod001", "check_id": 3, "condition": True},
        {"product_code": "prod001", "check_id": 4, "condition": True},
        {"product_code": "prod002", "check_id": 3, "condition": False},
        {"product_code": "prod002", "check_id": 4, "condition": False},
    ],
}


def bulk_insert_core_data():
    try:
        for model, records in data.items():
            objects = [model(**record) for record in records]
            db.session.bulk_save_objects(objects)
        db.session.commit()
        insert_features_values()
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error occured: {e}")


def insert_features_values():
    try:
        features = ProductsFeatures.query.all()
        subjects = Subjects.query.all()
        for f in features:
            for s in subjects:
                feature_value = random.uniform(0, 1)
                value_record = FeaturesValues(
                    subject_id=s.id,
                    feature_name=f.feature_name,
                    feature_value=round(feature_value, 2),
                )
                db.session.add(value_record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error occured: {e}")

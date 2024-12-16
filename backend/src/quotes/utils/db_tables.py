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

data = {
    Subjects: [
        {
            "first_name": "John",
            "second_name": "Doe",
            "middle_name": "Middle",
            "birth_date": date(1990, 1, 1),
            "gender": "Male",
        },
        {
            "first_name": "Jane",
            "second_name": "Smith",
            "middle_name": "Ann",
            "birth_date": date(1992, 2, 2),
            "gender": "Female",
        },
        {
            "first_name": "Alice",
            "second_name": "Brown",
            "middle_name": "Marie",
            "birth_date": date(1988, 3, 3),
            "gender": "Female",
        },
        {
            "first_name": "Bob",
            "second_name": "White",
            "middle_name": "Lee",
            "birth_date": date(1995, 4, 4),
            "gender": "Male",
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
    ],
    Products: [
        {"type": "osago"},
        {"type": "life"},
    ],
    ProductsFeatures: [
        {"product_id": 1, "feature_name": "driver_region"},
        {"product_id": 1, "feature_name": "driver_kvs"},
        {"product_id": 1, "feature_name": "driver_gender"},
        {"product_id": 1, "feature_name": "driver_age"},
        {"product_id": 1, "feature_name": "driver_bonus"},
        {"product_id": 2, "feature_name": "client_age"},
        {"product_id": 2, "feature_name": "client_gender"},
        {"product_id": 2, "feature_name": "client_smoking_status"},
        {"product_id": 2, "feature_name": "client_BMI"},
        {"product_id": 2, "feature_name": "client_occupation_risk"},
        {"product_id": 2, "feature_name": "client_medical_history"},
        {"product_id": 2, "feature_name": "client_residence_region_mortality"},
    ],
    Models: [
        {
            "model_name": "randomcop",
            "product_id": 1,
            "status": True,
            "model_version": "1.0",
            "model_description": "Скоринговая модель ",
        },
        {
            "model_name": "badcop",
            "product_id": 1,
            "status": True,
            "model_version": "1.1",
            "model_description": (
                "Скоринговая модель " "с низкими шансами на одобрение"
            ),
        },
        {
            "model_name": "goodcop",
            "product_id": 1,
            "status": True,
            "model_version": "1.1",
            "model_description": "Скоринговая ",
        },
        {
            "model_name": "life_insurance",
            "product_id": 2,
            "status": True,
            "model_version": "0.9",
            "model_description": (
                "Модель предназначена для расчета скора по продукту "
                "СТРАХОВАНИЕ ЖИЗНИ"
            ),
        },
    ],
}


def bulk_insert_data():
    try:
        # for model in reversed(data.keys()):
        #     db.session.query(model).delete()
        #     db.session.commit()
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

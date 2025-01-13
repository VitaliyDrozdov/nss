import hashlib

from flask import Blueprint, jsonify, request
from sqlalchemy import text

from quotes.config import db, logger
from quotes.routes.dq import dq1

bp = Blueprint("quotes", __name__)


def send_to_mdm(data):
    """
    Получение subject ids.

    Args:
        data (QuoteData): Validated data.

    Returns:
        dict: словарь из run ID и subject IDs.
        tuple: в случае ошибки JSON response и HTTP status code.
    """
    run_id = data.quote.header.runId
    subjects = data.quote.subjects
    subject_ids = list()
    for subject in subjects:
        first_name = subject.firstName
        second_name = subject.secondName
        birth_date = subject.birthDate
        documents = subject.documents
        for document in documents:
            document_type = document.documentType
            document_number = document.documentNumber
            issue_date = document.issueDate
            query = text(
                """
                SELECT s.id
                FROM "mdm.subjects" s
                JOIN "mdm.documents" d ON s.id = d.subject_id
                WHERE s.first_name = :first_name
                AND s.second_name = :second_name
                AND s.birth_date = :birth_date
                AND d.document_type = :document_type
                AND d.document_number = :document_number
                AND d.issue_date = :issue_date
            """
            )
            result = db.session.execute(
                query,
                {
                    "first_name": first_name,
                    "second_name": second_name,
                    "birth_date": birth_date,
                    "document_type": document_type,
                    "document_number": document_number,
                    "issue_date": issue_date,
                },
            ).fetchall()
            if result:
                subject_ids.extend(row[0] for row in result)
    if not subject_ids:
        return None
    return {"runId": run_id, "subjectIds": subject_ids}


def get_features(data, product_code):
    """Получение списка фичей."""
    run_id = data["runId"]
    subject_ids = data["subjectIds"]
    logger.info(f"Get features for subjectIds: {subject_ids}")
    features = list()
    for subj_id in subject_ids:

        query = text(
            """SELECT features.feature_name, feature_value
            FROM "fs.product_features" features

            JOIN "fs.feature_values" feature_values
            ON features.feature_name = feature_values.feature_name

            JOIN "fs.products" products
            ON products.product_code = features.product_code

            WHERE
            products.product_code = :product_code
            AND subject_id = :subj_id
            """
        )
        result = db.session.execute(
            query, {"product_code": product_code, "subj_id": subj_id}
        ).fetchall()
        feature_dict = dict()
        for res in result:
            feature_name, feature_value = res
            feature_dict[feature_name] = feature_value
        if feature_dict:
            features.append(feature_dict)
    logger.info("Получены фичи: %s", features)
    if not features:
        return None
    return {"runId": run_id, "features": features}


def hash_based_score(input_string, min_value=0.0, max_value=1.0):
    """Генерирует значение в заданном диапазоне на основе хэша строки."""
    hash_value = int(hashlib.md5(input_string.encode()).hexdigest(), 16)
    range_size = max_value - min_value
    normalized_value = (
        hash_value % 10000
    ) / 10000.0  # Значение в диапазоне [0, 1]
    return min_value + normalized_value * range_size


def predict(data, product_code=1, model_id=1):
    """Получение скорингового балла."""
    features_string = str(data["features"]) + str(model_id)
    if model_id == 1:  # randomcop
        prediction = hash_based_score(features_string, 0.0, 1.0)
    elif model_id == 2:  # badcop
        prediction = hash_based_score(features_string, 0.0, 0.5)
    elif model_id == 3:  # goodcop
        prediction = hash_based_score(features_string, 0.5, 1.0)
    elif model_id == 4:  # life_insurance
        prediction = hash_based_score(features_string, 0.0, 1.0)
    else:
        prediction = None  # Неизвестная модель

    logger.info("Got result of prediction: %s", prediction)
    return {
        "predict": {
            "percent": f"{prediction * 100:.2f}%",
            "score": prediction,
            "model_id": model_id,
        },
    }


@bp.route("/quote", methods=["POST"])
def handle_quote():
    """
    Принимает на вход json, отправляет запросы на MDM, Feature
    Proxy.
    Возращает результат скоринга из ML модели.

    """
    input_data = request.get_json()
    if input_data is None:
        return jsonify({"error": "No data in request"}), 400
    try:
        # ответ от dq1 эндпоинта:
        dq1_response = dq1(input_data)
        if isinstance(dq1_response, tuple):
            dq1_data, dq1_status_code = dq1_response
            # если ошибка, то добавляем указание какая dq не прошла:
            if dq1_status_code != 200 and dq1_status_code != 403:
                dq1_data = dq1_data.get_json()
                dq1_data["type"] = "DQ1 failed"
                return jsonify(dq1_data), dq1_status_code
        # если все ок, то просто дальше возращаем ответ:c
        validated_data = dq1_response
    except Exception as e:
        return (
            jsonify({"error": "Exception occured", "details": f"{str(e)}"}),
            400,
        )
    mdm_response = send_to_mdm(validated_data)  # отправка запроса на mdm
    if not mdm_response:
        return jsonify({"error": "no subjects found with input data"}), 404
    product_code = validated_data.quote.product.productCode
    features_response = get_features(mdm_response, product_code)
    if not features_response:
        return jsonify({"error": "no features found"}), 404
    prediction = predict(
        features_response,
        product_code,
    )
    if not prediction:
        return jsonify({"error": "could not make predicition"}), 400
    return jsonify(prediction), 200

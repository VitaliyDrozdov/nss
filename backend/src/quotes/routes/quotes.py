import logging

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from quotes.config import db
from quotes.core.mdm import send_to_mdm
from quotes.utils import validate_input_data
from sqlalchemy import text

bp = Blueprint("quotes", __name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_features(data, product_code):
    """Заглушка для запроса фичей из Feature Service."""
    run_id = data["runId"]
    subject_ids = data["subjectIds"]
    logger.info(f"Get features for subjectIds: {subject_ids}")
    features_response = {
        "runId": run_id,
        "features": [
            {
                "driver_region": "Moscow",
                "driver_kvs": "0.7",
                "driver_gender": "male",
                "driver_age": "30",
                "driver_bonus": "1",
            }
        ],
    }
    logger.info("Получены фичи: %s", features_response)
    return features_response


def send_vector_to_proxy(data, product_code):
    """Заглушка для отправки вектора в Proxy Service."""
    run_id = data["runId"]
    prediction_response = {
        "runId": run_id,
        "routedTo": "osago",
        "predict": {"percent": "38.62%", "score": 0.3862294713942135},
    }

    logger.info("Got result of prediction: %s", prediction_response)
    return prediction_response


@bp.route("/quote", methods=["POST"])
def handle_quote():
    """
    Эндпоинт /quote для сервиса оркестрации.

    Принимает на вход json, отправляет запросы на MDM, Feature
    Proxy.
    Возращает результат скоринга из ML модели.

    """
    input_data = request.get_json()
    if input_data is None:
        return jsonify({"error": "No data in request"}), 400
    try:
        validated_data = validate_input_data(input_data)
    except ValidationError as e:
        logger.error(
            f"validation error: {str(e)}",
        )
        return (
            jsonify({"error": "validation error", "details": f"{str(e)}"}),
            400,
        )
    except Exception as e:
        logger.info(f"Internal error: {str(e)}")
        return jsonify({"error": f"internal server error {str(e)}"}), 500

    mdm_response = send_to_mdm(validated_data)  # отправка запроса на mdm
    product_code = validated_data.quote.product.productCode
    features_response = get_features(mdm_response, product_code)
    prediction = send_vector_to_proxy(
        features_response,
        product_code,
    )
    return jsonify(prediction), 200


@bp.route("/db_data", methods=["GET"])
def get_data():
    with db.engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                ORDER BY table_schema, table_name;
                """
            )
        )
        tables = [
            {"schema": row[0], "table": row[1]} for row in result.fetchall()
        ]
    return jsonify({"tables": tables})

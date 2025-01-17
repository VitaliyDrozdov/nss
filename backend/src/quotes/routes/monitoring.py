from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from quotes.config import db
from quotes.utils import token_required

bp = Blueprint("monitoring", __name__)


@bp.route("/", methods=["GET", "POST"])
@token_required
def get_report_logs(user):
    base_query = """
    SELECT id, model_name, metric_name, monitoring_type, calculation_date
    FROM model_monitoring.report_log
    WHERE 1=1
    """

    count_query = """
    SELECT COUNT(*)
    FROM model_monitoring.report_log
    WHERE 1=1
    """

    filters = {}
    if request.method == "POST":
        incoming_filters = request.json or {}
    else:
        incoming_filters = request.args.to_dict()

    if "model_name" in incoming_filters:
        base_query += " AND model_name = :model_name"
        count_query += " AND model_name = :model_name"
        filters["model_name"] = incoming_filters["model_name"]
    if "metric_name" in incoming_filters:
        base_query += " AND metric_name = :metric_name"
        count_query += " AND metric_name = :metric_name"
        filters["metric_name"] = incoming_filters["metric_name"]
    if "monitoring_type" in incoming_filters:
        base_query += " AND monitoring_type = :monitoring_type"
        count_query += " AND monitoring_type = :monitoring_type"
        filters["monitoring_type"] = incoming_filters["monitoring_type"]
    if "calculation_date" in incoming_filters:
        try:
            filters["calculation_date"] = datetime.strptime(
                incoming_filters["calculation_date"], "%Y-%m-%dT%H:%M:%S"
            )
            base_query += " AND calculation_date >= :calculation_date"
            count_query += " AND calculation_date >= :calculation_date"
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "Invalid calculation_date format. Use YYYY-MM-DDTHH:MM:SS."  # noqa
                    }
                ),
                400,
            )

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    if (page and page < 1) or (page and per_page) < 1:
        return (
            jsonify({"error": "Pagination parameters must be positive"}),
            400,
        )
    offset = (page - 1) * per_page
    base_query += " LIMIT :per_page OFFSET :offset"

    filters["per_page"] = per_page
    filters["offset"] = offset

    try:
        total_records = db.session.execute(text(count_query), filters).scalar()
        result = db.session.execute(text(base_query), filters).mappings()
        rows = [dict(row) for row in result]
        total_pages = (total_records + per_page - 1) // per_page
        db.session.commit()
        return (
            jsonify(
                {
                    "page": page,
                    "total_pages": total_pages,
                    "total_records": total_records,
                    "per_page": per_page,
                    "data": rows,
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()


@bp.route("/create", methods=["POST"])
@token_required
def create_report_log(user):
    VALID_MODEL_NAMES = {"osago", "life_insurance"}
    VALID_MONITORING_TYPES = {"On-demand", "Scheduled"}
    data = request.json
    try:
        if (
            not data.get("model_name")
            or not data.get("metric_name")
            or not data.get("monitoring_type")
        ):
            return (
                jsonify(
                    {
                        "error": "Missing required fields",
                        "detail": "required: model_name, metric_name, monitoring_type.",  # noqa E501
                    }
                ),
                400,
            )

        if data.get("model_name") not in VALID_MODEL_NAMES:
            return (
                jsonify(
                    {
                        "error": f"Invalid model_name. Valid values are {', '.join(VALID_MODEL_NAMES)}."  # noqa E501
                    }
                ),
                400,
            )
        if data.get("monitoring_type") not in VALID_MONITORING_TYPES:
            return (
                jsonify(
                    {
                        "error": f"Invalid monitoring_type. Valid values are {', '.join(VALID_MONITORING_TYPES)}."  # noqa E501
                    }
                ),
                400,
            )
        insert_query = """
        INSERT INTO model_monitoring.report_log (model_name, metric_name, monitoring_type, calculation_date)
        VALUES (:model_name, :metric_name, :monitoring_type, :calculation_date)
        RETURNING id
        """  # noqa E501
        params = {
            "model_name": data["model_name"],
            "metric_name": data["metric_name"],
            "monitoring_type": data["monitoring_type"],
            "calculation_date": datetime.utcnow(),
        }

        result = db.session.execute(text(insert_query), params)
        db.session.commit()

        new_report_log_id = result.fetchone()[0]
        return (
            jsonify(
                {"message": "Report log created", "id": new_report_log_id}
            ),
            201,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

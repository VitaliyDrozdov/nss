from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from quotes.config import db
from quotes.utils import token_required

bp = Blueprint("dwh", __name__)


@bp.route("/", methods=["GET", "POST"])
@token_required
def get_data(user):
    base_query = """
    SELECT product_type, run_id, quote_id, briefcase_date, start_date, end_date,
    model_name, feature_name, feature_value, predict, is_insurance_case,
    data_insurance_case
    FROM dwh.data_mart
    WHERE 1=1
    """  # noqa E501

    count_query = """
    SELECT COUNT(*)
    FROM dwh.data_mart
    WHERE 1=1
    """
    filters = {}
    if request.method == "POST":
        incoming_filters = request.json or {}
    else:
        incoming_filters = request.args.to_dict()

    if "product_type" in incoming_filters:
        base_query += " AND product_type = :product_type"
        count_query += " AND product_type = :product_type"
        filters["product_type"] = incoming_filters["product_type"]
    if "model_name" in incoming_filters:
        base_query += " AND model_name = :model_name"
        count_query += " AND model_name = :model_name"
        filters["model_name"] = incoming_filters["model_name"]
    if "is_insurance_case" in incoming_filters:
        base_query += " AND is_insurance_case = :is_insurance_case"
        count_query += " AND is_insurance_case = :is_insurance_case"
        filters["is_insurance_case"] = incoming_filters[
            "is_insurance_case"
        ] in ["true", "1", True]

    if "feature_name" in incoming_filters:
        base_query += " AND feature_name = :feature_name"
        count_query += " AND feature_name = :feature_name"
        filters["feature_name"] = incoming_filters["feature_name"]
    if "start_date" in incoming_filters:
        try:
            filters["start_date"] = datetime.strptime(
                incoming_filters["start_date"], "%Y-%m-%d"
            )
            base_query += " AND start_date >= :start_date"
            count_query += " AND start_date >= :start_date"
        except ValueError:
            return (
                jsonify(
                    {"error": "Invalid start_date format. Use YYYY-MM-DD."}
                ),
                400,
            )
    if "end_date" in incoming_filters:
        try:
            filters["end_date"] = datetime.strptime(
                incoming_filters["end_date"], "%Y-%m-%d"
            )
            base_query += " AND end_date <= :end_date"
            count_query += " AND end_date <= :end_date"
        except ValueError:
            return (
                jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD."}),
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

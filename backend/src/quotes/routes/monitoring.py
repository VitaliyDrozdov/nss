import csv
import io
import os
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from flask import Blueprint, jsonify, request, send_file
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
        date_filter = incoming_filters["calculation_date"]
        now = datetime.now()

        if date_filter == "lastMonth":
            # first_day_this_month = now.replace(day=1)
            # last_day_last_month = first_day_this_month - timedelta(days=1)
            # start_date = last_day_last_month.replace(day=1)
            # end_date = first_day_this_month
            start_date = now = relativedelta(months=1)
        elif date_filter == "last3Months":
            start_date = now = relativedelta(months=3)
        elif date_filter == "lastWeek":
            start_date = now - timedelta(weeks=1)
            end_date = now
        elif date_filter == "lastYear":
            start_date = now.replace(year=now.year - 1)
            end_date = now
        else:
            return jsonify({"error": "Invalid calculation_date filter"}), 400
        base_query += " AND calculation_date >= :start_date AND calculation_date <= :end_date"  # noqa E501
        count_query += " AND calculation_date >= :start_date AND calculation_date <= :end_date"  # noqa E501
        filters["start_date"] = start_date
        filters["end_date"] = end_date

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
# @token_required
def create_report_log():
    data = request.json
    VALID_MODEL_NAMES = {"OSAGO", "LIFE_INSURANCE"}
    VALID_MONITORING_TYPES = {"On-demand", "Scheduled"}
    VALID_TIME_PERIODS = ["lastWeek", "lastMonth", "lastYear"]
    if (
        "time_period" not in data
        or data["time_period"] not in VALID_TIME_PERIODS
    ):
        return (
            jsonify(
                {
                    "error": "Invalid or missing time_period."
                    "Valid values are lastWeek, lastMonth, lastYear."
                }
            ),
            400,
        )
    time_period = data.get("time_period")
    now = datetime.now()
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
        model_name = data.get("model_name")
        if model_name.upper() not in VALID_MODEL_NAMES:
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

        if time_period == "lastWeek":
            start_date = now - timedelta(weeks=1)
        elif time_period == "last3Months":
            start_date = now = relativedelta(months=3)
        elif time_period == "lastMonth":
            # first_day_this_month = now.replace(day=1)
            # last_day_last_month = first_day_this_month - timedelta(days=1)
            # start_date = last_day_last_month.replace(day=1)
            start_date = now = relativedelta(months=1)
        elif time_period == "lastYear":
            start_date = now.replace(year=now.year - 1)
        end_date = now
        query = """
        SELECT feature_name, feature_value, start_date, end_date
        FROM dwh.data_mart
        WHERE start_date >= :start_date
        """
        # TODO:  WHERE + model_name
        q_params = {
            "start_date": start_date,
            "end_date": end_date,
            "model_name": model_name,
        }

        result = db.session.execute(text(query), q_params).mappings()
        rows = result.fetchall()

        # csv_file = io.StringIO()
        # csv_writer = csv.writer(csv_file)
        # csv_writer.writerow(["feature_name", "feature_value", "time_period"])
        os.makedirs("reports", exist_ok=True)
        file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join("reports", file_name)
        with open(file_path, "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                ["feature_name", "feature_value", "time_period"]
            )

            for row in rows:
                feature_name = row["feature_name"]
                feature_value = row["feature_value"]
                time_period_label = (
                    f"{start_date.strftime('%Y-%m-%d')}"
                    f"to {end_date.strftime('%Y-%m-%d')}"
                )
                csv_writer.writerow(
                    [feature_name, feature_value, time_period_label]
                )

        insert_query = """
        INSERT INTO model_monitoring.report_log (model_name, metric_name, monitoring_type, calculation_date, file)
        VALUES (:model_name, :metric_name, :monitoring_type, :calculation_date, :file)
        RETURNING id
        """  # noqa E501
        params = {
            "model_name": data["model_name"],
            "metric_name": data["metric_name"],
            "monitoring_type": data["monitoring_type"],
            "calculation_date": datetime.now(),
            "file": file_path,
        }
        result = db.session.execute(text(insert_query), params)
        db.session.commit()

        new_report_id = result.fetchone()[0]
        return (
            jsonify({"message": "Report log created", "id": new_report_id}),
            201,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()


@bp.route("/download/<int:report_id>", methods=["GET"])
# @token_required
def download_report(report_id):
    query = """
    SELECT file
    FROM model_monitoring.report_log
    WHERE id = :report_id
    """
    result = db.session.execute(text(query), {"report_id": report_id})
    file_path = result.fetchone()
    if not file_path:
        return (
            jsonify({"error": "File not found", "result": f"{file_path}"}),
            404,
        )

    try:
        with open(file_path[0], "rb") as f:
            file_data = f.read()
        return send_file(
            io.BytesIO(file_data),
            as_attachment=True,
            download_name=f"report_{report_id}.csv",
        )
    except FileNotFoundError:
        return jsonify({"error": "File not found", "check": "test"}), 404

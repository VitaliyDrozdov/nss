from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from quotes.config import db
from quotes.utils import token_required

bp = Blueprint("observability", __name__)


@bp.route("/", methods=["GET", "POST"])
@token_required
def get_incidents(user):
    base_query = """
    SELECT id_incident, state, priority, description, last_updated, service, trace_id
    FROM observability.incidents
    WHERE 1=1
    """  # noqa E501

    count_query = """
    SELECT COUNT(*)
    FROM observability.incidents
    WHERE 1=1
    """

    filters = {}
    if request.method == "POST":
        incoming_filters = request.json or {}
    else:
        incoming_filters = request.args.to_dict()

    if "state" in incoming_filters:
        base_query += " AND state = :state"
        count_query += " AND state = :state"
        filters["state"] = incoming_filters["state"]
    if "priority" in incoming_filters:
        base_query += " AND priority = :priority"
        count_query += " AND priority = :priority"
        filters["priority"] = incoming_filters["priority"]
    if "id_incident" in incoming_filters:
        base_query += " AND id_incident = :id_incident"
        count_query += " AND id_incident = :id_incident"
        filters["id_incident"] = incoming_filters["id_incident"]
    if "service" in incoming_filters:
        base_query += " AND service = :service"
        count_query += " AND service = :service"
        filters["service"] = incoming_filters["service"]
    if "trace_id" in incoming_filters:
        base_query += " AND trace_id = :trace_id"
        count_query += " AND trace_id = :trace_id"
        filters["trace_id"] = incoming_filters["trace_id"]
    if "last_updated" in incoming_filters:
        try:
            filters["last_updated"] = datetime.strptime(
                incoming_filters["last_updated"], "%Y-%m-%dT%H:%M:%S"
            )
            base_query += " AND last_updated >= :last_updated"
            count_query += " AND last_updated >= :last_updated"
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "Invalid last_updated format. Use YYYY-MM-DDTHH:MM:SS."  # noqa
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
def create_incident(user):
    VALID_STATES = ["Active", "In Progress", "Resolved"]
    VALID_PRIORITIES = ["High", "Medium", "Low"]
    data = request.json
    try:
        if (
            not data.get("state")
            or not data.get("priority")
            or not data.get("service")
        ):
            return (
                jsonify(
                    {
                        "error": "Missing required fields",
                        "detail": "required: state, priority, service.",
                    }
                ),
                400,
            )
        if data.get("state") not in VALID_STATES:
            return (
                jsonify(
                    {
                        "error": f"Invalid state. Valid values are {', '.join(VALID_STATES)}."  # noqa
                    }
                ),
                400,
            )
        if data.get("priority") not in VALID_PRIORITIES:
            return (
                jsonify(
                    {
                        "error": f"Invalid priority. Valid values are {', '.join(VALID_PRIORITIES)}."  # noqa
                    }
                ),
                400,
            )

        insert_query = """
        INSERT INTO observability.incidents (state, priority, description, last_updated, service, trace_id)
        VALUES (:state, :priority, :description, :last_updated, :service, :trace_id)
        RETURNING id_incident
        """  # noqa E501
        params = {
            "state": data["state"],
            "priority": data["priority"],
            "description": data.get("description", None),
            "last_updated": datetime.now(),
            "service": data["service"],
            "trace_id": data.get("trace_id", 1009),
        }

        result = db.session.execute(text(insert_query), params)
        db.session.commit()

        new_incident_id = result.fetchone()[0]
        return (
            jsonify(
                {"message": "Incident created", "incident_id": new_incident_id}
            ),
            201,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()


@bp.route("/<int:id_incident>", methods=["PUT", "DELETE"])
@token_required
def update_incident(user, id_incident):
    VALID_STATES = ["Active", "In Progress", "Resolved"]
    VALID_PRIORITIES = ["High", "Medium", "Low"]
    data = request.json
    try:
        select_query = "SELECT id_incident FROM observability.incidents WHERE id_incident = :id_incident"  # noqa
        incident = db.session.execute(
            text(select_query), {"id_incident": id_incident}
        ).fetchone()
        if not incident:
            return jsonify({"error": "Incident not found"}), 404
        if request.method == "PUT":
            if (
                not data.get("state")
                or not data.get("priority")
                or not data.get("service")
                or not data.get("trace_id")
            ):
                return jsonify({"error": "Missing required fields"}), 400
            update_query = """
            UPDATE observability.incidents
            SET state = :state,
                priority = :priority,
                description = :description,
                last_updated = :last_updated,
                service = :service,
                trace_id = :trace_id
            WHERE id_incident = :id_incident
            """

            params = {
                "state": data.get("state"),
                "priority": data.get("priority"),
                "description": data.get("description"),
                "last_updated": datetime.utcnow(),
                "service": data.get("service"),
                "trace_id": data.get("trace_id"),
                "id_incident": id_incident,
            }

            if params.get("state") not in VALID_STATES:
                return (
                    jsonify(
                        {
                            "error": f"Invalid state. Valid values are {', '.join(VALID_STATES)}."  # noqa
                        }
                    ),
                    400,
                )
            if params.get("priority") not in VALID_PRIORITIES:
                return (
                    jsonify(
                        {
                            "error": f"Invalid priority. Valid values are {', '.join(VALID_PRIORITIES)}."  # noqa
                        }
                    ),
                    400,
                )
            db.session.execute(text(update_query), params)
            db.session.commit()

            return (
                jsonify(
                    {"message": "Incident updated", "incident": id_incident}
                ),
                200,
            )

        elif request.method == "DELETE":
            delete_query = """
            DELETE FROM observability.incidents
            WHERE id_incident = :id_incident
            """
            db.session.execute(
                text(delete_query), {"id_incident": id_incident}
            )
            db.session.commit()
            return jsonify({"message": "Incident deleted successfully"}), 204

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

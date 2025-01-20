from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from quotes.config import db
from quotes.models.core import Models, Scores
from quotes.utils import admin_required, token_required

bp = Blueprint("model_catalog", __name__)


@bp.route("/", methods=["GET", "POST"])
@token_required
@admin_required
def get_models(user):
    if request.method == "GET":
        base_query = """
        SELECT model_id, product_code, model_name, status, model_version,
        model_description,
            creation_date, last_launch_date, last_modified_date
        FROM "ml.models"
        WHERE 1=1
        """
        count_query = """
        SELECT COUNT(*)
        FROM "ml.models"
        WHERE 1=1
        """

        filters = {}

        incoming_filters = request.args.to_dict()

        if "model_name" in incoming_filters:
            base_query += " AND model_name ILIKE :model_name"
            count_query += " AND model_name ILIKE :model_name"
            filters["model_name"] = f"%{incoming_filters['model_name']}%"

        try:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))
        except ValueError:
            return jsonify({"error": "Invalid pagination parameters"}), 400

        if page < 1 or per_page < 1:
            return (
                jsonify({"error": "Pagination parameters must be positive"}),
                400,
            )

        offset = (page - 1) * per_page
        base_query += " LIMIT :per_page OFFSET :offset"
        filters["per_page"] = per_page
        filters["offset"] = offset

        try:
            total_records = db.session.execute(
                text(count_query), filters
            ).scalar()
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

    elif request.method == "POST":
        data = request.json

        required_fields = ["model_name", "product_code", "status"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"'{field}' is required"}), 400

        new_model = Models(
            model_name=data["model_name"],
            product_code=data["product_code"],
            status=data["status"],
            model_version=data.get("model_version", "1.0"),
            model_description=data.get("model_description", ""),
            creation_date=datetime.now(),
            last_launch_date=None,
            last_modified_date=datetime.now(),
        )
        try:
            db.session.add(new_model)
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "Model created successfully",
                        "model_id": new_model.model_id,
                    }
                ),
                201,
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


@bp.route("/<int:model_id>", methods=["GET", "PUT", "DELETE"])
def model_detail(model_id):
    model = Models.query.get(model_id)
    if request.method == "GET":
        try:
            return (
                jsonify(
                    {
                        "model_id": model.model_id,
                        "product_code": model.product_code,
                        "model_name": model.model_name,
                        "status": model.status,
                        "model_version": model.model_version,
                        "model_description": model.model_description,
                        "creation_date": model.creation_date,
                        "last_launch_date": model.last_launch_date,
                        "last_modified_date": model.last_modified_date,
                    }
                ),
                200,
            )
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500
    if request.method == "PUT":
        data = request.json
        model_name = data.get("model_name")
        if model_name:
            model.model_name = model_name

        product_code = data.get("product_code")
        if product_code:
            model.product_code = product_code

        status = data.get("status")
        if status is not None:
            model.status = status

        model_version = data.get("model_version")
        if model_version:
            model.model_version = model_version

        model_description = data.get("model_description")
        if model_description:
            model.model_description = model_description

        model.last_modified_date = datetime.now()

        try:
            db.session.commit()
            return jsonify({"message": "Model updated successfully"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    elif request.method == "DELETE":

        if Scores.query.filter_by(model_id=model_id).first():
            return (
                jsonify(
                    {"error": "Cannot delete model with associated scores"}
                ),
                400,
            )

    try:
        db.session.delete(model)
        db.session.commit()
        return jsonify({"message": "Model deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

from datetime import datetime

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from quotes.config import db
from quotes.models.core import Products
from quotes.models.dq import CheckHistory, CheckProductStatus, Checks, Requests
from quotes.utils import admin_required, token_required, validate_input_data

bp = Blueprint("dq", __name__)


def calculate_age(birth_date):
    birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.today()
    age = (
        today.year
        - birth_date_obj.year
        - (
            (today.month, today.day)
            < (birth_date_obj.month, birth_date_obj.day)
        )
    )
    return age


def log_request(data, product_code, runId, status="received"):
    """
    Записывает информацию о поступившем JSON-запросе в таблицу Requests.
    """
    runId = data.get("quote").get("header").get("runId")
    if db.session.query(Requests).filter(Requests.runId == runId).first():
        return
    try:
        new_request = Requests(
            runId=runId,
            request=data,
            product_code=product_code,
            status=status,
            date=datetime.now(),
            deleted=False,
        )
        db.session.add(new_request)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Ошибка записи запроса в БД: {str(e)}")


def log_check_history(check_id, product_type, status, runId):
    """
    Логирует данные проверки в таблицу истории.
    """
    existing_log = (
        db.session.query(CheckHistory)
        .filter(
            CheckHistory.check_id == check_id,
            CheckHistory.product_type == product_type,
            CheckHistory.runId == runId,
        )
        .first()
    )

    if existing_log:
        existing_log.status = status
    else:
        new_entry = CheckHistory(
            check_id=check_id,
            product_type=product_type,
            status=status,
            date=datetime.now(),
            runId=runId,
        )
        db.session.add(new_entry)
    db.session.commit()


def validate_check_type(check_type, product_code):
    check = db.session.query(Checks).filter(Checks.type == check_type).first()
    product_check_status = (
        db.session.query(CheckProductStatus)
        .filter(
            CheckProductStatus.check_id == check.check_id,
            CheckProductStatus.product_code == product_code,
        )
        .first()
        .condition
    )
    if check:
        return check, product_check_status
    else:
        return jsonify({"error": "Проверка не найдена в БД."}), 400


def dq1(data=None):
    if data is None:
        data = request.get_json()
    product_code = data.get("quote").get("product").get("productCode", None)
    runId = data.get("quote").get("header").get("runId", None)
    if product_code is None:
        return (
            jsonify(
                {"error": "productCode не найден. Проверьте структуру JSON."}
            ),
            400,
        )
    product = (
        db.session.query(Products)
        .filter(Products.product_code == product_code)
        .first()
    )
    if not product:
        return (
            jsonify(
                {"error": f"productCode '{product_code}' не существует в БД."}
            ),
            400,
        )
    check, check_status = validate_check_type(
        check_type="DQ1", product_code=product_code
    )
    if check_status is True:
        try:
            product_type = product.product_type
            log_request(data=data, product_code=product_code, runId=runId)
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=True,
                runId=runId,
            )
            return validate_input_data(data)
        except ValidationError as e:
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=False,
                runId=runId,
            )
            return jsonify({"error": str(e), "details": "DQ1 failed"}), 400
    else:
        return (
            jsonify({"error": "Проверка DQ1 выключена для данного продукта."}),
            403,
        )


def dq2(data=None):
    if data is None:
        data = request.get_json()
    product = data.get("quote").get("product")
    product_code = product.get("productCode")
    product_type = product.get("productType")
    runId = data.get("quote").get("header").get("runId", None)
    if product_code is None or product_type is None:
        return (
            jsonify(
                {
                    "error": "productCode или productType не найдены. "
                    "Проверьте структуру JSON."
                }
            ),
            400,
        )
    log_request(data=data, product_code=product_code, runId=runId)
    check, check_status = validate_check_type(
        check_type="DQ2.1", product_code=product_code
    )
    # 2.1 Проверка продукта
    if check_status is True:
        product_type_exists = (
            db.session.query(Products)
            .filter(Products.product_type == product_type)
            .first()
        )
        if not product_type_exists:
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=False,
                runId=runId,
            )
            return (
                jsonify(
                    {
                        "error": "Расчет скорингового балла по данному страховому "  # noqa E501
                        "продукту не предусмотрен в системе.",
                        "description": f"productType '{product_type}'.",
                        "detals": "DQ2.1 failed",
                    }
                ),
                400,
            )

        # Проверка соответствия типа и кода продукта
        product_type_for_code = (
            db.session.query(Products)
            .filter(Products.product_code == product_code)
            .first()
            .product_type
        )
        if product_type_for_code != product_type:
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=False,
                runId=runId,
            )
            return (
                jsonify(
                    {
                        "error": "Расчет скорингового балла по данному страховому"  # noqa E501
                        "продукту не предусмотрен в системе.",
                        "descriptions": f"productType '{product_type},"
                        f"productCode: '{product_code}'.",
                        "detals": "DQ2.1 failed",
                    }
                ),
                400,
            )
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )
    else:
        return (
            jsonify(
                {"error": "Проверка DQ2.1 выключена для данного продукта."}
            ),
            400,
        )
    # 2.2 Проверка субъекта
    check, check_status = validate_check_type(
        check_type="DQ2.2", product_code=product_code
    )
    if check_status is True:
        # TODO: переделать для списка:
        birth_date = (
            data.get("quote", {}).get("subjects", {})[0].get("birthDate", None)
        )
        if birth_date is None:
            return (
                jsonify(
                    {
                        "error": "Дата рождения не указана. "
                        "Проверьте структуру JSON."
                    }
                ),
                400,
            )

        age = calculate_age(birth_date)
        if age < 18:
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=False,
                runId=runId,
            )
            return (
                jsonify(
                    {
                        "error": "Клиент не достиг совершеннолетия",
                        "detals": "DQ2.2 failed",
                    }
                ),
                400,
            )

        # 2.2 Проверка возраста субъекта (максимум 90 лет)
        if age > 90:
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=False,
                runId=runId,
            )
            return (
                jsonify(
                    {
                        "error": "Возраст клиента выше допустимого значения",
                        "detals": "DQ2.2 failed",
                    }
                ),
                400,
            )
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=False,
            runId=runId,
        )
        # 2.2 Проверка корректности пола субъекта
        gender = (
            data.get("quote", {}).get("subjects", {})[0].get("gender", None)
        )
        if gender not in ["male", "female"]:
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=False,
                runId=runId,
            )
            return (
                jsonify(
                    {
                        "error": "Выберите пол: female/male",
                        "detals": "DQ2.2 failed",
                    }
                ),
                400,
            )
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )
    else:
        return (
            jsonify(
                {"error": "Проверка DQ2.2 выключена для данного продукта."}
            ),
            400,
        )
    check, check_status = validate_check_type(
        check_type="DQ2.3", product_code=product_code
    )
    if check_status is True:
        # TODO: сделать поиск по нескольким документам
        doc_type = (
            data.get("quote", {})
            .get("subjects", {})[0]
            .get("documents", None)[0]
            .get("documentType", None)
        )
        if doc_type is None:
            return (
                jsonify(
                    {
                        "error": "Тип документа не найден. "
                        "Проверьте структуру JSON."
                    }
                ),
                400,
            )
        if doc_type not in {"passport", "driving_license"}:
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=False,
                runId=runId,
            )
            return (
                jsonify(
                    {
                        "error": "Неверный тип документа.",
                        "detals": "DQ2.3 failed",
                    }
                ),
                400,
            )
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )

    else:
        return (
            jsonify(
                {"error": "Проверка DQ2.3 выключена для данного продукта."}
            ),
            400,
        )
    return jsonify({"message": "Проверки DQ2 пройдены успешно."}), 200


@bp.route("/", methods=["GET"])
@token_required
@admin_required
def get_check_history(user):
    """
    Эндпоинт для получения списка всех проверок с возможностью фильтрации.
    """
    try:
        check_type = request.args.get("check_type")
        product_type = request.args.get("product_type")
        date = request.args.get("date")

        query = db.session.query(CheckHistory)
        if check_type:
            query = query.join(Checks).filter(Checks.type == check_type)
        if product_type:
            query = query.filter(CheckHistory.product_type == product_type)
        if date:
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(
                    CheckHistory.date.cast(db.Date) == date_obj
                )
            except ValueError:
                return (
                    jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}),
                    400,
                )
        results = query.all()

        response = [
            {
                "id": record.id,
                "runId": record.runId,
                "check_id": record.check_id,
                "product_type": record.product_type,
                "status": record.status,
                "date": record.date.isoformat(),
            }
            for record in results
        ]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:check_id>", methods=["GET", "DELETE", "PATCH"])
@token_required
@admin_required
def handle_check_dq(user, check_id):
    """
    Эндпоинт для получения, удаления записи из истории проверок
    или изменения статуса проверки.
    """
    check_exists = (
        db.session.query(CheckHistory).filter_by(id=check_id).first()
    )
    if not check_exists:
        return (
            jsonify({"error": f"Check with id {check_id} not found ."}),
            404,
        )
    if request.method == "GET":
        try:
            record = (
                db.session.query(CheckHistory).filter_by(id=check_id).first()
            )
            if not record:
                return (
                    jsonify({"error": f"Запись с id {check_id} не найдена"}),
                    404,
                )

            request_record = (
                db.session.query(Requests)
                .filter_by(runId=record.runId)
                .first()
            )
            if not request_record:
                return (
                    jsonify(
                        {"error": f"Запись с runId {record.runId} не найдена."}
                    ),
                    404,
                )

            response = {
                "id": record.id,
                "runId": record.runId,
                "check_id": record.check_id,
                "product_type": record.product_type,
                "status": record.status,
                "date": record.date.isoformat(),
                "request_json": request_record.request,
            }
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "DELETE":
        try:

            db.session.delete(check_exists)
            db.session.commit()

            return (
                jsonify({"message": f"Запись с id {check_id} удалена."}),
                204,
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    elif request.method == "PATCH":
        try:

            status = request.json.get("status")
            if not check_id or status is None:
                return jsonify({"error": "Missing required fields."}), 400

            check_exists.status = status
            db.session.commit()
            return (
                jsonify(
                    {"message": "Check product status updated successfully"}
                ),
                200,
            )

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


@bp.route("/manage", methods=["PUT"])
@token_required
@admin_required
def manage_checks(user):
    data = request.json
    check_type = data.get("check_type")
    product_type = data.get("product_type")
    condition = data.get("condition")
    if product_type not in {"osago", "life"}:
        return (
            jsonify(
                {"error": 'product_type must be in \'{"osago", "life"}\' '}
            ),
            400,
        )
    if check_type not in {"DQ1", "DQ2.1", "DQ2.2", "DQ2.3"}:
        return (
            jsonify(
                {
                    "error": 'check must be in \'{"DQ1", "DQ2.1", "DQ2.2", "DQ2.3"}\' '  # noqa E501
                }
            ),
            400,
        )
    if condition not in {True, False}:
        return (
            jsonify({"error": "condition must be True or False"}),
            400,
        )

    try:
        checks = (
            db.session.query(Checks).filter(Checks.type == check_type).all()
        )
        check_ids = [check.check_id for check in checks]
        product_code = (
            db.session.query(Products)
            .filter(Products.product_type == product_type)
            .first()
            .product_code
        )
        updated_rows = (
            db.session.query(CheckProductStatus)
            .filter(
                CheckProductStatus.check_id.in_(check_ids),
                CheckProductStatus.product_code == product_code,
            )
            .update({"condition": condition}, synchronize_session="fetch")
        )

        if updated_rows == 0:
            return (
                jsonify(
                    {"message": "No records updated. Check your filters."}
                ),
                404,
            )
        db.session.commit()
        action = "enabled" if condition else "disabled"
        return (
            jsonify(
                {"message": f"Checks type '{check_type}' have been {action}"}
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/checks", methods=["GET"])
@token_required
@admin_required
def get_models(user):
    query = """
    SELECT c.check_id as id, c.type, cp.product_code, cp.condition
    FROM "dq.checks" c
    JOIN "dq.check_product_status" cp USING(check_id)
    WHERE 1=1
    """
    try:
        result = db.session.execute(text(query)).mappings()
        rows = [dict(row) for row in result]
        db.session.commit()
        return (
            jsonify(rows),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

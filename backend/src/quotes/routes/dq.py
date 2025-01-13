from datetime import datetime

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from quotes.config import db
from quotes.models.core import Products
from quotes.models.dq import CheckHistory, CheckProductStatus, Checks, Requests
from quotes.utils import validate_input_data

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
            date=datetime.utcnow(),
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
            date=datetime.utcnow(),
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


# @bp.route("/dq1", methods=["POST"])
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
            return jsonify({"error": str(e)}), 400
    else:
        return (
            jsonify({"error": "Проверка DQ1 выключена для данного продукта."}),
            403,
        )


# @bp.route("/product", methods=["POST"])
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
    check, check_status = validate_check_type(
        check_type="DQ2", product_code=product_code
    )
    if check_status is True:
        # Проверка наличия кода продукта в таблице products
        product_exists = (
            db.session.query(Products)
            .filter(Products.product_type == product_type)
            .first()
        )
        if not product_exists:
            log_request(data=data, product_code=product_code, runId=runId)
            log_check_history(
                check_id=check.check_id,
                product_type=product_type,
                status=True,
                runId=runId,
            )
            return (
                jsonify(
                    {
                        "error": "Расчет скорингового балла по данному "
                        "страховому продукту не предусмотрен в системе.",
                        "details": f"productCode '{product_code}'.",
                    }
                ),
                400,
            )
    else:
        return (
            jsonify({"error": "Проверка DQ2 выключена для данного продукта."}),
            400,
        )

    # Проверка наличия типа продукта в таблице products
    product_type_exists = (
        db.session.query(Products)
        .filter(Products.product_type == product_type)
        .first()
    )
    if not product_type_exists:
        log_request(data=data, product_code=product_code, runId=runId)
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )
        return (
            jsonify(
                {
                    "error": "Расчет скорингового балла по данному страховому "
                    "продукту не предусмотрен в системе.",
                    "details": f"productType '{product_type}'.",
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
        log_request(data=data, product_code=product_code, runId=runId)
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )
        return (
            jsonify(
                {
                    "error": "Расчет скорингового балла по данному страховому "
                    "продукту не предусмотрен в системе.",
                    "details": f"productType '{product_type},"
                    f"productCode: '{product_code}'.",
                }
            ),
            400,
        )
    # 2.1 Проверка возраста субъекта (минимум 18 лет)
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
        log_request(data=data, product_code=product_code, runId=runId)
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )
        return jsonify({"error": "Клиент не достиг совершеннолетия"}), 400

    # 2.2 Проверка возраста субъекта (максимум 90 лет)
    if age > 90:
        log_request(data=data, product_code=product_code, runId=runId)
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )
        return (
            jsonify({"error": "Возраст клиента выше допустимого значения"}),
            400,
        )

    # 2.3 Проверка корректности пола субъекта
    gender = data.get("quote", {}).get("subjects", {})[0].get("gender", None)
    if gender not in ["male", "female"]:
        log_request(data=data, product_code=product_code, runId=runId)
        log_check_history(
            check_id=check.check_id,
            product_type=product_type,
            status=True,
            runId=runId,
        )
        return jsonify({"error": "Выберите пол: female/male"}), 400
    return jsonify({"message": "Проверка DQ2 пройдена успешно."}), 200

from datetime import datetime

from flask import Blueprint, jsonify, request

from quotes.config import db
from quotes.models.core import Products
from quotes.models.dq import CheckProductStatus, Checks
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


@bp.route("/dq1", methods=["POST"])
def dq1(data=None):
    if data is None:
        data = request.get_json()

    product_code = data.get("quote").get("product").get("productCode", None)
    if product_code is None:
        return (
            jsonify(
                {"error": "productCode не найден. Проверьте структуру JSON."}
            ),
            400,
        )
    if (
        not db.session.query(Products)
        .filter(Products.product_code == product_code)
        .first()
    ):
        return (
            jsonify(
                {"error": f"productCode '{product_code}' не существует в БД."}
            ),
            400,
        )

    check = db.session.query(Checks).filter(Checks.type == "DQ1").first()
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
        if product_check_status is True:
            try:
                return validate_input_data(data)
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        return (
            jsonify({"error": "Проверка DQ1 выключена для данного продукта."}),
            400,
        )
    else:
        return jsonify({"error": "Проверка DQ1 не найдена в БД."}), 400


@bp.route("/product", methods=["POST"])
def dq2(data=None):
    if data is None:
        data = request.get_json()
    product = data.get("quote").get("product")
    product_code = product.get("productCode")
    product_type = product.get("productType")

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

    # Проверка наличия кода продукта в таблице products
    product_exists = (
        db.session.query(Products)
        .filter(Products.product_type == product_type)
        .first()
    )
    if not product_exists:
        return (
            jsonify(
                {
                    "error": "Расчет скорингового балла по данному страховому "
                    "продукту не предусмотрен в системе.",
                    "details": f"productCode '{product_code}'.",
                }
            ),
            400,
        )

    # Проверка наличия типа продукта в таблице products
    product_type_exists = (
        db.session.query(Products)
        .filter(Products.product_type == product_type)
        .first()
    )
    if not product_type_exists:
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
        return jsonify({"error": "Клиент не достиг совершеннолетия"}), 400

    # 2.2 Проверка возраста субъекта (максимум 90 лет)
    if age > 90:
        return (
            jsonify({"error": "Возраст клиента выше допустимого значения"}),
            400,
        )

    # 2.3 Проверка корректности пола субъекта
    gender = data.get("quote", {}).get("subject", {}).get("gender", None)
    if gender not in ["male", "female"]:
        return jsonify({"error": "Выберите пол: female/male"}), 400
    return jsonify({"message": "Проверка DQ2 пройдена успешно."}), 200

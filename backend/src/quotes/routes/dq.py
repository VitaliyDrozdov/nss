from flask import Blueprint, jsonify, request

from quotes.config import db
from quotes.models.core import Products
from quotes.models.dq import CheckProductStatus, Checks
from quotes.utils import validate_input_data

bp = Blueprint("dq", __name__)


@bp.route("/dq1", methods=["POST"])
def dq1(data=None):
    if data is None:
        data = request.get_json()
    product_code = data.get("quote").get("product").get("productCode")
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
            return validate_input_data(data)
        return (
            jsonify({"error": "Проверка DQ1 выключена для данного продукта."}),
            400,
        )
    else:
        return jsonify({"error": "Проверка DQ1 не найдена в БД."}), 400


@bp.route("/product", methods=["POST"])
def dq2():
    pass
    # data = request.json
    # product = data.get("quote").get("product")
    # product_code = product.get("productCode")
    # product_type = product_code.get("productType")
    # producs_table = Table("products")

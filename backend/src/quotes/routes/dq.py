from flask import Blueprint

from quotes.utils import validate_input_data

bp = Blueprint("dq", __name__)


@bp.route("/dq1", methods=["POST"])
def dq1(data):
    # Тут какая то будет логика, проверка включена ли проверка dq1
    return validate_input_data(data)


@bp.route("/product", methods=["POST"])
def dq2():
    pass
    # data = request.json
    # product = data.get("quote").get("product")
    # product_code = product.get("productCode")
    # product_type = product_code.get("productType")
    # producs_table = Table("products")

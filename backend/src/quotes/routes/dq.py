from flask import Blueprint
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from quotes.config import Config

bp = Blueprint("dq", __name__)

DATABASE_URL = "sqlite:///dq_database.db"
engine_dq = create_engine(DATABASE_URL)
metadata_quotes = MetaData(bind=engine_dq)
Session_dq = sessionmaker(bind=engine_dq)
session_dq = Session_dq()

engine_quotes = create_engine(Config.SQLALCHEMY_DATABASE_URI)
metadata_quotes = MetaData(bind=engine_quotes)
Session_quotes = sessionmaker(bind=engine_quotes)
session_quotes = Session_quotes()


@bp.route("/dq/json", methods=["POST"])
def dq1():
    # тут по идее тоже самое, что и валидации входнящего json, которая уже есть
    pass


@bp.route("/dq/product", methods=["POST"])
def dq2():
    pass
    # data = request.json
    # product = data.get("quote").get("product")
    # product_code = product.get("productCode")
    # product_type = product_code.get("productType")
    # producs_table = Table("products")

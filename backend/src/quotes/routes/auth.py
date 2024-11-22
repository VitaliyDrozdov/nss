from flask import Blueprint, jsonify, request
from quotes.models import User

bp = Blueprint("auth", __name__)


# @bp.route("/register", methods=["POST"])
# def register():
#     data = request.get_json()
#     username = data.get("username")
#     # password = data.get("password")
#     role = data.get("role", "user")

#     if User.query.filter_by(username=username).first():
#         return jsonify({"message": "Username already exists"}), 400

#     hashed_password = ""
#     new_user = User(username=username, password=hashed_password, role=role)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({"message": "User registered"}), 201


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        token = user.generate_token()
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/protected", methods=["POST"])
def check_protected():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token is missing"}), 403

    token = token.split(" ")[1]

    user = User.query.filter_by(token=token).first()

    if user and user.check_token(token):
        return jsonify({"message": "Access granted"}), 200
    else:
        return jsonify({"error": "Invalid or expired token"}), 403

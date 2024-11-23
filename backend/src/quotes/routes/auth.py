import datetime

from flask import Blueprint, jsonify, request
from quotes.models.auth import Role, User, db
from quotes.utils import token_required
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    # email = request.json.get("email")
    if not username or not password:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "request_fields": {
                        "username": f"{username}",
                        "password": f"{password}",
                    },
                }
            ),
            400,
        )
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    user_role = Role.query.filter_by(name="userrole").first()
    if not user_role:
        user_role = Role(name="userrole")
        db.session.add(user_role)
        db.session.commit()
    new_user.roles.append(user_role)
    new_user.generate_token()
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        user.generate_token()
        db.session.commit()
        return jsonify({"access_token": user.token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/logout", methods=["POST"])
@token_required
def logout(user):
    user.token = ""
    user.token_expiry = datetime.datetime.now() - datetime.timedelta(days=2)
    db.session.commit()
    return jsonify({"message": "Logged out successfully."}), 200


@bp.route("/protected", methods=["GET"])
@token_required
def check_protected(user):
    return {"message": f"protected endpoint\n User: {user.username}"}


@bp.route("/profile", methods=["GET"])
@token_required
def profile(user):
    return jsonify({"username": user.username, "token": user.token})

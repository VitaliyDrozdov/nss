import uuid

import redis
from flask import Blueprint, jsonify, request
from users.auth import User, db

bp = Blueprint("users_routes", __name__)
redis_store = redis.Redis(host="localhost", port=6379, decode_responses=True)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    # password = data.get("password")
    role = data.get("role", "user")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = ""
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # user = User.query.filter_by(username=username).first()
    if username == "user" and password == "pass":
        token = str(uuid.uuid4())
        redis_store.set(token, "user", ex=3600)
        return jsonify({"access_token": token})
    # TODO: логика с ролями
    elif username == "admin" and password == "pass":
        token = str(uuid.uuid4())
        redis_store.set(token, "admin", ex=3600)
        return jsonify({"access_token": token})
    return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization").split(" ")[1]
    redis_store.delete(token)
    return jsonify({"message": "Logged out"})

import datetime
import os

from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from quotes.config import db, logger, mail
from quotes.models.auth import Role, User
from quotes.utils import (
    AdminProfileManager,
    UserProfileManager,
    is_admin,
    token_required,
)

bp = Blueprint("auth", __name__)
load_dotenv()


@bp.route("/register", methods=["POST"])
@token_required
def register(cur_user):
    """Регистрация новых пользователей."""
    if not is_admin(cur_user):
        return jsonify({"error": "You do not have permission"}), 403
    email = request.json.get("email")
    password = request.json.get("password")
    if not email or not password:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "request_fields": ["email", "password"],
                }
            ),
            400,
        )
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 400
    hashed_password = generate_password_hash(password)
    new_user = User(
        email=email,
        password=hashed_password,
        created_at=datetime.datetime.now(),
    )
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
    """Вход по username и password

    Returns:
        string: token
    """
    email = request.json.get("email")
    password = request.json.get("password")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user.is_blocked:
        return jsonify({"error": "Account is blocked."}), 403

    if check_password_hash(user.password, password):
        user.generate_token()
        db.session.commit()
        return jsonify({"access_token": user.token}), 200
    user.login_attempts += 1
    db.session.commit()
    if user.login_attempts >= 3:
        user.is_blocked = True
        db.session.commit()
        admin_email = os.getenv("ADMIN_EMAIL", "admin@mail.ru")
        msg = Message(
            "User Account Blockeds",
            sender="no-reply@neoscoring.com",
            recipients=[admin_email],
        )
        msg.body = (
            f"User with email {user.email} "
            "has been blocked due to multiple failed attempts."
        )
        logger.info(msg.as_string())
        mail.send(msg)
        return (
            jsonify(
                {"error": "Account blocked due to multiple failed attempts"}
            ),
            403,
        )
    return jsonify({"error": "Invalid credentials"}), 401


@bp.route("/logout", methods=["POST"])
@token_required
def logout(user):
    """Выход из текущего профиля. Токен обнуляется."""
    user.token = ""
    user.token_expiry = datetime.datetime.now() - datetime.timedelta(days=2)
    db.session.commit()
    return jsonify({"message": "Logged out successfully."}), 200


@bp.route("/profile", methods=["GET", "PATCH", "DELETE"])
@token_required
def profile(user):
    """Получение информации, обновление и удаление текущего пользователя."""
    user_manager = UserProfileManager(user, db.session)
    if request.method == "GET":
        return user_manager.get()
    elif request.method == "PATCH":
        return user_manager.update(request.json)
    elif request.method == "DELETE":
        return user_manager.delete()


@bp.route("/admin/<int:other_user_id>", methods=["GET", "PATCH", "DELETE"])
@token_required
def admin_profile(cur_user, other_user_id):
    """Эндпоинты для админов."""
    if not is_admin(cur_user):
        return jsonify({"error": "You do not have permission"}), 403

    existing_user = User.query.get_or_404(other_user_id)
    admin_manager = AdminProfileManager(existing_user, db.session)

    if request.method == "GET":
        return admin_manager.get()
    elif request.method == "PATCH":
        if is_admin(existing_user):
            return (
                jsonify({"error": "Can not change other admin's profile"}),
                403,
            )
        data = request.json
        return admin_manager.update(data)
    elif request.method == "DELETE":
        if is_admin(existing_user):
            return (
                jsonify({"error": "Can not delete other admin's profile"}),
                403,
            )
        return admin_manager.delete()


@bp.route("/reset_password", methods=["POST"])
@token_required
def reset_password(user):
    """Запрос на восстановление пароля."""
    email = request.json.get("email")
    user = User.query.filter_by(email=email).first()

    if user:
        user.generate_reset_uuid()
        user.token_expiry = datetime.datetime.now() + datetime.timedelta(
            hours=1
        )
        user.token = ""
        db.session.commit()
        # Отправка email с ссылкой для сброса пароля
        reset_url = (
            f"https://neoscoring.com/reset_password/{user.reset_password_uuid}"
        )
        msg = Message(
            "Password Reset Request",
            sender="no-reply@neoscoring.com",
            recipients=[email],
        )
        msg.body = "Для сброса пароля перейдите по ссылке: " f"{reset_url}"
        logger.info(msg.as_string())
        try:
            mail.send(msg)
        except Exception as e:
            return (
                jsonify({"error": "Failed to send email", "details": str(e)}),
                500,
            )
        return (
            jsonify({"message": "Message sent."}),
            200,
        )

    return jsonify({"error": "Email not found"}), 404


@bp.route("/reset_password/<uuid>", methods=["POST"])
def set_new_password(uuid):
    """Переход по ссылке для создания нового пароля."""
    user = User.query.filter_by(reset_password_uuid=uuid).first()
    if user and user.token_expiry > datetime.datetime.now():
        new_password = request.json.get("password")
        user.password = generate_password_hash(new_password)
        user.last_passoword_rest = datetime.datetime.now()
        user.reset_password_uuid = None
        user.token = ""
        user.token_expiry = datetime.datetime.now() - datetime.timedelta(
            days=2
        )
        db.session.commit()
        return jsonify({"message": "The password has been reset"}), 200
    return jsonify({"error": "Invalid or expired reset link."}), 400

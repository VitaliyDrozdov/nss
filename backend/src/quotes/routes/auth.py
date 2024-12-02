import datetime

from flask import Blueprint, jsonify, request
from quotes.models.auth import Role, User, db
from quotes.utils import UserProfileManager, is_admin, token_required
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    """Регистрация новых пользователей."""
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                    "request_fields": ["username", "password"],
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
    """Вход по username и password

    Returns:
        string: token
    """
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
    """Выход из текущего профиля. Токен обнуляется."""
    user.token = ""
    user.token_expiry = datetime.datetime.now() - datetime.timedelta(days=2)
    db.session.commit()
    return jsonify({"message": "Logged out successfully."}), 200


@bp.route("/protected", methods=["GET"])
@token_required
def check_protected(user):
    """Тестовый закрытый эндпоинт."""
    return {"message": f"protected endpoint\n User: {user.username}"}


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
    user_manager = UserProfileManager(existing_user, db.session)

    if request.method == "GET":
        return user_manager.get()

    elif request.method == "PATCH":
        if user_manager.is_admin():
            return (
                jsonify({"error": "Can not change other admin's profile"}),
                403,
            )
        data = request.json
        new_username = data.get("new_username")
        if User.query.filter_by(username=new_username).first():
            return jsonify({"error": "Username already exists"}), 400
        if new_username:
            existing_user.username = new_username

        roles = data.get("roles")
        if roles:
            existing_user.roles = [
                Role.query.filter_by(name=role).first() for role in roles
            ]
        user_manager.update(data)
        return jsonify({"message": f"Profile {other_user_id} updated"}), 200

    elif request.method == "DELETE":
        if user_manager.is_admin():
            return (
                jsonify({"error": "Can not delete other admin's profile"}),
                403,
            )

        # TODO    Тут почему то не работает, надо поправить
        return user_manager.delete()

import datetime

from flask import Blueprint, jsonify, request
from quotes.models.auth import Role, User, db, roles_users
from quotes.utils import is_admin, token_required
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
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


@bp.route("/profile", methods=["GET", "PATCH", "DELETE"])
@token_required
def profile(user):
    if request.method == "GET":
        return jsonify(
            {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "second_name": user.second_name,
                "created_at": (
                    user.created_at.isoformat() if user.created_at else None
                ),
                "last_login": (
                    user.last_login.isoformat() if user.last_login else None
                ),
                "roles": [role.name for role in user.roles],
            }
        )
    elif request.method == "PATCH":
        fields = {"password", "email", "first_name", "second_name"}
        data = request.json
        if not data:
            return jsonify({"error": "No data"}), 400

        # existing_user = User.query.filter_by(username=user.username).first()
        # if existing_user.id != user.id:
        #     return (
        #         jsonify({"error": "Can not change other profile"}),
        #         403,
        #     )
        for k, v in data.items():
            if k in fields and hasattr(user, k):
                if k == "password":
                    v = generate_password_hash(v)
                setattr(user, k, v)

        db.session.commit()
        return jsonify({"message": "Profile updated"}), 200
    elif request.method == "DELETE":
        try:
            # user.roles.clear()
            # for role in user.roles[:]:
            #     user.roles.remove(role)
            db.session.execute(
                roles_users.delete().where(roles_users.c.user_id == user.id)
            )
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "user deleted"}), 204
        except Exception as e:
            db.session.rollback()
            return (
                jsonify(
                    {"error": "Failed to delete profile", "details": str(e)}
                ),
                500,
            )


@bp.route("/admin/<int:other_user_id>", methods=["GET", "PATCH", "DELETE"])
@token_required
def admin_profile(cur_user, other_user_id):

    if not is_admin(cur_user):
        return jsonify({"error": "You do not have permission"}), 403
    existing_user = User.query.get_or_404(other_user_id)
    if request.method == "GET":
        return jsonify(
            {
                "username": existing_user.username,
                "email": existing_user.email,
                "first_name": existing_user.first_name,
                "second_name": existing_user.second_name,
                "created_at": (
                    existing_user.created_at.isoformat()
                    if existing_user.created_at
                    else None
                ),
                "last_login": (
                    existing_user.last_login.isoformat()
                    if existing_user.last_login
                    else None
                ),
                "roles": [role.name for role in existing_user.roles],
            }
        )

    elif request.method == "PATCH":
        if is_admin(existing_user):
            return (
                jsonify({"error": "Can not change other admin's profile"}),
                403,
            )

        data = request.json
        fields = {
            "password",
            "email",
            "first_name",
            "second_name",
        }
        if not data:
            return jsonify({"error": "No data"}), 400

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

        # Протестить
        # new_password = data.get("password")
        # if new_password:
        #     existing_user.password = generate_password_hash(new_password)

        for k, v in data.items():
            if k in fields and hasattr(existing_user, k):
                if k == "password":
                    v = generate_password_hash(v)
                setattr(existing_user, k, v)

        db.session.commit()
        return jsonify({"message": f"Profile {other_user_id} updated"}), 200

    elif request.method == "DELETE":
        if is_admin(existing_user):
            return (
                jsonify({"error": "Can not delete other admin's profile"}),
                403,
            )

        try:
            # TODO    Тут почему то не работает, надо поправить
            db.session.execute(
                roles_users.delete().where(
                    roles_users.c.user_id == other_user_id
                )
            )
            db.session.delete(existing_user)
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": (
                            f"User id{other_user_id}, "
                            f"username {existing_user.username} deleted"
                        )
                    }
                ),
                204,
            )
        except Exception as e:
            db.session.rollback()
            return (
                jsonify(
                    {"error": "Failed to delete profile", "details": str(e)}
                ),
                500,
            )

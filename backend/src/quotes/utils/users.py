import datetime
import os

from dotenv import load_dotenv
from flask import jsonify
from werkzeug.security import generate_password_hash

from quotes.models.auth import Role, User, db

load_dotenv()


def create_admin():
    """Скрипт создания админа после запуска приложения."""

    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.session().add(admin_role)
        db.session.commit()
        return "Admin user already exists"

    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_user = User.query.filter_by(email=os.getenv("ADMIN_EMAIL")).first()
    if not admin_user:
        hashed_password = generate_password_hash(admin_password)
        admin_user = User(
            email=os.getenv("ADMIN_EMAIL"), password=hashed_password
        )
        admin_user.roles.append(admin_role)
        admin_user.generate_token()
        db.session.add(admin_user)
        db.session.commit()
        return "Admin user created with default values"


class BaseProfileManager:
    def __init__(self, user, db_session):
        self.user = user
        self.db_session = db_session

    def get_fields(self):
        return {
            "username",
            "email",
            "first_name",
            "second_name",
            "created_at",
            "last_login",
            "password",
        }

    def get(self):
        accessible_fields = self.get_fields()
        data = {
            field: getattr(self.user, field, None)
            for field in accessible_fields
        }

        if "last_login" in accessible_fields:
            data["last_login"] = self.user.last_login.isoformat()
        if "roles" in accessible_fields:
            data["roles"] = [role.name for role in self.user.roles]

        return jsonify(data)

    def update(self, data):
        fields = self.get_fields()
        if not data or not any(key in fields for key in data):
            return jsonify({"error": "No valid fields to update"}), 400

        for k, v in data.items():
            if k in fields:
                if k == "password":
                    v = generate_password_hash(v)
                    self.user.last_password_reset = datetime.datetime.now()
                setattr(self.user, k, v)
        self.db_session.commit()
        return jsonify({"message": "Profile updated"}), 200

    def delete(self):
        try:
            self.db_session.delete(self.user)
            self.db_session.commit()
            return jsonify({"message": f"User {self.user.email} deleted"}), 204
        except Exception as e:
            self.db_session.rollback()
            return (
                jsonify(
                    {"error": "Failed to delete profile", "details": str(e)}
                ),
                500,
            )


class UserProfileManager(BaseProfileManager):
    def get_fields(self):
        return super().get_fields()


class AdminProfileManager(BaseProfileManager):

    def __init__(self, user, db_session):
        super().__init__(user, db_session)
        # self.current_user = current_user

    def get_fields(self):
        fields = super().get_fields()
        fields.update(
            {"login_attempts", "is_blocked", "last_password_reset", "roles"}
        )
        return fields

    def update(self, data):
        if not data:
            return jsonify({"error": "No valid fields to update"}), 400
        roles = data.get("roles")
        if roles:
            roles_objects = [
                Role.query.filter_by(name=role).first() for role in roles
            ]
            missing_roles = [
                role for role, obj in zip(roles, roles_objects) if obj is None
            ]
            if missing_roles:
                return (
                    jsonify(
                        {
                            "error": (
                                "Roles not found: "
                                f"{', '.join(missing_roles)}"
                            )
                        }
                    ),
                    400,
                )
            data.pop("roles")
        is_blocked = data.get("is_blocked")
        if is_blocked is not None:
            self.user.is_blocked = is_blocked
            if not is_blocked:
                self.user.login_attempts = 0
            data.pop("is_blocked")
        if not any(key in self.get_fields() for key in data):
            self.db_session.commit()
            return jsonify({"message": "Profile updated"}), 200
        return super().update(data)


def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

from flask import jsonify
from quotes.models.auth import Role, User, db, roles_users
from werkzeug.security import generate_password_hash


def create_admin():
    """Скрипт создания админа после запуска приложения."""

    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.session().add(admin_role)
        db.session.commit()
        return "Admin user already exists"

    admin_password = "admin"
    admin_user = User.query.filter_by(email="admin@email.ru").first()
    if not admin_user:
        hashed_password = generate_password_hash(admin_password)
        admin_user = User(email="admin@mail.ru", password=hashed_password)
        admin_user.roles.append(admin_role)
        admin_user.generate_token()
        db.session.add(admin_user)
        db.session.commit()
        return "Admin user created with default values"


class UserProfileManager:
    """Менеджер для энпоинтов пользователей."""

    def __init__(self, user, db_session) -> None:
        self.user = user
        self.db_session = db_session

    def get(self):
        return jsonify(
            {
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "second_name": self.user.second_name,
                "created_at": (
                    self.user.created_at.isoformat()
                    if self.user.created_at
                    else None
                ),
                "last_login": (
                    self.user.last_login.isoformat()
                    if self.user.last_login
                    else None
                ),
                "roles": [role.name for role in self.user.roles],
            }
        )

    def update(self, data):
        fields = {
            "password",
            "email",
            "first_name",
            "second_name",
        }
        if not data or not any([val in fields for val in data]):
            return jsonify({"error": "No data"}), 400

        for k, v in data.items():
            if k in fields and hasattr(self.user, k):
                if k == "password":
                    v = generate_password_hash(v)
                setattr(self.user, k, v)

        self.db_session.commit()
        return jsonify({"message": "Profile updated"}), 200

    def delete(self):
        try:

            self.db_session.execute(
                roles_users.delete().where(
                    roles_users.c.user_id == self.user.id
                )
            )
            db.session.delete(self.user)
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": (
                            f"User id{self.user.id}, "
                            f"self.username {self.user.username} deleted"
                        )
                    }
                ),
                204,
            )
        except Exception as e:
            self.db_session.rollback()
            return (
                jsonify(
                    {"error": "Failed to delete profile", "details": str(e)}
                ),
                500,
            )

    def is_admin(self):
        return any(role.name == "admin" for role in self.user.roles)


def is_admin(user):
    return any(role.name == "admin" for role in user.roles)


# class BaseCLICommand:
#     def __init__(self, app):
#         self.app = app

#     def register(self):
#         raise NotImplementedError()


# class GenerateUsers(BaseCLICommand):
#     def register(self):
#         @self.app.cli.command("create_users")
#         def create_users():
#             roles = ("admin", "userrole")
#             data = {
#                 "admin1": {
#                     "username": "admin1",
#                     "email": "admin1@example.com",
#                     "password": "admin1_password",
#                     "role": roles[0],
#                 },
#                 "user1": {
#                     "username": "user1",
#                     "email": "user1@example.com",
#                     "password": "user1_password",
#                     "role": roles[1],
#                 },
#                 "user2": {
#                     "username": "admin1",
#                     "email": "admin1@example.com",
#                     "password": "admin1_password",
#                     "role": roles[1],
#                 },
#             }

#         with self.app.app_context():
#             db.create_all()

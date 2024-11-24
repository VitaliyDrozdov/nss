from functools import wraps

from flask import jsonify, request
from quotes.models.auth import Role, User, db
from quotes.models.quotes import QuoteData
from werkzeug.security import generate_password_hash


def validate_input_data(data):
    """
    Валидирует данные по QuoteData модели Pydantic.

    Args:
        data (dict): Входящий json.

    Returns:
        QuoteData: завалидированный json как экземпляр QuoteData.
        tuple: в случае ошибки JSON response и HTTP status code.
    """
    validated_data = QuoteData(**data)
    return validated_data


def token_required(f):
    @wraps(f)
    def decorated_f(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        if token.startswith("Bearer"):
            token = token.split(" ")[1]
        else:
            return jsonify({"error": "Reqires 'Bearer' in request "}), 400
        user = User.query.filter_by(token=token).first()
        if not user or not user.check_token(token):
            return jsonify({"error": "Invalid or expired token"}), 401
        return f(user, *args, **kwargs)

    return decorated_f


def create_admin():
    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.session().add(admin_role)
        db.session.commit()
        return "Admin user already exists"

    admin_password = "admin"
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        hashed_password = generate_password_hash(admin_password)
        admin_user = User(username="admin", password=hashed_password)
        admin_user.roles.append(admin_role)
        admin_user.generate_token()
        db.session.add(admin_user)
        db.session.commit()
        return "Admin user created with default values"


def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

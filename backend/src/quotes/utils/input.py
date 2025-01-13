from functools import wraps

from flask import jsonify, request

from quotes.models.auth import User
from quotes.models.quotes import QuoteData


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
    """Декоратор для доступа только залогиненного пользователя."""

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
        print(f"User found: {user.email}")
        return f(user, *args, **kwargs)

    return decorated_f

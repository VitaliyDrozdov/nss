import uuid
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


roles_users = db.Table(
    "roles_users",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id", ondelete="CASCADE")
    ),
    db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id", ondelete="CASCADE")
    ),
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship(
        "User",
        secondary=roles_users,
        backref=db.backref("user_roles", lazy="dynamic"),
    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    token_expiry = db.Column(db.DateTime, nullable=False)
    roles = db.relationship("Role", secondary=roles_users)
    email = db.Column(db.String(50), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    second_name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime)

    def generate_token(self, expiration=3600):
        token = str(uuid.uuid4())
        self.token = token
        self.token_expiry = datetime.now() + timedelta(seconds=expiration)
        return token

    def check_token(self, token):
        if (
            token
            and self.token == token
            and self.token_expiry > datetime.now()
        ):
            return True
        return False

# import uuid
# from datetime import datetime, timedelta
# from typing import List, Literal, Optional

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # token = db.Column(db.String(100), unique=True, nullable=False)
    # token_expiry = db.Column(db.DateTime, nullable=False)
    # role = db.Column(db.String(50), default="user")
    def get_id(self):
        return str(self.id)

    # def generate_token(self, expiration=3600):
    #     token = str(uuid.uuid4())
    #     self.token = token
    #     self.token_expiry = datetime.now() + timedelta(seconds=expiration)
    #     db.session.commit()
    #     return token

    # def check_token(self, token):
    #     if self.token == token and self.token_expiry > datetime.now():
    #         return True
    #     return False

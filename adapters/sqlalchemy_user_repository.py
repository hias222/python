from flask_sqlalchemy import SQLAlchemy
from domain.user import User
import uuid

db = SQLAlchemy()

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class UserRepository:
    def add_user(self, username, email):
        user = UserModel(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return User(user.id, user.username, user.email, user.guid)

    def get_user(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            return User(user.id, user.username, user.email)
        return None

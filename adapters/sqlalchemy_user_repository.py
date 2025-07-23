from flask_sqlalchemy import SQLAlchemy
from domain.user import User
import uuid
import datetime

db = SQLAlchemy()

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.utcnow(), onupdate=lambda: datetime.datetime.utcnow())

class UserRepository:
    def add_user(self, username, email):
        user = UserModel(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return self._to_domain_user(user)

    def get_user(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            return self._to_domain_user(user)
        return None

    def get_all_users(self):
        users = UserModel.query.all()
        return [self._to_domain_user(u) for u in users]
    
    def delete_user_by_username(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def get_user_by_username(self, username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return self._to_domain_user(user)
        return None
    
    def _to_domain_user(self, user_model):
        return User(
            user_model.id,
            user_model.username,
            user_model.email,
            user_model.guid,
            user_model.created_at,
            user_model.updated_at
        )

from . import db
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    def __repr__(self):
        return f"User('{self.email}', '{self.password}')"

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        
        if not email or not password:
          print('Email or password not provided')
          return None

        user = cls.query.filter_by(email=email).first()
        if not user: #or not check_password_hash(user.password, password):
          print('User credentials are incorrect')
          return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from directory import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(128), unique=False, nullable=False)

    @validates('password')
    def validate_password(self, key, value):
        if value is None:
            raise ValueError('Password can\'t be null')
        if len(value) < 6:
            raise ValueError('Password should be atleast 6 characters.')
        return generate_password_hash(value)

    @validates('username')
    def validate_username(self, key, value):
        if value is None:
            raise ValueError('Username can\'t be null')
        if not value.isidentifier():
            raise ValueError('Username is invalid.')
        return value

    def check_password(self, password):
        return check_password_hash(self.password, password)
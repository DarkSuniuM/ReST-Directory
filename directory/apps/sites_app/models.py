import re
import datetime as dt
from sqlalchemy import Column, Integer, DateTime, String, Text
from sqlalchemy.orm import validates
from directory import db


class Site(db.Model):
    __tablename__ = 'sites'

    id = Column(Integer(), primary_key=True)
    create_date = Column(DateTime(), nullable=False, unique=False, default=dt.datetime.utcnow)
    name = Column(String(128), nullable=False, unique=False)
    description = Column(Text(), nullable=True, unique=False)
    address = Column(String(128), nullable=False, unique=True)
    icon = Column(String(256), nullable=True, unique=False)

    @validates('name')
    def validate_name(self, key, value):
        if value is None:
            raise ValueError('Name can\'t be null')
        if len(value) > 128:
            raise ValueError('Name cant be longer than 128 characters.')
        return value

    @validates('address')
    def validate_address(self, key, value):
        if value is None:
            raise ValueError('Address can\'t be null')
        pattern = re.compile(r'^(http|https):\/\/[a-zA-Z0-9][a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,}$')
        if not pattern.match(value):
            raise ValueError('Address is not valid')
        if len(value) > 128:
            raise ValueError('Address cant be longer than 128 characters.')
        return value

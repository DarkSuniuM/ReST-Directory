from flask import request, abort
from sqlalchemy.exc import IntegrityError
from directory import db
from . import users
from .models import User


@users.route('/', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'JSON Only!'}, 400
    
    args = request.get_json()

    try:
        new_user = User()
        new_user.username = args.get('username')
        new_user.password = args.get('password')
        db.session.add(new_user)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {'error': f'{e}'}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Username is duplicated.'}, 400

    return {'message': 'Account created successfully'}, 201

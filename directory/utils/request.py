from flask import request
from functools import wraps


def json_only(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if not request.is_json:
            return {'error': 'JSON Only!'}, 400
        return function(*args, **kwargs)
    return decorator
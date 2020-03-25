"""ICO service utility functions"""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from constants import UNAUTHORIZED


def with_identity(api_method):
    """create JWT identity object for request"""

    @wraps(api_method)
    def with_identity_func(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity:
            return jsonify({'msg': 'Please provider a jwt token'}), UNAUTHORIZED

        kwargs["identity"] = identity
        result = api_method(*args, **kwargs)
        return result

    return with_identity_func

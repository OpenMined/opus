import os
from functools import wraps

from authlib.integrations.flask_oauth2 import current_token
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import create_access_token, create_refresh_token
from app.utils.spec import docs_path

from app.constants import BAD_REQUEST, UNAUTHORIZED, SUCCESS
from app.models import Users

BASE_URL = '/users'
USERS_LOGIN = {'rule': '/login', 'methods': ['POST'], 'endpoint': 'login'}
USERS_REGISTER = {'rule': '/register', 'methods': ['POST'], 'endpoint': 'register'}
USERS_PROFILE = {'rule': '/profile', 'methods': ['GET'], 'endpoint': 'profile'}

users = Blueprint(name='users', import_name=__name__, url_prefix=BASE_URL)


@users.route(**USERS_REGISTER)
@swag_from(
    docs_path('api', 'users', 'users_register.yaml'), methods=['POST'], endpoint='users.register'
)
def users_register():
    request_data = request.get_json()
    user = Users.query.filter_by(**request_data).first()
    if user:
        return jsonify(user.brief), SUCCESS
    user = Users.create(**request_data)
    return jsonify(user.brief), SUCCESS


@users.route(**USERS_LOGIN)
@swag_from(
    docs_path('api', 'users', 'users_login.yaml'), methods=['POST'], endpoint='users.login'
)
def users_login():
    request_data = request.get_json()
    user = Users.query.filter_by(email=request_data['email']).first()
    if user is None:
        return jsonify({"msg": "User not found"}), BAD_REQUEST
    elif not user.password_correct(request_data['password']):
        return jsonify({"msg": "Password and username don't match"}), UNAUTHORIZED

    return jsonify({
        'access_token': create_access_token(identity=request_data['email']),
        'refresh_token': create_refresh_token(identity=request_data['email'])
    }), SUCCESS


def require_oauth(scope):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return current_app.extensions['require_oauth'](scope)(f)(*args, **kwargs)

        return decorated

    return wrapper


@users.route(**USERS_PROFILE)
@swag_from(docs_path('api', 'users', 'users_profile.yaml'), methods=['GET'], endpoint='users.profile')
@require_oauth('profile')
def api_me():
    user = current_token.users
    return jsonify(id=user.id, username=user.username), SUCCESS

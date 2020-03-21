import os
from functools import wraps

from authlib.integrations.flask_oauth2 import current_token
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, current_app

BASE_URL = '/users'
USER_LIST_VIEW = {'rule': '', 'methods': ['GET'], 'endpoint': 'list'}
USER_VIEW = {'rule': '/<id>', 'methods': ['GET'], 'endpoint': 'get'}
USER_PROFILE = {'rule': '/profile', 'methods': ['GET'], 'endpoint': 'profile'}

users = Blueprint(name='users', import_name=__name__, url_prefix=BASE_URL)

docs_path = lambda *args: os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', *args))


def require_oauth(scope):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return current_app.extensions['require_oauth'](scope)(f)(*args, **kwargs)

        return decorated

    return wrapper


@users.route(**USER_PROFILE)
@swag_from(docs_path('api', 'users', 'users_profile.yaml'), methods=['GET'], endpoint='users.profile')
@require_oauth('profile')
def api_me():
    user = current_token.users
    return jsonify(id=user.id, username=user.username)

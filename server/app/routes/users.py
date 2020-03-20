import os

from app.models import Users
from app.services.oauth2 import require_oauth
from authlib.integrations.flask_oauth2 import current_token
from flasgger.utils import swag_from
from flask import Blueprint, jsonify

BASE_URL = '/users'
USER_LIST_VIEW = {'rule': '', 'methods': ['GET'], 'endpoint': 'list'}
USER_VIEW = {'rule': '/<id>', 'methods': ['GET'], 'endpoint': 'get'}
USER_PROFILE = {'rule': '/profile', 'methods': ['GET'], 'endpoint': 'profile'}

users = Blueprint(name='users', import_name=__name__, url_prefix=BASE_URL)

docs_path = lambda *args: os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', *args))


@users.route(**USER_LIST_VIEW)
@swag_from(docs_path('api', 'users', 'users_list.yaml'), methods=['GET'], endpoint='users.list')
def users_list():
    """
    Get list of Users
    """
    result = Users.query.all()
    return jsonify(result)


@users.route(**USER_VIEW)
@swag_from(docs_path('api', 'users', 'users_with_id_get.yaml'), methods=['GET'], endpoint='users.get')
def users_get(id):
    """
    Get user by id
    """
    result = Users.query.filter_by(id=id).first()
    return jsonify(result)


@users.route(**USER_PROFILE)
@swag_from(docs_path('api', 'users', 'users_with_id_get.yaml'), methods=['GET'], endpoint='users.profile')
@require_oauth('profile')
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)

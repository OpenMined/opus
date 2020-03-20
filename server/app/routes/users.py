import os
from flask import Blueprint, jsonify
from app.models import User
from flasgger.utils import swag_from

BASE_URL = '/users'
USER_LIST_VIEW = {'rule': '', 'methods': ['GET'], 'endpoint': 'list'}
USER_VIEW = {'rule': '/<id>', 'methods': ['GET'], 'endpoint': 'get'}

users = Blueprint(name='users', import_name=__name__, url_prefix=BASE_URL)

docs_path = lambda *args: os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', *args))


@users.route(**USER_LIST_VIEW)
@swag_from(docs_path('api', 'users', 'users_list.yaml'), methods=['GET'], endpoint='users.list')
def users_list():
    """
    Get list of Users
    TO DO: This will need to be a paginated API to handle massive amounts of users.
    """
    result = User.query.all()
    return jsonify(result)

@users.route(**USER_VIEW)
@swag_from(docs_path('api', 'users', 'users_with_id_get.yaml'), methods=['GET'], endpoint='users.get')
def users_get(id):
    """
    Get user by id
    """
    return jsonify(User.query.get_or_404(id).to_dict())
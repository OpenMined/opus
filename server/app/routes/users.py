from functools import wraps
import requests

from authlib.integrations.flask_oauth2 import current_token
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, current_app, request

from app.constants import SUCCESS, Extensions
from app.errors.messages import error_response, INCORRECT_PASSWORD, USER_NOT_FOUND_MSG, INVALID_CREDENTIAL_MSG
from app.models import Users
from app.utils.permissions import encode_refresh_token, encode_access_token
from app.utils.spec import docs_path

# Connecting to the SSI container.
SSI_ENDPOINT = 'http://ssi:3002'

BASE_URL = '/users'
USERS_LOGIN = {'rule': '/login', 'methods': ['POST'], 'endpoint': 'login'}
USERS_QR_LOGIN = {'rule': '/qr_login', 'methods': ['GET'], 'endpoint': 'qr_login'}
USERS_REGISTER = {'rule': '/register', 'methods': ['POST'], 'endpoint': 'register'}
USERS_PROFILE = {'rule': '/profile', 'methods': ['GET'], 'endpoint': 'profile'}

users = Blueprint(name='users', import_name=__name__, url_prefix=BASE_URL)

@users.route(**USERS_REGISTER)
@swag_from(
    docs_path('api', 'users', 'users_register.yaml'), methods=['POST'], endpoint='users.register'
)
def users_register():
    request_data = request.get_json()
    email = request_data['email']
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify(user.brief), SUCCESS

    password = request_data['password']
    if not password or password != request_data['passwordMatch']:
        return error_response(INCORRECT_PASSWORD)

    # At this point we call out to the SSI backend and send a POST request. 
    # POST request is going to contain the request data so that can be used to create the VC
    r = requests.post(SSI_ENDPOINT + '/users/register', json={'email': email, 'password': password})
    print(r.json())

    # Make sure we create the user in the db
    # NOTE: Password should be hashed.
    user = Users.create(email=email, password=password, username=email.split('@')[0])
    return jsonify(r.json()), SUCCESS


@users.route(**USERS_LOGIN)
@swag_from(
    docs_path('api', 'users', 'users_login.yaml'), methods=['POST'], endpoint='users.login'
)
def users_login():
    request_data = request.get_json()
    user = Users.query.filter_by(email=request_data['email']).first()
    if user is None:
        return error_response(USER_NOT_FOUND_MSG)
    elif not user.password_correct(request_data['password']):
        return error_response(INVALID_CREDENTIAL_MSG)

    return jsonify({
        'access_token': encode_access_token(request_data['email']),
        'refresh_token': encode_refresh_token(request_data['email'])
    }), SUCCESS


@users.route(**USERS_QR_LOGIN)
@swag_from(
    docs_path('api', 'users', 'users_qr_login.yaml'), methods=['GET'], endpoint='users.qr_login'
)
def users_qr_login():
    r = requests.get(SSI_ENDPOINT + '/users/qr_login')
    print(r.json())
    return jsonify(r.json()), SUCCESS
    

def require_oauth(scope):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return current_app.extensions[Extensions.REQUIRE_OAUTH](scope)(f)(*args, **kwargs)

        return decorated

    return wrapper


@users.route(**USERS_PROFILE)
@swag_from(docs_path('api', 'users', 'users_profile.yaml'), methods=['GET'], endpoint='users.profile')
@require_oauth('profile')
def api_me():
    user = current_token.users
    return jsonify(id=user.id, username=user.username), SUCCESS

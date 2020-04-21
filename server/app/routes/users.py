from functools import wraps
import requests

from authlib.integrations.flask_oauth2 import current_token
from flasgger.utils import swag_from
from flask import Blueprint, jsonify, current_app, request

from app.constants import SUCCESS, Extensions
from app.errors.messages import error_response, INCORRECT_PASSWORD, USER_NOT_FOUND_MSG, INVALID_CREDENTIAL_MSG, ALREADY_REGISTERED, BAD_VERIFICATION_MSG
from app.models import Users
from app.utils.permissions import encode_refresh_token, encode_access_token
from app.utils.spec import docs_path

SSI_ENDPOINT = 'http://ssi:3002'
STREETCRED_ENDPOINT = 'https://api.streetcred.id/agency/v1'
# NOTE: USE python-dotenv to extract these from the SSI .env file.
STREETCRED_AUTH_HEADERS = {'Authorization': 'Bearer GlW22ny3vQDdFaxxSP6Ym8WoxN9vr71RfPYZRvIADV8',
                           'X-Streetcred-Subscription-Key': 'acd24c30ed3c4ad3b8ce004f802ce459'}

BASE_URL = '/users'
USERS_LOGIN = {'rule': '/login', 'methods': ['POST'], 'endpoint': 'login'}
USERS_QR_LOGIN = {'rule': '/qr_login', 'methods': ['GET', 'POST'], 'endpoint': 'qr_login'}
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
        # NOTE: There needs to be some more logic here. TO prevent users from seeing a broken QR code.
        return error_response(ALREADY_REGISTERED)

    password = request_data['password']
    if not password or password != request_data['passwordMatch']:
        return error_response(INCORRECT_PASSWORD)

    # At this point we call out to the SSI backend and send a POST request. 
    # POST request is going to contain the request data so that can be used to create the VC
    r = requests.post(SSI_ENDPOINT + '/users/register', json={'email': email, 'password': password})

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
    docs_path('api', 'users', 'users_qr_login.yaml'), methods=['GET', 'POST'], endpoint='users.qr_login'
)
def users_qr_login():
    if request.method == 'POST':
        request_data = request.get_json()
        verification_id = request_data['verification_id']

        # Need to ensure that the object ID provided has been successfully verified 
        # and isn't a junk string, so we POST it to the Streetcred endpoint.
        r = requests.post(SSI_ENDPOINT + '/users/login_verifications', json={'verification_id': verification_id})
        verification = r.json()

        if (verification['state'] == 'Accepted') and (verification['isValid'] == True):
            email = verification['proof']['email']['value']
            
            user = Users.query.filter_by(email=email).first()
            if user is None:
                return error_response(USER_NOT_FOUND_MSG)
            
            return jsonify({
                'access_token': encode_access_token(email),
                'refresh_token': encode_refresh_token(email)
            }), SUCCESS
        else:
            # NOTE: Change this to provide the front end with information that the state is still requested.
            # This shouldn't be an error code!
            return error_response(BAD_VERIFICATION_MSG)
    else:    
        r = requests.get(SSI_ENDPOINT + '/users/qr_login')
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

import os

from app.models import Users
from authlib.oauth2 import OAuth2Error
from flasgger.utils import swag_from
from flask import Blueprint, request, session, current_app, jsonify, render_template

BASE_URL = '/oauth'
OAUTH_AUTHORIZE = {'rule': '/authorize', 'methods': ['POST', 'GET'], 'endpoint': 'authorize'}
OAUTH_TOKEN = {'rule': '/token', 'methods': ['POST'], 'endpoint': 'token'}
OAUTH_REVOKE = {'rule': '/revoke', 'methods': ['POST'], 'endpoint': 'revoke'}

oauth = Blueprint(name='oauth', import_name=__name__, url_prefix=BASE_URL)

docs_path = lambda *args: os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', *args))


def current_user():
    if 'id' in session:
        uid = session['id']
        return Users.query.get(uid)
    return None


@oauth.route(**OAUTH_AUTHORIZE)
@swag_from(docs_path('api', 'oauth', 'oauth_authorize.yaml'), methods=['POST', 'GET'], endpoint='oauth.authorize')
def oauth_authorize():
    user = current_user()
    if request.method == 'GET':
        try:
            grant = current_app.extensions['authorization'].validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return jsonify(dict(error.get_body()))
        return render_template('authorize.html', user=user, grant=grant)
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = Users.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return current_app.extensions['authorization'].create_authorization_response(grant_user=grant_user)


@oauth.route(**OAUTH_TOKEN)
@swag_from(docs_path('api', 'oauth', 'oauth_token.yaml'), methods=['POST'], endpoint='oauth.token')
def oauth_token():
    return current_app.extensions['authorization'].create_token_response()


@oauth.route(**OAUTH_REVOKE)
@swag_from(docs_path('api', 'oauth', 'oauth_revoke.yaml'), methods=['GET'], endpoint='oauth.revoke')
def oauth_revoke():
    return current_app.extensions['authorization'].create_endpoint_response('revocation')

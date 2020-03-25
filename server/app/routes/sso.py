import datetime

from app.constants import SUCCESS
from app.models import Users, OAuth2Token
from app.utils.permissions import with_identity
from app.utils.spec import docs_path
from flasgger.utils import swag_from
from flask import Blueprint, current_app, redirect, jsonify

from constants import BAD_REQUEST

BASE_URL = '/sso'
SSO_PROVIDERS = {'rule': '/providers', 'methods': ['GET'], 'endpoint': 'providers'}
SSO_GITHUB = {'rule': '/github', 'methods': ['GET'], 'endpoint': 'github'}
SSO_GITHUB_AUTHORIZE = {'rule': '/github/authorize', 'methods': ['GET'], 'endpoint': 'authorize_github'}

sso = Blueprint(name='sso', import_name=__name__, url_prefix=BASE_URL)


@sso.route(**SSO_PROVIDERS)
@swag_from(docs_path('api', 'sso', 'sso_providers.yaml'), methods=['GET'], endpoint='sso.providers')
@with_identity
def sso_providers(identity):
    print(identity)
    tokens = OAuth2Token.query.filter_by(users=Users.query.filfer_by(email=identity['email']))
    return jsonify({tokens}), SUCCESS


@sso.route(**SSO_GITHUB)
@swag_from(docs_path('api', 'sso', 'sso_github.yaml'), methods=['GET'], endpoint='sso.github')
def sso_github():
    oauth = current_app.extensions['authlib.integrations.flask_client']
    github = oauth.create_client('github')
    redirect_uri = f"{current_app.config['JWT_DECODE_ISSUER']}/sso/github/authorize"
    return github.authorize_redirect(redirect_uri=redirect_uri)


@sso.route(**SSO_GITHUB_AUTHORIZE)
@swag_from(docs_path('api', 'sso', 'sso_github_authorize.yaml'), methods=['GET'], endpoint='sso.github_authorize')
def sso_github_authorize():
    oauth = current_app.extensions['authlib.integrations.flask_client']
    github = oauth.create_client('github')
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user')
    profile = resp.json()
    user = Users.query.filter_by(email=profile['email']).first()
    if not user:
        return redirect(current_app.config['FRONTEND_HOST'], BAD_REQUEST, jsonify({"msg": "User not found"}))

    OAuth2Token.create(
        client_id=github.client_id,
        provider='github',
        token_type=token['token_type'],
        access_token=token['access_token'],
        scope=token['scope'],
        issued_at=datetime.datetime.now().timestamp(),
        user_id=user.id
    )
    return redirect(current_app.config['FRONTEND_HOST']), SUCCESS

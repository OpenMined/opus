import datetime

from flasgger.utils import swag_from
from flask import Blueprint, current_app, redirect, jsonify
from sqlalchemy import and_
from app.constants import BAD_REQUEST
from app.constants import SUCCESS, Extensions
from app.models import Users, OAuth2Token
from app.utils.permissions import with_identity
from app.utils.spec import docs_path

BASE_URL = '/sso'
SSO_PROVIDERS = {'rule': '/providers', 'methods': ['GET'], 'endpoint': 'providers'}
SSO_GITHUB = {'rule': '/github', 'methods': ['GET'], 'endpoint': 'github'}
SSO_GITHUB_AUTHORIZE = {'rule': '/github/authorize', 'methods': ['GET'], 'endpoint': 'github_authorize'}
SSO_GITHUB_REVOKE = {'rule': '/github/revoke', 'methods': ['POST'], 'endpoint': 'github_revoke'}

sso = Blueprint(name='sso', import_name=__name__, url_prefix=BASE_URL)


@sso.route(**SSO_PROVIDERS)
@swag_from(docs_path('api', 'sso', 'sso_providers.yaml'), methods=['GET'], endpoint='sso.providers')
@with_identity
def sso_providers(identity):
    tokens = OAuth2Token.query \
        .join(Users, Users.id == OAuth2Token.user_id) \
        .filter(Users.email == identity).all()
    result = []
    if tokens:
        result = [token.provider for token in tokens]
    return jsonify(result), SUCCESS


@sso.route(**SSO_GITHUB)
@swag_from(docs_path('api', 'sso', 'sso_github.yaml'), methods=['GET'], endpoint='sso.github')
def sso_github():
    oauth = current_app.extensions[Extensions.AUTHLIB_FLASK_CLIENT.value]
    return oauth.github.authorize_redirect(
        redirect_uri=f"{current_app.config['JWT_DECODE_ISSUER']}/sso/github/authorize"
    )


@sso.route(**SSO_GITHUB_AUTHORIZE)
@swag_from(docs_path('api', 'sso', 'sso_github_authorize.yaml'), methods=['GET'], endpoint='sso.github_authorize')
def sso_github_authorize():
    oauth = current_app.extensions[Extensions.AUTHLIB_FLASK_CLIENT.value]
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user')
    profile = resp.json()
    user = Users.query.filter_by(email=profile['email']).first()
    if not user:
        return redirect(current_app.config['FRONTEND_HOST'], BAD_REQUEST, jsonify({"message": "User not found"}))

    OAuth2Token.create(
        client_id=oauth.github.client_id,
        provider='github',
        token_type=token['token_type'],
        access_token=token['access_token'],
        scope=token['scope'],
        issued_at=datetime.datetime.now().timestamp(),
        user_id=user.id
    )
    return redirect(current_app.config['FRONTEND_HOST']), SUCCESS


@sso.route(**SSO_GITHUB_REVOKE)
@swag_from(docs_path('api', 'sso', 'sso_github_revoke.yaml'), methods=['POST'], endpoint='sso.github_revoke')
@with_identity
def sso_github_revoke(identity):
    tokens = OAuth2Token.query \
        .join(Users, Users.id == OAuth2Token.user_id) \
        .filter(and_(Users.email == identity, OAuth2Token.provider == 'github')) \
        .all()
    [token.delete() for token in tokens]
    return jsonify({'message': 'success'}), SUCCESS

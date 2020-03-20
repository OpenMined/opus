import os
import time

from app.models import db, Users, OAuth2Client
from app.services.oauth2 import authorization
from authlib.oauth2 import OAuth2Error
from flasgger.utils import swag_from
from flask import Blueprint, request, session
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt

BASE_URL = '/oauth'
OAUTH_AUTHORIZE = {'rule': '/authorize', 'methods': ['POST', 'GET'], 'endpoint': 'authorize'}
OAUTH_CLIENT = {'rule': '/client', 'methods': ['POST', 'GET'], 'endpoint': 'client'}
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


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


@oauth.route(**OAUTH_CLIENT)
@swag_from(docs_path('api', 'oauth', 'oauth_client.yaml'), methods=['GET', 'POST'], endpoint='oauth.client')
def create_client():
    user = current_user()
    if not user:
        return redirect('/')
    if request.method == 'GET':
        return render_template('create_client.html')
    form = request.form
    client_id = gen_salt(24)
    client = OAuth2Client(client_id=client_id, user_id=user.id)
    # Mixin doesn't set the issue_at date
    client.client_id_issued_at = int(time.time())
    if client.token_endpoint_auth_method == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)
    db.session.add(client)
    db.session.commit()
    return redirect('/')


@oauth.route(**OAUTH_AUTHORIZE)
@swag_from(docs_path('api', 'oauth', 'oauth_authorize.yaml'), methods=['GET', 'POST'], endpoint='oauth.authorize')
def oauth_authorize():
    user = current_user()
    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
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
    return authorization.create_authorization_response(grant_user=grant_user)


@oauth.route(**OAUTH_TOKEN)
@swag_from(docs_path('api', 'oauth', 'oauth_token.yaml'), methods=['GET'], endpoint='oauth.token')
def oauth_token():
    return authorization.create_token_response()


@oauth.route(**OAUTH_REVOKE)
@swag_from(docs_path('api', 'oauth', 'oauth_revoke.yaml'), methods=['GET'], endpoint='oauth.revoke')
def oauth_revoke():
    return authorization.create_endpoint_response('revocation')

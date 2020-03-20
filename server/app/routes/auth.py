from flask import Blueprint, Response, redirect, url_for, jsonify, request, g
from flask_login import current_user, login_user
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User, db
from .errors import bad_request, error_response
from flasgger.utils import swag_from

import os

BASE_URL = ''
GET_TOKENS_VIEW = {'rule': '/tokens', 'methods': ['POST'], 'endpoint': 'get_tokens'}
REVOKE_TOKENS_VIEW = {'rule': '/tokens', 'methods': ['DELETE'], 'endpoint': 'revoke_tokens'}
LOGIN_VIEW = {'rule': '/login', 'methods': ['POST'], 'endpoint': 'login'}
SIGNUP_VIEW = {'rule': '/signup', 'methods': ['POST'], 'endpoint': 'signup'}

auth = Blueprint(name='auth', import_name=__name__, url_prefix=BASE_URL)

docs_path = lambda *args: os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', *args))

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)

# Endpoint for getting an authentication token
@auth.route(**GET_TOKENS_VIEW)
@basic_auth.login_required
@swag_from(docs_path('api', 'auth', 'get_tokens.yaml'), methods=['POST'], endpoint='auth.get_tokens')
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

# Endpoint for revoking an authentication token
@auth.route(**REVOKE_TOKENS_VIEW)
@token_auth.login_required
@swag_from(docs_path('api', 'auth', 'revoke_tokens.yaml'), methods=['DELETE'], endpoint='auth.revoke_tokens')
def revoke_token():
  g.current_user.revoke_token()
  db.session.commit()
  return '', 204

# Login route for users to authenticate into
@auth.route(**LOGIN_VIEW)
def login():
  # Think I've done this wrong. Don't need to make use of LoginManager. 
  # Simply need to return the token back to the front end.
  # Will implement token authentication and then strip back the unnecessary stuff. 
  data = request.get_json()
  user = User.query.filter_by(email=data['email']).first()
  
  if user is None or not user.check_password(data['password']):
    return bad_request('That email or password is incorrect. Please try again.')
  
  login_user(user)
  response = jsonify({
    "result": "success",
    "email": data["email"]
  })
  response.status_code = 200
  return response

# Signup route for when new users post their data
@auth.route(**SIGNUP_VIEW)
def signup():
  data = request.get_json() or {}
  if User.query.filter_by(email=data['email']).first():
    return bad_request('That email address has already been registered. Please try a different one!')

  user = User()
  user.from_dict(data, new_user=True)
  db.session.add(user)
  db.session.commit()
  
  response = jsonify(user.to_dict())
  response.status_code = 201
  response.headers['Location'] = url_for('users.get', id=user.id)

  return response



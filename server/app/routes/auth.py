from flask import Blueprint, Response, redirect, url_for, jsonify, request, g
from flask_login import current_user, login_user
from flask_httpauth import HTTPBasicAuth
from app.models import User, db
from .errors import bad_request, error_response

BASE_URL = ''
LOGIN_VIEW = {'rule': '/login', 'methods': ['POST'], 'endpoint': 'login'}
SIGNUP_VIEW = {'rule': '/signup', 'methods': ['POST'], 'endpoint': 'signup'}

auth = Blueprint(name='auth', import_name=__name__, url_prefix=BASE_URL)

basic_auth = HTTPBasicAuth()

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

@auth.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

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



from flask import Blueprint, Response, redirect, url_for, jsonify, request
from flask_login import current_user, login_user
from app.models import User, db
from .errors import bad_request

BASE_URL = ''
LOGIN_VIEW = {'rule': '/login', 'methods': ['POST'], 'endpoint': 'login'}
SIGNUP_VIEW = {'rule': '/signup', 'methods': ['POST'], 'endpoint': 'signup'}

auth = Blueprint(name='auth', import_name=__name__, url_prefix=BASE_URL)

# Login route for users to authenticate into
@auth.route(**LOGIN_VIEW)
def login():
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



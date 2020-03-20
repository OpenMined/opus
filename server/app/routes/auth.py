from flask import Response, redirect, url_for, jsonify, request
from flask_login import current_user, login_user
from app.models import User

BASE_URL = ''
LOGIN_VIEW = {'rule': '/login', 'methods': ['GET', 'POST'], 'endpoint': 'list'}
SIGNUP_VIEW = {'rule': '/signup', 'methods': ['POST'], 'endpoint': 'get'}

auth = Blueprint(name='auth', import_name=__name__, url_prefix=BASE_URL)

@auth.route(**LOGIN_VIEW)
def login():
  if request.method == 'POST':
    json = request.get_json()
    user = User.query.filter_by(email=json['email']).first()
    if user is None or not user.check_password(json['password']):
      return Response("Fail")
    login_user(user)
    # This shouldn't be a Flask redirect, it should
    # return the user to home page for the app in React
    return redirect(url_for('index'))

# Signup route for when new users post their data
@auth.route(**SIGNUP_VIEW)
def signup():
  if current_user.is_authenticated:
      # This shouldn't be a Flask redirect, it should
      # return the user to home page for the app in React
      return redirect(url_for('index'))
  json = request.json()
  user = User(email=form.email.data)
  user.set_password(form.password.data)
  db.session.add(user)
  db.session.commit()
  # Need to send the front end the correct response for when a user signs up
  return redirect(url_for('index'))

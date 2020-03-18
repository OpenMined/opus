from flask import Response, redirect, url_for, jsonify, request
from flask_login import current_user, login_user
from app.models import User

def init_base_routes(app):
  @app.route('/')
  def index():
    return Response("Hello, world!")

  @app.route('/login', methods=['GET', 'POST'])
  def login():
    if request.method == 'POST':
      json = request.get_json()
      user = User.query.filter_by(email=json['email']).first()
      if user is None or not user.check_password(json['password']):
        return Response("Fail")
      login_user(user)
      return redirect(url_for('index'))
    
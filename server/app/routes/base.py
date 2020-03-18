from flask import Response, redirect, url_for
from flask_login import current_user, login_user
from app.models import User

def init_base_routes(app):
  @app.route('/')
  def index():
    return Response("Hello, world!")

  @app.route('/login', methods=['GET', 'POST'])
  def login():
    if current_user.is_authenticated:
      return redirect(url_for('index'))
    form = LoginForm()

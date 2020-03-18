from flask import Response, redirect, url_for
from flask_login import current_user, login_user
from app.models import User

def init_base_routes(app):
  @app.route('/')
  def index():
    return Response("Hello, world!")

  @app.route('/login', methods=['GET', 'POST'])
  def login():
    # When the front end is integrated with the back end this will be replaced
    # with the data posted by the fetch call. 
    # Something like request.get_data() should help here
    if current_user.is_authenticated:
      return redirect(url_for('index'))
    
    if request.method == 'POST':
      print(request.get_data())
      request.get_data()
      user = User.query.filter_by(email=request.data["email"]).first()
      if user is None or not user.check_password(request.data["password"]):
        return redirect(url_for('login'))
      login_user(user)
    return redirect(url_for('index'))

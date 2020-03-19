import os
from flask import Flask
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
  app = Flask(__name__)
  CORS(app)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  from . import routes, services, models
  routes.init_app(app)
  models.init_app(app)
  return app

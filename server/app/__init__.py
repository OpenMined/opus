import os

from flask import Flask
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))


PACKAGE_VERSION = "0.0.0"
APP_NAME = 'Private Identity Server'

def create_app():
  app = Flask(__name__)
  CORS(app)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  register_blueprints(app)
  register_extensions(app)

  return app


def register_extensions(app):
  """
  Register extensions with the Flask application.
  Order is important!
  """
  from .models import db
  from .extensions import migrate
  from .spec import configure_spec
  db.init_app(app)
  migrate.init_app(app, db)
  configure_spec(app)

def register_blueprints(app):
  """register all needed flask blueprints with the current app"""

  from .routes import all_blueprints

  for bp in all_blueprints:
    app.register_blueprint(bp)

import os
from flask import Flask
from flask_cors import CORS

def create_app():
  app = Flask(__name__)
  CORS(app)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  from . import routes, services, models
  routes.init_app(app)
  models.init_app(app)
  return app

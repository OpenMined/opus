import json
import os

from flask import Flask, Request
from werkzeug.exceptions import BadRequest

from .database import db
from .extensions import migrate, password_hasher, config_oauth_server, config_oauth_client, jwt, cors
from .routes import all_blueprints
from .spec import configure_spec

PACKAGE_VERSION = "0.0.0"
APP_NAME = 'Private Identity Server'


class CustomRequest(Request):
    def on_json_loading_failed(self, e):
        if isinstance(e, json.JSONDecodeError):
            raise json.JSONDecodeError(e.msg, e.doc, e.pos)
        raise BadRequest('Failed to decode JSON object: {0}'.format(e))


def create_app():
    app = Flask(__name__)
    app.request_class = CustomRequest

    load_config(app)
    register_blueprints(app)
    register_extensions(app)
    return app


def load_config(app):
    from werkzeug.utils import import_string
    config = {
        "development": "app.config.DevelopmentConfig",
        "production": "app.config.ProductionConfig",
        "test": "app.config.TestConfig",
        "default": "app.config.DevelopmentConfig"
    }
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    config_obj = import_string(config[config_name])
    config_obj.apply_config(app)


def register_extensions(app):
    """
    Register extensions with the Flask application.
    Order is important!
    """
    password_hasher(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    config_oauth_client(app)
    config_oauth_server(app)
    configure_spec(app)


def register_blueprints(app):
    """register all needed flask blueprints with the current app"""
    for bp in all_blueprints:
        app.register_blueprint(bp)

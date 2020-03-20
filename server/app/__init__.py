import os

from flask import Flask

from .services.oauth2 import config_oauth

PACKAGE_VERSION = "0.0.0"
APP_NAME = 'Private Identity Server'


def create_app():
    app = Flask(__name__)

    load_config(app)

    register_blueprints(app)
    register_extensions(app)

    return app


def load_config(app):
    config = {
        "development": "app.config.DevelopmentConfig",
        "production": "app.config.ProductionConfig",
        "test": "app.config.TestConfig",
        "default": "app.config.DevelopmentConfig"
    }
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    from werkzeug.utils import import_string
    config_obj = import_string(config[config_name])
    config_obj.apply_config(app)


def register_extensions(app):
    """
    Register extensions with the Flask application.
    Order is important!
    """
    from .database import db
    from .extensions import migrate, password_hasher
    from .spec import configure_spec
    password_hasher(app)
    db.init_app(app)
    migrate.init_app(app, db)
    config_oauth(app)
    configure_spec(app)


def register_blueprints(app):
    """register all needed flask blueprints with the current app"""

    from .routes import all_blueprints

    for bp in all_blueprints:
        app.register_blueprint(bp)

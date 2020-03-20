import os

from flask import Config


class DevelopmentConfig(Config):
    @staticmethod
    def apply_config(app):
        mapping = {
            'PORT': 5000,
            'FLASK_DEBUG': True,
            'SQLALCHEMY_DATABASE_URI': os.getenv(
                'SQLALCHEMY_DATABASE_URI',
                'postgresql://postgres:pis_local_5432@localhost:5432'
            ),
            'SQLALCHEMY_TRACK_MODIFICATIONS': os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', True),
            'DEBUG': True,
            'SQLALCHEMY_ECHO': True,
            'AUTHLIB_INSECURE_TRANSPORT': True
        }
        app.config.from_mapping(mapping)


class TestConfig(DevelopmentConfig):
    pass


class ProductionConfig(Config):
    @staticmethod
    def apply_config(app):
        mapping = {
            'PORT': 5000,
            'FLASK_DEBUG': False,
            'SQLALCHEMY_DATABASE_URI': os.environ['SQLALCHEMY_DATABASE_URI'],
            'SQLALCHEMY_TRACK_MODIFICATIONS': os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', True),
            'DEBUG': False,
            'SQLALCHEMY_ECHO': False,
            'AUTHLIB_INSECURE_TRANSPORT': False
        }
        app.config.from_mapping(mapping)

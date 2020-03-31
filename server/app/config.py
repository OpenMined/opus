import datetime
import os

from flask import Config


class DevelopmentConfig(Config):
    @staticmethod
    def apply_config(app):
        mapping = {
            'OAUTH_JWT_CONFIG': {
                'key': '-----BEGIN EC PRIVATE KEY-----\nMIHcAgEBBEIA3YrYysvfsUvosUMxCpAtqnmwYFVpAlrgl3oTQsQPuLoPuCyAkzbV\n90nIPd6R/9xtXkehGuv5DvRiWuLsWXBB/X+gBwYFK4EEACOhgYkDgYYABAAIeRlB\nGyaNMbzzd7PHPpVDxzFdqDhlCn2dLXtRb7pYMvr5VE59E/nQKVXbRMKZapcJvBhg\nV00wms62S5RzCm2HdwCsYsrDd5tVhLHbjQSzrqbud38zuRsFXoOltvW2uLnIAU2q\nrhh1S6o7i61BGOdfg+9YuiwHS/UCRT6VFOyHydapKw==\n-----END EC PRIVATE KEY-----\n',
                'pub_key': '-----BEGIN PUBLIC KEY-----\nMIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQACHkZQRsmjTG883ezxz6VQ8cxXag4\nZQp9nS17UW+6WDL6+VROfRP50ClV20TCmWqXCbwYYFdNMJrOtkuUcwpth3cArGLK\nw3ebVYSx240Es66m7nd/M7kbBV6Dpbb1tri5yAFNqq4YdUuqO4utQRjnX4PvWLos\nB0v1AkU+lRTsh8nWqSs=\n-----END PUBLIC KEY-----\n',
                'alg': 'ES512',
                'iss': 'http://localhost:500',
                'exp': datetime.timedelta(minutes=15).seconds,
            },
            'JWT_PRIVATE_KEY': '-----BEGIN EC PRIVATE KEY-----\nMIHcAgEBBEIA3YrYysvfsUvosUMxCpAtqnmwYFVpAlrgl3oTQsQPuLoPuCyAkzbV\n90nIPd6R/9xtXkehGuv5DvRiWuLsWXBB/X+gBwYFK4EEACOhgYkDgYYABAAIeRlB\nGyaNMbzzd7PHPpVDxzFdqDhlCn2dLXtRb7pYMvr5VE59E/nQKVXbRMKZapcJvBhg\nV00wms62S5RzCm2HdwCsYsrDd5tVhLHbjQSzrqbud38zuRsFXoOltvW2uLnIAU2q\nrhh1S6o7i61BGOdfg+9YuiwHS/UCRT6VFOyHydapKw==\n-----END EC PRIVATE KEY-----\n',
            'JWT_PUBLIC_KEY': '-----BEGIN PUBLIC KEY-----\nMIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQACHkZQRsmjTG883ezxz6VQ8cxXag4\nZQp9nS17UW+6WDL6+VROfRP50ClV20TCmWqXCbwYYFdNMJrOtkuUcwpth3cArGLK\nw3ebVYSx240Es66m7nd/M7kbBV6Dpbb1tri5yAFNqq4YdUuqO4utQRjnX4PvWLos\nB0v1AkU+lRTsh8nWqSs=\n-----END PUBLIC KEY-----\n',
            'JWT_ALGORITHM': 'ES512',
            'FRONTEND_HOST': os.getenv('FRONTEND_HOST', 'http://localhost:3000'),
            'JWT_DECODE_ISSUER': os.getenv('JWT_DECODE_ISSUER', 'http://localhost:5000'),
            'JWT_ACCESS_TOKEN_EXPIRES': datetime.timedelta(minutes=15),
            'JWT_REFRESH_TOKEN_EXPIRES': datetime.timedelta(days=30),
            'PORT': 5000,
            'FLASK_DEBUG': True,
            'SECRET_KEY': '7d88acba72577d7ba964710bab26af4d',
            'SQLALCHEMY_DATABASE_URI': os.getenv(
                'SQLALCHEMY_DATABASE_URI',
                'postgresql://postgres:opus_local_5432@localhost:5432'
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
            'JWT_PRIVATE_KEY': os.environ["JWT_PRIVATE_KEY"],
            'JWT_PUBLIC_KEY': os.environ["JWT_PUBLIC_KEY"],
            'JWT_ALGORITHM': 'ES512',
            'JWT_DECODE_ISSUER': os.environ["JWT_DECODE_ISSUER"],
            'JWT_ACCESS_TOKEN_EXPIRES': os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", datetime.timedelta(minutes=15)),
            'JWT_REFRESH_TOKEN_EXPIRES': os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", datetime.timedelta(days=30)),
            'FLASK_DEBUG': False,
            'SECRET_KEY': os.environ['SECRET_KEY'],
            'SQLALCHEMY_DATABASE_URI': os.environ['SQLALCHEMY_DATABASE_URI'],
            'SQLALCHEMY_TRACK_MODIFICATIONS': os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', True),
            'DEBUG': False,
            'SQLALCHEMY_ECHO': False,
            'AUTHLIB_INSECURE_TRANSPORT': False
        }
        app.config.from_mapping(mapping)

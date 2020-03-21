import argon2
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer, ResourceProtector)
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_save_token_func,
    create_bearer_token_validator,
)
from flask_migrate import Migrate

from .database import db
from .models import OAuth2Token, OAuth2Client
from .services.oauth2 import AuthorizationCodeGrant, OpenIDCode, HybridGrant

migrate = Migrate()


def register_as_extension(app, name, object_instance):
    if not hasattr(app, 'extensions'):
        app.extensions = {}

    if name in app.extensions:
        raise RuntimeError("Flask extension already initialized")

    app.extensions[name] = object_instance


def config_oauth(app):
    require_oauth = ResourceProtector()
    authorization = AuthorizationServer()
    query_client = create_query_client_func(db.session, OAuth2Client)
    save_token = create_save_token_func(db.session, OAuth2Token)
    authorization.init_app(
        app,
        query_client=query_client,
        save_token=save_token
    )
    # support all openid grants
    authorization.register_grant(AuthorizationCodeGrant, [
        OpenIDCode(require_nonce=True, **app.config['OAUTH_JWT_CONFIG']),
    ])
    authorization.register_grant(HybridGrant)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())

    register_as_extension(app, 'authorization', authorization)
    register_as_extension(app, 'require_oauth', require_oauth)


def password_hasher(app):
    password_hasher = argon2.PasswordHasher(
        time_cost=app.config.get('ARGON2_TIME_COST', argon2.DEFAULT_TIME_COST),
        memory_cost=app.config.get('ARGON2_MEMORY_COST', argon2.DEFAULT_MEMORY_COST),
        parallelism=app.config.get('ARGON2_PARALLELISM', argon2.DEFAULT_PARALLELISM),
        hash_len=app.config.get('ARGON2_HASH_LENGTH', argon2.DEFAULT_HASH_LENGTH),
        salt_len=app.config.get('ARGON2_SALT_LENGTH', argon2.DEFAULT_RANDOM_SALT_LENGTH),
        encoding=app.config.get('ARGON2_ENCODING', 'utf-8')
    )
    register_as_extension(app, 'password_hasher', password_hasher)

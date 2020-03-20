import argon2
from flask_migrate import Migrate

migrate = Migrate()


def password_hasher(app):
    time_cost = app.config.get('ARGON2_TIME_COST', argon2.DEFAULT_TIME_COST)
    memory_cost = app.config.get('ARGON2_MEMORY_COST', argon2.DEFAULT_MEMORY_COST)
    parallelism = app.config.get('ARGON2_PARALLELISM', argon2.DEFAULT_PARALLELISM)
    hash_len = app.config.get('ARGON2_HASH_LENGTH', argon2.DEFAULT_HASH_LENGTH)
    salt_len = app.config.get('ARGON2_SALT_LENGTH', argon2.DEFAULT_RANDOM_SALT_LENGTH)
    encoding = app.config.get('ARGON2_ENCODING', 'utf-8')
    ph = argon2.PasswordHasher(
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=hash_len,
        salt_len=salt_len,
        encoding=encoding
    )
    if not hasattr(app, 'extensions'):
        app.extensions = {}

    if 'password_hasher' in app.extensions:
        raise RuntimeError("Flask extension already initialized")

    app.extensions['password_hasher'] = ph

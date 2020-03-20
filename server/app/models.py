from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from flask import current_app

from .constants import CASCADE, KEEP_PARENTS
from .database import CRUDMixin, db, GUID


def check_password_hash(pw_hash, password):
    return current_app.extensions['password_hasher'].verify(pw_hash, password)


class Users(CRUDMixin, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128))

    oauth2_client = db.relationship("OAuth2Client", uselist=True, back_populates="users", cascade=CASCADE)
    oauth2_code = db.relationship("OAuth2AuthorizationCode", uselist=True, back_populates="users", cascade=CASCADE)
    oauth2_token = db.relationship("OAuth2Token", uselist=True, back_populates="users", cascade=CASCADE)

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = current_app.extensions['password_hasher'].hash(password)


class OAuth2Client(CRUDMixin, db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    user_id = db.Column('user_id', GUID(), db.ForeignKey('users.id', name="oauth2_client_user_id_fkey"), nullable=False)
    users = db.relationship("Users", uselist=False, back_populates="oauth2_client", cascade=KEEP_PARENTS)


class OAuth2AuthorizationCode(CRUDMixin, db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    user_id = db.Column('user_id', GUID(), db.ForeignKey('users.id', name="oauth2_code_user_id_fkey"), nullable=False)
    users = db.relationship("Users", uselist=False, back_populates="oauth2_code", cascade=KEEP_PARENTS)


class OAuth2Token(CRUDMixin, db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    user_id = db.Column('user_id', GUID(), db.ForeignKey('users.id', name="oauth2_token_user_id_fkey"), nullable=False)
    users = db.relationship("Users", uselist=False, back_populates="oauth2_token", cascade=KEEP_PARENTS)

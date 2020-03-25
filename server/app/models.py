from app.constants import CASCADE, KEEP_PARENTS
from app.database import CRUDMixin, db, GUID
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from flask import current_app


class Users(CRUDMixin, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128))

    oauth2_client = db.relationship("OAuth2Client", uselist=True, back_populates="users", cascade=CASCADE)
    oauth2_code = db.relationship("OAuth2AuthorizationCode", uselist=True, back_populates="users", cascade=CASCADE)
    oauth2_token = db.relationship("OAuth2Token", uselist=True, back_populates="users", cascade=CASCADE)

    # required by authlib/integrations/sqla_oauth2/functions.py
    def get_user_id(self):
        return self.id

    @property
    def password(self):
        raise AttributeError('password not readable')

    @property
    def brief(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }

    @password.setter
    def password(self, password):
        self.password_hash = current_app.extensions['password_hasher'].hash(password)

    def password_correct(self, password):
        return current_app.extensions['password_hasher'].verify(self.password_hash, password)


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

    provider = db.Column('provider', db.String(255), nullable=False, default='pis')

    user_id = db.Column('user_id', GUID(), db.ForeignKey('users.id', name="oauth2_token_user_id_fkey"), nullable=False)
    users = db.relationship("Users", uselist=False, back_populates="oauth2_token", cascade=KEEP_PARENTS)

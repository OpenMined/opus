from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager

import base64
from datetime import datetime, timedelta
import os

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login = LoginManager()

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  token = db.Column(db.String(32), index=True, unique=True)
  token_expiration = db.Column(db.DateTime)

  # For use with the API, allows get requests to easily serve JSON
  # about the users. Should allow the API model to flexibly expanded upon
  def to_dict(self):
    data = {
      'id': self.id,
      'email': self.email,
    }
    return data

  # Allows API to easily consume json about users.
  def from_dict(self, data, new_user=False):
    # Should be extensible for when User model becomes more complex
    for field in ['email']:
      if field in data:
        setattr(self, field, data[field])
    if new_user and 'password' in data:
      self.set_password(data['password'])

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def get_token(self, expires_in=3600):
    now = datetime.utcnow()
    if self.token and self.token_expiration > now + timedelta(seconds=60):
        return self.token
    self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    self.token_expiration = now + timedelta(seconds=expires_in)
    db.session.add(self)
    return self.token

  def revoke_token(self):
      self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

  @staticmethod
  def check_token(token):
      user = User.query.filter_by(token=token).first()
      if user is None or user.token_expiration < datetime.utcnow():
          return None
      return user

  def __repr__(self):
    return '<Email {}>'.format(self.email)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

  

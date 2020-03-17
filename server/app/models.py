from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
  db.init_app(app)
  migrate.init_app(app, db)


class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)

  def __repr__(self):
    return '<id {}>'.format(self.id)

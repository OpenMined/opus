from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)

  def __repr__(self):
    return '<id {}>'.format(self.id)

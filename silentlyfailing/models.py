from datetime import datetime
import flask_sqlalchemy
from flask_login import UserMixin
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash


db = flask_sqlalchemy.SQLAlchemy()
migrate = Migrate()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    content = db.Column(db.String)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.String)

    def __repr__(self):
        return '<Post %r>' % (self.subject)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):
        return {
            'subject': self.subject,
            'content': self.content,
            'author': self.author,
            'time': self.time,
        }


def setup_admin_user(db):
    username = os.environ['ADMIN_USERNAME']
    password = os.environ['ADMIN_PASSWORD']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(id=1, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

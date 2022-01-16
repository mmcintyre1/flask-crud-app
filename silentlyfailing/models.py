from datetime import datetime
from flask_login import UserMixin
import os
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash


from silentlyfailing import db


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
    title = db.Column(db.String)
    slug = db.Column(db.String(255))
    body = db.Column(db.String)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.String)

    def __repr__(self):
        return f'<Post {self.title}>'

    @property
    def serialize(self):
        return {
            'title': self.title,
            'body': self.body,
            'created_date': self.created_date,
            'last_updated': self.last_updated,
            'author': self.author,
        }

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def update_post(self, title, body):
        self.title = title
        self.body = body
        self.last_updated = datetime.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def setup_admin_user(db):
    username = os.environ['ADMIN_USERNAME']
    password = os.environ['ADMIN_PASSWORD']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(id=1, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


db.event.listen(Post.title, 'set', Post.slugify, retval=False)

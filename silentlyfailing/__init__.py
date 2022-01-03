
from flask import Flask

from .models import db


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    app.app_context().push()

    db.init_app(app)
    db.create_all()

    @ app.route('/')
    @ app.route('/index')
    def index():
        return 'Hello, World!'

    return app

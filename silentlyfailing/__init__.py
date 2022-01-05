
from flask import Flask

from .models import db, migrate


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        db.create_all()

    @app.route('/')
    @app.route('/index')
    def index():
        return 'Hello, World!'

    return app


from distutils.core import setup
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor


db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = "sf.login"


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # register blueprints
    from .routes import sf
    app.register_blueprint(sf)
    from .commands import setup_admin
    app.cli.add_command(setup_admin)

    with app.app_context():
        # initialize extensions
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)
        ckeditor.init_app(app)

    return app

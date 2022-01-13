
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    from .routes import sf
    app.register_blueprint(sf)

    with app.app_context():
        # initialize extensions
        from silentlyfailing import models
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)

        # setup admin user
        models.setup_admin_user(db)

    return app


from flask import Flask

from .models import db, migrate, setup_admin_user
from .routes import sf, login_manager


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    with app.app_context():
        # register blueprints
        app.register_blueprint(sf)

        # initialize plugins
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)

        # setup database
        db.create_all()

        # setup admin user
        setup_admin_user(db)

    return app

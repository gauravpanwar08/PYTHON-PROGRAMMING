from flask import Flask

from app.config import Config
from app.extensions import db

from app.models import User

from app.routes.home_routes import home_bp
from app.routes.user_routes import user_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)

    return app

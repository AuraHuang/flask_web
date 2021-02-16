from flask import Flask
from apps.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    from apps.shares_resturn.routes import shares_return_bp
    app.register_blueprint(shares_return_bp, url_prefix="/shares-return")

    return app
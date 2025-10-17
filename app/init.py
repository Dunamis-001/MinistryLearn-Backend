from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, jwt, ma, api, swagger
from .resources.health import health_bp
from .resources import auth as auth_resource
from .openapi.swagger import swagger_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    app.register_blueprint(swagger_blueprint, url_prefix="/docs")
    app.register_blueprint(health_bp, url_prefix="/health")

    # API resources
    auth_resource.register(api)

    return app
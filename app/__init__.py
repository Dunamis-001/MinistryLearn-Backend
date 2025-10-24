from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, jwt, ma, api, swagger
from .resources.health import health_bp
from .resources import auth as auth_resource
from .resources import courses as courses_resource
from .resources import enrollments as enrollments_resource
from .resources import modules as modules_resource
from .resources import lessons as lessons_resource
from .resources import assessments as assessments_resource
from .resources import submissions as submissions_resource
from .resources import certifications as certifications_resource
from .resources import media as media_resource
from .resources import announcements as announcements_resource
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
    courses_resource.register(api)
    enrollments_resource.register(api)
    modules_resource.register(api)
    lessons_resource.register(api)
    assessments_resource.register(api)
    submissions_resource.register(api)
    certifications_resource.register(api)
    media_resource.register(api)
    announcements_resource.register(api)

    return app
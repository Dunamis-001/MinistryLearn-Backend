from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, jwt, ma, api
from .resources.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix="/health")

    # Create API blueprint
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(api_bp)

    # Import and register API resources after app initialization
    try:
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

        # Register API resources
        print("Registering API resources...")
        auth_resource.register(api)
        print("✓ Auth resources registered")
        courses_resource.register(api)
        print("✓ Courses resources registered")
        enrollments_resource.register(api)
        print("✓ Enrollments resources registered")
        modules_resource.register(api)
        print("✓ Modules resources registered")
        lessons_resource.register(api)
        print("✓ Lessons resources registered")
        assessments_resource.register(api)
        print("✓ Assessments resources registered")
        submissions_resource.register(api)
        print("✓ Submissions resources registered")
        certifications_resource.register(api)
        print("✓ Certifications resources registered")
        media_resource.register(api)
        print("✓ Media resources registered")
        announcements_resource.register(api)
        print("✓ Announcements resources registered")
        
        # Register the API blueprint with the app
        app.register_blueprint(api_bp)
        
        # Print all registered routes
        print("\nRegistered routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.methods} {rule.rule}")
            
    except Exception as e:
        print(f"Error registering resources: {e}")
        import traceback
        traceback.print_exc()

    # Root route to avoid 404 at service base URL
    @app.route("/", methods=["GET"]) 
    def index():
        return jsonify({
            "message": "MinistryLearn API",
            "health": "/health/",
            "docs": "/docs/",
            "api_prefix": "/api"
        }), 200

    return app
from flask import Flask, Blueprint
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, jwt, ma, api
from .resources.health import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Register CLI commands
    from .commands import create_example_courses, fix_leadership_thumbnail, remove_all_videos
    app.cli.add_command(create_example_courses)
    app.cli.add_command(fix_leadership_thumbnail)
    app.cli.add_command(remove_all_videos)
    
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
        from .resources import ai_chat as ai_chat_resource
        from .resources import ai_features as ai_features_resource

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
        ai_chat_resource.register(api)
        print("✓ AI Chat resources registered")
        ai_features_resource.register(api)
        print("✓ AI Features resources registered")
        
        # Register the API blueprint with the app
        app.register_blueprint(api_bp)
        
        # Configure CORS AFTER blueprints are registered
        # Apply CORS to entire app for development
        CORS(app, 
             origins="*",
             methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
             allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
             supports_credentials=True)
        
        # Note: Removed manual after_request handler to avoid duplicate CORS headers
        # The CORS middleware above handles all CORS headers
        
        # Print all registered routes
        print("\nRegistered routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.methods} {rule.rule}")
            
    except Exception as e:
        print(f"Error registering resources: {e}")
        import traceback
        traceback.print_exc()

    return app
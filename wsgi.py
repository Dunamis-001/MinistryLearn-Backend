from app import create_app
from flasgger import Swagger
import os
from flask_migrate import upgrade

app = create_app()

# Initialize Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, config=swagger_config)

# Auto-run migrations on startup (useful on Render free tier without shell)
if os.getenv("AUTO_MIGRATE", "true").lower() == "true":
    try:
        with app.app_context():
            upgrade()
            print("✓ Database migrations applied")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
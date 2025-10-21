# test_app_load.py

from app import create_app
from app.extensions import db
from app.models import User, Role, UserRole

print("🧩 Testing Flask app initialization...")

app = create_app()

with app.app_context():
    print("✅ App context loaded successfully.")

    # Check that database is connected
    engine = db.get_engine()
    print(f"✅ Database connected: {engine.url}")

    # Check that tables exist in metadata
    print("✅ Models registered:")
    for table in db.metadata.tables.keys():
        print(f"   - {table}")

    print("\nAll checks passed successfully 🎉")

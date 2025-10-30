import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("postgresql://"):
        # Use psycopg3 driver automatically if a plain postgresql URL is provided
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
    SWAGGER = {
        "title": "MinistryLearn API",
        "uiversion": 3,
    }
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Cloudinary settings
    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
    
    # SendGrid settings
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
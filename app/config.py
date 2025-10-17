import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
    SWAGGER = {
        "title": "MinistryLearn API",
        "uiversion": 3,
    }
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
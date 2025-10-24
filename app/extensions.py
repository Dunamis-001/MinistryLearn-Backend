from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow 
from flask_restful import Api
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(prefix="/api")
swagger = Swagger()
ma = Marshmallow()  # ✅ create a proper Marshmallow instance

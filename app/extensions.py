from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from marshmallow import Schema
from flask_restful import Api
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api()  # Remove prefix from here, we'll handle it differently
swagger = Swagger()
ma = Schema  # marker, not used directly; schemas are marshmallow.Schema classes
from flask import Blueprint
from flasgger import Swagger

swagger_blueprint = Blueprint("swagger_ui", __name__)

def init_swagger(app):
    Swagger(app)
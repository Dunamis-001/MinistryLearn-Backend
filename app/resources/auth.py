from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..schemas.auth import RegisterSchema, LoginSchema
from ..services.auth_service import AuthService

register_schema = RegisterSchema()
login_schema = LoginSchema()

def register(api):
    api.add_resource(RegisterResource, "/auth/register")
    api.add_resource(LoginResource, "/auth/login")
    api.add_resource(ProfileResource, "/auth/profile")
    api.add_resource(RefreshResource, "/auth/refresh")

class RegisterResource(Resource):
    def post(self):
        """Register a new user"""
        try:
            data = register_schema.load(request.get_json() or {})
            user = AuthService.register_user(
                data["email"], 
                data["username"], 
                data["password"]
            )
            return {"message": "User registered successfully"}, 201
        except ValueError as e:
            return {"message": str(e)}, 409
        except Exception as e:
            return {"message": "Registration failed"}, 400

class LoginResource(Resource):
    def post(self):
        """Login user and return tokens"""
        try:
            data = login_schema.load(request.get_json() or {})
            result = AuthService.authenticate_user(data["email"], data["password"])
            return result, 200
        except ValueError as e:
            return {"message": str(e)}, 401
        except Exception as e:
            return {"message": "Login failed"}, 400

class ProfileResource(Resource):
    @jwt_required()
    def get(self):
        """Get current user profile"""
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return user.to_dict(), 200

class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        try:
            user_id = get_jwt_identity()
            result = AuthService.refresh_token(user_id)
            return result, 200
        except ValueError as e:
            return {"message": str(e)}, 401
        except Exception as e:
            return {"message": "Token refresh failed"}, 400
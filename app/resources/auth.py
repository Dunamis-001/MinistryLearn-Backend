from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..models.role import Role
from ..schemas.auth import RegisterSchema, LoginSchema

register_schema = RegisterSchema()
login_schema = LoginSchema()

def register(api):
    api.add_resource(RegisterResource, "/auth/register")
    api.add_resource(LoginResource, "/auth/login")
    api.add_resource(ProfileResource, "/auth/profile")
    api.add_resource(RefreshResource, "/auth/refresh")

class RegisterResource(Resource):
    def post(self):
        data = register_schema.load(request.get_json() or {})
        if User.query.filter((User.email == data["email"]) | (User.username == data["username"])).first():
            return {"message": "Email or username already exists"}, 409
        user = User(email=data["email"], username=data["username"])
        user.set_password(data["password"])
        # default role Learner
        learner = Role.query.filter_by(name="Learner").first()
        if learner:
            user.roles.append(learner)
        db.session.add(user)
        db.session.commit()
        return {"message": "Registered"}, 201

class LoginResource(Resource):
    def post(self):
        data = login_schema.load(request.get_json() or {})
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return {"message": "Invalid credentials"}, 401
        roles = [r.name for r in user.roles]
        access = create_access_token(identity=user.id, additional_claims={"roles": roles})
        refresh = create_refresh_token(identity=user.id)
        return {"access_token": access, "refresh_token": refresh, "roles": roles}, 200

class ProfileResource(Resource):
    @jwt_required()
    def get(self):
        uid = get_jwt_identity()
        user = User.query.get_or_404(uid)
        return {"id": user.id, "email": user.email, "username": user.username, "roles": [r.name for r in user.roles]}, 200

class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        uid = get_jwt_identity()
        user = User.query.get_or_404(uid)
        roles = [r.name for r in user.roles]
        access = create_access_token(identity=user.id, additional_claims={"roles": roles})
        return {"access_token": access}, 200
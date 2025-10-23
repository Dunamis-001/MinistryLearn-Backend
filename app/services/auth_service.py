from flask_jwt_extended import create_access_token, create_refresh_token
from ..extensions import db
from ..models.user import User
from ..models.role import Role

class AuthService:
    @staticmethod
    def register_user(email, username, password):
        """Register a new user with default Learner role"""
        # Check if user already exists
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            raise ValueError("Email or username already exists")
        
        # Create new user
        user = User(email=email, username=username)
        user.set_password(password)
        
        # Assign default Learner role
        learner_role = Role.query.filter_by(name="Learner").first()
        if learner_role:
            user.roles.append(learner_role)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user and return tokens"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise ValueError("Invalid credentials")
        
        roles = [role.name for role in user.roles]
        access_token = create_access_token(
            identity=user.id, 
            additional_claims={"roles": roles}
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "roles": roles
        }
    
    @staticmethod
    def refresh_token(user_id):
        """Create new access token from refresh token"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        roles = [role.name for role in user.roles]
        access_token = create_access_token(
            identity=user.id, 
            additional_claims={"roles": roles}
        )
        
        return {"access_token": access_token}
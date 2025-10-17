from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if not claims or "roles" not in claims:
                return jsonify({"message": "Forbidden"}), 403
            user_roles = claims.get("roles", [])
            if not any(r in user_roles for r in roles):
                return jsonify({"message": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
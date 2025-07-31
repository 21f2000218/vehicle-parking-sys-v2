from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.extensions import jwt
from model.user import User
from services.auth_service import AuthService

def has_role(*roles_allowed):
    roles = [r.lower() for r in roles_allowed]
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role', '').lower()
            if user_role not in roles:
                return jsonify({"msg": "Forbidden: insufficient role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@jwt.token_in_blocklist_loader
def check_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return AuthService.is_token_revoked(jti)

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has been revoked or expired"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token expired"}), 401

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = User.query.get(identity)
    return {"role": user.role.value if user else "user"}


# @jwt_required(optional=True)
# def authenticate():
#     identity = get_jwt_identity()
#     if not identity:
#         return jsonify({"msg": "Missing or invalid token"}), 401
#     return jsonify({"msg": "Authenticated", "identity": identity}), 200
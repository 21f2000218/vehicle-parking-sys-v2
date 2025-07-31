from datetime import datetime, timedelta

from flask import current_app
from flask_jwt_extended import create_access_token
from model.enum import RoleEnum
from model.tokens import Tokens
from model.user import User

from app.extensions import db

class AuthService:
    @staticmethod
    def create_user(username, email, password, license_no, role):
        user = User(username=username, email=email, license_no=license_no, role=role)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def refresh(refresh):
        token = Tokens.query.filter_by(jti=refresh, token_type="refresh", expiry=False).first()

        if not token:
            return {"error": "Invalid or expired refresh token"}, 401
        
        user = User.query.get(token.user_id)

        if not user:
            return {"error": "User not found"}, 404
        
        access_token = create_access_token(identity=user.email)
        return {"access_token": access_token}
    
    @staticmethod
    def store_token(jti, user_id, token_type):
        token = Tokens(
            jti=jti,
            user_id=user_id,
            token_type=token_type,
            expiry=False,
            created_at=datetime.now()
        )
        db.session.add(token)
        db.session.commit()

    @staticmethod
    def revoke_token(jti, user_id):
        token = Tokens.query.filter_by(jti=jti, user_id=user_id).first()
        if token:
            token.mark_expired()
        else:
            token = Tokens(
                jti=jti,
                user_id=user_id,
                token_type="unknown",
                created_at=datetime.now(),
                expiry=True,
                revoked_at=datetime.now()
            )
            db.session.add(token)
            db.session.commit()

    @staticmethod
    def is_token_revoked(jti):
        token = Tokens.query.filter_by(jti=jti).first()
        if not token:
            return False
        return token.expiry
    
    @staticmethod
    def expire_tokens():
        """Should be run as a scheduled job, not on every request!"""
        access_expires = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
        refresh_expires = current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES')
        now = datetime.now()

        access_expiry_duration = (
            timedelta(seconds=access_expires) if isinstance(access_expires, int) else access_expires
        )
        refresh_expiry_duration = (
            timedelta(seconds=refresh_expires) if isinstance(refresh_expires, int) else refresh_expires
        )

        access_tokens = Tokens.query.filter_by(expiry=False, token_type="access").all()
        for token in access_tokens:
            if now > token.created_at + access_expiry_duration:
                token.expiry = True
                token.revoked_at = now

        refresh_tokens = Tokens.query.filter_by(expiry=False, token_type="refresh").all()
        for token in refresh_tokens:
            if now > token.created_at + refresh_expiry_duration:
                token.expiry = True
                token.revoked_at = now

        db.session.commit()
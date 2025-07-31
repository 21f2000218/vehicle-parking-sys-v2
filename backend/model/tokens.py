from app.extensions import db
from datetime import datetime


class Tokens(db.Model):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.now())
    expiry = db.Column(db.Boolean, default=False, nullable=False)
    token_type = db.Column(db.String(20), nullable=False)

    user = db.relationship('User', back_populates='tokens')

    def mark_expired(self):
        self.expiry = True
        db.session.add(self)
        db.session.commit()
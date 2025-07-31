from datetime import datetime
from enum import Enum
from app.extensions import db, pwd_context
from sqlalchemy.ext.hybrid import hybrid_property

from model.enum import RoleEnum

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    license_no = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.Enum(
            RoleEnum,
            values_callable=lambda e: [m.value for m in e],
            name="roleenum",
            native_enum=False
        ),
        nullable=False,
        default=RoleEnum.USER.value     
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tokens = db.relationship('Tokens', back_populates='user', lazy='dynamic')
    reservations = db.relationship("Reservation", back_populates="user")

    @hybrid_property
    def password(self):
        return self.pwd_hash

    @password.setter
    def password(self, raw_password):
        self.pwd_hash = pwd_context.hash(raw_password)

    def check_password(self, raw_password):
        return pwd_context.verify(raw_password, self.pwd_hash)
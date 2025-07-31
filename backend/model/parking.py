from app.extensions import db
from datetime import datetime

from model.enum import ReservationStatusEnum, SpotEnum

class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    pincode = db.Column(db.String(10))
    price_per_hour = db.Column(db.Float, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    spots = db.relationship('ParkingSpot', back_populates='lot', cascade="all, delete-orphan")

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.Enum(SpotEnum), default=SpotEnum.AVAILABLE, nullable=False, native_enum=False)
    remarks = db.Column(db.String(255))
    last_updated = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)
    
    lot = db.relationship('ParkingLot', back_populates='spots')
    reservation = db.relationship('Reservation', back_populates='spot', lazy='dynamic', cascade="all, delete-orphan")




class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    parking_in_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    parking_out_time = db.Column(db.DateTime)
    total_cost = db.Column(db.Float)
    duration_in_minutes = db.Column(db.Integer)
    status = db.Column(db.Enum(ReservationStatusEnum), default=ReservationStatusEnum.ACTIVE, nullable=False, native_enum=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    vehicle_no = db.Column(db.String(20), nullable=False)
    
    user = db.relationship('User', back_populates='reservations')
    spot = db.relationship('ParkingSpot', back_populates='reservation')



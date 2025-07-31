from model.parking import ParkingLot, ParkingSpot, Reservation
from model.user import User
from model.enum import SpotEnum, ReservationStatusEnum
from app.extensions import db, cache
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask import render_template

class ParkingService:
    
    # USER SERVICES

    @cache.cached(timeout=600)
    def get_parking_history(self, user_id: int):
        try:
            return Reservation.query.filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            raise Exception("Database error: " + str(e))

    def release_spot(self, reservation_id: int, parking_out_time: datetime):
        print("inside, release_spot")
        reservation = Reservation.query.filter_by(id=reservation_id).first()
        if not reservation:
            raise Exception("Reservation not found")
        if reservation.status == ReservationStatusEnum.COMPLETED:
            raise Exception("Spot already released")
        reservation.parking_out_time = parking_out_time
        print("reservation.parking_in_time", reservation.parking_in_time)
        print("parking_out_time", parking_out_time)
        duration = (parking_out_time.replace(tzinfo=None) - reservation.parking_in_time).total_seconds() / 60
        print("duration in minutes", duration)
        reservation.duration_in_minutes = int(duration)
        lot = ParkingLot.query.get(reservation.spot.lot_id)
        reservation.total_cost = (lot.price_per_hour or 0) * (duration / 60)
        reservation.status = ReservationStatusEnum.COMPLETED
        reservation.spot.status = SpotEnum.AVAILABLE
        
        actual_available = ParkingSpot.query.filter_by(lot_id=lot.id, status=SpotEnum.AVAILABLE, is_active=True).count() + 1  # +1 because this spot is now available
        lot.available_spots = actual_available
        
        db.session.commit()
        
        cache.clear()
        cache.clear()
        
        return reservation

    def get_available_lots_by_location(self, location: str):
        lots = ParkingLot.query.filter(
            ParkingLot.prime_location_name.ilike(f"%{location}%"),
            ParkingLot.is_active == True
        ).all()
        return lots

    def book_spot(self, user_id: int, lot_id: int, vehicle_no: str):
        lot = ParkingLot.query.filter_by(id=lot_id, is_active=True).first()
        if not lot:
            raise Exception("Parking lot not found")
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status=SpotEnum.AVAILABLE, is_active=True).first()
        if not spot:
            raise Exception("No available spots")
        reservation = Reservation(
            user_id=user_id,
            spot=spot,
            vehicle_no=vehicle_no,
            parking_in_time=datetime.now(),
            status=ReservationStatusEnum.ACTIVE
        )
        spot.status = SpotEnum.OCCUPIED
        
        actual_available = ParkingSpot.query.filter_by(lot_id=lot_id, status=SpotEnum.AVAILABLE, is_active=True).count() - 1  # -1 because this spot is now occupied
        lot.available_spots = actual_available
        
        db.session.add(reservation)
        db.session.commit()
        
        cache.clear()
        cache.clear()
        
        return reservation

    # ADMIN SERVICES

    def get_spots_by_lot(self, lot_id: int):
        lot = ParkingLot.query.filter_by(id=lot_id).first()
        if not lot:
            raise Exception("Parking lot not found")
        return lot.spots

    def edit_parking_lot(self, lot_id: int, price_per_hour: float = None, available_spots: int = None):
        lot = ParkingLot.query.filter_by(id=lot_id).first()
        if not lot:
            raise Exception("Parking lot not found")
        if price_per_hour is not None:
            lot.price_per_hour = price_per_hour
        if available_spots is not None:
            current_spots = ParkingSpot.query.filter_by(lot_id=lot_id, is_active=True).count()
            diff = available_spots - current_spots
            if diff > 0:
                for _ in range(diff):
                    spot = ParkingSpot(
                        lot_id=lot.id,
                        status=SpotEnum.AVAILABLE,
                        is_active=True,
                        last_updated=datetime.now()
                    )
                    db.session.add(spot)
            elif diff < 0:
                removable = ParkingSpot.query.filter_by(lot_id=lot_id, status=SpotEnum.AVAILABLE, is_active=True).limit(-diff).all()
                if len(removable) < -diff:
                    raise Exception("Not enough available spots to remove")
                for spot in removable:
                    db.session.delete(spot)
            actual_available = ParkingSpot.query.filter_by(lot_id=lot_id, status=SpotEnum.AVAILABLE, is_active=True).count()
            lot.available_spots = actual_available

            
        db.session.commit()
        cache.clear()
        return lot

    def create_parking_lot(self, data):
        lot = ParkingLot(
            prime_location_name=data['prime_location_name'],
            address=data['address'],
            pincode=data.get('pincode'),
            price_per_hour=data['price_per_hour'],
            available_spots=data['available_spots'],
            is_active=True,
            created_by=data.get('created_by'),
            created_at=datetime.now()
        )
        db.session.add(lot)
        db.session.flush()  

        spots_created = 0
        for _ in range(data['available_spots']):
            spot = ParkingSpot(
                lot_id=lot.id,
                status=SpotEnum.AVAILABLE,
                is_active=True,
                last_updated=datetime.now()
            )
            db.session.add(spot)
            spots_created += 1

        lot.available_spots = spots_created
        db.session.commit()
        cache.clear()

        return lot
    
    def delete_parking_lot(self, lot_id: int):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            raise Exception("Lot not found")
        occupied = ParkingSpot.query.filter_by(lot_id=lot_id, status=SpotEnum.OCCUPIED).count()
        if occupied > 0:
            raise Exception("Cannot delete lot with occupied spots")
        db.session.delete(lot)
        db.session.commit()
        return True
    
    def get_lot_available_spots(self, lot_id):
        return ParkingSpot.query.filter_by(lot_id=lot_id, status=SpotEnum.AVAILABLE, is_active=True).count()

    def get_spot_details(self, spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            raise Exception("Spot not found")
        return spot
    

    def delete_parking_spot(self, spot_id: int):
        spot = ParkingSpot.query.filter_by(id=spot_id).first()
        if not spot:
            raise Exception("Spot not found")
        if spot.status == SpotEnum.OCCUPIED:
            raise Exception("Cannot delete occupied spot")
        
        lot_id = spot.lot_id
        db.session.delete(spot)

        lot = ParkingLot.query.get(lot_id)
        if lot:
            actual_available = ParkingSpot.query.filter_by(lot_id=lot_id, status=SpotEnum.AVAILABLE, is_active=True).count() - 1  # -1 because we're deleting one
            lot.available_spots = actual_available
        
        db.session.commit()

        cache.clear()
        return True

    def get_occupied_spots(self):
        return ParkingSpot.query.filter_by(status=SpotEnum.OCCUPIED).all()

    def search(self, location=None, user_id=None, parking_id=None):
        query = Reservation.query
        if location:
            query = query.join(Reservation.spot).join(ParkingSpot.lot).filter(ParkingLot.prime_location_name.ilike(f"%{location}%"))
        if user_id:
            query = query.filter(Reservation.user_id == user_id)
        if parking_id:
            query = query.filter(Reservation.spot_id == parking_id)
        return query.all()

    def get_registered_users(self):
        return User.query.all()
    
    @cache.cached(timeout=600)
    def get_all_lots(self):
        return ParkingLot.query.all()

    def get_admin_summary(self):
        lots = ParkingLot.query.all()
        lot_stats = []
        total_available = 0
        total_occupied = 0
        for lot in lots:
            bookings = Reservation.query.join(ParkingSpot).filter(ParkingSpot.lot_id == lot.id).all()
            revenue = sum(b.total_cost or 0 for b in bookings)
            available = lot.available_spots - len([b for b in bookings if not b.parking_out_time])
            occupied = lot.available_spots - available
            lot_stats.append({'name': lot.prime_location_name, 'revenue': revenue})
            total_available += available
            total_occupied += occupied
        return {
            'lots': lot_stats,
            'available': total_available,
            'occupied': total_occupied
        }
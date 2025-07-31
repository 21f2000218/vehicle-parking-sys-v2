from app.extensions import db
from model.user import User
from model.enum import RoleEnum, SpotEnum, ReservationStatusEnum
from model.parking import ParkingLot, ParkingSpot, Reservation
from datetime import datetime, timedelta

from app.extensions import db
from model.user import User
from model.enum import RoleEnum, SpotEnum, ReservationStatusEnum
from model.parking import ParkingLot, ParkingSpot, Reservation
from datetime import datetime, timedelta
import random

def seed_dummy_data():
    db.session.query(Reservation).delete()
    db.session.query(ParkingSpot).delete()
    db.session.query(ParkingLot).delete()
    db.session.query(User).delete()
    db.session.commit()

    # 1 admin
    admin = User(
        username="admin1",
        email="21f2000218@ds.study.iitm.ac.in",
        license_no="ADMIN123",
        role=RoleEnum.ADMIN,
        password="adminpass"
    )
    db.session.add(admin)
    db.session.commit()

    # 4 users
    users = []
    user_data = [
        ("user1", "user1@example.com", "USER1LIC"),
        ("Nitesh", "nitesharya120@gmail.com", "USER2LIC"),
        ("Ishitha", "ishithaac2312@gmail.com", "USER3LIC"),
        ("Bindu", "201327052@student.hindustanuniv.ac.in", "USER4LIC"),
    ]
    for uname, email, lic in user_data:
        user = User(
            username=uname,
            email=email,
            license_no=lic,
            role=RoleEnum.USER,
            password="userpass"
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()

    # 5 lots
    lots = []
    lot_names = ["Central Mall", "Tech Park", "Dadar", "Chennai Tambaram", "Saidapet"]
    for i, name in enumerate(lot_names):
        lot = ParkingLot(
            prime_location_name=name,
            address=f"Address {i+1}",
            pincode=f"41100{i+1}",
            price_per_hour=20.0 + i * 5,
            available_spots=random.randint(4, 8),
            is_active=True,
            created_by=admin.id,
            created_at=datetime.now() - timedelta(days=365)
        )
        db.session.add(lot)
        lots.append(lot)
    db.session.flush()

    # Add spots to lots
    for lot in lots:
        for _ in range(5):
            spot = ParkingSpot(
                lot_id=lot.id,
                status=SpotEnum.AVAILABLE,
                is_active=True,
                last_updated=datetime.now()
            )
            db.session.add(spot)
    db.session.commit()

    # Add reservations spread across the year
    spots = ParkingSpot.query.all()
    for month in range(1, 13):
        for user in users:
            for _ in range(random.randint(2, 4)):  # 2-4 reservations per user per month
                spot = random.choice(spots)
                day = random.randint(1, 28)
                in_time = datetime(datetime.now().year, month, day, random.randint(8, 18))
                duration = random.randint(30, 180)
                out_time = in_time + timedelta(minutes=duration)
                cost = (spot.lot.price_per_hour or 20.0) * (duration / 60)
                status = random.choice([ReservationStatusEnum.COMPLETED, ReservationStatusEnum.ACTIVE])
                reservation = Reservation(
                    user_id=user.id,
                    spot_id=spot.id,
                    vehicle_no=f"MH12{random.randint(1000,9999)}",
                    parking_in_time=in_time,
                    parking_out_time=out_time if status == ReservationStatusEnum.COMPLETED else None,
                    duration_in_minutes=duration if status == ReservationStatusEnum.COMPLETED else None,
                    total_cost=cost if status == ReservationStatusEnum.COMPLETED else None,
                    status=status
                )
                db.session.add(reservation)
    db.session.commit()

    # --- FIX: Sync spot status with reservation status ---
    for spot in ParkingSpot.query.all():
        active_res = Reservation.query.filter_by(
            spot_id=spot.id,
            status=ReservationStatusEnum.ACTIVE
        ).first()
        if active_res:
            spot.status = SpotEnum.OCCUPIED
        else:
            spot.status = SpotEnum.AVAILABLE
    db.session.commit()


# Usage: Run this in Flask shell or as a CLI command with app context.

# Usage: Call seed_dummy_data() from a Flask shell or script with app context.
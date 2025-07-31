from app import celery
from app.extensions import db, mail
from model.user import User
from model.parking import Reservation, ParkingLot
from datetime import datetime, timedelta
from flask import render_template
from utils.notifications import send_email
import calendar
from flask import current_app

@celery.task()
def monthly_reports():
    with current_app.app_context():
        now = datetime.now()
        day1 = datetime(now.year, now.month, 1)
        last_month = day1 - timedelta(days=1)
        start = datetime(last_month.year, last_month.month, 1)
        end = datetime(last_month.year, last_month.month, calendar.monthrange(last_month.year, last_month.month)[1], 23, 59, 59)
        users = User.query.all()
        for user in users:
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parking_in_time >= start,
                Reservation.parking_in_time <= end
            ).all()
            total_bookings = len(reservations)
            spent = sum(reserv.total_cost or 0 for reserv in reservations)
            usage = {}
            for reserv in reservations:
                lot_id = reserv.spot.lot_id
                usage[lot_id] = usage.get(lot_id, 0) + 1
            most_used_lot = None
            if usage:
                most_used_lot_id = max(usage, key=usage.get)
                most_used_lot = ParkingLot.query.get(most_used_lot_id).prime_location_name
            html_content = render_template(
                "backend\\utils\\templates\\monthly_report.html",
                user=user,
                total_bookings=total_bookings,
                total_spent=spent,
                most_used_lot=most_used_lot,
                reservations=reservations,
                start=start,
                end=end
            )
            send_email(user.email, "Your Monthly Parking Activity Report", html_content)
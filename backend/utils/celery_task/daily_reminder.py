from app import celery
from app.extensions import db
from model.user import User
from model.parking import Reservation, ParkingLot
from datetime import datetime, date
from utils.notifications import send_email
from flask import current_app


@celery.task()
def daily_reminders():
    with current_app.app_context():
        today = date.today()
        users = User.query.all()
        print(users)
        for user in users:
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parking_in_time >= datetime(today.year, today.month, today.day)
                ).count() >0
            print(reservations)
            if not reservations:
                send_email(user.email, "Parking Reminder", "<p>This Mails are auto-generated from the application. If you want to unsubscribe click the link below <br><br> LOL! </p>")
        new_lots = ParkingLot.query.filter(
            ParkingLot.created_at >= datetime(today.year, today.month, today.day)
        ).all() 
        if new_lots:
            for user in users:
                send_email(user.email, "New Parking Lot Available", "<p>A new parking lot has been added. Check it out!</p>")

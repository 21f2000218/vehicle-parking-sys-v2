from app import celery
import csv
import io
from app.extensions import mail
from model.user import User
from model.parking import Reservation
from flask_mail import Message
from flask import current_app

@celery.task()
def export_user_csv(user_id):
    user = User.query.get(user_id)
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Reservation ID', 'Spot ID', 'Lot', 'In Time', 'Out Time', 'Cost', 'Status'])
    for r in reservations:
        writer.writerow([
            r.id,
            r.spot_id,
            r.spot.lot.prime_location_name,
            r.parking_in_time,
            r.parking_out_time,
            r.total_cost,
            r.status.value
        ])
    output.seek(0)
    print(user.email)
    with current_app.app_context():
        msg = Message("Your Parking History CSV", recipients=[user.email])
        msg.body = "Attached is your parking history in CSV format."
        msg.attach("parking_history.csv", "text/csv", output.read())
        mail.send(msg)
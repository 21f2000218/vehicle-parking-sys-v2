
import calendar
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required

from model.parking import Reservation
from model.user import User
from schemas.parking_schema import ParkingLotSchema, ReservationSchema
from schemas.user_schema import UserSchema
from services.parking_service import ParkingService
from utils.celery_task.export import export_user_csv
from utils.celery_task.daily_reminder import daily_reminders
from utils.celery_task.monthly_report import monthly_reports
parking_service = ParkingService()

user_parking_bp = Blueprint("parking_user", __name__, url_prefix='/parking')

@user_parking_bp.route('/user/history', methods=['GET'])
@jwt_required()
def user_history():
    print("Fetching user parking history")
    user_id = get_jwt_identity()
    try:
        print("User ID:", user_id)
        reservations = parking_service.get_parking_history(user_id)
        return jsonify(ReservationSchema(many=True).dump(reservations)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_parking_bp.route('/user/release/<int:reservation_id>', methods=['PUT'])
@jwt_required()
def user_release(reservation_id):
    data = request.get_json()
    try:
        parking_out_time = datetime.fromisoformat(data['parking_out_time'])
        reservation = parking_service.release_spot(reservation_id, parking_out_time)
        return jsonify(ReservationSchema().dump(reservation)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_parking_bp.route('/user/available-lots', methods=['GET'])
@jwt_required()
def user_available_lots():
    location = request.args.get('location', '')
    try:
        lots = parking_service.get_available_lots_by_location(location)
        result = []
        for lot in lots:
            lot_data = ParkingLotSchema().dump(lot)
            lot_data['available_spots'] = parking_service.get_lot_available_spots(lot.id)
            result.append(lot_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_parking_bp.route('/user/book', methods=['POST'])
@jwt_required()
def user_book():
    data = request.get_json()
    user_id = get_jwt_identity()
    try:
        reservation = parking_service.book_spot(
            user_id=user_id,
            lot_id=data['lot_id'],
            vehicle_no=data['vehicle_no']
        )
        return jsonify(ReservationSchema().dump(reservation)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_parking_bp.route('/me', methods=['GET'])
@jwt_required()
def view_own_details():
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(UserSchema().dump(user)), 200

@user_parking_bp.route('/user/export-csv', methods=['POST'])
@jwt_required()
def export_csv():
    user_id = get_jwt_identity()
    export_user_csv.delay(user_id)
    return jsonify({"msg": "Export started. You will be notified when ready."}), 202

@user_parking_bp.route('/user/daily-reminder', methods=['POST'])
@jwt_required()
def reminders():
    user_id = get_jwt_identity()
    daily_reminders.delay()
    monthly_reports.delay()
    return jsonify({"msg": "You will be notified when ready."}), 202


@user_parking_bp.route('/user/monthly-summary', methods=['GET'])
@jwt_required()
def user_monthly_summary():
    user_id = get_jwt_identity()
    
    now = datetime.now()
    months = [calendar.month_abbr[m] for m in range(1, 13)]
    bookings = [0]*12
    spent = [0]*12
    lot_usage = {}
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    for r in reservations:
        m = r.parking_in_time.month - 1
        bookings[m] += 1
        spent[m] += r.total_cost or 0
        lot = r.spot.lot.prime_location_name
        lot_usage[lot] = lot_usage.get(lot, 0) + 1
    lots = [{'name': k, 'count': v} for k, v in lot_usage.items()]
    return jsonify({
        'months': months,
        'bookings': bookings,
        'spent': spent,
        'lots': lots
    })

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.parking import Reservation
from model.user import User
from utils.auth import has_role
from services.parking_service import ParkingService
from schemas.parking_schema import ParkingLotSchema, ParkingSpotSchema, ReservationSchema
from schemas.user_schema import UserSchema
from datetime import datetime
from app.extensions import db
from utils.celery_task.export import export_user_csv
from datetime import datetime
import calendar

admin_parking_bp = Blueprint("parking", __name__, url_prefix='/parking')
service = ParkingService()

@admin_parking_bp.route('/admin/spots/<int:lot_id>', methods=['GET'])
@jwt_required()
@has_role('admin')
def admin_spots(lot_id):
    try:
        spots = service.get_spots_by_lot(lot_id)
        return jsonify(ParkingSpotSchema(many=True).dump(spots)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_parking_bp.route('/admin/parking-lot/<int:lot_id>', methods=['PUT'])
@jwt_required()
@has_role('admin')
def admin_edit_lot(lot_id):
    data = request.get_json()
    try:
        lot = service.edit_parking_lot(
            lot_id,
            price_per_hour=data.get('price_per_hour'),
            available_spots=data.get('available_spots')
        )
        return jsonify(ParkingLotSchema().dump(lot)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_parking_bp.route('/admin/parking-lot', methods=['POST'])
@jwt_required()
@has_role('admin')
def admin_create_lot():
    data = request.get_json()
    try:
        data['created_by'] = get_jwt_identity()
        lot = service.create_parking_lot(data)
        return jsonify(ParkingLotSchema().dump(lot)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_parking_bp.route('/admin/parking-lot/<int:lot_id>', methods=['DELETE'])
@jwt_required()
@has_role('admin')
def admin_delete_lot(lot_id):
    try:
        service.delete_parking_lot(lot_id)
        return jsonify({'msg': 'Lot deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_parking_bp.route('/admin/spot/<int:spot_id>', methods=['DELETE'])
@jwt_required()
@has_role('admin')
def admin_delete_spot(spot_id):
    try:
        service.delete_parking_spot(spot_id)
        return jsonify({'msg': 'Spot deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_parking_bp.route('/admin/occupied-spots', methods=['GET'])
@jwt_required()
@has_role('admin')
def admin_occupied_spots():
    try:
        spots = service.get_occupied_spots()
        return jsonify(ParkingSpotSchema(many=True).dump(spots)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_parking_bp.route('/admin/search', methods=['GET'])
@jwt_required()
@has_role('admin')
def admin_search():
    location = request.args.get('location')
    user_id = request.args.get('user_id')
    parking_id = request.args.get('parking_id')
    try:
        reservations = service.search(location, user_id, parking_id)
        return jsonify(ReservationSchema(many=True).dump(reservations)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_parking_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@has_role('admin')
def admin_users():
    try:
        users = service.get_registered_users()
        return jsonify(UserSchema(many=True).dump(users)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@admin_parking_bp.route('/spot/<int:spot_id>', methods=['GET'])
@jwt_required()
def spot_details(spot_id):
    try:
        spot = service.get_spot_details(spot_id)
        return jsonify(ParkingSpotSchema().dump(spot)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    
@admin_parking_bp.route('/admin/parking-lots', methods=['GET'])
@jwt_required()
@has_role('admin')
def admin_list_lots():
    lots = service.get_all_lots()
    result = []
    for lot in lots:
        lot_data = ParkingLotSchema().dump(lot)
        lot_data['available_spots'] = service.get_lot_available_spots(lot.id)
        result.append(lot_data)
    return jsonify(result), 200
    
@admin_parking_bp.route('/me', methods=['POST'])
@jwt_required()
def edit_own_details():
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    for field in ['username', 'email', 'license_no']:
        if field in data:
            setattr(user, field, data[field])
    if 'password' in data:
        user.password = data['password']
    user.updated_at = datetime.now()
    db.session.commit()
    return jsonify(UserSchema().dump(user)), 200

@admin_parking_bp.route('/summary', methods=['GET'])
@jwt_required()
@has_role('admin')
def admin_summary():
    data = service.get_admin_summary()
    return jsonify(data)
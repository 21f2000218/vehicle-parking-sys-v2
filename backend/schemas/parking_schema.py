from marshmallow import Schema, fields, post_load, pre_dump, validate

from model.parking import ParkingLot, Reservation


class ParkingLotSchema(Schema):
    id = fields.Int(dump_only=True)
    prime_location_name = fields.Str(required=True, validate=validate.Length(min=1))
    address = fields.Str(required=True, validate=validate.Length(min=1))
    pincode = fields.Str(validate=validate.Length(equal=6))
    price_per_hour = fields.Float(required=True, validate=validate.Range(min=0))
    available_spots = fields.Int(required=True, validate=validate.Range(min=1))
    is_active = fields.Bool()
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_parking_lot(self, data, **kwargs):
        return ParkingLot(**data)
    

    
class ParkingSpotSchema(Schema):
    id = fields.Int(dump_only=True)
    lot_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(["AVAILABLE", "OCCUPIED"]))
    remarks = fields.Str()
    last_updated = fields.DateTime(dump_only=True)
    is_active = fields.Bool()
    
    @pre_dump
    def serialize_enum(self, obj, **kwargs):
        obj.status = obj.status.value if hasattr(obj.status, "value") else obj.status
        return obj

class ReservationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    spot_id = fields.Int(required=True)
    vehicle_no = fields.Str(required=True, validate=validate.Length(min=1))
    parking_in_time = fields.DateTime(dump_only=True)
    parking_out_time = fields.DateTime(allow_none=True)
    total_cost = fields.Float(dump_only=True)
    status = fields.Str(validate=validate.OneOf(["ACTIVE", "RELEASED"]))

    @pre_dump
    def serialize_enum(self, obj, **kwargs):
        obj.status = obj.status.value if hasattr(obj.status, "value") else obj.status
        return obj

    @post_load
    def make_reservation(self, data, **kwargs):
        return Reservation(**data)

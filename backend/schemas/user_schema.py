
from marshmallow import Schema, ValidationError, fields, pre_load, validate, validates

from model.enum import RoleEnum
from model.user import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.And(
        validate.Length(min=3, max=80),
        validate.Regexp(r"^[A-Za-z0-9_.-]+$", error="Username must contain only letters, numbers and ./_/- characters")))
    email = fields.Email(required=True)
    license_no = fields.String(required=True)
    role = fields.String(required=True, validate=validate.OneOf([r.value for r in RoleEnum]))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)
    
    @validates("username")
    def validate_username_unique(self, value, **kwargs):
        if User.query.filter_by(username=value).first():
            raise ValidationError("Username already exists")

    @validates("email")
    def validate_email_unique(self, value, **kwargs):
        if User.query.filter_by(email=value).first():
            raise ValidationError("Email already exists")

    @validates("license_no")
    def validate_license_unique(self, value, **kwargs):
        if User.query.filter_by(license_no=value).first():
            raise ValidationError("License number already exists")
        
    @pre_load
    def normalize_role(self, data, **kwargs):
        if "role" in data:
            data["role"] = data["role"].strip().lower()
        return data

    @validates("role")
    def ensure_valid_role(self, value, **kwargs):
        if value not in {m.value for m in RoleEnum}:
            raise ValidationError(f"Role must be one of {[m.value for m in RoleEnum]}")

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class TokenRefreshSchema(Schema):
    refresh = fields.Str(required=True)


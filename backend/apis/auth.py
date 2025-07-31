from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jti, get_jwt, jwt_required, get_jwt_identity, create_access_token, create_refresh_token, unset_jwt_cookies
from model.user import User
from services.auth_service import AuthService
from schemas.user_schema import UserSchema, LoginSchema

auth = Blueprint("auth", __name__, url_prefix='/auth')
user_schema = UserSchema()
login_schema = LoginSchema()

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    user = AuthService.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        license_no=data['license_no'],
        role=data['role']
    )
    return jsonify(user_schema.dump(user)), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    user = AuthService.authenticate(data['username'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    AuthService.store_token(get_jti(access), user.id, 'access')
    AuthService.store_token(get_jti(refresh), user.id, 'refresh')

    return jsonify({'access_token': access, 'refresh_token': refresh}), 200

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    user = User.query.get(identity)
    AuthService.store_token(get_jti(access_token), user.id, 'access')
    return jsonify(access_token=access_token), 200

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    user_id = get_jwt_identity()
    AuthService.revoke_token(jti, user_id)
    response = jsonify({'msg': 'Logged out'})
    unset_jwt_cookies(response)
    return response, 200

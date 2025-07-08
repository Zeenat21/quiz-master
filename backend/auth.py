from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User, Role

from datetime import timedelta,datetime

auth_bp = Blueprint('auth', __name__)

# Helper: Role checker
def has_role(user, role_name):
    return any(role.name == role_name for role in user.roles)

# User Registration Route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    qualification = data.get('qualification')
    dob_str = data.get('dob')
    # dob = dob.date() if dob else None
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)

    user = User(
        email=email,
        password=hashed_password,
        full_name=full_name,
        qualification=qualification,
        dob=dob
    )

    # Assign default "user" role
    user_role = Role.query.filter_by(name="user").first()
    if not user_role:
        user_role = Role(name="user", description="Standard User Role")
        db.session.add(user_role)
        db.session.commit()

    user.roles.append(user_role)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Login Route (both Admin and User)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    roles = [role.name for role in user.roles]

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": roles},
        expires_delta=timedelta(days=1)
    )


    return jsonify({
        'access_token': access_token,
        'roles': roles,
        'email':user.email,
        'full_name': user.full_name
    }), 200

# Optional: Check current token and user
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    claims = get_jwt()
    user = User.query.get(user_id)

    return jsonify({
        'id': user.id,
        'email': user.email,
        'roles': claims['roles'],
        'full_name': user.full_name
    })

##Log out!
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        user.last_seen = datetime.utcnow()
        db.session.commit()

    return jsonify({'msg': 'Logged out and last_seen updated'}), 200

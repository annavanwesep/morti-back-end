from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity 


from app.models.user import User
from app.models.message import Message

trust_bp = Blueprint('trust', __name__, url_prefix="/trust")

@trust_bp.route("", methods=['POST'])
@jwt_required()
def add_trusted_user(user_id):
    try:
        trusted_user = User.query.get(user_id)
        if not trusted_user:
            return jsonify({'error': 'User not found'}), 404

        current_user = get_current_user()  # Implement a function to get the current logged-in user

        if current_user == trusted_user:
            return jsonify({'error': 'You cannot trust yourself'}), 400

        current_user.trusted_users.append(trusted_user)
        db.session.commit()

        return jsonify({'message': f'You now trust {trusted_user.username}'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred'}), 500
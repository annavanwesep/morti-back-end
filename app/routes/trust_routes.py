from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity 


from app.models.user import User
from app.models.message import Message

trust_bp = Blueprint('trust', __name__, url_prefix="/trust")

#As a signed in user, add a person who you trust by email 
@trust_bp.route("", methods=['POST'])
@jwt_required()
def add_trusted_user():
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        print("ERROR", str(e))
        return {"error": "An error ocurred when retriveing current user"}, 404

    request_body = request.get_json()

    if "email" not in request_body:
        return {"error": "All fields are required"}, 400
    trusted_user = User.query.filter_by(email=request_body["email"]).first()
    if not trusted_user:
        return {"error": "User not found"}, 404
    
    current_user.trusted_users.append(trusted_user)
    db.session.commit()
    return jsonify({'message': f'You now trust {trusted_user.first_name}'}), 201

#Get all the people the current user trusts 
@trust_bp.route("/trustees", methods=["GET"])
@jwt_required()
def get_all_trusted_people():
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        print("ERROR", str(e))
        return {"error": "An error ocurred when retriveing current user"}, 404
    
    trusted_people = current_user.trusted_users.all()

    trusted_people_response = []
    for user in trusted_people :
        trusted_people_response.append({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email})
    return jsonify(trusted_people_response), 200

#Get all the people who trust the current user
@trust_bp.route("/trusted_by", methods=['GET'])
@jwt_required()
def get_users_trusting_current_user():
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        return {"error": "An error occurred while retrieving current user"}, 404

    users_trusting_current_user = User.query.filter(User.trusted_users.contains(current_user)).all()

    trusted_by_response = []
    for user in users_trusting_current_user :
        trusted_by_response.append(
            {"first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email}
        )
    return jsonify(trusted_by_response), 200

#Untrust a user
@trust_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_trusted_user(id):
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        return {"error": "An error occurred while retrieving current user"}, 404
    
    user_to_untrust = User.query.get(id)
    if user_to_untrust is None:
        return {"error": "User not found"}, 404

    current_user.trusted_users.remove(user_to_untrust)
    db.session.commit()
    return jsonify({'message': f'You have removed {user_to_untrust.first_name} from trusted users'}), 200
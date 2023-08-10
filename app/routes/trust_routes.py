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
@trust_bp.route("", methods=["GET"])
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
    for person in trusted_people :
        trusted_people_response.append(
            {"first_name": person.first_name,
            "last_name": person.last_name,
            "email": person.email}
        )
    return jsonify(trusted_people_response), 200
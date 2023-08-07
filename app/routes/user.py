from flask import Blueprint, request, jsonify, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, get_jwt, get_jwt_identity 
from datetime import datetime, timedelta, timezone
from app.models.user import User
from app import db

# No url prefix for register/login users 
user_bp = Blueprint("users", __name__)

bcrypt = Bcrypt()

@user_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_one_user(email):
    user_to_delete = get_valid_item_by_id(User, email)

    db.session.delete(user_to_delete)
    db.session.commit()

    return f"User {user_to_delete.message} is deleted!", 200

# CREATE A NEW USER
@user_bp.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    #saving hashed password to database, cannot pass in password directly from user using from_dict method
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "msg": "Account sucessfully created"
    }), 201
    



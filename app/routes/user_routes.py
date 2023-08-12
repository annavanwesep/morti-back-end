from flask import Blueprint, request, jsonify, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required, get_jwt, get_jwt_identity 
from datetime import datetime, timedelta, timezone
from app.models.user import User
from app.routes.helper_routes import get_valid_item_by_id
from app import db

# No url prefix for register/login users 
user_bp = Blueprint("users", __name__)

bcrypt = Bcrypt()

@user_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(days=10))
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

@user_bp.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"msg": "Wrong email or password"}, 401
        
    access_token = create_access_token(identity=email)
    return {'access_token':access_token}
    

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

#Register using email and password
@user_bp.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401 
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "id": user.id,
        "email": user.email
    }), 200

#To logout a user and revoke token 
@user_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg":"logout successful"})
    unset_jwt_cookies(response)
    return response

@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def my_profile():
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        print("ERROR", str(e))
        return {"error": "An error ocurred when retriveing current user"}, 404

    response_body= {
        "about": f"Hello {current_user.first_name}! Send Farewells",
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name
    }
    return jsonify(response_body), 200

#GET ALL USERS/DEBUGGING
@user_bp.route("/users", methods=['GET'])
def handle_users():
    user_query = request.args.get("users")
    if user_query:
        users = User.query.filter_by(user=user_query)
    else:
        users = User.query.all()

    all_users_response = []
    for user in users :
        all_users_response.append(user.to_dict())
    return jsonify(all_users_response), 200


#GET A SINGLE USER/DEBUGGING
@user_bp.route("/users/<id>", methods=['GET'])
def user(id):
    board = get_valid_item_by_id(User, id)
    return board.to_dict(), 200

#Clarify the purpose of this route
#Mark suggested using user here instead of id(?)
@user_bp.route("/", methods=['GET']) 
def get():
    #get token from the request header
    #decode the token 
    #verify the hash
    #if invalid, return 5xx
    #if valid, get user email from decoded token
    #id = decodedtoken.email
    
    user = get_valid_item_by_id(User, id)

    return user.to_dict(), 200

#Research how to delelte logged in user, delete account and messages?
@user_bp.route("/<id>", methods=["DELETE"])
def delete(id):
    user = get_valid_item_by_id(User, id)
    db.session.delete(user)
    db.session.commit()

    return f"{user.first_name} is deleted!", 200

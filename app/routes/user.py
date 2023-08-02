from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect, asc
from app.models.message import Message
from app import db
from app.routes.routes_helper import get_valid_item_by_id
from app.models.user import User

# All routes defined with user_bp start with url_prefix (/users)
user_bp = Blueprint("users", __name__, url_prefix="/users")

#get single user
@user_bp.route("/<id>", methods=['GET'])
def user(id):
    board = get_valid_item_by_id(User, id)
    return board.to_dict(), 200

@user_bp.route("", methods=['GET']) #Mark suggested using user here instead of id
def get():
    #get token from the request header
    #decode the token 
    #verify the hash
    #if invalid, return 5xx
    #if valid, get user email from decoded token
    #id = decodedtoken.email
    
    user = get_valid_item_by_id(User, id)

    return user.to_dict(), 200

@user_bp.route("/<id>", methods=["DELETE"])
def delete(id):
    user = get_valid_item_by_id(User, id)
    db.session.delete(user)
    db.session.commit()

    return f"{user.first_name} is deleted!", 200

# CREATE A NEW USER
@user_bp.route("", methods=['POST'])
def create():
    request_body = request.get_json()
    user = User.from_dict(request_body)
    db.session.add(user)
    db.session.commit()

    # Give back our response
    return {
        "id": user.id,
        "email": user.email,
        "msg": "Successfully created"
    }, 201
    



from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect, asc
from app.models.message import Message
from app import db
from app.routes.routes_helper import get_valid_item_by_id
from app.models.user import User

# All routes defined with user_bp start with url_prefix (/users)
user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_one_user(email):
    user_to_delete = get_valid_item_by_id(User, email)

    db.session.delete(user_to_delete)
    db.session.commit()

    return f"User {user_to_delete.message} is deleted!", 200

# CREATE A NEW USER
user_bp.route("", methods=['POST'])
def create_new_user():
    request_body = request.get_json()
    new_user = User.from_dict(request_body)

    db.session.add(new_user)
    db.session.commit()

    # Give back our response
    return {
        "id": new_user.user_id,
        "email": new_user.email,
        "msg": "Successfully created"
    }, 201
    



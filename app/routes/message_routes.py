from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity 
from datetime import datetime, timedelta, timezone

from app.models.user import User
from app.models.message import Message

messages_bp = Blueprint("farewell messages", __name__, url_prefix="/farewell_messages")

# CREATE A NEW FAREWELL MESSAGE
@messages_bp.route("", methods=['POST'])
@jwt_required()
def create_farewell_message():
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        print("ERROR", str(e))
        return {"Error": "An error ocurred when retriveing current user"}
    request_body = request.get_json()
    
    if "title" not in request_body or "text_message" not in request_body or "audio_message" not in request_body or "recipient_email" not in request_body:
        return {"error": "All fields are required"}, 400 
    
    recipient_email = request_body["recipient_email"]
    recipient = User.query.filter_by(email=recipient_email).first()
    try:
        new_message = Message(
        title=request_body["title"],
        text_message=request_body["text_message"],
        audio_message=request_body["audio_message"],
        recipient_email=recipient.email,
        recipient_id=recipient.id,
        user_id=current_user.id
    )
    except Exception as e:
        print("Error:", str(e))
        return {"error": "An error occurred while creating the message"}, 500

    db.session.add(new_message)
    db.session.commit()

    # Give back our response
    return {
        "id": new_message.id,
        "title": new_message.title,
        "text_message": new_message.text_message,
        "audio_message": new_message.audio_message,
        "recipient_email": new_message.recipient_email,
        "recipient_id": new_message.recipient_id,
        "user_id": new_message.user_id,
        "msg": "Successfully created"
    }, 201

#Get all messages that the current signed in user has created 
@messages_bp.route("", methods=['GET'])
@jwt_required()
def handle_farewell_messages():
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        print("ERROR", str(e))
        return {"Error": "An error ocurred when retriveing current user"}
    
    messages = Message.query.filter_by(user_id=current_user.id)
    
    farewell_messages_response = []
    for message in messages :
        farewell_messages_response.append(message.to_dict())
    return jsonify(farewell_messages_response), 200

#Mark selected message by id as IS_SENT to TRUE
#AS IS, THIS ROUTE MARKS YOUR **OWN** MESSAGES TO BE SENT, INSTEAD OF YOUR TRUSTED PERSON 
# NOT CORRECT YET: NEED SELF REFERENTIAL TABLE TO LINK USERS 
@messages_bp.route("/<id>/is_deceased", methods=["PATCH"])
@jwt_required()
def patch_messages(id):
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        print("ERROR", str(e))
        return {"Error": "An error ocurred when retriveing current user"}
    
    message_to_update = Message.query.filter_by(user_id=current_user.id, id=id).first()
    print("Query message:", message_to_update)
    
    if message_to_update is None:
        return {"Error": "Message not found"}, 404
    
    try:
        message_to_update.is_sent = True
        db.session.commit()
        return f"Message {id} has been updated!", 200
    except Exception as e:
        print("ERROR", str(e))
        db.session.rollback()
        return {"Error": "An error occurred while updating the message"}, 500

    
# DELETE ONE FAREWELL MESSAGE
@messages_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_one_message(id):
    current_user_email = get_jwt_identity()
    try:
        current_user = User.query.filter_by(email=current_user_email).first()
    except Exception as e:
        print("ERROR", str(e))
        return {"Error": "An error ocurred when retriveing current user"}
    
    message_to_delete = Message.query.filter_by(user_id=current_user.id, id=id).first()
    print("Query message:", message_to_delete)
    
    if message_to_delete is None:
        return {"Error": "Message not found"}, 404

    try:
        db.session.delete(message_to_delete)
        db.session.commit()
        return f"Message {id} is deleted!", 200
    except Exception as e:
        print("ERROR", str(e))
        db.session.rollback()
        return {"Error": "An error occurred while deleting the message"}, 500


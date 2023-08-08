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

# #Get all farewell messages created by the current signed in user
# @messages_bp.route("", methods=['GET'])
# @jwt_required(optional=True)
# def handle_farewell_messages():
#     message_query = request.args.get("messages")
#     if message_query:
#         messages = Message.query.filter_by(message=message_query)
#     else:
#         messages = Message.query.all()

#     farewell_messages_response = []
#     for message in messages :
#         farewell_messages_response.append(message.to_dict())
#     return jsonify(farewell_messages_response), 200

#Get all messages from the current signed in user 
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

    

# DELETE ONE FAREWELL MESSAGE
@messages_bp.route("/<message_id>/delete", methods=["DELETE"])
def delete_one_message(message_id):
    message_to_delete = get_valid_item_by_id(Message, message_id)

    db.session.delete(message_to_delete)
    db.session.commit()

    return f"Message {message_to_delete} is deleted!", 200


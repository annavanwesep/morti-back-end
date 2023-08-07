from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from sqlalchemy import inspect, asc

from app.models.user import User
from app.models.message import Message
from app.routes.routes_helper import get_valid_item_by_id

farewell_messages_bp = Blueprint("farewell messages", __name__, url_prefix="/farewell_messages")

farewell_messages_bp = Blueprint("farewell messages", __name__, url_prefix="/farewell_messages")
#get  all farewell messages
@farewell_messages_bp.route("", methods=['GET'])
def handle_farewell_messages():
    message_query = request.args.get("messages")
    if message_query:
        messages = Message.query.filter_by(message=message_query)
    else:
        messages = Message.query.all()

    farewell_messages_response = []
    for message in messages :
        farewell_messages_response.append(message.to_dict())
    return jsonify(farewell_messages_response), 200

#GET A SINGLE MESSAGE
@farewell_messages_bp.route("/<message_id>", methods=['GET'])
def get_one_message(message_id):
    message = get_valid_item_by_id(Message, message_id)
    return message.to_dict(), 200

# CREATE A NEW FAREWELL MESSAGE
@farewell_messages_bp.route("", methods=['POST'])
def create_farewell_message():
    request_body = request.get_json()
    new_message = Message.from_dict(request_body)

    db.session.add(new_message)
    db.session.commit()

    # Give back our response
    return {
        "id": new_message.id,
        "text_message": new_message.text_message,
        "audio_message": new_message.audio_message,
        "id_recipient": new_message.id_recipient,
        "recipient_email": new_message.recipient_email,
        "msg": "Successfully created"
    }, 201
    

# DELETE ONE FAREWELL MESSAGE
@farewell_messages_bp.route("/<message_id>/delete", methods=["DELETE"])
def delete_one_message(message_id):
    message_to_delete = get_valid_item_by_id(Message, message_id)

    db.session.delete(message_to_delete)
    db.session.commit()

    return f"Message {message_to_delete} is deleted!", 200

#MARK ALL MESSAGES AS IS_SENT TO TRUE PATCH
@farewell_messages_bp.route("/<message_id>/is_deceased", methods=["PATCH"])
def patch_messages(message_id):
    message_to_update = get_valid_item_by_id(Message, message_id)
    
    # update card likes count to increment by 1.
    message_to_update.is_sent = True
    db.session.commit()
    return message_to_update.to_dict(), 200
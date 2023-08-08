from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from sqlalchemy import inspect, asc

from app.models.user import User
from app.models.message import Message
from app.routes.routes_helper import get_valid_item_by_id

messages_bp = Blueprint("farewell messages", __name__, url_prefix="/farewell_messages")
#get  all farewell messages
@messages_bp.route("", methods=['GET'])
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

#get single message
@messages_bp.route("/<message_id>", methods=['GET'])
def get_one_message(message_id):
    message = get_valid_item_by_id(Message, message_id)
    return message.to_dict(), 200

    

# DELETE ONE FAREWELL MESSAGE
@messages_bp.route("/<message_id>/delete", methods=["DELETE"])
def delete_one_message(message_id):
    message_to_delete = get_valid_item_by_id(Message, message_id)

    db.session.delete(message_to_delete)
    db.session.commit()

    return f"Message {message_to_delete} is deleted!", 200


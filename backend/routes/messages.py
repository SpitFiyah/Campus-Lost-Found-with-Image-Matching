from flask import Blueprint, g, jsonify, request
from backend.extensions import db
from backend.models.item import Item
from backend.models.message import Message
from backend.services.notification_service import create_notification
from backend.utils.auth import login_required

messages_bp = Blueprint("messages", __name__, url_prefix="/api/messages")


@messages_bp.get("")
@login_required
def list_messages():
    messages = db.session.scalars(db.select(Message).where((Message.sender_id == g.current_user.id) | (Message.receiver_id == g.current_user.id)).order_by(Message.created_at.asc())).all()
    return jsonify({"success": True, "data": {"messages": [message.to_dict() for message in messages]}, "message": "Messages loaded."})


@messages_bp.post("")
@login_required
def send_message():
    data = request.get_json(silent=True) or {}
    text = str(data.get("message", "")).strip()
    receiver_id = data.get("receiver_id")
    if not text or len(text) > 2000 or not receiver_id:
        return jsonify({"success": False, "error": {"code": "INVALID_MESSAGE", "message": "Receiver and a message of 1-2000 characters are required."}}), 400
    item = db.session.get(Item, data.get("item_id")) if data.get("item_id") else None
    if item and item.user_id != g.current_user.id and receiver_id != item.user_id:
        return jsonify({"success": False, "error": {"code": "FORBIDDEN", "message": "Message must be associated with an accessible item."}}), 403
    message = Message(sender_id=g.current_user.id, receiver_id=receiver_id, item_id=item.id if item else None, message=text)
    db.session.add(message)
    create_notification(receiver_id, "New message", f"You received a message from {g.current_user.name}.", "NEW_MESSAGE", item.id if item else None)
    db.session.commit()
    return jsonify({"success": True, "data": {"message": message.to_dict()}, "message": "Message sent."}), 201

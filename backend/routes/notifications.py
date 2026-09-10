from flask import Blueprint, g, jsonify
from backend.extensions import db
from backend.models.notification import Notification
from backend.utils.auth import login_required

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")


@notifications_bp.get("")
@login_required
def list_notifications():
    notifications = db.session.scalars(db.select(Notification).where(Notification.user_id == g.current_user.id).order_by(Notification.created_at.desc())).all()
    return jsonify({"success": True, "data": {"notifications": [item.to_dict() for item in notifications], "unread_count": sum(not item.is_read for item in notifications)}, "message": "Notifications loaded."})


@notifications_bp.put("/<int:notification_id>/read")
@login_required
def mark_read(notification_id):
    item = db.session.get(Notification, notification_id)
    if not item or item.user_id != g.current_user.id:
        return jsonify({"success": False, "error": {"code": "NOT_FOUND", "message": "Notification not found."}}), 404
    item.is_read = True
    db.session.commit()
    return jsonify({"success": True, "data": {"notification": item.to_dict()}, "message": "Notification marked read."})

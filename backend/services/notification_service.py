from backend.extensions import db
from backend.models.notification import Notification


def create_notification(user_id, title, message, notification_type="GENERAL", item_id=None, match_id=None):
    notification = Notification(user_id=user_id, type=notification_type, title=title, message=message, related_item_id=item_id, related_match_id=match_id)
    db.session.add(notification)
    return notification

from datetime import datetime, timezone
from backend.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    related_item_id = db.Column(db.Integer, db.ForeignKey("items.id", ondelete="SET NULL"))
    related_match_id = db.Column(db.Integer, db.ForeignKey("matches.id", ondelete="SET NULL"))
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {"id": self.id, "type": self.type, "title": self.title, "message": self.message, "related_item_id": self.related_item_id, "related_match_id": self.related_match_id, "is_read": self.is_read, "created_at": self.created_at.isoformat()}

from datetime import datetime, timezone
from backend.extensions import db


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id", ondelete="SET NULL"))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])
    item = db.relationship("Item")

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "sender_name": self.sender.name if self.sender else None,
            "receiver_id": self.receiver_id,
            "receiver_name": self.receiver.name if self.receiver else None,
            "item_id": self.item_id,
            "item_name": self.item.name if self.item else None,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat(),
        }

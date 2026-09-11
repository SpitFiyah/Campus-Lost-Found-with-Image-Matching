from datetime import datetime, timezone

from backend.extensions import db


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    reason = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable=False, default="PENDING", index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    reporter = db.relationship("User")
    item = db.relationship("Item")

    def to_dict(self):
        return {
            "id": self.id,
            "reporter_id": self.reporter_id,
            "reporter_name": self.reporter.name if self.reporter else None,
            "item_id": self.item_id,
            "item_name": self.item.name if self.item else None,
            "reason": self.reason,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

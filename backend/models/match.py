from datetime import datetime, timezone
from backend.extensions import db


class Match(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lost_item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    found_item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    image_similarity = db.Column(db.Float, nullable=False)
    location_score = db.Column(db.Float, nullable=False)
    category_score = db.Column(db.Float, nullable=False)
    color_score = db.Column(db.Float, nullable=False)
    date_score = db.Column(db.Float, nullable=False)
    final_score = db.Column(db.Float, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="PENDING", index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    lost_item = db.relationship("Item", foreign_keys=[lost_item_id])
    found_item = db.relationship("Item", foreign_keys=[found_item_id])

    def to_dict(self):
        return {"id": self.id, "lost_item": self.lost_item.to_dict(), "found_item": self.found_item.to_dict(), "image_similarity": self.image_similarity, "location_score": self.location_score, "category_score": self.category_score, "color_score": self.color_score, "date_score": self.date_score, "final_score": self.final_score, "status": self.status, "created_at": self.created_at.isoformat()}

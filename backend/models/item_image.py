from datetime import datetime, timezone

from backend.extensions import db


class ItemImage(db.Model):
    __tablename__ = "item_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True)
    image_path = db.Column(db.String(500), nullable=False)
    embedding_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    item = db.relationship("Item", back_populates="images")

    def to_dict(self):
        return {"id": self.id, "image_path": self.image_path, "created_at": self.created_at.isoformat() if self.created_at else None}

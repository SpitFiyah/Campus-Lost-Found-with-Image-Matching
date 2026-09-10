from datetime import datetime, timezone

from backend.extensions import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    type = db.Column(db.String(10), nullable=False, index=True)
    name = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(80))
    location = db.Column(db.String(100), nullable=False, index=True)
    date_lost_found = db.Column(db.Date, nullable=False, index=True)
    time_lost_found = db.Column(db.Time)
    status = db.Column(db.String(20), nullable=False, default="ACTIVE", index=True)
    private_verification_answer = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    images = db.relationship("ItemImage", back_populates="item", cascade="all, delete-orphan")

    def to_dict(self, include_private=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "color": self.color,
            "location": self.location,
            "date_lost_found": self.date_lost_found.isoformat(),
            "time_lost_found": self.time_lost_found.isoformat() if self.time_lost_found else None,
            "status": self.status,
            "images": [image.to_dict() for image in self.images],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_private:
            data["private_verification_answer"] = self.private_verification_answer
        return data

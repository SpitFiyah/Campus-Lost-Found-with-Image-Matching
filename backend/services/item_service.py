from datetime import date, time

from sqlalchemy import func

from backend.extensions import db
from backend.models.item import Item
from backend.models.item_image import ItemImage
from backend.utils.file_utils import save_validated_image


ALLOWED_TYPES = {"LOST", "FOUND"}
ALLOWED_STATUSES = {"ACTIVE", "MATCHED", "RETURNED", "CLOSED", "REMOVED"}
LOCATIONS = {"Block A", "Block B", "Library", "Cafeteria", "Auditorium", "Parking", "Sports Ground", "Hostel", "Main Gate", "Laboratory"}


def parse_item_data(data):
    required = ("type", "name", "category", "description", "location", "date_lost_found")
    missing = [field for field in required if not str(data.get(field, "")).strip()]
    if missing:
        return None, ("INVALID_ITEM", f"Missing required fields: {', '.join(missing)}")
    item_type = str(data["type"]).strip().upper()
    if item_type not in ALLOWED_TYPES:
        return None, ("INVALID_ITEM", "Type must be LOST or FOUND.")
    location = str(data["location"]).strip()
    if location not in LOCATIONS:
        return None, ("INVALID_ITEM", "Choose a valid campus location.")
    try:
        item_date = date.fromisoformat(str(data["date_lost_found"]).strip())
        item_time = time.fromisoformat(str(data["time_lost_found"]).strip()) if data.get("time_lost_found") else None
    except ValueError:
        return None, ("INVALID_ITEM", "Use ISO date and time formats.")
    if len(str(data["name"]).strip()) > 160 or len(str(data["category"]).strip()) > 80:
        return None, ("INVALID_ITEM", "Name or category is too long.")
    return {
        "type": item_type,
        "name": str(data["name"]).strip(),
        "category": str(data["category"]).strip(),
        "description": str(data["description"]).strip(),
        "color": str(data.get("color", "")).strip() or None,
        "location": location,
        "date_lost_found": item_date,
        "time_lost_found": item_time,
        "private_verification_answer": str(data.get("private_verification_answer", "")).strip() or None,
    }, None


def create_item(user_id, data, files, upload_folder):
    values, error = parse_item_data(data)
    if error:
        return None, error
    if not files:
        return None, ("IMAGE_REQUIRED", "Upload at least one image.")
    item = Item(user_id=user_id, **values)
    db.session.add(item)
    try:
        for file_storage in files:
            image_path, image_error = save_validated_image(file_storage, upload_folder)
            if image_error:
                db.session.rollback()
                return None, image_error
            item.images.append(ItemImage(image_path=image_path))
        db.session.commit()
    except OSError:
        db.session.rollback()
        return None, ("IMAGE_STORAGE_ERROR", "The image could not be stored.")
    return item, None


def search_items(filters):
    query = db.select(Item).where(Item.status != "REMOVED").order_by(Item.created_at.desc())
    if filters.get("q"):
        query = query.where(func.lower(Item.name).contains(str(filters["q"]).lower()))
    for field in ("type", "category", "color", "location", "status"):
        if filters.get(field):
            query = query.where(getattr(Item, field) == str(filters[field]).strip().upper() if field == "type" else getattr(Item, field) == str(filters[field]).strip())
    if filters.get("date"):
        try:
            query = query.where(Item.date_lost_found == date.fromisoformat(filters["date"]))
        except ValueError:
            return None, ("INVALID_FILTER", "Date filter must use YYYY-MM-DD.")
    return db.session.scalars(query).all(), None

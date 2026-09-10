from datetime import date
from pathlib import Path

from PIL import Image

from backend.app import create_app
from backend.config import Config
from backend.extensions import db
from backend.models import Item, ItemImage, User
from backend.services.auth_service import register_user
from backend.services.matching_service import process_item_matches


def image_for(color, path):
    Image.new("RGB", (96, 96), color).save(path, format="PNG")


def get_or_create_user(data):
    user = db.session.scalar(db.select(User).where(User.college_email == data["college_email"]))
    if user:
        return user
    user, error = register_user(data)
    if error:
        raise RuntimeError(error[1])
    return user


def run_seed():
    app = create_app(Config)
    with app.app_context():
        db.create_all()
        upload_folder = Path(app.config["UPLOAD_FOLDER"])
        upload_folder.mkdir(parents=True, exist_ok=True)
        lost_user = get_or_create_user({"name": "Asha Rao", "college_email": "asha@campus.edu", "password": "demoPass123", "student_id": "DEMO-L001", "department": "Design"})
        found_user = get_or_create_user({"name": "Noah Chen", "college_email": "noah@campus.edu", "password": "demoPass123", "student_id": "DEMO-F001", "department": "Computing"})
        if not Item.query.filter_by(name="Blue canvas backpack").first():
            lost_path = upload_folder / "seed-lost.png"
            found_path = upload_folder / "seed-found.png"
            image_for("blue", lost_path)
            image_for("blue", found_path)
            lost = Item(user_id=lost_user.id, type="LOST", name="Blue canvas backpack", category="Bag", description="Blue canvas backpack with a stitched handle.", color="Blue", location="Library", date_lost_found=date(2026, 8, 20), private_verification_answer="Small astronomy patch")
            found = Item(user_id=found_user.id, type="FOUND", name="Blue canvas backpack", category="Bag", description="Blue backpack found near the reading room.", color="Blue", location="Library", date_lost_found=date(2026, 8, 20))
            lost.images.append(ItemImage(image_path=lost_path.name))
            found.images.append(ItemImage(image_path=found_path.name))
            db.session.add_all([lost, found])
            db.session.commit()
            process_item_matches(lost, upload_folder)
        print("Seed data ready. Demo password: demoPass123")


if __name__ == "__main__":
    run_seed()

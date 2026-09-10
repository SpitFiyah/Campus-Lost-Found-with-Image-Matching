from io import BytesIO

from PIL import Image

from backend.models.item import Item
from backend.services.matching_service import process_item_matches


def make_image(color):
    stream = BytesIO()
    Image.new("RGB", (20, 20), color).save(stream, format="PNG")
    stream.seek(0)
    return stream


def register_and_login(client, email, student_id):
    client.post("/api/auth/register", json={"name": email, "college_email": email, "password": "strongpass123", "student_id": student_id, "department": "Computing"})
    client.post("/api/auth/login", json={"college_email": email, "password": "strongpass123"})


def create_item(client, item_type, filename, stream):
    return client.post("/api/items", data={"type": item_type, "name": "Blue backpack", "category": "Bag", "description": "Canvas backpack", "color": "Blue", "location": "Library", "date_lost_found": "2026-08-20", "images": (stream, filename)}, content_type="multipart/form-data")


def test_matching_creates_ranked_match_and_notifications(client, app):
    register_and_login(client, "lost@campus.edu", "L001")
    lost_response = create_item(client, "LOST", "lost.png", make_image("blue"))
    lost_id = lost_response.get_json()["data"]["item"]["id"]
    client.post("/api/auth/logout")
    register_and_login(client, "found@campus.edu", "F001")
    found_response = create_item(client, "FOUND", "found.png", make_image("blue"))
    assert found_response.status_code == 201, found_response.get_json()

    with app.app_context():
        from backend.models.match import Match
        from backend.models.notification import Notification
        assert db_count(Match) == 1
        assert db_count(Notification) == 2
        assert Match.query.first().final_score > 90


def db_count(model):
    return model.query.count()

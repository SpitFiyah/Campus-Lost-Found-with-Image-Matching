import tempfile
from io import BytesIO
from pathlib import Path

from PIL import Image

from backend.extensions import db
from backend.matching.embedding import generate_embedding
from backend.matching.similarity import cosine_similarity
from backend.models.item import Item
from backend.models.match import Match
from backend.models.notification import Notification
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


def count(model):
    return db.session.scalar(db.select(db.func.count()).select_from(model))


def test_matching_creates_ranked_match_and_notifications(client, app):
    register_and_login(client, "lost@campus.edu", "L001")
    lost_response = create_item(client, "LOST", "lost.png", make_image("blue"))
    assert lost_response.status_code == 201, lost_response.get_json()
    client.post("/api/auth/logout")
    register_and_login(client, "found@campus.edu", "F001")
    found_response = create_item(client, "FOUND", "found.png", make_image("blue"))
    assert found_response.status_code == 201, found_response.get_json()

    with app.app_context():
        assert count(Match) == 1
        assert count(Notification) == 2
        match = db.session.scalar(db.select(Match))
        assert match.final_score > 90


def test_matching_does_not_create_duplicate_matches_on_reprocessing(client, app):
    register_and_login(client, "lostdup@campus.edu", "L002")
    lost_response = create_item(client, "LOST", "lost.png", make_image("purple"))
    lost_item_id = lost_response.get_json()["data"]["item"]["id"]
    client.post("/api/auth/logout")

    register_and_login(client, "founddup@campus.edu", "F002")
    create_item(client, "FOUND", "found.png", make_image("purple"))
    client.post("/api/auth/logout")

    with app.app_context():
        assert count(Match) == 1
        lost_item = db.session.get(Item, lost_item_id)
        process_item_matches(lost_item, app.config["UPLOAD_FOLDER"])
        assert count(Match) == 1


def embedding_for_color(color):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / f"{color}.png"
        Image.new("RGB", (40, 40), color).save(path, format="PNG")
        return generate_embedding(path)


def test_matching_scores_same_color_pair_higher_than_an_unrelated_color():
    """Minimal same-item-vs-unrelated-item evaluation (see docs/matching-algorithm.md)."""
    blue_a = embedding_for_color("blue")
    blue_b = embedding_for_color("blue")
    red = embedding_for_color("red")

    same_color_similarity = cosine_similarity(blue_a, blue_b)
    unrelated_similarity = cosine_similarity(blue_a, red)

    assert same_color_similarity > unrelated_similarity

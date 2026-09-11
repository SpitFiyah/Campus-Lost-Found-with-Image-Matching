from io import BytesIO

from PIL import Image


def register_and_login(client, email="uploader@campus.edu", student_id="UP1"):
    client.post(
        "/api/auth/register",
        json={"name": "Uploader", "college_email": email, "password": "strongpass123", "student_id": student_id, "department": "Computing"},
    )
    client.post("/api/auth/login", json={"college_email": email, "password": "strongpass123"})


def item_fields():
    return {
        "type": "LOST",
        "name": "Upload edge case item",
        "category": "Bag",
        "description": "A bag.",
        "color": "Grey",
        "location": "Library",
        "date_lost_found": "2026-08-20",
    }


def test_missing_image_field_is_rejected(client):
    register_and_login(client)
    response = client.post("/api/items", data=item_fields(), content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "IMAGE_REQUIRED"


def test_disallowed_extension_is_rejected(client):
    register_and_login(client)
    stream = BytesIO(b"not an image at all")
    response = client.post(
        "/api/items",
        data={**item_fields(), "images": (stream, "notes.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "INVALID_IMAGE"


def test_valid_image_in_an_unsupported_format_is_rejected(client):
    register_and_login(client)
    # A genuine, valid GIF - PIL can open it fine, but GIF isn't in the
    # supported extension/mimetype allowlist (JPG, PNG, WEBP only).
    stream = BytesIO()
    Image.new("RGB", (10, 10), "blue").save(stream, format="GIF")
    stream.seek(0)
    response = client.post(
        "/api/items",
        data={**item_fields(), "images": (stream, "photo.gif")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "INVALID_IMAGE"


def test_oversized_upload_is_rejected_with_413(client, app):
    register_and_login(client)
    oversized = BytesIO(b"0" * (app.config["MAX_CONTENT_LENGTH"] + 1024))
    response = client.post(
        "/api/items",
        data={**item_fields(), "images": (oversized, "big.png")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 413
    assert response.get_json()["error"]["code"] == "FILE_TOO_LARGE"

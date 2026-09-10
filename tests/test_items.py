from io import BytesIO

from PIL import Image


def image_file(color="red", filename="item.png", image_format="PNG"):
    stream = BytesIO()
    Image.new("RGB", (20, 20), color).save(stream, format=image_format)
    stream.seek(0)
    return stream, filename


def sign_in(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Item Owner",
            "college_email": "owner@campus.edu",
            "password": "strongpass123",
            "student_id": "S100",
            "department": "Computing",
        },
    )
    client.post("/api/auth/login", json={"college_email": "owner@campus.edu", "password": "strongpass123"})


def item_payload(stream, filename="item.png"):
    return {
        "type": "LOST",
        "name": "Red wallet",
        "category": "Wallet",
        "description": "Leather wallet",
        "color": "Red",
        "location": "Library",
        "date_lost_found": "2026-08-20",
        "private_verification_answer": "Blue stitch",
        "images": (stream, filename),
    }


def test_item_creation_validates_image_and_hides_private_answer(client):
    sign_in(client)
    stream, filename = image_file()

    response = client.post("/api/items", data=item_payload(stream, filename), content_type="multipart/form-data")

    assert response.status_code == 201, response.get_json()
    item = response.get_json()["data"]["item"]
    assert item["private_verification_answer"] == "Blue stitch"
    public_item = client.get(f"/api/items/{item['id']}").get_json()["data"]["item"]
    assert "private_verification_answer" not in public_item
    assert public_item["images"][0]["image_path"].endswith(".png")


def test_invalid_image_and_search_filter(client):
    sign_in(client)
    stream, _ = image_file()
    response = client.post(
        "/api/items",
        data={**item_payload(stream), "images": (BytesIO(b"not-an-image"), "item.png")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "INVALID_IMAGE"

    stream, filename = image_file()
    assert client.post("/api/items", data=item_payload(stream, filename), content_type="multipart/form-data").status_code == 201
    response = client.get("/api/items?type=LOST&location=Library")
    assert response.status_code == 200
    assert len(response.get_json()["data"]["items"]) == 1


def test_item_creation_requires_authentication(client):
    stream, filename = image_file()

    response = client.post("/api/items", data=item_payload(stream, filename), content_type="multipart/form-data")

    assert response.status_code == 401

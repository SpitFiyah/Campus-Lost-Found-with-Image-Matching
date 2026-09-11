from io import BytesIO

from PIL import Image


def register_and_login(client, email, student_id):
    client.post(
        "/api/auth/register",
        json={"name": email, "college_email": email, "password": "strongpass123", "student_id": student_id, "department": "Computing"},
    )
    client.post("/api/auth/login", json={"college_email": email, "password": "strongpass123"})


def create_item(client, item_type, color="teal"):
    stream = BytesIO()
    Image.new("RGB", (20, 20), color).save(stream, format="PNG")
    stream.seek(0)
    return client.post(
        "/api/items",
        data={
            "type": item_type,
            "name": "Notification test item",
            "category": "Bag",
            "description": "A bag.",
            "color": "Teal",
            "location": "Library",
            "date_lost_found": "2026-08-20",
            "images": (stream, "item.png"),
        },
        content_type="multipart/form-data",
    )


def test_notifications_require_authentication(client):
    assert client.get("/api/notifications").status_code == 401


def test_matching_creates_unread_notification_that_can_be_marked_read(client):
    register_and_login(client, "notiflost@campus.edu", "NL1")
    create_item(client, "LOST")
    client.post("/api/auth/logout")

    register_and_login(client, "notiffound@campus.edu", "NF1")
    create_item(client, "FOUND")
    client.post("/api/auth/logout")

    register_and_login(client, "notiflost@campus.edu", "NL1")
    listed = client.get("/api/notifications").get_json()["data"]
    assert listed["unread_count"] == 1
    notification_id = listed["notifications"][0]["id"]
    assert listed["notifications"][0]["is_read"] is False

    marked = client.put(f"/api/notifications/{notification_id}/read")
    assert marked.status_code == 200
    assert marked.get_json()["data"]["notification"]["is_read"] is True

    listed_again = client.get("/api/notifications").get_json()["data"]
    assert listed_again["unread_count"] == 0

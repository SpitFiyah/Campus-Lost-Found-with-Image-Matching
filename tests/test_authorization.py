from io import BytesIO

from PIL import Image


def image_file(color="green", filename="item.png"):
    stream = BytesIO()
    Image.new("RGB", (20, 20), color).save(stream, format="PNG")
    stream.seek(0)
    return stream, filename


def register_and_login(client, email, student_id, name="Test User"):
    client.post(
        "/api/auth/register",
        json={"name": name, "college_email": email, "password": "strongpass123", "student_id": student_id, "department": "Computing"},
    )
    client.post("/api/auth/login", json={"college_email": email, "password": "strongpass123"})


def create_item(client, item_type="LOST", name="Owner's item"):
    stream, filename = image_file()
    response = client.post(
        "/api/items",
        data={
            "type": item_type,
            "name": name,
            "category": "Bag",
            "description": "A bag.",
            "color": "Green",
            "location": "Library",
            "date_lost_found": "2026-08-20",
            "images": (stream, filename),
        },
        content_type="multipart/form-data",
    )
    return response.get_json()["data"]["item"]


def test_user_cannot_edit_another_users_item(client):
    register_and_login(client, "owner@campus.edu", "OWN1")
    item = create_item(client)
    client.post("/api/auth/logout")

    register_and_login(client, "intruder@campus.edu", "INT1")
    response = client.put(f"/api/items/{item['id']}", data={"name": "Hijacked name"})

    assert response.status_code == 403
    assert response.get_json()["error"]["code"] == "FORBIDDEN"


def test_user_cannot_delete_another_users_item(client):
    register_and_login(client, "owner2@campus.edu", "OWN2")
    item = create_item(client)
    client.post("/api/auth/logout")

    register_and_login(client, "intruder2@campus.edu", "INT2")
    response = client.delete(f"/api/items/{item['id']}")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "ITEM_NOT_FOUND"


def test_user_cannot_act_on_a_match_they_are_not_part_of(client):
    register_and_login(client, "lostowner@campus.edu", "L100")
    lost_item = create_item(client, "LOST", "Lost item")
    client.post("/api/auth/logout")

    register_and_login(client, "foundowner@campus.edu", "F100")
    create_item(client, "FOUND", "Found item")
    client.post("/api/auth/logout")

    register_and_login(client, "bystander@campus.edu", "BY100")
    matches = client.get(f"/api/items/{lost_item['id']}/matches")
    assert matches.status_code == 403

    register_and_login(client, "lostowner@campus.edu", "L100")
    matches = client.get(f"/api/items/{lost_item['id']}/matches")
    match_id = matches.get_json()["data"]["matches"][0]["id"]
    client.post("/api/auth/logout")

    register_and_login(client, "bystander@campus.edu", "BY100")
    response = client.post(f"/api/matches/{match_id}/accept")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "MATCH_NOT_FOUND"


def test_message_about_item_requires_sender_or_receiver_to_own_it(client):
    register_and_login(client, "itemowner@campus.edu", "OWN3")
    item = create_item(client)
    client.post("/api/auth/logout")

    register_and_login(client, "sender@campus.edu", "SEND1")
    client.post("/api/auth/logout")

    register_and_login(client, "unrelated@campus.edu", "UNREL1")
    response = client.post(
        "/api/messages",
        json={"item_id": item["id"], "receiver_id": 999999, "message": "This should not be allowed."},
    )

    assert response.status_code == 403
    assert response.get_json()["error"]["code"] == "FORBIDDEN"


def test_user_cannot_mark_another_users_notification_read(client):
    register_and_login(client, "notifowner@campus.edu", "NOT1")
    lost_item = create_item(client, "LOST", "Notif lost item")
    client.post("/api/auth/logout")

    register_and_login(client, "notiffinder@campus.edu", "NOT2")
    create_item(client, "FOUND", "Notif found item")
    notifications = client.get("/api/notifications").get_json()["data"]["notifications"]
    notification_id = notifications[0]["id"]
    client.post("/api/auth/logout")

    register_and_login(client, "notifintruder@campus.edu", "NOT3")
    response = client.put(f"/api/notifications/{notification_id}/read")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"

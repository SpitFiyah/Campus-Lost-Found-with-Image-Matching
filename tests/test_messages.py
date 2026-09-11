def register_and_login(client, email, student_id, name):
    client.post(
        "/api/auth/register",
        json={"name": name, "college_email": email, "password": "strongpass123", "student_id": student_id, "department": "Computing"},
    )
    client.post("/api/auth/login", json={"college_email": email, "password": "strongpass123"})


def test_send_and_list_messages_between_two_users(client):
    register_and_login(client, "alice@campus.edu", "MSG1", "Alice")
    client.post("/api/auth/logout")
    register_and_login(client, "bob@campus.edu", "MSG2", "Bob")
    bob_id = client.get("/api/auth/me").get_json()["data"]["user"]["id"]
    client.post("/api/auth/logout")

    register_and_login(client, "alice@campus.edu", "MSG1", "Alice")
    response = client.post("/api/messages", json={"receiver_id": bob_id, "message": "Hi Bob, is this your bag?"})

    assert response.status_code == 201
    sent = response.get_json()["data"]["message"]
    assert sent["sender_name"] == "Alice"
    assert sent["receiver_name"] == "Bob"

    listed = client.get("/api/messages").get_json()["data"]["messages"]
    assert len(listed) == 1
    assert listed[0]["message"] == "Hi Bob, is this your bag?"


def test_message_requires_receiver_and_nonempty_text(client):
    register_and_login(client, "carol@campus.edu", "MSG3", "Carol")

    missing_receiver = client.post("/api/messages", json={"message": "hello"})
    assert missing_receiver.status_code == 400
    assert missing_receiver.get_json()["error"]["code"] == "INVALID_MESSAGE"

    empty_message = client.post("/api/messages", json={"receiver_id": 1, "message": "   "})
    assert empty_message.status_code == 400


def test_messages_require_authentication(client):
    response = client.get("/api/messages")
    assert response.status_code == 401

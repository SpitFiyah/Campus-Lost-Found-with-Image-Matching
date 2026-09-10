def registration_payload(email="student@campus.edu", student_id="S001"):
    return {
        "name": "Test Student",
        "college_email": email,
        "password": "strongpass123",
        "student_id": student_id,
        "department": "Computing",
    }


def test_registration_hashes_password_and_returns_public_user(client, app):
    response = client.post("/api/auth/register", json=registration_payload())

    assert response.status_code == 201
    user = response.get_json()["data"]["user"]
    assert user["college_email"] == "student@campus.edu"
    assert "password_hash" not in user


def test_duplicate_registration_is_rejected(client):
    payload = registration_payload()
    assert client.post("/api/auth/register", json=payload).status_code == 201

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 409
    assert response.get_json()["error"]["code"] == "DUPLICATE_USER"


def test_login_profile_update_and_logout(client):
    client.post("/api/auth/register", json=registration_payload())

    response = client.post(
        "/api/auth/login",
        json={"college_email": "STUDENT@CAMPUS.EDU", "password": "strongpass123"},
    )
    assert response.status_code == 200
    assert client.get("/api/auth/me").status_code == 200
    assert client.put("/api/auth/profile", json={"phone": "555-0100"}).status_code == 200

    assert client.post("/api/auth/logout").status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_protected_and_admin_routes_enforce_authorization(client):
    assert client.get("/api/auth/me").status_code == 401
    client.post("/api/auth/register", json=registration_payload())
    client.post(
        "/api/auth/login",
        json={"college_email": "student@campus.edu", "password": "strongpass123"},
    )

    response = client.get("/api/admin/access-check")

    assert response.status_code == 403
    assert response.get_json()["error"]["code"] == "FORBIDDEN"

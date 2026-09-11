from io import BytesIO

from PIL import Image


def register_and_login(client, email, student_id):
    client.post(
        "/api/auth/register",
        json={"name": email, "college_email": email, "password": "strongpass123", "student_id": student_id, "department": "Computing"},
    )
    client.post("/api/auth/login", json={"college_email": email, "password": "strongpass123"})


def make_admin(app, email):
    from backend.extensions import db
    from backend.models.user import User

    with app.app_context():
        user = db.session.scalar(db.select(User).where(User.college_email == email))
        user.role = "ADMIN"
        db.session.commit()


def create_item(client):
    stream = BytesIO()
    Image.new("RGB", (20, 20), "orange").save(stream, format="PNG")
    stream.seek(0)
    return client.post(
        "/api/items",
        data={
            "type": "LOST",
            "name": "Admin test item",
            "category": "Bag",
            "description": "A bag.",
            "color": "Orange",
            "location": "Library",
            "date_lost_found": "2026-08-20",
            "images": (stream, "item.png"),
        },
        content_type="multipart/form-data",
    ).get_json()["data"]["item"]


def test_admin_routes_require_admin_role(client):
    register_and_login(client, "plainstudent@campus.edu", "PLAIN1")
    for path in ("/api/admin/users", "/api/admin/items", "/api/admin/reports", "/api/admin/statistics"):
        assert client.get(path).status_code == 403


def test_admin_can_list_users_items_and_statistics(client, app):
    register_and_login(client, "student@campus.edu", "STU1")
    create_item(client)
    client.post("/api/auth/logout")

    register_and_login(client, "admin@campus.edu", "ADM1")
    make_admin(app, "admin@campus.edu")
    client.post("/api/auth/logout")
    register_and_login(client, "admin@campus.edu", "ADM1")

    users = client.get("/api/admin/users").get_json()["data"]["users"]
    assert any(user["college_email"] == "student@campus.edu" for user in users)

    items = client.get("/api/admin/items").get_json()["data"]["items"]
    assert any(item["name"] == "Admin test item" for item in items)

    stats = client.get("/api/admin/statistics").get_json()["data"]
    assert stats["total_items"] >= 1
    assert stats["total_users"] >= 2
    assert isinstance(stats["hotspots"], list)
    assert isinstance(stats["categories"], list)


def test_admin_can_review_flagged_reports(client, app):
    register_and_login(client, "reporteditem@campus.edu", "RPT1")
    item = create_item(client)
    client.post("/api/auth/logout")

    register_and_login(client, "flagger@campus.edu", "FLG1")
    flag = client.post(f"/api/items/{item['id']}/report", json={"reason": "Suspected fraud"})
    assert flag.status_code == 201
    client.post("/api/auth/logout")

    register_and_login(client, "reportadmin@campus.edu", "ADM2")
    make_admin(app, "reportadmin@campus.edu")
    client.post("/api/auth/logout")
    register_and_login(client, "reportadmin@campus.edu", "ADM2")

    reports = client.get("/api/admin/reports").get_json()["data"]["reports"]
    assert len(reports) == 1
    assert reports[0]["item_name"] == "Admin test item"
    assert reports[0]["reporter_name"] == "flagger@campus.edu"
    report_id = reports[0]["id"]

    updated = client.put(f"/api/admin/reports/{report_id}", json={"status": "REVIEWED"})
    assert updated.status_code == 200
    assert updated.get_json()["data"]["report"]["status"] == "REVIEWED"

    invalid = client.put(f"/api/admin/reports/{report_id}", json={"status": "NOT_A_REAL_STATUS"})
    assert invalid.status_code == 400
    assert invalid.get_json()["error"]["code"] == "INVALID_STATUS"

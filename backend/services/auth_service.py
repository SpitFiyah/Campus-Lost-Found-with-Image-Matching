import re

from sqlalchemy import or_

from backend.extensions import db
from backend.models.user import User


COLLEGE_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_registration(data):
    required_fields = ("name", "college_email", "password", "student_id", "department")
    missing_fields = [field for field in required_fields if not str(data.get(field, "")).strip()]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"

    email = str(data["college_email"]).strip().lower()
    if not COLLEGE_EMAIL_PATTERN.fullmatch(email):
        return "Enter a valid college email address."
    if len(data["password"]) < 8:
        return "Password must be at least 8 characters long."
    if len(str(data["name"]).strip()) > 120 or len(str(data["department"]).strip()) > 120:
        return "Name and department must be 120 characters or fewer."
    if len(str(data["student_id"]).strip()) > 50:
        return "Student ID must be 50 characters or fewer."
    return None


def register_user(data):
    validation_error = validate_registration(data)
    if validation_error:
        return None, ("INVALID_REGISTRATION", validation_error)

    email = str(data["college_email"]).strip().lower()
    student_id = str(data["student_id"]).strip()
    existing_user = db.session.scalar(
        db.select(User).where(or_(User.college_email == email, User.student_id == student_id))
    )
    if existing_user:
        return None, ("DUPLICATE_USER", "College email or student ID is already registered.")

    user = User(
        name=str(data["name"]).strip(),
        college_email=email,
        student_id=student_id,
        department=str(data["department"]).strip(),
        phone=str(data.get("phone", "")).strip() or None,
        role="STUDENT",
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user, None


def authenticate_user(email, password):
    normalized_email = str(email or "").strip().lower()
    user = db.session.scalar(db.select(User).where(User.college_email == normalized_email))
    if not user or not user.check_password(password or ""):
        return None
    return user


def update_profile(user, data):
    allowed_fields = ("name", "department", "phone")
    for field in allowed_fields:
        if field in data:
            value = str(data[field]).strip()
            if not value and field != "phone":
                return None, ("INVALID_PROFILE", f"{field.replace('_', ' ').capitalize()} cannot be empty.")
            if field in ("name", "department") and len(value) > 120:
                return None, ("INVALID_PROFILE", f"{field.replace('_', ' ').capitalize()} is too long.")
            user.__setattr__(field, value or None)
    db.session.commit()
    return user, None

import logging

from flask import Blueprint, g, jsonify, request, session
from sqlalchemy.exc import IntegrityError

from backend.extensions import db
from backend.services.auth_service import authenticate_user, register_user, update_profile
from backend.utils.auth import login_required, load_current_user

logger = logging.getLogger(__name__)


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def error_response(code, message, status):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    try:
        user, error = register_user(data)
    except IntegrityError:
        db.session.rollback()
        return error_response("DUPLICATE_USER", "College email or student ID is already registered.", 409)
    if error:
        status = 409 if error[0] == "DUPLICATE_USER" else 400
        return error_response(error[0], error[1], status)
    return jsonify({"success": True, "data": {"user": user.to_public_dict()}, "message": "Account created successfully."}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if not data.get("college_email") or not data.get("password"):
        return error_response("INVALID_LOGIN", "College email and password are required.", 400)
    user = authenticate_user(data["college_email"], data["password"])
    if user is None:
        logger.warning("Failed login attempt for %s", data["college_email"])
        return error_response("INVALID_LOGIN", "Invalid college email or password.", 401)
    session.clear()
    session["user_id"] = user.id
    return jsonify({"success": True, "data": {"user": user.to_public_dict()}, "message": "Signed in successfully."})


@auth_bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"success": True, "data": {}, "message": "Signed out successfully."})


@auth_bp.get("/me")
@login_required
def current_user():
    return jsonify({"success": True, "data": {"user": g.current_user.to_public_dict()}, "message": "Current user loaded."})


@auth_bp.get("/profile")
@login_required
def profile():
    return jsonify({"success": True, "data": {"user": g.current_user.to_public_dict()}, "message": "Profile loaded."})


@auth_bp.put("/profile")
@login_required
def update_current_profile():
    data = request.get_json(silent=True) or {}
    user, error = update_profile(g.current_user, data)
    if error:
        return error_response(error[0], error[1], 400)
    return jsonify({"success": True, "data": {"user": user.to_public_dict()}, "message": "Profile updated successfully."})


@auth_bp.get("/session")
def session_status():
    user = load_current_user()
    return jsonify({"success": True, "data": {"authenticated": user is not None, "user": user.to_public_dict() if user else None}, "message": "Session status loaded."})
